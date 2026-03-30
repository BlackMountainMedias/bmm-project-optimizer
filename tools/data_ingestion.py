"""Upload type definitions, fuzzy column matching, data validation, and CSV template generation."""
import io
import pandas as pd
from difflib import SequenceMatcher

# ---------------------------------------------------------------------------
# Upload type definitions
# ---------------------------------------------------------------------------
UPLOAD_TYPES = {
    "Budget / Bid": {
        "description": "Original bid or budget with line-item cost breakdown",
        "required_mappings": {
            "project_name": "Project name or job number",
            "phase": "Construction phase (e.g. Sitework, Structural)",
            "cost_category": "Cost type (Labor, Materials, Equipment, Subcontractor)",
            "line_item": "Specific line item description",
            "budgeted_amount": "Budgeted dollar amount",
        },
        "optional_mappings": {
            "contingency_pct": "Contingency percentage",
            "bid_date": "Date the bid was submitted",
            "notes": "Additional notes",
        },
    },
    "Actuals / Costs": {
        "description": "Actual costs incurred — invoices, cost reports, job cost exports",
        "required_mappings": {
            "project_name": "Project name or job number",
            "phase": "Construction phase",
            "cost_category": "Cost type",
            "line_item": "Specific line item description",
            "actual_amount": "Actual dollar amount spent",
        },
        "optional_mappings": {
            "invoice_date": "Date of invoice or cost entry",
            "vendor": "Vendor or subcontractor name",
            "po_number": "Purchase order number",
            "notes": "Additional notes",
        },
    },
    "Change Orders": {
        "description": "Approved or pending change orders with cost and schedule impact",
        "required_mappings": {
            "project_name": "Project name or job number",
            "co_number": "Change order number",
            "description": "Description of the change",
            "cost_impact": "Dollar impact of the change",
        },
        "optional_mappings": {
            "phase": "Affected phase",
            "status": "Status (Pending, Approved, Rejected)",
            "schedule_impact_days": "Schedule impact in days",
            "date_submitted": "Date submitted",
            "date_approved": "Date approved",
            "requested_by": "Who requested the change",
            "notes": "Additional notes",
        },
    },
    "Timecards / Timesheets": {
        "description": "Crew or worker timecards with hours and rates",
        "required_mappings": {
            "project_name": "Project name or job number",
            "worker_name": "Worker or crew member name",
            "date": "Date of work",
            "hours": "Hours worked",
        },
        "optional_mappings": {
            "phase": "Construction phase",
            "hourly_rate": "Pay rate per hour",
            "overtime_hours": "Overtime hours",
            "cost_code": "Cost code",
            "crew": "Crew name or number",
            "notes": "Additional notes",
        },
    },
    "Material Orders & Deliveries": {
        "description": "Material purchase orders and delivery tracking",
        "required_mappings": {
            "project_name": "Project name or job number",
            "material": "Material description",
            "quantity": "Quantity ordered",
            "unit_cost": "Cost per unit",
        },
        "optional_mappings": {
            "phase": "Construction phase",
            "vendor": "Supplier / vendor",
            "po_number": "Purchase order number",
            "order_date": "Date ordered",
            "delivery_date": "Expected or actual delivery date",
            "status": "Status (Ordered, Delivered, Backordered)",
            "total_cost": "Total cost (qty × unit cost)",
            "notes": "Additional notes",
        },
    },
    "Project Schedule": {
        "description": "Milestones, phases, and planned dates for schedule tracking",
        "required_mappings": {
            "project_name": "Project name or job number",
            "task_name": "Task or milestone name",
            "planned_start": "Planned start date",
            "planned_end": "Planned end date",
        },
        "optional_mappings": {
            "phase": "Construction phase",
            "actual_start": "Actual start date",
            "actual_end": "Actual end date",
            "pct_complete": "Percent complete",
            "predecessor": "Predecessor task",
            "notes": "Additional notes",
        },
    },
}

# ---------------------------------------------------------------------------
# Fuzzy column matching
# ---------------------------------------------------------------------------
# Common aliases that map messy real-world column names to internal fields
_ALIASES = {
    "project_name": ["project", "project name", "job", "job name", "job number", "job #", "job no", "project id", "proj"],
    "phase": ["phase", "construction phase", "work phase", "division"],
    "cost_category": ["cost category", "category", "cost type", "type", "cost code type"],
    "line_item": ["line item", "description", "item", "line", "detail", "cost item", "work item"],
    "budgeted_amount": ["budget", "budgeted", "budgeted amount", "bid amount", "bid", "estimated cost", "est cost", "original budget"],
    "actual_amount": ["actual", "actuals", "actual amount", "actual cost", "cost", "spent", "total cost", "invoice amount"],
    "cost_impact": ["cost impact", "amount", "change amount", "co amount", "delta", "cost change"],
    "co_number": ["co number", "co #", "co no", "change order", "change order number", "co id"],
    "worker_name": ["worker", "employee", "name", "crew member", "worker name", "employee name"],
    "date": ["date", "work date", "shift date", "day"],
    "hours": ["hours", "hrs", "hours worked", "reg hours", "regular hours", "total hours"],
    "hourly_rate": ["rate", "hourly rate", "pay rate", "pay rate ($/hr)", "wage", "hr rate"],
    "material": ["material", "item", "product", "description", "material description"],
    "quantity": ["quantity", "qty", "amount", "units", "count"],
    "unit_cost": ["unit cost", "unit price", "price", "cost per unit", "rate", "$/unit"],
    "task_name": ["task", "milestone", "activity", "task name", "milestone name"],
    "planned_start": ["planned start", "start date", "plan start", "baseline start", "early start"],
    "planned_end": ["planned end", "end date", "plan end", "plan finish", "baseline finish", "early finish"],
    "vendor": ["vendor", "supplier", "sub", "subcontractor"],
}


def _similarity(a, b):
    """Simple string similarity ratio."""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def get_column_suggestions(file_columns, required_mappings, optional_mappings=None):
    """For each internal field, suggest the best matching column from the uploaded file.

    Returns dict of {internal_field: suggested_column_or_None}.
    """
    all_mappings = dict(required_mappings)
    if optional_mappings:
        all_mappings.update(optional_mappings)

    file_cols_lower = {c.lower().strip(): c for c in file_columns}
    suggestions = {}

    for field in all_mappings:
        best_score = 0.0
        best_col = None

        # Check exact match first
        if field in file_cols_lower:
            suggestions[field] = file_cols_lower[field]
            continue

        # Check aliases
        aliases = _ALIASES.get(field, [])
        for alias in aliases:
            if alias in file_cols_lower:
                suggestions[field] = file_cols_lower[alias]
                best_score = 1.0
                best_col = file_cols_lower[alias]
                break

        if best_score >= 1.0:
            continue

        # Fuzzy match against all file columns
        for fc_lower, fc_original in file_cols_lower.items():
            # Match against field name
            score = _similarity(field, fc_lower)
            if score > best_score:
                best_score = score
                best_col = fc_original

            # Match against aliases
            for alias in aliases:
                score = _similarity(alias, fc_lower)
                if score > best_score:
                    best_score = score
                    best_col = fc_original

        if best_score >= 0.55:
            suggestions[field] = best_col
        else:
            suggestions[field] = None

    return suggestions


# ---------------------------------------------------------------------------
# Data quality validation
# ---------------------------------------------------------------------------
def validate_data(df, upload_type, column_map):
    """Run quality checks on the mapped data. Returns (score, issues).

    Each issue is a dict with keys: severity ('error'|'warning'), message, count.
    """
    issues = []
    total_checks = 0
    passed_checks = 0

    # Build the mapped dataframe
    mapped = pd.DataFrame()
    for internal_field, file_col in column_map.items():
        if file_col and file_col in df.columns:
            mapped[internal_field] = df[file_col]

    if mapped.empty:
        return 0, [{"severity": "error", "message": "No columns mapped", "count": 0}]

    # --- Check: missing required fields ---
    type_def = UPLOAD_TYPES[upload_type]
    for field in type_def["required_mappings"]:
        total_checks += 1
        col = column_map.get(field)
        if not col or col not in df.columns:
            issues.append({"severity": "error", "message": f"Required field '{field}' is not mapped", "count": 1})
        else:
            missing = df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum()
            if missing > 0:
                issues.append({"severity": "warning", "message": f"'{field}' has {missing} blank/missing values", "count": int(missing)})
                if missing < len(df) * 0.5:
                    passed_checks += 1
            else:
                passed_checks += 1

    # --- Check: numeric fields for impossible values ---
    numeric_fields = {
        "budgeted_amount": {"min": 0, "max": 500_000_000, "label": "Budget amounts"},
        "actual_amount": {"min": 0, "max": 500_000_000, "label": "Actual amounts"},
        "cost_impact": {"min": -100_000_000, "max": 100_000_000, "label": "Cost impact"},
        "hours": {"min": 0, "max": 24, "label": "Hours"},
        "hourly_rate": {"min": 0, "max": 500, "label": "Hourly rate"},
        "quantity": {"min": 0, "max": 1_000_000, "label": "Quantity"},
        "unit_cost": {"min": 0, "max": 1_000_000, "label": "Unit cost"},
    }

    for field, rules in numeric_fields.items():
        col = column_map.get(field)
        if col and col in df.columns:
            total_checks += 1
            vals = pd.to_numeric(df[col], errors="coerce")
            non_numeric = vals.isna().sum() - df[col].isna().sum()
            if non_numeric > 0:
                issues.append({"severity": "error", "message": f"{rules['label']}: {non_numeric} non-numeric values", "count": int(non_numeric)})
            else:
                passed_checks += 0.5  # partial credit

            below = (vals < rules["min"]).sum()
            above = (vals > rules["max"]).sum()
            if below > 0:
                issues.append({"severity": "warning", "message": f"{rules['label']}: {below} values below {rules['min']}", "count": int(below)})
            elif above > 0:
                issues.append({"severity": "warning", "message": f"{rules['label']}: {above} values above {rules['max']:,.0f}", "count": int(above)})
            else:
                passed_checks += 0.5

    # --- Check: date fields for future dates ---
    date_fields = ["date", "bid_date", "invoice_date", "order_date", "delivery_date",
                    "date_submitted", "date_approved", "planned_start", "planned_end",
                    "actual_start", "actual_end"]
    for field in date_fields:
        col = column_map.get(field)
        if col and col in df.columns:
            total_checks += 1
            try:
                dates = pd.to_datetime(df[col], errors="coerce")
                future = (dates > pd.Timestamp.now() + pd.Timedelta(days=365)).sum()
                if future > 0:
                    issues.append({"severity": "warning", "message": f"'{field}': {future} dates more than 1 year in the future", "count": int(future)})
                else:
                    passed_checks += 1
            except Exception:
                passed_checks += 1

    # --- Check: duplicate rows ---
    total_checks += 1
    dupes = df.duplicated().sum()
    if dupes > 0:
        issues.append({"severity": "warning", "message": f"{dupes} fully duplicate rows", "count": int(dupes)})
    else:
        passed_checks += 1

    # Calculate score
    score = int((passed_checks / max(total_checks, 1)) * 100)
    score = max(0, min(100, score))

    return score, issues


# ---------------------------------------------------------------------------
# CSV template generation
# ---------------------------------------------------------------------------
def generate_template_csv(upload_type):
    """Generate a CSV template (as bytes) with correct headers and 2 sample rows."""
    type_def = UPLOAD_TYPES[upload_type]
    all_fields = list(type_def["required_mappings"].keys())
    if type_def.get("optional_mappings"):
        all_fields += list(type_def["optional_mappings"].keys())

    # Sample data per upload type
    samples = {
        "Budget / Bid": [
            {"project_name": "Sample Project A", "phase": "Sitework", "cost_category": "Labor",
             "line_item": "Excavation & Grading", "budgeted_amount": 175000},
            {"project_name": "Sample Project A", "phase": "Structural", "cost_category": "Materials",
             "line_item": "Ready-Mix Concrete", "budgeted_amount": 280000},
        ],
        "Actuals / Costs": [
            {"project_name": "Sample Project A", "phase": "Sitework", "cost_category": "Labor",
             "line_item": "Excavation & Grading", "actual_amount": 182000},
            {"project_name": "Sample Project A", "phase": "Structural", "cost_category": "Materials",
             "line_item": "Ready-Mix Concrete", "actual_amount": 295000},
        ],
        "Change Orders": [
            {"project_name": "Sample Project A", "co_number": "CO-001",
             "description": "Additional foundation work due to soil conditions", "cost_impact": 45000},
            {"project_name": "Sample Project A", "co_number": "CO-002",
             "description": "Owner-requested finish upgrade", "cost_impact": 22000},
        ],
        "Timecards / Timesheets": [
            {"project_name": "Sample Project A", "worker_name": "John Smith",
             "date": "2026-03-01", "hours": 8},
            {"project_name": "Sample Project A", "worker_name": "Jane Doe",
             "date": "2026-03-01", "hours": 10},
        ],
        "Material Orders & Deliveries": [
            {"project_name": "Sample Project A", "material": "Structural Steel I-Beams",
             "quantity": 50, "unit_cost": 1200},
            {"project_name": "Sample Project A", "material": "Ready-Mix Concrete (CY)",
             "quantity": 200, "unit_cost": 165},
        ],
        "Project Schedule": [
            {"project_name": "Sample Project A", "task_name": "Foundation Work",
             "planned_start": "2026-04-01", "planned_end": "2026-05-15"},
            {"project_name": "Sample Project A", "task_name": "Steel Erection",
             "planned_start": "2026-05-16", "planned_end": "2026-07-30"},
        ],
    }

    rows = samples.get(upload_type, [])
    template_df = pd.DataFrame(rows)

    # Ensure all fields are present as columns
    for field in all_fields:
        if field not in template_df.columns:
            template_df[field] = ""

    template_df = template_df[all_fields]

    buf = io.BytesIO()
    template_df.to_csv(buf, index=False)
    return buf.getvalue()

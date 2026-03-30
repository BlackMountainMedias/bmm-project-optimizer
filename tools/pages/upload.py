"""Data Upload page."""
import streamlit as st
import pandas as pd
from data_loader import BUDGET_COLS, ACTUALS_COLS
from data_ingestion import UPLOAD_TYPES, get_column_suggestions, validate_data, generate_template_csv


def render():
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h1 style="font-size: 32px; margin-bottom: 4px;">Data Upload</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Import your project data — budget, actuals, change orders, timecards, and more
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Previously uploaded data summary ---
    if "uploaded_data" in st.session_state and st.session_state.uploaded_data:
        st.markdown('<div class="section-header">Previously Uploaded Data</div>', unsafe_allow_html=True)
        for utype, udata in st.session_state.uploaded_data.items():
            udf = udata["df"]
            with st.expander(f"**{utype}** — {len(udf):,} records", expanded=False):
                st.dataframe(udf.head(20), use_container_width=True, hide_index=True)
        if st.button("Clear All Uploaded Data", type="secondary"):
            st.session_state.uploaded_data = {}
            st.rerun()
        st.markdown("---")

    # --- Two-column layout: upload form | templates ---
    up_left, up_right = st.columns([1.4, 1], gap="large")

    with up_right:
        st.markdown('<div class="section-header">CSV Templates</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 13px; margin-bottom: 16px;">Download a pre-formatted template for each data type, fill it in, and upload on the left.</p>', unsafe_allow_html=True)
        for tname in UPLOAD_TYPES:
            tdata = generate_template_csv(tname)
            safe_name = tname.lower().replace(" ", "_").replace("/", "").replace("&", "and")
            st.download_button(
                label=f"Download {tname} Template",
                data=tdata,
                file_name=f"bmm_template_{safe_name}.csv",
                mime="text/csv",
                key=f"tmpl_{safe_name}",
                use_container_width=True,
            )

    with up_left:
        st.markdown('<div class="section-header">Upload Data</div>', unsafe_allow_html=True)

        # Step 1: Select upload type
        type_names = list(UPLOAD_TYPES.keys())
        upload_type = st.selectbox("Upload Type", type_names, key="upload_type_select")
        type_def = UPLOAD_TYPES[upload_type]
        st.caption(type_def["description"])

        # Step 2: File uploader
        uploaded_file = st.file_uploader(
            "Upload file", type=["csv", "xlsx"], key="file_uploader",
            help="Drag and drop or click to browse. Supports CSV and XLSX."
        )

        if uploaded_file is not None:
            # Parse the file
            try:
                if uploaded_file.name.endswith(".xlsx"):
                    raw_df = pd.read_excel(uploaded_file)
                else:
                    raw_df = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Could not read file: {e}")
                st.stop()

            # Step 3: File preview
            st.markdown("#### File Preview")
            st.caption(f"{len(raw_df):,} rows × {len(raw_df.columns)} columns")
            st.dataframe(raw_df.head(10), use_container_width=True, hide_index=True)

            st.markdown("---")

            # Step 4: Column mapper with fuzzy suggestions
            st.markdown("#### Column Mapping")
            st.caption("Map your file's columns to the required fields. We auto-suggest matches.")

            suggestions = get_column_suggestions(
                raw_df.columns.tolist(),
                type_def["required_mappings"],
                type_def.get("optional_mappings"),
            )

            file_col_options = ["-- Skip (don't map) --"] + list(raw_df.columns)
            column_map = {}

            # Required fields
            req_cols = st.columns(2)
            for i, (field, desc) in enumerate(type_def["required_mappings"].items()):
                col = req_cols[i % 2]
                suggested = suggestions.get(field)
                default_idx = file_col_options.index(suggested) if suggested and suggested in file_col_options else 0
                chosen = col.selectbox(
                    f"{field} *",
                    file_col_options,
                    index=default_idx,
                    help=desc,
                    key=f"map_{field}",
                )
                column_map[field] = None if chosen == "-- Skip (don't map) --" else chosen

            # Optional fields
            if type_def.get("optional_mappings"):
                with st.expander("Optional Fields", expanded=False):
                    opt_cols = st.columns(2)
                    for i, (field, desc) in enumerate(type_def["optional_mappings"].items()):
                        col = opt_cols[i % 2]
                        suggested = suggestions.get(field)
                        default_idx = file_col_options.index(suggested) if suggested and suggested in file_col_options else 0
                        chosen = col.selectbox(
                            field,
                            file_col_options,
                            index=default_idx,
                            help=desc,
                            key=f"map_{field}",
                        )
                        column_map[field] = None if chosen == "-- Skip (don't map) --" else chosen

            st.markdown("---")

            # Step 5: Data quality score
            st.markdown("#### Data Quality")
            score, issues = validate_data(raw_df, upload_type, column_map)

            if score >= 90:
                score_color = "#22c55e"
                score_label = "Excellent"
            elif score >= 70:
                score_color = "#f59e0b"
                score_label = "Fair — review warnings below"
            else:
                score_color = "#ef4444"
                score_label = "Poor — fix errors before importing"

            st.markdown(f"""
            <div style="background: #111827; border: 1px solid #1e293b; border-radius: 12px;
                        padding: 20px; display: flex; align-items: center; gap: 20px; margin-bottom: 16px;">
                <div style="font-size: 48px; font-weight: 800; color: {score_color}; line-height: 1;">{score}</div>
                <div>
                    <div style="font-size: 18px; font-weight: 600; color: {score_color};">{score_label}</div>
                    <div style="color: #64748b; font-size: 13px; margin-top: 4px;">
                        {len(issues)} issue{'s' if len(issues) != 1 else ''} found
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if issues:
                with st.expander("View Issues", expanded=score < 70):
                    for issue in issues:
                        icon = "🔴" if issue["severity"] == "error" else "🟡"
                        st.markdown(f"{icon} **{issue['severity'].upper()}**: {issue['message']}")

            st.markdown("---")

            # Step 6: Merge toggle
            merge = st.checkbox(
                "Merge with existing uploaded data (uncheck to replace)",
                value=True, key="merge_toggle",
            )

            # Step 7: Import button
            unmapped_required = [f for f in type_def["required_mappings"] if not column_map.get(f)]
            if unmapped_required:
                st.warning(f"Required fields not mapped: {', '.join(unmapped_required)}")

            if st.button("Process & Import", type="primary", use_container_width=True, disabled=len(unmapped_required) > 0):
                # Build normalized dataframe
                normalized = pd.DataFrame()
                for internal_field, file_col in column_map.items():
                    if file_col and file_col in raw_df.columns:
                        normalized[internal_field] = raw_df[file_col]

                # Coerce numeric columns
                for col in normalized.columns:
                    if "amount" in col or col in ("hours", "hourly_rate", "unit_cost", "quantity",
                                                   "cost_impact", "schedule_impact_days"):
                        normalized[col] = pd.to_numeric(normalized[col], errors="coerce").fillna(0)

                # Store in session state
                if "uploaded_data" not in st.session_state:
                    st.session_state.uploaded_data = {}

                if merge and upload_type in st.session_state.uploaded_data:
                    existing = st.session_state.uploaded_data[upload_type]["df"]
                    normalized = pd.concat([existing, normalized], ignore_index=True)

                st.session_state.uploaded_data[upload_type] = {"df": normalized, "column_map": column_map}

                # Clear cached app_data so it reloads with new uploads
                if "app_data" in st.session_state:
                    del st.session_state["app_data"]

                st.balloons()
                st.success(f"Imported {len(normalized):,} records as **{upload_type}**")

                # Show summary metrics
                imp_cols = st.columns(3)
                imp_cols[0].metric("Records", f"{len(normalized):,}")
                if "project_name" in normalized.columns:
                    imp_cols[1].metric("Projects", f"{normalized['project_name'].nunique()}")
                if "phase" in normalized.columns:
                    imp_cols[2].metric("Phases", f"{normalized['phase'].nunique()}")

    # --- If we have both budget and actuals uploaded, offer to view dashboard ---
    uploaded = st.session_state.get("uploaded_data", {})
    has_budget = "Budget / Bid" in uploaded
    has_actuals = "Actuals / Costs" in uploaded

    if has_budget and has_actuals:
        st.markdown("---")
        st.success("Budget and Actuals data uploaded. Switch to **Portfolio Overview** in the sidebar to view the dashboard with your data.")
        if st.button("Use Uploaded Data for Dashboard", type="primary"):
            st.session_state["use_uploaded_for_dashboard"] = True
            if "app_data" in st.session_state:
                del st.session_state["app_data"]
            st.rerun()


render()

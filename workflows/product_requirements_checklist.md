# BMM Project Optimizer — Product Requirements Checklist

## 1. Product Requirements

### User Roles (Buyer vs User Mismatch)
- [ ] **Buyer:** VP of Ops / Director of Project Controls — approves purchase
- [ ] **Champion:** Controller or Sr. PM — evaluates and recommends
- [ ] **Daily Users:** Project Managers, Estimators, Field Supers, Controllers
- [ ] Role-based views: each persona sees what they need, nothing more

### Data Inputs
- [ ] Bid estimates and budget line items (CSV, manual entry)
- [ ] Project schedule with milestones, phases, dependencies
- [ ] Crew assignments by phase
- [ ] Timecards / labor hours (actual vs estimated)
- [ ] Material lists: quantities, costs, suppliers, delivery dates
- [ ] Change orders (critical: separate scope change from true overrun)
- [ ] Invoices and subcontractor costs
- [ ] Equipment hours and costs

### Data Readiness & Quality
- [ ] Define who owns data cleanup — us vs client
- [ ] Data validation on import (outlier caps already built: hours≤24, rate≤$500, crew≤100)
- [ ] Missing data handling — what's required vs optional
- [ ] Data freshness requirements: real-time, daily, or weekly refresh
- [ ] Mapping tool for client cost codes → system categories

### Integration
- [ ] Priority 1: CSV/Excel import (universal, works day one)
- [ ] Priority 2: Procore API
- [ ] Priority 3: Sage, QuickBooks, Viewpoint
- [ ] Priority 4: Primavera P6, MS Project (schedule data)
- [ ] Priority 5: Payroll / timesheet systems
- [ ] Each integration = faster onboarding = faster time-to-value

### Risk Detection (Be Specific About What "Accurate" Means)
- [ ] Budget variance by line item, phase, cost category
- [ ] Schedule slippage: milestone risk, float remaining, downstream cascade
- [ ] Labor productivity: actual hours vs estimated by task type
- [ ] Material waste: actual usage vs estimated quantities
- [ ] Supplier reliability: late delivery patterns
- [ ] Procurement timing: reorder needs based on burn rate

### Forecasting
- [ ] Forecasting window: 1 week, 2 weeks, 30 days, phase-level, full project
- [ ] Confidence scoring on predictions (not just "red/yellow/green")
- [ ] Distinguish trend-based forecast from rule-based alerts

### Explainability
- [ ] Every alert must show: what triggered it, what data it's based on, what to do
- [ ] No black-box outputs — users must trust the "why"
- [ ] Drill-down from summary → detail → raw data

### Alert Design (Avoid Alert Fatigue)
- [ ] Severity scoring: critical / warning / info
- [ ] Threshold tuning per company (what counts as "over budget" varies)
- [ ] Prioritized action list — top 3 items with dollar impact, not 50 flags
- [ ] Digest mode vs real-time: VP gets daily summary, PM gets live alerts

### Change Order Handling
- [ ] Separate approved scope change from true cost overrun
- [ ] Track change order impact on budget and schedule
- [ ] Show "budget with changes" vs "original budget" views

### Workflow Fit
- [ ] Each alert maps to a specific action someone can take
- [ ] Not just dashboards — trigger decisions
- [ ] Exportable reports for owner meetings, bank draws, internal reviews

---

## 2. Sales & Go-to-Market

### ICP (Ideal Customer Profile)
- [ ] $100–500M annual revenue ICI general contractor
- [ ] 5–15 active projects at any time, $2–20M each
- [ ] Currently using spreadsheets + monthly cost reports
- [ ] Has felt pain of late-discovered overruns

### Offer Structure
- [ ] $125K / 2-year license ($62.5K/year)
- [ ] ROI pitch: 16:1 if it prevents one mid-size overrun
- [ ] Pilot option: 1-2 projects to prove value before full commitment

### Proof Points (What Buyers Will Demand)
- [ ] Specific, measurable claims: "Identified variance risk 21 days earlier on 68% of pilot projects"
- [ ] Narrow > broad: accuracy at what? (variance detection, schedule risk, waste tracking)
- [ ] Case study or pilot data showing dollar savings
- [ ] Counterfactual: "Here's what would have happened without intervention"

### Common Objections
- [ ] "We already have Procore" → Procore tracks, we predict and recommend
- [ ] "Our data is messy" → We handle mapping and validation on import
- [ ] "My PMs won't use it" → PM view is simpler than their current spreadsheets
- [ ] "How do I know it works?" → Pilot program, measured savings
- [ ] "What if it's wrong?" → Every recommendation shows its reasoning + data source
- [ ] "Guaranteed savings?" → Don't promise guarantees; promise measurable visibility

### Pitch Sequence
- [ ] Hook: "You're finding out about problems 3 weeks too late"
- [ ] Problem: $400K lost on a single 10% overrun
- [ ] Agitate: Monthly reports, gut feel, same mistakes repeating
- [ ] Solution: Real-time intelligence, dollar-denominated recommendations
- [ ] Proof: Specific example alert with dollar impact
- [ ] Close: $62.5K/year vs $1M in prevented overruns

---

## 3. Legal / Compliance / Security

### Contracts
- [ ] Clear limits of liability — software provides recommendations, not guarantees
- [ ] Disclaimer: decisions remain with the client's team
- [ ] NDA template for prospect conversations
- [ ] Data processing agreement (DPA)

### Security (What Enterprise Buyers Will Ask)
- [ ] Encryption at rest and in transit
- [ ] Role-based access control (RBAC)
- [ ] Audit logs: who viewed/changed what, when
- [ ] Data retention and deletion policies
- [ ] Backup and disaster recovery
- [ ] Where data is stored (cloud provider, region)
- [ ] SOC 2 compliance timeline (not needed day one, but buyers will ask)

### Privacy
- [ ] No crew surveillance or individual performance scoring
- [ ] Aggregate data only — no PII in reports
- [ ] Client owns their data, can export or delete anytime

### Multi-Tenant / Permissions
- [ ] Company-level isolation
- [ ] Division / branch separation within a company
- [ ] JV partner access with scoped permissions
- [ ] Project-level access control

---

## 4. Onboarding & Adoption

### Time to First Value
- [ ] Target: first useful insight within 1 week of data import
- [ ] Guided setup wizard: import bid, import schedule, import actuals
- [ ] Pre-built templates for common ICI cost code structures
- [ ] "Quick win" report after first import showing what the tool found

### User Adoption
- [ ] PM training: 30-minute walkthrough, not a 2-day course
- [ ] Field usability: mobile-friendly for site teams (even if limited view)
- [ ] Weekly email digest so VP stays engaged without logging in
- [ ] Champion program: one internal advocate trained to drive adoption

### Support & Customer Success
- [ ] Who helps clients troubleshoot imports?
- [ ] Who helps interpret reports and operationalize recommendations?
- [ ] Quarterly business review showing measured impact
- [ ] Dedicated CS rep for accounts over threshold

---

## 5. Reporting & ROI Proof

### Reports by Persona
- [ ] **VP of Ops:** Portfolio view, red/yellow/green, top 3 actions, margin summary
- [ ] **Project Manager:** Line-item budget tracker, schedule Gantt, material tracker, weekly trends
- [ ] **Controller:** Cost-to-complete forecast, variance analysis, change order impact
- [ ] **Executive/Owner:** Quarterly margin summary, cross-project patterns, platform ROI

### ROI Measurement
- [ ] Track: alerts generated → actions taken → dollars saved
- [ ] Compare: project outcomes with tool vs historical baseline
- [ ] Renewal justification: "The platform identified $X in risk across Y projects this year"
- [ ] False positive / false negative tracking — measure signal quality over time

### Benchmarking
- [ ] Compare current project against historical jobs (same type, size, region)
- [ ] Crew productivity benchmarks by trade and task type
- [ ] Cost code benchmarks: expected vs actual by category
- [ ] Supplier performance benchmarks: delivery time, quality, pricing

---

## Priority Order for Building

1. **CSV import + budget vs actual dashboard** (core value, works without integrations)
2. **Schedule risk alerts** (high impact, differentiator)
3. **Material tracking + supplier intelligence** (unique angle)
4. **Change order separation** (critical for trust)
5. **Procore integration** (adoption accelerator)
6. **Forecasting engine** (competitive moat)
7. **Benchmarking** (requires historical data — comes with scale)

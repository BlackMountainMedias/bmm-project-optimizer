"""AI Assistant page — conversational interface over project data + web search."""
import os
import json
import streamlit as st
from shared import load_data

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_data_context():
    """Summarise the loaded project data into a text block for the LLM."""
    data = st.session_state.get("app_data")
    if not data:
        return "No project data loaded."

    parts = []

    df = data.get("df")
    if df is not None and not df.empty:
        projects = df["project_name"].unique().tolist()
        total_budget = df["budgeted_amount"].sum()
        total_actual = df["actual_amount"].sum()
        total_var = total_actual - total_budget
        parts.append(
            f"BUDGET DATA: {len(projects)} projects — "
            f"Total Budget ${total_budget:,.0f}, Total Actual ${total_actual:,.0f}, "
            f"Variance ${total_var:+,.0f}"
        )
        # Per-project snapshot
        for proj in projects:
            pdf = df[df["project_name"] == proj]
            b = pdf["budgeted_amount"].sum()
            a = pdf["actual_amount"].sum()
            v = a - b
            phases = pdf["phase"].unique().tolist() if "phase" in pdf.columns else []
            parts.append(
                f"  Project '{proj}': Budget ${b:,.0f}, Actual ${a:,.0f}, "
                f"Variance ${v:+,.0f}, Phases: {phases}"
            )
        # Line-item detail (limit to keep context manageable)
        detail_cols = ["project_name", "phase", "cost_category", "line_item",
                       "budgeted_amount", "actual_amount", "variance", "variance_pct"]
        avail = [c for c in detail_cols if c in df.columns]
        parts.append(f"\nLINE ITEMS ({len(df)} rows):")
        for _, row in df[avail].iterrows():
            parts.append("  " + " | ".join(f"{c}: {row[c]}" for c in avail))

    co_df = data.get("co_df")
    if co_df is not None and not co_df.empty:
        parts.append(f"\nCHANGE ORDERS ({len(co_df)} records):")
        for _, row in co_df.iterrows():
            parts.append("  " + " | ".join(f"{c}: {row[c]}" for c in co_df.columns))

    schedule_df = data.get("schedule_df")
    if schedule_df is not None and not schedule_df.empty:
        parts.append(f"\nSCHEDULE ({len(schedule_df)} tasks):")
        for _, row in schedule_df.iterrows():
            parts.append("  " + " | ".join(f"{c}: {row[c]}" for c in schedule_df.columns))

    timecards_df = data.get("timecards_df")
    if timecards_df is not None and not timecards_df.empty:
        parts.append(f"\nTIMECARDS ({len(timecards_df)} entries):")
        for _, row in timecards_df.head(200).iterrows():
            parts.append("  " + " | ".join(f"{c}: {row[c]}" for c in timecards_df.columns))
        if len(timecards_df) > 200:
            parts.append(f"  ... and {len(timecards_df) - 200} more rows")

    materials_df = data.get("materials_df")
    if materials_df is not None and not materials_df.empty:
        parts.append(f"\nMATERIALS ({len(materials_df)} orders):")
        for _, row in materials_df.iterrows():
            parts.append("  " + " | ".join(f"{c}: {row[c]}" for c in materials_df.columns))

    return "\n".join(parts) if parts else "No project data loaded."


def _call_claude(messages, data_context, web_search=False):
    """Call the Anthropic API. Returns the assistant's reply text."""
    try:
        import anthropic
    except ImportError:
        return "Install the `anthropic` package: `pip install anthropic`"

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return ("No API key found. Set `ANTHROPIC_API_KEY` in your environment "
                "or `.env` file to enable the AI Assistant.")

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You are BMM AI Assistant — a construction project intelligence bot for "
        "Blue Mac Construction. You have deep knowledge of construction project "
        "management, budgeting, scheduling, labor productivity, and materials "
        "procurement.\n\n"
        "You have access to the company's current project data below. Use it to "
        "answer questions accurately. When referencing numbers, use full dollar "
        "amounts (never abbreviate). Be concise and direct.\n\n"
        "If the user asks about industry benchmarks, regulations, best practices, "
        "or anything beyond the uploaded data, use your general knowledge to help.\n\n"
        f"COMPANY PROJECT DATA:\n{data_context}"
    )

    kwargs = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1500,
        "system": system_prompt,
        "messages": messages,
    }

    response = client.messages.create(**kwargs)
    return response.content[0].text


# ---------------------------------------------------------------------------
# Page UI
# ---------------------------------------------------------------------------

def render():
    load_data()

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">AI Assistant</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Ask anything about your projects, budgets, labor, schedules — or the construction industry
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialise chat history
    if "ai_messages" not in st.session_state:
        st.session_state["ai_messages"] = []

    # Examples note for empty state
    if not st.session_state["ai_messages"]:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b3515 0%, #ff6b3508 100%);
                    border-left: 3px solid #ff6b35; border-radius: 8px;
                    padding: 14px 18px; margin-bottom: 20px;">
            <span style="color: #e2e8f0; font-size: 13px; font-weight: 600;">Examples of what you can ask:</span>
            <span style="color: #94a3b8; font-size: 12px; display: block; margin-top: 6px; line-height: 1.8;">
                "Which project has the highest budget variance?" &nbsp;|&nbsp;
                "What are the biggest change orders?" &nbsp;|&nbsp;
                "Any schedule delays I should worry about?" &nbsp;|&nbsp;
                "How does our labor cost compare to budget?" &nbsp;|&nbsp;
                "Show me overtime trends across all projects" &nbsp;|&nbsp;
                "What's the industry standard OT percentage for commercial construction?"
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state["ai_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                <div style="background: #1e3a5f; border: 1px solid #2563eb; border-radius: 12px 12px 2px 12px;
                            padding: 12px 16px; max-width: 75%; color: #e2e8f0; font-size: 14px;">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                <div style="background: #111827; border: 1px solid #1e293b; border-radius: 12px 12px 12px 2px;
                            padding: 12px 16px; max-width: 85%; color: #cbd5e1; font-size: 14px;
                            line-height: 1.6;">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Ask about your projects, budgets, labor, schedules...")

    if user_input:
        st.session_state["ai_messages"].append({"role": "user", "content": user_input})

        # Build context and call API
        data_context = _build_data_context()
        api_messages = [{"role": m["role"], "content": m["content"]}
                        for m in st.session_state["ai_messages"]]

        with st.spinner("Thinking..."):
            reply = _call_claude(api_messages, data_context)

        st.session_state["ai_messages"].append({"role": "assistant", "content": reply})
        st.rerun()

    # Clear chat button
    if st.session_state["ai_messages"]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear conversation", type="secondary"):
            st.session_state["ai_messages"] = []
            st.rerun()


render()

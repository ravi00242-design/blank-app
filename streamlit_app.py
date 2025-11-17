# streamlit_app.py
import streamlit as st
from datetime import datetime
import random
import json

# ---------------------------------------------------------
# FULL STREAMLIT DEMO — AI Follow-Up & Lead Resurrection Agent
# Features:
# ✔ WhatsApp-style chat UI
# ✔ Multi-step follow-up generator
# ✔ LLM polish stub (easily replaceable with API call)
# ✔ Lead history + memory simulation
# ✔ Dashboard-style metrics
# ✔ Branding + UI polish
# ---------------------------------------------------------

st.set_page_config(page_title="AI Follow-Up Agent Demo", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
      .sidebar .sidebar-content {background: #f8fafc;}
      .agent-bubble {background:#dcf8c6; padding:10px; border-radius:12px; margin:6px 0;}
      .lead-bubble {background:#e9eef6; padding:10px; border-radius:12px; margin:6px 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header / Branding
# -----------------------------
st.markdown(
    """
    <div style="text-align:center">
      <h1 style="color:#0ea5e9; margin-bottom:4px;">🤖 AI Follow-Up & Lead Resurrection — Demo</h1>
      <p style="color:#374151; margin-top:0;">Automated follow-ups, multi-step sequences, CRM simulation & client-ready flows.</p>
    </div>
    <hr>
    """,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.markdown(
    """
    ## 🚀 AI Business OS — Demo
    Use this demo to simulate how follow-ups are generated and scheduled.
    - Generate follow-ups
    - View CRM simulation
    - Show stepwise follow-up plan
    - Swap industry templates
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("### ⚙️ Demo Controls")
demo_tone = st.sidebar.selectbox("Polish Tone (LLM stub)", ["Professional", "Casual", "Urgent", "Persuasive"])
show_sequence = st.sidebar.checkbox("Show follow-up sequence", value=True)
simulate_metrics = st.sidebar.checkbox("Simulate dashboard metrics", value=True)

# -----------------------------
# Dashboard Snapshot (Demo)
# -----------------------------
if simulate_metrics:
    st.subheader("📊 Dashboard Snapshot (Demo Data)")
    cols = st.columns(4)
    cols[0].metric("Revived Leads", random.randint(12, 55))
    cols[1].metric("Follow-Ups Sent", random.randint(70, 180))
    cols[2].metric("Conversion Boost", f"{random.randint(20,45)}%")
    cols[3].metric("Hours Saved", random.randint(24, 120))
    st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------
# Chat + Controls
# -----------------------------
st.subheader("💬 WhatsApp-Style Chat Simulator")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lead_logs" not in st.session_state:
    st.session_state.lead_logs = []

industry = st.selectbox(
    "Select Industry Context:",
    [
        "Real Estate",
        "Clinics / Dental",
        "Automobile Sales",
        "Education / Coaching",
        "Finance / Loans",
        "Immigration",
        "Generic / Other",
    ],
)

# Industry templates
TEMPLATES = {
    "Real Estate": "Hi {{name}}, following up on the property you checked earlier. Want updated pricing or available units?",
    "Clinics / Dental": "Hi {{name}}, checking in about your consultation. I can send doctor slots or treatment costs.",
    "Automobile Sales": "Hi {{name}}, we have updated prices & variants for the car you enquired about. Want details?",
    "Education / Coaching": "Hi {{name}}, I can share course fees, syllabus, and new batch timings.",
    "Finance / Loans": "Hi {{name}}, I can help you with your loan enquiry. I can pre-check eligibility and share updated interest rates.",
    "Immigration": "Hi {{name}}, following up on your immigration consultation request. I can share eligibility, process steps, and booking link.",
    "Generic / Other": "Hi {{name}}, just checking in — did you get the info you needed?",
}

lead_name = st.text_input("Lead Name", "John")
lead_phone = st.text_input("Lead Phone (demo)", "91800XXXXX")
lead_msg = st.text_area("Lead's Last Message (simulate)", "Hi, I'm busy but I want the info soon.")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Generate AI Follow-Up"):
        # Base template
        base = TEMPLATES.get(industry, TEMPLATES["Generic / Other"]).replace("{{name}}", lead_name)
        # Simulated LLM polish
        def llm_polish(text, context, tone="Professional"):
            # Replace this stub with a real LLM API call as needed.
            tone_suffix = {
                "Professional": "Regards, Team",
                "Casual": "Cheers!",
                "Urgent": "Limited slots — act now!",
                "Persuasive": "Many clients decide in 24 hours — don't miss out!",
            }.get(tone, "Regards, Team")
            polished = f"{text}\n\n{tone_suffix}\n\n(Polished with context: {context})"
            return polished

        context = f"Simulated context: previous inquiry about price; no reply in 3 days. Industry: {industry}"
        polished = llm_polish(base, context, tone=demo_tone)
        st.session_state.chat_history.append(("agent", polished))
        # Log CRM event
        log = {
            "lead": lead_name,
            "phone": lead_phone,
            "industry": industry,
            "generated_at": datetime.now().isoformat(),
            "message": polished,
        }
        st.session_state.lead_logs.append(log)

with col1:
    if st.button("Simulate Lead Reply"):
        st.session_state.chat_history.append(("lead", lead_msg))

# Display chat window
st.markdown("### 🟩 Chat Window")
chat_container = st.container()
with chat_container:
    for sender, msg in st.session_state.chat_history:
        if sender == "lead":
            st.markdown(f"<div class='lead-bubble'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='agent-bubble'>{msg}</div>", unsafe_allow_html=True)

# -----------------------------
# Multi-Step Follow-Up Sequence
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🔁 Multi-Step Follow-Up Flow")

default_steps = [
    "Day 1: Soft nudge — ask if they need more info.",
    "Day 2: Value add — send useful asset (pricing PDF or checklist).",
    "Day 3: Urgency angle — limited slots/units available.",
    "Day 5: Final ping — last chance / callback offer.",
]
if show_sequence:
    for s in default_steps:
        st.write(f"- {s}")

# Allow quick customization
if st.checkbox("Customize sequence (demo)"):
    seq_text = st.text_area("Edit sequence (one per line):", "\n".join(default_steps), height=120)
    seq_lines = [x.strip() for x in seq_text.splitlines() if x.strip()]
    st.write("Resulting sequence:")
    for s in seq_lines:
        st.write(f"- {s}")

# -----------------------------
# CRM Log / Lead History Simulation
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🗂️ CRM Log (Simulated)")

if st.session_state.lead_logs:
    # Show last 6 logs
    for entry in reversed(st.session_state.lead_logs[-6:]):
        st.markdown(
            f"**{entry['generated_at']}** — **{entry['lead']} ({entry['industry']})**\n\n"
            f"{entry['message']}\n\n---"
        )
else:
    st.info("No CRM logs yet. Generate a follow-up to create logs.")

# JSON download
if st.session_state.lead_logs:
    if st.download_button("Download CRM Logs (JSON)", json.dumps(st.session_state.lead_logs, indent=2), file_name="crm_logs.json"):
        st.success("Downloaded CRM logs.")

# -----------------------------
# Demo Controls & Notes
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("⚙️ Demo Notes & Replaceable LLM Stub")
st.write(
    """
    This demo uses a simple `llm_polish` stub. To make responses come from a real model:
    - Replace `llm_polish` with a call to your LLM/Inference endpoint (vLLM/TGI/Groq/OpenAI).
    - For privacy and cost control: use templates + LLM polish only for final touch.
    """
)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Demo built for sales & client walkthroughs. Production backend (FastAPI + connectors + LangGraph) required to send real messages or integrate with client CRMs.")

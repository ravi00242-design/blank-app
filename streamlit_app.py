# streamlit_app.py — Updated to use LM Studio Local LLM (via HTTP endpoint)
# This version uses LM Studio running locally at http://localhost:1234/v1/chat/completions
# Replace the endpoint with your actual LM Studio API URL if different.

import streamlit as st
import requests
from datetime import datetime
import random
import json

# ---------------------------------------------------------
# CONFIG — LM Studio endpoint
# ---------------------------------------------------------
LMSTUDIO_URL = "LMSTUDIO_URL = "https://guidelines-die-racial-gui.trycloudflare.com/v1/chat/completions"
"  # Default LM Studio server
MODEL_NAME = "gemma-2-2b-it"  # LM Studio automatically assigns internal model names, optional

# LLM Polish using LM Studio --------------------------------------------------
def llm_polish(text, context, tone="Professional"):
    prompt = f"Tone: {tone}\nContext: {context}\nMessage: {text}\nPolish and keep concise."

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(LMSTUDIO_URL, json=payload, timeout=20)
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[LLM ERROR] {e}\n\nOriginal message: {text}"

# ---------------------------------------------------------
# STREAMLIT UI SECTION
# ---------------------------------------------------------
st.set_page_config(page_title="AI Follow-Up Agent Demo (LM Studio)", page_icon="🤖", layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#0ea5e9;'>🤖 AI Follow-Up Agent Demo — LM Studio Powered</h1>
<p style='text-align:center; color:#334155;'>This demo uses your LOCAL LM Studio LLM for polishing follow-up messages.</p>
<hr>
""", unsafe_allow_html=True)

# Sidebar ----------------------------------------------------
st.sidebar.header("Demo Controls")
demo_tone = st.sidebar.selectbox("Tone:", ["Professional", "Casual", "Urgent", "Persuasive"])
show_sequence = st.sidebar.checkbox("Show follow-up sequence", True)
sim_metrics = st.sidebar.checkbox("Show dashboard metrics", True)

# Dashboard (fake metrics) -----------------------------------
if sim_metrics:
    cols = st.columns(4)
    cols[0].metric("Revived Leads", random.randint(20,60))
    cols[1].metric("Follow-Ups Sent", random.randint(50,180))
    cols[2].metric("Conversion Boost", f"{random.randint(15,40)}%")
    cols[3].metric("Hours Saved", random.randint(20,120))
    st.markdown("<hr>", unsafe_allow_html=True)

# Chat State --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lead_logs" not in st.session_state:
    st.session_state.lead_logs = []

# Industry Templates -----------------------------------------
industry = st.selectbox(
    "Industry Context",
    [
        "Real Estate", "Clinics / Dental", "Automobile Sales",
        "Education / Coaching", "Finance / Loans",
        "Immigration", "Generic / Other"
    ]
)

TEMPLATES = {
    "Real Estate": "Hi {{name}}, following up on the property you checked earlier. Want updated pricing or available units?",
    "Clinics / Dental": "Hi {{name}}, checking in about your consultation. I can send doctor slots or treatment costs.",
    "Automobile Sales": "Hi {{name}}, we have updated prices & variants for the car you enquired about. Want details?",
    "Education / Coaching": "Hi {{name}}, I can share course fees, syllabus, and upcoming batch timings.",
    "Finance / Loans": "Hi {{name}}, I can help check your loan eligibility and share updated interest rates.",
    "Immigration": "Hi {{name}}, following up on your immigration consultation request.",
    "Generic / Other": "Hi {{name}}, just checking in — did you get the info you needed?",
}

lead_name = st.text_input("Lead Name", "John")
lead_phone = st.text_input("Lead Phone (demo)", "91800XXXXX")
lead_msg = st.text_area("Lead's Last Message (simulate)", "Hi, I'm busy but want info.")

# ------------------------------
# Buttons
# ------------------------------
generate = st.button("Generate AI Follow-Up (LM Studio)")
reply = st.button("Simulate Lead Reply")

# Lead Reply
if reply:
    st.session_state.chat_history.append(("lead", lead_msg))

# Generate Follow-up ----------------------------------------
if generate:
    base_template = TEMPLATES[industry].replace("{{name}}", lead_name)

    context = f"Previous inquiry 3 days ago. Industry: {industry}. Tone: {demo_tone}."

    polished = llm_polish(base_template, context, demo_tone)

    st.session_state.chat_history.append(("agent", polished))

    st.session_state.lead_logs.append({
        "lead": lead_name,
        "phone": lead_phone,
        "industry": industry,
        "message": polished,
        "timestamp": datetime.now().isoformat()
    })

# -------------------------------------------------------------
# WhatsApp-style chat window
# -------------------------------------------------------------
st.subheader("🟩 Chat Window")
for sender, msg in st.session_state.chat_history:
    if sender == "lead":
        st.markdown(f"<div style='background:#e5e7eb;padding:10px;border-radius:10px;margin:6px;width:70%;'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#dcf8c6;padding:10px;border-radius:10px;margin:6px;margin-left:30%;width:70%;text-align:right;'>{msg}</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Follow-up sequence
# -------------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🔁 Multi-Step Follow-Up Sequence")

steps = [
    "Day 1 — Soft nudge",
    "Day 2 — Value add with helpful resource",
    "Day 3 — Urgency angle",
    "Day 5 — Final follow-up",
]

if show_sequence:
    for s in steps:
        st.write(f"- {s}")

# -------------------------------------------------------------
# CRM simulation log
# -------------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🗂️ CRM Log (Simulated)")

if st.session_state.lead_logs:
    st.json(st.session_state.lead_logs[-5:])
else:
    st.info("No CRM logs yet.")

# -------------------------------------------------------------
st.caption("Demo uses LM Studio local LLM for polishing follow-up messages.")

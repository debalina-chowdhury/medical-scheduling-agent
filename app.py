import streamlit as st
import anthropic
import json
from dotenv import load_dotenv
import os

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# Page config
st.set_page_config(
    page_title="MedSchedule AI",
    page_icon="📅",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f7ff;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .tool-badge {
        background-color: #e8f4ea;
        border-left: 3px solid #2e7d32;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.85em;
        margin: 4px 0;
    }
    .header-container {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 style="color:white; margin:0">📅 MedSchedule AI</h1>
    <p style="color:#e3f2fd; margin:0">Intelligent medical practice scheduling assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/hospital.png", width=80)
    st.markdown("### How it works")
    st.markdown("""
    1. 🔍 **Finds** the right provider
    2. ✅ **Verifies** patient eligibility  
    3. 📋 **Processes** referrals
    4. 📅 **Books** appointments
    """)
    st.markdown("---")
    st.markdown("### Try asking:")
    st.markdown("""
    - *"Book P001 with a cardiologist Monday"*
    - *"Process this referral for P002: chest pain, urgent cardiology needed"*
    - *"Find an orthopedic surgeon for P003"*
    """)
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

tools = [
    {
        "name": "find_provider",
        "description": "Find a provider by specialty. Always use this first before checking eligibility or booking.",
        "input_schema": {
            "type": "object",
            "properties": {
                "specialty": {"type": "string", "description": "Medical specialty e.g. cardiology, dermatology"}
            },
            "required": ["specialty"]
        }
    },
    {
        "name": "verify_patient_eligibility",
        "description": "Verify if a patient is eligible to see a specific provider",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "The patient ID"},
                "provider_id": {"type": "string", "description": "The provider ID"}
            },
            "required": ["patient_id", "provider_id"]
        }
    },
    {
        "name": "book_appointment",
        "description": "Book an appointment for a patient with a provider",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "The patient ID"},
                "provider_id": {"type": "string", "description": "The provider ID"},
                "appointment_time": {"type": "string", "description": "Appointment time"},
                "reason": {"type": "string", "description": "Reason for visit"}
            },
            "required": ["patient_id", "provider_id", "appointment_time"]
        }
    },
    {
        "name": "process_referral",
        "description": "Process an incoming referral and extract key information",
        "input_schema": {
            "type": "object",
            "properties": {
                "referral_text": {"type": "string", "description": "The referral document text"},
                "patient_id": {"type": "string", "description": "The patient ID"}
            },
            "required": ["referral_text"]
        }
    }
]

def execute_tool(tool_name, tool_input):
    if tool_name == "find_provider":
        specialty = tool_input["specialty"]
        return (
            f"Found available providers for {specialty}: "
            f"Dr. Sarah Johnson (ID: DR001) - accepting new patients, available Mon 9am and Wed 2pm. "
            f"Dr. Michael Chen (ID: DR002) - accepting new patients, available Tue 11am and Fri 3pm."
        )
    elif tool_name == "verify_patient_eligibility":
        return f"Patient {tool_input['patient_id']} is eligible to see provider {tool_input['provider_id']} — insurance verified, no referral required."
    elif tool_name == "book_appointment":
        return f"✅ Appointment confirmed for patient {tool_input['patient_id']} with provider {tool_input['provider_id']} at {tool_input['appointment_time']}. Confirmation sent via SMS."
    elif tool_name == "process_referral":
        return f"Referral processed — patient needs specialist consult, urgent priority, insurance pre-auth required. Recommended follow-up within 48 hours."

def run_agent(user_query):
    messages = [{"role": "user", "content": user_query}]
    steps = []

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="You are a medical scheduling assistant for a busy practice. Always use find_provider first to get provider IDs — never ask patients for internal IDs. Keep responses concise and patient-friendly. If a specific doctor is not found, offer the next available provider in that specialty.",
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    steps.append(f"**{block.name}** → {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            return response.content[0].text, steps

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"],
        avatar="🏥" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])
        if "steps" in message and message["steps"]:
            with st.expander("🔧 Agent reasoning"):
                for step in message["steps"]:
                    st.markdown(f'<div class="tool-badge">{step}</div>',
                        unsafe_allow_html=True)

# Chat input
query = st.chat_input("Ask about scheduling, referrals, or patient eligibility...")

if query:
    with st.chat_message("user", avatar="👤"):
        st.write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant", avatar="🏥"):
        with st.spinner("Processing..."):
            answer, steps = run_agent(query)
        if steps:
            with st.expander("🔧 Agent reasoning"):
                for step in steps:
                    st.markdown(f'<div class="tool-badge">{step}</div>',
                        unsafe_allow_html=True)
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "steps": steps
    })
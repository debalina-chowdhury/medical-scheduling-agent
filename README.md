# 📅 MedSchedule AI

An AI-powered medical practice scheduling assistant built with Anthropic's Claude API and Streamlit. The agent handles end-to-end appointment workflows — finding providers, verifying insurance eligibility, processing referrals, and booking appointments — all through natural language.

## Demo

**Example queries:**
- *"Book patient P001 with a cardiologist on Monday"*
- *"Process this referral for P002: chest pain, urgent cardiology needed"*
- *"Find an orthopedic surgeon for P003 and check eligibility"*
- *"Patient P001 has chest pain — find a cardiologist, verify insurance, and book urgent appointment"*

## How It Works

1. Receives a natural language query
2. Automatically finds the right provider by specialty
3. Verifies patient insurance eligibility
4. Processes referral documents if needed
5. Books the appointment and confirms via SMS

## Tools

| Tool | Description |
|---|---|
| find_provider | Find available providers by specialty |
| verify_patient_eligibility | Check insurance and eligibility |
| process_referral | Extract key info from referral documents |
| book_appointment | Schedule and confirm appointments |

## Why This Matters

Medical practices waste thousands of hours annually on manual scheduling, referral processing, and eligibility checks. This agent automates the full workflow — the same problem being solved at scale by companies like Parakeet Health, Innovaccer, and Cohere Health.

## Tech Stack

- Anthropic Claude (claude-sonnet-4-5)
- Streamlit
- Python 3.9

## Setup

1. Clone the repo
2. Run: pip install -r requirements.txt
3. Add your API key: echo "ANTHROPIC_API_KEY=your-key-here" > .env
4. Run: streamlit run app.py
5. Open http://localhost:8501

## Project Structure

- app.py — Streamlit frontend and agent loop
- requirements.txt — Dependencies
- .env — API key (not pushed to GitHub)
- .gitignore — Ignores .env
- README.md — This file

## Future Improvementss

- Connect to real EHR APIs (eClinicalWorks, Epic, Athena)
- Integrate with insurance eligibility APIs (Availity, Change Healthcare)
- Add voice input for hands-free scheduling
- Deploy to Streamlit Cloud

## Author

Debalina Chowdhury
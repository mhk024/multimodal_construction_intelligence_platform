# Multimodal Construction Intelligence Platform

A Streamlit capstone prototype for visual site-safety triage, preliminary crack triage, project-planning estimates, and weather-aware site guidance.

## Features

- **Site Safety & PPE Audit:** upload JPG/PNG, request structured JSON from Gemini, review visible PPE indicators and hazards, download a report.
- **Crack Diagnostics:** preliminary image triage with defect category, possible causes, urgency, and next-step suggestions.
- **Planning & Valuation:** editable cost and valuation assumptions, indicative steel/cement thumb rules, progress tracking, JSON export, and a conceptual-render prompt.
- **Daily Site Assistant:** weather-dependent checklists and optional multi-turn Gemini chat.
- **Demo mode:** leave the Gemini key blank to explore the interface without making API calls.
- **No database:** data is kept in Streamlit session state; uploaded images/reports are not intentionally persisted by this app.

## Run locally

Python 3.9+ is the project target. A current supported Python version is recommended.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If your device's application-control policy blocks `pip.exe`, invoke pip through the virtual environment's Python as shown above. If installation is also blocked, contact your device administrator; do not disable security controls.

### macOS / Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Gemini API key

Create a Gemini API key through Google's official AI developer platform. Paste it into the password-type sidebar field for the current session. The app does not save the key to a file. Avoid sharing screenshots that expose the key.

The app uses `gemini-2.5-flash` through the `google-genai` SDK. Model names, API access, quota, pricing, and availability can change. If a request fails, the UI reports an error rather than pretending a real image analysis succeeded.

For Streamlit Community Cloud, add dependencies from `requirements.txt`, set the app entry point to `app.py`, and configure secrets if you later modify the app to read a server-side secret. This version intentionally asks for a session-only key in the sidebar.

## Calculation assumptions

The construction budget is `built-up area × user-entered construction rate`. CapEx incurred is the budget multiplied by completion percentage. Indicative valuation is `built-up area × user-entered valuation rate`. Material requirements use editable thumb-rule assumptions. These are rough early-stage estimates, not an engineer-approved bill of quantities or a professional real-estate valuation.

## Safety and engineering limitations

- Image-based PPE detection can miss obscured items and cannot certify legal or site-specific compliance.
- A photograph cannot reliably establish crack width without a scale reference, root cause, or structural safety.
- Do not use this app to approve occupancy, specify structural repairs, or replace a qualified engineer / safety officer.
- Weather checklists are generic prompts. Follow official alerts, the project safety plan, manufacturer limits, and local rules.
- Do not upload confidential project photos or personal data unless you have authorization and an appropriate data-handling basis.

## Project structure

```text
multimodal_construction_intelligence_platform/
├── app.py
├── modules/
│   ├── __init__.py
│   ├── ai_engine.py
│   ├── planning.py
│   ├── advisory.py
│   └── ui.py
├── requirements.txt
└── README.md
```

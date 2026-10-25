import json
import streamlit as st
from modules.ai_engine import analyze_image, ask_assistant
from modules.planning import estimate_project
from modules.advisory import weather_advisory
from modules.ui import inject_css, render_status

st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

st.title("🏗️ Multimodal Construction Intelligence Platform")
st.caption("Skill Wallet Capstone Project 1 · AI-assisted site intelligence and real-estate decision support")
st.warning(
    "Decision-support prototype only. Image findings, crack severity, material quantities, and valuations are estimates—not "
    "certified safety inspections, structural diagnoses, quantity surveys, or professional valuations. "
    "Have a qualified site safety officer / structural engineer review critical decisions."
)

with st.sidebar:
    st.header("⚙️ Workspace")
    api_key = st.text_input(
        "Google Gemini API key",
        type="password",
        help="Used only for this session. Do not commit API keys to source control.",
        placeholder="Paste API key (optional)",
    )
    st.caption("No key? The app uses clearly labelled demonstration results.")
    st.divider()
    st.subheader("Architecture")
    st.markdown(
        "- **UI:** Streamlit\n"
        "- **Vision & chat:** Gemini multimodal API (optional)\n"
        "- **Planning:** transparent rule-based estimates\n"
        "- **Reports:** downloadable JSON\n"
        "- **Storage:** session state only; no external database"
    )
    st.divider()
    st.caption("Navigation")
    st.markdown("1. Site Safety & PPE Audit\n2. Crack Diagnostics\n3. Planning & Valuation\n4. Daily Site Assistant")

tabs = st.tabs([
    "🦺 Site Safety & PPE",
    "🧱 Crack Diagnostics",
    "📐 Planning & Valuation",
    "🌦️ Daily Site Assistant",
])

def json_download(data, filename):
    st.download_button(
        "⬇️ Download JSON report",
        data=json.dumps(data, indent=2, ensure_ascii=False),
        file_name=filename,
        mime="application/json",
        use_container_width=False,
    )

with tabs[0]:
    st.subheader("Site Safety & PPE Audit")
    st.write("Upload a clear site photo. The model reports visible evidence and uncertainty; obscured PPE must not be treated as confirmed compliance.")
    photo = st.file_uploader("Construction site photo", type=["jpg", "jpeg", "png"], key="safety_photo")
    context = st.text_area("Optional site context", placeholder="e.g., slab casting, work at height, active lifting operation", key="safety_context")
    if photo:
        st.image(photo, caption="Uploaded site photo", use_container_width=True)
        if st.button("Run PPE & hazard audit", type="primary", key="run_safety"):
            with st.spinner("Reviewing image…"):
                result = analyze_image(api_key, photo.getvalue(), photo.type, "safety", context)
            st.session_state["last_safety"] = result
    result = st.session_state.get("last_safety")
    if result:
        cols = st.columns(3)
        cols[0].metric("Safety score", f"{result.get('safety_score', '—')}/100")
        cols[1].metric("Overall status", result.get("overall_status", "Review required"))
        hazards = result.get("hazards", [])
        cols[2].metric("Hazards identified", len(hazards))
        render_status(result.get("overall_status", "Review required"))
        st.markdown("#### PPE checklist")
        ppe = result.get("ppe_detection", {})
        if isinstance(ppe, dict):
            rows = [{"Item": k.replace("_", " ").title(), "Status": str(v)} for k, v in ppe.items()]
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.json(ppe)
        st.markdown("#### Hazards & corrective actions")
        if hazards:
            for i, hazard in enumerate(hazards, 1):
                with st.expander(f"{i}. {hazard.get('hazard', 'Hazard')} · {hazard.get('severity', 'Unknown')}"):
                    st.write(hazard.get("evidence", "Evidence not specified."))
                    st.write("**Corrective remedy:**", hazard.get("remedy", "Review with site safety officer."))
        else:
            st.info("No hazards were returned. This is not proof that the site is hazard-free.")
        st.markdown("#### Structured report")
        st.json(result)
        json_download(result, "site_safety_audit.json")

with tabs[1]:
    st.subheader("Crack Diagnostics & Structural Integrity")
    st.write("Upload a close-up photo with a scale reference if available. Image-only width estimates are highly uncertain.")
    crack_photo = st.file_uploader("Concrete / wall surface photo", type=["jpg", "jpeg", "png"], key="crack_photo")
    crack_context = st.text_area("Optional context", placeholder="e.g., age of structure, location of crack, recent settlement or leakage", key="crack_context")
    if crack_photo:
        st.image(crack_photo, caption="Uploaded surface photo", use_container_width=True)
        if st.button("Analyze visible defect", type="primary", key="run_crack"):
            with st.spinner("Analyzing visible surface…"):
                result = analyze_image(api_key, crack_photo.getvalue(), crack_photo.type, "crack", crack_context)
            st.session_state["last_crack"] = result
    result = st.session_state.get("last_crack")
    if result:
        c1, c2, c3 = st.columns(3)
        c1.metric("Defect classification", result.get("defect_type", "Uncertain"))
        c2.metric("Estimated width", f"{result.get('estimated_crack_width_mm', 'Unknown')} mm")
        c3.metric("Urgency", result.get("urgency", "Engineer review"))
        st.info(result.get("limitations", "Image-based assessment is preliminary."))
        st.markdown("#### Findings")
        st.write("**Possible root causes**")
        for item in result.get("root_causes", []):
            st.markdown(f"- {item}")
        st.write("**Recommended next steps**")
        for item in result.get("recommended_repairs", []):
            st.markdown(f"- {item}")
        st.write("**Additional observations**")
        st.write(result.get("observations", "No additional observations returned."))
        st.markdown("#### Structured report")
        st.json(result)
        json_download(result, "crack_diagnostics.json")

with tabs[2]:
    st.subheader("Project Planning & Real Estate Valuation")
    st.write("Indicative planning estimates using editable assumptions. Local rates vary substantially; replace defaults with a quantity surveyor's rates.")
    col1, col2 = st.columns(2)
    with col1:
        structure = st.selectbox("Structure type", ["Residential apartment", "Independent house", "Commercial building", "Warehouse / industrial"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, max_value=2_000_000, value=5000, step=100)
        tier = st.selectbox("City tier", ["Tier 1", "Tier 2", "Tier 3"])
    with col2:
        completion = st.slider("Completion percentage", 0, 100, 35, 5)
        land_area = st.number_input("Land / plot area (sq ft)", min_value=0, max_value=2_000_000, value=2000, step=100)
        location = st.text_input("City / locality (optional)", placeholder="e.g., Indore")
    with st.expander("Advanced assumptions (₹ per sq ft)"):
        rates = st.number_input("Construction rate", min_value=800, max_value=12000, value=2200, step=100)
        valuation_rate = st.number_input("Indicative asset value rate (built-up ₹/sq ft)", min_value=1000, max_value=50000, value=4500, step=250)
        steel_kg = st.number_input("Steel assumption (kg per sq ft)", min_value=2.0, max_value=12.0, value=4.0, step=0.5)
        cement_bags = st.number_input("Cement assumption (bags per sq ft)", min_value=0.2, max_value=2.0, value=0.40, step=0.05)
    estimate = estimate_project(structure, area, tier, completion, land_area, rates, valuation_rate, steel_kg, cement_bags, location)
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated project budget", estimate["formatted"]["project_budget"])
    m2.metric("CapEx incurred to date", estimate["formatted"]["capex_incurred"])
    m3.metric("Indicative market valuation", estimate["formatted"]["market_valuation"])
    st.progress(completion / 100, text=f"Milestone progress: {completion}%")
    st.markdown("#### Materials & cost breakdown")
    st.dataframe([
        {"Metric": "Estimated steel requirement", "Value": f'{estimate["steel_requirement_tonnes"]:,.2f} tonnes'},
        {"Metric": "Estimated cement requirement", "Value": f'{estimate["cement_requirement_bags"]:,.0f} bags'},
        {"Metric": "Remaining indicative budget", "Value": estimate["formatted"]["remaining_budget"]},
        {"Metric": "Land area supplied", "Value": f'{land_area:,.0f} sq ft'},
        {"Metric": "Location", "Value": location or "Not specified"},
    ], use_container_width=True, hide_index=True)
    st.caption("Materials are thumb-rule estimates for early planning only, not a bill of quantities. Valuation excludes legal, financing, tax, title, and market-comparable analysis.")
    json_download(estimate, "project_planning_estimate.json")
    st.markdown("#### Conceptual 3D rendering prompt")
    render_prompt = (
        f"Photorealistic conceptual architectural visualization of a {structure.lower()}, "
        f"{area} square feet built-up area, located in {location or tier + ' Indian city'}, "
        "realistic Indian construction context, professional daylight exterior view, safe site, "
        "high quality materials, architectural visualization, no text, no logos."
    )
    st.text_area("Generated prompt", value=render_prompt, height=100)
    st.link_button("Open Pollinations image generator", "https://pollinations.ai/", help="Copy the prompt above into the image generator. Provider URLs and access may change.")

with tabs[3]:
    st.subheader("Daily Site Assistant & Weather-Aware Advisory")
    weather = st.selectbox("Today's weather condition", ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"])
    advisory = weather_advisory(weather)
    if advisory["level"] == "Critical":
        st.error(advisory["headline"])
    elif advisory["level"] == "High":
        st.warning(advisory["headline"])
    else:
        st.info(advisory["headline"])
    for item in advisory["actions"]:
        st.markdown(f"- {item}")
    st.caption("Follow local meteorological alerts, the project safety plan, equipment manufacturer limits, and the responsible engineer's directions.")
    st.divider()
    st.markdown("#### Construction engineering assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    user_prompt = st.chat_input("Ask about construction planning, site safety, materials, or maintenance…")
    if user_prompt:
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
        with st.chat_message("assistant"):
            with st.spinner("Preparing guidance…"):
                answer = ask_assistant(api_key, user_prompt, weather, st.session_state.chat_history[:-1])
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

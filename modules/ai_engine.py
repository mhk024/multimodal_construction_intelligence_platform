import json
import io
from PIL import Image

def _demo_safety():
    return {
        "safety_score": 72,
        "overall_status": "Review required",
        "ppe_detection": {
            "helmet": "Unclear — verify on site",
            "high_visibility_vest": "Partially visible / uncertain",
            "steel_toe_boots": "Not reliably assessable from this image",
            "safety_harness": "Not assessable unless work-at-height context is visible"
        },
        "hazards": [
            {
                "hazard": "Potential PPE non-compliance",
                "severity": "Medium",
                "evidence": "Demonstration result only; no real image inference was performed.",
                "remedy": "Conduct a supervisor-led PPE check and ensure required PPE is worn correctly."
            }
        ],
        "limitations": "Demonstration mode: supply a Gemini API key for image-specific analysis."
    }

def _demo_crack():
    return {
        "defect_type": "Uncertain",
        "estimated_crack_width_mm": "Unknown",
        "root_causes": ["Cannot infer cause reliably without image-specific analysis and site context."],
        "recommended_repairs": [
            "Photograph with a scale reference and record crack location, length, and change over time.",
            "Ask a qualified structural engineer to inspect before selecting a repair method."
        ],
        "urgency": "Engineer review",
        "observations": "Demonstration result only; no real image inference was performed.",
        "limitations": "A photograph alone cannot establish structural safety. Do not use this output to approve occupancy or repair design."
    }

def _gemini_call(api_key, prompt, image_bytes=None, mime_type="image/jpeg"):
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        contents = [prompt]
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json" if image_bytes else "text/plain",
                temperature=0.2,
            ),
        )
        return response.text
    except Exception as exc:
        raise RuntimeError(
            "Gemini request failed. Check the API key, network access, model availability, and installed google-genai package. "
            f"Technical detail: {exc}"
        ) from exc

def analyze_image(api_key, image_bytes, mime_type, mode, context=""):
    if not api_key:
        return _demo_safety() if mode == "safety" else _demo_crack()
    # Validate image bytes before sending to the model.
    try:
        Image.open(io.BytesIO(image_bytes)).verify()
    except Exception as exc:
        raise ValueError("The uploaded file could not be read as a valid image.") from exc

    if mode == "safety":
        prompt = f"""
You are a cautious construction-site visual assistant. Analyze the supplied image and return ONLY valid JSON.
Context supplied by user: {context or "None"}.
Use visible evidence only. Mark obscured or unobservable PPE as "Unclear"; do not claim boots or harnesses are absent if they cannot be seen.
Schema:
{{
 "safety_score": integer 0-100,
 "overall_status": "Compliant" | "Review required" | "Unsafe",
 "ppe_detection": {{
   "helmet": "Compliant" | "Non-compliant" | "Unclear",
   "high_visibility_vest": "Compliant" | "Non-compliant" | "Unclear",
   "steel_toe_boots": "Compliant" | "Non-compliant" | "Unclear",
   "safety_harness": "Compliant" | "Non-compliant" | "Unclear"
 }},
 "hazards": [{{"hazard": string, "severity": "Low"|"Medium"|"High"|"Critical", "evidence": string, "remedy": string}}],
 "limitations": string
}}
Do not claim legal compliance certification. OSHA/IS 456 are context references only; site-specific rules and local regulations must be checked by a qualified person. Do not infer compliance from an image alone.
"""
    else:
        prompt = f"""
You are a cautious visual assistant for preliminary concrete/wall defect triage. Analyze the supplied image and return ONLY valid JSON.
Context supplied by user: {context or "None"}.
Schema:
{{
 "defect_type": "Hairline"|"Settlement"|"Structural Shear"|"Thermal Expansion"|"Spalling"|"Uncertain",
 "estimated_crack_width_mm": number|string,
 "root_causes": [string],
 "recommended_repairs": [string],
 "urgency": "Routine monitoring"|"Prompt engineer review"|"Urgent engineer review"|"Immediate area isolation and engineer review",
 "observations": string,
 "limitations": string
}}
Estimate width only if a reliable scale reference is visible; otherwise use "Unknown". Do not prescribe a definitive repair design from a photo. Mention that epoxy injection or re-grouting may be appropriate only after an engineer confirms defect type, cause, and suitability. Never declare a structure safe based on the image.
"""
    try:
        raw = _gemini_call(api_key, prompt, image_bytes, mime_type)
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise ValueError("Model output was not a JSON object.")
        return result
    except Exception as exc:
        # Do not silently convert a failed real analysis into fake results.
        raise RuntimeError(str(exc)) from exc

def ask_assistant(api_key, question, weather, history):
    system_prompt = f"""You are a practical construction project assistant. Current selected weather: {weather}.
Give concise, cautious guidance about construction planning, materials, maintenance, and safety.
For structural defects, electrical hazards, work at height, lifting, or imminent danger, recommend stopping unsafe work and consulting a qualified professional.
Do not claim to replace engineers, safety officers, legal requirements, or local weather alerts. State assumptions and avoid unsupported exact engineering specifications."""
    if not api_key:
        return (
            "Demo mode is active, so I cannot provide AI-generated, context-specific answers. "
            "General checklist: follow the approved method statement and site safety plan; verify materials and measurements; "
            "document issues with photos and dates; and escalate structural, electrical, lifting, or work-at-height risks to the responsible professional. "
            "Add a Gemini API key in the sidebar to enable the interactive assistant."
        )
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        conversation = [system_prompt]
        for item in history[-8:]:
            role = "User" if item["role"] == "user" else "Assistant"
            conversation.append(f"{role}: {item['content']}")
        conversation.append(f"User: {question}")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="\n\n".join(conversation),
            config=types.GenerateContentConfig(temperature=0.4),
        )
        return response.text or "I could not generate a response. Please try again."
    except Exception as exc:
        return f"Assistant unavailable: {exc}. Check your API key and connection, or use the general site safety plan."

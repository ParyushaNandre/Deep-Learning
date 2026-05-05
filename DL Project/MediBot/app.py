"""
🏥 Symptom Checker + Doctor Advice Bot
========================================
Powered by Groq API (Free) + Gradio UI

Pipeline:
  User describes symptoms
       ↓
  Groq AI (llama-3.3-70b) analyzes symptoms
       ↓
  Returns: Possible conditions + Severity + First Aid + Doctor advice
       ↓
  Gradio UI displays everything clearly

Author  : Your Name
Project : GenAI Healthcare Bot
"""

import json
import gradio as gr
from groq import Groq

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Paste your Groq API key here
# Get FREE key from: https://console.groq.com → API Keys → Create API Key
GROQ_API_KEY = "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"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Model to use — llama-3.3-70b is fast, smart, and FREE on Groq
MODEL = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — ANALYZE SYMPTOMS USING GROQ
# ─────────────────────────────────────────────────────────────────────────────

def analyze_symptoms(symptoms, age, gender, existing_conditions):
    """
    Sends user symptoms to Groq AI and gets back a structured JSON analysis.

    Parameters:
        symptoms            : str  — what the user is feeling
        age                 : str  — user's age group
        gender              : str  — user's gender
        existing_conditions : str  — any pre-existing medical conditions

    Returns:
        dict — parsed JSON with full medical analysis
    """

    # Build context string from user profile
    profile = f"Patient: {age}, {gender}"
    if existing_conditions and existing_conditions.strip():
        profile += f", Pre-existing conditions: {existing_conditions}"

    # System prompt — tells Groq to act as a medical assistant
    system_prompt = """
You are MediBot, a knowledgeable medical assistant AI.
Your job is to analyze patient symptoms and provide helpful medical information.

IMPORTANT RULES:
- Always remind the user you are NOT a real doctor
- Never diagnose definitively — always say "possible" or "may suggest"
- Always recommend seeing a real doctor for serious symptoms
- Be empathetic and clear in your language
- Return ONLY valid JSON, no markdown, no extra text
"""

    # User prompt — structured to get consistent JSON output
    user_prompt = f"""
{profile}
Symptoms reported: {symptoms}

Analyze these symptoms and return ONLY a valid JSON object in this EXACT format:

{{
    "severity_level": "Low / Moderate / High / Emergency",
    "severity_emoji": "🟢 / 🟡 / 🔴 / 🚨",
    "summary": "A 2-sentence plain-English summary of what might be going on",
    "possible_conditions": [
        {{
            "name": "Condition Name",
            "likelihood": "Common / Possible / Less Likely",
            "brief_explanation": "One sentence explanation of this condition"
        }}
    ],
    "immediate_action": "What should the patient do RIGHT NOW in 1-2 sentences",
    "see_doctor": {{
        "should_go": true,
        "urgency": "Right Now / Within 24 Hours / Within a Week / When Convenient",
        "reason": "Why they should or don't need to see a doctor"
    }},
    "first_aid_tips": [
        "Tip 1",
        "Tip 2",
        "Tip 3"
    ],
    "lifestyle_advice": [
        "Advice 1",
        "Advice 2",
        "Advice 3"
    ],
    "warning_signs": [
        "Warning sign to watch out for 1",
        "Warning sign to watch out for 2"
    ],
    "disclaimer": "This analysis is AI-generated and NOT a substitute for professional medical advice. Always consult a qualified doctor for diagnosis and treatment."
}}

Return ONLY the JSON object. No explanation. No markdown. No code blocks.
"""

    # Call Groq API
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        temperature=0.3,    # Low temperature = more consistent medical responses
        max_tokens=1500
    )

    raw = response.choices[0].message.content.strip()

    # Clean up markdown code blocks if Groq adds them
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        raw = "\n".join(lines).strip()

    # Parse JSON
    data = json.loads(raw)
    return data


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — FORMAT OUTPUT AS READABLE TEXT
# ─────────────────────────────────────────────────────────────────────────────

def format_output(data, symptoms):
    """
    Takes the JSON from Groq and formats it into a clean,
    readable text report for display in Gradio.
    """

    lines = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines.append("🏥 MEDIBOT — SYMPTOM ANALYSIS REPORT")
    lines.append("═" * 58)
    lines.append(f"📋 Symptoms Entered : {symptoms}")
    lines.append("═" * 58)

    # ── Severity Level ────────────────────────────────────────────────────────
    severity  = data.get("severity_level", "Unknown")
    sev_emoji = data.get("severity_emoji", "⚪")
    lines.append(f"\n{sev_emoji}  SEVERITY LEVEL : {severity.upper()}")
    lines.append(f"   {data.get('summary', '')}")

    # ── Immediate Action ──────────────────────────────────────────────────────
    lines.append(f"\n⚡ IMMEDIATE ACTION")
    lines.append(f"   {data.get('immediate_action', 'N/A')}")

    # ── Doctor Recommendation ─────────────────────────────────────────────────
    doc = data.get("see_doctor", {})
    should_go = doc.get("should_go", True)
    urgency   = doc.get("urgency", "When Convenient")
    reason    = doc.get("reason", "")
    doc_icon  = "🚨" if should_go else "✅"

    lines.append(f"\n👨‍⚕️  DOCTOR VISIT")
    if should_go:
        lines.append(f"   {doc_icon} YES — {urgency}")
    else:
        lines.append(f"   {doc_icon} Not urgent right now")
    lines.append(f"   Reason : {reason}")

    # ── Possible Conditions ───────────────────────────────────────────────────
    conditions = data.get("possible_conditions", [])
    lines.append(f"\n🔍 POSSIBLE CONDITIONS ({len(conditions)} found)")
    lines.append("   " + "─" * 50)
    for i, cond in enumerate(conditions, 1):
        likelihood = cond.get("likelihood", "")
        name       = cond.get("name", "")
        explanation = cond.get("brief_explanation", "")

        # Emoji based on likelihood
        if "Common" in likelihood:
            icon = "🔴"
        elif "Possible" in likelihood:
            icon = "🟡"
        else:
            icon = "🟢"

        lines.append(f"   {i}. {icon} {name}  [{likelihood}]")
        lines.append(f"      {explanation}")

    # ── First Aid Tips ────────────────────────────────────────────────────────
    first_aid = data.get("first_aid_tips", [])
    lines.append(f"\n🩹 FIRST AID TIPS")
    for tip in first_aid:
        lines.append(f"   ✅ {tip}")

    # ── Lifestyle Advice ──────────────────────────────────────────────────────
    lifestyle = data.get("lifestyle_advice", [])
    lines.append(f"\n🌿 LIFESTYLE ADVICE")
    for advice in lifestyle:
        lines.append(f"   💡 {advice}")

    # ── Warning Signs ─────────────────────────────────────────────────────────
    warnings = data.get("warning_signs", [])
    lines.append(f"\n⚠️  WARNING SIGNS — See a doctor IMMEDIATELY if you notice:")
    for w in warnings:
        lines.append(f"   🔺 {w}")

    # ── Disclaimer ────────────────────────────────────────────────────────────
    lines.append(f"\n{'═' * 58}")
    lines.append(f"⚠️  DISCLAIMER")
    lines.append(f"   {data.get('disclaimer', '')}")
    lines.append(f"{'═' * 58}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN FUNCTION — Called by Gradio
# ─────────────────────────────────────────────────────────────────────────────

def symptom_checker(symptoms, age, gender, existing_conditions):
    """
    Main pipeline function connected to Gradio UI.

    Flow:
        User Input → Groq Analysis (JSON) → Formatted Text Output
    """

    # Input validation
    if not symptoms or not symptoms.strip():
        return "⚠️  Please describe your symptoms to get an analysis."

    if len(symptoms.strip()) < 10:
        return "⚠️  Please describe your symptoms in more detail (at least 10 characters)."

    try:
        print(f"\n🔍 Analyzing symptoms: '{symptoms[:60]}...'")
        print(f"   Profile: {age}, {gender}")

        # Step 1 — Get analysis from Groq
        data = analyze_symptoms(symptoms, age, gender, existing_conditions)
        print("✅ Groq analysis complete!")

        # Step 2 — Format into readable text
        output = format_output(data, symptoms)
        print("✅ Output formatted!")

        return output

    except json.JSONDecodeError:
        return "❌ Error: AI returned an unexpected format. Please try again."

    except Exception as e:
        error = str(e)
        if "401" in error or "invalid_api_key" in error.lower():
            return "❌ Invalid API Key! Please check your GROQ_API_KEY in app.py"
        elif "rate" in error.lower():
            return "⏳ Rate limit hit. Please wait a few seconds and try again."
        else:
            return f"❌ Error: {error}"


# ─────────────────────────────────────────────────────────────────────────────
# GRADIO UI — Clean, Simple, Medical Theme
# ─────────────────────────────────────────────────────────────────────────────

with gr.Blocks(
    title="🏥 MediBot — Symptom Checker"
) as app:

    # ── Header ────────────────────────────────────────────────────────────────
    gr.Markdown("""
    # 🏥 MediBot — Symptom Checker + Doctor Advice Bot
    **Describe your symptoms → Get instant AI-powered analysis, first aid tips, and doctor advice**

    > ⚠️ **Disclaimer:** This is an AI assistant, NOT a real doctor. Always consult a qualified medical professional for actual diagnosis and treatment.
    ---
    """)

    # ── Patient Profile ───────────────────────────────────────────────────────
    gr.Markdown("### 👤 Patient Profile")
    with gr.Row():
        age = gr.Dropdown(
            choices=[
                "Child (0–12 years)",
                "Teenager (13–17 years)",
                "Young Adult (18–30 years)",
                "Adult (31–50 years)",
                "Middle-aged (51–65 years)",
                "Senior (65+ years)"
            ],
            value="Young Adult (18–30 years)",
            label="Age Group"
        )
        gender = gr.Dropdown(
            choices=["Male", "Female", "Other / Prefer not to say"],
            value="Male",
            label="Gender"
        )

    existing_conditions = gr.Textbox(
        label="Pre-existing Medical Conditions (optional)",
        placeholder="e.g. Diabetes, Hypertension, Asthma — or leave blank if none",
        lines=1
    )

    # ── Symptoms Input ────────────────────────────────────────────────────────
    gr.Markdown("### 🤒 Describe Your Symptoms")
    symptoms_input = gr.Textbox(
        label="What are you feeling? Describe in detail",
        placeholder="e.g. I have a severe headache since morning, mild fever around 101°F, and my throat is sore. I also feel tired and my body is aching...",
        lines=4
    )

    # ── Submit Button ─────────────────────────────────────────────────────────
    analyze_btn = gr.Button("🔍 Analyze Symptoms", variant="primary", size="lg")

    # ── Output ────────────────────────────────────────────────────────────────
    gr.Markdown("### 📋 Analysis Report")
    output_box = gr.Textbox(
        label="MediBot Report",
        lines=35,
        placeholder="Your symptom analysis will appear here after clicking Analyze..."
    )

    # ── Connect button to function ────────────────────────────────────────────
    analyze_btn.click(
        fn=symptom_checker,
        inputs=[symptoms_input, age, gender, existing_conditions],
        outputs=output_box
    )

    # Also trigger on Enter key in symptoms box
    symptoms_input.submit(
        fn=symptom_checker,
        inputs=[symptoms_input, age, gender, existing_conditions],
        outputs=output_box
    )

    # ── Example Symptoms ──────────────────────────────────────────────────────
    gr.Markdown("### 💡 Example Symptoms — Click to Try:")
    gr.Examples(
        examples=[
            ["I have a high fever of 103°F since 2 days, severe headache, and body pain. I also feel chills.",
             "Young Adult (18–30 years)", "Male", ""],

            ["My chest is hurting badly for the last 30 minutes, I feel shortness of breath and my left arm feels numb.",
             "Middle-aged (51–65 years)", "Male", "Hypertension"],

            ["I have been feeling very sad and hopeless for the past 2 weeks. I can't sleep properly and have lost my appetite.",
             "Teenager (13–17 years)", "Female", ""],

            ["I have a runny nose, mild cough, sore throat, and slight fever since yesterday. No serious pain.",
             "Adult (31–50 years)", "Female", ""],

            ["I suddenly have a severe headache, my vision is blurry, and I feel like vomiting.",
             "Senior (65+ years)", "Male", "Diabetes"],
        ],
        inputs=[symptoms_input, age, gender, existing_conditions]
    )

    # ── Footer ────────────────────────────────────────────────────────────────
    gr.Markdown("""
    ---
    **Emergency?** 🚨 Call **112** (India) immediately | Powered by **Groq AI** (llama-3.3-70b) | Built with **Gradio**
    """)


# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🏥 MediBot is starting...")
    print("📌 Open your browser at: http://localhost:7860")
    print("🛑 Press Ctrl+C to stop\n")
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="teal", secondary_hue="blue")
    )

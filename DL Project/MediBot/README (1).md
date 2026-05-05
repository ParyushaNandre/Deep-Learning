# 🏥 MediBot — Symptom Checker + Doctor Advice Bot

AI-powered symptom checker using **Groq API** (Free) + **Gradio UI**

---

## ⚡ Quick Setup (VS Code)

### Step 1 — Get FREE Groq API Key
1. Go to **https://console.groq.com**
2. Sign up / log in (no credit card needed!)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"** → give it a name → copy the key
5. Key looks like: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
6. Free tier includes **generous daily limits** — more than enough!

### Step 2 — Set Up Project Folder in VS Code
1. Create a folder called `medibot`
2. Put `app.py` and `requirements.txt` inside it
3. Open the folder in VS Code (`File → Open Folder`)

### Step 3 — Open Terminal in VS Code
Press `Ctrl + `` ` `` ` (backtick) to open the terminal

### Step 4 — Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it — Windows:
venv\Scripts\activate

# Activate it — Mac/Linux:
source venv/bin/activate
```
You should see `(venv)` appear in your terminal — that means it's active.

### Step 5 — Install Dependencies
```bash
pip install -r requirements.txt
```
This installs Groq and Gradio. Takes about 30 seconds.

### Step 6 — Add Your API Key
Open `app.py` and find **line 29**:
```python
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
```
Replace with your actual key:
```python
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
Save the file (Ctrl+S).

### Step 7 — Run the App
```bash
python app.py
```

### Step 8 — Open in Browser
Go to: **http://localhost:7860**
Your MediBot is live! 🎉

---

## 🎮 How to Use the Bot

1. Select your **Age Group** and **Gender**
2. Enter any **pre-existing conditions** (or leave blank)
3. Describe your symptoms in detail in the text box
4. Click **"Analyze Symptoms"**
5. Get a full report with:
   - Severity level (Low / Moderate / High / Emergency)
   - Possible conditions with likelihood
   - Immediate action steps
   - Doctor visit recommendation + urgency
   - First aid tips
   - Lifestyle advice
   - Warning signs to watch for

---

## 📁 Project Structure
```
medibot/
├── app.py            ← Main application (all code here)
├── requirements.txt  ← Python dependencies
└── README.md         ← Setup instructions
```

---

## 🔑 API Details

| Service | Model Used | Free Tier |
|---------|------------|-----------|
| Groq | llama-3.3-70b-versatile | Free with daily limits |
| Gradio | — | Always free |

---

## ⚠️ Important Disclaimer
This bot is for **educational purposes only**.
It is NOT a substitute for professional medical advice.
Always consult a qualified doctor for real medical issues.

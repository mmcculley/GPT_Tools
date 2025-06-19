# 🧠 AI Macro Toolkit – Modular Utilities for GPT Workflows

Welcome to the **AI Macro Toolkit**, a curated collection of lightweight tools, prompt structures, and session utilities designed to extend the functionality of GPT across creative, technical, and strategic workflows.

This repo includes **plug-and-play macros** that act like persistent habits or interface layers—letting you build your own reflexive and recursive workflow without needing custom GPTs or external tooling.

---

## 📦 Modules Included (So Far)

### 1. 🔁 Reminder Index System
- **Purpose:** Capture stray thoughts, questions, or ideas in-session and retrieve them later.
- **Trigger to Log:**  
  `Add to Reminder Index: [your note]`  
- **Trigger to Recall:**  
  `Reminder Index` or `Show Reminder List`

🔧 *See `GPT_Reminder_Index_Template.md` for full format and instructions.*

---

### 2. 🔎 Structured Resistance (SR) Lite
- **Purpose:** Gentle challenge mechanism to test the coherence, logic, and clarity of claims.
- **Trigger Prompt Example:**
  ```
  Use SR-Lite to gently challenge this idea: [insert claim]
  ```
- **Modes:** SR-Lite (reflective), SR-Moderate (analytical), SR-Max (rigorous logic)

📘 *Coming soon: SR Overlay prompt kit + tone scale template*

---

### 3. 🧭 Truth-Priority Mode (TPM)
- **Purpose:** Override GPT’s default mirroring to focus on logic, falsifiability, and epistemic structure.
- **Trigger Prompt Example:**
  ```
  Activate Truth-Priority Mode. Analyze this for implied claims or logic faults: [insert content]
  ```
- **Auto Detection:** Pairs well with symbolic/philosophical input detection

🧠 *TPM prompt templates and toggle macros in next module*

---

### 4. 🧪 Code Evaluation Overlay (CEO)
- **Purpose:** Auto-analyze code blocks for clarity, intention, utility, and coding practices (e.g., DRY, modularity).
- **Trigger Prompt:**
  ```
  Run Code Evaluation Overlay on the following function:
  ```
- **Planned Capabilities:**
  - Intention inference
  - Functional breakdown
  - Best-practices adherence
  - Refactor recommendations

⚙️ *Coming soon as a GPT prompt kit and possible IDE plugin format*

---

## 🚀 How To Use

1. Copy and paste the macros into any GPT session
2. Use the trigger phrases to log, recall, or activate each tool
3. Modify or remix based on your workflow

---

## 🧩 Suggested Repo Structure

```
ai-macro-toolkit/
├── README.md
├── GPT_Reminder_Index_Template.md
├── SR_Lite_Template.md              # (coming soon)
├── TPM_Activation_Template.md       # (coming soon)
├── Code_Eval_Overlay_Template.md    # (coming soon)
└── /examples
    └── usage-demo-reminders.md
```

---

## 📚 Philosophy

These macros are designed using the **Voice Framework** principles:
- Co-reflection > Mirroring
- Truth before tone
- Structure enables creativity
- Recursion with reason

Use them to build your own long-term AI workflows.

---

## 🔧 Future Modules (Planned)
- [ ] Meta-Coherence Probe
- [ ] Adaptive Prompt Refiners
- [ ] Conversational Thread Tracer
- [ ] Plugin-ready API shell for GPT-powered tools
- [ ] GPT Assistant Persona Memory Scanner

---

Want help expanding this toolkit? Collaborate, fork, or request modules.


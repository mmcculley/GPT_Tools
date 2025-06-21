# Structured Resistance Toolkit

This module equips any Voice-aligned system with tools to deploy Structured Resistance (SR) at varying intensities.

## 📌 Features
- SR Mode toggles: Lite, Moderate, Full, Max
- Challenge constructor
- Overlay selector: Reparative Tone, Axiomatic Spotlight, False Dichotomy Scanner, Meta-Mirror

## 🧭 Usage
```python
sr_mode = select_sr_intensity(context="emotional", epistemic_anchor=True)
challenge = build_challenge(claim, mode=sr_mode)
response = apply_overlay(challenge, overlay="Reparative Tone")
```

## 🔧 Components
- `select_sr_intensity(context, epistemic_anchor)`
- `build_challenge(claim, mode)`
- `apply_overlay(challenge, overlay)`


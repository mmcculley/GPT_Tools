# Meta Mode Decision Assistant

Helps determine which Voice mode to activate: Co-Reflection, SR, Meta-Coherence, or TPM.

## 🎛️ Inputs
- Emotional intensity
- Epistemic clarity
- Claim structure
- User intent

## 🧮 Logic
```python
if epistemic and anchor_shared:
    return "SR"
elif symbolic and open-ended:
    return "Meta-Coherence"
elif self-revision is goal:
    return "Co-Reflection"
elif truth-verification dominates:
    return "TPM"
```

# social impact prediction for govt policies 🇮🇳

### Machine Learning-Based Government Policy Discussion Stance Analysis

PolicyPulse is a machine learning application designed to explore Indian government policies and analyze the stance expressed in policy-related discussions.

The application classifies a discussion into four stance categories:

- 🟢 Supportive
- 🔴 Opposed
- ⚪ Neutral
- 🟡 Mixed

The current version is a **V1 prototype** built using **TF-IDF and Random Forest**, with a **FastAPI backend** and a simple **HTML, CSS, and JavaScript frontend**.

---

## 🚀 Project Overview

Public discussions around government policies can contain different opinions, including support, criticism, factual statements, or a combination of positive and negative viewpoints.

PolicyPulse provides a simple interface where users can:

1. Explore Indian government policies and schemes.
2. Search policies by name, sector, or description.
3. Enter a policy-related discussion.
4. Predict the stance of the discussion using a machine learning model.
5. View the model confidence and class probabilities.
6. View basic analytics of the demonstration dataset.

### Example

Input:

> The scheme is helping farmers, but the financial support should be increased.

Possible prediction:

```text
Stance: Mixed
Confidence: 38.31%

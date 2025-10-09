# 🧠 AI/ML Concept for SmartSeat Project

## 1. Objective

The AI/ML component of the SmartSeat project is designed to assist users in selecting the most suitable seat in shared environments such as libraries, study areas, or coworking spaces. The system uses data-driven logic to recommend seats based on user preferences and environmental factors, improving both efficiency and comfort.

## 2. Initial Concept (Sprint 1)

The initial AI/ML concept focuses on helping users **choose a quiet seat near a power outlet**. This baseline acts as the foundation for the decision-making logic within the SmartSeat system, using a simple rule-based model that evaluates seats based on noise level and proximity to power sources.

### Example Logic

```python
score = (0.6 * quietness) + (0.4 * power_availability)
```

The seat with the highest score is recommended to the user.

## 3. Planned Extensions (Sprint 2–3)

In future sprints, the AI/ML system will be extended to include additional environmental and user-based factors, transforming it into a more adaptive and personalized recommendation engine.

### Planned Feature Expansion

| Phase              | Focus Area                   | Example Factors                    | Expected Outcome                |
| ------------------ | ---------------------------- | ---------------------------------- | ------------------------------- |
| **Sprint 1 (Now)** | Baseline – Quiet + Power     | Noise level, power outlet distance | Functional rule-based logic     |
| **Sprint 2**       | Environment Enhancement      | Lighting, occupancy, temperature   | Multi-factor recommendation     |
| **Sprint 3**       | Personalization & Adaptation | User feedback, preference learning | Personalized AI recommendations |

## 4. Extended Concept Examples

| Concept Version            | Example Sentence                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
|  **Basic Version**       | "Choose a quiet seat near a power outlet."                                                        |
|  **Extended Version 1**  | "Choose a quiet, well-lit seat near a power outlet."                                              |
|  **Extended Version 2**  | "Choose a quiet and comfortable seat with good lighting and a strong Wi-Fi connection."           |
|  **Advanced ML Version** | "Recommend a personalized seat based on user preferences, comfort, and environmental conditions." |

## 5. Future Development

As SmartSeat evolves, the AI/ML model will shift from a static rule-based approach to a learning system trained on real user data. This will enable:

* Personalized recommendations based on individual preferences
* Improved accuracy through continuous learning
* Enhanced user satisfaction by adapting to real-world behavior patterns

## 6. Summary

The AI/ML concept in SmartSeat begins with a simple rule-based baseline (quiet + power) and progressively integrates richer environmental and behavioral data. By Sprint 3, the system aims to provide **personalized, intelligent seat recommendations**, aligning with the project's goal of helping users find their ideal seat in under 30 seconds.

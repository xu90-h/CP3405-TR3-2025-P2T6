import pandas as pd

# Load data
seats = pd.read_csv("data/seats.csv")

# Rule-based scoring
def seat_score(row):
    return (0.5 * row["available"]) + (0.3 * row["distance_from_teacher"]) + (0.2 * row["fairness_score"])

seats["score"] = seats.apply(seat_score, axis=1)
best = seats.loc[seats["score"].idxmax()]

print("=== SmartSeat AI Baseline ===")
print("Recommended seat:", best["seat_id"])
print("Score:", round(best["score"], 2))

from db import SeatDataProcessor


class RLSeatRecommender:
    def __init__(self):
        self.seat_size = 7
        self.learning_rate = 0.1

    def _calc_seat_score(self, seat_id: str, preference: dict) -> float:
        row = ord(seat_id[0]) - ord("A")
        col = int(seat_id[1:]) - 1
        attr = SeatDataProcessor.get_seat_attr(row, col)

        score = 0.0
        if attr["middle_pos"]:
            score += preference["position"]
        if attr["window"]:
            score += preference["window"]
        if attr["aisle"]:
            score += preference["aisle"]
        return score

    def get_recommend(self, history_seats: list, preference: dict) -> str:
        seat_scores = []
        # Strictly generate seat IDs in A1-G7 format
        for row_char in "ABCDEFG":
            for col in range(1, 8):
                seat_id = f"{row_char}{col}"
                if seat_id in history_seats:
                    continue
                score = self._calc_seat_score(seat_id, preference)
                seat_scores.append((seat_id, score))

        if not seat_scores:
            return max(history_seats, key=history_seats.count) if history_seats else "A1"
        return max(seat_scores, key=lambda x: x[1])[0]

    def update_preference(self, preference: dict, row: int, col: int) -> None:
        attr = SeatDataProcessor.get_seat_attr(row, col)
        update_keys = []
        if attr["middle_pos"]:
            update_keys.append("position")
        if attr["window"]:
            update_keys.append("window")
        if attr["aisle"]:
            update_keys.append("aisle")

        for key in preference:
            if key in update_keys:
                preference[key] += self.learning_rate
            else:
                preference[key] -= self.learning_rate / (3 - len(update_keys)) if len(update_keys) < 3 else 0

        total = sum(preference.values())
        for key in preference:
            preference[key] = round(preference[key] / total, 2)
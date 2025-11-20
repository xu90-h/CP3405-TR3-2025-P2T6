import numpy as np
from db import get_current_seat_status


class SimpleRLSeatRecommender:
    def __init__(self):
        # Initialize 7×7 seating data
        self.seat_rows = ["A", "B", "C", "D", "E", "F", "G"]
        self.seat_cols = [str(i) for i in range(1, 8)]
        self.all_seats = [f"{r}{c}" for r in self.seat_rows for c in self.seat_cols]

        # Initialize the Q-table (each seat corresponds to a value)
        self.q_table = {seat: 0.0 for seat in self.all_seats}

    def get_free_seats(self):
        """Get current available seats"""
        seat_status = get_current_seat_status()
        return [s["seat_id"] for s in seat_status if s["status"] == "free"]

    def recommend(self):
        """Recommend the best available seat based on reinforcement learning"""
        free_seats = self.get_free_seats()
        if not free_seats:
            return "No vacant seats"

        # Choose the free seat with the highest Q value
        best_seat = max(free_seats, key=lambda s: self.q_table[s])
        # Update Q-table (give a positive reward for successful recommendations)
        self.q_table[best_seat] += 0.1 * (1 - self.q_table[best_seat])

        return best_seat
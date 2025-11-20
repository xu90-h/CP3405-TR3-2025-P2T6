import numpy as np
from db import get_current_seat_status, conn, cursor


class SimpleRLSeatRecommender:
    def __init__(self):
        # Initialize Q-table (dynamic adaptation to number of seats)
        self.seat_data = get_current_seat_status()
        self.seat_count = len(self.seat_data)
        self.q_table = np.zeros((self.seat_count, 1))  # The action space only has 'choose seat'”
        self.seat_id_to_idx = {s["seat_id"]: i for i, s in enumerate(self.seat_data)}
        self.idx_to_seat_id = {i: s["seat_id"] for i, s in enumerate(self.seat_data)}

    def update_q_table(self, seat_idx, reward):
        """Update Q-table (core logic of reinforcement learning)"""
        self.q_table[seat_idx] += 0.1 * (reward - self.q_table[seat_idx])

    def recommend(self):
        # Read real-time seat status
        self.seat_data = get_current_seat_status()
        # Index of available seats
        free_seat_idxs = [
            self.seat_id_to_idx[s["seat_id"]]
            for s in self.seat_data if s["status"] == "free"
        ]
        if not free_seat_idxs:
            return "No vacant seats"

        # Choose the free seat with the highest Q value
        free_q_values = self.q_table[free_seat_idxs]
        best_idx = free_seat_idxs[np.argmax(free_q_values)]
        recommended_seat = self.idx_to_seat_id[best_idx]

        # Update Q Table (Reward: Successful Referral)
        self.update_q_table(best_idx, reward=1)
        # Update the database status to 'Ordered'
        cursor.execute('''
            UPDATE seat_info SET status = "booked" WHERE seat_id = ?
        ''', (recommended_seat,))
        conn.commit()
        return recommended_seat
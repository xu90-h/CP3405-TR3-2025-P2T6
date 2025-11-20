import numpy as np
from db import get_current_seat_status


class SimpleRLSeatRecommender:
    def __init__(self):
        # 初始化7×7座位数据
        self.seat_rows = ["A", "B", "C", "D", "E", "F", "G"]
        self.seat_cols = [str(i) for i in range(1, 8)]
        self.all_seats = [f"{r}{c}" for r in self.seat_rows for c in self.seat_cols]

        # 初始化Q表（每个座位对应一个价值）
        self.q_table = {seat: 0.0 for seat in self.all_seats}

    def get_free_seats(self):
        """获取当前空闲座位"""
        seat_status = get_current_seat_status()
        return [s["seat_id"] for s in seat_status if s["status"] == "free"]

    def recommend(self):
        """基于强化学习推荐最佳空闲座位"""
        free_seats = self.get_free_seats()
        if not free_seats:
            return "No vacant seats"

        # 选择Q值最高的空闲座位
        best_seat = max(free_seats, key=lambda s: self.q_table[s])
        # 更新Q表（推荐成功给予正奖励）
        self.q_table[best_seat] += 0.1 * (1 - self.q_table[best_seat])

        return best_seat
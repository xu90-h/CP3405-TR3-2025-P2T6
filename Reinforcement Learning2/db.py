class SeatDataProcessor:
    @staticmethod
    def is_window(row: int, col: int) -> bool:
        return col == 0 or col == 6

    @staticmethod
    def is_aisle(row: int, col: int) -> bool:
        return col == 3

    @staticmethod
    def is_middle_position(row: int) -> bool:
        return 2 <= row <= 4

    @staticmethod
    def get_seat_attr(row: int, col: int) -> dict:
        return {
            "window": SeatDataProcessor.is_window(row, col),
            "aisle": SeatDataProcessor.is_aisle(row, col),
            "middle_pos": SeatDataProcessor.is_middle_position(row)
        }
from dataclasses import dataclass


@dataclass(frozen=True)
class Reward:
    points: float
    cashback: float

    @staticmethod
    def calculate(amount: float) -> "Reward":
        points = amount * 10
        cashback = amount * 0.05
        return Reward(points=points, cashback=cashback)

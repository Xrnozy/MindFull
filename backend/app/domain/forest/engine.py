"""Forest growth engine — tree progression, green points calculation."""
from __future__ import annotations

GROWTH_STAGES = ["seed", "sapling", "young", "mature", "ancient"]
STAGE_THRESHOLDS = {"seed": 0, "sapling": 10, "young": 50, "mature": 200, "ancient": 1000}


def calculate_growth_stage(carbon_absorbed_g: float) -> str:
    """Determine tree growth stage based on carbon absorbed."""
    stage = "seed"
    for name, threshold in STAGE_THRESHOLDS.items():
        if carbon_absorbed_g >= threshold:
            stage = name
    return stage


def calculate_green_points(
    efficiency_score: float,
    streak_bonus: float = 1.0,
) -> int:
    """
    Green points = Base_Points × Efficiency_Multiplier × Streak_Bonus.
    Base is 1 point per prompt, multiplied by efficiency and streak.
    """
    base_points = 1
    efficiency_multiplier = efficiency_score / 50.0  # 100% efficiency → 2x
    points = base_points * efficiency_multiplier * streak_bonus
    return max(1, int(round(points)))


def calculate_carbon_absorption(growth_stage: str, days_alive: int) -> float:
    """Calculate carbon absorbed per day based on growth stage."""
    rates = {"seed": 0.01, "sapling": 0.05, "young": 0.15, "mature": 0.5, "ancient": 1.0}
    rate = rates.get(growth_stage, 0.01)
    return round(rate * days_alive, 4)

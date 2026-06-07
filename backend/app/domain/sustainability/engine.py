"""
Sustainability Scoring Engine.

Carbon footprint, water usage, electricity estimation formulas,
and the sustainability score algorithm.

Formula:
  Carbon (g) = (input_tokens × energy_per_token_in × PUE + output_tokens × energy_per_token_out × PUE) × carbon_intensity
  Water (mL) = electricity_wh × water_factor
  Electricity (Wh) = (input_tokens × energy_per_token_in + output_tokens × energy_per_token_out) × PUE
"""
from __future__ import annotations

from dataclasses import dataclass
from app.core.config import settings


# ──────────────────────────────────────────────
# Model-specific energy/cost factors
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class ModelFactor:
    """Energy and cost factors for a specific AI model."""
    provider: str
    name: str
    energy_per_1k_tokens_in_wh: float
    energy_per_1k_tokens_out_wh: float
    cost_per_1k_tokens_in_usd: float
    cost_per_1k_tokens_out_usd: float
    carbon_per_1k_tokens_g: float  # Pre-computed reference value


# Emission factors per model (approximate values from published research)
MODEL_FACTORS: dict[str, ModelFactor] = {
    "gpt-4o": ModelFactor("openai", "gpt-4o", 0.0048, 0.0144, 0.005, 0.015, 0.0021),
    "gpt-4-turbo": ModelFactor("openai", "gpt-4-turbo", 0.0064, 0.0192, 0.01, 0.03, 0.0028),
    "gpt-3.5-turbo": ModelFactor("openai", "gpt-3.5-turbo", 0.0012, 0.0036, 0.0005, 0.0015, 0.0005),
    "claude-3.5-sonnet": ModelFactor("anthropic", "claude-3.5-sonnet", 0.0040, 0.0120, 0.003, 0.015, 0.0017),
    "claude-3-opus": ModelFactor("anthropic", "claude-3-opus", 0.0080, 0.0240, 0.015, 0.075, 0.0035),
    "claude-3-haiku": ModelFactor("anthropic", "claude-3-haiku", 0.0008, 0.0024, 0.00025, 0.00125, 0.0003),
    "gemini-pro": ModelFactor("google", "gemini-pro", 0.0032, 0.0096, 0.0005, 0.0015, 0.0010),
    "gemini-1.5-pro": ModelFactor("google", "gemini-1.5-pro", 0.0036, 0.0108, 0.00125, 0.005, 0.0012),
    "gemini-1.5-flash": ModelFactor("google", "gemini-1.5-flash", 0.0010, 0.0030, 0.000075, 0.0003, 0.0004),
    "llama-3-70b": ModelFactor("meta", "llama-3-70b", 0.0056, 0.0168, 0.0008, 0.0008, 0.0024),
    "llama-3-8b": ModelFactor("meta", "llama-3-8b", 0.0016, 0.0048, 0.0002, 0.0002, 0.0007),
    "mistral-large": ModelFactor("mistral", "mistral-large", 0.0048, 0.0144, 0.004, 0.012, 0.0021),
}

# Default fallback for unknown models
_DEFAULT_FACTOR = ModelFactor("unknown", "unknown", 0.0040, 0.0120, 0.005, 0.015, 0.0017)


def get_model_factor(model_name: str) -> ModelFactor:
    """Get the emission factor for a model, falling back to a sensible default."""
    return MODEL_FACTORS.get(model_name.lower(), _DEFAULT_FACTOR)


# ──────────────────────────────────────────────
# Carbon Footprint Calculation
# ──────────────────────────────────────────────
def calculate_carbon_g(
    input_tokens: int,
    output_tokens: int,
    model_name: str,
    pue: float | None = None,
    carbon_intensity_g_per_kwh: float | None = None,
) -> float:
    """
    Calculate carbon footprint in grams of CO₂.

    Cf = (T_in × E_in + T_out × E_out) × PUE × CI_grid
    """
    factor = get_model_factor(model_name)
    pue = pue or settings.DEFAULT_PUE
    ci = carbon_intensity_g_per_kwh or settings.DEFAULT_CARBON_INTENSITY_G_PER_KWH

    electricity_wh = (
        (input_tokens / 1000) * factor.energy_per_1k_tokens_in_wh +
        (output_tokens / 1000) * factor.energy_per_1k_tokens_out_wh
    ) * pue

    carbon_g = (electricity_wh / 1000) * ci  # Convert Wh to kWh
    return round(carbon_g, 6)


def calculate_electricity_wh(
    input_tokens: int,
    output_tokens: int,
    model_name: str,
    pue: float | None = None,
) -> float:
    """Calculate electricity consumption in watt-hours."""
    factor = get_model_factor(model_name)
    pue = pue or settings.DEFAULT_PUE

    electricity_wh = (
        (input_tokens / 1000) * factor.energy_per_1k_tokens_in_wh +
        (output_tokens / 1000) * factor.energy_per_1k_tokens_out_wh
    ) * pue
    return round(electricity_wh, 6)


def calculate_water_ml(electricity_wh: float) -> float:
    """
    Estimate water usage in mL.
    Data centers use ~1.8L per kWh for cooling (industry average).
    """
    water_ml = (electricity_wh / 1000) * 1800  # 1.8L/kWh = 1800 mL/kWh
    return round(water_ml, 4)


def calculate_cost_usd(input_tokens: int, output_tokens: int, model_name: str) -> float:
    """Calculate the estimated API cost in USD."""
    factor = get_model_factor(model_name)
    cost = (
        (input_tokens / 1000) * factor.cost_per_1k_tokens_in_usd +
        (output_tokens / 1000) * factor.cost_per_1k_tokens_out_usd
    )
    return round(cost, 6)


# ──────────────────────────────────────────────
# Sustainability Score
# ──────────────────────────────────────────────
def calculate_sustainability_score(
    total_prompts: int,
    avg_efficiency_score: float,
    total_carbon_g: float,
    baseline_carbon_g_per_prompt: float = 0.003,
) -> float:
    """
    Sustainability score (0–100).

    Factors:
    1. Prompt efficiency (40%): Higher efficiency → higher score
    2. Carbon efficiency (30%): Lower carbon per prompt vs baseline → higher score
    3. Volume awareness (30%): Penalizes excessive usage
    """
    if total_prompts == 0:
        return 100.0

    # Efficiency component (0–40)
    efficiency_component = (avg_efficiency_score / 100) * 40

    # Carbon efficiency (0–30): ratio of actual vs baseline
    actual_per_prompt = total_carbon_g / total_prompts
    carbon_ratio = min(actual_per_prompt / baseline_carbon_g_per_prompt, 2.0)
    carbon_component = max(0, (1 - carbon_ratio / 2)) * 30

    # Volume awareness (0–30): diminishing returns on high usage
    import math
    volume_factor = 1 / (1 + math.log1p(total_prompts / 100))
    volume_component = volume_factor * 30

    score = efficiency_component + carbon_component + volume_component
    return round(min(max(score, 0), 100), 2)

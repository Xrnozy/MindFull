"""
Prompt Coach — Prompt Efficiency Analyzer.

Scores prompts for efficiency, clarity, specificity, and provides
token/cost/carbon predictions and model recommendations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from app.domain.sustainability.engine import (
    get_model_factor, calculate_carbon_g, calculate_cost_usd, MODEL_FACTORS
)


@dataclass
class AnalysisResult:
    efficiency_score: float
    clarity_score: float
    specificity_score: float
    context_ratio: float
    repetition_penalty: float
    token_prediction: int
    cost_prediction: float
    carbon_prediction: float
    suggestions: list[str]
    recommended_model: str


def analyze_prompt(prompt_text: str, intended_model: str = "gpt-4o") -> AnalysisResult:
    """
    Analyze a prompt for efficiency, clarity, and sustainability impact.
    Uses text heuristics (no external API calls required).
    """
    words = prompt_text.split()
    word_count = len(words)
    char_count = len(prompt_text)

    # 1. Clarity score: penalize very short or very long prompts
    if word_count < 3:
        clarity = 20.0
    elif word_count < 10:
        clarity = 50.0
    elif word_count <= 100:
        clarity = 85.0
    elif word_count <= 300:
        clarity = 70.0
    else:
        clarity = max(40.0, 80 - (word_count - 300) * 0.1)

    # 2. Specificity: presence of specific instructions, constraints, format requests
    specificity_markers = [
        r'\b(format|output|respond|provide|include|list|table|json|csv|markdown)\b',
        r'\b(step|steps|example|examples|specifically|exactly)\b',
        r'\b(do not|don\'t|avoid|never|must|required)\b',
        r'\b(context|background|given|assuming)\b',
    ]
    specificity_hits = sum(1 for p in specificity_markers if re.search(p, prompt_text, re.IGNORECASE))
    specificity = min(100, 30 + specificity_hits * 17.5)

    # 3. Context ratio: useful content vs filler
    filler_words = {'please', 'kindly', 'would', 'could', 'maybe', 'perhaps', 'basically', 'actually', 'just', 'really'}
    filler_count = sum(1 for w in words if w.lower() in filler_words)
    context_ratio = max(0, 1.0 - (filler_count / max(word_count, 1)) * 2)

    # 4. Repetition penalty
    unique_words = len(set(w.lower() for w in words))
    repetition = 1.0 - (unique_words / max(word_count, 1))
    repetition_penalty = min(repetition * 50, 30)

    # 5. Overall efficiency
    efficiency_score = (
        clarity * 0.30 +
        specificity * 0.30 +
        context_ratio * 100 * 0.25 -
        repetition_penalty * 0.15
    )
    efficiency_score = round(min(max(efficiency_score, 0), 100), 1)

    # 6. Token prediction (rough: ~0.75 tokens per word for input, ~2x for output)
    predicted_input_tokens = int(word_count * 1.33)
    predicted_output_tokens = predicted_input_tokens * 2  # typical response multiplier

    # 7. Cost & carbon prediction
    cost_prediction = calculate_cost_usd(predicted_input_tokens, predicted_output_tokens, intended_model)
    carbon_prediction = calculate_carbon_g(predicted_input_tokens, predicted_output_tokens, intended_model)

    # 8. Model recommendation
    recommended_model = _recommend_model(predicted_input_tokens, predicted_output_tokens)

    # 9. Suggestions
    suggestions = _generate_suggestions(
        word_count, clarity, specificity, context_ratio, repetition_penalty
    )

    return AnalysisResult(
        efficiency_score=efficiency_score,
        clarity_score=round(clarity, 1),
        specificity_score=round(specificity, 1),
        context_ratio=round(context_ratio, 3),
        repetition_penalty=round(repetition_penalty, 1),
        token_prediction=predicted_input_tokens + predicted_output_tokens,
        cost_prediction=cost_prediction,
        carbon_prediction=carbon_prediction,
        suggestions=suggestions,
        recommended_model=recommended_model,
    )


def _recommend_model(input_tokens: int, output_tokens: int) -> str:
    """Recommend the most carbon-efficient model that meets the task needs."""
    candidates = sorted(
        MODEL_FACTORS.values(),
        key=lambda m: m.carbon_per_1k_tokens_g,
    )
    # For simple tasks (<500 tokens), recommend the cheapest model
    total = input_tokens + output_tokens
    if total < 500:
        return candidates[0].name
    elif total < 2000:
        # Medium complexity: balance cost and quality
        return candidates[len(candidates) // 3].name
    else:
        # Complex: mid-range model
        return candidates[len(candidates) // 2].name


def _generate_suggestions(
    word_count: int, clarity: float, specificity: float,
    context_ratio: float, repetition_penalty: float,
) -> list[str]:
    """Generate actionable prompt improvement suggestions."""
    suggestions = []
    if word_count < 10:
        suggestions.append("Add more context to your prompt for better AI responses.")
    if word_count > 300:
        suggestions.append("Consider breaking this into a shorter, more focused prompt.")
    if clarity < 60:
        suggestions.append("Improve clarity by structuring your prompt with clear sections.")
    if specificity < 50:
        suggestions.append("Add output format instructions (e.g., 'respond in JSON', 'list 5 items').")
    if context_ratio < 0.7:
        suggestions.append("Remove filler words (please, just, basically) to improve efficiency.")
    if repetition_penalty > 10:
        suggestions.append("Reduce repetitive phrasing to save tokens.")
    if not suggestions:
        suggestions.append("Great prompt! Your efficiency is above average.")
    return suggestions

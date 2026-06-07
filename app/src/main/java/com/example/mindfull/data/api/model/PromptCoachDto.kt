package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class PromptAnalyzeRequest(
    val prompt_text: String,
    val intended_model: String = "gpt-4o"
)

@Serializable
data class PromptAnalysisResponse(
    val id: String? = null,
    val efficiency_score: Double,
    val clarity_score: Double,
    val specificity_score: Double,
    val context_ratio: Double,
    val repetition_penalty: Double,
    val token_prediction: Int,
    val cost_prediction: Double,
    val carbon_prediction: Double,
    val suggestions: List<String> = emptyList(),
    val recommended_model: String
)

@Serializable
data class ModelBenchmarkResponse(
    val model_name: String,
    val provider: String,
    val avg_tokens_per_watt: Double,
    val cost_per_1k_tokens_in: Double,
    val cost_per_1k_tokens_out: Double,
    val carbon_per_1k_tokens: Double
)

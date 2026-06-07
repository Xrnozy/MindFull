package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class PromptLogRequest(
    val model: String,
    val input_tokens: Int,
    val output_tokens: Int,
    val duration_ms: Int? = null,
    val client_source: String = "android",
    val session_id: String? = null
)

@Serializable
data class SustainabilityMetricResponse(
    val carbon_g: Double,
    val water_ml: Double,
    val electricity_wh: Double,
    val cost_usd: Double
)

@Serializable
data class PromptLogResponse(
    val id: String,
    val sustainability: SustainabilityMetricResponse,
    // val gamification: JsonObject? = null // Add if needed
)

@Serializable
data class SustainabilityScoreResponse(
    val score: Double,
    val total_prompts: Int,
    val total_carbon_g: Double,
    val total_water_ml: Double,
    val total_electricity_wh: Double,
    val total_cost_usd: Double,
    val period: String = "all_time"
)

@Serializable
data class DailyAggregateResponse(
    val date: String,
    val total_prompts: Int,
    val total_input_tokens: Int,
    val total_output_tokens: Int,
    val total_carbon_g: Double,
    val total_water_ml: Double,
    val total_electricity_wh: Double,
    val total_cost_usd: Double,
    val sustainability_score: Double
)

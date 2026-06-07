package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class ReflectionRequest(
    val prompt_text: String,
    val confidence_before: Double? = null
)

@Serializable
data class ReflectionResponse(
    val id: String,
    val reflection_questions: List<String>
)

@Serializable
data class ConfidenceTrackRequest(
    val reflection_id: String,
    val confidence_after: Double,
    val did_proceed: Boolean,
    val delay_seconds: Int = 0
)

@Serializable
data class LearningRetentionResponse(
    val id: String,
    val topic: String,
    val retention_score: Double,
    val last_tested_at: String? = null,
    val decay_rate: Double
)

@Serializable
data class DependencyScoreResponse(
    val score: Double,
    val period_start: String,
    val period_end: String
)

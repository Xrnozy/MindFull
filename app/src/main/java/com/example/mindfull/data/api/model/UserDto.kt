package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class UserResponse(
    val id: String,
    val email: String,
    val full_name: String? = null,
    val avatar_url: String? = null,
    val role: String,
    val is_active: Boolean,
    val total_xp: Int,
    val level: Int,
    val dependency_score: Double,
    val org_id: String? = null,
    val created_at: String,
    val updated_at: String
)

@Serializable
data class UserStats(
    val total_xp: Int = 0,
    val level: Int = 1,
    val total_prompts: Int = 0,
    val total_carbon_g: Double = 0.0,
    val total_water_ml: Double = 0.0,
    val total_electricity_wh: Double = 0.0,
    val sustainability_score: Double = 0.0,
    val dependency_score: Double = 0.0,
    val green_points: Int = 0,
    val trees_planted: Int = 0,
    val current_streak: Int = 0,
    val achievements_count: Int = 0
)

@Serializable
data class UserUpdate(
    val full_name: String? = null,
    val avatar_url: String? = null
)

package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class ForestResponse(
    val id: String,
    val user_id: String,
    val total_green_points: Int,
    val total_trees_planted: Int,
    val level: String, // Seedling, Sapling, etc.
    val next_milestone_points: Int
)

@Serializable
data class TreeDto(
    val id: String,
    val species: String,
    val planted_at: String,
    val status: String,
    val carbon_offset_estimate: Double
)

@Serializable
data class PlantTreeRequest(
    val species: String? = null
)

@Serializable
data class CommunityGoal(
    val id: String,
    val title: String,
    val description: String,
    val current_value: Long,
    val target_value: Long,
    val unit: String,
    val is_completed: Boolean
)

@Serializable
data class Campaign(
    val id: String,
    val name: String,
    val description: String,
    val start_date: String,
    val end_date: String,
    val image_url: String? = null
)

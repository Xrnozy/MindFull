package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class EcoProfile(
    val id: String,
    val name: String,
    val type: String, // organization, individual
    val sustainability_score: Double,
    val total_carbon_footprint: Double,
    val trees_sponsored: Int,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val efficiency_metrics: Map<String, Double>? = null,
    val commitments: List<String>? = null,
    val logo_url: String? = null
)

@Serializable
data class Certification(
    val id: String,
    val name: String,
    val issued_at: String,
    val expiry_date: String? = null,
    val status: String
)

@Serializable
data class UpdateProfileRequest(
    val name: String? = null,
    val commitments: List<String>? = null,
    val is_public: Boolean? = null
)

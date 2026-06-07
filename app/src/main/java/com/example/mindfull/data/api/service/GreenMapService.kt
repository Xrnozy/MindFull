package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.*
import retrofit2.http.*

interface GreenMapService {
    @GET("api/v1/greenmap/profiles")
    suspend fun listProfiles(): List<EcoProfile>

    @GET("api/v1/greenmap/profiles/{profile_id}")
    suspend fun getProfile(@Path("profile_id") profileId: String): EcoProfile

    @PUT("api/v1/greenmap/profiles/{profile_id}")
    suspend fun updateProfile(
        @Path("profile_id") profileId: String,
        @Body request: UpdateProfileRequest
    ): EcoProfile

    @GET("api/v1/greenmap/profiles/{profile_id}/certifications")
    suspend fun getCertifications(@Path("profile_id") profileId: String): List<Certification>
}

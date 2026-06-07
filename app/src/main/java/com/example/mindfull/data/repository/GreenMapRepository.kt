package com.example.mindfull.data.repository

import com.example.mindfull.data.api.model.UpdateProfileRequest
import com.example.mindfull.data.api.service.GreenMapService

class GreenMapRepository(private val service: GreenMapService) {
    suspend fun listProfiles() = service.listProfiles()
    suspend fun getProfile(profileId: String) = service.getProfile(profileId)
    suspend fun updateProfile(profileId: String, name: String? = null, commitments: List<String>? = null, isPublic: Boolean? = null) = 
        service.updateProfile(profileId, UpdateProfileRequest(name, commitments, isPublic))
    suspend fun getCertifications(profileId: String) = service.getCertifications(profileId)
}

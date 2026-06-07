package com.example.mindfull.data.repository

import com.example.mindfull.data.api.model.*
import com.example.mindfull.data.api.service.ThinkAheadService

class ThinkAheadRepository(private val service: ThinkAheadService) {
    suspend fun reflect(promptText: String): Result<ReflectionResponse> {
        return try {
            val response = service.reflect(ReflectionRequest(promptText))
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Reflection failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun trackConfidence(request: ConfidenceTrackRequest): Result<Unit> {
        return try {
            val response = service.trackConfidence(request)
            if (response.isSuccessful) Result.success(Unit) else Result.failure(Exception("Tracking failed"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getRetention(): Result<List<LearningRetentionResponse>> {
        return try {
            val response = service.getRetention()
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to fetch retention: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getDependencyScore(): Result<DependencyScoreResponse> {
        return try {
            val response = service.getDependencyScore()
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to fetch dependency score: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

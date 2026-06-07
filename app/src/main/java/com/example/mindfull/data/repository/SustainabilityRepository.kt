package com.example.mindfull.data.repository

import com.example.mindfull.data.api.model.DailyAggregateResponse
import com.example.mindfull.data.api.model.PromptLogRequest
import com.example.mindfull.data.api.model.PromptLogResponse
import com.example.mindfull.data.api.model.SustainabilityScoreResponse
import com.example.mindfull.data.api.service.SustainabilityService

class SustainabilityRepository(private val sustainabilityService: SustainabilityService) {
    suspend fun logPrompt(request: PromptLogRequest): Result<PromptLogResponse> {
        return try {
            val response = sustainabilityService.logPrompt(request)
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to log prompt: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getScore(): Result<SustainabilityScoreResponse> {
        return try {
            val response = sustainabilityService.getScore()
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to get score: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getHistory(startDate: String? = null, endDate: String? = null): Result<List<DailyAggregateResponse>> {
        return try {
            val response = sustainabilityService.getHistory(startDate, endDate)
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to get history: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

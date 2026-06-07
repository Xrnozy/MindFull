package com.example.mindfull.data.repository

import com.example.mindfull.data.api.model.ModelBenchmarkResponse
import com.example.mindfull.data.api.model.PromptAnalysisResponse
import com.example.mindfull.data.api.model.PromptAnalyzeRequest
import com.example.mindfull.data.api.service.PromptCoachService

class PromptCoachRepository(private val service: PromptCoachService) {
    suspend fun analyze(promptText: String): Result<PromptAnalysisResponse> {
        return try {
            val response = service.analyze(PromptAnalyzeRequest(promptText))
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Analysis failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getModels(): Result<List<ModelBenchmarkResponse>> {
        return try {
            val response = service.getModels()
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to fetch models: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

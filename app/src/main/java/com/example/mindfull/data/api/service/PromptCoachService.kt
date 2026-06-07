package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.ModelBenchmarkResponse
import com.example.mindfull.data.api.model.PromptAnalysisResponse
import com.example.mindfull.data.api.model.PromptAnalyzeRequest
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface PromptCoachService {
    @POST("api/v1/prompt-coach/analyze")
    suspend fun analyze(@Body request: PromptAnalyzeRequest): Response<PromptAnalysisResponse>

    @GET("api/v1/prompt-coach/history")
    suspend fun getHistory(): Response<List<PromptAnalysisResponse>>

    @GET("api/v1/prompt-coach/models")
    suspend fun getModels(): Response<List<ModelBenchmarkResponse>>
}

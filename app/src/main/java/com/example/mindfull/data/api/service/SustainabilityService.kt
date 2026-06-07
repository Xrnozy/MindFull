package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.DailyAggregateResponse
import com.example.mindfull.data.api.model.PromptLogRequest
import com.example.mindfull.data.api.model.PromptLogResponse
import com.example.mindfull.data.api.model.SustainabilityScoreResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface SustainabilityService {
    @POST("api/v1/sustainability/log")
    suspend fun logPrompt(@Body request: PromptLogRequest): Response<PromptLogResponse>

    @GET("api/v1/sustainability/score")
    suspend fun getScore(): Response<SustainabilityScoreResponse>

    @GET("api/v1/sustainability/history")
    suspend fun getHistory(
        @Query("start_date") startDate: String? = null,
        @Query("end_date") endDate: String? = null
    ): Response<List<DailyAggregateResponse>>
}

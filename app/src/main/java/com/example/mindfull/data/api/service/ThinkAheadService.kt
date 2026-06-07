package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.*
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ThinkAheadService {
    @POST("api/v1/think-ahead/reflect")
    suspend fun reflect(@Body request: ReflectionRequest): Response<ReflectionResponse>

    @POST("api/v1/think-ahead/confidence")
    suspend fun trackConfidence(@Body request: ConfidenceTrackRequest): Response<Unit>

    @GET("api/v1/think-ahead/retention")
    suspend fun getRetention(): Response<List<LearningRetentionResponse>>

    @GET("api/v1/think-ahead/dependency-score")
    suspend fun getDependencyScore(): Response<DependencyScoreResponse>
}

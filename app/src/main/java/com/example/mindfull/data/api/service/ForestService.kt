package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.*
import retrofit2.http.*

interface ForestService {
    @GET("api/v1/forest/")
    suspend fun getForest(): ForestResponse

    @POST("api/v1/forest/plant")
    suspend fun plantTree(@Body request: PlantTreeRequest): TreeDto

    @GET("api/v1/forest/trees")
    suspend fun listTrees(): List<TreeDto>

    @GET("api/v1/forest/community-goals")
    suspend fun getCommunityGoals(): List<CommunityGoal>

    @GET("api/v1/forest/campaigns")
    suspend fun getCampaigns(): List<Campaign>
}

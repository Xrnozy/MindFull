package com.example.mindfull.data.repository

import com.example.mindfull.data.api.model.PlantTreeRequest
import com.example.mindfull.data.api.service.ForestService

class ForestRepository(private val service: ForestService) {
    suspend fun getForest() = service.getForest()
    suspend fun plantTree(species: String? = null) = service.plantTree(PlantTreeRequest(species))
    suspend fun listTrees() = service.listTrees()
    suspend fun getCommunityGoals() = service.getCommunityGoals()
    suspend fun getCampaigns() = service.getCampaigns()
}

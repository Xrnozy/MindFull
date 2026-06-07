package com.example.mindfull

import android.app.Application
import com.example.mindfull.data.api.ApiClient
import com.example.mindfull.data.local.TokenManager
import com.example.mindfull.data.repository.AuthRepository
import com.example.mindfull.data.repository.ForestRepository
import com.example.mindfull.data.repository.GreenMapRepository
import com.example.mindfull.data.repository.PromptCoachRepository
import com.example.mindfull.data.repository.ThinkAheadRepository
import com.example.mindfull.data.repository.SustainabilityRepository
import com.example.mindfull.data.repository.UserRepository

class MindfullApplication : Application() {
    
    lateinit var apiClient: ApiClient
    lateinit var tokenManager: TokenManager
    lateinit var authRepository: AuthRepository
    lateinit var userRepository: UserRepository
    lateinit var sustainabilityRepository: SustainabilityRepository
    lateinit var promptCoachRepository: PromptCoachRepository
    lateinit var thinkAheadRepository: ThinkAheadRepository
    lateinit var forestRepository: ForestRepository
    lateinit var greenMapRepository: GreenMapRepository

    override fun onCreate() {
        super.onCreate()
        
        tokenManager = TokenManager(this)
        apiClient = ApiClient(this)
        
        authRepository = AuthRepository(apiClient.authService, tokenManager)
        userRepository = UserRepository(apiClient.userService)
        sustainabilityRepository = SustainabilityRepository(apiClient.sustainabilityService)
        promptCoachRepository = PromptCoachRepository(apiClient.promptCoachService)
        thinkAheadRepository = ThinkAheadRepository(apiClient.thinkAheadService)
        forestRepository = ForestRepository(apiClient.forestService)
        greenMapRepository = GreenMapRepository(apiClient.greenMapService)
    }
}

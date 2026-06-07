package com.example.mindfull.data.api

import android.content.Context
import com.example.mindfull.data.api.service.AuthService
import com.example.mindfull.data.api.service.ForestService
import com.example.mindfull.data.api.service.GreenMapService
import com.example.mindfull.data.api.service.PromptCoachService
import com.example.mindfull.data.api.service.ThinkAheadService
import com.example.mindfull.data.api.service.SustainabilityService
import com.example.mindfull.data.api.service.UserService
import com.example.mindfull.data.local.TokenManager
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory

class ApiClient(context: Context) {
    private val BASE_URL = "http://100.118.48.12:8000/"

    private val json = Json {
        ignoreUnknownKeys = true
        coerceInputValues = true
    }

    private val tokenManager = TokenManager(context)

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(AuthInterceptor(tokenManager))
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    val authService: AuthService = retrofit.create(AuthService::class.java)
    val userService: UserService = retrofit.create(UserService::class.java)
    val sustainabilityService: SustainabilityService = retrofit.create(SustainabilityService::class.java)
    val promptCoachService: PromptCoachService = retrofit.create(PromptCoachService::class.java)
    val forestService: ForestService = retrofit.create(ForestService::class.java)
    val greenMapService: GreenMapService = retrofit.create(GreenMapService::class.java)
    val thinkAheadService: ThinkAheadService = retrofit.create(ThinkAheadService::class.java)
}

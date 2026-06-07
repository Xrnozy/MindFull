package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.LoginResponse
import com.example.mindfull.data.api.model.UserLoginRequest
import com.example.mindfull.data.api.model.UserRegisterRequest
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthService {
    @POST("api/v1/auth/register")
    suspend fun register(@Body request: UserRegisterRequest): Response<Unit>

    @POST("api/v1/auth/login")
    suspend fun login(@Body request: UserLoginRequest): Response<LoginResponse>
}

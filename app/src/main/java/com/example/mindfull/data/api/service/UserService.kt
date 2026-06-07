package com.example.mindfull.data.api.service

import com.example.mindfull.data.api.model.UserResponse
import com.example.mindfull.data.api.model.UserStats
import com.example.mindfull.data.api.model.UserUpdate
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT

interface UserService {
    @GET("api/v1/users/me")
    suspend fun getMe(): Response<UserResponse>

    @PUT("api/v1/users/me")
    suspend fun updateMe(@Body request: UserUpdate): Response<UserResponse>

    @GET("api/v1/users/me/stats")
    suspend fun getMyStats(): Response<UserStats>
}

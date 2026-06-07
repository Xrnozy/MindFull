package com.example.mindfull.data.repository

import com.example.mindfull.data.api.model.UserResponse
import com.example.mindfull.data.api.model.UserStats
import com.example.mindfull.data.api.model.UserUpdate
import com.example.mindfull.data.api.service.UserService

class UserRepository(private val userService: UserService) {
    suspend fun getMe(): Result<UserResponse> {
        return try {
            val response = userService.getMe()
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to get profile: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateMe(request: UserUpdate): Result<UserResponse> {
        return try {
            val response = userService.updateMe(request)
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to update profile: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getMyStats(): Result<UserStats> {
        return try {
            val response = userService.getMyStats()
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) Result.success(body) else Result.failure(Exception("Empty body"))
            } else {
                Result.failure(Exception("Failed to get stats: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

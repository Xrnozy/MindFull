package com.example.mindfull.data.repository

import com.example.mindfull.data.api.service.AuthService
import com.example.mindfull.data.api.model.UserLoginRequest
import com.example.mindfull.data.api.model.UserRegisterRequest
import com.example.mindfull.data.local.TokenManager

class AuthRepository(
    private val authService: AuthService,
    private val tokenManager: TokenManager
) {
    suspend fun login(request: UserLoginRequest): Result<Unit> {
        return try {
            val response = authService.login(request)
            if (response.isSuccessful) {
                val loginResponse = response.body()
                if (loginResponse != null) {
                    tokenManager.saveToken(loginResponse.access_token)
                    Result.success(Unit)
                } else {
                    Result.failure(Exception("Empty response body"))
                }
            } else {
                Result.failure(Exception("Login failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun register(request: UserRegisterRequest): Result<Unit> {
        return try {
            val response = authService.register(request)
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Registration failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun logout() {
        tokenManager.clearToken()
    }
}

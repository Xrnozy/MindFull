package com.example.mindfull.data.api.model

import kotlinx.serialization.Serializable

@Serializable
data class UserRegisterRequest(
    val email: String,
    val password: String,
    val full_name: String? = null
)

@Serializable
data class UserLoginRequest(
    val email: String,
    val password: String
)

@Serializable
data class LoginResponse(
    val access_token: String,
    val token_type: String = "bearer"
)

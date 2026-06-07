package com.example.mindfull.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.mindfull.data.api.model.UserLoginRequest
import com.example.mindfull.data.api.model.UserRegisterRequest
import com.example.mindfull.data.repository.AuthRepository
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class AuthViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _authState = MutableSharedFlow<AuthResult>()
    val authState: SharedFlow<AuthResult> = _authState

    fun login(email: String, password: String) {
        viewModelScope.launch {
            _isLoading.value = true
            val result = repository.login(UserLoginRequest(email, password))
            _isLoading.value = false
            if (result.isSuccess) {
                _authState.emit(AuthResult.Success)
            } else {
                _authState.emit(AuthResult.Error(result.exceptionOrNull()?.message ?: "Login failed"))
            }
        }
    }

    fun register(email: String, password: String, fullName: String) {
        viewModelScope.launch {
            _isLoading.value = true
            val result = repository.register(UserRegisterRequest(email, password, fullName))
            _isLoading.value = false
            if (result.isSuccess) {
                _authState.emit(AuthResult.RegisterSuccess)
            } else {
                _authState.emit(AuthResult.Error(result.exceptionOrNull()?.message ?: "Registration failed"))
            }
        }
    }

    sealed class AuthResult {
        object Success : AuthResult()
        object RegisterSuccess : AuthResult()
        data class Error(val message: String) : AuthResult()
    }
}

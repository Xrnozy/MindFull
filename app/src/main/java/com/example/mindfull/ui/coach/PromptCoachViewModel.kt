package com.example.mindfull.ui.coach

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.mindfull.data.api.model.PromptAnalysisResponse
import com.example.mindfull.data.repository.PromptCoachRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class PromptCoachViewModel(private val repository: PromptCoachRepository) : ViewModel() {

    private val _analysisResult = MutableStateFlow<PromptAnalysisResponse?>(null)
    val analysisResult: StateFlow<PromptAnalysisResponse?> = _analysisResult

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage

    fun analyzePrompt(text: String) {
        if (text.isBlank()) return
        
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null
            repository.analyze(text).onSuccess { result ->
                _analysisResult.value = result
            }.onFailure { error ->
                _errorMessage.value = error.message ?: "Analysis failed"
            }
            _isLoading.value = false
        }
    }
}

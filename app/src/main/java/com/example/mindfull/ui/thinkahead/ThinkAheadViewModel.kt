package com.example.mindfull.ui.thinkahead

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.mindfull.data.api.model.DependencyScoreResponse
import com.example.mindfull.data.api.model.LearningRetentionResponse
import com.example.mindfull.data.api.model.ReflectionResponse
import com.example.mindfull.data.repository.ThinkAheadRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ThinkAheadViewModel(private val repository: ThinkAheadRepository) : ViewModel() {

    private val _reflection = MutableStateFlow<ReflectionResponse?>(null)
    val reflection: StateFlow<ReflectionResponse?> = _reflection

    private val _dependencyScore = MutableStateFlow<DependencyScoreResponse?>(null)
    val dependencyScore: StateFlow<DependencyScoreResponse?> = _dependencyScore

    private val _retention = MutableStateFlow<List<LearningRetentionResponse>>(emptyList())
    val retention: StateFlow<List<LearningRetentionResponse>> = _retention

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun requestReflection(prompt: String) {
        viewModelScope.launch {
            _isLoading.value = true
            repository.reflect(prompt).onSuccess {
                _reflection.value = it
            }
            _isLoading.value = false
        }
    }

    fun loadData() {
        viewModelScope.launch {
            repository.getDependencyScore().onSuccess {
                _dependencyScore.value = it
            }
            repository.getRetention().onSuccess {
                _retention.value = it
            }
        }
    }
}

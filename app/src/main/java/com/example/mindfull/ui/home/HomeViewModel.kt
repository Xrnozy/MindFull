package com.example.mindfull.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.mindfull.data.api.model.UserResponse
import com.example.mindfull.data.api.model.UserStats
import com.example.mindfull.data.api.model.SustainabilityScoreResponse
import com.example.mindfull.data.repository.SustainabilityRepository
import com.example.mindfull.data.repository.UserRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class HomeViewModel(
    private val userRepository: UserRepository,
    private val sustainabilityRepository: SustainabilityRepository
) : ViewModel() {

    private val _userProfile = MutableStateFlow<UserResponse?>(null)
    val userProfile: StateFlow<UserResponse?> = _userProfile

    private val _userStats = MutableStateFlow<UserStats?>(null)
    val userStats: StateFlow<UserStats?> = _userStats

    private val _sustainabilityScore = MutableStateFlow<SustainabilityScoreResponse?>(null)
    val sustainabilityScore: StateFlow<SustainabilityScoreResponse?> = _sustainabilityScore

    private val _mascotAdvice = MutableStateFlow("Optimizing your intelligence and impact today.")
    val mascotAdvice: StateFlow<String> = _mascotAdvice

    fun loadDashboardData() {
        viewModelScope.launch {
            userRepository.getMe().onSuccess { profile ->
                _userProfile.value = profile
            }
            userRepository.getMyStats().onSuccess { stats ->
                _userStats.value = stats
                updateMascotAdvice(stats)
            }
            sustainabilityRepository.getScore().onSuccess { score ->
                _sustainabilityScore.value = score
            }
        }
    }

    private fun updateMascotAdvice(stats: UserStats) {
        _mascotAdvice.value = when {
            stats.dependency_score > 0.5 -> "You're relying a bit much on AI lately. Try the Think-A-Head challenges!"
            stats.current_streak > 5 -> "Amazing! You're on a ${stats.current_streak} day streak of sustainable AI usage."
            stats.total_carbon_g > 1000 -> "Your AI footprint is growing. Consider using gpt-4o-mini for simpler tasks."
            else -> "Hello! I'm Coach Eagle. Ready to optimize your prompts today?"
        }
    }
}

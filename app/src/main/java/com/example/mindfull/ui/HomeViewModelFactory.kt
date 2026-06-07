package com.example.mindfull.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.mindfull.data.repository.SustainabilityRepository
import com.example.mindfull.data.repository.UserRepository
import com.example.mindfull.ui.home.HomeViewModel

class HomeViewModelFactory(
    private val userRepository: UserRepository,
    private val sustainabilityRepository: SustainabilityRepository
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(HomeViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return HomeViewModel(userRepository, sustainabilityRepository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

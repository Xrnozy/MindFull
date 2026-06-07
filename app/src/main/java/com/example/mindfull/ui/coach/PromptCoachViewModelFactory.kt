package com.example.mindfull.ui.coach

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.mindfull.data.repository.PromptCoachRepository

class PromptCoachViewModelFactory(private val repository: PromptCoachRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(PromptCoachViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return PromptCoachViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

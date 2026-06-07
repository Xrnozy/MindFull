package com.example.mindfull.ui.forest

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.mindfull.data.repository.ForestRepository

class ForestViewModelFactory(private val repository: ForestRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ForestViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ForestViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

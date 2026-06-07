package com.example.mindfull.ui.thinkahead

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.mindfull.data.repository.ThinkAheadRepository

class ThinkAheadViewModelFactory(private val repository: ThinkAheadRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ThinkAheadViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ThinkAheadViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

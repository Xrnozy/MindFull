package com.example.mindfull.ui.greenmap

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.mindfull.data.repository.GreenMapRepository

class GreenMapViewModelFactory(private val repository: GreenMapRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(GreenMapViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return GreenMapViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

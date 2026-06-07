package com.example.mindfull.ui.forest

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.mindfull.data.api.model.*
import com.example.mindfull.data.repository.ForestRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ForestViewModel(private val repository: ForestRepository) : ViewModel() {

    private val _forest = MutableStateFlow<ForestResponse?>(null)
    val forest = _forest.asStateFlow()

    private val _trees = MutableStateFlow<List<TreeDto>>(emptyList())
    val trees = _trees.asStateFlow()

    private val _communityGoals = MutableStateFlow<List<CommunityGoal>>(emptyList())
    val communityGoals = _communityGoals.asStateFlow()

    private val _campaigns = MutableStateFlow<List<Campaign>>(emptyList())
    val campaigns = _campaigns.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage = _errorMessage.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _forest.value = repository.getForest()
                _trees.value = repository.listTrees()
                _communityGoals.value = repository.getCommunityGoals()
                _campaigns.value = repository.getCampaigns()
                _errorMessage.value = null
            } catch (e: Exception) {
                _errorMessage.value = e.message
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun plantTree(species: String? = null) {
        viewModelScope.launch {
            try {
                repository.plantTree(species)
                loadData() // Refresh data
            } catch (e: Exception) {
                _errorMessage.value = e.message
            }
        }
    }
}

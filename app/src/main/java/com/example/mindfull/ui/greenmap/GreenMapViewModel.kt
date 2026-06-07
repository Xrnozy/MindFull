package com.example.mindfull.ui.greenmap

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.mindfull.data.api.model.*
import com.example.mindfull.data.repository.GreenMapRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class GreenMapViewModel(private val repository: GreenMapRepository) : ViewModel() {

    private val _profiles = MutableStateFlow<List<EcoProfile>>(emptyList())
    val profiles = _profiles.asStateFlow()

    private val _selectedProfile = MutableStateFlow<EcoProfile?>(null)
    val selectedProfile = _selectedProfile.asStateFlow()

    private val _certifications = MutableStateFlow<List<Certification>>(emptyList())
    val certifications = _certifications.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage = _errorMessage.asStateFlow()

    fun loadProfiles() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _profiles.value = repository.listProfiles()
                _errorMessage.value = null
            } catch (e: Exception) {
                _errorMessage.value = e.message
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun selectProfile(profileId: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _selectedProfile.value = repository.getProfile(profileId)
                _certifications.value = repository.getCertifications(profileId)
                _errorMessage.value = null
            } catch (e: Exception) {
                _errorMessage.value = e.message
            } finally {
                _isLoading.value = false
            }
        }
    }
}

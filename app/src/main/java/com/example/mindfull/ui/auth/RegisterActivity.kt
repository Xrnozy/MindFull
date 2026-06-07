package com.example.mindfull.ui.auth

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.mindfull.MindfullApplication
import com.example.mindfull.R
import kotlinx.coroutines.launch

class RegisterActivity : AppCompatActivity() {

    private val viewModel: AuthViewModel by viewModels {
        AuthViewModelFactory((application as MindfullApplication).authRepository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_register)

        val nameInput = findViewById<EditText>(R.id.name_input)
        val emailInput = findViewById<EditText>(R.id.email_input)
        val passwordInput = findViewById<EditText>(R.id.password_input)
        val registerButton = findViewById<Button>(R.id.register_button)
        val loginLink = findViewById<TextView>(R.id.login_link)
        val loadingProgress = findViewById<ProgressBar>(R.id.loading_progress)

        registerButton.setOnClickListener {
            val name = nameInput.text.toString()
            val email = emailInput.text.toString()
            val password = passwordInput.text.toString()
            if (name.isNotEmpty() && email.isNotEmpty() && password.isNotEmpty()) {
                viewModel.register(email, password, name)
            } else {
                Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show()
            }
        }

        loginLink.setOnClickListener {
            finish()
        }

        lifecycleScope.launch {
            viewModel.isLoading.collect { isLoading ->
                loadingProgress.visibility = if (isLoading) View.VISIBLE else View.GONE
                registerButton.isEnabled = !isLoading
            }
        }

        lifecycleScope.launch {
            viewModel.authState.collect { result ->
                when (result) {
                    is AuthViewModel.AuthResult.RegisterSuccess -> {
                        Toast.makeText(this@RegisterActivity, "Registration successful! Please login.", Toast.LENGTH_LONG).show()
                        finish()
                    }
                    is AuthViewModel.AuthResult.Error -> {
                        Toast.makeText(this@RegisterActivity, result.message, Toast.LENGTH_LONG).show()
                    }
                    else -> {}
                }
            }
        }
    }
}

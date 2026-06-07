package com.example.mindfull.ui.auth

import android.content.Intent
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
import com.example.mindfull.MainActivity
import com.example.mindfull.MindfullApplication
import com.example.mindfull.R
import kotlinx.coroutines.launch

class LoginActivity : AppCompatActivity() {

    private val viewModel: AuthViewModel by viewModels {
        AuthViewModelFactory((application as MindfullApplication).authRepository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

        val emailInput = findViewById<EditText>(R.id.email_input)
        val passwordInput = findViewById<EditText>(R.id.password_input)
        val loginButton = findViewById<Button>(R.id.login_button)
        val registerLink = findViewById<TextView>(R.id.register_link)
        val loadingProgress = findViewById<ProgressBar>(R.id.loading_progress)

        loginButton.setOnClickListener {
            val email = emailInput.text.toString()
            val password = passwordInput.text.toString()
            if (email.isNotEmpty() && password.isNotEmpty()) {
                viewModel.login(email, password)
            } else {
                Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show()
            }
        }

        registerLink.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
        }

        lifecycleScope.launch {
            viewModel.isLoading.collect { isLoading ->
                loadingProgress.visibility = if (isLoading) View.VISIBLE else View.GONE
                loginButton.isEnabled = !isLoading
            }
        }

        lifecycleScope.launch {
            viewModel.authState.collect { result ->
                when (result) {
                    is AuthViewModel.AuthResult.Success -> {
                        startActivity(Intent(this@LoginActivity, MainActivity::class.java))
                        finish()
                    }
                    is AuthViewModel.AuthResult.Error -> {
                        Toast.makeText(this@LoginActivity, result.message, Toast.LENGTH_LONG).show()
                    }
                    else -> {}
                }
            }
        }
    }
}

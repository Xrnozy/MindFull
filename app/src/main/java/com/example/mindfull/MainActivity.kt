package com.example.mindfull

import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.transition.AutoTransition
import androidx.transition.TransitionManager
import com.example.mindfull.ui.HomeViewModelFactory
import com.example.mindfull.ui.auth.LoginActivity
import com.example.mindfull.ui.coach.PromptCoachViewModel
import com.example.mindfull.ui.coach.PromptCoachViewModelFactory
import com.example.mindfull.ui.forest.ForestViewModel
import com.example.mindfull.ui.forest.ForestViewModelFactory
import com.example.mindfull.ui.greenmap.GreenMapViewModel
import com.example.mindfull.ui.greenmap.GreenMapViewModelFactory
import com.example.mindfull.ui.home.HomeViewModel
import com.example.mindfull.ui.thinkahead.ThinkAheadViewModel
import com.example.mindfull.ui.thinkahead.ThinkAheadViewModelFactory
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.MapView
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.android.material.card.MaterialCardView
import kotlinx.coroutines.launch
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var contentArea: ViewGroup
    private lateinit var viewHome: View
    private lateinit var viewCoach: View
    private lateinit var viewThinkAhead: View
    private lateinit var viewImpact: View
    private lateinit var viewForest: View
    private lateinit var viewGreenMap: View
    private lateinit var logoutButton: ImageButton

    // UI elements for Forest
    private lateinit var forestStatusText: TextView
    private lateinit var plantTreeButton: Button
    private lateinit var treesList: LinearLayout
    private lateinit var communityGoalsList: LinearLayout

    // UI elements for GreenMap
    private lateinit var ecoProfilesList: LinearLayout
    private lateinit var greenMapView: MapView
    private var googleMap: GoogleMap? = null

    // UI elements for Home
    private lateinit var userLevelText: TextView
    private lateinit var userXpText: TextView
    private lateinit var xpProgress: ProgressBar
    private lateinit var greetingText: TextView
    private lateinit var streakValueText: TextView
    private lateinit var greenPointsText: TextView
    private lateinit var carbonValueText: TextView
    private lateinit var waterValueText: TextView
    private lateinit var electricityValueText: TextView
    private lateinit var promptsCountText: TextView
    private lateinit var scoreValueText: TextView
    private lateinit var dependencyScoreText: TextView
    private lateinit var treesPlantedText: TextView
    private lateinit var mascotAdviceText: TextView

    // UI elements for Prompt Coach
    private lateinit var coachUserLevelText: TextView
    private lateinit var coachUserXpText: TextView
    private lateinit var coachXpProgress: ProgressBar
    private lateinit var promptInput: EditText
    private lateinit var analyzeButton: Button
    private lateinit var coachLoading: ProgressBar
    private lateinit var analysisResultsContainer: View
    private lateinit var efficiencyScoreText: TextView
    private lateinit var modelRecommendationText: TextView
    private lateinit var tokenPreviewText: TextView
    private lateinit var carbonPreviewText: TextView
    private lateinit var feedbackList: LinearLayout

    // UI elements for Think-A-Head
    private lateinit var thinkDependencyScoreText: TextView
    private lateinit var reflectionInput: EditText
    private lateinit var reflectButton: Button
    private lateinit var reflectionResults: View
    private lateinit var reflectionQuestionsList: LinearLayout
    private lateinit var retentionList: LinearLayout

    private val homeViewModel: HomeViewModel by viewModels {
        val app = application as MindfullApplication
        HomeViewModelFactory(app.userRepository, app.sustainabilityRepository)
    }

    private val coachViewModel: PromptCoachViewModel by viewModels {
        val app = application as MindfullApplication
        PromptCoachViewModelFactory(app.promptCoachRepository)
    }

    private val thinkAheadViewModel: ThinkAheadViewModel by viewModels {
        val app = application as MindfullApplication
        ThinkAheadViewModelFactory(app.thinkAheadRepository)
    }

    private val forestViewModel: ForestViewModel by viewModels {
        val app = application as MindfullApplication
        ForestViewModelFactory(app.forestRepository)
    }

    private val greenMapViewModel: GreenMapViewModel by viewModels {
        val app = application as MindfullApplication
        GreenMapViewModelFactory(app.greenMapRepository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        
        contentArea = findViewById(R.id.content_area)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, 0, systemBars.right, 0)
            insets
        }

        initViews()
        setupNavigation()
        setupLogout()
        setupCoach()
        setupThinkAhead()
        setupForest()
        setupGreenMap()
        observeViewModels()
        
        greenMapView.onCreate(savedInstanceState)
        greenMapView.getMapAsync { map ->
            googleMap = map
            map.uiSettings.isZoomControlsEnabled = true
        }
        
        homeViewModel.loadDashboardData()
        thinkAheadViewModel.loadData()
    }

    private fun initViews() {
        viewHome = findViewById(R.id.view_home)
        viewCoach = findViewById(R.id.view_coach)
        viewThinkAhead = findViewById(R.id.view_think_ahead)
        viewImpact = findViewById(R.id.view_impact)
        viewForest = findViewById(R.id.view_forest)
        viewGreenMap = findViewById(R.id.view_greenmap)
        logoutButton = findViewById(R.id.logout_button)

        // Home
        userLevelText = findViewById(R.id.user_level_text)
        userXpText = findViewById(R.id.user_xp_text)
        xpProgress = findViewById(R.id.xp_progress)
        greetingText = findViewById(R.id.greeting_text)
        streakValueText = findViewById(R.id.streak_value_text)
        greenPointsText = findViewById(R.id.green_points_text)
        carbonValueText = findViewById(R.id.carbon_value_text)
        waterValueText = findViewById(R.id.water_value_text)
        electricityValueText = findViewById(R.id.electricity_value_text)
        promptsCountText = findViewById(R.id.prompts_count_text)
        scoreValueText = findViewById(R.id.score_value_text)
        dependencyScoreText = findViewById(R.id.dependency_score_text)
        treesPlantedText = findViewById(R.id.trees_planted_text)
        mascotAdviceText = findViewById(R.id.mascot_advice_text)

        // Coach
        coachUserLevelText = findViewById(R.id.coach_user_level_text)
        coachUserXpText = findViewById(R.id.coach_user_xp_text)
        coachXpProgress = findViewById(R.id.coach_xp_progress)
        promptInput = findViewById(R.id.prompt_input)
        analyzeButton = findViewById(R.id.analyze_button)
        coachLoading = findViewById(R.id.coach_loading)
        analysisResultsContainer = findViewById(R.id.analysis_results_container)
        efficiencyScoreText = findViewById(R.id.efficiency_score_text)
        modelRecommendationText = findViewById(R.id.model_recommendation_text)
        tokenPreviewText = findViewById(R.id.token_preview_text)
        carbonPreviewText = findViewById(R.id.carbon_preview_text)
        feedbackList = findViewById(R.id.feedback_list)

        // Think-A-Head
        thinkDependencyScoreText = findViewById(R.id.think_dependency_score_text)
        reflectionInput = findViewById(R.id.reflection_input)
        reflectButton = findViewById(R.id.reflect_button)
        reflectionResults = findViewById(R.id.reflection_results)
        reflectionQuestionsList = findViewById(R.id.reflection_questions_list)
        retentionList = findViewById(R.id.retention_list)

        // Forest
        forestStatusText = findViewById(R.id.forest_status_text)
        plantTreeButton = findViewById(R.id.plant_tree_button)
        treesList = findViewById(R.id.trees_list)
        communityGoalsList = findViewById(R.id.community_goals_list)

        // GreenMap
        ecoProfilesList = findViewById(R.id.eco_profiles_list)
        greenMapView = findViewById(R.id.green_map_view)
    }

    private fun setupCoach() {
        analyzeButton.setOnClickListener {
            val text = promptInput.text.toString()
            if (text.isNotBlank()) {
                coachViewModel.analyzePrompt(text)
            } else {
                Toast.makeText(this, "Please enter a prompt", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun setupThinkAhead() {
        reflectButton.setOnClickListener {
            val text = reflectionInput.text.toString()
            if (text.isNotBlank()) {
                thinkAheadViewModel.requestReflection(text)
            } else {
                Toast.makeText(this, "What are you thinking about?", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun setupForest() {
        plantTreeButton.setOnClickListener {
            forestViewModel.plantTree()
        }
    }

    private fun setupGreenMap() {
        greenMapViewModel.loadProfiles()
    }

    private fun observeViewModels() {
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                // Home observations
                launch {
                    homeViewModel.userProfile.collect { profile ->
                        profile?.let { greetingText.text = "Hello, ${it.full_name ?: "Explorer"}." }
                    }
                }
                launch {
                    homeViewModel.userStats.collect { stats ->
                        stats?.let {
                            userLevelText.text = "Level ${it.level}"
                            userXpText.text = "${it.total_xp} XP"
                            xpProgress.progress = it.total_xp % 100
                            
                            // Also update Coach section stats
                            coachUserLevelText.text = "Level ${it.level}"
                            coachUserXpText.text = "${it.total_xp} XP"
                            coachXpProgress.progress = it.total_xp % 100

                            streakValueText.text = "${it.current_streak}d"
                            greenPointsText.text = it.green_points.toString()
                            carbonValueText.text = "${it.total_carbon_g.toInt()}g"
                            waterValueText.text = "${it.total_water_ml.toInt()}ml"
                            electricityValueText.text = "${it.total_electricity_wh.toInt()}Wh"
                            promptsCountText.text = it.total_prompts.toString()
                            dependencyScoreText.text = "Dependency: ${if(it.dependency_score < 0.3) "Low" else "Medium"}"
                            treesPlantedText.text = "${it.trees_planted} trees planted"
                        }
                    }
                }
                launch {
                    homeViewModel.mascotAdvice.collect { advice ->
                        mascotAdviceText.text = advice
                    }
                }
                launch {
                    homeViewModel.sustainabilityScore.collect { score ->
                        score?.let {
                            scoreValueText.text = when {
                                it.score > 0.8 -> "A+"
                                it.score > 0.6 -> "B"
                                else -> "C"
                            }
                        }
                    }
                }

                // Coach observations
                launch {
                    coachViewModel.isLoading.collect { isLoading ->
                        coachLoading.visibility = if (isLoading) View.VISIBLE else View.GONE
                        analyzeButton.isEnabled = !isLoading
                        if (isLoading) analysisResultsContainer.visibility = View.GONE
                    }
                }
                launch {
                    coachViewModel.errorMessage.collect { error ->
                        error?.let { Toast.makeText(this@MainActivity, it, Toast.LENGTH_LONG).show() }
                    }
                }
                launch {
                    coachViewModel.analysisResult.collect { result ->
                        result?.let {
                            analysisResultsContainer.visibility = View.VISIBLE
                            val rawScore = it.efficiency_score
                            // If API returns 0.0-1.0, multiply by 100. If it returns 0-100, use as is.
                            val displayScore = if (rawScore <= 1.0) (rawScore * 100).toInt() else rawScore.toInt()
                            efficiencyScoreText.text = "${displayScore}%"
                            modelRecommendationText.text = "Recommended: ${it.recommended_model}"
                            tokenPreviewText.text = "${it.token_prediction} tokens"
                            carbonPreviewText.text = "${String.format(Locale.getDefault(), "%.2f", it.carbon_prediction)}g CO2e"
                            
                            feedbackList.removeAllViews()
                            it.suggestions.forEach { suggestion ->
                                val tv = TextView(this@MainActivity).apply {
                                    text = "• $suggestion"
                                    setPadding(0, 4, 0, 4)
                                    setTextColor(getColor(R.color.brand_inactive))
                                }
                                feedbackList.addView(tv)
                            }
                        }
                    }
                }

                // Think-A-Head observations
                launch {
                    thinkAheadViewModel.dependencyScore.collect { score ->
                        score?.let {
                            thinkDependencyScoreText.text = String.format(Locale.getDefault(), "%.2f", it.score)
                        }
                    }
                }
                launch {
                    thinkAheadViewModel.reflection.collect { reflection ->
                        reflection?.let {
                            reflectionResults.visibility = View.VISIBLE
                            reflectionQuestionsList.removeAllViews()
                            it.reflection_questions.forEach { question ->
                                val tv = TextView(this@MainActivity).apply {
                                    text = question
                                    setPadding(0, 8, 0, 8)
                                    setTypeface(null, Typeface.BOLD)
                                    setTextColor(getColor(R.color.brand_primary))
                                }
                                reflectionQuestionsList.addView(tv)
                            }
                        }
                    }
                }
                launch {
                    thinkAheadViewModel.retention.collect { items ->
                        retentionList.removeAllViews()
                        items.take(3).forEach { item ->
                            val card = MaterialCardView(this@MainActivity).apply {
                                layoutParams = LinearLayout.LayoutParams(
                                    LinearLayout.LayoutParams.MATCH_PARENT,
                                    LinearLayout.LayoutParams.WRAP_CONTENT
                                ).apply { setMargins(0, 0, 0, 8) }
                                radius = 12f
                                cardElevation = 0f
                                setCardBackgroundColor(getColor(R.color.white))
                                
                                val inner = LinearLayout(this@MainActivity).apply {
                                    orientation = LinearLayout.VERTICAL
                                    setPadding(16, 16, 16, 16)
                                }
                                inner.addView(TextView(this@MainActivity).apply {
                                    text = item.topic
                                    setTypeface(null, Typeface.BOLD)
                                    setTextColor(getColor(R.color.brand_primary))
                                })
                                inner.addView(TextView(this@MainActivity).apply {
                                    text = "Understanding: ${(item.retention_score * 100).toInt()}%"
                                    textSize = 12f
                                    setTextColor(getColor(R.color.brand_inactive))
                                })
                                addView(inner)
                            }
                            retentionList.addView(card)
                        }
                    }
                }

                // Forest observations
                launch {
                    forestViewModel.forest.collect { forest ->
                        forest?.let {
                            forestStatusText.text = "Status: ${it.level} (${it.total_green_points} GP)"
                        }
                    }
                }
                launch {
                    forestViewModel.trees.collect { trees ->
                        treesList.removeAllViews()
                        trees.forEach { tree ->
                            val tv = TextView(this@MainActivity).apply {
                                text = "🌲 ${tree.species} (${tree.status})"
                                setPadding(0, 8, 0, 8)
                                setTextColor(getColor(R.color.brand_primary))
                            }
                            treesList.addView(tv)
                        }
                    }
                }
                launch {
                    forestViewModel.communityGoals.collect { goals ->
                        communityGoalsList.removeAllViews()
                        goals.forEach { goal ->
                            val tv = TextView(this@MainActivity).apply {
                                text = "🎯 ${goal.title}: ${goal.current_value}/${goal.target_value} ${goal.unit}"
                                setPadding(0, 8, 0, 8)
                                setTextColor(getColor(R.color.brand_inactive))
                            }
                            communityGoalsList.addView(tv)
                        }
                    }
                }

                // GreenMap observations
                launch {
                    greenMapViewModel.profiles.collect { profiles ->
                        ecoProfilesList.removeAllViews()
                        googleMap?.clear()
                        
                        profiles.forEach { profile ->
                            // Add marker to map if coordinates exist
                            if (profile.latitude != null && profile.longitude != null) {
                                val pos = LatLng(profile.latitude, profile.longitude)
                                googleMap?.addMarker(
                                    MarkerOptions()
                                        .position(pos)
                                        .title(profile.name)
                                        .snippet("Score: ${(profile.sustainability_score * 100).toInt()}%")
                                )
                                // Move camera to the first one for now
                                if (profiles.indexOf(profile) == 0) {
                                    googleMap?.moveCamera(CameraUpdateFactory.newLatLngZoom(pos, 10f))
                                }
                            }

                            val card = MaterialCardView(this@MainActivity).apply {
                                layoutParams = LinearLayout.LayoutParams(
                                    LinearLayout.LayoutParams.MATCH_PARENT,
                                    LinearLayout.LayoutParams.WRAP_CONTENT
                                ).apply { setMargins(0, 0, 0, 12) }
                                radius = 16f
                                cardElevation = 0f
                                setCardBackgroundColor(getColor(R.color.white))
                                
                                val inner = LinearLayout(this@MainActivity).apply {
                                    orientation = LinearLayout.VERTICAL
                                    setPadding(16, 16, 16, 16)
                                }
                                inner.addView(TextView(this@MainActivity).apply {
                                    text = profile.name
                                    setTypeface(null, Typeface.BOLD)
                                    textSize = 16f
                                    setTextColor(getColor(R.color.brand_primary))
                                })
                                inner.addView(TextView(this@MainActivity).apply {
                                    text = "Sustainability Score: ${(profile.sustainability_score * 100).toInt()}%"
                                    textSize = 12f
                                    setTextColor(getColor(R.color.brand_inactive))
                                })
                                addView(inner)
                            }
                            ecoProfilesList.addView(card)
                        }
                    }
                }
            }
        }
    }

    private fun setupLogout() {
        logoutButton.setOnClickListener {
            lifecycleScope.launch {
                val app = application as MindfullApplication
                app.authRepository.logout()
                startActivity(Intent(this@MainActivity, LoginActivity::class.java))
                finish()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        greenMapView.onResume()
    }

    override fun onPause() {
        super.onPause()
        greenMapView.onPause()
    }

    override fun onDestroy() {
        super.onDestroy()
        greenMapView.onDestroy()
    }

    override fun onLowMemory() {
        super.onLowMemory()
        greenMapView.onLowMemory()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        greenMapView.onSaveInstanceState(outState)
    }

    private fun setupNavigation() {
        val bottomNav = findViewById<BottomNavigationView>(R.id.bottom_nav)
        bottomNav.setOnItemSelectedListener { item ->
            val tab = when (item.itemId) {
                R.id.nav_home -> "home"
                R.id.nav_coach -> "coach"
                R.id.nav_think_ahead -> "think_ahead"
                R.id.nav_forest -> "forest"
                R.id.nav_greenmap -> "greenmap"
                else -> "home"
            }
            setActiveTab(tab)
            true
        }
    }

    private fun setActiveTab(tab: String) {
        TransitionManager.beginDelayedTransition(contentArea, AutoTransition().setDuration(200))
        viewHome.visibility = View.GONE
        viewCoach.visibility = View.GONE
        viewThinkAhead.visibility = View.GONE
        viewImpact.visibility = View.GONE
        viewForest.visibility = View.GONE
        viewGreenMap.visibility = View.GONE

        when (tab) {
            "home" -> viewHome.visibility = View.VISIBLE
            "coach" -> viewCoach.visibility = View.VISIBLE
            "think_ahead" -> viewThinkAhead.visibility = View.VISIBLE
            "impact" -> viewImpact.visibility = View.VISIBLE
            "forest" -> {
                viewForest.visibility = View.VISIBLE
                forestViewModel.loadData()
            }
            "greenmap" -> viewGreenMap.visibility = View.VISIBLE
        }
    }
}

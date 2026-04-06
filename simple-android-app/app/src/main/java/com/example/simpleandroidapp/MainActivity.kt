package com.example.simpleandroidapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.simpleandroidapp.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ideaChipOne.setOnClickListener {
            binding.ideaInput.setText(getString(R.string.idea_chip_one_value))
        }
        binding.ideaChipTwo.setOnClickListener {
            binding.ideaInput.setText(getString(R.string.idea_chip_two_value))
        }
        binding.ideaChipThree.setOnClickListener {
            binding.ideaInput.setText(getString(R.string.idea_chip_three_value))
        }
        binding.ideaChipFour.setOnClickListener {
            binding.ideaInput.setText(getString(R.string.idea_chip_four_value))
        }

        binding.generateButton.setOnClickListener {
            generateApp()
        }
    }

    private fun generateApp() {
        val rawIdea = binding.ideaInput.text?.toString()?.trim().orEmpty()
        val idea = if (rawIdea.isBlank()) getString(R.string.default_idea) else rawIdea

        binding.resultNameText.text = buildAppName(idea)
        binding.resultSummaryText.text = getString(R.string.generated_summary, idea)
        binding.resultFeaturesText.text = buildFeatureList(idea)
        binding.resultStatusText.text = getString(R.string.generated_status)
    }

    private fun buildAppName(idea: String): String {
        val words = idea.split(" ")
            .map { it.trim().replace(Regex("[^A-Za-z0-9]"), "") }
            .filter { it.isNotBlank() }
            .take(2)
            .joinToString(" ")

        return if (words.isBlank()) {
            getString(R.string.fallback_app_name)
        } else {
            "$words ${getString(R.string.app_name_suffix)}"
        }
    }

    private fun buildFeatureList(idea: String): String {
        return getString(
            R.string.generated_features,
            idea,
            idea,
            idea
        )
    }
}

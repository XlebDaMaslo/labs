package com.example.andloc

import android.Manifest
import android.content.pm.PackageManager
import android.location.Location
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.*
import kotlinx.coroutines.*
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

class MainActivity : AppCompatActivity() {
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private val handler = Handler(Looper.getMainLooper())
    private val interval: Long = 5000 // 5 секунд
    private var job: Job? = null

    // Интерфейс для работы с сервером
    interface ApiService {
        @POST("/location")
        suspend fun sendLocation(@Body locationData: LocationData)
    }

    // Данные о местоположении
    data class LocationData(val latitude: Double, val longitude: Double)

    private val retrofit = Retrofit.Builder()
        .baseUrl("https://yourserver.com") // Замените на свой URL сервера
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val apiService = retrofit.create(ApiService::class.java)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)

        findViewById<Button>(R.id.startButton).setOnClickListener {
            startSendingLocation()
        }

        findViewById<Button>(R.id.stopButton).setOnClickListener {
            stopSendingLocation()
        }
    }

    private fun startSendingLocation() {
        job = CoroutineScope(Dispatchers.IO).launch {
            while (isActive) {
                sendLocationToServer()
                delay(interval)
            }
        }
    }

    private fun stopSendingLocation() {
        job?.cancel()
    }

    private suspend fun sendLocationToServer() {
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                1001
            )
            return
        }

        fusedLocationClient.lastLocation.addOnSuccessListener { location: Location? ->
            location?.let {
                val locationData = LocationData(it.latitude, it.longitude)
                CoroutineScope(Dispatchers.IO).launch {
                    try {
                        apiService.sendLocation(locationData)
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }
            }
        }
    }
}

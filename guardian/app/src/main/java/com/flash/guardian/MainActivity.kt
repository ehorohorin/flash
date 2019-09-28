package com.flash.guardian

import android.Manifest
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import com.google.gson.Gson
import com.google.zxing.BarcodeFormat
import com.google.zxing.ResultPoint
import com.journeyapps.barcodescanner.BarcodeCallback
import com.journeyapps.barcodescanner.BarcodeResult
import com.journeyapps.barcodescanner.DefaultDecoderFactory
import com.tbruyelle.rxpermissions2.RxPermissions
import io.reactivex.disposables.Disposable
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    private var disposable: Disposable? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        disposable = RxPermissions(this).request(Manifest.permission.CAMERA).subscribe {
            if (it) {
                zxing_barcode_scanner.barcodeView.decoderFactory = DefaultDecoderFactory(listOf(BarcodeFormat.QR_CODE))
                zxing_barcode_scanner.decodeContinuous(barcodeCallback)
            } else {
                Toast.makeText(this, "Need camera permission", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        zxing_barcode_scanner.resume()
    }

    override fun onPause() {
        super.onPause()
        zxing_barcode_scanner.pause()
    }

    override fun onDestroy() {
        super.onDestroy()
        disposable?.dispose()
    }

    private val barcodeCallback = object : BarcodeCallback {
        override fun barcodeResult(result: BarcodeResult?) {
            result?.text?.let {
                zxing_barcode_scanner.pause()
                Log.d("SCANNER READ", it)
                try {
                    val data = Gson().fromJson(it, Ticket::class.java)
                    checkTicket(data)
                } catch (e: Exception) {
                    zxing_barcode_scanner.resume()
                    Log.d("SCANNER PARSE", e.message ?: "unknown error parse data")
                }
            }
        }

        override fun possibleResultPoints(resultPoints: MutableList<ResultPoint>?) {
        }

    }

    private fun checkTicket(data: Ticket) {
        AlertDialog.Builder(this)
            .setTitle("Билет")
            .setMessage(if (data.valid) "Билет проверен" else "Билет недействителен!")
            .setCancelable(false)
            .setPositiveButton("OK") { _, _ ->
                zxing_barcode_scanner.resume()
            }
            .show()
    }
}

package com.flash.guardian

import com.google.gson.annotations.SerializedName

data class Ticket (
    @SerializedName("name") val name : String,
    @SerializedName("parkzone") val parkzone : String,
    @SerializedName("passport") val passport : String,
    @SerializedName("signature") val signature : String,
    @SerializedName("valid_after") val valid_after : String,
    @SerializedName("valid_before") val valid_before : String
//    var valid: Boolean = false
//    var name: String = ""
//    var parkzone: String = ""

// var isValid() : Boolean = false (return false)

)

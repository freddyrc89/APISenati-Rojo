package com.freddy.proyectoqrasistencia.network

import com.freddy.proyectoqrasistencia.model.Invitado
import com.freddy.proyectoqrasistencia.model.RegistroResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

// Define los endpoints
interface InvitadoApiService {

    @POST("/invitado")
    fun registrarInvitado(@Body invitado: Invitado): Call<RegistroResponse>

    @GET("/invitados")
    fun listarInvitados(): Call<List<Invitado>>
}
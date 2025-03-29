package com.freddy.proyectoqrasistencia.model

    data class Invitado(
        val nombre: String,
        val apellido: String
    )

    data class RegistroResponse(
        val mensaje: String,
        val invitado: Invitado
    )

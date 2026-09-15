const botonChat = document.getElementById("botonChat");
const cerrarChat = document.getElementById("cerrarChat");

const chatbot = document.getElementById("chatbot");

const entrada = document.getElementById("entrada");
const enviar = document.getElementById("enviar");

const mensajes = document.getElementById("mensajes");


// ABRIR CHAT

botonChat.addEventListener("click", function() {

    chatbot.style.display = "flex";

    entrada.focus();

});


// CERRAR CHAT

cerrarChat.addEventListener("click", function() {

    chatbot.style.display = "none";

});


// ENVIAR MENSAJE

enviar.addEventListener("click", enviarMensaje);


// PRESIONAR ENTER

entrada.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        enviarMensaje();

    }

});


// FUNCIÓN PRINCIPAL

function enviarMensaje() {

    const pregunta = entrada.value.trim();

    if (pregunta === "") {
        return;
    }


    // Mostrar pregunta del usuario

    agregarMensaje(pregunta, "usuario");


    // Limpiar campo

    entrada.value = "";


    // Generar respuesta

    setTimeout(function() {

        const respuesta = responderPregunta(pregunta);

        agregarMensaje(respuesta, "bot");

    }, 500);

}


// AGREGAR MENSAJE

function agregarMensaje(texto, tipo) {

    const mensaje = document.createElement("div");

    mensaje.classList.add("mensaje");

    if (tipo === "usuario") {

        mensaje.classList.add("usuario");

    } else {

        mensaje.classList.add("bot");

    }

    mensaje.innerHTML = texto;

    mensajes.appendChild(mensaje);

    mensajes.scrollTop = mensajes.scrollHeight;

}


// RESPUESTAS

function responderPregunta(pregunta) {

    const texto = pregunta.toLowerCase();


    if (
        texto.includes("servicio") ||
        texto.includes("servicios")
    ) {

        return `
            SOLDESP ofrece servicios relacionados con
            ingeniería, fabricación, soldadura y
            mantenimiento industrial.
        `;

    }


    if (
        texto.includes("cotización") ||
        texto.includes("cotizacion") ||
        texto.includes("presupuesto")
    ) {

        return `
            Para solicitar una cotización puedes
            comunicarte con SOLDESP mediante nuestros
            canales de contacto y proporcionar los
            detalles de tu requerimiento.
        `;

    }


    if (
        texto.includes("ubicación") ||
        texto.includes("ubicacion") ||
        texto.includes("dónde") ||
        texto.includes("donde")
    ) {

        return `
            SOLDESP se encuentra en Ilo, Moquegua,
            Perú.
        `;

    }


    if (
        texto.includes("contacto") ||
        texto.includes("teléfono") ||
        texto.includes("telefono")
    ) {

        return `
            Puedes comunicarte con SOLDESP mediante
            sus canales oficiales de contacto.
        `;

    }


    if (
        texto.includes("soldadura")
    ) {

        return `
            SOLDESP desarrolla trabajos relacionados
            con soldadura industrial y fabricación de
            estructuras.
        `;

    }


    if (
        texto.includes("hola") ||
        texto.includes("buenas")
    ) {

        return `
            ¡Hola! 👋 Soy el asistente virtual de
            SOLDESP. ¿Qué información necesitas?
        `;

    }


    return `
        No encontré una respuesta específica para
        tu consulta.

        Puedes preguntar sobre nuestros servicios,
        cotizaciones, soldadura, ubicación o contacto.
    `;

}
const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const OpenAI = require("openai");

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

app.post("/chat", async (req, res) => {

    try {

        const pregunta = req.body.pregunta;

        if (!pregunta) {
            return res.status(400).json({
                error: "No se recibió ninguna pregunta."
            });
        }

        const respuesta = await client.responses.create({

            model: "gpt-5.6-luna",

            instructions: `
            Eres el Asistente Virtual de SOLDESP.

            Tu función es ayudar a los visitantes de la página
            web de SOLDESP con información sobre sus servicios,
            contacto, cotizaciones y orientación general.

            SOLDESP es una empresa relacionada con ingeniería,
            soldadura y servicios industriales.

            Información disponible:

            - Ubicación: Ilo, Moquegua - Perú.
            - Teléfono: (053) 495247.
            - Celular: 953660826.
            - Correo: recursos.humanos@soldesp.com.pe.
            - Horario:
              Lunes a viernes: 8:00 a.m. - 4:00 p.m.
              Sábados: 8:00 a.m. - 12:00 p.m.

            Algunos servicios de SOLDESP incluyen:

            - Alquiler de equipos.
            - Servicios de fabricación.
            - Mantenimiento de plantas industriales.
            - Mantenimiento de plantas desalinizadoras.
            - Caldería, fabricación y montaje de estructuras metálicas.
            - Fabricación y montaje de piping/spool.
            - Soldaduras especiales.
            - Arenado y pintura.
            - Digitalización de planos.

            Reglas:

            1. Responde siempre en español.
            2. Sé claro y fácil de entender.
            3. No inventes información sobre SOLDESP.
            4. Si no tienes información suficiente, indícalo.
            5. Para cotizaciones específicas, recomienda contactar
               directamente con SOLDESP.
            6. No prometas precios, fechas o trabajos que no estén
               confirmados.
            7. Mantén las respuestas breves y útiles.
            `,

            input: pregunta
        });

        res.json({
            respuesta: respuesta.output_text
        });

    } catch (error) {

        console.error(error);

        res.status(500).json({
            error: "Ocurrió un error al comunicarse con el asistente."
        });
    }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {

    console.log(`Servidor SOLDESP ejecutándose en http://localhost:${PORT}`);

});
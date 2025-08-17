from django.db.models.signals import post_save  # guardar o crear
from django.dispatch import receiver  # para recibir señales con un decorador
from .models import BitacoraModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Desde bitacoramodel recibimos:
# usuario (tiene su salario quincenal)
# incidencia (prompt)
# nota (opcionalmente recibimos mas detalles)
# Si es que se cubrio un puesto diferente
# El salario/puesto que se cubrio (solo aplica si se cubrio un puesto diferente)


@receiver(post_save, sender=BitacoraModel)
def actualizar_bitacora(sender, instance, created, **kwargs):
    if not created:
        # Lógica para actualizar el estado de una bitacora
        # si el estado cambia a "resuelta", se calcula el monto de la incidencia
        if instance.estado == "resuelta":
            prompt = f"""
            Eres un sistema de cálculo de incidencias de nómina. 
            Debes devolver exclusivamente un número entero o decimal positivo que represente el monto de dinero asociado a la incidencia en pesos mexicanos. 
            No incluyas texto adicional, ni explicaciones, ni símbolos.

            Datos del empleado:
            - Salario quincenal: {instance.usuario.salario}

            Incidencia:
            {instance.incidencia.prompt}

            Detalles adicionales:
            - Nota: {instance.nota}
            - ¿Cubrió un puesto diferente?: {instance.cubre_puesto}
            - Salario del puesto cubierto (si aplica): {instance.salario}

            Reglas de cálculo:
            1. Todas las incidencias se calculan en proporción al salario quincenal del empleado:
            - Un día adicional de trabajo → salario_quincenal / 15.
            - Medio día → salario_quincenal / 30.
            - Porcentajes u otros conceptos → aplicarlos sobre el salario_quincenal.
            - Faltas o descuentos → se calculan igual que los pagos, pero siempre se devuelven en valor absoluto (positivo).

            2. Si cubre un puesto diferente:
            - Calcula la diferencia entre el salario quincenal del puesto cubierto y el salario quincenal del empleado.
            - Si la diferencia es positiva, súmala al cálculo final.
            - Si la diferencia es negativa o cero, ignórala (se mantiene el salario base del empleado).

            3. Si el empleado hace un turno extra cubriendo un puesto diferente:
            - Calcula el monto del turno extra según la incidencia (ejemplo: un día adicional = salario_quincenal / 15).
            - Calcula la diferencia de salario entre el puesto cubierto y el del empleado.
            - El monto final es: diferencia_de_salario + monto_turno_extra.

            4. Siempre devuelve únicamente el número positivo resultante (ejemplo: 300, 150, 450.50).
            """
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=1,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=False,
                stop=None,
            )
            monto = completion.choices[0].message.content.strip()
            monto = float(monto) if monto else 0
            # Actualizar sin disparar señal
            BitacoraModel.objects.filter(pk=instance.pk).update(monto=monto)
        elif instance.estado == "rechazada":
            BitacoraModel.objects.filter(pk=instance.pk).update(monto=0)

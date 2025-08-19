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
            salario_puesto_cubierto = (
                instance.salario.monto if instance.salario else "No aplica"
            )
            prompt = f"""
            Eres un sistema de cálculo de incidencias de nómina. 
            Debes devolver exclusivamente un número entero o decimal positivo que represente el monto de dinero asociado a la incidencia en pesos mexicanos. 
            No incluyas texto adicional, ni explicaciones, ni símbolos.

            Datos del empleado:
            - Salario quincenal del empleado: {instance.usuario.salario.monto}

            Incidencia:
            {instance.incidencia.prompt}

            Detalles adicionales:
            - Nota: {instance.nota}
            - ¿Cubrió un puesto diferente?: {instance.cubre_puesto}
            - Salario del puesto cubierto (si aplica): {salario_puesto_cubierto}

            Reglas de cálculo:

            PASO 1 - Determinar el salario base para el cálculo:
            - Si NO cubre un puesto diferente (cubre_puesto = False): Usar el salario quincenal del empleado.
            - Si SÍ cubre un puesto diferente (cubre_puesto = True): Usar el salario del puesto cubierto.

            PASO 2 - Calcular la incidencia:
            Todas las incidencias se calculan sobre el salario determinado en el PASO 1:
            - Un día adicional de trabajo → salario_base / 15
            - Medio día → salario_base / 30
            - Prima dominical (25%) → (salario_base / 15) * 1.25
            - Porcentajes → aplicarlos sobre el salario_base
            - Faltas o descuentos → calcular igual que los pagos, pero devolver en valor absoluto (positivo)

            Ejemplos:
            - Empleado gana 3000 quincenales, cubre puesto de 4500 quincenales, prima dominical:
              → Cálculo: (4500 / 15) * 1.25 = 300 * 1.25 = 375
            
            - Empleado gana 3000 quincenales, NO cubre otro puesto, prima dominical:
              → Cálculo: (3000 / 15) * 1.25 = 200 * 1.25 = 250

            - Empleado gana 2000 quincenales, cubre puesto de 3500 quincenales, día adicional:
              → Cálculo: 3500 / 15 = 233.33

            IMPORTANTE: Cuando se cubre un puesto diferente, TODOS los cálculos se basan únicamente en el salario del puesto cubierto, NO en el salario del empleado original.

            Devuelve únicamente el número positivo resultante (ejemplo: 300, 150, 450.50).
            """
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=False,
                stop=None,
            )
            monto = completion.choices[0].message.content.strip()
            monto = float(monto) if monto else 0
            monto = round(monto, 2)
            # Actualizar sin disparar señal
            BitacoraModel.objects.filter(pk=instance.pk).update(monto=monto)
        elif instance.estado == "rechazada":
            BitacoraModel.objects.filter(pk=instance.pk).update(monto=0)

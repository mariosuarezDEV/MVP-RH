from groq import Groq


def calculate_incidence():
    client = Groq(api_key="clave")

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "La prima dominical Se otorga a los empleados que laboran en domingo y equivale al 25% del salario diario, como compensación adicional por trabajar en un día de descanso habitual. El empleado Luis Mario gana $6,300 MXN a la quincena, cuanto es el monto de la incidencia mencionada? dame solo el valor en numero\n\n",
            }
        ],
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

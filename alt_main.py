import os
import openai

openai.api_key = "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"


def ask_question(prompt, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
    )

    answer = response.choices[0].text.strip()
    return answer


def diagnose_patient(symptoms, possible_diagnoses):
    context = "You are a medical professional trying to diagnose a patient."
    diagnosis_probabilities = {diagnosis: 0 for diagnosis in possible_diagnoses}

    for symptom in symptoms:
        question = f"What other details can you provide about the symptom: {symptom}?"
        user_response = ask_question(question, context)

        associated_symptoms = generate_associated_symptoms(
            user_response, diagnosis_probabilities
        )

        for other_symptom in associated_symptoms:
            for diagnosis in possible_diagnoses:
                if other_symptom.lower() in user_response.lower():
                    diagnosis_probabilities[diagnosis] += 1

        severity_question = f"On a scale of 1 to 10, how severe is the {symptom}?"
        user_severity_response = int(
            input(ask_question(severity_question, context) + " ")
        )

        severity_factor = user_severity_response / 10
        diagnosis_probabilities[diagnosis] *= severity_factor

    likely_diagnosis = max(diagnosis_probabilities, key=diagnosis_probabilities.get)
    return likely_diagnosis


def generate_associated_symptoms(user_response, diagnosis_probabilities):
    associated_symptoms = []

    associated_symptoms_response = ask_question(
        "What other symptoms are often associated with this condition?", user_response
    )

    if "cough" in associated_symptoms_response:
        associated_symptoms.append("cough")
    if "fatigue" in associated_symptoms_response:
        associated_symptoms.append("fatigue")

    return associated_symptoms


possible_diagnoses = ["Influenza", "Dengue", "Malaria"]
user_symptoms = ["fever", "coughing", "joint pain"]
likely_diagnosis = diagnose_patient(user_symptoms, possible_diagnoses)
print(f"The most likely diagnosis is: {likely_diagnosis}")

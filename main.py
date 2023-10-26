import os
import openai

openai.api_key = "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"


def ask_question(messages):
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response["choices"][0]["message"]


def run_conversation(symptoms, diagnoses):
    messages = [
        {
            "role": "system",
            "content": f"Given the following symptoms you have make a possible diagnosis. The primary diagnosis is {' '.join(diagnoses)}. Ask further questions to make the diagnosis more accurate. The questions must be framed in the way a doctor would ask a patient questions. Just return the questions.",
        },
        {
            "role": "user",
            "content": " ".join(symptoms),
        },
    ]
    response_message = ask_question(messages)
    questions = response_message["content"].split("\n")
    questions.pop()
    questions.pop()
    answers = list()

    for question in questions:
        answers.append(input(str(question) + " : "))

    messages.extend(
        [
            {
                "role": "assistant",
                "content": "\n".join(questions),
            },
            {
                "role": "user",
                "content": "\n".join(answers)
                + ".\nNow Generate a diagnosis using these answers.",
            },
        ]
    )

    diagnosis = ask_question(messages)
    diagnosis = diagnosis["content"]

    name = input("What's your Name? : ")
    age = input("What's your Age : ")

    messages.extend(
        [
            {
                "role": "assistant",
                "content": diagnosis,
            },
            {
                "role": "user",
                "content": f"generate a report from the above information to assist the doctor into making a diagnosis. Age of this patient is {age} and name is {name}",
            },
        ]
    )

    report = ask_question(messages)

    print(report["content"])


preliminary_diagnoses = ["Common Cold", "Influenza"]
user_symptoms = ["coughing", "fever", "body aching", "cold"]
run_conversation(user_symptoms, preliminary_diagnoses)

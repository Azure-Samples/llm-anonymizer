#!/usr/bin/env python3
"""
Example entrypoint for using the PiiAnonymizer class from src/anonymizer.py
"""
from src.anonymizer import PiiAnonymizer
from dotenv import load_dotenv

load_dotenv()


def main() -> None:

    # Define your System Prompt and Sample Text
    system_prompt = "Você é um assistente que identifica a intenção principal do usuário baseado em um input. " \
                    "Retorne apenas a intenção do usuário, não retorne informações sobre o usuário ou informações pessoais." \
                    "Retorne o resultado como um JSON seguindo a estrutura: {\"intention\": \"<user intention>\"}" \
                    "Considere apenas as seguintes intenções: Conhecer cartões de crédito, Informações de Saldo ou Reclamações." \


    # Sample text containing PII
    sample_text = (
        "Olá, meu nome é José Almeida, meu CPF é 379.799.200-90 e meu RG 11.456.264-7. "
        "Meu telefone é (11) 92875-5858 e meu e-mail joalmeida@contoso.com. "
        "Trabalho na Contoso e gostaria de conhecer os cartões de crédito disponíveis para meu perfil."
    )

    # Initialize the anonymizer
    anonymizer = PiiAnonymizer()

    # Recognize entities and generate fake data
    entities = anonymizer.recognize_pii_entities([sample_text])
    fake_data = anonymizer.generate_fake_data(entities)

    # Replace PII with fake values
    anonymized_texts = anonymizer.replace_with_fake_data([sample_text], fake_data)

    # Print results
    print("Original Text:\n", sample_text)
    print("\nAnonymized Text:\n", anonymized_texts[0])

    original_intent = anonymizer.aoai_api_call(input_text=sample_text, system_prompt=system_prompt)
    masked_intent = anonymizer.aoai_api_call(input_text=anonymized_texts[0], system_prompt=system_prompt)

    print("\n")
    print("Intent from original text: %s", original_intent['intention'])
    print("Intent from masked text: %s", masked_intent['intention'])


if __name__ == "__main__":
    main()

import os, json
import logging
from typing import List, Dict, Any
from faker import Faker
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from openai import AzureOpenAI

# configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s: %(message)s"
)

# silence all other loggers (only root will emit INFO+)
for name in list(logging.root.manager.loggerDict):
    if name != "root":
        logging.getLogger(name).setLevel(logging.WARNING)

class PiiRandomizer:
    """Class to handle PII recognition, fake data generation, replacement, and Azure OpenAI calls."""

    def __init__(
        self,
        language_endpoint: str = None,
        language_key: str = None,
        openai_endpoint: str = None,
        openai_key: str = None,
        openai_api_version: str = "2024-02-01",
        model_name: str = "gpt-4o"
    ):
        # Initialize Azure Text Analytics client
        self.language_endpoint = language_endpoint or os.getenv("AZURE_LANGUAGE_ENDPOINT")
        self.language_key = language_key or os.getenv("AZURE_LANGUAGE_KEY")

        if not self.language_endpoint or not self.language_key:
            raise ValueError("Azure Language endpoint and key must be set via arguments or environment variables.")

        self.text_analytics_client = TextAnalyticsClient(
            endpoint=self.language_endpoint,
            credential=AzureKeyCredential(self.language_key)
        )

        # Initialize Azure OpenAI client
        self.openai_endpoint = openai_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_key = openai_key or os.getenv("AZURE_OPENAI_API_KEY")

        if not self.openai_endpoint or not self.openai_key:
            raise ValueError("Azure OpenAI endpoint and key must be set via arguments or environment variables.")

        self.openai_client = AzureOpenAI(
            azure_endpoint=self.openai_endpoint,
            api_key=self.openai_key,
            api_version=openai_api_version
        )

        self.model_name = model_name
        self.fake = Faker("pt_BR")

    def recognize_pii_entities(self, documents: List[str], language: str = "pt-br") -> List[Dict[str, Any]]:
        """Recognize PII entities in provided documents."""
        response = self.text_analytics_client.recognize_pii_entities(documents, language=language)
        entities: List[Dict[str, Any]] = []
        for doc in response:
            if not doc.is_error:
                for ent in doc.entities:
                    entities.append({
                        "text": ent.text,
                        "category": ent.category,
                        "confidence_score": ent.confidence_score
                    })
        return entities

    def generate_fake_data(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate fake values for each PII entity based on its category."""
        fake_data: List[Dict[str, Any]] = []
        for entity in entities:
            cat = entity["category"]
            if cat == "Person":
                fake_value = self.fake.name()
            elif cat == "BRCPFNumber":
                fake_value = self.fake.cpf()
            elif cat == "BRNationalIDRG":
                fake_value = self.fake.rg()
            elif cat == "Address":
                fake_value = self.fake.address().replace("\n", ", ")
            elif cat == "PhoneNumber":
                fake_value = self.fake.phone_number()
            elif cat == "Organization":
                fake_value = self.fake.company()
            elif cat == "Email":
                fake_value = self.fake.email()
            else:
                fake_value = self.fake.word()
            fake_data.append({
                "original_text": entity["text"],
                "category": cat,
                "fake_value": fake_value,
                "confidence_score": entity["confidence_score"]
            })

        return fake_data

    def replace_with_fake_data(self, texts: List[str], fake_data: List[Dict[str, Any]]) -> List[str]:
        """Replace original PII in texts with generated fake data."""
        replaced_texts: List[str] = []

        for text in texts:
            new_text = text
            for item in fake_data:
                new_text = new_text.replace(item["original_text"], item["fake_value"])
            replaced_texts.append(new_text)

        return replaced_texts

    def aoai_api_call(self, input_text: str, system_prompt: str = None) -> dict:
        """Call Azure OpenAI chat completion to identify user intent from input text."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ]

            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                max_completion_tokens=4096,
                messages=messages,
                response_format={"type": "json_object"}
            )
            intent = response.choices[0].message.content.strip()

            # Parse the intent JSON response
            intent = json.loads(intent)

            return intent

        except Exception as e:
            logging.error("Azure OpenAI call failed: %s", e)
            raise


def main() -> None:
    """Sample usage of the PiiRandomizer class."""

    # Define your System Prompt and Sample Text
    system_prompt = "Você é um assistente que identifica a intenção principal do usuário baseado em um input. " \
                    "Retorne apenas a intenção do usuário, não retorne informações sobre o usuário ou informações pessoais." \
                    "Retorne o resultado como um JSON seguindo a estrutura: {\"intention\": \"<user intention>\"}" \
                    "Considere apenas as seguintes intenções: Conhecer cartões de crédito, Informações de Saldo ou Reclamações." \

    sample_text = (
        "Olá, meu nome é José Almeida, meu CPF é 379.799.200-90 e meu RG 11.456.264-7. "
        "Meu telefone é (11) 92875-5858 e meu e-mail joalmeida@contoso.com. "
        "Trabalho na Contoso e gostaria de conhecer os cartões de crédito disponíveis para meu perfil."
    )

    randomizer = PiiRandomizer()
    texts = [sample_text]

    entities = randomizer.recognize_pii_entities(texts)
    fake_data = randomizer.generate_fake_data(entities)
    replaced_texts = randomizer.replace_with_fake_data(texts, fake_data)
    
    print("\n")
    logging.info("Original Text: %s", sample_text)

    print("\n")
    logging.info("Masked Text: %s", replaced_texts[0])

    original_intent = randomizer.aoai_api_call(input_text=sample_text, system_prompt=system_prompt)
    masked_intent = randomizer.aoai_api_call(input_text=replaced_texts[0], system_prompt=system_prompt)

    print("\n")
    logging.info("Intent from original text: %s", original_intent['intention'])
    logging.info("Intent from masked text: %s", masked_intent['intention'])

if __name__ == "__main__":
    main()


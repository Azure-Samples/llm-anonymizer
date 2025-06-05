# llm-anonymizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-green.svg)](https://www.python.org/)

An elegant toolkit to detect and anonymize PII (Personally Identifiable Information) in text using Azure Text Analytics, generate realistic fake data in multiple languages with Faker, and analyze user intent with Azure OpenAI. Perfect for preserving privacy and testing conversational AI scenarios side-by-side with original and anonymized inputs, with full support for language customization.

- **PII Recognition**: Leverages Azure Text Analytics to accurately identify entities such as names, CPF, RG, addresses, phone numbers, emails, and organizations. The default parameter is configured for Brazilian Portuguese. You can use other languages as well, please check the [language support documentation](https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/language-support).
- **Fake Data Generation**: Uses [Faker](https://faker.readthedocs.io/). The default parameter is configured for Brazilian Portuguese to replace sensitive fields with realistic fake data (names, CPFs, RGs, addresses, etc.). You can use other languages as well, please check the [available locales](https://fakerjs.dev/guide/localization.html#available-locales).
- **Anonymized vs. Original Analysis**: Call Azure OpenAI on both original and anonymized text to compare detected user intent.
- **Class-based API**: Clean `PiiAnonymizer` class with methods for recognition, fake data generation, replacement, and chat completions.
- **Configurable & Extensible**: Environment-based configuration with sensible defaults and clear error messages if credentials are missing.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- An Azure Cognitive Services Text Analytics resource
- An Azure OpenAI resource

### 2. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Azure-Samples/llm-anonymizer.git
   cd llm-anonymizer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

Set the following environment variables in your shell or `.env` file:

```bash
export AZURE_LANGUAGE_ENDPOINT=<your-text-analytics-endpoint>
export AZURE_LANGUAGE_KEY=<your-text-analytics-key>
export AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
export AZURE_OPENAI_API_KEY=<your-openai-key>
```

### 4. Usage

Run the example entrypoint to see PII masking and intent comparison in action:

```bash
python main.py
```

You should see output like:

```text
Original Text:
Olá, meu nome é José Almeida, meu CPF é 379.799.200-90 e meu RG 11.456.264-7. Meu telefone é (11) 92875-5858 e meu e-mail joalmeida@contoso.com. Trabalho na Contoso e gostaria de conhecer os cartões de crédito disponíveis para meu perfil.

Anonymized Text:
Olá, meu nome é <FAKE_NAME>, meu CPF é <FAKE_CPF> e meu RG <FAKE_RG>. Meu telefone é <FAKE_PHONE> e meu e-mail <FAKE_EMAIL>. Trabalho na <FAKE_ORG> e gostaria de conhecer os cartões de crédito disponíveis para meu perfil.

Intent from original text: "Conhecer cartões de crédito"
Intent from masked text: "Conhecer cartões de crédito"
```

## 🛠️ Project Structure

```
llm-anonymizer/
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── src/
    └── anonymizer.py      # Main class and CLI demonstration
```

## ⚙️ API Overview

```python
from anonymizer import PiiAnonymizer

# Initialize with default Brazilian Portuguese
anonymizer = PiiAnonymizer()

# Or override PII extraction language and Faker locale, e.g. English:
anonymizer_en = PiiAnonymizer(
    text_language='en',    # for Azure PII extraction
    faker_locale='en_US'    # for realistic fake data in English
)

# Step 1: Recognize entities
entities = anonymizer.recognize_pii_entities([text])

# Step 2: Generate fake data
fake = anonymizer.generate_fake_data(entities)

# Step 3: Replace in text
masked_text = anonymizer.replace_with_fake_data([text], fake)[0]

# Step 4: Get user intent
intent = anonymizer.aoai_api_call(masked_text)
```

## 📄 License

This project is released under the [MIT License](LICENSE).

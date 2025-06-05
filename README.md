# llm-randomizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-green.svg)](https://www.python.org/)

An elegant toolkit to detect and anonymize PII (Personally Identifiable Information) in text using Azure Text Analytics, generate realistic Brazilian Portuguese fake data with Faker, and analyze user intent with Azure OpenAI. Perfect for preserving privacy and testing conversational AI scenarios side-by-side with original and anonymized inputs.

## 🌟 Features

- **PII Recognition**: Leverages Azure Text Analytics to accurately identify entities such as names, CPF, RG, addresses, phone numbers, emails, and organizations in Portuguese text.
- **Fake Data Generation**: Uses [Faker](https://faker.readthedocs.io/) configured for `pt_BR` to replace sensitive fields with realistic fake data (names, CPFs, RGs, addresses, etc.).
- **Anonymized vs. Original Analysis**: Call Azure OpenAI (`gpt-4o`) on both original and anonymized text to compare detected user intent.
- **Class-based API**: Clean `PiiRandomizer` class with methods for recognition, fake data generation, replacement, and chat completions.
- **Configurable & Extensible**: Environment-based configuration with sensible defaults and clear error messages if credentials are missing.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- An Azure Cognitive Services Text Analytics resource
- An Azure OpenAI resource

### 2. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Azure-Samples/llm-randomizer.git
   cd llm-randomizer
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

Run the script to see PII masking and intent comparison in action:

```bash
python src/randomizer.py
```

You should see logs like:

```
INFO:root:Original Text: Olá, meu nome é José Almeida, meu CPF é ...
INFO:root:Masked Text: Olá, meu nome é <FAKE_NAME>, meu CPF é <FAKE_CPF>...
INFO:root:Intent from original text: "Conhecer cartões de crédito"
INFO:root:Intent from masked text: "Conhecer cartões de crédito"
```

## 🛠️ Project Structure

```
llm-randomizer/
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── src/
    └── randomizer.py      # Main class and CLI demonstration
```

## ⚙️ API Overview

```python
from randomizer import PiiRandomizer

# Initialize (reads env vars if not passed)
randomizer = PiiRandomizer()

# Step 1: Recognize entities
entities = randomizer.recognize_pii_entities([text])

# Step 2: Generate fake data
fake = randomizer.generate_fake_data(entities)

# Step 3: Replace in text
masked_text = randomizer.replace_with_fake_data([text], fake)[0]

# Step 4: Get user intent
intent = randomizer.aoai_api_call(masked_text)
```

## 📄 License

This project is released under the [MIT License](LICENSE).

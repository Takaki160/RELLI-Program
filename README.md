# RELLI-Program

## Introduction

RELLI-Program is a program led by the [UCLA MQE](https://master.econ.ucla.edu/) students in collaboration with the [RELLI Company](https://www.relli.co/).

The goal of this program is to develop an evaluation system that can assess investment projects before uploading them to the RELLI platform.

The program is divided into two projects:

1. **Financial Model**: This project will be developed by the *Finance Team* and will focus on creating a comprehensive financial model based on various financial indicators in the *investment project document* to assess investment projects.

2. **Technical Implementation**: This project will be developed by the *Tech Team* and will focus on building a program that can extract relevant data from the *investment project document* (PDF format) and utilize the financial model to provide the assessment.

This repository contains the code for the *Technical Implementation* project of the program.

## Project Structure

The project is organized into the following directories:

- `/data`: Contains sample investment project documents and any necessary data files.
- `/code`: Contains the source code for the technical implementation.
- `/docs`: Contains documentation related to the project.

## Project Overview

The project will be using **Python** as the primary programming language.

The main components of the project include:

1. **Reading Documents**: Using the `PyMuPDF` library to batch read investment project documents in PDF format and convert them into text format.

2. **Data Extraction**: Using open-source Large Language Models (LLMs) like `Llama` and `Gemini` to extract necessary financial indicators from the text.

3. **Financial Evaluation**: Integrating the financial model developed by the *Finance Team* to assess the investment projects based on the extracted data.

### Using LLMs Locally

To use the LLMs locally, you may need to install [Ollama](https://ollama.com/), and download models via terminal commands. Take `Llama 3.1` as an example:

```bash
# Download the model
ollama pull llama:3.1
```

```bash
# Activate Ollama server
ollama serve
```

```bash
# Run the model locally
ollama run llama:3.1
```

You can then use the model in Python by sending requests to the Ollama server using the `requests` library.

### Using LLMs via API

You can also use LLMs via LLM APIs. Take Google Gemini API as an example, you need to acquire an API key from the [Google AI Studio](https://aistudio.google.com/). For using the API in Python, you can refer to its [official documentation](https://ai.google.dev/gemini-api/docs/quickstart).

## Roadmap

1. **Week 1-2**: Research and select appropriate LLMs for data extraction. Collect sample investment project documents and corresponding financial indicators. The sample dataset should be the following format:

    | Project Name | Document (PDF) | Financial Indicator 1 | Financial Indicator 2 | ... |
    |--------------|----------------|-----------------------|-----------------------|-----|
    | Project A    | project_a.pdf  | Value A1              | Value A2              | ... |
    | Project B    | project_b.pdf  | Value B1              | Value B2              | ... |
    | ...          | ...            | ...                   | ...                   | ... |

2. **Week 3**: Develop the document reading and data extraction modules.

3. **Week 4-6**: Test the program on sample documents and refine the extraction process by selecting the best-performing LLMs and optimizing prompts.

4. **Week 7-8**: Integrate the financial model into the program and conduct end-to-end testing.

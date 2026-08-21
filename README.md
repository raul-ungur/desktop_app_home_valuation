# App Home Valuation

A desktop home-valuation project built with **Python, PySide6, FastAPI, and Ollama**.

The application is divided into two parts:

- **PC_A – Client:** a PySide6 desktop application where the user enters the house information.
- **PC_B – Server:** a FastAPI server that receives the data from PC_A, sends a prompt to a locally running Ollama LLM, and returns the generated response to the client.

## Current Architecture

```text
PC_A - PySide6
    |
    | HTTP POST + JSON
    v
PC_B - FastAPI
    |
    | Local API request
    v
Ollama - Local LLM
    |
    | Generated response
    v
FastAPI
    |
    | JSON response
    v
PC_A - PySide6
```

## What Has Been Implemented

The project currently demonstrates:

- A PySide6 desktop GUI.
- Input fields for:
  - square meters
  - number of rooms
  - number of bathrooms
  - garage availability
- A reset function for the form.
- Communication between two computers over a local network.
- A FastAPI REST API on PC(B).
- POST requests from the PySide6 client to the FastAPI server.
- Pydantic request validation.
- Integration between FastAPI and Ollama.
- Local LLM inference through Ollama, without using a paid external LLM API.
- A loading popup while the request is processed.
- A separate popup displaying the LLM response.
- Basic client/server separation.

> Note: This project is currently intended as a portfolio/demo project. It is designed to be tested locally and is not intended to be deployed directly to the public internet without additional security and production configuration.

## Requirements

For the easiest test setup, it is recommended to use **two computers connected to the same local network**:

- **PC_A:** runs the PySide6 client.
- **PC_B:** runs FastAPI and Ollama.

The two computers can also be replaced by a single computer for development, but the two-PC setup demonstrates the client/server architecture more clearly.

## Testing the Project

To test the application, follow both instruction files:

1. `instruction_pc_A.txt` – setup and run the PySide6 client.
2. `instruction_pc_B.txt` – setup Ollama, FastAPI, and run the server.

**Important:** before starting PC_A, replace the server IP address in the client code with the local IP address of PC_B.

Example:

```python
SERVER_URL = "http://192.168.1.7:8000"
```

The IP address `192.168.1.7` is only an example. Your PC_B will probably have a different address.

## Project Structure

```text
APP_HOME_VALUATION/
│
├── README.md
│
├── PC_A/
│   ├── main.py
│   └── instruction_pc_A.txt
│
└── PC_B/
    ├── server_api.py
    └── instruction_pc_B.txt
```

The exact filenames can be changed to match the current project files.

## Notes

The LLM runs locally through Ollama on PC_B. Therefore, the project does not require a paid OpenAI/Anthropic/etc. API for the current implementation.

The quality and speed of the generated response depend on the local LLM model and the hardware of PC_B.

## Future Improvements

Possible future improvements include:

- A real machine-learning house-price prediction model trained on a dataset.
- Database integration on the server side.
- More robust input validation.
- Authentication/API keys.
- Rate limiting.
- HTTPS and a reverse proxy for public deployment.
- Better error handling and logging.
- Packaging the PySide6 application as an executable.

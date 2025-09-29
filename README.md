# RAG Project

This project implements a Retrieval-Augmented Generation (RAG) system. The core idea behind RAG is to combine the strengths of information retrieval with the generative capabilities of large language models (LLMs). Instead of relying solely on the LLM's pre-trained knowledge, a RAG system first retrieves relevant documents or knowledge snippets from a vast corpus and then uses this retrieved information to inform and guide the LLM's response.

## Purpose

The main purpose of this project is to:

*   **Enhance LLM Accuracy:** By providing real-time, relevant information, the system aims to reduce hallucinations and improve the factual accuracy of LLM-generated responses.
*   **Improve Contextual Understanding:** The retrieved documents offer a richer context to the LLM, leading to more coherent and contextually appropriate outputs.
*   **Enable Knowledge Base Interaction:** Users can interact with a defined knowledge base (e.g., documents, articles) to get answers grounded in specific information.

## Technology Stack

This project utilizes the following key technologies:

*   **Python:** The primary programming language for the backend logic and services.
*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Ollama:** Used for running large language models locally.
*   **Qdrant:** A vector similarity search engine, used here as a vector database to store and retrieve document embeddings.
*   **Docker & Docker Compose:** For containerization and orchestration, ensuring easy setup and consistent environments.

## Project Structure

The project is organized into the following main directories:

*   `api/`: Contains the FastAPI application, including controllers, services, and models.
*   `models/`: Stores information related to the large language models used, such as `Modelfile` for Ollama.
*   `tests/`: Contains unit and integration tests for the application.

## Setup and Running the Project

### Prerequisites

Before running the project, ensure you have the following installed:

*   Docker
*   Docker Compose

### Steps to Run

1.  **Build and Run Docker Containers:**

    Navigate to the project root and run:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images (if not already built) and start the necessary services (FastAPI application, Ollama, Qdrant).

2.  **Access the API Documentation:**

    Once the services are up, you can access the FastAPI interactive API documentation (Swagger UI) at:
    `http://localhost:8000/docs`

3.  **Interact with the RAG System:**

    You can use the API documentation to:
    *   Upload documents to the knowledge base.
    *   Query the RAG system with your questions.

## API Endpoints (Conceptual)

*   `/kb/upload`: Upload documents to the knowledge base.
*   `/query`: Query the RAG system with a given question.

## Future Enhancements

*   Implement more sophisticated document parsing and chunking strategies.
*   Add support for multiple LLM providers.
*   Develop a user interface for easier interaction.
*   Improve error handling and logging.

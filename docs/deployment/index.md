# Deployment

This project demonstrates RFQ parsing using Retrieval Augmented Generation (RAG) and deploys open-source components with Docker.

Click here for [Demo project repository](https://github.com/parrisma/rfq-rag/) & full code

---

## Table of Contents

- [Deployment](#deployment)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
---
## Deployment

**Components:**

1.  **Ollama:** ([ollama.com](https://ollama.com/)) - Downloads and runs Large Language Models (LLMs).
2.  **ChromaDB:** ([trychroma.com](https://www.trychroma.com/)) - A vector database for storing example RFQs. This enables the *Retrieval Augmented* part of RAG, specializing the LLM prompt.

---

## Prerequisites

1.  **Linux Environment:**
    * While compatible with both Windows and Linux, a Linux environment is recommended.
    * For Windows users, utilize **Windows Subsystem for Linux (WSL 2)** ([ubuntu.com/desktop/wsl](https://ubuntu.com/desktop/wsl)).
    * WSL 2 is integrated into Docker Desktop.
    * Execute project scripts within a Linux (Ubuntu) shell on WSL 2 or a native Linux system.

2.  **Docker:**
    * A basic Docker installation is required ([docker.com](https://www.docker.com/)).
    * This project uses simple Docker containers, without Kubernetes or complex orchestration.

3.  **GPU and Memory:**
    * A dedicated GPU and ample system memory are strongly recommended for optimal performance when running LLMs locally.
    * Testing was conducted on a system with an NVIDIA RTX 4090 and 128GB of RAM.
    * For systems with lower resources, explore smaller models from the [Ollama model directory](https://ollama.com/search).
    * Smaller models offer faster processing but may exhibit reduced accuracy for complex reasoning tasks.
    * The demo will still run on lower spec machines.

4. **Python**
    * Conda and pip were used to manage the virtual environment
    * the environment.yml is [here](https://github.com/parrisma/rfq-rag/blob/main/environment.yml) - edit the last line of the file so the ```prefix``` matches your home directory
    * Create env ```conda env create -f environment.yml```

---

## Setup Instructions

Follow these steps to set up the project:

1.  **Open a Linux Shell:**
    * Start a Linux terminal on your system (WSL 2 or native Linux).

2.  **Clone the Repository:**
    * Use `git clone` to download the project files.
    ```sh
    mkdir rfq-rag
    cd rfq-rag
    git clone https://github.com/parrisma/rfq-rag
    ```

3.  **Navigate to the Scripts Directory:**
    * Change your current directory to the `scripts` folder:

    ```sh
    cd scripts
    ```

4.  **Run the Bootstrap Script:**
    * Execute the `bootstrap.sh` script, providing your username as an argument:

    ```sh
    ./bootstrap.sh <your-user-name>
    ```

    * **What this script does:**
        * Downloads and starts both Ollama and Chroma DB using Docker.
        * Creates necessary directories in your home folder for persisting data from these services.
        * Downloads and starts the default Large Language Model (LLM) within Ollama.

* **To use a different LLM model:**

    1.  **Access the Ollama Container:**
        * Connect to the running Ollama container named `ollama-gpu`:
            ```sh
            docker exec -it ollama-gpu /bin/bash
            ```
    1.  **Find Your Model:**
        * Browse the [Ollama model directory](https://ollama.com/search) to find the desired model.
    1.  **Run the Model:**
        * Inside the Ollama container, execute:
            ```sh
            ollama run <model-name>
            ```
            * Note: Downloading the model may take time depending on its size.

    1.  **Verify the Model:**
        * Exit the current model:
            ```sh
            /bye
            ```
        * Check the running models:
            ```sh
            ollama ps
            ```
            * This confirms your chosen model is active.
    1.  **Let the demo script know**
        * Pass in command line arg
        ```sh
        python ./rfq-rag-main-demo.py -om=<model name>
        ```
        you will also need to pass in other command line arguments depending on the tests you want to run. Not covered here.

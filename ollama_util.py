from typing import Tuple, List
import os
import requests
import json
from ollama import embeddings

ollama_host = "http://localhost:11434"
#ollama_model = "llama2:7b"
ollama_model = "llama3.3:latest"

# Create embedding and load files into Chroma
#


def generate_ollama_embedding(text: str,
                              model: str,
                              host: str) -> List[float]:
    """
    Generates an embedding for the given text using Ollama.

    Args:
        text (str): The text to embed.
        model (str): The Ollama model to use.
        host (str): The Ollama server address.

    Returns:
        list: The embedding vector, or None if an error occurs.
    """
    try:
        if os.environ.get("OLLAMA_HOST") != host:
            os.environ["OLLAMA_HOST"] = host
        response = embeddings(model=model, prompt=text)
        return response['embedding']
    except Exception as e:
        print(f"Ollama - Error generating embedding: {e}")
        return None


def ollama_runing_and_model_loaded(host: str,
                                   model_name: str) -> bool:
    try:
        response = requests.get(f"{host}/api/tags")
        response.raise_for_status()
        models = [m["name"] for m in response.json()["models"]]
        loaded_ok = model_name in models
        if loaded_ok:
            print(f"Ollama - model is loaded OK [{model_name}]")
        else:
            print(f"Ollama - model is not loaded [{model_name}]")
        return loaded_ok
    except requests.exceptions.RequestException as e:
        print(
            f"Ollama - An error occurred, getting model [{model_name}] status: {e}")
        return False


def get_ollama_response(prompt: str,
                        model: str,
                        host: str,
                        temperature=0.2) -> Tuple[bool, str]:
    try:
        ollama_host = os.environ.get('OLLAMA_HOST', host)
        url = f"{ollama_host}/api/chat"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            # Important to disable streaming for this simple example.
            'stream': False,
            'options': {'temperature': temperature}
        }

        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        return (True, data['message']['content'])

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to Ollama: {e}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON response from Ollama."
    except KeyError:
        return "Error: Unexpected response format from Ollama."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

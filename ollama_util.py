from typing import Tuple, List, Dict
from enum import Enum
import os
import requests
import json
from ollama import embeddings
from langchain_prompt import get_taxonomy_prompt, get_parse_prompt, Example
from product_def import products


class OllamaModel(Enum):
    LLAMA2_7B = "llama2:7b"
    LLAMA3_3_LATEST = "llama3.3:latest"
    QWEN2_5_72B = "qwen2.5:72b"


ollama_model = OllamaModel.QWEN2_5_72B.value
ollama_host = "http://localhost:11434"

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


def ollama_running_and_model_loaded(host: str,
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


def clean_json_str(jason_str: str) -> str:
    jason_str = jason_str.replace('\n', '')
    jason_str = jason_str.replace('\`', '')
    jason_str = jason_str.replace('\'', '')

    first_bracket_index = jason_str.find('[')
    last_bracket_index = jason_str.rfind(']')

    if first_bracket_index == -1 or last_bracket_index == -1:
        return None  # No brackets found

    if first_bracket_index == last_bracket_index:
        return None  # only one bracket found

    if first_bracket_index > last_bracket_index:
        return None  # first bracket after last bracket

    return jason_str[first_bracket_index+1:last_bracket_index]


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
        json_str = clean_json_str(data['message']['content'])
        return (True, json.loads(json_str))

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to Ollama: {e}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON response from Ollama."
    except KeyError:
        return "Error: Unexpected response format from Ollama."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_product_taxonomy(ref_request: str,
                         model: str,
                         host: str
                         ) -> Tuple[bool, Dict]:
    """
        Use currently loaded Ollama LLM to review the given RFQ and return what product type the RFQ is talking about
    """
    prompt = get_taxonomy_prompt(product_list=products, rfq=ref_request)
    res, reply = get_ollama_response(prompt, model=model, host=host)
    return res, reply


def save_prompt(prompt: str,
                test_id: str) -> None:
    try:
        prompt_filename = f"prompt-{test_id}.txt"
        with open(prompt_filename, 'w') as file:
            file.write(prompt)
        print(f"RfqRag - Fully qualified Prompt saved to: {prompt_filename}")
    except Exception as e:
        print(f"RfqRag - Failed to save prompt: {e} exiting test [{test_id}]")
        exit(1)
    return


def get_parsed_rfq(ref_request: str,
                   product: str,
                   ex1: Example,
                   ex2: Example,
                   ex3: Example,
                   ex4: Example,
                   ex5: Example,
                   test_id: str,
                   model: str,
                   host: str
                   ) -> Tuple[bool, Dict]:
    """
        Use currently loaded Ollama LLM to review the given RFQ and parse out all pricing parameters
    """
    prompt = get_parse_prompt(ref_request, product, ex1, ex2, ex3, ex4, ex5)
    save_prompt(prompt, test_id)
    res, reply = get_ollama_response(prompt, model=model, host=host)
    return res, reply

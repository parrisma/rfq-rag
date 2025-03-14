import json
from chroma_util import get_similar_rfqs
from compare import compare_json_expected_actual
from langchain_prompt import Example
from ollama_util import get_ollama_response, get_parsed_rfq, get_product_taxonomy
from rfq_generator import generate_random_rfq


def run_prompt_test(saved_prompt_filename: str,
                    _ollama_model: str,
                    _ollama_host: str) -> None:

    print("\n############ L O A D  S A V E D  P R O M P T ###########")
    try:
        print(f"RfqRag - Loading saved prompt from file: {saved_prompt_filename}")
        with open(saved_prompt_filename, 'r') as file:
            saved_prompt = file.read()
    except FileNotFoundError:
        print(f"RfqRag - Saved Prompt {saved_prompt_filename} does not exist, exiting")
        return

    print("\n############ P A R S E  R F Q ############")
    _, reply = get_ollama_response(saved_prompt,
                                   model=_ollama_model,
                                   host=_ollama_host)

    print(f"\nreply: {json.dumps(reply, indent=4)}")

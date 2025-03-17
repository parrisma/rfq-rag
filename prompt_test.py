import json
from langchain_prompt import Example
from ollama_util import get_ollama_response, get_parsed_rfq, get_product_taxonomy
from trail import log


def run_prompt_test(saved_prompt_filename: str,
                    ollama_model: str,
                    ollama_host: str,
                    temperature: float) -> None:

    log().debug("\n############ L O A D  S A V E D  P R O M P T ###########")
    try:
        log().debug(f"Loading saved prompt from file: {saved_prompt_filename}")
        with open(saved_prompt_filename, 'r') as file:
            saved_prompt = file.read()
    except FileNotFoundError:
        log().debug(f"Saved Prompt {saved_prompt_filename} does not exist, exiting")
        return

    log().debug("\n############ P A R S E  R F Q ############")
    _, reply = get_ollama_response(saved_prompt,
                                   model=ollama_model,
                                   host=ollama_host,
                                   temperature=temperature)

    log().debug(f"\nreply: {json.dumps(reply, indent=4)}")

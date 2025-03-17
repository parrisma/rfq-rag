import os
import sys
import platform
import argparse
from typing import Tuple, Any, Dict
from chroma_util import test_chroma_connection
from ollama_util import ollama_running_and_model_loaded
from trail import log


def clear_screen() -> None:
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


known_unix_platforms = ["Linux", "Darwin", "CYGWIN"]


def get_username() -> str:
    try:
        if platform.system() == "Windows":
            return os.environ.get("USERNAME") or os.environ.get("USER") or os.getlogin()
        elif platform.system() in known_unix_platforms:
            return os.environ.get("USER") or os.environ.get("LOGNAME") or os.getlogin()
        else:
            return None
    except Exception:  # catch absolutely anything else.
        return None


def get_options(ollama_host: str,
                ollama_model: str,
                chroma_host: str,
                chroma_port: str) -> Tuple[Any]:
    parser = argparse.ArgumentParser(
        description="Command line arguments for the RFQ RAG Demo")
    usr_name = get_username()
    if usr_name:
        parser.add_argument("-u", "--username", type=str, default=usr_name,
                            help="The username to use for the demo, default is the current user.")
    else:
        parser.add_argument("-u", "--username", type=str,
                            help="The username to use for the demo, default is the current user.")
    # Optional arguments
    parser.add_argument("-om", "--ollama-model", type=str, default=ollama_model,
                        help=f"Ollama LLM to use, default is {ollama_model}")
    parser.add_argument("-oh", "--ollama-host", type=str,
                        default=ollama_host, help=f"Ollama host & port URI to use, default is {ollama_host}")
    parser.add_argument("-ch", "--chroma_host", type=str,
                        default=chroma_host, help=F"Chroma hostname to use, default is {chroma_host}")
    parser.add_argument("-cp", "--chroma_port", type=str,
                        default=chroma_port, help=f"Chroma port to use, default is {chroma_port}")
    parser.add_argument("-cs", "--clear-screen", type=bool,
                        default=True, help="Clear terminal before running the demo")
    parser.add_argument("-rc", "--remove_collections", action="store_true",
                        help="Delete all Chroma collections before running the demo.")
    parser.add_argument("-uc", "--use_collection", type=str,
                        default=None, help="The name of an existing chroma collection to use, default is a new collection.")
    parser.add_argument("-pt", "--product-type-test", action="store_true",
                        help="Run product type test")
    parser.add_argument("-st", "--similarity-test", action="store_true",
                        help="Run similarity test by looking up similar RFQ in Vector DB (Chroma)")
    parser.add_argument("-ft", "--full-rfq-test", action="store_true",
                        help="Run full RFQ test and compare LLM extracted results with test results")
    parser.add_argument("-nr", "--num_rfq", type=int,
                        default=25, help="The number of random RFQ's to generate for the simulation")
    parser.add_argument("-kr", "--keep-rfq", action="store_true",
                        help="Keep any collections created as part of the demo rather than deleting them at the end")
    parser.add_argument("-nt", "--num_tests", type=int,
                        default=5, help="The number test cycles to perform for rfq parsing")
    parser.add_argument("-p", "--prompt", type=str,
                        default=None, help="The filename of a saved prompt that is to be loaded and parsed")
    parser.add_argument("-t", "--temperature", type=float,
                        default=0.2, help="The model temperature, a positive float normally in range 0.0 to 1.0, default=0.2")
    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 2:
            log().debug("Error: Invalid command-line arguments.")
            parser.log().debug_help()
            sys.exit(1)
        else:
            raise

    if args.use_collection is not None:
        args.remove_collections = False

    if args.temperature < 0.0 or args.temperature > 1.0:
        log().debug("Error: Invalid model temperature value. Must be in range 0.0 to 1.0 as RFQ parsing needs to be more deterministic than random.")
        sys.exit(1)

    log().debug("\n############ C O N T R O L  S E T T I N G S ###########\n")
    log().debug(f"Username: {args.username}")
    log().debug(f"Ollama Model: {args.ollama_model}")
    log().debug(f"Ollama Host: {args.ollama_host}")
    log().debug(f"Chroma Host: {args.chroma_host}")
    log().debug(f"Chroma Port: {args.chroma_port}")
    log().debug(f"Clear Screen: {args.clear_screen}")
    log().debug(f"Remove Collections: {args.remove_collections}")
    log().debug(f"Use Collection: {args.use_collection}")
    log().debug(f"Product Type Test: {args.product_type_test}")
    log().debug(f"Similarity Test: {args.similarity_test}")
    log().debug(f"Full RFQ Test: {args.full_rfq_test}")
    log().debug(f"Number of RFQs: {args.num_rfq}")
    log().debug(f"Keep RFQ: {args.keep_rfq}")
    log().debug(f"Number of Tests: {args.num_tests}")
    log().debug(f"Prompt Filename: {args.prompt}")
    log().debug(f"Model Temperature: {args.temperature}\n")

    return (args.username,
            args.ollama_model,
            args.ollama_host,
            args.chroma_host,
            args.chroma_port,
            args.clear_screen,
            args.remove_collections,
            args.use_collection,
            args.product_type_test,
            args.similarity_test,
            args.full_rfq_test,
            args.num_rfq,
            args.keep_rfq,
            args.num_tests,
            args.prompt,
            args.temperature)


def flatten_dict(nested_dict: Dict,
                 flat_dict: Dict = None,
                 key: str = '') -> Dict:
    if not isinstance(nested_dict, dict):
        raise TypeError(f"input, nested dicts must be a dictionary but given : {type(nested_dict)}")

    if flat_dict is None:
        flat_dict = {}

    for k, v in nested_dict.items():
        new_key = f"{key}.{k}" if key else k

        if isinstance(v, dict):
            flatten_dict(v, flat_dict, new_key)
        else:
            flat_dict[new_key] = v

    return flat_dict


def check_services_status(ollama_host: str,
                          ollama_model: str,
                          chroma_host: str,
                          chroma_port: str) -> None:
    log().debug("\n############ C H E C K   O L L A M A ###################\n")
    ollama_status = ollama_running_and_model_loaded(host=ollama_host, model_name=ollama_model)
    log().debug(f"Ollama - running & required LLM loaded: {ollama_status}")

    log().debug("\n############ C H E C K   C H R O M A - D B #############\n")
    chroma_status = test_chroma_connection(host=chroma_host, port=chroma_port)
    log().debug(f"Chroma - running : {chroma_status}")

    if not ollama_status or not chroma_status:
        log().debug("Error - run ./scripts/start-ollama.sh to ensure all required services are running as containers")
        exit()

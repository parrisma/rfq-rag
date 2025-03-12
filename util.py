import json
import sys
from time import sleep
from typing import Tuple, Any, Dict
import os
import platform
import argparse


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

    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 2:
            print("Error: Invalid command-line arguments.")
            parser.print_help()
            sys.exit(1)
        else:
            raise

    if args.use_collection is not None:
        args.remove_collections = False

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
            args.num_tests)


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

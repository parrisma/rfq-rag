from typing import Tuple, Any
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


ollama_host = ""
# ollama_model = "llama2:7b"
ollama_model = "llama3.3:latest"
chroma_host = "localhost"
chroma_port = 8000


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
    parser.add_argument("-om", "--ollama-model", type=str,
                        default=ollama_model, help=f"Ollama LLM to use, defualt is {ollama_model}")
    parser.add_argument("-oh", "--ollama-host", type=str,
                        default=ollama_host, help=f"Ollama host & port URI to use, default is {ollama_host}")
    parser.add_argument("-ch", "--chroma_host", type=str,
                        default=chroma_host, help=F"Chroma hostname to use, default is {chroma_host}")
    parser.add_argument("-cp", "--chroma_port", type=str,
                        default=chroma_port, help=f"Chroma port to use, default is {chroma_port}")
    parser.add_argument("-cs", "--clear-screen", type=bool,
                        default=True, help="Clear terminal before running the demo, default is True.")
    parser.add_argument("-cr", "--remove_collections", type=bool,
                        default=True, help="Delete all Chroma collections before running the demo, default is True.")
    parser.add_argument("-cu", "--use_collection", type=str,
                        default="last", help="The name of an existing chroma collection to use, default is 'last'.")

    args = parser.parse_args()
    return (args.username,
            args.ollama_model,
            args.ollama_host,
            args.chroma_host,
            args.chroma_port,
            args.clear_screen,
            args.remove_collections,
            args.use_collection)

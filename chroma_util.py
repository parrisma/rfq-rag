from typing import Tuple, List, Callable
import numpy as np
import json
import uuid
import requests
from chromadb.config import Settings
import chromadb

# Chroma settings
#

chroma_host = "localhost"
chroma_port = 8000


def chroma_bootstrap_and_deepclean(chroma_host: str,
                                   chroma_port: str,
                                   use_collection: str = None,
                                   remove_all: bool = True) -> Tuple:
    client_settings = Settings(
        chroma_api_impl="chromadb.api.fastapi.FastAPI",
        chroma_server_host=chroma_host,
        chroma_server_http_port=chroma_port)

    persistent_client = chromadb.PersistentClient(settings=client_settings)

    collections = persistent_client.list_collections()
    if remove_all:
        print("Chroma - Clean up existing chroma collections:")
        for col in collections:
            print(f"Chroma - Deleting old collection: {col}")
            persistent_client.delete_collection(col)

    new_collection = False
    if "last" == use_collection and len(collections) == 1:
        collection_name = collections[0]
        collection = persistent_client.get_collection(collection_name)
        print(f"Chroma - Using last collection: {collection_name}")
    elif use_collection in collections:
        collection = persistent_client.get_or_create_collection(use_collection)
        print(f"Chroma - Using existing collection: {collection_name}")
    else:
        new_collection = True
        collection_name = f"rfq_rag_collection_{uuid.uuid4()}"
        print(f"Chroma - creating new collection: {collection_name}")

    collections = persistent_client.list_collections()
    for col in collections:
        print(f"Chroma - New collection created: {col}")

    return (persistent_client, collection, new_collection)


def test_chroma_connection(host: str,
                           port: str) -> bool:
    try:
        url = f"http://{host}:{port}/api/v1/heartbeat"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        heartbeat_data = response.json()
        print(f"Chroma - connection successful. Heartbeat: {heartbeat_data}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Chroma - connection failed: {e}")
        return False


def get_similar_rfqs(rfq_to_match: str,
                     embedding_generator: Callable[[str], List[float]],
                     collection: chromadb.Collection,
                     num_similar: int = 5) -> List[List[str]]:
    search_embedding = embedding_generator(rfq_to_match)
    similar_docs = collection.query(
        query_embeddings=[search_embedding],
        n_results=num_similar,
        # where_document={"$contains": "ELN"},
        include=["distances", "documents", "metadatas"])
    sdst = np.array(similar_docs["distances"]).T
    sdoc = np.array(similar_docs["documents"]).T
    smet = np.array(similar_docs["metadatas"]).T
    suid = (np.array([json.loads(itm[0]["meta"])["uuid"]
            for itm in smet]).T).reshape(np.shape(smet)[0], 1)
    res = np.hstack((sdst, sdoc, suid)).tolist()
    return res

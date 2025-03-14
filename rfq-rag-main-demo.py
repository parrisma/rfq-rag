from functools import partial
from generate_rfq_examples import generate_and_load_rfq_support_examples
from parsing_test import run_parsing_test
from product_taxonomy_test import product_type_test
from prompt_test import run_prompt_test
from util import check_services_status, clear_screen, get_options
from chroma_util import clean_up_collection,  chroma_bootstrap_and_deepclean,  chroma_host, chroma_port
from ollama_util import generate_ollama_embedding,  ollama_host, ollama_model

_, \
    _ollama_model, \
    _ollama_host, \
    _chroma_host, \
    _chroma_port, \
    _clear_screen, \
    _chroma_remove_all, \
    _use_collection, \
    _product_type_test, \
    _similarity_test, \
    _full_rfq_test, \
    _num_rfq, \
    _keep_rfq, \
    _num_test, \
    _prompt = get_options(ollama_host, ollama_model, chroma_host, chroma_port)

if _clear_screen:
    clear_screen()

# Check Ollama and Chroma services are running & exit with error if not
#
check_services_status(_ollama_host, _ollama_model, _chroma_host, _chroma_port)


if _prompt is None:
    # Purge Chroma of any existing collections and create a dedicated collection just for this demo
    #
    persistent_client, collection, new_collection = chroma_bootstrap_and_deepclean(_chroma_host,
                                                                                   _chroma_port,
                                                                                   _use_collection,
                                                                                   _chroma_remove_all)

    embedding_generator = partial(generate_ollama_embedding,
                                  model=_ollama_model,
                                  host=_ollama_host)

    if new_collection:
        res = generate_and_load_rfq_support_examples(_num_rfq,
                                                     embedding_generator,
                                                     collection)
    else:
        print("RfqRag - Using existing collection of RFQs and Embeddings\n")

    if _product_type_test:
        product_type_test(_num_test,
                          _ollama_model,
                          _ollama_host)

    if _similarity_test or _full_rfq_test:
        run_parsing_test(_similarity_test,
                         _full_rfq_test,
                         _num_test,
                         _ollama_model,
                         _ollama_host,
                         embedding_generator,
                         collection)
    if new_collection and not _keep_rfq:
        clean_up_collection(persistent_client,
                            collection)
else:
    run_prompt_test(_prompt,
                    _ollama_model,
                    _ollama_host)

print(f"RfqRag - All Done\n")

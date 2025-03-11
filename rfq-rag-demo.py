import json
import uuid
from functools import partial
from util import clear_screen, get_options, flatten_dict
from chroma_util import test_chroma_connection, chroma_bootstrap_and_deepclean, get_similar_rfqs, chroma_host, chroma_port
from ollama_util import ollama_runing_and_model_loaded, generate_ollama_embedding, get_product_taxonomy, get_parsed_rfq, ollama_host, ollama_model
from rfq_generator import generate_random_rfq
from langchain_prompt import Example
from compare import compare_json_expected_actual

_username, \
    _ollama_model, \
    _ollama_host, \
    _chroma_host, \
    _chroma_port, \
    _clear_screen, \
    _chroma_remove_all, \
    _use_collection, \
    _product_type_test, \
    _similarity_test, \
    _num_rfq = get_options(ollama_host, ollama_model, chroma_host, chroma_port)

if _clear_screen:
    clear_screen()

print("\n############ C H E C K   O L L A M A ###################\n")
ollama_status = ollama_runing_and_model_loaded(host=_ollama_host, model_name=_ollama_model)
print(f"Ollama - running & required LLM loaded: {ollama_status}")

print("\n############ C H E C K   C H R O M A - D B #############\n")
chroma_status = test_chroma_connection(host=_chroma_host, port=_chroma_port)
print(f"Chroma - running : {chroma_status}")

if not ollama_status or not chroma_status:
    print("Error - run ./scripts/start-ollama.sh to ensure all requried services are running as conatiners")
    exit()

# Purge Chroma of any existing collections and create a dedicated collection just for this demo
#
persistent_client, collection, new_collection = chroma_bootstrap_and_deepclean(_chroma_host,
                                                                               _chroma_port,
                                                                               _use_collection,
                                                                               _chroma_remove_all)

# Generate a set of RFQ's that will act as the support example for the final RFQ parsing
# In practice these would be real RFQ examples that had been hand seclected from production
# and the prameters verified.
#
print("\n############ G E N E R A T E  T E S T  R F Q s #########\n")
embedding_generator = partial(generate_ollama_embedding,
                              model=_ollama_model,
                              host=_ollama_host)
if new_collection:
    print("RfqRag - Generating RFQ support examples to be used to support final RFQ parsing\n")
    full_docs = []
    for i in range(_num_rfq):
        doc = generate_random_rfq()
        full_docs.append(doc)
        print(".", end="")
        if (i+1) % 50 == 0:
            print("")
    print("\n############ C R E A T E  E M B E D D I N G S  #########")
    print("############ A N D  L O A D  I N  C H R O M A  #########\n")
    print("RfqRag - Generating embeddings for RFQ support examples and loading into Chroma (vector DB)\n")
    docs = [doc["request"] for doc in full_docs]
    metas = [flatten_dict(rfq) for rfq in full_docs]
    guids = [str(uuid.uuid4()) for _ in range(len(docs))]

    embedding_values = []
    i = 0
    for doc in docs:
        embedding_values.append(embedding_generator(doc))
        print(".", end="")
        if (i+1) % 50 == 0:
            print("")
        i += 1

    print("")
    res = collection.add(ids=guids,
                         embeddings=embedding_values,
                         documents=docs,
                         metadatas=metas)

    print("RfqRag - RFQ support examples loaded into Chroma\n")
else:
    print("RfqRag - Using existing collection of RFQs and Embeddings\n")

if _product_type_test:
    print("\n############ U S E  M O D E L  T O  F I N D ###########")
    print("############     P R O D U C T  T Y P E     ###########")
    score = 0
    num_tests = 5
    for _ in range(num_tests):
        test_rfq = generate_random_rfq()
        res, reply = get_product_taxonomy(test_rfq["request"],
                                          model=_ollama_model,
                                          host=_ollama_host)
        print(f"reply: {json.dumps(reply, indent=4)}")
        if (reply['product'] == test_rfq['product']):
            print(f"Product Type Correct LLM prediction: [{reply['product']}] equals expected [{test_rfq['product']}]")
            score += 1
        else:
            print(f"Product Type Incorrect LLM prediction: [{reply['product']}] does not equal expected [{test_rfq['product']}]")
        print("\n------------------\n")
    print(f"Product Type Test Score: ({(score/num_tests)*100:.0f}%)")

if _similarity_test:
    print("\n############ C H E C K   E M B E D D I N G  ############")
    print("############ G E T  S I M I L A R  R F Q s #############\n")
    test_rfq = generate_random_rfq()
    res, reply = get_product_taxonomy(test_rfq["request"],
                                      model=_ollama_model,
                                      host=_ollama_host)
    print(f"RfqRag - Similar RFQs to: {test_rfq['request']}")
    similar = get_similar_rfqs(test_rfq["request"],
                               reply['product'],
                               embedding_generator,
                               collection)
    for d, r, m, u in similar:
        print(f"Dist: [{float(d):7.2f}], Doc: {r}")

    ex = [Example(e[1], json.dumps(e[2])) for e in similar]
    res, reply = get_parsed_rfq(ref_request=test_rfq["request"],
                                product=reply['product'],
                                ex1=ex[0],
                                ex2=ex[1],
                                ex3=ex[2],
                                ex4=ex[3],
                                ex5=ex[4],
                                model=_ollama_model,
                                host=_ollama_host)
    print(f"\nreply: {json.dumps(reply, indent=4)}")
    compare_json_expected_actual(test_rfq['parameters'], reply)

if new_collection:
    print("\n############ D E L E T E  C O L L E C T I O N #########")
    persistent_client.delete_collection(name=collection.name)
    print(f"RfqRag - Collection {collection.name} deleted")

print(f"RfqRag - All Done\n")

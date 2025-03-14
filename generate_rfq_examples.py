import uuid
from rfq_generator import generate_random_rfq
from util import flatten_dict

## **NOTES**
## * **All** data, names, products etc in the demo are **totally fictional** and designed & invented up **just for illustration**.
## * The financial products are only partially defined, with sufficient just to prove they can be differentiated.

def generate_and_load_rfq_support_examples(_num_rfq: int, 
                                           embedding_generator: callable, 
                                           collection: object) -> dict:
    print("\n############ G E N E R A T E  T E S T  R F Q s #########\n")
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
    return res
    print("RfqRag - RFQ support examples loaded into Chroma\n")

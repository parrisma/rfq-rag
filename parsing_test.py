import json
from chroma_util import get_similar_rfqs
from compare import compare_json_expected_actual
from langchain_prompt import Example
from ollama_util import get_parsed_rfq, get_product_taxonomy
from rfq_generator import generate_random_rfq


def run_parsing_test(_num_test: int, 
                     _ollama_model: str, 
                     _ollama_host: str, 
                     _full_rfq_test: bool, 
                     embedding_generator: callable, 
                     collection: list) -> None:
    score = 0
    num_tests = _num_test

    for test_cycle in range(num_tests):
        print("\n############ C H E C K   E M B E D D I N G  ############")
        print("############ G E T  S I M I L A R  R F Q s #############\n")
        print(f"RfqRag - Generate random RFQ request for test cycle: {test_cycle}")
        test_rfq = generate_random_rfq()
        print(f"RfqRag - Get product taxonomy for RFQ [{test_rfq['request']}]")
        print(f"RfqRag - Meta: {json.dumps(test_rfq['parameters'], indent=4)}")
        res, reply = get_product_taxonomy(test_rfq["request"],
                                          model=_ollama_model,
                                          host=_ollama_host)
        if res:
            print(f"RfqRag - Get similar RFQs act as examples in RFQ parsing prompt")
            print(f"RfqRag - Product type: {reply['product']}")
            print(f"RfqRag - Language: {reply['language']}")
            print(f"RfqRag - Confidence: {reply['confidence']:.2f}")
            print(f"RfqRag - Explanation: {reply['explanation']}")
            print(f"RfqRag - Advice: {reply['advice']}")

            similar = get_similar_rfqs(test_rfq["request"],
                                       reply['product'],
                                       embedding_generator,
                                       collection)
            print(f"\nRfqRag - List of similar RFQ's with distances measure from the random RFQ")
            for d, r, m, u in similar:
                print(f"RfqRag - Dist: [{float(d):7.2f}], Doc: {r}")
        else:
            print(f"RfqRag - Error getting product taxonomy for RFQ")
            continue

        if _full_rfq_test and res:
            ex = [Example(e[1], json.dumps(e[2])) for e in similar]

            print("\n############ F U L L  R F Q  P A R S I N G ############")

            print(f"RfqRag - Parse RFQ using LLM for product type: {reply['product']}")
            res, reply = get_parsed_rfq(ref_request=test_rfq["request"],
                                        product=reply['product'],
                                        ex1=ex[0],
                                        ex2=ex[1],
                                        ex3=ex[2],
                                        ex4=ex[3],
                                        ex5=ex[4],
                                        model=_ollama_model,
                                        host=_ollama_host)
            print(f"\nrequest: {test_rfq['request']}")
            print(f"\nreply: {json.dumps(reply, indent=4)}")
            match, diffs = compare_json_expected_actual(test_rfq['parameters'], reply)
            if match:
                print(f"RfqRag - RFQ parsing correct")
                score += 1
            else:
                print(f"RfqRag - RFQ parsing failed")
                print(f"RfqRag - Differences: {json.dumps(diffs, indent=4)}")
    if _full_rfq_test:
        print(f"\nFull RFQ Test Score: ({(score/_num_test)*100:.0f}%)")

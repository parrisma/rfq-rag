import json
from chroma_util import get_similar_rfqs
from compare import compare_json_expected_actual
from langchain_prompt import Example
from ollama_util import get_parsed_rfq, get_product_taxonomy
from rfq_generator import generate_random_rfq
import uuid


def run_parsing_test(_similarity_test: bool,
                     _full_rfq_test: bool,
                     _num_test: int,
                     _ollama_model: str,
                     _ollama_host: str,
                     embedding_generator: callable,
                     collection: list) -> None:
    score = 0
    num_tests = _num_test

    print("\n############ R U N  F U L L  T E S T S  #################\n")
    print(f"RfqRag - Running [{num_tests}] test cycles")
    for test_cycle in range(num_tests):
        test_id = str(uuid.uuid4())
        print("\n----------------------------------------------------------------\n")
        print(f"\nRfqRag - Generate random RFQ request for test cycle: [{test_cycle}] with test id: [{test_id}]")
        test_rfq = generate_random_rfq()

        print(f"RfqRag - Test RFQ [{test_rfq['request']}]")
        res, reply = get_product_taxonomy(test_rfq["request"],
                                          model=_ollama_model,
                                          host=_ollama_host)
        if res:
            if _similarity_test:
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
            print(f"\nRfqRag - List of similar RFQ's with distances measure to augment the prompt")
            for d, r, _, _ in similar:
                print(f"RfqRag - Dist: [{float(d):7.2f}], Doc: {r}")
        else:
            print(f"RfqRag - Error getting product taxonomy for RFQ - exiting tests")
            exit(1)

        if _full_rfq_test and res:
            ex = [Example(e[1], json.dumps(e[2])) for e in similar]
            print(f"RfqRag - Parse RFQ using LLM for product type: {reply['product']}")
            res, reply = get_parsed_rfq(ref_request=test_rfq['request'],
                                        product=reply['product'],
                                        ex1=ex[0],
                                        ex2=ex[1],
                                        ex3=ex[2],
                                        ex4=ex[3],
                                        ex5=ex[4],
                                        test_id=test_id,
                                        model=_ollama_model,
                                        host=_ollama_host)
            print(f"\nConfidence: {reply['confidence']}")
            print(f"Explanation: {reply['explanation']}") 
            print(f"Advice: {reply['advice']}")
            match, diffs = compare_json_expected_actual(test_rfq['parameters'], reply)
            if match:
                print(f"RfqRag - RFQ parsing correct")
                print(f"RfqRag - Parsed Parameters: {json.dumps(test_rfq['parameters'], indent=4)}")
                save_params(test_rfq["parameters"], test_id)
                score += 1
            else:
                print(f"RfqRag - RFQ parsing failed")
                print(f"RfqRag - Differences: {json.dumps(diffs, indent=4)}")
    if _full_rfq_test:
        print(f"\nFull RFQ Test Score: ({(score/_num_test)*100:.0f}%)")


def save_params(params: dict,
                test_id: str) -> None:
    try:
        with open(f"params-{test_id}.json", "w") as f:
            json.dump(params, f, indent=4)
            print(f"RfqRag - Parameters saved to: params-{test_id}.json")
    except Exception as e:
        print(f"RfqRag - Error saving parameters: {e} exiting test [{test_id}]")
        exit(1)

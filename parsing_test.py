import uuid
import json
from chroma_util import get_similar_rfqs
from compare import compare_json_expected_actual
from langchain_prompt import Example
from ollama_util import get_parsed_rfq, get_product_taxonomy
from rfq_generator import generate_random_rfq
from trail import log


def run_parsing_test(similarity_test: bool,
                     full_rfq_test: bool,
                     num_test: int,
                     ollama_model: str,
                     ollama_host: str,
                     temperature: float,
                     embedding_generator: callable,
                     collection: list) -> None:
    score = 0
    num_tests = num_test

    log().debug("\n############ R U N  F U L L  T E S T S  #################\n")
    log().debug(f"Running [{num_tests}] test cycles")
    for test_cycle in range(num_tests):
        test_id = str(uuid.uuid4())
        log().debug("\n----------------------------------------------------------------\n")
        log().debug(f"\nRfqRag - Generate random RFQ request for test cycle: [{test_cycle}] with test id: [{test_id}]")
        test_rfq = generate_random_rfq()

        log().debug(f"Test RFQ [{test_rfq['request']}]")
        res, reply = get_product_taxonomy(test_rfq["request"],
                                          model=ollama_model,
                                          host=ollama_host,
                                          temperature=temperature)
        if res:
            if similarity_test:
                log().debug(f"Get similar RFQs act as examples in RFQ parsing prompt")
                log().debug(f"Product type: {reply['product']}")
                log().debug(f"Language: {reply['language']}")
                log().debug(f"Confidence: {reply['confidence']:.2f}")
                log().debug(f"Explanation: {reply['explanation']}")
                log().debug(f"Advice: {reply['advice']}")

            similar = get_similar_rfqs(test_rfq["request"],
                                       reply['product'],
                                       embedding_generator,
                                       collection)
            log().debug(f"\nRfqRag - List of similar RFQ's with distances measure to augment the prompt")
            for d, r, _, _ in similar:
                log().debug(f"Dist: [{float(d):7.2f}], Doc: {r}")
        else:
            log().debug(f"Error getting product taxonomy for RFQ - exiting tests")
            exit(1)

        if full_rfq_test and res:
            ex = [Example(e[1], json.dumps(e[2])) for e in similar]
            log().debug(f"Parse RFQ using LLM for product type: {reply['product']}")
            res, reply = get_parsed_rfq(ref_request=test_rfq['request'],
                                        product=reply['product'],
                                        ex1=ex[0],
                                        ex2=ex[1],
                                        ex3=ex[2],
                                        ex4=ex[3],
                                        ex5=ex[4],
                                        test_id=test_id,
                                        model=ollama_model,
                                        host=ollama_host,
                                        temperature=temperature)
            log().debug(f"\nConfidence: {reply['confidence']}")
            log().debug(f"Explanation: {reply['explanation']}")
            log().debug(f"Advice: {reply['advice']}")
            match, diffs = compare_json_expected_actual(test_rfq['parameters'], reply)
            if match:
                log().debug(f"RFQ parsing correct")
                log().debug(f"Parsed Parameters: {json.dumps(test_rfq['parameters'], indent=4)}")
                save_params(test_rfq["parameters"], test_id)
                score += 1
            else:
                log().debug(f"RFQ parsing failed")
                log().debug(f"Differences: {json.dumps(diffs, indent=4)}")
    if full_rfq_test:
        log().debug(f"\nFull RFQ Test Score: ({(score/num_test)*100:.0f}%)")


def save_params(params: dict,
                test_id: str) -> None:
    try:
        with open(f"./data/params-{test_id}.json", "w") as f:
            json.dump(params, f, indent=4)
            log().debug(f"Parameters saved to: params-{test_id}.json")
    except Exception as e:
        log().debug(f"Error saving parameters: {e} exiting test [{test_id}]")
        exit(1)

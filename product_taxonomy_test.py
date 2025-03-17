import json
from ollama_util import get_product_taxonomy
from rfq_generator import generate_random_rfq
from trail import log


def product_type_test(num_test: int,
                      ollama_model: str,
                      ollama_host: str,
                      temperature) -> None:
    log().debug("\n############ U S E  M O D E L  T O  F I N D ###########")
    log().debug("############     P R O D U C T  T Y P E     ###########")
    score = 0
    num_tests = num_test
    for _ in range(num_tests):
        test_rfq = generate_random_rfq()
        res, reply = get_product_taxonomy(test_rfq["request"],
                                          model=ollama_model,
                                          host=ollama_host,
                                          temperature=temperature)
        log().debug(f"reply: {json.dumps(reply, indent=4)}")
        if (reply['product'] == test_rfq['product']):
            log().debug(f"Product Type Correct LLM prediction: [{reply['product']}] equals expected [{test_rfq['product']}]")
            score += 1
        else:
            log().debug(
                f"Product Type Incorrect LLM prediction: [{reply['product']}] does not equal expected [{test_rfq['product']}]")
        log().debug("\n------------------\n")
    log().debug(f"\nProduct Type Test Score: ({(score/num_test)*100:.0f}%)")

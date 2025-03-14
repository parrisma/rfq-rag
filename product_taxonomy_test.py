import json
from ollama_util import get_product_taxonomy
from rfq_generator import generate_random_rfq


def product_type_test(_num_test: int,
                      _ollama_model: str,
                      _ollama_host: str) -> None:
    print("\n############ U S E  M O D E L  T O  F I N D ###########")
    print("############     P R O D U C T  T Y P E     ###########")
    score = 0
    num_tests = _num_test
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
    print(f"\nProduct Type Test Score: ({(score/_num_test)*100:.0f}%)")

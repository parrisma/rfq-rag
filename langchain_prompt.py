from typing import List
from langchain.prompts import PromptTemplate

taxonomy_prompt_template = """
you are an expert sales trader on a structured equity derivatives desk.
You are given a request for a quote given and you must determine the type of structured equity derivative product the request is for.
your response can only be a product type in this comma separated list [{products}]
if the product type is not obvious or you have to make assumptions the response will be the single word unknown.
you will also assign a confidence level that you have the correct product.
your overall response will be in the form of a json message of this format:
[
    {{
        "product": "product type here",
        "confidence: " "between 0 and 100%",
        "explanation": "explanation of given product type here"
    }}
]
The request for quote is as follows:
{request}
"""

taxonomy_prompt = PromptTemplate(
    input_variables=["products", "request"],
    template=taxonomy_prompt_template
)


def get_taxonomy_prompt(product_list: List[str],
                        rfq: str) -> str:
    return taxonomy_prompt.format(products=", ".join(product_list),
                                  request=rfq)


parse_prompt_template = """
You are a sales trader on a structured equity derivatives desk.
Given the following examples of hand written structured equity derivatives RFQs,
please parse the RFQs into structured data fields that can be used to generate a trade ticket.
for each RFQ, please provide the following structured data fields:
- Trade Type
- Underlying
- Option Type
- Strike
- Expiry
- Quantity
"""

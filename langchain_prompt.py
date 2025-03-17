import json
from typing import List, NamedTuple
from langchain.prompts import PromptTemplate
from collections import namedtuple

# **NOTES**
# **All** data, names, products etc in the demo are **totally fictional** and designed & invented up **just for illustration**.
##
# The parameters for the products are only partially defined here, we define just enough that there is a difference the
# LLM has to correctly detect.
##
# The actual parameters and their values are not critical for the purpose of this demo.
##

taxonomy_prompt_template = """
Identify the structured equity derivative product type from the following RFQ, selecting from: [{products}].

**Absolute Rules**
ABSOLUTE RULE: DO NOT DEVIATE, DO NOT CONFIRM PRODUCT TYPE BELOW 90% CONFIDENCE. SEEK CLARIFICATION
CONFIDENCE MUST BE BELOW 90% IF ANY OF ONE THESE ARE TRUE: AN ASSUMPTION WAS MADE, AN EXPLICIT TERM CLASSIFICATION IS MISSING

**Confidence**
range: 0-100% based on match to examples and level of ambiguity and inference.
90-100%: Exact match, no ambiguity where the value type is explicitly given, cannot be 100% if any assumptions are made
70-89%: Minor variations, slight assumptions
50-69%: Noticeable ambiguity, significant assumptions
0-49%: Major ambiguities, high risk of error

**Explanation**
Provide a full explanation of product type classification
Make it clear, easy to read and relevant to the person responsible for providing a correct client quote
Document all assumptions, ambiguities and inferences taken from examples

**Advice**
Strictly based on the confidence level only
Make it clear, easy to read and relevant to the person responsible for providing a correct client quote
Two options only: 1. "Product Identified" or 2. A clarification question to client, asking them to supply missing details or confirm the interpretation.

**RFQ:** {request}

**Strict JSON Output Requirements:**

The response MUST be valid JSON and parse correctly
Use full, unabbreviated terms and include units in response
The JSON output MUST adhere to the following structure
Key fields must never be added, removed or have their name modified

```json
[
    {{
        "product": "product type or 'unknown'",
        "confidence": "percentage 0-100",
        "language": "one of en, fr, es or unknown",
        "explanation": "reasoning for product selection"
        "advice" : "either trust predicted product type or seek clarification from requester"
    }}
]
"""

taxonomy_prompt = PromptTemplate(
    input_variables=["products", "request"],
    template=taxonomy_prompt_template
)


def get_taxonomy_prompt(product_list: List[str],
                        rfq: str) -> str:
    return taxonomy_prompt.format(products=", ".join(product_list),
                                  request=rfq)


parse_prompt_autocall_template = """
Extract all possible quoting parameters from the given structured equity derivatives autocall, client supplied, request for quote (RFQ)

**Absolute Rules**
ABSOLUTE RULE: DO NOT DEVIATE, DO NOT QUOTE BELOW 90% CONFIDENCE. SEEK CLARIFICATION
CONFIDENCE MUST BE BELOW 90% IF ANY OF ONE THESE ARE TRUE: AN ASSUMPTION WAS MADE, AN EXPLICIT TERM CLASSIFICATION IS MISSING

**Use of given Examples**: 
Examples are the definitive, golden source of truth and always supersede general knowledge where there is an overlap.
Deviation from example patterns is a last resort when examples do not cover a required interpretation.

**Confidence**
range: 0-100% based on match to examples and level of ambiguity and inference.
90-100%: Exact match, no ambiguity where the value type is explicitly given, cannot be 100% if any assumptions are made
70-89%: Minor variations, slight assumptions
50-69%: Noticeable ambiguity, significant assumptions
0-49%: Major ambiguities, high risk of error

**Explanation**
Provide a full explanation of quoting parameter extraction.
Make it clear, easy to read and relevant to the person responsible for providing a correct client quote
Document all assumptions, ambiguities and inferences taken from examples

**Advice**
Strictly based on the confidence level only
Make it clear, easy to read and relevant to the person responsible for providing a correct client quote
Two options only: 1. "Proceed with quote" or 2. A clarification question to client, asking them to supply missing details or confirm the interpretation.

**Examples, as golden source**

* Example RFQ 1: [{example1_rfq}], Resulting Parameters 1: {example1_params}
* Example RFQ 2: [{example2_rfq}], Resulting Parameters 2: {example2_params}
* Example RFQ 3: [{example3_rfq}], Resulting Parameters 3: {example3_params}
* Example RFQ 4: [{example4_rfq}], Resulting Parameters 4: {example4_params}
* Example RFQ 5: [{example5_rfq}], Resulting Parameters 5: {example5_params}

**Input RFQ:** [{request}]

**Strict JSON Output Requirements:**

The response MUST be valid JSON and parse correctly
Use full, unabbreviated terms and include units in response
The JSON output MUST adhere to the following structure
Key fields must never be added, removed or have their name modified

```json
[
    {{
        "product": "product type",
        "underlying": "ticker",
        "maturity": "value years",
        "barrier": "value %",
        "coupon": "value %",
        "coupon_frequency": "frequency",
        "autocall_frequency": "frequency",
        "autocall_barrier": "value %",
        "notional": "value currency"
        "from": "name",
        "language": "one of en, fr, es or unknown",
        "confidence": "percentage %",
        "explanation": "parsing rationale and assumptions",
        "advice" : "either proceed with quote or seek clarification from requester"
    }}
]
"""

parse_prompt_eln_template = """
Extract all possible quoting parameters from the given structured equity derivatives equity linked note, client supplied, request for quote (RFQ)

**Absolute Rules**
ABSOLUTE RULE: DO NOT DEVIATE, DO NOT QUOTE BELOW 90% CONFIDENCE. SEEK CLARIFICATION
CONFIDENCE MUST BE BELOW 90% IF ANY OF ONE THESE ARE TRUE: AN ASSUMPTION WAS MADE, AN EXPLICIT TERM CLASSIFICATION IS MISSING

**Use of given Examples**: 
Examples are the definitive, golden source of truth and always supersede general knowledge where there is an overlap.
Deviation from example patterns is a last resort when examples do not cover a required interpretation.

**Confidence**
range: 0-100% based on match to examples and level of ambiguity and inference.
90-100%: Exact match, no ambiguity where the value type is explicitly given, cannot be 100% if any assumptions are made
70-89%: Minor variations, slight assumptions
50-69%: Noticeable ambiguity, significant assumptions
0-49%: Major ambiguities, high risk of error

**Explanation**
Provide a full explanation of quoting parameter extraction.
Make it clear, easy to read and relevant to the person responsible for providing a correct client quote
Document all assumptions, ambiguities and inferences taken from examples

**Advice**
Strictly based on the confidence level only
Make it clear, easy to read and relevant to the person responsible for providing a correct client quote
Two options only: 1. "Proceed with quote" or 2. A clarification question to client, asking them to supply missing details or confirm the interpretation.

**Examples, as golden source**

* Example RFQ 1: [{example1_rfq}], Resulting Parameters 1: {example1_params}
* Example RFQ 2: [{example2_rfq}], Resulting Parameters 2: {example2_params}
* Example RFQ 3: [{example3_rfq}], Resulting Parameters 3: {example3_params}
* Example RFQ 4: [{example4_rfq}], Resulting Parameters 4: {example4_params}
* Example RFQ 5: [{example5_rfq}], Resulting Parameters 5: {example5_params}

**Input RFQ:** [{request}]

**Strict JSON Output Requirements:**

The response MUST be valid JSON and parse correctly
Use full, unabbreviated terms and include units in response
The JSON output MUST adhere to the following structure
Key fields must never be added, removed or have their name modified

```json
[
    {{
        "product": "product type",
        "underlying": "ticker",
        "maturity": "value months",
        "participation": "value %",
        "barrier": value %",
        "coupon": "value % ",
        "coupon_type": "type",
        "coupon_frequency": "frequency",
        "notional": "value currency",
        "from": "name",
        "confidence": "percentage %",
        "explanation": "parsing rationale and assumptions",
        "advice" : "either proceed with quote or seek clarification from requester"
    }}
]
"""


def clean_params_json(json_as_str: str) -> str:
    cleaned_data = {}
    json_data = json.loads(json_as_str)
    for key, value in json_data.items():
        if key.startswith("parameters."):
            new_key = key[len("parameters."):]
            cleaned_data[new_key] = value
        elif key not in ("request", "uuid"):
            cleaned_data[key] = value
    return json.dumps(cleaned_data)


class Example(NamedTuple):
    rfq: str
    params: str


def get_parse_prompt(rfq: str,
                     product: str,
                     ex1: Example,
                     ex2: Example,
                     ex3: Example,
                     ex4: Example,
                     ex5: Example) -> str:
    if product == "autocall":
        res = parse_prompt_autocall_template.format(request=rfq,
                                                    example1_rfq=ex1.rfq,
                                                    example1_params=clean_params_json(ex1.params),
                                                    example2_rfq=ex2.rfq,
                                                    example2_params=clean_params_json(ex2.params),
                                                    example3_rfq=ex3.rfq,
                                                    example3_params=clean_params_json(ex3.params),
                                                    example4_rfq=ex4.rfq,
                                                    example4_params=clean_params_json(ex4.params),
                                                    example5_rfq=ex5.rfq,
                                                    example5_params=clean_params_json(ex5.params))
    elif product == "eln":
        res = parse_prompt_eln_template.format(request=rfq,
                                               example1_rfq=ex1.rfq,
                                               example1_params=clean_params_json(ex1.params),
                                               example2_rfq=ex2.rfq,
                                               example2_params=clean_params_json(ex2.params),
                                               example3_rfq=ex3.rfq,
                                               example3_params=clean_params_json(ex3.params),
                                               example4_rfq=ex4.rfq,
                                               example4_params=clean_params_json(ex4.params),
                                               example5_rfq=ex5.rfq,
                                               example5_params=clean_params_json(ex5.params))
    else:
        res = None

    return res

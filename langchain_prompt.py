from typing import List, NamedTuple
from langchain.prompts import PromptTemplate
from collections import namedtuple

taxonomy_prompt_template = """
Identify the structured equity derivative product type from the following RFQ, selecting from: [{products}].

**RFQ:** {request}

**Response (JSON):**

```json
[
    {{
        "product": "product type or 'unknown'",
        "confidence": "percentage (0-100)",
        "explanation": "reasoning for product selection"
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
Parse the following structured equity derivatives autocall RFQ into JSON, extracting product-specific parameters with consistent units.

**Examples:**

* RFQ: [{example1_rfq}], Parameters: {example1_params}
* RFQ: [{example2_rfq}], Parameters: {example2_params}
* RFQ: [{example3_rfq}], Parameters: {example3_params}
* RFQ: [{example4_rfq}], Parameters: {example4_params}
* RFQ: [{example5_rfq}], Parameters: {example5_params}

**Input RFQ:** [{request}]

**Output JSON (include units):**

```json
[
    {{
        "product": "product type",
        "underlying": "ticker",
        "maturity": "value months",
        "barrier": "value %",
        "coupon": "frequency",
        "coupon_rate": "value %",
        "autocall_frequency": "frequency",
        "autocall_barrier": "value %",
        "notional": "value currency",
        "from": "name",
        "confidence": "percentage %",
        "explanation": "parsing rationale and assumptions"
    }}
]
"""

parse_prompt_eln_template = """
Parse the following structured equity derivatives equity linked note (ELN) RFQ into JSON, extracting product-specific parameters with consistent units.

**Examples:**

* RFQ: [{example1_rfq}], Parameters: {example1_params}
* RFQ: [{example2_rfq}], Parameters: {example2_params}
* RFQ: [{example3_rfq}], Parameters: {example3_params}
* RFQ: [{example4_rfq}], Parameters: {example4_params}
* RFQ: [{example5_rfq}], Parameters: {example5_params}

**Input RFQ:** [{request}]

**Output JSON (include units):**

```json
[
    {{
        "underlying": "ticker",
        "maturity": "value months",
        "participation": "value %",
        "barrier": value %",
        "coupon": "value % ",
        "coupon_type": "frequency",
        "notional": "value currency",
        "from": "name",
        "confidence": "percentage %",
        "explanation": "parsing rationale and assumptions"
    }}
"""


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
                                                    example1_params=ex1.params,
                                                    example2_rfq=ex2.rfq,
                                                    example2_params=ex2.params,
                                                    example3_rfq=ex3.rfq,
                                                    example3_params=ex3.params,
                                                    example4_rfq=ex4.rfq,
                                                    example4_params=ex4.params,
                                                    example5_rfq=ex5.rfq,
                                                    example5_params=ex5.params)
    elif product == "eln":
        res = parse_prompt_eln_template.format(request=rfq,
                                               example1_rfq=ex1.rfq,
                                               example1_params=ex1.params,
                                               example2_rfq=ex2.rfq,
                                               example2_params=ex2.params,
                                               example3_rfq=ex3.rfq,
                                               example3_params=ex3.params,
                                               example4_rfq=ex4.rfq,
                                               example4_params=ex4.params,
                                               example5_rfq=ex5.rfq,
                                               example5_params=ex5.params)
    else:
        res = None

    return res

import json
from typing import List, NamedTuple
from langchain.prompts import PromptTemplate
from collections import namedtuple

taxonomy_prompt_template = """
Identify the structured equity derivative product type from the following RFQ, selecting from: [{products}].

**Strict Clarification Policy:*

* **Any ambiguity or potential for multiple interpretations MUST result in a request for clarification.**
* **If there is ANY doubt about the meaning of a term or phrase, request clarification.**
* **Assume the worst-case scenario regarding ambiguity and prioritize accuracy over speed.**

**Instructions:**

1.  Identify the product type based on the RFQ
2.  Provide a confidence level for the identification
3.  Determine the language of the RFQ is written in
4.  **Explanation Section:**
    * Explicitly state all assumptions made during parsing.
    * If any term or phrase has the potential for multiple interpretations, clearly state the ambiguity and explain how it was resolved.
    * Reduce the "confidence" value significantly if any assumptions or ambiguous terms were used.
5.  **Advice Section:**
    * **NEVER state "ok to quote" if there is ANY ambiguity.**
    * **ALWAYS write a request for clarification, addressed to the requester, stating precisely what needs clarification, if there is ANY doubt.**
    * The request for clarification should be a complete sentence and directly address the requester.

**RFQ:** {request}

**Response (JSON):**

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
Parse the following structured equity derivatives autocall RFQ into JSON, extracting product-specific parameters with consistent units.

**Crucial Guidance: Examples as the Definitive Standard**

* **The provided examples are the ABSOLUTE and UNDISPUTED source of truth for how RFQ language maps to specific parameters.**
* **You MUST treat the examples as the GOLD STANDARD. Any deviation from the patterns and relationships demonstrated in the examples is STRONGLY DISCOURAGED.**
* **Your primary task is to identify and replicate the patterns of language-to-parameter mapping found in the examples.**
* **PRIORITIZE the examples above any general knowledge, assumptions, or interpretations. If a pattern is clearly established in the examples, you MUST adhere to it, even if it contradicts other information.**
* **Pay close attention to how specific phrases and keywords in the examples correspond to particular parameters and their units.**
* **Maintain CONSISTENCY with the examples in terms of parameter extraction, unit representation, and JSON structure.**

**Strict Clarification Policy:**

* **Any ambiguity or potential for multiple interpretations MUST result in a request for clarification.**
* **If there is ANY doubt about the meaning of a term or phrase, request clarification.**
* **Assume the worst-case scenario regarding ambiguity and prioritize accuracy over speed.**

**Instructions:**

1.  **Extract Product Parameters:** 
    * Extract all relevant product-specific parameters with consistent units.
    * Every parameter must be quoted with units
    * Use the examples as the primary source of truth for how RFQ language maps to parameters.
    * Use FULL, UNABBREVIATED terms in the output JSON.
2.  **Explanation Section:**
    * Explicitly state all assumptions made during parsing.
    * If any term or phrase has the potential for multiple interpretations, clearly state the ambiguity and explain how it was resolved.
    * Reduce the "confidence" value significantly if any assumptions or ambiguous terms were used.
3.  **Advice Section:**
    * **NEVER state "ok to quote" if there is ANY ambiguity.**
    * **ALWAYS write a request for clarification, addressed to the requester, stating precisely what needs clarification, if there is ANY doubt.**
    * The request for clarification should be a complete sentence and directly address the requester.
    
**Examples:**

* RFQ: [{example1_rfq}], Parameters: {example1_params}
* RFQ: [{example2_rfq}], Parameters: {example2_params}
* RFQ: [{example3_rfq}], Parameters: {example3_params}
* RFQ: [{example4_rfq}], Parameters: {example4_params}
* RFQ: [{example5_rfq}], Parameters: {example5_params}

**Input RFQ:** [{request}]

**Strict JSON Output Requirements:**

* **The response MUST be valid JSON and parse correctly.**
* **The JSON output MUST adhere to the following structure:**

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
        "language": "one of en, fr, es or unknown",
        "confidence": "percentage %",
        "explanation": "parsing rationale and assumptions",
        "advice" : "either proceed with quote or seek clarification from requester"
    }}
]
"""

parse_prompt_eln_template = """
Parse the following structured equity derivatives autocall RFQ into JSON, extracting product-specific parameters with consistent units.

**Crucial Guidance: Examples as the Definitive Standard**

* **The provided examples are the ABSOLUTE and UNDISPUTED source of truth for how RFQ language maps to specific parameters.**
* **You MUST treat the examples as the GOLD STANDARD. Any deviation from the patterns and relationships demonstrated in the examples is STRONGLY DISCOURAGED.**
* **Your primary task is to identify and replicate the patterns of language-to-parameter mapping found in the examples.**
* **PRIORITIZE the examples above any general knowledge, assumptions, or interpretations. If a pattern is clearly established in the examples, you MUST adhere to it, even if it contradicts other information.**
* **Pay close attention to how specific phrases and keywords in the examples correspond to particular parameters and their units.**
* **Maintain CONSISTENCY with the examples in terms of parameter extraction, unit representation, and JSON structure.**

**Strict Clarification Policy:**

* **Any ambiguity or potential for multiple interpretations MUST result in a request for clarification.**
* **If there is ANY doubt about the meaning of a term or phrase, request clarification.**
* **Assume the worst-case scenario regarding ambiguity and prioritize accuracy over speed.**

**Instructions:**

1.  **Extract Product Parameters:** 
    * Extract all relevant product-specific parameters with consistent units.
    * Every parameter must be quoted with units
    * Use the examples as the primary source of truth for how RFQ language maps to parameters.
    * Use FULL, UNABBREVIATED terms in the output JSON.
2.  **Explanation Section:**
    * Explicitly state all assumptions made during parsing.
    * If any term or phrase has the potential for multiple interpretations, clearly state the ambiguity and explain how it was resolved.
    * Reduce the "confidence" value significantly if any assumptions or ambiguous terms were used.
3.  **Advice Section:**
    * **NEVER state "ok to quote" if there is ANY ambiguity.**
    * **ALWAYS write a request for clarification, addressed to the requester, stating precisely what needs clarification, if there is ANY doubt.**
    * The request for clarification should be a complete sentence and directly address the requester.

**Examples:**

* RFQ: [{example1_rfq}], Parameters: {example1_params}
* RFQ: [{example2_rfq}], Parameters: {example2_params}
* RFQ: [{example3_rfq}], Parameters: {example3_params}
* RFQ: [{example4_rfq}], Parameters: {example4_params}
* RFQ: [{example5_rfq}], Parameters: {example5_params}

**Input RFQ:** [{request}]

**Strict JSON Output Requirements:**

* **The response MUST be valid JSON and parse correctly.**
* **The JSON output MUST adhere to the following structure:**

```json
[
    {{
        "product": "product type",
        "underlying": "ticker",
        "maturity": "value months",
        "participation": "value %",
        "barrier": value %",
        "coupon": "value % ",
        "coupon_type": "frequency",
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

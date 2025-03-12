# Overview

## Table of Contents

- [Design Overview](#design-overview)
- [Problem Statement](#problem-statement)
- [Application of RAG](#application-of-rag)
- [Demo Operation](#create-examples)
    1. [Creating Example RFQs](#create-examples)
    1. [Retrieve Relevant Examples](#retrieve-relevant-examples)

## Design Overview

Retrieval Augmented Generation (RAG) is a valuable technique when you need a Large Language Model (LLM) to generate responses based on:

* **Up-to-date information:** For tasks involving very recent news.
* **Internal data:** For accessing your organization's proprietary information.
* **Specialized interpretations:** For requiring context-specific understanding beyond general knowledge.

## Problem Statement

**Objective:** 
* Automate RFQ pricing detail extraction for seamless client quoting.

**Key Results:**

* Accurate, multilingual (EN, FR, ES) pricing data structured for automated systems reply.
* Confidence scoring implemented to prevent low-confidence automated responses.
* Clear, LLM-generated explanations of parsing assumptions provided.
* Client clarification requests generated when necessary.

## Application of RAG

1. **Create Examples** Select cross section of relevant data to act as examples in prompt.
1. **Receive RFQ to automate** 
1. **Retrieve Relevant Examples:** Gather examples related to the current RFQ automation.
1. **Augment the Prompt:** Add example directly in the prompt to automate RFQ response.
1. **Prioritize the Examples:** LLM responds with given examples as source of truth.
1. **Reply to Client**: Process RFQ of if LLM response ambiguous, seek client clarification

## Creating Example RFQs

We need to [create a varied set of RFQ examples](https://github.com/parrisma/rfq-rag/blob/main/rfq_generator.py), covering different clients, languages, and products, and manually verify the pricing for each, given a request and response we can save for later use.

![Alt text](./rag-example-creation.png)

The demo project creates totally fictional requests for quote for two financial products. These RFQ,s, by design, are colloquial, with typo's and abbreviations and are in three languages, examples below

```text
> Veuillez tarifer cette eln. Coupon 3 pct fix, Action RSH.T,  40 pct, Taille USD $40000, Terme 2 ans, Fréq Cpn annuel, Part 70 pct. Veuillez répondre quand vous le pouvez. David

> Necesito un precio para esta autocall RFQ, gracias. Monto USD $50000, Sub EDA.US, Venc 3 años, Cupón an, frecuencia auto trim, barr auto 100 porcentaje,  60 pct,  15 pct. Saludos, avísame. Alejandro

> Need a price on dis eln RFQ, thx.  40 percent, Cpn 2 % fixed, Under TPH.SW, Notional USD $5000,  quarterly, Participation 90 percent, Mat 2 yrs. Thank you in advance for your prompt response. Grace
```
For each example we also remember the exact details, such that we can save and use the text and the expected result as examples to give to the model.

```json
"parameters": {
    "underlying": "TGF.PA",
    "maturity": "1 years",
    "barrier": "60 percent",
    "coupon": "annually",
    "coupon_rate": "10 percent",
    "autocall_frequency": "annual",
    "autocall_barrier": "102 percent",
    "notional": "USD $10000",
    "from": "Ben Davis",
    "language": "en"
}
```
## Example Saving to Vector Database.

When we get our RFQ we need to be able to look up similar

## Retrieve Relevant Examples

### Explanation

A big part of RAG is being able to find examples to add to the prompt that are similar in *meaning*, in our case similar quotes. 

Imagine you want to find wise quotes that are similar in meaning to a specific one, not just ones that use the same words. Regular text search is like looking for an exact word match, missing the underlying message. 

To solve this, we use embeddings and vector databases. Embeddings turn quotes into sets of numbers that capture their meaning. Think of it as creating a map where quotes with similar meanings are placed closer together. 

Vector databases store these number-maps along with the original quotes. So when you ask for quotes with similar meaning, the database finds the number-maps that are closest to your example, and then gives you the corresponding quotes. 

So, it allows computers to understand the "gist" of the quotes and find related ones based on their meaning, not just their words.

### Example

if we get the RFQ
```text
¿Podría cotizar este instrumento autocall?  1 años, Subyac CIF.T,  semestralmente,  semestralmente, Barrera 60 pct,  12 porcentaje,  105 %, Nominal USD $20000. Por favor avisa cuando tengas precios disponibles. Enrique Martínez
```
We need five similar examples, with the expected parameters (as JSON) to embed in the prompt. So we ask the vector DB (Chroma) to search for similar examples we saved earlier. As we can see below it has found examples in spanish (even tho the database has english and spanish also), they are also for teh same financial product.

```text
> Dist: [7661.57], Doc: Oye, cotiza esta autocall. barr auto 105 porcentaje, Nominal USD $10000, frec llamada semestralmente, Subyacente LZL.US, Plazo 1 años,  12 %, Barrera 50 %, Cupón semi. Por favor, házmelo saber cuando tengas el precio. Francisco Martínez

> Dist: [9708.86], Doc: Estoy buscando una cotización rápida para esta autocall. Barrera 50 %, frec auto anual,  anual, Venc 2 años,  15 porcentaje, Subyac YSR.MX, Nominal USD $40000, barrera auto 100 %. Gracias, avísame pronto. Francisco Martínez

> Dist: [14481.69], Doc: Oye, ¿alguna idea de precio para esta autocall RFQ? Cantidad USD $45000, Barrera 50 %, barr auto 102 pct,  15 %, Expiración 2 años, frecuencia auto anualmente, Cupón anualmente,  CDM.HK. Avísame tus pensamientos. Alejandro Ruiz

> Dist: [18032.08], Doc: Necesitamos un precio para esta autocall. frecuencia de autocall anual, Plazo 5 años,  anual, Acción LZL.US,  70 pct, barrera de autocall 102 porcentaje, Cantidad USD $20000,  10 porcentaje. Por favor avisa cuando tengas un precio. Ivonne Williams

> Dist: [18782.44], Doc: ¿Alguna posibilidad de conseguir una cotización para esta nota autocall?  8 porcentaje,  102 %, Cup anualmente, frec anualmente, Ticker LVL.PA,  USD $40000, Barrera 50 %, Expiración 5 años. Avísame cuando lo tengas. Jacobo
```

### Resulting Prompt

Here is a full example of a [prompt with examples](./rfq-prompt-with-examples.html). The added examples are in red and the prompt being parsed is shown in blue.

This was formed using langchain library, which takes a simple text template and allows values to be embdded.

e.g.
```python
# Define template with what you need to configure
template = PromptTemplate.from_template(
    """
    Write a short story about a {animal} that wants to be a {profession}. 
    The story should be set in {location} and have a {tone} tone.
    """
)

# Inject the configurable details
prompt = template.format(
    animal="squirrel",
    profession="chef",
    location="a bustling city park",
    tone="humorous",
)
```
This is all **totally imaginary** data, but if you cut and paste the whole prompt into any web based LLM such as Gemini, you will see that it can parse the rfq and will give output as below. This is exactly what we do in the demo, except the LLM we call is one running locally (privatly) on our computer. 


```json
[
    {
        "product": "eln",
        "underlying": "TER.L",
        "maturity": "12 years",
        "participation": "80 percent",
        "barrier": "50 percent",
        "coupon": "2 percent",
        "coupon_type": "fixed",
        "coupon_frequency": "quarterly",
        "notional": "USD $35000",
        "from": "Ali",
        "confidence": "100%",
        "explanation": "Extracted all parameters based on the patterns observed in the provided examples. The term 'qtr' is interpreted as 'quarterly', and 'Und' is interpreted as 'underlying'. 'Mat' is interpreted as maturity. The coupon is indicated as '2 % fixed' which is parsed as coupon of 2 percent and coupon type of fixed.",
        "advice": "ok to quote"
    }
]
```

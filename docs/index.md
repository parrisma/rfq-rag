# Automating Tedious Tasks with AI: RFQ Parsing with RAG

Click here for [Demo project repository](https://github.com/parrisma/rfq-rag/) & full code

**NOTE** *all product terms, names etc used in this demo are 100% fictional, made up just for the purpose of illustration.*

## Contents

1. [Overview](#overview)
1. [Approach](./main)
1. [Deployment](./deployment)
1. [Demo Examples](./demo)
1. **Concepts** (external links)
   - [Retrieval Augmented Generation](https://www.google.com/url?sa=E&source=gmail&q=https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/)
   - [Prompt Engineering](https://www.google.com/url?sa=E&source=gmail&q=https://platform.openai.com/docs/guides/prompt-engineering)
   - [LangChain as RAG workflow](https://www.google.com/search?q=https://python.langchain.com/docs/get_started/introduction.html)
   - [Vector Databases](https://www.google.com/url?sa=E&source=gmail&q=https://www.pinecone.io/learn/vector-database/)
   - [LLM Model hosting, Ollama](https://ollama.com/)
   - [Structured Products](https://www.investopedia.com/articles/optioninvestor/07/structured_products.asp), [ELN](https://www.investopedia.com/terms/e/equity-linkednote.asp) and [Autocall](./autocall.md)

## Overview
Repetitive tasks drain energy and stifle creativity. So, how do we offload them to AI? Large Language Models (LLMs) offer a powerful solution, but they often lack the specialized knowledge or access to sensitive data required for real-world applications.

That's where **Retrieval Augmented Generation (RAG)** comes in! Imagine running your own private LLM, safe from internet exposure, and injecting it with the precise data it needs to excel. This is RAG's super power.

But how do we find that "precise data"? Understanding the context of complex information is key. This is where **vector databases** shine. They allow us to store and retrieve documents based on their semantic similarity to a given query, ensuring the LLM gets the most relevant information.

**This demo project tackles a real-world challenge: parsing handwritten client requests for quotes (RFQs) on specialized financial products.**

These RFQs are:

* **Technical and complex:** Full of jargon and intricate details.
* **Multilingual:** Arriving in English, French, and Spanish.
* **Variable:** Written with typos, abbreviations, and jumbled information.

Because we're dealing with client interactions, accuracy is paramount. We need a system that does not misinform. So, to simulate this challenge, we've generated hundreds of realistic, albeit **fictional**, RFQs. These requests, covering two complex product types, are designed to mimic the chaos of real-world client communications.

**Our RAG-powered solution delivers:**

* **Accurate Trade Term Extraction:**
    * As structured text for direct automated pricing.
* **Reliable Confidence Levels:**
    * 0-100% risk assessment for direct replies.
* **Clear Assumption Explanations:**
    * Written reasoning and assumptions made by LLM.
* **Actionable Recommendations:**
    * Advice to reply (high confidence) or detailed request to client for clarification.

## Work Flow

The full workflow is shown below.

![Creation of Examples](./main/rag-full-flow.png)

1. **RFQ From Client**
    * free test in any of three languagess fr two product types
1. **Get similar examples to client RFQ**
    * Use embeddings & vector DB to get sematically similar quotes
1. **Create the prompt with RFQ & examples**
    * Supply examples to prompt to give LLM specialist knowledge
1. **Ask LLM to extract parameters & explanation**
    * The explanation helps with the AI explainability problem if the result is questioned by client in the future
1. **If all OK price the product**
    * If extract is confident, we can auto price
1. **Pass price or error report to trader**
    * The price will be sent back, normally via person for sanity checks
    * Trader can also look a clarification commentary from model
1. **Pass price or request for clarification with client**
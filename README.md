# Automating Tedious Tasks with AI: RFQ Parsing with RAG

Let's face it, repetitive tasks drain our energy and stifle creativity. But what if we could offload them to AI? Large Language Models (LLMs) offer a powerful solution, but they often lack the specialized knowledge or access to sensitive data required for real-world applications.

That's where **Retrieval Augmented Generation (RAG)** comes in! Imagine running your own private LLM, safe from internet exposure, and injecting it with the precise data it needs to excel. This is RAG's magic.

But how do we find that "precise data"? Understanding the context of complex information is key. This is where **vector databases** shine. They allow us to store and retrieve documents based on their semantic similarity to a given query, ensuring the LLM gets the most relevant information.

**This demo project tackles a real-world challenge: parsing handwritten client requests for quotes (RFQs) on specialized financial products.**

These RFQs are:

* **Technical and complex:** Full of jargon and intricate details.
* **Multilingual:** Arriving in English, French, and Spanish.
* **Variable:** Written with typos, abbreviations, and jumbled information.

And because we're dealing with client interactions, accuracy is paramount. We need a system that:

* **Extracts trade terms with precision:** Converting messy text into structured data for automated pricing.
* **Provides a confidence score:** Letting us know when to seek clarification.
* **Explains its reasoning:** Detailing any assumptions made.
* **Recommends action:** Advising whether to quote or request more information.

To simulate this challenge, we've generated hundreds of realistic, albeit fictional, RFQs. These requests, covering two complex product types, are designed to mimic the chaos of real-world client communications.

**Our RAG-powered solution delivers:**

* **Accurate Trade Term Extraction:**
    * As structured text for direct automated pricing.
* **Reliable Confidence Levels:**
    * 0-100% risk assessment for direct replies.
* **Clear Assumption Explanations:**
    * Written reasoning and assumptions made by LLM.
* **Actionable Recommendations:**
    * Advice to reply (high confidence) or detailed request to client for clarification.

**Dive deeper into the project and explore a live demo on [GitHub Pages](https://parrisma.github.io/rfq-rag/) to see how this is all possible!**
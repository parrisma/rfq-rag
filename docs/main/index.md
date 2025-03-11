# Overview

## Project Overview

Retrieval Augmented Generation (RAG) is a valuable technique when you need a Large Language Model (LLM) to generate responses based on:

* **Up-to-date information:** For tasks involving very recent news.
* **Internal data:** For accessing your organization's proprietary information.
* **Specialized interpretations:** For requiring context-specific understanding beyond general knowledge.

## RAG Explained

The RAG process is simple:

1.  **Retrieve Relevant Data:** Gather data specifically related to the current context.
2.  **Augment the Prompt:** Include this retrieved data directly in the prompt sent to the LLM.
3.  **Prioritize the Data:** Clearly instruct the LLM to treat the provided data as the primary source of truth.

**Example: RFQ Parsing**

In this project's Request for Quote (RFQ) parsing scenario:

* We retrieve five previously parsed RFQs that are similar to the new RFQ.
* We include these examples, showing their correct pricing parameter extractions, in the prompt.
* We instruct the LLM to use these examples as a guide for parsing the new RFQ.

Here is a full example of a [prompt with examples](./rfq-prompt-with-examples.pdf)
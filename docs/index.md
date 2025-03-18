# Automating Tedious Manual Finance Tasks with LLMs

Click here for [Demo project repository](https://github.com/parrisma/rfq-rag/) & full code

## NOTES

* **All** data, names, and products in the demo are fictional and for illustration only.
* The financial products are partially defined, just enough to show differentiation.

## Contents

1. [Automation Challenge](#historical-challenge)
    1. [LLMs gaps for automation tasks](#llms-gaps-for-automation-tasks)
    1. [The LLM Model Temperature Paradox](#the-llm-model-temperature-paradox)
    1. [Retrieval Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
    1. [Commodity Process](#commodity-process)
    1. [Intuition](#intuition)
    1. [Demo: Parsing Requests for Quotes](#demo-parsing-requests-for-quotes)
1. [Conclusion](#conclusion)
1. [Core Concepts](#core-concepts)
1. [Technology](#technology)
1. [WorkFlow](#workflow)
1. [Example LLM Prompt](./main/rfq-prompt-with-examples.html) _test it on your favourite WEB LLM_

## Historical Challenge

Manual processing of written financial workflows is inefficient, error-prone, and costly. Automation has been attempted for decades but often fails due to its rigidity and inability to adapt to changes in written processes. This limitation can now be addressed using Large Language Models (LLMs).

### LLMs gaps for automation tasks

LLMs bring automation potential but face key challenges:

1. **Missing Specifics**: LLMs lack real-time or company-specific knowledge essential for accurate financial tasks.
1. **Non-Determinism**: Responses can vary, causing inconsistent automation, a.k.a. Model temperature (see [The LLM Model Temperature Paradox](#the-llm-model-temperature-paradox))
1. **Explainability**: Finance requires clear explanations for audits and compliance, which historical automation has not been able to supply.

### The LLM Model Temperature Paradox

Imagine asking 100 journalists to summarize a breaking news story for traders. You want them to use their expertise but also provide consistent summaries. If they write creatively, the summaries will vary wildly; if they think and write too rigidly, salient details may be missed. This is akin to an LLM's "temperature setting": high temperature promotes creativity but inconsistent results; low temperature ensures consistency but risks overlooking key details. So, in any LLM automation solution, striking the right balance is essential for reliable automation.

### Retrieval Augmented Generation (RAG)

RAG enables LLMs to understand written requests better. It incorporates proprietary and **specialized knowledge** into AI workflows, addresses **explainability**, and—with the right model temperature—can produce **deterministic** results for onward automation.

### Commodity Process

It's now quick and cost-effective to deploy RAG solutions using readily available LLMs, private model hosting (even on PCs with GPUs !), and open-source or enterprise vector databases.

### Intuition

Getting the **intuition** for RAG into the hands of those performing manual tasks allows their perspective to shape its application, uncover more opportunities, and improve client services, thus cutting costs.

### Demo: Parsing Requests for Quotes

As an example, consider automating the parsing of manual requests for quotes (RFQs) for structured products. We have created a demo that illustrates the approach's potential.

The demo solution handles RFQs in English, French, and Spanish, including colloquial language, abbreviations, and typos, for two types of structured products, and delivers on:

* **Specific Knowledge**: Prompt augmented with related pre parsed RFQs.
* **Determinism**: Produces reliable JSON outputs for automation.
* **Explainability**: Clearly explains reasoning and assumptions.

This demonstrates how RAG connects complex language to automated, regulated finance workflows.

**Dive deeper into the project on our [GitHub Pages](https://parrisma.github.io/rfq-rag/) to see how this is works!**

## Conclusion

RAG has been around for a while but still has significant untapped applications in automating residual or enduring manual comprehension process.

However its not a free lunch

* Much can be automated but it does not 100% eliminate human oversight.
* Commodity tooling, but requires specialists to build and operate.
* Models have bias, so on-going evaluation and selection is needed.
* Vector databases contain much sensitive data needing appropriate security.
* Compute costs could be a factor at scale as running LLM's is compute intensive.
* Regulatory approval would be an issue with customer facing applications.
* Augmentation examples must be kept current as a data driven process.
* Determinism is not guaranteed, so error detection must be designed in.

## Core Concepts

1. **Understanding**
    * Large language models [understand](./main/rfq-prompt-with-examples.html#rules) the meaning of text, not just the words. This lets them interpret requests like 'extract pricing terms' even if there are abbreviations, shortcuts, or mistakes. And they can work across languages, like in our demo with Spanish, French, and English.
1. **Augmentation**
    * LLMs convert text into a kind of 'meaning code' called embeddings. This allows them to see when texts are similar. We use this to store correctly interpreted past RFQs in a special database (vector database), where the 'meaning code' is the key. So when we ask the LMM to interpret a new RFQ, the system finds similar past RFQs and their correct interpretations and adds them to the prompt. This helps the LLM give a more accurate answer, as it can use validated and very specific knowledge
1. **Explainability**
    * When AI makes decisions, we need to be able to explain how it arrived at those decisions or assumptions. If something goes wrong, we must be able to show why the AI made a certain choice. With the demo, the LLM explains its reasoning in plain language and provides a confidence score. If the score is low, the automation is interrupted to seek more clarification, this makes the process more reliable and transparent.

## Technology

1. [Ollama](https://ollama.com/) to run an host LLM's.
1. [ChromaDB](https://www.trychroma.com/) the vector database to support sematic augmentation.
1. [Langchain](https://www.google.com/search?q=https://python.langchain.com/docs/get_started/introduction.html) prompt building.
1. [Python](https://www.python.org/) as the glue language.

## WorkFlow

The full workflow is shown below.

![Workflow](./main/rag-full-flow.png)

1. **RFQ From Client**
    * free text in any of three languages for two product types
1. **Get similar examples to client RFQ**
    * Use embeddings & vector DB to get semantically similar quotes
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

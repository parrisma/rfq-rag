# Automating Tedious Manual Finance Tasks with LLMs

## NOTES

- **All** data, names, and products in the demo are fictional and for illustration only.
- The financial products are partially defined, just enough to show differentiation.

### Historical Challenge

Manual processing of written financial workflows is inefficient, error-prone, and costly. Automation has been attempted for decades but often fails due to its rigidity and inability to adapt to changes in written processes. This limitation can now be addressed using Large Language Models (LLMs).

### LLMs gaps for automation tasks

LLMs bring automation potential but face key challenges:

1. **Missing Specifics**: LLMs lack real-time or company-specific knowledge essential for accurate financial tasks.
2. **Non-Determinism**: Responses can vary, causing inconsistent automation, a.k.a. Model temperature (see [The LLM Model Temperature Paradox](#the-llm-model-temperature-paradox))
3. **Explainability**: Finance requires clear explanations for audits and compliance, which historical automation has not been able to supply.

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

- **Specific Knowledge**: Prompt augmented with related pre parsed RFQs.
- **Determinism**: Produces reliable JSON outputs for automation.
- **Explainability**: Clearly explains reasoning and assumptions.

This demonstrates how RAG connects complex language to automated, regulated finance workflows.

**Dive deeper into the project on our [GitHub Pages](https://parrisma.github.io/rfq-rag/) to see how this is works!**

### Conclusion

RAG has been around for a while but still has significant untapped applications in automating residual or enduring manual comprehension process.

However its not a free lunch

- Much can be automated but it does not 100% eliminate human oversight.
- Commodity tooling, but requires specialists to build and operate.
- Models have bias, so on-going evaluation and selection is needed.
- Vector databases contain much sensitive data needing appropriate security.
- Compute costs could be a factor at scale as running LLM's is compute intensive.
- Regulatory approval would be an issue with customer facing applications.
- Augmentation examples must be kept current as a data driven process.
- Determinism is not guaranteed, so error detection must be designed in.

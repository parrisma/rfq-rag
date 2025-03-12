# Way to use demo script

Click here for [Demo project repository](https://github.com/parrisma/rfq-rag/) & full code

## Table of Contents

- [See all demo commands](#see-all-demo-commands)
- [Generate RFQs' Only](#generate-rfqs-only)
- [Test getting similar RFQ only](#test-getting-similar-rfq-only)
- [Test full RFQ parsing](#test-full-rfq-parsing)

---

**Note**, _all of these commands are run from project root & after having started Ollama and Chroma, see [deployment](../deployment/index.md)_

## See all demo commands
```sh
python rfq-rag-main-demo -h
```

## Generate RFQs' Only
The following command generates RFQ's and loads them into the vector DB. This can be time consuming to do for 100's of examples as calculating the vector embeddings means calling the LLM for each one.

Generate 200 RFQ examples and then exit, these can be re used for subsequent tests
```sh
python rfq-rag-main-demo -nr 200
```

## Test getting similar RFQ only
Use the last RFQ's generated, run the similarity test for 5 newly generated RFQ's
```sh
python rfq-rag-main-demo -uc=last -st -nt=5
```

## Test full RFQ parsing
This test generates RFQs, creates augmented prompts which are then parsed by the LLM. The response from the LLM is then compared to the expected results and a count of success is maintained

Use the last RFQ's generated, run the full test for 5 newly generated RFQ's
```sh
python rfq-rag-main-demo -uc=last -ft -nt=5
```
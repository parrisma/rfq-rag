# RFQ Pasring with Retreival Augmented Generation

## Deployment

This is project uses docker to deploy the open source components needed

1. Ollama - Service for downloading and running large language model
1. ChromaDB - A vector database used to store example RFQs to specialise the LMM prompt. This is *retreival augmented* part of RAG
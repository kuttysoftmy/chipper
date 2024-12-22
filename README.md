<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/chipper_logo.jpeg" width="240" alt="Logo Chipper RAG Util"/></p>
<h3 align="center">Chipper</h3>

**Chipper** is a learning and research project by [Tilman Griesel](https://linktr.ee/griesel), the Retrieval Augmented
Generation (RAG) with
integrated large language models (LLMs). It supports embedding pipelines, document chunking, web content scraping and
query workflows.
query workflows. Chipper is based on **Haystack**, **Ollama** and **ElasticSearch** and can be used as a local tool
or an internal service that can be deployed via Docker.

**This is not a production-ready tool and should not be used as such. Users are responsible for any damages or issues
resulting from its use.**

If you find this project helpful, leaving a star would mean a lot and help others discover it too.

## Features

- Embedding pipelines for source code and documents.
- Document chunking for efficient and precise retrieval.
- Configurable scraper utility for web content integration.
- ElasticSearch for scalable vector-based retrieval.
- CLI and web client interfaces.
- Docker-ready for deployment.

## Installation and Setup

Use the **Makefile** to set up and run Chipper.

## Demo

<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/demo_01.gif"alt="Chipper RAG Util Demo"/></p>

## Roadmap & Open-Goals

1. **Docker Implementation**

   - Finalize current Docker setup to ensure streamlined deployment.
   - Test and validate the implementation across various environments.
   - Document the Docker workflow for ease of use by the team and contributors.

2. **Automated Model Management**

   - Implement automatic pulling and updating of Ollama models.
   - Add support for model versioning to maintain compatibility.
   - Provide clear logging and notifications for pull operations.

3. **Codebase Optimization**

   - Conduct a general cleanup of the codebase for readability and maintainability.
   - Remove unused dependencies and redundant code.
   - Standardize coding practices and implement linting tools.

4. **Enhanced Parameter Configurations**
   - Extend and refine the parameter settings available for Ollama models.
   - Introduce advanced options for fine-tuning and optimization.
   - Validate parameter changes with real-world use cases to ensure effectiveness.

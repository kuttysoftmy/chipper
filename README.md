<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/logo_chiper_bg.png" width="240" alt="Logo Chipper RAG Util"/></p>
<h3 align="center">Chipper</h3>

**Chipper** blends Retrieval-Augmented Generation (RAG) techniques with large language models (LLMs) to help with embedding pipelines, document chunking, web scraping, and query workflows. Built on **Haystack**, **Ollama**, **Docker**, **Tailwind** and **ElasticSearch**, you can use Chipper as a local tool or spin it up as a service with Docker.

This project started as a way to help my girlfriend with her new book. The idea was to use local RAG and LLMs to ask questions about characters and explore creative possibilities, all without sharing proprietary details or your own book with cloud services like ChatGPT. What began as a bunch of scripts is now growing into a fully dockerized service architecture.

**Quick note:** This is just a research project, so it’s not built for production. Use it for experimenting, and keep in mind you’re responsible for anything that goes sideways.

If you like what you see, leaving a star would be sweet and will help more people discover Chipper!

### Features

- Create embeddings for source code and documents.
- Break down documents into chunks for faster, smarter searches.
- Scrape web content with a tool you can tweak to fit your needs.
- Use ElasticSearch for powerful, scalable searches.
- Choose between a CLI or a web client interface.
- Easily deploy it with Docker.

## Installation and Setup

Use the **Makefile** to set up and run Chipper.

## Demo

<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/demo_01.png"alt="Chipper RAG Util Demo Web"/></p>
<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/demo_02.png"alt="Chipper RAG Util Demo Web"/></p>
<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/demo_03.png"alt="Chipper RAG Util Demo Web"/></p>

### Roadmap

1. **Streamlining Docker Setup**

   - Wrap up the current Docker configuration to make deployments easier.
     - **WIP**
   - Test it out in different environments to ensure everything works smoothly.
   - Put together a simple guide to help the team and contributors navigate the setup.

2. **Simplifying Model Management**

   - Set up a system to automatically pull and update Ollama models.
     - **WIP**
   - Add support for model versioning so compatibility is never an issue.
   - Make sure pull operations come with clear logs and handy notifications.

3. **Polishing the Codebase**

   - Tidy up the code to make it cleaner and easier to work with.
     - **WIP**
   - Get rid of unnecessary dependencies and redundant pieces of code.
   - Align with standardized coding practices and bring in linting tools to keep things consistent.

4. **Expanding Parameter Options**
   - Broaden and fine-tune the settings available for Ollama models.
   - Introduce more advanced options for tweaking and optimizing.
   - Test parameter changes with practical scenarios to confirm they deliver results.

---

## CLI Demo

<p align="center"><img src="https://raw.githubusercontent.com/TilmanGriesel/chipper/refs/heads/main/docs/public/assets/demo_cli_01.gif"alt="Chipper RAG Util Demo CLI"/></p>

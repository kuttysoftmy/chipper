import logging
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from typing import List, Set

from haystack import Document

from src.cli.helper import parse_args
from src.core.document_processor import DocumentProcessor
from src.core.rag_pipeline import RAGPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_blacklist(base_path: str) -> Set[str]:
    blacklist_file = Path(base_path) / '.ragignore'
    default_blacklist = {}

    if blacklist_file.exists():
        try:
            with open(blacklist_file, 'r') as f:
                custom_blacklist = {line.strip() for line in f if line.strip() and not line.startswith('#')}
            logger.info(f"Loaded custom blacklist from .ragignore: {custom_blacklist}")
            return default_blacklist.union(custom_blacklist)
        except Exception as e:
            logger.warning(f"Error reading .ragignore file: {e}. Using default blacklist.")
            return default_blacklist
    else:
        logger.info("No .ragignore file found. Using default blacklist.")
        return default_blacklist


def open_folder_dialog() -> str:
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(
        title='Select Folder with Documents',
        mustexist=True
    )

    return folder_path


def log_args(args):
    logger.info("Configuration:")
    config_dict = {
        "Elasticsearch URL": args.es_url,
        "Ollama URL": args.ollama_url,
        "Model": args.model,
        "Embedding Model": args.embedding_model,
        "Document Path": args.path or "Not specified",
        "File Extensions": ", ".join(args.extensions),
        "Skip Embedding": args.skip_embed,
        "Debug Mode": args.debug
    }

    for key, value in config_dict.items():
        logger.info(f"{key}: {value}")


def process_documents(args) -> List[Document]:
    logger.info("Starting document processing")
    blacklist = load_blacklist(args.path)
    processor = DocumentProcessor(
        base_path=args.path,
        file_extensions=args.extensions,
        blacklist=blacklist
    )
    documents = processor.process_files()
    logger.info(f"Processed {len(documents)} documents")
    return documents


def main():
    args = parse_args()

    log_args(args)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    try:
        logger.info("Initializing RAG pipeline")
        rag = RAGPipeline(
            es_url=args.es_url,
            ollama_url=args.ollama_url,
            model_name=args.model,
            embedding_model=args.embedding_model
        )
        logger.debug("RAG pipeline initialized successfully")

        if not args.skip_embed:
            if not args.path:
                logger.info("No document path provided, opening folder picker")
                args.path = open_folder_dialog()
                if not args.path:
                    logger.warning("No folder selected, skipping document embedding")
                    documents = []
                else:
                    logger.info(f"Selected folder: {args.path}")
                    documents = process_documents(args)
            else:
                documents = process_documents(args)

            if documents:
                logger.info("Starting document embedding")
                rag.embed_documents(documents)
                logger.info(f"Successfully embedded {len(documents)} documents")
            else:
                logger.warning("No documents to embed")

        if args.query:
            logger.info(f"Processing query: {args.query}")
            rag.run_query(args.query)
        else:
            logger.info("No query provided")

    except Exception as e:
        logger.error("Error in pipeline execution", exc_info=True)
        raise


if __name__ == "__main__":
    logger.info("Starting RAG Pipeline Execution")
    main()

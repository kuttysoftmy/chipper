import argparse
import os

from dotenv import load_dotenv

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process documents with text embeddings and query capability",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Document Processing Arguments
    parser.add_argument(
        "--path",
        type=str,
        help="Base path to process documents from"
    )

    parser.add_argument(
        "--extensions",
        type=str,
        nargs="+",
        default=[".txt", ".md", ".py", ".cpp", ".hpp", ".qml"],
        help="List of file extensions to process",
    )

    # Pipeline Control Arguments
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug logging"
    )

    parser.add_argument(
        "--skip-embed",
        action="store_true",
        help="Skip embedding"
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Query to run against the processed documents"
    )

    # Service Configuration
    parser.add_argument(
        "--es-url",
        type=str,
        default=os.getenv("ES_URL", "http://localhost:9200"),
        help="URL for the Elasticsearch service",
    )

    parser.add_argument(
        "--ollama-url",
        type=str,
        default=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        help="URL for the Ollama service",
    )

    # Model Configuration
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "llama2"),
        help="Model to use for query responses"
    )

    parser.add_argument(
        "--embedding-model",
        type=str,
        default=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        help="Model to use for embeddings",
    )

    args = parser.parse_args()

    return args

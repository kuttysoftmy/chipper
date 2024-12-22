import logging
import os
import secrets
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from haystack import Document
from werkzeug.middleware.proxy_fix import ProxyFix

from src.core.rag_pipeline import RAGPipeline

load_dotenv()

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["1000 per day", "10 per minute"],
    storage_uri="memory://"
)

API_KEY = os.getenv('WEB_API_KEY')
if not API_KEY:
    API_KEY = secrets.token_urlsafe(32)
    logger.info(f"Generated API key: {API_KEY}")

SYSTEM_PROMPT = os.getenv('WEB_SYSTEM_PROMPT', 'You are a helpful assistant.')

rag = RAGPipeline(
    es_url=os.getenv('ES_URL'),
    ollama_url=os.getenv('OLLAMA_URL'),
    model_name=os.getenv('MODEL_NAME'),
    embedding_model=os.getenv('EMBEDDING_MODEL'),
    system_prompt=SYSTEM_PROMPT
)


def process_query():
    try:
        data = request.get_json()
        query = data['query']
        conversation = data.get('conversation', [])

        result = rag.run_query(
            query=query,
            conversation=conversation,
            print_response=False
        )

        latest_interaction = [
            {"role": "user", "content": query,
             "timestamp": datetime.now().isoformat()},
            {"role": "assistant", "content": result["llm"]["replies"][0],
             "timestamp": datetime.now().isoformat()}
        ]

        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "conversation": conversation + latest_interaction
        })

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your request"
        }), 500


def process_embedding():
    try:
        data = request.get_json()
        if not data or 'documents' not in data:
            return jsonify({
                "success": False,
                "error": "No documents provided"
            }), 400

        documents = [Document(**doc) for doc in data['documents']]
        rag.embed_documents(documents)

        return jsonify({
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"Successfully embedded {len(documents)} documents"
        })

    except Exception as e:
        logger.error(f"Error processing embedding request: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your request"
        }), 500


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.before_request
def before_request():
    logger.info(f"Request {request.method} {request.path} from {request.remote_addr}")
    if os.getenv('WEB_REQUIRE_SECURE', 'False').lower() == 'true' and not request.is_secure:
        return jsonify({"error": "HTTPS required"}), 403


@app.after_request
def after_request(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.route('/api/query', methods=['POST'])
@require_api_key
def query_endpoint():
    return process_query()


@app.route('/api/embed', methods=['POST'])
@require_api_key
def embed_endpoint():
    return process_embedding()


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


if __name__ == '__main__':
    app.run(
        host=os.getenv('WEB_HOST', '0.0.0.0'),
        port=int(os.getenv('WEB_PORT', '5001')),
        debug=os.getenv('WEB_DEBUG', 'False').lower() == 'true'
    )

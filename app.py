from flask import Flask, jsonify, request
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from pythonjsonlogger import jsonlogger
import logging
import uuid
import os  
from datetime import datetime

# Configuration constants
APP_NAME = os.getenv('APP_NAME', 'DevOps Project API')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
API_VERSION = 'v1'

# Configuration du logging structuré
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s'
)
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

# Initialisation Flask
app = Flask(__name__)
CORS(app)

# Métriques Prometheus
metrics = PrometheusMetrics(app, group_by='path')

# Base de données en mémoire (simple liste)
items_db = [
    {"id": 1, "name": "Item 1", "description": "First item", "created_at": datetime.now().isoformat()},
    {"id": 2, "name": "Item 2", "description": "Second item", "created_at": datetime.now().isoformat()}
]
next_id = 3

# Middleware pour ajouter request_id à chaque requête
@app.before_request
def before_request():
    request.request_id = str(uuid.uuid4())
    logger.info(f"Incoming request", extra={
        'request_id': request.request_id,
        'method': request.method,
        'path': request.path
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to verify API availability.
    
    Returns:
        tuple: JSON response with status and timestamp, HTTP 200
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": APP_NAME,
        "version": API_VERSION
    }), 200

# GET all items
@app.route('/api/items', methods=['GET'])
def get_items():
    """
    Retrieve all items from the database.
    
    Returns:
        tuple: JSON response with items list and count, HTTP 200
    """
    logger.info("Fetching all items", extra={'request_id': request.request_id})
    return jsonify({
        "items": items_db,
        "count": len(items_db)
    }), 200

# GET item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id: int):
    """
    Retrieve a specific item by ID.
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        tuple: JSON response with item data or error, HTTP 200 or 404
    """
    logger.info(f"Fetching item {item_id}", extra={'request_id': request.request_id})
    
    item = next((item for item in items_db if item["id"] == item_id), None)
    
    if item is None:
        logger.warning(f"Item {item_id} not found", extra={'request_id': request.request_id})
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item), 200

# POST create new item
@app.route('/api/items', methods=['POST'])
def create_item():
    global next_id
    
    data = request.get_json()
    
    if not data or 'name' not in data:
        logger.error("Invalid request data", extra={'request_id': request.request_id})
        return jsonify({"error": "Name is required"}), 400
    
    new_item = {
        "id": next_id,
        "name": data['name'],
        "description": data.get('description', ''),
        "created_at": datetime.now().isoformat()
    }
    
    items_db.append(new_item)
    next_id += 1
    
    logger.info(f"Created item {new_item['id']}", extra={
        'request_id': request.request_id,
        'item_id': new_item['id']
    })
    
    return jsonify(new_item), 201

# DELETE item by ID
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items_db
    
    logger.info(f"Deleting item {item_id}", extra={'request_id': request.request_id})
    
    item = next((item for item in items_db if item["id"] == item_id), None)
    
    if item is None:
        logger.warning(f"Item {item_id} not found for deletion", extra={'request_id': request.request_id})
        return jsonify({"error": "Item not found"}), 404
    
    items_db = [item for item in items_db if item["id"] != item_id]
    
    logger.info(f"Deleted item {item_id}", extra={'request_id': request.request_id})
    
    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error("Internal server error", extra={'request_id': getattr(request, 'request_id', 'unknown')})
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting DevOps API server on port {port} (debug={debug_mode})")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)  # nosec B104
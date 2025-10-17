from flask import jsonify, request
from google.cloud import firestore
from datetime import datetime
import functions_framework

# Initialize Firestore client
db = firestore.Client()

# Collection name
TASKS_COLLECTION = 'tasks'

# Helper function to get next task ID
def get_next_task_id():
    """Generate the next task ID by counting documents"""
    tasks_ref = db.collection(TASKS_COLLECTION)
    docs = tasks_ref.stream()
    count = sum(1 for _ in docs)
    return count + 1

# Helper function to convert Firestore document to dict
def task_to_dict(doc):
    """Convert Firestore document to dictionary"""
    task_data = doc.to_dict()
    task_data['id'] = doc.id
    return task_data

# 1. Create Task Function (HTTP Trigger)
@functions_framework.http
def create_task(request):
    """HTTP Cloud Function to create a new task"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        request_json = request.get_json(silent=True)
        
        if not request_json or 'title' not in request_json:
            return (jsonify({'error': 'Title is required'}), 400, headers)
        
        # Get next task ID
        task_id = get_next_task_id()
        
        # Create task object
        task = {
            'id': task_id,
            'title': request_json['title'],
            'description': request_json.get('description', ''),
            'completed': False,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Save to Firestore using task_id as document ID
        db.collection(TASKS_COLLECTION).document(str(task_id)).set(task)
        
        return (jsonify({
            'message': 'Task created successfully',
            'task': task
        }), 201, headers)
        
    except Exception as e:
        return (jsonify({'error': str(e)}), 500, headers)

# 2. Get All Tasks Function (HTTP Trigger)
@functions_framework.http
def get_tasks(request):
    """HTTP Cloud Function to retrieve all tasks"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        # Get all tasks from Firestore
        tasks_ref = db.collection(TASKS_COLLECTION)
        docs = tasks_ref.order_by('id').stream()
        
        tasks = [task_to_dict(doc) for doc in docs]
        
        return (jsonify({
            'count': len(tasks),
            'tasks': tasks
        }), 200, headers)
        
    except Exception as e:
        return (jsonify({'error': str(e)}), 500, headers)

# 3. Delete Task Function (HTTP Trigger)
@functions_framework.http
def delete_task(request):
    """HTTP Cloud Function to delete a task"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'DELETE',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        task_id = request.args.get('id')
        
        if not task_id:
            return (jsonify({'error': 'Task ID is required'}), 400, headers)
        
        # Check if task exists
        task_ref = db.collection(TASKS_COLLECTION).document(str(task_id))
        task = task_ref.get()
        
        if not task.exists:
            return (jsonify({'error': 'Task not found'}), 404, headers)
        
        # Delete the task
        task_ref.delete()
        
        return (jsonify({
            'message': f'Task {task_id} deleted successfully'
        }), 200, headers)
        
    except Exception as e:
        return (jsonify({'error': str(e)}), 500, headers)

# 4. Get Task Statistics Function (HTTP Trigger) - Bonus
@functions_framework.http
def get_task_stats(request):
    """HTTP Cloud Function to get task statistics"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        # Get all tasks from Firestore
        tasks_ref = db.collection(TASKS_COLLECTION)
        docs = list(tasks_ref.stream())
        
        total_tasks = len(docs)
        completed_tasks = sum(1 for doc in docs if doc.to_dict().get('completed', False))
        pending_tasks = total_tasks - completed_tasks
        
        # Simulated metrics
        stats = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'total_api_calls_today': 156,
            'average_response_time_ms': 145,
            'success_rate_percent': 99.8,
            'active_functions': 4,
            'report_generated_at': datetime.utcnow().isoformat()
        }
        
        return (jsonify({
            'message': 'Task statistics retrieved successfully',
            'simulated_metrics': stats
        }), 200, headers)
        
    except Exception as e:
        return (jsonify({'error': str(e)}), 500, headers)
import functions_framework
from flask import jsonify
from datetime import datetime
import random

@functions_framework.http
def get_task_stats(request):
    """
    Get task statistics and system info.
    This is a bonus function that provides analytics (different from basic CRUD).
    """
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {'Access-Control-Allow-Origin': '*'}
    
    if request.method != 'GET':
        return (jsonify({'error': 'Method not allowed'}), 405, headers)
    
    # Generate statistics (simulated for demonstration)
    stats = {
        'report_generated_at': datetime.utcnow().isoformat(),
        'system_info': {
            'function_name': 'get-task-stats',
            'region': 'europe-west1',
            'runtime': 'python313',
            'type': 'HTTP-triggered Cloud Function'
        },
        'simulated_metrics': {
            'total_api_calls_today': random.randint(10, 100),
            'average_response_time_ms': round(random.uniform(50, 200), 2),
            'success_rate_percent': round(random.uniform(95, 99.9), 2),
            'active_functions': 4
        },
        'message': 'This bonus function demonstrates analytics capabilities beyond basic CRUD operations'
    }
    
    return (jsonify(stats), 200, headers)
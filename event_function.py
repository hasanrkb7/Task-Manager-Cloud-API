import functions_framework
from datetime import datetime
import json

@functions_framework.cloud_event
def log_task_activity(cloud_event):
    """
    This function is triggered by Cloud Storage events.
    It logs activity whenever a file is uploaded to the bucket.
    This demonstrates an event-driven cloud function (not API-triggered).
    """
    
    # Get event data
    data = cloud_event.data
    
    # Extract information
    bucket_name = data.get("bucket", "unknown")
    file_name = data.get("name", "unknown")
    
    # Create log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": cloud_event.get("type", "unknown"),
        "bucket": bucket_name,
        "file": file_name,
        "message": f"Storage event detected: file '{file_name}' in bucket '{bucket_name}'"
    }
    
    # Print to Cloud Logging
    print(f"EVENT LOG: {json.dumps(log_entry)}")
    
    # Return success (but this won't be sent anywhere for event functions)
    return "OK"
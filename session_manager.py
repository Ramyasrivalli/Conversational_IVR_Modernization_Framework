sessions = {}

def create_session(session_id, caller_id):
    sessions[session_id] = {
        "caller_id": caller_id,
        "history": [],
        "context": {}
    }

def get_session(session_id):
    return sessions.get(session_id)

def delete_session(session_id):
    if session_id in sessions:
        del sessions[session_id]
def format_pnr_response(data):
    if not data:
        return "PNR not found."
    return f"Your ticket is {data['status']}. Coach {data['coach']}, Seat {data['seat']}."

def format_train_response(data):
    if not data:
        return "Train not found."
    return f"Train {data['name']} runs from {data['from']} to {data['to']}."
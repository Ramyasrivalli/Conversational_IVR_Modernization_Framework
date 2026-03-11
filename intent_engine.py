import re

def detect_intent(message):
    message = message.lower()

    if "pnr" in message:
        return "PNR_STATUS"

    if "train" in message:
        return "TRAIN_SCHEDULE"

    if "book" in message:
        return "BOOK_TICKET"

    if "cancel" in message:
        return "CANCEL_TICKET"

    return "FALLBACK"


def extract_entities(intent, message):
    if intent == "PNR_STATUS":
        match = re.search(r"\d{10}", message)
        return {"pnr": match.group() if match else None}

    if intent == "TRAIN_SCHEDULE":
        match = re.search(r"\d{5}", message)
        return {"train_number": match.group() if match else None}

    return {}
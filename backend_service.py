pnr_database = {
    "1234567890": {
        "status": "Confirmed",
        "train": "12627 Karnataka Express",
        "seat": "B2-45"
    },
    "9876543210": {
        "status": "Waiting List 3",
        "train": "12002 Shatabdi Express",
        "seat": None
    }
}

train_database = {
    "12627": {
        "name": "Karnataka Express",
        "departure": "18:00",
        "platform": "3"
    },
    "12002": {
        "name": "Shatabdi Express",
        "departure": "06:00",
        "platform": "1"
    }
}


def get_pnr_status(pnr):
    return pnr_database.get(pnr, {
        "status": "PNR not found",
        "train": None,
        "seat": None
    })


def get_train_schedule(train_number):
    return train_database.get(train_number, {
        "name": None,
        "departure": None,
        "platform": None
    })
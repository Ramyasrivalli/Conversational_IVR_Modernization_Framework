from fastapi import FastAPI, Request
from fastapi.responses import Response
from backend_service import pnr_database, train_database

app = FastAPI()


def speak_time(time_str):
    hour, minute = map(int, time_str.split(":"))
    period = "AM"
    if hour >= 12:
        period = "PM"
    hour = hour % 12
    if hour == 0:
        hour = 12
    if minute == 0:
        return f"{hour} {period}"
    return f"{hour} {minute} {period}"


def speak_seat(seat):
    if seat is None:
        return "Seat not assigned"
    seat = seat.replace("-", " ")
    return " ".join(list(seat))


def menu():
    return """
    <Gather input="speech" timeout="5" speechTimeout="auto"
    language="en-IN" action="/twilio-webhook" method="POST">
        <Say>
        You may say check PNR, train schedule,
        book ticket, cancel ticket, or end call.
        </Say>
    </Gather>
    """


@app.post("/twilio-webhook")
async def twilio_webhook(request: Request):

    form = await request.form()
    speech = form.get("SpeechResult")
    digits = form.get("Digits")

    if not speech and not digits:
        twiml = f"""
        <Response>
            <Say>Welcome to IRCTC IVR.</Say>
            {menu()}
        </Response>
        """
        return Response(content=twiml, media_type="application/xml")


    if speech:
        speech = speech.lower()

        if "end" in speech or "exit" in speech or "bye" in speech:
            twiml = """
            <Response>
                <Say>Thank you for calling IRCTC. Goodbye.</Say>
                <Hangup/>
            </Response>
            """
            return Response(content=twiml, media_type="application/xml")


        if "pnr" in speech:
            twiml = """
            <Response>
                <Gather input="dtmf" numDigits="10"
                timeout="10" action="/twilio-webhook" method="POST">
                    <Say>Please enter your ten digit PNR number.</Say>
                </Gather>
            </Response>
            """
            return Response(content=twiml, media_type="application/xml")


        if "train" in speech:
            twiml = """
            <Response>
                <Gather input="dtmf" numDigits="5"
                timeout="10" action="/twilio-webhook" method="POST">
                    <Say>Please enter your five digit train number.</Say>
                </Gather>
            </Response>
            """
            return Response(content=twiml, media_type="application/xml")


        if "book" in speech:
            twiml = f"""
            <Response>
                <Say>
                Ticket booking is available on the IRCTC website
                or mobile application.
                </Say>
                {menu()}
            </Response>
            """
            return Response(content=twiml, media_type="application/xml")


        if "cancel" in speech:
            twiml = f"""
            <Response>
                <Say>
                Your ticket cancellation request has been initiated.
                </Say>
                {menu()}
            </Response>
            """
            return Response(content=twiml, media_type="application/xml")


        twiml = f"""
        <Response>
            <Say>Sorry, I did not understand.</Say>
            {menu()}
        </Response>
        """
        return Response(content=twiml, media_type="application/xml")


    if digits:

        if len(digits) == 10:

            if digits in pnr_database:

                data = pnr_database[digits]
                seat_text = speak_seat(data["seat"])

                train_parts = data["train"].split(" ", 1)
                train_number = train_parts[0]
                train_name = train_parts[1] if len(train_parts) > 1 else ""

                twiml = f"""
                <Response>
                    <Say>
                    PNR number
                    <say-as interpret-as="digits">{digits}</say-as>
                    is {data["status"]}.
                    Train number
                    <say-as interpret-as="digits">{train_number}</say-as>
                    {train_name}.
                    Seat {seat_text}.
                    </Say>
                    {menu()}
                </Response>
                """

            else:

                twiml = f"""
                <Response>
                    <Say>
                    PNR number
                    <say-as interpret-as="digits">{digits}</say-as>
                    was not found.
                    </Say>
                    {menu()}
                </Response>
                """

            return Response(content=twiml, media_type="application/xml")


        if len(digits) == 5:

            if digits in train_database:

                train = train_database[digits]
                time_text = speak_time(train["departure"])

                twiml = f"""
                <Response>
                    <Say>
                    Train number
                    <say-as interpret-as="digits">{digits}</say-as>
                    is {train["name"]}.
                    Departure time {time_text}.
                    Platform number
                    <say-as interpret-as="digits">{train["platform"]}</say-as>.
                    </Say>
                    {menu()}
                </Response>
                """

            else:

                twiml = f"""
                <Response>
                    <Say>
                    Train number
                    <say-as interpret-as="digits">{digits}</say-as>
                    was not found.
                    </Say>
                    {menu()}
                </Response>
                """

            return Response(content=twiml, media_type="application/xml")
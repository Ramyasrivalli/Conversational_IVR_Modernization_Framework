import os
from twilio.rest import Client

print("Starting call script...")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

call = client.calls.create(
    url="https://sheldon-unpriggish-overfloridly.ngrok-free.dev/twilio-webhook",
    to="+919982486999",
    from_="+16184645514"
)

print("Call SID:", call.sid)
print("Call Status:", call.status)
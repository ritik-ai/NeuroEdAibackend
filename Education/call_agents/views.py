from django.shortcuts import render


# Create your views here.
client = vonage.Client(
    application_id="",
    private_key="",
)

response = client.voice.create_call({
    'to': [{'type': 'phone', 'number':""}],
    'from': {'type': 'phone', 'number': ""},
    'ncco': [{'action': 'talk', 'text': 'This is a text to speech call from Nexmo'}]
})

print(response)

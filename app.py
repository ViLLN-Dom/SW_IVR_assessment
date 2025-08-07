from flask import Flask, request, Response
from signalwire.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    gather = response.gather(timeout=10, num_digits=1, action='/gather', method='POST')
    gather.say("Thanks for calling Position Prospect Records. Press 1 to speak to support. Press 2 to speak to A&R. Press 3 to speak to our communication team.")
    response.redirect('/no-input')
    return Response(str(response), mimetype='text/xml')

@app.route("/gather", methods=['POST'])
def gather():
    digit = request.form.get('Digits')
    response = VoiceResponse()
    
    if digit == '1':
        response.say("Our support team members are currently assisting other clients. Please wait for the next available representative to answer your call.")
        response.enqueue('support')
        response.play('https://screenapp.io/TqSDFYG3vS.mp3')

    elif digit == '2':
        response.say("Our A&R team is currently unavailable. At the tone, please leave a message and our team will get back to your shortly.")
        response.record(max_length=15, action='/handle-recording', method='POST')

    elif digit == '3':
        response.say("The Communication team is currently unavailable. Please leave a message.")
        response.record(max_length=15, action='/handle-recording', method='POST')

    else: 
        response.say("Invalid input. Goodbye.")



    return Response(str(response), mimetype='text/xml')

@app.route("/handle-recording", methods=['POST'])
def handle_recording():
    recording_url = request.form.get('RecordingUrl')
    response = VoiceResponse()
    response.say("Thank you for your message. Goodbye.")
    print("Recording URL:", recording_url)
    return Response(str(response), mimetype='text/xml')

@app.route("/no-input", methods=['POST'])
def no_input():
    response = VoiceResponse()
    response.say("We didn't receive any input. Goodbye")
    return Response(str(response), mimetype= 'text/xml")

if __name__ == "__main__":
    app.run(port=5000)


    


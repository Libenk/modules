from flask import Flask, request, jsonify, send_file
import io

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:34998", "allow_headers": ["Content-Type"]}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:34998')
    return response
@app.route('/api/audio-to-text', methods=['POST'])
def audio_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400

    audio = request.files['audio']
    # Add your logic for converting audio to text here
    transcription = "Transcribed text from audio file."
    return jsonify({"text": transcription})

@app.route('/api/text-to-audio', methods=['POST'])
def text_to_audio():
    data = request.get_json()
    text = data.get('text', '')
    print(data)
    if not text:
        return jsonify({"error": "No text provided."}), 400

    # Add your logic for converting text to audio here
    # Simulating audio file creation
    mock_audio = io.BytesIO()
    mock_audio.write(b"Mock audio content based on text-to-audio conversion.")
    mock_audio.seek(0)

    return send_file(mock_audio, mimetype="audio/mpeg", as_attachment=True, download_name="output.mp3")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

from flask import Flask, request, send_file, jsonify
import tempfile
import subprocess
import os

app = Flask(__name__)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    # Expecting JSON with 'text' and optional 'voice_sample' (base64 or file upload in future)
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400

    text = data['text']
    voice_sample = data.get('voice_sample')  # Path to voice sample file, if any

    with tempfile.NamedTemporaryFile('w+', suffix='.txt', delete=False) as tf:
        tf.write(text)
        tf.flush()
        textfile_path = tf.name

    output_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    output_wav.close()
    output_path = output_wav.name

    cmd = ['python', 'generate_audio.py', textfile_path, '-o', output_path]
    if voice_sample:
        cmd.extend(['--voice_sample', voice_sample])

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Stream output to keep connection alive
        while proc.poll() is None:
            yield b' '  # Send whitespace to keep connection alive
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            return jsonify({'error': stderr.decode()}), 500
        return send_file(output_path, mimetype='audio/wav', as_attachment=True, download_name='output.wav')
    finally:
        os.remove(textfile_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

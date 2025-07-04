from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    textfile = data.get('textfile')
    voice_sample = data.get('voice_sample')
    output = data.get('output', 'output.wav')

    if not textfile or not os.path.exists(textfile):
        return jsonify({'error': 'textfile is required and must exist'}), 400

    cmd = ['python', 'generate_audio.py', textfile]
    if voice_sample:
        cmd += ['--voice_sample', voice_sample]
    if output:
        cmd += ['--output', output]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return jsonify({'message': f'Audio generated: {output}', 'stdout': result.stdout, 'stderr': result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to generate audio', 'stdout': e.stdout, 'stderr': e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

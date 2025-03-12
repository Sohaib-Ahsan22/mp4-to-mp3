from flask import Flask, request, render_template, send_file
import os
import uuid
import ffmpeg

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        
        filename = str(uuid.uuid4()) + ".mp4"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        output_filename = filename.replace(".mp4", ".mp3")
        output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)
        
        try:
            ffmpeg.input(filepath).output(output_filepath, format='mp3').run()
            return send_file(output_filepath, as_attachment=True)
        except Exception as e:
            return f"Conversion failed: {e}", 500
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

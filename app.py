import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

import ocr
import solver

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve_route():
    uploaded = request.files.get('image')
    if not uploaded or uploaded.filename == '':
        flash('No file uploaded')
        return redirect(url_for('index'))

    filename = secure_filename(uploaded.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded.save(path)

    try:
        text = ocr.image_to_text(path)
        if not text:
            raise ValueError('OCR could not read any text from the image.')
        problem_type, steps, plot_path = solver.solve(text)
    except Exception as exc:
        flash(str(exc))
        return redirect(url_for('index'))

    plot_url = url_for('static', filename=os.path.join('plots', os.path.basename(plot_path)))
    return render_template('result.html', ocr_text=text, steps=steps, plot_url=plot_url, problem_type=problem_type)


if __name__ == '__main__':
    app.run(debug=True)


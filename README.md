# CalcVision

CalcVision is a simple Flask web application that solves basic calculus problems from uploaded images. It works completely offline using Tesseract OCR and SymPy.

## Features
- Upload an image containing a calculus expression.
- Extract the math expression using Tesseract.
- Detect derivatives, integrals, and limits.
- Solve the problem with SymPy and show a few textual steps.
- Plot the original and resulting functions using Matplotlib.

## Usage
1. Install dependencies (requires Python 3):
   ```bash
   pip install flask sympy pytesseract pillow matplotlib numpy
   ```
   Ensure the `tesseract` command is installed on your system.
2. Run the application:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser, upload an image of a calculus problem, and view the result.

All processing happens locally; no internet connection is required.


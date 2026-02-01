# 📷 Image to LaTeX Converter (Streamlit App)

This project is a Streamlit-based Image to LaTeX Converter that allows users to upload an image containing mathematical expressions, select a specific region, apply image preprocessing, and extract the corresponding LaTeX code using the pix2tex (LatexOCR) model.

# Features

Upload images containing mathematical equations

Interactive snipping tool to select only the required equation

Robust image preprocessing pipeline for better OCR accuracy

Automatic conversion of equations into LaTeX code

Real-time preview of extracted LaTeX

# Image Processing Pipeline (Core Focus)

The accuracy of LaTeX extraction heavily depends on preprocessing. This project applies the following steps:

1. Image Upload & Conversion

Uploaded images are handled using PIL

Converted to OpenCV (NumPy array) format for processing

2. Region Selection (Snipping Tool)

Uses streamlit-drawable-canvas

User draws a rectangle to isolate the mathematical portion

Prevents unnecessary background noise from affecting OCR

3. Preprocessing Steps

The selected region undergoes:

Grayscale Conversion

cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Gaussian Blurring

Reduces noise and smooths edges

Otsu’s Binary Thresholding

Enhances contrast between symbols and background

Converts image to binary for improved OCR performance

4. Format Conversion

Processed image is converted back to PIL format

Required input format for the pix2tex model

# LaTeX Extraction

Uses pix2tex (LatexOCR) deep learning model

Takes the preprocessed image and outputs LaTeX code

Displays:

Raw LaTeX

Rendered equation using st.latex()

 # Technologies Used

Python

Streamlit

OpenCV

NumPy

Pillow (PIL)

pix2tex (LatexOCR)

streamlit-drawable-canvas

# Installation
git clone https://github.com/NishaAnwar/Image2LaTeXConvertor.git

pip install -r requirements.txt

# ▶️ Run the App
streamlit run app.py



⚠️ Notes

Clear images with good contrast give best results

Works best when only the equation is selected

Performance depends on image quality and preprocessing

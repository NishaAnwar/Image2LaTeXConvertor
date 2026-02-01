import cv2
import numpy as np
import streamlit as st
from PIL import Image
from pix2tex.cli import LatexOCR
from streamlit_drawable_canvas import st_canvas

####Fisrt of all we will set streamlit app page
st.set_page_config(page_title="Image to LaTeX Converter", layout="wide")


def pil_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_image):
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def extract_latex_with_pix2tex(image):
    try:
        model = LatexOCR()
        latex_code = model(image)
        return latex_code
    except Exception as e:
        st.error(f"Error using pix2tex: {str(e)}")
        return None

st.title("📷 Image to LaTeX Converter 🖋️")

st.markdown("""
    Welcome to the Image to LaTeX Converter! Upload an image containing mathematical equations, 
    and this app will extract and convert them to LaTeX code.
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

if uploaded_file is not None:
    st.success("File uploaded successfully.")
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Snipping tool to select the mathematical portion
    st.write("Draw a rectangle to snip the mathematical portion:")
    canvas_result = st_canvas(
        fill_color="rgba(200, 130, 0, 0.3)",
        stroke_width=2,
        stroke_color="blue",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="rect",
        key="canvas",
    )

    if canvas_result.json_data is not None:####information about the shapes drawn on the canvas

        rect = canvas_result.json_data["objects"]###Retrieves the list of objects drawn on the canvas.

        if rect:
            rect = rect[0]    ####Accesses the first rectangle object from the list of objects.
            x, y, w, h = rect['left'], rect['top'], rect['width'], rect['height'] ###Extracts the position (left, top) and size (width, height) of the rectangle


            image_cv = pil_to_cv2(image)
            cropped_image = image_cv[int(y):int(y + h), int(x):int(x + w)]
            ###Crops the selected area from the original image based on the rectangle coordinates.

            #st.write("Cropped Image:")
            #st.image(cropped_image, caption='Snipped Portion', use_column_width=True)


            preprocessed_image = preprocess_image(cropped_image)

            #st.write("Preprocessed Image:")
            #st.image(preprocessed_image, caption='Preprocessed Portion', use_column_width=True, channels="GRAY")

####changes the image format to PIL, which is needed for further processing with the pix2tex model.
            preprocessed_image_pil = cv2_to_pil(preprocessed_image)


            if isinstance(preprocessed_image_pil, Image.Image):
                # Extract LaTeX code using pix2tex
                st.write("Extracting LaTeX code with pix2tex...")
                with st.spinner("Processing..."):
                    latex_code_pix2tex = extract_latex_with_pix2tex(preprocessed_image_pil) ##preprocessed image

                if latex_code_pix2tex:
                    st.subheader("LaTeX code (pix2tex):")
                    st.code(latex_code_pix2tex)
                    st.latex(latex_code_pix2tex)
                else:
                    st.warning("No LaTeX code detected using pix2tex.")
            else:
                st.error("Error: The preprocessed image is not in the correct format for pix2tex.")
        else:
            st.warning("Please draw a rectangle to select the mathematical portion.")
else:
    st.info("Please upload an image to proceed.")

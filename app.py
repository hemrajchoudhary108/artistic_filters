import io 
import base64
import streamlit
import cv2
from filters import *
from PIL import Image

# Generating link to download image
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="{filename}">{text}</a>'
    return href



def main():
    # Set title.
    st.title("Artistic Image Filters")

    # Upload image.
    uploaded_file = st.file_uploader("Choose an image file:", type=["png", "jpg"])
    
    if uploaded_file is not None:
        # Read the image.
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        input_col, output_col = st.columns(2)
        with input_col:
            st.header("Input Image:")
            st.image(image, channels="BGR", use_container_width=True)

        # Apply filters.
        st.header("Filter Examples:")
        # Display a selection box for choosing the filter to apply.
        option = st.selectbox(
            "Select a filter:",
            (
                "None",
                "Black and White",
                "Sepia",
                "Vignette",
                "Sepia / Vintage",
                "Pencil Sketch",

            ),
        )

        # Flag for showing output image.
        output_flag = 1
        # Colorspace of output image.
        color = "BGR"

        
        
        if option == "None":
            output_flag = 0
        elif option == "Black and White":
            output = black_and_white(image)
            color = "GRAY"
        elif option == "Sepia":
            output = sepia(image)
        elif option == 'Vignette':
            level = st.slider("Vignette Level", 0, 5, 2)
            output = vignette(image, level)
        elif option == "Sepia / Vintage":
            level = st.slider("Vignette Level", 0, 5, 2)
            output = sepia(image)
            output = vignette(output, level)
        elif option == "Pencil Sketch":
            ksize = st.slider("Blur kernel size", 1, 11, 5, step=2)
            output = pencil_sketch(image, ksize)
            color = "GRAY"
        
        with output_col:
            if output_flag == 1:
                st.header("Output Image:")
                st.image(output, channels=color, use_container_width=True)
                if color == 'BGR':
                    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                output = Image.fromarray(output)

                # Generate download link.
                st.markdown(get_image_download_link(output, "output.jpg", "Download Output Image"), unsafe_allow_html=True)

    # Define columns for thumbnail images.
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption("Black and White")
        st.image("images/filter_bw.jpg")
    with col2:
        st.caption("Sepia / Vintage")
        st.image("images/filter_sepia.jpg")
    with col3:
        st.caption("Vignette Effect")
        st.image("images/filter_vignette.jpg")
    with col4:
        st.caption("Pencil Sketch")
        st.image("images/filter_pencil_sketch.jpg")
if __name__ == "__main__":
    main()
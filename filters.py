import cv2
import numpy as np
import streamlit as st

@st.cache_data
def black_and_white(image):
    black_and_white_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return black_and_white_image

@st.cache_data
def sepia(image):
    img = image.copy()

    # Converting the image from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Converting the image to float64
    img = np.array(img, dtype=np.float64)
    image_sepia = cv2.transform(img, np.matrix([[0.393, 0.769, 0.189],
                                                [0.349, 0.686, 0.168],
                                                [0.272, 0.534, 0.131]]))
    # Clipping the image pixel values
    image_sepia = np.clip(image_sepia, 0, 255)

    # Converting the image from float64 to uint8
    image_sepia = np.array(image_sepia, dtype=np.uint8)

    # Converting the image from RGB to BGR
    image_sepia = cv2.cvtColor(image_sepia, cv2.COLOR_RGB2BGR)

    return image_sepia


@st.cache_data
def vignette(image, level=2):
    height, width, _ = image.shape

    # Generating the vignete mask using cv2.getGaussianKernel

    kernel_x = cv2.getGaussianKernel(width, width/level)
    kernel_y = cv2.getGaussianKernel(height, height/level)

    # Generating kernel matrix of size (HxW)
    kernel = kernel_y * kernel_x.T
    
    # Normalizing the masks so the centered pixel remains the same but edge pixel are closer to 0
    mask = kernel / kernel.max()

    # Applying the mask to each channel in the input image
    image_copy = image.copy()
    for i in range(3):
        image_copy[:, :, i] = image_copy[:, :, i] * mask
    
    return image_copy


@st.cache_data
def pencil_sketch(image, ksize=11, sigma_s=80, sigma_r=0.1, shadow_factor=0.05):

    # Applying GaussianBlur to reduce the noise in the image and smoothen it
    img_blur = cv2.GaussianBlur(image, (ksize, ksize), 0, 0)

    # Applying the pencil sketch effect to the image
    img_sketch_bw, _ = cv2.pencilSketch(img_blur, sigma_s=sigma_s, sigma_r=sigma_r, shade_factor=shadow_factor)

    return img_sketch_bw

    


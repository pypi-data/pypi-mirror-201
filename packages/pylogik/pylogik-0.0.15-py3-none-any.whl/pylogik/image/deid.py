import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_filter
from PIL import Image
import pydicom.data
import os
from os import listdir
import glob 
import pandas as pd
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from ..easyocr import easyocr
from .functions import *

def deid_us(directory_path = "/path/to/directory", output_directory_path = "/path/to/directory", rename_files = False):
    """
    DeId -- process image data for text removal/extraction
    Parameters
    ----------
    directory_path : str
        string to input path directory
    rename_files : Bool (optional)
        rename files/folders for futher de-identification (default = False)
    output_directory_path : str 
        string to output path directory 
    Returns
        folders with deidentified jpegs and csvs for processing
    ----------
    """

    # Set the directory path containing the files to process
    directory_path = directory_path
    # Set the output directory path
    output_directory_path = output_directory_path
    # Set the log file name
    log_file_name = "processed_files.log"
    skipped_files_name = "skipped_files.log"
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory_path):
        os.makedirs(output_directory_path)
    # Set the log file path
    log_file_path = os.path.join(output_directory_path, log_file_name)
    skipped_file_path = os.path.join(output_directory_path, skipped_files_name)
    # Initialize the list of files processed
    processed_files = []
    # Check if the log file exists, and if it does, read in the processed files
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                processed_files.append(line.strip())

    # Loop through the directory tree and process each file
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            # Get the full file path
            file_path = os.path.join(dirpath, filename)

            # Check if the file has already been processed
            if file_path in processed_files:
                print(f"Skipping file: {file_path}")
                continue

            # Processing this file:
            print(f"Processing file: {file_path}")
            
            try:
                # read in the image depending on the kind of the image it is (png, jpeg, dicom) etc
                pixel_array = image_read_3d(filename, file_path)            
            
                # select frame for text extraction/masking
                image_2_extract = get_1_frame(pixel_array)
            
                #call in reader: 
                reader = easyocr.Reader(['en'], gpu=True)
                txt_results = reader.readtext(image_2_extract, detail=1, paragraph=False)
                
                # create mask from extracted text 
                df_text, mask_text = text_mask(txt_results, image_2_extract, filename)
    
                # apply mask to array
                img_stack = apply_2d_mask_to_array(mask_text, pixel_array)
                
                # compression mask 
                compress_mask, rowmin, rowmax, colmin, colmax = smart_geometry(img_stack)
                
                #apply compression mask:
                img_stack = apply_2d_mask_to_array(compress_mask, img_stack)
                
                #image crop 
                img_smaller = img_crop(img_stack, rowmin, rowmax, colmin, colmax)
    
                ## write files to new folder 
                write_2_output(filename, img_smaller, output_directory_path, df_text, rename=rename_files)
    
                # Add the file to the list of processed files
                processed_files.append(file_path)
                
                # Write the file path to the log file
                with open(log_file_path, "a") as log_file:
                     log_file.write(f"{file_path}\n")
                     
            except:
                with open(skipped_file_path, "a") as skipped_file:
                   skipped_file.write(f"{file_path}\n")
                   continue

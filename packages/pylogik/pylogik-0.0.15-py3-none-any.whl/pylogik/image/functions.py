import numpy as np
import pydicom
from PIL import Image
import cv2
from scipy.ndimage import gaussian_filter
from pathlib import Path
import cv2
import re
import random
import string
#import easyocr
import numpy as np
from skimage.color import rgb2gray
from skimage import morphology
from skimage import measure
from scipy.ndimage import gaussian_filter
from PIL import Image
import pydicom
import pydicom.data
import os
from os import listdir
import glob 
import math
import pandas as pd
from sympy import symbols, Eq, solve
from pydicom.pixel_data_handlers import convert_color_space

def mask_subset(processed, OG, k=True):
    """
    Returns True if mask1 is a subset of mask2 to a degree of 0.85, False otherwise
    """
    # calculate intersection
    intersection = np.sum(OG[processed==k])
    subset = intersection/(np.sum(OG))
    #print("subset is: ", subset)
    # Return True if the Jaccard similarity coefficient is at least 0.9, False otherwise
    return subset

def dice_score(mask1, mask2):
    intersection = np.logical_and(mask1, mask2)
    return 2.0 * np.sum(intersection) / (np.sum(mask1) + np.sum(mask2))

def rgb2gray(rgb):
    """
    convert an rgb 2 grayscale image
    """
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def apply_2d_mask_to_array(mask, array):
    """
    Applies a 2D mask to all frames of an array
    """
    if len(array.shape)==4:
        # Get the dimensions of the input array
        n_frames, n_rows, n_cols, num_channels = array.shape 
        # Create an output array with the same shape as the input array
        output = np.zeros_like(array)
        # Apply the mask to each frame of the input array and store the result in the output array
        #mask = np.tile(mask[np.newaxis, np.newaxis], (n_frames, 1, 1, num_channels))
        label3 = np.stack([mask, mask, mask], axis=2)
        for i in range(n_frames):
            output[i,:,:,:] = np.multiply(array[i,:,:,:], label3)
        # Return the output array
        return output
    elif len(array.shape)==3:
        # Get the dimensions of the input array
        n_frames, n_rows, n_cols = array.shape 
        # Create an output array with the same shape as the input array
        output = np.zeros_like(array)
        # Apply the mask to each frame of the input array and store the result in the output array
        for i in range(n_frames):
            output[i,:,:] = np.multiply(array[i,:,:], mask)
        # Return the output array
        return output
    elif len(array.shape)==2:
        # Get the dimensions of the input array
        n_rows, n_cols = array.shape 
        # Create an output array with the same shape as the input array
        output = np.zeros_like(array)
        # Apply the mask to 2d image
        output[i,:,:] = np.multiply(array[:,:], mask)
        # Return the output array
        return output
    else:
        pass

def image_read_3d(filename, file_path):
    """
    Reads in different image file types and returns the image to be processed 
    """
    # Check if the file is a DICOM
    if filename.endswith(".dcm"):
        # Read in the DICOM using pydicom
        dicom = pydicom.dcmread(file_path)
        # Extract the pixel array from the DICOM
        #pixel_array = dicom.pixel_array
        format = is_ybr_or_rgb(dicom)
        if format is not None:
            if format == 'YBR':
                rgb = convert_color_space(dicom.pixel_array, "YBR_FULL", "RGB", per_frame=True)
            elif format == 'RGB':
                rgb = dicom.pixel_array 
            else:
                pass
        else:
            rgb = dicom.pixel_array      
        return rgb
    # Check if the file is a JPEG or PNG
    elif filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Read in the image using Pillow
        image = Image.open(file_path)
        # Convert the image to a numpy array using opencv-python
        pixel_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return pixel_array        
    # File is not a supported format
    else:
        try:
            # Read in the DICOM using pydicom
            dicom = pydicom.dcmread(file_path)
            # Extract the pixel array from the DICOM
            #pixel_array = dicom.pixel_array
            format = is_ybr_or_rgb(dicom)
            if format is not None:
                if format == 'YBR':
                    rgb = convert_color_space(dicom.pixel_array, "YBR_FULL", "RGB", per_frame=True)
                elif format == 'RGB':
                    rgb = dicom.pixel_array 
                else:
                    pass
            else:
                rgb = dicom.pixel_array      
            return rgb
        except:
            print(f"Skipping unsupported file: {filename}")
        
def is_ybr_or_rgb(ds):
    photometric_interpretation = ds.get('PhotometricInterpretation', '')
    if photometric_interpretation.startswith('YBR'):
        return 'YBR'
    elif photometric_interpretation == 'RGB':
        return 'RGB'
    else:
        return None
        
        
def area_filter(mask, min_area=0, max_area=np.inf):
    # Perform connected component analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    # Initialize filtered mask
    filtered_mask = np.zeros_like(mask)

    # Loop over each component and its statistics
    for label, stat in enumerate(stats):
        # Ignore background component (label 0)
        if label == 0:
            continue

        # Check if component's area is within the desired range
        area = stat[cv2.CC_STAT_AREA]
        if area < min_area or area > max_area:
            continue

        # Add component to filtered mask
        component_mask = (labels == label).astype(np.uint8) * 255
        filtered_mask = cv2.bitwise_or(filtered_mask, component_mask)
    return filtered_mask

def compress_de_id(img_stack):
    """
    see how much futher we can get the image stack compressed
    """
    if len(img_stack.shape)==4:
        #img = img_stack[:,:,:,0] # red channel only 
        img  = img_stack
        img = np.max(img, axis=0)
        numrows = img.shape[0]
        img = rgb2gray(img)
        #guass_filt = gaussian_filter(img, sigma=0.25)
        thresh = 0
        binary = img > thresh
        diff_rows = 710 - numrows
        if diff_rows > 50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(12*adjust_ratio)
            dilation_kernel = round(2*adjust_ratio)
        elif diff_rows < -50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(12*adjust_ratio)
            dilation_kernel = round(2*adjust_ratio)
        else:
            erosion_kernel = 12
            dilation_kernel = 2
        # erosion
        kernel_e = morphology.disk(erosion_kernel)
        erosion = morphology.binary_erosion(binary, kernel_e)
        # dilation
        kernel_d = morphology.disk(dilation_kernel)
        bool_mask = morphology.binary_dilation(erosion, kernel_d)
        # Convert boolean mask to 0 to 255 grayscale image
        gray_img_mask = bool_mask.astype(np.uint8) * 255
        area_filt_mask = area_filter(gray_img_mask, min_area=1000)
        # Convert grayscale image to boolean mask
        bool_mask = area_filt_mask.astype(bool)
        rows, cols = np.where(bool_mask == True)
        rowmax, rowmin, colmax, colmin = rows.max(), rows.min(), cols.max(), cols.min()
        
        # return the mask for further compression and the min and max rows/columns 
        return bool_mask, rowmin, rowmax, colmin, colmax 
    elif len(img_stack.shape) == 3:
        img = np.max(img, axis=0)
        numrows = img.shape[0]
        guass_filt = gaussian_filter(img, sigma=1)
        thresh = 0
        binary = guass_filt > thresh
        diff_rows = 710 - numrows
        if diff_rows > 50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        elif diff_rows < -50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        else:
            erosion_kernel = 15
            dilation_kernel = 12
        # erosion
        kernel_e = morphology.disk(erosion_kernel)
        erosion = morphology.binary_erosion(binary, kernel_e)
        # dilation
        kernel_d = morphology.disk(dilation_kernel)
        compress_mask = morphology.binary_dilation(erosion, kernel_d)
        rows, cols = np.where(compress_mask == True)
        rowmax, rowmin, colmax, colmin = rows.max(), rows.min(), cols.max(), cols.min()
        return compress_mask, rowmin, rowmax, colmin, colmax 
    elif len(img_stack.shape) == 2:
        numrows = img.shape[0]
        guass_filt = gaussian_filter(img, sigma=1)
        thresh = 0
        binary = guass_filt > thresh
        diff_rows = 710 - numrows
        if diff_rows > 50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        elif diff_rows < -50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        else:
            erosion_kernel = 15
            dilation_kernel = 12
        # erosion
        kernel_e = morphology.disk(erosion_kernel)
        erosion = morphology.binary_erosion(binary, kernel_e)
        # dilation
        kernel_d = morphology.disk(dilation_kernel)
        compress_mask = morphology.binary_dilation(erosion, kernel_d)
        rows, cols = np.where(compress_mask == True)
        rowmax, rowmin, colmax, colmin = rows.max(), rows.min(), cols.max(), cols.min()
        return compress_mask, rowmin, rowmax, colmin, colmax
    else:
        return img_stack

def img_crop(img_stack, rowmin, rowmax, colmin, colmax):
    """
    crops image based on compression mask
    """
    if len(img_stack.shape)==4:
        img_smaller = img_stack[:, rowmin:rowmax+1, colmin:colmax+1,:]
        return img_smaller
    elif len(img_stack.shape)==3:  
        img_smaller = img_stack[:, rowmin:rowmax+1, colmin:colmax+1]
        return img_smaller
    elif len(img_stack.shape)==2:
        img_smaller = img_stack[rowmin:rowmax+1, colmin:colmax+1,:]
        return img_smaller
    else:
        pass  

def get_1_frame(array):
    """
    Selects a frame from which to built the text extraction from, returns image_2_extact  
    """
    # if image is a volume with multicolors
    # if array size is 4: 
    if len(array.shape)==4:
        array = array[:,:,:,0]
        if len(array.shape)==3:
            mid_volume = int(array.shape[0]/2)
            image_2_extract = array[mid_volume,:,:]
            return image_2_extract
    # if array size is 3: 
    elif len(array.shape) == 3:
        if array.shape[2] == 3:
            image_2_extract = rgb2gray(array)
            return image_2_extract
        else:
            mid_volume = int(array.shape[0]/2)
            image_2_extract = array[mid_volume,:,:]
            return image_2_extract
    elif len(array.shape) == 2:
        image_2_extract = array
        return image_2_extract
    else:
        print("Array shape does not conform to expected dimensions")

def sector_mask(shape, centre, radius, angle_range):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """
    x,y = np.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin,tmax = np.deg2rad(angle_range)
    # ensure stop angle > start angle
    if tmax < tmin:
        tmax += 2*np.pi
    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = np.arctan2(x-cx,y-cy) - tmin
    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)
    # circular mask
    circmask = r2 <= radius*radius
    # angular mask
    anglemask = theta <= (tmax-tmin)
    return circmask*anglemask

def midpoint(p1, p2):
    return (round((p1[0]+p2[0])/2), round((p1[1]+p2[1])/2))

def slope_calc(p1, p2):
    return (p2[1] - p1[1])/(p2[0] - p1[0])

def text_mask(txt_results, TwoDarray, filename):
    """
    Mask text in image
    """
    mask_text = np.ones(TwoDarray.shape)
    df = pd.DataFrame()
    top_left = []
    top_right = []
    bottom_left = []
    bottom_right = []
    text_extract = []
    probs = []
    for (bbox, text, prob) in txt_results:
        #Define bounding boxes
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        prob_round = round(prob,2)
        top_left.append(tl)
        top_right.append(tr)
        bottom_left.append(bl)
        bottom_right.append(br)
        text_extract.append(text)
        probs.append(prob_round)
        # replace with 0's where there is text for mask:
        mask_text[tl[1]:bl[1],tl[0]:tr[0]] = 0
    
    df = pd.DataFrame({'text': text_extract, 'filename':filename})
    #split filename for creating csv from extracted text 
    #tempTuple = os.path.splitext(filename)
    #filename_short = tempTuple[0]
    #save_name = filename_short + '_text_and_meta' + '.csv'
    #df.to_csv(save_name, index=False)
    #CWD = os.getcwd()
    return df, mask_text

def write_2_output(filename, img_stack, output_path, df_text, rename = False):
    """
    Write series of images to a folder 
    """
    if rename == False:
        #creating folder to store output
        folder_name = [x for x in map(str.strip, filename.split('.')) if x]
        if folder_name[-1] == 'dcm' or folder_name[-1] == 'jpeg' or folder_name[-1] == 'jpg' or folder_name[-1] == 'png':
            folder_name = "".join(folder_name[:-1])
        else:
            folder_name = ".".join(folder_name)
        # Parent Directory path
        parent_dir = output_path
        # Path
        path_temp = os.path.join(parent_dir, folder_name)
        # create the directory
        os.mkdir(path_temp)
        os.chdir(path_temp)
        # if the image is 4 dimensional (RBG and multiple frames)
        if len(img_stack.shape)==4:
            for frame in range(img_stack.shape[0]-1):
                single_frame = img_stack[frame,:,:,:]     
                # create a PIL Image object from the numpy array
                result = Image.fromarray(single_frame, mode='RGB')
                frame_save_name = folder_name + str(frame) + '.jpeg'
                # save the image as a JPEG file
                result.save(frame_save_name, format='JPEG')                
        # if the image is 3 dimensional (multiple frames)
        elif len(img_stack.shape)==3:
            for frame in range(img_stack.shape[0]-1):
                result = img_stack[frame,:,:]      
                frame_save_name = folder_name + str(frame) + '.jpeg'
                cv2.imwrite(frame_save_name, result)
        elif len(img_stack.shape)==2:
            frame_save_name = folder_name + '.jpeg'
            cv2.imwrite(frame_save_name, img_stack)
            
        else:
            pass
        text_file_name = folder_name + "_txt.csv"
        df_text.to_csv(text_file_name)
    else:
        # Define the length of the folder/file name
        length = 10
        # Define the characters to be used for the folder/file name
        characters = string.ascii_lowercase + string.digits
        # Generate a random folder/file name using the defined length and characters
        folder_name = ''.join(random.choice(characters) for i in range(length))
        # Parent Directory path
        parent_dir = output_path
        # Path
        path_temp = os.path.join(parent_dir, folder_name)
        # create the directory
        os.mkdir(path_temp)
        os.chdir(path_temp)
        # if the image is 4 dimensional (RBG and multiple frames)
        if len(img_stack.shape)==4:
            for frame in range(img_stack.shape[0]-1):
                single_frame = img_stack[frame,:,:,:]     
                # create a PIL Image object from the numpy array
                result = Image.fromarray(single_frame, mode='RGB')
                frame_save_name = folder_name + str(frame) + '.jpeg'
                # save the image as a JPEG file
                result.save(frame_save_name, format='JPEG')                
        # if the image is 3 dimensional (multiple frames)
        elif len(img_stack.shape)==3:
            for frame in range(img_stack.shape[0]-1):
                result = img_stack[frame,:,:]      
                frame_save_name = folder_name + str(frame) + '.jpeg'
                cv2.imwrite(frame_save_name, result)
        elif len(img_stack.shape)==2:
            frame_save_name = folder_name + '.jpeg'
            cv2.imwrite(frame_save_name, img_stack)
        
        else:
            pass
        text_file_name = folder_name + "_txt.csv"
        df_text.to_csv(text_file_name)
    
    
def find_arc(mask):
    """
    Find the arc or lack thereof (if square)
    """
    rows, cols = np.where(mask == True)
    y_max, y_min = rows.max(), rows.min()
    x_max, x_min = cols.max(), cols.min()
    left_pointy = np.argmax(mask[:,x_min])
    right_pointy = np.argmax(mask[:,x_max])
    center_pointx = np.argmax(mask[y_max,:])
    point_4_radius = [center_pointx, y_max]
    #print(left_pointy, right_pointy)

    # determine differences to check which points to use:
    if abs(left_pointy - right_pointy) > 20:
        max_2 = np.max([left_pointy, right_pointy])
        if max_2 == left_pointy:
            #print("left_pointy being used")
            # then b/w the two other points find a new third:
            new_x = round((center_pointx - x_min)/2)
            # find maximum value in that column/x value:
            new_y = np.argmax(mask[:,new_x])
            #set 3 points we will use:
            point1 = [x_min, left_pointy]
            point2 = [new_x, new_y]
            point3 = [center_pointx, y_max]
            is_symmetric = False
            most_lateral = [x_min, left_pointy]

        else:
            #print("right_pointy being used")
            new_x = round((x_max - center_pointx)/2)
            new_y = np.argmax(mask[:,new_x])
            #set 3 points we will use:
            point1 = [center_pointx, y_max]
            point2 = [new_x, new_y]
            point3 = [x_max, right_pointy]
            is_symmetric = False
            #most_lateral = [x_max, right_pointy]
    else:
        point1 = [x_min, left_pointy]
        point2 = [center_pointx, y_max]
        point3 = [x_max, right_pointy]
        is_symmetric = True

    # get the slopes and midpoints: 
    slope_line_1_2 = slope_calc(point1, point2)
    midpoint_line_1_2 = midpoint(point1, point2)
    slope_line_2_3 = slope_calc(point2, point3)
    midpoint_line_2_3 = midpoint(point2, point3)

    # negative reciprocal:
    slope_perp_12 = -(slope_line_1_2)**(-1)
    slope_perp_23 = -(slope_line_2_3)**(-1)

    # solve the system of equations: 
    x, y = symbols('x y')
    eq1 = Eq(-1*slope_perp_12*x + y, slope_perp_12*(-1*midpoint_line_1_2[0])+midpoint_line_1_2[1])
    eq2 = Eq(-1*slope_perp_23*x + y, slope_perp_23*(-1*midpoint_line_2_3[0])+midpoint_line_2_3[1])
    center = solve((eq1,eq2), (x, y))

    if y_min < round(center[y]):
        center[y] = y_min
        center[x] = np.where(mask[y_min,:] == True)[0][0]
    else:
        pass
    
    center_coords = (center[y], center[x])
    center_coords_slope = (center[x], center[y])

    #check for curvilinear/phased vs square probe:
    # will adjust as needed in here in future version

    # check if we need to reflect
    if is_symmetric == True:
        left_side_slope = slope_calc(center_coords_slope, point1)
        right_side_slope = slope_calc(center_coords_slope, point3)
        angle_roi = math.atan(abs((left_side_slope - right_side_slope)/(1+ left_side_slope*right_side_slope)))*180/math.pi
        angle_roi = round(angle_roi)
        finishing_arc = 180 - math.atan(abs((left_side_slope - 0)/(1+ left_side_slope*0)))*180/math.pi
        starting_arc1 = finishing_arc - angle_roi
        starting_arc2 = finishing_arc - (180 - angle_roi)
        
        # calculate radius 
        radius = round(math.sqrt((point_4_radius[0] - center[x])**2 + (point_4_radius[1] - center[y])**2))
    else:
        # split slides into 3 rois for calculating the slope         
        r_increment = round((cols.max() - center_coords_slope[0])/3)
        r_xsec1 = center_coords_slope[0] + r_increment
        r_xsec2 = center_coords_slope[0] + r_increment + r_increment
        
        l_increment = round((center_coords_slope[0] - cols.min())/3)
        l_xsec1 = cols.min() + l_increment
        l_xsec2 = cols.min() + l_increment + l_increment
        
        right_slopes = []
        left_slopes = []
        point1 = [x_min, left_pointy]
        point3 = [x_max, right_pointy]
        right_slopes.append(slope_calc(center_coords_slope, point3))
        left_slopes.append(slope_calc(center_coords_slope, point1))
        
        for x_point in [r_xsec1, r_xsec2]:
            rows, cols = np.where(mask[:,:x_point] == True)
            x_max = cols.max()
            right_pointy = np.argmax(mask[:,x_max])
            point = [x_max, right_pointy]
            right_slope = slope_calc(center_coords_slope, point)
            right_slopes.append(right_slope)
            
        for x_point in [l_xsec1, l_xsec2]:
            rows, cols = np.where(mask[:,x_point:] == True)
            x_min = x_point + cols.min() # on original array 
            # get min value for slope:
            left_pointy = np.where(mask[:,x_min] == True)[0].min()
            point = [x_min, left_pointy]
            left_slope = slope_calc(center_coords_slope, point)
            left_slopes.append(left_slope)
        
        left_side_slope = np.max(left_slopes)
        right_side_slope = np.min(right_slopes)
        
        angle_roi = math.atan(abs((left_side_slope - right_side_slope)/(1+ left_side_slope*right_side_slope)))*180/math.pi
        angle_roi = round(angle_roi)
        finishing_arc = 180 - math.atan(abs((left_side_slope - 0)/(1+ left_side_slope*0)))*180/math.pi
        starting_arc1 = finishing_arc - angle_roi
        starting_arc2 = finishing_arc - (180 - angle_roi)
        # calculate radius 
        radius = round(math.sqrt((point_4_radius[0] - center[x])**2 + (point_4_radius[1] - center[y])**2))
    
    #check for curvilinear vs phased:
    # is there space b/w the calculate center and the input mask?
    tip = round(np.argmin(mask[:,center[x]]))
    if (tip - center[y]) > 10:
        notch_radius = round(tip - center[y])
    else:
        notch_radius = 0
    # return components necessary to drawn sector
    return center_coords, radius, starting_arc1, starting_arc2, finishing_arc, notch_radius

def create_circular_mask(radius, center, array):
    """
    creates a circular mask
    """
    # Create a grid of coordinates
    x, y = np.meshgrid(np.arange(array.shape[1]), np.arange(array.shape[0]))
    # Calculate the distance of each point from the center
    dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    # Create the mask
    mask = dist <= radius
    return mask

def label_mask(mask):
    labels_mask = measure.label(mask)  
    regions = measure.regionprops(labels_mask)
    regions.sort(key=lambda x: x.area, reverse=True)
    if len(regions) > 1:
        for rg in regions[1:]:
            labels_mask[rg.coords[:,0], rg.coords[:,1]] = 0
    labels_mask[labels_mask!=0] = 1
    return labels_mask

def smart_geometry(img_stack):
    """
    contour matching for ultrasound
    """
    if len(img_stack.shape)==4:
        img = img_stack[:,:,:,0]
        img = np.max(img, axis=0)
        numrows = img.shape[0]
        guass_filt = gaussian_filter(img, sigma=1)
        thresh = 0
        binary = guass_filt > thresh
        
        diff_rows = 710 - numrows
        if diff_rows > 50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        elif diff_rows < -50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        else:
            erosion_kernel = 15
            dilation_kernel = 12
        # erosion
        kernel_e = morphology.disk(erosion_kernel)
        erosion = morphology.binary_erosion(binary, kernel_e)
        # label mask
        labeled_mask = label_mask(erosion)
        # dilation of labeled mask 
        kernel_d = morphology.disk(dilation_kernel)
        bool_mask = morphology.binary_dilation(labeled_mask, kernel_d)
        # return the mask for further compression and the min and max rows/column
        center_coords, radius, starting_arc1, starting_arc2, finishing_arc, notch_radius = find_arc(bool_mask)
        mask_final_v1 = sector_mask(img.shape, center_coords, radius, (starting_arc1, finishing_arc))
        mask_final_v2 = sector_mask(img.shape, center_coords, radius, (starting_arc2, finishing_arc))
        
        mask_dict = {'v1':dice_score(mask_final_v1, bool_mask), 'v2':dice_score(mask_final_v2, bool_mask)}
        max_key = max(mask_dict, key=mask_dict.get)
        
        if max_key == 'v1':
            mask_final = mask_final_v1
        elif max_key == 'v2':
            mask_final = mask_final_v2
        else: 
            mask_final = mask_final_v1
        
        if notch_radius != 0:
            notch_mask = create_circular_mask(radius = notch_radius, center=center_coords, array = img)
            mask_final = (mask_final == True) & (~notch_mask == True) 
        else:
            pass
        
        #check to see if subset approximates otherwise return the bool mask 
        if mask_subset(mask_final, bool_mask) >= 0.9:
            mask_final = mask_final
        else:
            mask_final = bool_mask
        
        rows, cols = np.where(mask_final == True)
        rowmax, rowmin, colmax, colmin = rows.max(), rows.min(), cols.max(), cols.min()
        
        return mask_final, rowmin, rowmax, colmin, colmax
    
    # if this is a 3D image
    elif len(img_stack.shape) == 3:
        img = np.max(img, axis=0)
        numrows = img.shape[0]
        guass_filt = gaussian_filter(img, sigma=1)
        thresh = 0
        binary = guass_filt > thresh
        diff_rows = 710 - numrows
        if diff_rows > 50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        elif diff_rows < -50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        else:
            erosion_kernel = 15
            dilation_kernel = 12
        # erosion
        kernel_e = morphology.disk(erosion_kernel)
        erosion = morphology.binary_erosion(binary, kernel_e)
        # dilation
        kernel_d = morphology.disk(dilation_kernel)
        bool_mask = morphology.binary_dilation(erosion, kernel_d)
        # return the mask for further compression and the min and max rows/columns

        center_coords, radius, starting_arc1, starting_arc2, finishing_arc, notch_radius = find_arc(bool_mask)
        mask_final_v1 = sector_mask(img.shape, center_coords, radius, (starting_arc1, finishing_arc))
        mask_final_v2 = sector_mask(img.shape, center_coords, radius, (starting_arc2, finishing_arc))
        
        mask_dict = {'v1':dice_score(mask_final_v1, bool_mask), 'v2':dice_score(mask_final_v2, bool_mask)}
        max_key = max(mask_dict, key=mask_dict.get)
        
        if max_key == 'v1':
            mask_final = mask_final_v1
        elif max_key == 'v2':
            mask_final = mask_final_v2
        else: 
            mask_final = mask_final_v1
        
        if notch_radius != 0:
            notch_mask = create_circular_mask(radius = notch_radius, center=center_coords, array = img)
            mask_final = (mask_final == True) & (~notch_mask == True) 
        else:
            pass
        
        #check to see if subset approximates otherwise return the bool mask 
        if mask_subset(mask_final, bool_mask) >= 0.9:
            mask_final = mask_final
        else:
            mask_final = bool_mask
        
        rows, cols = np.where(mask_final == True)
        rowmax, rowmin, colmax, colmin = rows.max(), rows.min(), cols.max(), cols.min()
        
        return mask_final, rowmin, rowmax, colmin, colmax
    
    # if this is a 2D image
    elif len(img_stack.shape) == 2:
        img = img_stack
        numrows = img.shape[0]
        guass_filt = gaussian_filter(img, sigma=1)
        thresh = 0
        binary = guass_filt > thresh
        diff_rows = 710 - numrows
        if diff_rows > 50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        elif diff_rows < -50:
            adjust_ratio = numrows/710 
            erosion_kernel = round(15*adjust_ratio)
            dilation_kernel = round(12*adjust_ratio)
        else:
            erosion_kernel = 15
            dilation_kernel = 12
        # erosion
        kernel_e = morphology.disk(erosion_kernel)
        erosion = morphology.binary_erosion(binary, kernel_e)
        # dilation
        kernel_d = morphology.disk(dilation_kernel)
        
        bool_mask = morphology.binary_dilation(erosion, kernel_d)
        # return the mask for further compression and the min and max rows/columns
        center_coords, radius, starting_arc1, starting_arc2, finishing_arc, notch_radius = find_arc(bool_mask)
        mask_final_v1 = sector_mask(img.shape, center_coords, radius, (starting_arc1, finishing_arc))
        mask_final_v2 = sector_mask(img.shape, center_coords, radius, (starting_arc2, finishing_arc))
        
        mask_dict = {'v1':dice_score(mask_final_v1, bool_mask), 'v2':dice_score(mask_final_v2, bool_mask)}
        max_key = max(mask_dict, key=mask_dict.get)
        
        if max_key == 'v1':
            mask_final = mask_final_v1
        elif max_key == 'v2':
            mask_final = mask_final_v2
        else: 
            mask_final = mask_final_v1
        
        if notch_radius != 0:
            notch_mask = create_circular_mask(radius = notch_radius, center=center_coords, array = img)
            mask_final = (mask_final == True) & (~notch_mask == True) 
        else:
            pass
        
        #check to see if subset approximates otherwise return the bool mask 
        if mask_subset(mask_final, bool_mask) >= 0.9:
            mask_final = mask_final
        else:
            mask_final = bool_mask
        
        rows, cols = np.where(mask_final == True)
        rowmax, rowmin, colmax, colmin = rows.max(), rows.min(), cols.max(), cols.min()
        
        return mask_final, rowmin, rowmax, colmin, colmax
        
    else:
        return img_stack
    


# /usr/bin/env python
import os
import glob
import SimpleITK as sitk
import numpy as np
from nifti_op import load_nifti, get_nifti_mask_bbox
from xeon_op import hardcore_process
from pandas_op import generate_dataframe
from basic_op import *


# calculate file size, return in MB
def get_file_size(file_path):
    """
    Args:
        file_path: file path
    Returns:
        file size
    """
    file_size = os.path.getsize(file_path) / 1024 / 1024
    if file_size > 1:
        return round(file_size)
    else:
        return round(file_size, 2)


def get_nifti_img_file_info(file_path):
    """
    Args:
        file_path: file path
    Returns:
        file size, file dimension, file spacing
    """
    patient_id = os.path.basename(file_path)[:-7]
    
    if "_0000" in patient_id:
        patient_id.replace("_0000", "")

    img_npy, img_origin, img_spacing, img_direction = load_nifti(
        file_path, load_info=True)
    if img_spacing[0] != img_spacing[1]:
        raise ValueError("Spacing is not equal in x and y direction")

    img_min, img_max = np.min(img_npy), np.max(img_npy)
    img_file_size = get_file_size(file_path)

    return patient_id, img_npy.shape[0],  round(img_spacing[2],2), \
        img_npy.shape[1], img_npy.shape[2], round(img_spacing[0],2), img_min, img_max, str(img_npy.dtype), str(img_file_size)+'MB'


def get_nifti_img_mask_info(files_path):
    """
    Args:
        file_path: file path
    Returns:
        file size, file dimension, file spacing
    """

    img_path, mask_path = files_path
    img_npy, img_origin, img_spacing, img_direction = load_nifti(
        img_path, load_info=True)
    mask_npy = load_nifti(mask_path, load_info=False)

    if img_npy.shape != mask_npy.shape:
        raise ValueError("Image and mask shape not match")
    if img_spacing[0] != img_spacing[1]:
        raise ValueError("Spacing is not equal in x and y direction")

    patient_id = os.path.basename(img_path)[:-7]
    
    if "_0000" in patient_id:
        patient_id = patient_id.replace("_0000", "")

    img_min, img_max = np.min(img_npy), np.max(img_npy)
    img_file_size = get_file_size(img_path)

    label_num = len(np.unique(mask_npy)) - 1
    foreground_ratio = (np.sum(mask_npy > 0) / np.prod(mask_npy.shape)) * 100
    foreground_coord = get_nifti_mask_bbox(mask_npy,
                                           return_mask=False,
                                           return_coord=True)
    bbox_z, bbox_h, bbox_w = foreground_coord[1] - foreground_coord[0], foreground_coord[3] - foreground_coord[2],\
                            foreground_coord[5] - foreground_coord[4]

    return patient_id, img_npy.shape[0],  round(img_spacing[2],2), img_npy.shape[1], \
        img_npy.shape[2], round(img_spacing[0],2), img_min, img_max, str(img_npy.dtype),\
        label_num, str(round(foreground_ratio,2))+"%", bbox_z, bbox_h, bbox_w, str(img_file_size)+'MB'


def get_nifti_dataset_info(img_list,
                           mask_list=None,
                           excel_path=None,
                           num_workers=8):
    """ get nifti dataset information

    Parameters
    ----------
    img_list : list
    mask_list : list, optional
    excel_path : str, optional
    num_workers : int, optional
    """

    if excel_path is None:
        excel_path = 'dataset_info.xlsx'

    if mask_list is not None:
        file_list = list(zip(img_list, mask_list))
        res = hardcore_process(get_nifti_img_mask_info,
                               file_list,
                               num_workers=8)
        generate_dataframe(res, column_name=['Patient_id', 'Z', 'Z_spacing', 'H', 'W', 'HW_spacing', 'Min',\
            'Max', 'Type', 'Label', 'Foreground_ratio','BBox_Z', 'BBox_H', 'BBox_W', 'Size'], save_excel=True,
                           excel_path=excel_path)

    else:
        res = hardcore_process(get_nifti_img_file_info,
                               img_list,
                               num_workers=num_workers)
        generate_dataframe(res,
                           column_name=[
                               'Patient_id', 'Z', 'Z_spacing', 'H', 'W',
                               'HW_spacing', 'Min', 'Max', 'Type', 'Size'
                           ],
                           save_excel=True,
                           excel_path=excel_path)


if __name__ == '__main__':

    _ = programStart()
    dataset_img_list = glob.glob(
        '/exports/lkeb-hpc/rgao/Workspace/Dataset/MS_CT_Prostate/LUMC_Prostate/imagesTr/*.nii.gz'
    )
    dataset_img_list.sort()
    dataset_mask_list = [
        i.replace("imagesTr", "labelsTr").replace("_0000", "")
        for i in dataset_img_list
    ]
    get_nifti_dataset_info(img_list=dataset_img_list,
                           mask_list=dataset_mask_list,
                           excel_path='LUMC_info.xlsx',
                           num_workers=8)
    programEnd(_, 'Testing')
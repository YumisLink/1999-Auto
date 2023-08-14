import os
from datetime import datetime
import glob
import shutil

from loguru import logger

img_num = -1
img_limit = 1000

def save_img_log(refresh_num=False):
    global img_num
    
    src_path = 'cache/screenshot.png'
    dst_dir = os.path.join('logs', 'imgs')
    dst_path = os.path.join(dst_dir, f'{datetime.now():%Y-%m-%d-%H-%M-%S}--{img_num}.png')
    if refresh_num or img_num < 0 or img_num % 100 == 99:
        img_num = len(glob.glob(os.path.join(dst_dir, '*.png')))
    
    if img_num >= img_limit:
        logger.warning(f"Image limit reached: {img_limit}")
        return False
    
    if not os.path.exists(src_path):
        logger.warning(f"Image not found: {src_path}")
        return False
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src_path, dst_path)
    img_num += 1
    logger.info(f"Image saved: {dst_path}, now {img_num} images in total")
    return True
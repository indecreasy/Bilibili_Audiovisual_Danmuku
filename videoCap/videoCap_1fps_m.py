import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

GALLERY_PATH = '/Volumes/SSD/Data/video/'

video_list = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot_6.csv')
bvid_list = video_list['bvid'].values.tolist()
cid_list = video_list['cid'].values.tolist()

def process_video(bvid):
    video_path = GALLERY_PATH + '{}/{}.mp4'.format(bvid, bvid)

    if not os.path.exists(video_path):
        return

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    data_list = []

    # 跳帧处理
    skip_frames = 5

    # 处理每一帧并记录亮度和对比度信息
    for i in range(0, total_frames, skip_frames):
        ret, frame = cap.read()

        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        brightness_mean = np.mean(frame)
        brightness_max = np.max(frame)
        brightness_min = np.min(frame)

        contrast = np.std(frame_gray)
        saturation_mean = np.mean(hsv[:, :, 1])

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture = np.mean(laplacian)

        b, g, r = cv2.split(frame)
        hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
        hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
        hist_b = hist_b / np.sum(hist_b)
        hist_g = hist_g / np.sum(hist_g)
        hist_r = hist_r / np.sum(hist_r)
        color_entropy = -np.sum(hist_b * np.log2(hist_b + 1e-7)) \
                        - np.sum(hist_g * np.log2(hist_g + 1e-7)) \
                        - np.sum(hist_r * np.log2(hist_r + 1e-7))

        data_list.append({
            'frame': i,
            'second': int(i // fps),
            'brightness_mean': brightness_mean,
            'brightness_max': brightness_max,
            'brightness_min': brightness_min,
            'saturation_mean': saturation_mean,
            'texture': texture,
            'contrast': contrast,
            'color_entropy': color_entropy
        })

    df = pd.DataFrame(data_list)
    df_grouped = df.groupby('second').mean().reset_index()
    df_grouped.to_csv(GALLERY_PATH + '{}/{}_1fps.csv'.format(bvid, bvid), index=False)

# 使用线程池
with ThreadPoolExecutor(max_workers=4) as executor:
    # 提交任务到线程池
    futures = [executor.submit(process_video, bvid) for bvid in tqdm(bvid_list)]

    # 等待所有任务完成
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        pass
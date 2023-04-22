import cv2
import numpy as np
from scipy.stats import entropy
import pandas as pd
from tqdm import tqdm
import os

'''
要分析MP4视频每一帧的画面平均亮度、最高亮度、最低亮度和对比度，可以使用Python中的OpenCV库。
在这个示例中，我们首先使用cv2.VideoCapture打开视频文件，并使用cv2.CAP_PROP_FPS和cv2.CAP_PROP_FRAME_COUNT获取帧速率和总帧数。
接下来，我们遍历每一帧，计算亮度和对比度，并将结果存储在Python列表中。
最后，我们使用pandas.DataFrame将数据列表转换为数据框，并使用pandas.DataFrame.to_csv将结果保存到CSV文件中。

颜色熵的计算：
首先使用cv2.cvtColor将颜色空间从BBGR转换为HSV，以便计算饱和度。
然后使用cv2.Laplacian函数计算图像的纹理，这里我们采用Laplacian滤波器来检测图像的高频部分。
最后，使用cv2.calcHist函数计算颜色直方图，并将结果用于计算颜色熵。

在每一帧处理完毕后，我们将其对应的信息添加到列表中，然后创建一个数据框并将结果保存到CSV文件中。

请注意，这里计算的饱和度、纹理和颜色熵是基于整个帧的，因此可能会受到图像中物体数量、颜色分布等因素的影响。
如果需要更精确的分析结果，可以尝试使用ROI(感兴趣区域)来排除一些干扰项，或者使用更复杂的计算方法。

如果要在上面的代码中引入ROI，可以使用cv2.rectangle函数来绘制矩形框，将矩形框内的区域作为ROI来进行分析。

'''

GALLERY_PATH = '/Volumes/SSD/Data/video/'
SUCCESS_CID_PATH = "/Volumes/SSD/Data/Danmuku/successful_cids.csv"

# 读取csv中的bvid、cid
video_list = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot_1.csv')
bvid_list = video_list['bvid'].values.tolist()
cid_list = video_list['cid'].values.tolist()


# def record_successful_cid(self, cid):
#     with open(SUCCESS_CID_PATH, "a") as f:
#         f.write(f"{cid}\n")
#
# def load_successful_cids():
#     successful_cids_filepath = SUCCESS_CID_PATH
#     if not os.path.exists(successful_cids_filepath):
#         with open(successful_cids_filepath, "w") as f:
#             f.write("cid\n")
#         return set()

for bvid in tqdm(bvid_list):

    # successful_cids = load_successful_cids()
    #
    # # 检查是否已经保存成功
    # if bvid in successful_cids:
    #     print(f"bvid {bvid} already saved, skipping...")
    #     continue

    video_path = GALLERY_PATH + '{}/{}.mp4'.format(bvid, bvid)

    if not os.path.exists(video_path):
        continue

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频帧速率和总帧数、宽度、高度
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 初始化数据列表
    frame_list = []
    brightness_mean_list = []
    brightness_max_list = []
    brightness_min_list = []
    saturation_mean_list = []
    contrast_list = []
    texture_list = []
    color_entropy_list = []

    # # 定义ROI的左上角和右下角坐标
    # x1, y1, x2, y2 = 100, 100, 300, 300

    # 跳帧处理
    skip_frames = 5

    # 处理每一帧并记录亮度和对比度信息
    for i in range(0, total_frames, skip_frames):
        # 读取一帧
        ret, frame = cap.read()

        if not ret:
            break

        # 灰度图像
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # # 绘制ROI框
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #
        # # 获取ROI内的区域
        # roi = frame[y1:y2, x1:x2]
        #
        # # 转换颜色空间为HSV
        # hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # 转换颜色空间为HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 计算平均亮度、最高亮度和最低亮度
        brightness_mean = np.mean(frame)
        brightness_max = np.max(frame)
        brightness_min = np.min(frame)

        # 计算对比度
        contrast = np.std(frame_gray)

        # 计算平均饱和度
        saturation_mean = np.mean(hsv[:, :, 1])

        # 计算图像纹理
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture = np.mean(laplacian)

        # 计算颜色熵
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

        # 将信息添加到列表中
        frame_list.append(i)
        brightness_mean_list.append(brightness_mean)
        brightness_max_list.append(brightness_max)
        brightness_min_list.append(brightness_min)
        saturation_mean_list.append(saturation_mean)
        texture_list.append(texture)
        contrast_list.append(contrast)
        color_entropy_list.append(color_entropy)

    # 创建数据框
    data = {'frame': frame_list,
            'second': [int(frame // fps) for frame in frame_list],
            'brightness_mean': brightness_mean_list,
            'brightness_max': brightness_max_list,
            'brightness_min': brightness_min_list,
            'saturation_mean': saturation_mean_list,
            'texture': texture_list,
            'contrast': contrast_list,
            'color_entropy': color_entropy_list}

    df = pd.DataFrame(data)

    # 对数据按每秒进行分组，并计算平均值
    df_grouped = df.groupby('second').mean().reset_index()

    # 将结果保存到CSV文件中
    df_grouped.to_csv(GALLERY_PATH + '{}/{}_1fps.csv'.format(bvid, bvid), index=False)
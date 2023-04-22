import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.interpolate import interp1d
from fastdtw import fastdtw
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

# 读取索引CSV文件，获取所有情感序列CSV文件的路径
index_csv = '/Volumes/SSD/Data/VideoinfoCntSelected.csv'
index_df = pd.read_csv(index_csv)
bvid_file_paths = index_df['bvid'].tolist()

# 定义移动平均窗口大小
window_size = 5

# 存储所有情感序列的平滑值
smoothed_data = []

for bvid in tqdm(bvid_file_paths):
    # 读取情感序列CSV文件
    csv_path = f'/Volumes/SSD/Data/Merge_selected/{bvid}_merged.csv'
    if not os.path.exists(csv_path):
        print(bvid+'skip')
        continue

    df = pd.read_csv(csv_path)

    # 计算移动平均值
    emotion_column = 'sentiment_count_product'  # 根据实际情况修改情感列名称
    df[f'{emotion_column}_moving_average'] = df[emotion_column].rolling(window=window_size).mean()

    # 存储平滑后的情感序列
    smoothed_data.append(df[f'{emotion_column}_moving_average'].dropna().values)

# 计算目标长度，例如，所有序列的平均长度
target_length = int(np.mean([len(series) for series in smoothed_data if len(series) > 0]))
print(target_length)

# 使用插值调整所有序列的长度
smoothed_data_resampled = []
for series in smoothed_data:
    if len(series) > 1:
        # 创建插值函数
        x = np.linspace(0, 1, len(series))
        f = interp1d(x, series, kind='linear')

        # 生成新的等间距x值
        x_new = np.linspace(0, 1, target_length)

        # 使用插值函数计算新的y值
        y_new = f(x_new)
    elif len(series) == 1:
        # 对于只有一个数据点的序列，重复该点以达到目标长度
        y_new = np.full(target_length, series[0])
    else:
        # 跳过空序列
        y_new = np.full(target_length, 0)

    # 存储调整后的序列
    smoothed_data_resampled.append(y_new)

# 将调整后的序列转换为NumPy数组
smoothed_data_resampled = np.array(smoothed_data_resampled)


# 数据标准化
scaler = StandardScaler()
smoothed_data_standardized = scaler.fit_transform(smoothed_data_resampled)

# 执行KMeans聚类
n_clusters = 50
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(smoothed_data_standardized)
labels = kmeans.labels_

# 计算每个聚类的平均序列
cluster_averages = []
for cluster_label in range(n_clusters):
    cluster_data = smoothed_data_resampled[labels == cluster_label]
    cluster_average = cluster_data.mean(axis=0)
    cluster_averages.append(cluster_average)

# 绘制每个聚类的原始和平滑序列，以及聚类的平均趋势折线
for cluster_label in range(n_clusters):
    plt.figure(figsize=(10, 6))
    cluster_data = smoothed_data_resampled[labels == cluster_label]

    for i, series in enumerate(cluster_data):
        # 绘制原始序列（透明度较低）
        plt.plot(smoothed_data_resampled[i], alpha=0.3, label=f"Series {i}")

    # 绘制平均趋势折线（粗细、颜色和透明度均有所不同）
    plt.plot(cluster_averages[cluster_label], linewidth=3, color="red", alpha=0.7, label="Average Trend")

    plt.title(f"Cluster {cluster_label + 1}")
    # plt.legend()
    plt.show()

# # 计算DTW距离矩阵
# n_series = smoothed_data_resampled.shape[0]
# distance_matrix = np.zeros((n_series, n_series))
#
# for i in range(n_series):
#     for j in range(i+1, n_series):
#         distance, _ = fastdtw(smoothed_data_resampled[i], smoothed_data_resampled[j])
#         distance_matrix[i, j] = distance
#         distance_matrix[j, i] = distance
#
# # 将距离矩阵转换为SciPy可以接受的格式
# condensed_distance_matrix = squareform(distance_matrix)
#
# # 使用层次聚类进行聚类
# linkage_matrix = linkage(condensed_distance_matrix, method='ward')
#
# # 选择合适的截断距离以确定聚类数量
# # 请注意，这个值可能需要根据您的数据和需求进行调整
# cluster_cutoff_distance = 25
# labels = fcluster(linkage_matrix, cluster_cutoff_distance, criterion='distance')
#
# # 绘制聚类结果（与之前的示例相似）
# n_clusters = len(np.unique(labels))
# cluster_averages = []
#
# for cluster_label in range(1, n_clusters + 1):
#     cluster_data = smoothed_data_resampled[labels == cluster_label]
#     cluster_average = cluster_data.mean(axis=0)
#     cluster_averages.append(cluster_average)
#
# for cluster_label in range(1, n_clusters + 1):
#     plt.figure(figsize=(10, 6))
#     cluster_data = smoothed_data_resampled[labels == cluster_label]
#
#     for i, series in enumerate(cluster_data):
#         plt.plot(series, alpha=0.3, label=f"Series {i}")
#
#     plt.plot(cluster_averages[cluster_label - 1], linewidth=3, color="red", alpha=0.7, label="Average Trend")
#     plt.title(f"Cluster {cluster_label}")
#     plt.legend()
#     plt.show()
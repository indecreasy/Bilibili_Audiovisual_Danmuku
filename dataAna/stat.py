import pandas as pd
import numpy as np
from scipy.stats import spearmanr

# 音调色度加权平均
def calculate_weighted_chroma(chroma_features):
    # 为每个音调分配权重
    weights = np.arange(1, 13)
    # print(weights)
    # print(chroma_features)

    # 将Chroma features乘以相应的权重
    weighted_chroma = chroma_features * weights[:, np.newaxis]

    # 计算每个时间窗口中加权Chroma features的和
    weighted_chroma_sum = np.sum(weighted_chroma, axis=0)

    return weighted_chroma_sum


# 读取CSV文件
data = pd.read_csv('/Volumes/SSD/Data/Merge_selected_rate.csv')

# chroma_list = ['chroma_0','chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11']
#
# data['weighted_chroma_sum'] = data.apply(lambda row: calculate_weighted_chroma([data[index] for index in chroma_list]), axis=1)
#
# print(data.head())

# 将datetime列的字符串转换为datetime对象
data['order_pubdate'] = pd.to_datetime(data['order_pubdate'])

# 创建新列'timestamp'，将datetime对象转换为Unix时间戳（整数）
data['pubdate'] = data['order_pubdate'].apply(lambda x: int(x.timestamp()))

data.to_csv('/Volumes/SSD/Data/Merge_selected_rate.csv')
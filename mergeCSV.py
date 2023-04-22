import pandas as pd
import os
from tqdm import  tqdm
import numpy as np

# 设定要合并的CSV文件所在的文件夹路径
csv_folder_path = '/Volumes/SSD/Data/Merge_selected'

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

    # print(weighted_chroma_sum)

    return weighted_chroma_sum

# 获取文件夹中所有CSV文件的文件名列表
csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]

# 创建一个空的DataFrame，用于存储合并后的数据
merged_df = pd.DataFrame()

# 遍历CSV文件列表，逐个读取并合并到merged_df中
for csv_file in tqdm(csv_files):
    file_path = os.path.join(csv_folder_path, csv_file)
    temp_df = pd.read_csv(file_path)
    chroma_list = ['chroma_0', 'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5',
                   'chroma_6', 'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11']

    # 从temp_df中提取chroma_list中的所有列
    chroma_features = temp_df[chroma_list].values.T

    # 计算加权平均值
    weighted_chroma_sum = calculate_weighted_chroma(chroma_features)

    # 将加权平均值添加到temp_df中
    temp_df['weighted_chroma_sum'] = weighted_chroma_sum

    # 将temp_df合并到merged_df中
    merged_df = pd.concat([merged_df, temp_df], ignore_index=True)


# 将合并后的DataFrame输出为一个新的CSV文件
merged_df.to_csv('/Volumes/SSD/Data/Merge_selected.csv', index=False)

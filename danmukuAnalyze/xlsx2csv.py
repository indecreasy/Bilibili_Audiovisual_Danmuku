import os
import pandas as pd
from tqdm import tqdm

# 设置文件夹路径
from_folder_path = '/Volumes/SSD/Data/data'
to_folder_path = '/Volumes/SSD/Data/Danmuku'

# 获取所有Xlsx文件的文件名
file_names = [f for f in os.listdir(from_folder_path) if f.endswith('.xlsx')]

# 循环遍历每个文件，并将其转换为csv格式
for file_name in tqdm(file_names):
    # 读取Xlsx文件
    df = pd.read_excel(os.path.join(from_folder_path, file_name))

    # 将文件名中的xlsx替换成csv，作为新文件名
    csv_file_name = file_name.replace('.xlsx', '.csv')

    # 保存为csv文件
    df.to_csv(os.path.join(to_folder_path, csv_file_name), index=False)

    # print(f'{file_name} 转换为 {csv_file_name} 完成')

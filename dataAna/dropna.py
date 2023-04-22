import pandas as pd

# 读取数据
data = pd.read_csv('/Volumes/SSD/Data/Merge_selected.csv')
print(len(data))
#删除空值行
data.dropna(subset=['sentiment_count_product'], inplace=True)
data.dropna(subset=['frame'], inplace=True)
data.dropna(subset=['loudness'], inplace=True)

# 创建一个空列表来存储"BVID"列有NaN值的行的值
# missing_loudness_bvids = []
print(data.isna().sum())
# # 遍历每一行
# for index, row in data.iterrows():
#     # 检查该行的"loudness"列是否有NaN值
#     if pd.isna(row['frame']):
#         # 如果有NaN值，将该行的"BVID"值添加到列表中
#         missing_loudness_bvids.append(row['bvid'])

data.to_csv('/Volumes/SSD/Data/Merge_selected_dropna.csv')
# data.isna().sum().to_csv('3.csv')
print(len(data))


# # 使用set()函数对列表进行去重
# my_set = set(missing_loudness_bvids)
#
# # 将集合转换回列表
# missing_loudness_bvids = list(my_set)
# print(missing_loudness_bvids)
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime

# 读取原始CSV文件
input_csv = '/Volumes/SSD/Data/getVideoinfo_byhot.csv'  # 更改为您的输入CSV文件名
data = pd.read_csv(input_csv)
data['datetime'] = data['order_pubdate'].apply(
    lambda str: datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S"))


# 筛选出2023年1月1日之后的数据
data_filtered = data[data['datetime'] > '2023-01-01']

# 降序排列
sorted_data_2023 = data_filtered.sort_values(by='datetime', ascending=False)
sorted_data = data.sort_values(by='datetime', ascending=False)

# 重置索引
sorted_data_2023 = sorted_data_2023.reset_index(drop=True)
sorted_data = sorted_data.reset_index(drop=True)

print(sorted_data_2023)

mpl.use('TkAgg')  # !IMPORTANT
plt.rcParams['font.sans-serif'] = ['KaiTi_GB2312']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
sorted_data_2023.hist(xlabelsize=10, ylabelsize=10, figsize=(12, 12))
plt.show()

sorted_data_2023.to_csv("/Volumes/SSD/Data/getVideoinfo_byhot_2023.csv", index=False)


# 分割数据
num_files = 6
rows_per_file = 1000
splits = []

for i in range(num_files):
    start = i * rows_per_file
    end = start + rows_per_file
    splits.append(sorted_data[start:end])


# 对分割后的每一部分画图
# 分析6000条
mpl.use('TkAgg')  # !IMPORTANT
plt.rcParams['font.sans-serif'] = ['KaiTi_GB2312']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）

for idx, split_data in enumerate(splits):  # 修改为 idx, split_data
    # 删除多余的 pd.DataFrame(split_data) 行
    split_data.hist(xlabelsize=10, ylabelsize=10, figsize=(12, 12))
    plt.suptitle(f"Split {idx + 1}")  # 添加子图标题
    plt.show()


# 将每个分割后的部分保存为单独的CSV文件
output_filename_template = "/Volumes/SSD/Data/getVideoinfo_byhot_{}.csv"  # 更改为您喜欢的输出文件名模板

for i, split_data in enumerate(splits):
    output_filename = output_filename_template.format(i + 1)
    split_data.to_csv(output_filename, index=False)

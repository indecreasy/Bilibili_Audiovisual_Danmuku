import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime

# 分析6000条
mpl.use('TkAgg')  # !IMPORTANT

info_df = pd.read_csv('/Volumes/SSD/Data/getVideoinfo_byhot.csv')

# info_df['order_pubdate'] = info_df['order_pubdate'].apply(
#     lambda str: datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S"))

info_df['datetime'] = pd.to_datetime(info_df['order_pubdate'])

# ########去重

# # 去除'bvid'列中的重复值
# df_unique = info_df.drop_duplicates(subset='bvid', keep='first')
#
# # 输出去除重复值后的DataFrame
# print("\n去除'bvid'列重复值后的DataFrame：")
# print(df_unique)

# ########画图

plt.rcParams['font.sans-serif'] = ['KaiTi_GB2312']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）


'''
在这个示例中，我们首先使用pd.read_csv()函数读取CSV文件。然后，我们将'datetime'列转换为datetime类型。接着，我们使用plt.scatter()函数绘制散点图，横坐标为'datetime'列，纵坐标为'cid'列。我们还设置了横坐标轴的格式和标签的旋转角度，以便更好地显示日期和时间。

运行这段代码，你应该会看到一个显示'datetime'和'cid'关系的散点图。
'''
# 绘制散点图
fig, ax = plt.subplots()
ax.scatter(info_df['datetime'], info_df['cid'])

# 设置横坐标轴格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

# 设置横坐标轴标签的旋转角度
plt.xticks(rotation=45)

# 设置轴标签
plt.xlabel('Datetime')
plt.ylabel('CID')

# info_df.hist(xlabelsize=10, ylabelsize=10, figsize=(12, 12))
# info_df.hist(column='order_pubdate')

plt.show()

# # 视频图像特征
# mpl.use('TkAgg')  # !IMPORTANT
#
# df = pd.read_csv('/Volumes/SSD/Data_demo/Video/BV1r84y187sb/BV1r84y187sb_1fps.csv')
#
#
# plt.rcParams['font.sans-serif'] = ['KaiTi_GB2312']  # 步骤一（替换sans-serif字体）
# plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
#
# # 绘制折线图
# plt.plot(df['second'], df['brightness_mean'], label='brightness_mean')
# plt.plot(df['second'], df['saturation_mean'], label='saturation_mean')
#
# # 添加标题和轴标签
# plt.title('Line plot')
# plt.xlabel('second')
# plt.ylabel('Value')
#
# # 添加图例
# plt.legend()
#
# # 显示图形
# plt.show()


# # 视频声音特征
# mpl.use('TkAgg')  # !IMPORTANT
#
# df = pd.read_csv('/Volumes/SSD/Data_demo/Video/BV1r84y187sb/BV1r84y187sb_sound_1FPS.csv')
#
# plt.rcParams['font.sans-serif'] = ['KaiTi_GB2312']  # 步骤一（替换sans-serif字体）
# plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
#
# # 绘制折线图
# plt.plot(df['index'], df['loudness'], label='loudness')
# plt.plot(df['index'], df['spectral_centroid'], label='spectral_centroid')
#
# # 添加标题和轴标签
# plt.title('Line plot')
# plt.xlabel('second')
# plt.ylabel('Value')
#
# # 添加图例
# plt.legend()
#
# # 显示图形
# plt.show()

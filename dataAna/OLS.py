# 导入所需的库
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

# 读取数据
data = pd.read_csv('/Volumes/SSD/Data/Merge_selected_dropna.csv')

X_list = ['brightness_mean', 'saturation_mean', 'texture', 'contrast', 'color_entropy', 'loudness',
          'chroma_0', 'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5', 'chroma_6',
          'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11', 'mfcc_0', 'mfcc_1',
          'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10',
          'mfcc_11', 'mfcc_12', 'mfcc_13', 'mfcc_14', 'mfcc_15', 'mfcc_16', 'mfcc_17', 'mfcc_18',
          'mfcc_19', 'spectral_centroid', 'spectral_rolloff', 'zero_crossing_rate', 'duration',
          'view']

# 准备数据
X = data[X_list]  # 自变量
y = data['sentiment_count_product']  # 因变量

# 拆分数据集
test_size = 0.2
if len(X) * test_size < 1:
    test_size = 1 / len(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)

# 使用statsmodels进行线性回归
X_train_sm = sm.add_constant(X_train)  # 添加截距项
model = sm.OLS(y_train, X_train_sm)
results = model.fit()

# 创建包含变量名、t统计量和p值的表格
t_p_values = pd.DataFrame({'Variable': results.params.index, 't Value': results.tvalues, 'p Value': results.pvalues})

# 输出表格
print(t_p_values)
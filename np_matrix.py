import numpy as np

from sklearn.preprocessing import StandardScaler

import pandas as pd
dataset_df=pd.read_csv("matches_list_ranking_31000.csv")
print (dataset_df.shape[0],dataset_df.shape[1])
heroes_released=129
x_matrix = np.zeros((dataset_df.shape[0], 2 * heroes_released + 3))#创建新矩阵 长度 为8e6
print (len(x_matrix))
# for i in range(5):
#     for j in range(5):
#     	if i>j:
#     		print(i,j)
np.random.seed(123)#123当时用seed时候,假设这堆数据使用了n 那么我下次再使用n时 生成的是同一堆"随机数据"
data = [[np.random.randint(1, 10) for j in range(0, 3)] for i in range(1, 5)]
data=np.array(data)
mean = np.mean(data, axis=0)#均值 
std = np.std(data, axis=0)#方差
print((3+2+2+1)/10)
# print((3+2+2+1+5+5+4+8+9+4)/10)

print (mean,std)
# data = np.random.randint(10, 4)#生成10*4的随机矩阵,浮点数
print(data)
scaler = StandardScaler()
scaler.fit(data)
trans_data = scaler.transform(data)
print("-----")
print(trans_data)
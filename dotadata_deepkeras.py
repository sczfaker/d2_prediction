     
"""根据对局数据型训练1个预测模型
   可以对胜率进行预测
   LSTM 两个时间节点，第一个时间节点为天辉英雄的稀疏向量，第二个时间节点为夜魇英雄的稀疏向量
   英雄共117个，最后一个英雄为马尔斯(编号129)，"""

# TODO ====参数区==== TODO
predict_step = 1
team_num = 2   # 多少个月的数据作为训练集
cnn_output_dim = 64 # CNN层输出特征维度
kernel_size = 13
pool_size = 2       # 池化倍数 TODO 注意！！ 需要保证 cnn_output_dim ÷ pool_size 的结果是一个整数
hidden_size = 500  # 神经元数目
epochs = 2000      # 训练轮次
batch_size = 64  # 批处理大小
model_saved_path = ".\\model_keras\\"#/也可以   # 模型保存路径#
# model_name = '50000_samples_20191029_LSTM'
# model_name = '100000_samples_20191030_CNN+LSTM_kernel_13_batch_1000'
model_name = '2e6_samples_20200727_LSTM_mmr_0915.h5'#训练生成模型使用模型名
hero_id_max = 129   # 英雄id的最大值
# TODO ====参数区==== TODO

import os
# os.environ['THEANO_FLAGS'] = "device=gpu"  # 改变环境变量添加THEANO_FLAGS,在导入theano的时候可以设置使用gpu
import numpy as np
import math
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Embedding, Masking, Dropout, Conv1D, MaxPooling1D, Reshape
from keras.models import load_model
from json import load,dump,loads
import time
import datetime
import sys
#from keras.utils.visualize_plots import figures   # TODO：一个手动添加的模块，用来绘制误差值随着迭代次数的曲线，并保存图像
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib.dates as mdates       # 让坐标显示月份
import matplotlib as mpl 
mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签  
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号  
import pandas as pd
# import sys,io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')



# print (len(pd_match["radiant_win"]))
#print (len(pd_match.radiant_win))
#y_lable = pd_match.radiant_team#(pd_match.radiant_win==1.0).astype(np.int)

#print (len(y_label),len(x_label))
class DL_PICKS(object):
    """docstring for ClassName"""
    def __init__(self, arg1=None,arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.using_model_name="2e6_samples_20200727_LSTM_mmr_0915.h5"#预测使用模型名
        self.modle_path="./model_keras/"
    def make_samples(self,x_input,y_input):
        train_x = []
        train_y = []
        test_x = []
        test_y = []
        validate_x = []
        validate_y = []
        for i in range(len(x_input)):
            if i%10==8:
                test_x.append(x_input[i])
                test_y.append(y_input[i])
            elif i%10==9:
                validate_x.append(x_input[i])
                validate_y.append(y_input[i])
            else:
                train_x.append(x_input[i])
                train_y.append(y_input[i])
        return train_x,train_y,test_x,test_y,validate_x,validate_y
    def training(self):
        train_x,train_y,test_x,test_y,validate_x,validate_y = self.make_samples(self.arg1,self.arg2)
        tx = np.array(train_x).reshape(len(train_x),team_num,hero_id_max)
        ty = np.array(train_y).reshape(len(train_y),1)
        test_x = np.array(test_x).reshape(len(test_x),team_num,hero_id_max)
        test_y = np.array(test_y).reshape(len(test_y),1)
        validate_x = np.array(validate_x).reshape(len(validate_x),team_num,hero_id_max)
        validate_y = np.array(validate_y).reshape(len(validate_y),1)
         #TODO ==============样本制作 结束==================
        print('=========== tx.shape:',tx.shape,' ===============')
        print('=========== ty.shape:',ty.shape,' ===============')
        print('=========== test_x.shape:',test_x.shape,' ===============')
        print('=========== test_y.shape:',test_y.shape,' ===============')
        print('=========== validate_x.shape:',validate_x.shape,' ===============')
        print('=========== validate_y.shape:',validate_y.shape,' ===============')
        # TODO CNN + LSTM 模型  ---使用该模型时需注释掉另外两个模型
        # model = Sequential()
        # model.add(Conv1D(cnn_output_dim,kernel_size,padding='same',input_shape=(team_num,hero_id_max)))  #(none,team_num,9) 转换为 (none,team_num,32)
        # model.add(MaxPooling1D(pool_size=pool_size,data_format='channels_first'))  #(none,team_num,32)转换为 (none,team_num,16)
        # model.add(LSTM(hidden_size, input_shape=(team_num,(cnn_output_dim/pool_size)), return_sequences=False))  # 输入(none,team_num,129)  输出向量 (hidden_size,)
        # model.add(Dropout(0.2))
        # model.add(Dense(10))
        # model.add(Dropout(0.2))
        # model.add(Dense(1))              # 全连接到一个元素
        # model.add(Activation('sigmoid'))
        # model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])

        # TODO 纯LSTM 模型  ---使用该模型时需注释掉另外两个模型
        model = Sequential()
        model.add(LSTM(hidden_size, input_shape=(team_num,hero_id_max), return_sequences=False))  # 输入(none,team_num,129)  输出向量 (hidden_size,)
        model.add(Dropout(0.2))
        model.add(Dense(10))
        model.add(Dropout(0.2))
        model.add(Dense(1))              # 全连接到一个元素
        model.add(Activation('sigmoid'))
        model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])

        # TODO 纯CNN 模型  ---使用该模型时需注释掉另外两个模型
        # model = Sequential()
        # model.add(Conv1D(cnn_output_dim,kernel_size,padding='same',activation='relu',input_shape=(team_num,hero_id_max)))  #(none,team_num,129) 转换为 (none,team_num,32)
        # model.add(MaxPooling1D(pool_size=pool_size,data_format='channels_first'))  #(none,team_num,32)转换为 (none,team_num,16)
        # model.add(Reshape((int(team_num*cnn_output_dim/pool_size),), input_shape=(team_num,int(cnn_output_dim/pool_size))))
        # model.add(Dropout(0.2))
        # model.add(Dense((10),input_shape=(team_num,cnn_output_dim/pool_size)))
        # model.add(Dropout(0.2))
        # model.add(Dense(1))              # 全连接到一个元素
        # model.add(Activation('sigmoid'))
        # model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
        


        callbacks = [keras.callbacks.EarlyStopping(monitor='val_loss', patience=2, verbose=0, mode='min'),\
            keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=1, verbose=0, mode='min',\
                 epsilon=0.0001, cooldown=0, min_lr=0)]
        hist = model.fit(tx,ty,batch_size=batch_size,epochs=epochs,shuffle=True,\
            validation_data=(validate_x, validate_y),callbacks=callbacks)
        model.save(model_saved_path+model_name)
    def testing(self,tag_line):
        train_x,train_y,test_x,test_y,validate_x,validate_y = self.make_samples(self.arg1,self.arg2)
        tx = np.array(train_x).reshape(len(train_x),team_num,hero_id_max)
        ty = np.array(train_y).reshape(len(train_y),1)
        test_x = np.array(test_x).reshape(len(test_x),team_num,hero_id_max)
        test_y = np.array(test_y).reshape(len(test_y),1)
        validate_x = np.array(validate_x).reshape(len(validate_x),team_num,hero_id_max)
        validate_y = np.array(validate_y).reshape(len(validate_y),1)
        # tx = tx[40000:]
        # ty = ty[40000:]
        # test_x = test_x[5000:]
        # test_y = test_y[5000:]
        # validate_x = validate_x[5000:]
        # validate_y = validate_y[5000:]
         #TODO ==============样本制作 结束==================
        print('=========== tx.shape:',tx.shape,' ===============')
        print('=========== ty.shape:',ty.shape,' ===============')
        print('=========== test_x.shape:',test_x.shape,' ===============')
        print('=========== test_y.shape:',test_y.shape,' ===============')
        print('=========== validate_x.shape:',validate_x.shape,' ===============')
        print('=========== validate_y.shape:',validate_y.shape,' ===============')
        # TODO 开始加载模型
        keras.backend.clear_session()    # 计算图清空，防止越来越慢
        model = load_model(model_saved_path+model_name)
        out0 = model.predict(test_x)
        correct_num = 0
        for i in range(len(out0)):
            if out0[i][0]<0.5:
                temp_result = 0.0#预测天辉胜利值为0也就是天辉失败
            else:
                temp_result = 1.0
            if temp_result==test_y[i][0]:
                correct_num += 1
        print('测试集准确率：',float(correct_num)/len(test_x))

        out1 = model.predict(tx)
        correct_num = 0
        for i in range(len(out1)):
            if out1[i][0]<0.5:#预测是1的值的概率小于0.5
                temp_result = 0.0#所以 预测天辉失败 radiant_win==False==0=True
            else:
                temp_result = 1.0
            if temp_result==ty[i][0]:
                correct_num += 1
        print('训练集准确率：',float(correct_num)/len(tx))

        out2 = model.predict(validate_x)
        correct_num = 0
        for i in range(len(out2)):
            if out2[i][0]<0.5:
                temp_result = 0.0
            else:
                temp_result = 1.0
            if temp_result==validate_y[i][0]:
                correct_num += 1
        print('验证集准确率：',float(correct_num)/len(validate_x))

        correct_num = 0
        compare_num = 0
        for i in range(len(out0)):
            if out0[i][0]<(1.0-tag_line) or out0[i][0]>tag_line:
                compare_num += 1
                if out0[i][0]<0.5:
                    temp_result = 0.0
                else:
                    temp_result = 1.0
                if temp_result==test_y[i][0]:
                    correct_num += 1
        if compare_num!=0:
            print('测试集,预测胜率在'+str(tag_line)+'以上的准确率：',float(correct_num)/compare_num,\
                ' ('+str(correct_num)+'/'+str(compare_num)+')')
        else:
            print('测试集,预测胜率在'+str(tag_line)+'以上的准确率：','0.0',\
                ' ('+str(correct_num)+'/'+str(compare_num)+')')
        for i in range(5):
            tag_line = 0.75+0.05*i
            correct_num = 0
            compare_num = 0
            for i in range(len(out0)):
                if out0[i][0]<(1.0-tag_line) or out0[i][0]>tag_line:
                    compare_num += 1
                    if out0[i][0]<0.5:
                        temp_result = 0.0
                    else:
                        temp_result = 1.0
                    if temp_result==test_y[i][0]:
                        correct_num += 1
            if compare_num!=0:
                print('测试集,预测胜率在'+str(tag_line)+'以上的准确率：',float(correct_num)/compare_num,\
                    ' ('+str(correct_num)+'/'+str(compare_num)+')')
            else:
                print('测试集,预测胜率在'+str(tag_line)+'以上的准确率：','0.0',\
                    ' ('+str(correct_num)+'/'+str(compare_num)+')')
    def query(self):
        model = load_model(self.modle_path+self.using_model_name)
        self.match_url=[]
        with open("hero_id_name.json","r+") as f:
            self.hero_id_name=load(f)
        from dotadata_mining_banpick import Ban_Pick
        radiant,dire=[],[]
        radiant_name,dire_name=[],[]
        self.instance=Ban_Pick()
        r_vector=np.zeros(129)
        d_vector=np.zeros(129)
        print (instance.match_url,"比赛实时列表长度:",len(instance.match_url))
        radiant_full,dire_full,rname,dname=self.instance.get_vpgame()#get_vpgame()
        print(radiant_full,dire_full,rname,dname)   
        self.instance.match_url=[1]
        x_label=[]
        for one_full_url in self.instance.match_url:
            radiant_full,dire_full,rname,dname=self.instance.get_vpgame()#get_kuaikegame()get_vpgame
            print(radiant_full,dire_full,rname,dname)
            print(radiant_full,dire_full)
            if len(radiant_full)==5 and len(dire_full)==5:        
                for i,j in zip(radiant_full,dire_full):
                    r_vector[i-1]=1
                    d_vector[j-1]=1
                    radiant_name.append(self.hero_id_name[str(i)])
                    dire_name.append(self.hero_id_name[str(j)])
                x_label.append([r_vector,d_vector])        
                test_x = np.array(x_label).reshape(len(x_label),2,129)
        out0 = model.predict(test_x)
        if out0[0][0]<0.5:
            # print (1-out0[0][0])
            temp_result = 0.0#预测radiant_win的值为0,所以天辉失败
            print("预测右边胜利,right win:",1-out0[0][0],radiant_full,radiant_name,rname,"vs",dire_full,dire_name,dname,)
        else:
            # print (out0[0])
            print("预测左边胜利,right lose:",out0[0][0],radiant_full,radiant_name,rname,"vs",dire_full,dire_name,dname)
            temp_result = 1.0
     
if __name__ == '__main__':
    UPDATE_MODEL=False
    if UPDATE_MODEL==True:
        x_label,y_label=[],[]
        fname="matches_list_ranking_2e6_0915.csv"#matches_list_ranking_2e6.csv"#"normalmatch_2e5.csv"
        # fname="real_match_current_2e3_0915.csv"#只使用职业比赛
        pd_match=pd.read_csv(fname)
        for one_game in pd_match.values:
            radiant_win, radiant_heroes, dire_heroes = one_game[1], one_game[2], one_game[3]    
            radiant_heroes = list(map(int, radiant_heroes.split(',')))
            dire_heroes = list(map(int, dire_heroes.split(',')))
            r_vector=np.zeros(129)
            d_vector=np.zeros(129)
            for i,j in zip(radiant_heroes,dire_heroes):
                r_vector[i-1]=1
                d_vector[j-1]=1
            x_label.append([r_vector,d_vector])
        y_label = list(pd_match.radiant_win)#(pd_match.radiant_win==1.0).astype(np.int)
        instance=DL_PICKS(arg1=x_label,arg2=y_label)
        instance.training()
        tag_line = 0.55
        instance.testing(tag_line)
    else:
        instance=DL_PICKS(arg1=None,arg2=None)
        instance.query()
    # instance.training()
    # tag_line = 0.55
    # instance.testing(tag_line)
# assert 1>2
# with open(DATA_PATH+"matches_list_ranking_2e6.csv",'r',encoding='utf-8') as fo_1:
#     line_matches = fo_1.readlines()
#     sample_in = []
#     sample_out = []
#     for i in range(len(line_matches))[1:]:
#         split = line_matches[i].split(', ')
#         radiant = split[2]
#         dire = split[3]
#         # print(split[4][:-1])
#         if split[4][:-1]=='True':
#             win = 1.0
#         else:
#             win = 0.0
#         radiant = list(map(int,radiant.split(',')))
#         dire = list(map(int,dire.split(',')))
#         radiant_vector = np.zeros(hero_id_max)
#         dire_vector = np.zeros(hero_id_max)
#         for item in radiant:
#             radiant_vector[item-1] = 1
#         for item in dire:
#             dire_vector[item-1] = 1
#         sample_in.append([radiant_vector,dire_vector])
#         sample_out.append(win)
# print (len(sample_in),len(sample_out))
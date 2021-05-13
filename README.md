# 螺旋桨RNA结构预测竞赛第六名方案

## 团队信息

团队名称：逍遥郎1392

团队成员：谢自强

团队成绩：初赛 4.559（第20名），复赛 3.769 （第6名）

## 项目描述
任务：对于给定的RNA碱基序列，要求构建模型预测RNA碱基不成对的概率。

工程环境：Python3.7+PaddlePaddle2.0.2，fork官方基线系统；

## 工程结构

├── 1746242.ipynb..................................... # Notebook  
├── README.md  
├── LICENSE  
├── requirements.txt  
├── 螺旋桨RNA结构预测竞赛第六名解决方案.pdf.............# 方案简介  
├── data
│   └── data67691  
├── postprocess........................................... #  初赛后处理及结果  
│   ├── postprocess.py  
│   ├── predict.files...........................................# 初赛最优结果

│   ├── predict.files_baseline_self

│   ├── predict.files_baseline_swish

│   ├── predict.files_baseline

│   └── predict.files_baseline_and_dev

├── postprocess_2...........................................#  复赛后处理及结果

│   ├── postprocess.py

│   ├── predict.files...........................................# 复赛最优结果

│   ├── predict.files.zip

│   ├── predict.files_add_dev

│   ├── predict.files_bl

│   ├── predict.files_bl_self

│   └── predict.files_bl_swish

├── work............................................................# 训练工程1 

│   ├── create_result.py

│   ├── data

│   ├── model...........................................# 模型位置

│   ├── model-0.......................................# 模型位置

│   ├── model_x2

│   ├── README.txt

│   ├── src

│   ├── test_log.txt

│   └── train_log.txt

└── work2..........................................................# 训练工程2

​    ├── create_result.py

​    ├── data

​    ├── model ...........................................# 模型位置

​    ├── README.txt

​    ├── src

​    ├── test_log.txt

​    └── train_log.txt

## 1. 数据集

初赛数据集包含训练集4750条，验证集250条，测试集444条，采用官方给定的数据进行训练，不再单独划分；

## 2. 方案分析

#### 2.1 baseline

直接利用baseline自带的模型生成结果提交，验证了整个测试、结果生成和提交流程；

模型位置：work/model-0/model_dev=0.0772          

#### 2.2 训练baseline网络

直接无修改训练baseline网络，生成结果并提交；

模型位置：work/model/model_bl_self=0.0676      

#### 2.3 增大网络训练

将baseline网络增大一倍，layers参数由8设置为16，dmodel参数由128修改设置为256；

模型位置：work/model_x2/model_x2_dev=0.0660

#### 2.4 增加训练epoch

将训练epoch，由10增加为20，训练baseline网络，效果不理想，模型最终未保存；

#### 2.5 修改激活函数

将网络自带的Relu激活函数修改为swish激活函数，该工程为work2；

修改代码：work2/src/network.py

模型位置：work2/model/model_dev=0.0700

#### 2.6 全数据训练

充足的训练数据才是模型效果的保障，因此最后考虑采用训练加验证合并训练的方法，同时为了使新增数据得到充分训练，将其扩充为2倍加入到训练集中，训练baseline网络；

数据文件：work/data/train_dev2.txt

模型位置：work/model/model_add_dev=0.0624

## 3. 模型融合

在上述方案中，如原baseline网络训练多次，很多效果不是很理想，仅保留了其中最好的结果的模型。然后采用多个模型结果融合的方法进一步提升指标。

模型融合采用4个模型，分别是：

a. baseline模型（2.1）

b. baseline训练模型（2.2）

c. 修改激活函数的模型（2.5）

d. 全数据训练模型（2.6）

融合方式采用线性加权的方式，为4个模型生成的概率值分别赋给不同的权重然后生成融合后的结果；

**初赛**中，通过分配不同的比例的权重进行多次的对比与测试，最终采用的融合比例为0.8/0.1/0.05/0.05，**初赛为第20名**；

最终的结果：postprocess/predict.files.zip

**复赛**中，由于不同模型对复赛的测试集的效果与初赛有很大的不同，因此在分别测试了单个模型的结果后，需要对比例进行调整和验证，最终的比例为0.45/0.01/0/0.45，**复赛为第6名**；

最终的结果：postprocess_2/predict.files.zip

## 4. 结果复现

环境准备：在aistudio上，fork官方基线系统https://aistudio.baidu.com/aistudio/projectdetail/1444108

删除或重命名自带的work文件夹，然后上传拷贝本方案代码至work文件夹位置；

#### 4.1 利用模型生成可提交结果

进入work文件夹，执行：

python src/main.py test --model-path-base model-0/model_dev=0.0772

执行完成后会在当前目录生成test_log.txt，然后在当前目录执行：

python create_result.py

生成predict.files文件夹即为可提交的结果，并重命名为predict.files_bl；

按照上述方法，执行： 

python src/main.py test --model-path-base model/ model_bl_self=0.0676

python create_result.py

生成predict.files并重命名为predict.files_bl_self；

执行：

python src/main.py test --model-path-base model/ model_add_dev=0.0624

python create_result.py

生成predict.files并重命名为predict.files_bl_add_dev；

然后进入work2文件夹，执行：

python src/main.py test --model-path-base model/ model_dev=0.0700

python create_result.py

生成predict.files并重命名为predict.files_bl_swish；

#### 4.2 生成模型融合结果

将4.1中生成的4个重命名的以predict.files开头的文件夹拷贝到postprocess_2文件夹，并执行：

python postprocess.py

完成后会生成predict.files文件夹，即是最终的结果；

最后执行：

zip –r predict.files.zip predict.files

生成最终提交的压缩文件predict.files.zip。

#### 说明：

1. 以上步骤为生成复赛结果的步骤；

2. 如果需要生成初赛的结果，需要修改work/src/dataset.py中line40和line41的测试集路径，将B_board_112_seqs.txt修改为test_nolabel.txt，work2同理；

3. 按照4.1步骤生成4个文件夹，然后拷贝到postprocess文件夹中，修改postprocess.py中的文件名，然后执行该文件即可；


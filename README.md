# 叉院集群使用指南

## 集群登录

#### 配置
- IP： 202.121.138.165
- 端口：8000
- 用户名：username
- 密码: password

#### 通过终端登录
```shell
ssh username@202.121.138.166 -p 8000
```

#### 通过终端文件传输
```shell
scp -P 8000 localfilepath username@202.121.138.166:/nfsshare/home/username/...
```


##### 注：
可以使用软件传输：
- Terminus(推荐)[教育版本免费使用](https://termius.com/education)   [多点同步配置](https://www.jianshu.com/p/507fa8ddd0b5)
-  scp
-  sftp

## 集群操作
#### 常用命令
- 查看集群状态
```shell
bhosts
```


- 查看队列
```shell
bqueues
```

- 查看节点运行情况
```shell
lsload
```

- 查看提交任务id及其状态
```shell
bjobs
```

- 查看运行中的任务的输出
```shell
bpeek <任务id>
```

- 终止任务
```shell
bkill <任务id>
```

- 提交任务
```shell
bsub <参数> <命令>
## for example
bsub -J hello python main.py
```

- 参数较复杂时，可以把参数和命令专门写在某个文件里，如
```shell
bsub < run.sh
```

`run.sh`文件的具体内容如下

```shell
#/bin/bash
#BSUB -J hello
python main.py
```

#### bsub 常用参数

| 参数        | 示例                                    | 含义                           |
| ----------- | --------------------------------------- | ------------------------------ |
| -J NAME     | -J hello                                | 指定任务名称为 hello           |
| -n 数字     | -n 1                                    | 指定1块CPU                     |
| -e 文件路径 | -e /nfsshare/home/USER/log/hello_%J.err | 指定报错文件，其中%J代表任务ID |
| -o 文件路径 | -o /nfsshare/home/USER/log/hello_%J.out | 指定输出文件，其中%J代表任务ID |
| -q 队列名称 | -q gauss                                | 指定任务队列为GPU队列          |
| -gpu        | -gpu "num=x:mode=exclusive_process"     | 指定使用x个gpu,并选择使用模式  |

##### 注：
-  队列部分，使用CPU填写cauchy，使用GPU填写gauss
-  大部分情况下选择num=1, 如果有并行化gpu运行代码可以选取使用多个gpu

下面给出一个run.sh的具体示例

```shell
#/bin/bash
#BSUB -J NAME
#BSUB -e /nfsshare/home/USER/log/NAME_%J.err
#BSUB -o /nfsshare/home/USER/log/NAME_%J.out
#BSUB -n 1
#BSUB -q gauss
#BSUB -gpu "num=1:mode=exclusive_process"
python main.py
```



## python 使用技巧

大部分人最常跑的还是python代码，这里我总结一下集群上的python使用技巧。
### 配置自己的python环境

建议自己配置属于自己的环境，大家的需求非常多样，集群上的python版本极有可能不满足大家的要求，建议自己配置自己的python环境，这里给出自定义python环境的参考，[安装anaconda 教程请点击](https://blog.csdn.net/wyf2017/article/details/118676765)，其中需要注意的是，文件大概率无法使用命令直接下载，可以先下载到本地再使用 Terminus或scp上传

#### 测试gpu使用
```shell
# 创建虚拟环境
conda create --name env python=3.7
# 激活虚拟环境
conda activate env
# 安装torch相关包
conda install pytorch==1.5.1 torchvision==0.6.1 cudatoolkit=10.1 -c pytorch -y
# 提交测试脚本，见run.sh, test_gpu.py, 注意需要在虚拟环境下提交任务
bsub < run.sh
```

#### pip安装

有时候我们会碰到无法使用conda安装，只有pip安装的一些包，比如`garage`, 可以在pip后面加上--user参数

```shell
pip install --user garage
```



## 非常用软件安装

集群的环境配置还是较为基础的，如果有一些个人定制话的软件需求，可以先参考 [linux非root用户怎么装软件](https://www.jianshu.com/p/0ef082354fc9)

如果仍然无法成功需要root权限，请在issue中提出。


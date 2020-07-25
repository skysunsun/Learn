---
title: 论文笔记-Deep Hierarchical Saliency Network for Salient Object Detection
commentable: True
data: 2019-06-24
mathjax: true
tags: 特征层次
categories: 论文笔记
description: 特征层次细化
---

# [Deep Hierarchical Saliency Network for Salient Object Detection](https://zpascal.net/cvpr2016/Liu_DHSNet_Deep_Hierarchical_CVPR_2016_paper.pdf)

## 针对问题

1. 如何构建真正意义上的特征表征
2. 如何探索所有潜在的突出线索
3. 如何找到最佳的集成策略
4. 如何有效地保护对象细节

## 整体结构

似曾相识的感觉
![ZkEjYR.png](https://s2.ax1x.com/2019/06/24/ZkEjYR.png)

### GV-CNN

同样是VGG-16提取特征，轻车熟路，但是加了个带sigmoid的全连接层，节点为784，然后把这个重构为 $28\times28 $的矩阵（这个操作我是服的），这个生成的只是一个粗略的显著性图，而且尺寸是四个下采样之后的，所以细节部分是丢失的。对于细节的丢失，文中说了两个原因
1. 四个下采样让网络丢掉了空间信息，从而导致了这个问题
2. 因为有全连接层的存在，所以参数量是和输入呈线性关系的（这个是个什么理由？？）
为了解决这些问题，就有了如下的模块

### HRCNN

#### Recurrent Convolutional Layer.（RCL）
[![Zk1HoV.png](https://s2.ax1x.com/2019/06/24/Zk1HoV.png)](https://imgchr.com/i/Zk1HoV)
这个做为啥就有效呢?
>多个重复连接使得子网从输入层到输出层有多条路径，便于学习。此外，RCL单元的有效接受域随着时间步长而增大，使得单元能够在不增加网络参数的情况下接受到越来越大的上下文。
但是卷积和核的大小都是$3\times3$这个能增加感受域么？

对于位于RCL中第k个特征图上$(i,j)$的单元,它在第$t$步的状态：
$$
x_{i j k}(t)=g\left(f\left(z_{i j k}(t)\right)\right)
$$
就是加了个$relu:f$和局部归一化$LRN:g$只要是为了防止梯度爆炸，那么这个$z_{i j k}(t)$怎么得到呢？
$$
z_{i j k}(t)=\left(\mathbf{w}_{k}^{f}\right)^{T} \mathbf{u}^{(i j)}+\left(\mathbf{w}_{k}^{r}\right)^{T} \mathbf{x}^{(i j)}(t-1)+b_{k}
$$
其中$\mathbf{u}^{(i, j)}$和$\mathbf{X}^{(i, j)}(t-1)$分别是前一层的前馈输入和当前层在$t-1$时刻的递归输入。那么这个$g\left(f_{i j k}(t)\right)$怎么得到呢？（作者这些骚操作我是服的）
$$
g\left(f_{i j k}(t)\right)=\frac{f_{i j k}(t)}{\left(1+\frac{\alpha}{N} \sum_{k^{\prime}=\max (0, k-N / 2)}^{\min (K, k+N / 2)}\left(f_{i j k^{\prime}}\right)^{2}\right)^{\beta}}
$$

这里作者把$f\left(z_{i j k}(t)\right)$换成了$f_{i j k}(t)$（感觉一行就写完的公式，作者硬是把这个公式玩出了新花样）$K$是特征图的总数,$N$是临近的特征图的大小

#### Hierarchical Saliency Map Refinement

1. 在融合之前，用64个$1\times1$的卷积核先缩小vgg-16特征图个数，同时用了sigmoid函数
2. 用RCL生成的特征图融合，上采样一倍
3. 如此反复

从图中可以看到每一个RCL生成的特征图都是在G&T的监督下进行的。


## 思考
### 好的地方

1. 主要模块RCL的运用吧
2. 作者提到这是首次考虑到全局信息

### 没看懂的地方

1. 在VGG 最后一个块生成的特征图的过程中，作者先用了全连接层，然后再搞成矩阵，这个操作还是头一次见

---
title: 论文笔记-Convolutional Networks for Biomedical Image Segmentation
commentable: True
data: 2019-07-24
mathjax: true
tags: 网络结构
---

# [Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/pdf/1505.04597.pdf)

## 针对问题

1. 深度学习需要大量的样本
2. 样本不平衡问题

## 整体结构


![eAi0Vx.png](https://s2.ax1x.com/2019/07/23/eAi0Vx.png)

如图所示，网络包含下采样和上采样两部分（文中为收缩和扩张模块）

### 下采样

采用两个不进行填充的$3\times3$卷积，跟着一个$Relu$激活函数，然后$2\times2$的池化层用于下采样，同样每下采样一次扩大一倍特征层数

### 上采样

上采样之后跟一个$2\times2$的卷积用于减少特征层数，然后和下采样的特征融合，但是并不是直接融合（因为尺寸不对应）而是对下采样特征进行了剪裁，最后同样使用两个不进行填充的$3\times3$的卷积，同样跟着一个$Relu$激活函数，不同的是这次是把特征减少一半
> The cropping is necessary due to the loss of border pixels in every convolution.

不是很理解这个操作，剪裁了不是丢失更多么？

最后使用$1\times1$卷积输出特征图。文中没有说明上采样用的啥方法....

### 损失函数

使用$softmax$和交叉熵损失结合
$$
p_{k}(\mathrm{x})=\exp \left(a_{k}(\mathrm{x})\right) /\left(\sum_{k^{\prime}=1}^{K} \exp \left(a_{k^{\prime}}(\mathrm{x})\right)\right)\\
E=\sum_{\mathbf{x} \in \Omega} w(\mathbf{x}) \log \left(p_{\ell(\mathbf{x})}(\mathbf{x})\right)
$$
$a_{k}(\mathrm{x})$为第$k$个通道的$x$像素的激活值，$K$是类别数目，$l$为每个像素的真值，$w$给一些像素引入的权重映射（懵逼....）
$$
w(\mathbf{x})=w_{c}(\mathbf{x})+w_{0} \cdot \exp \left(-\frac{\left(d_{1}(\mathbf{x})+d_{2}(\mathbf{x})\right)^{2}}{2 \sigma^{2}}\right)
$$

$w_{c}$为权重映射用于平衡类频率，$d_{1}$表示到最近单元格边界的距离，$d_{2}$表示到第二近单元格边界的距离，文中设置$w_{0}=10$，$\sigma \approx 5$


## 思考


1. 这篇论文是用于医学图像的，实验部分也看不懂，后面的损失函数也是看的有点懵逼，主要还是这个网络的结构设计
2. 低层信息和高层信息融合好像就是从这里开始的吧
3. 文中由于数据缺少，对数据做了增强

### 没看懂的地方

1. 文中不用填充卷积保持卷积尺寸一致呀？
2. 文中在特征融合的时候进行特征剪裁，一是为了尺寸对应，但文中说的主要原因却不是这个

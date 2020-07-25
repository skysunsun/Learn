---
title: 论文笔记-DenseNet
commentable: True
data: 2019-07-05
mathjax: true
tags: 网络结构
categories: 论文笔记
description: 特征重用
---

# [Densely Connected Convolutional Networks](https://arxiv.org/pdf/1608.06993.pdf)

## 针对问题

1. 深度导致的信息丢失
2. 随着网络深度的增加，梯度消失/爆炸
3. 对短连接进行改进

## 和$Resnet$的区别
假设$x_0$为输入，$\ell$表示$L$层，$H_{\ell}(\cdot)$表示$L$层的一系列操作（正则化等，卷积，池化）, $L$层的输出为$\mathrm{x}_{\ell}$
### $Resnet$
$$
\mathbf{x}_{\ell}=H_{\ell}\left(\mathbf{x}_{\ell-1}\right)+\mathbf{x}_{\ell-1}
$$
文中说到$Resnet$通过加法运算阻碍徐信息流。。。。感觉好牵强啊！！！哈哈哈哈，要怎么解决这个问题呢？
$$
\mathbf{x}_{\ell}=H_{\ell}\left(\left[\mathbf{x}_{0}, \mathbf{x}_{1}, \ldots, \mathbf{x}_{\ell-1}\right]\right)
$$
![Z4io6g.png](https://s2.ax1x.com/2019/07/13/Z4io6g.png)
用了特征层的连接（或者是特征层的叠加）而不是简单的加法，这里的$H_{\ell}(\cdot)$包含的操作有$BN,ReLU,Conv(3\times3)$

由于卷积网络通过缩小尺寸来弥补特征深度增加的时间复杂度，以此来维持每层有大致相同的时间复杂度，但是这个就存在一个问题，通过特征叠加要求特征的尺寸必须是相等的，不能跨尺寸连接。所以文中的密连连接只存在于每一个卷积块中，然后通过转换层进行特征减小（文中缩小一半）和下采样，转换层包括连个操作：
$$
Conv(1\times1)\\
Avgpool(2\times2)
$$
![Z4V98x.png](https://s2.ax1x.com/2019/07/13/Z4V98x.png)
那每个卷积块到底把特征缩小到多少呢？（也就是上面每个密连块中的每个点的输出层数）这就是文中称为增长率的东西，文中在Imgnet中设置为12，同时设置了只有只向后输送4层，虽然设置为12已经很小了，但是同一个密连块中越到后面层会越来越多，这个会导致参数的爆炸增长，为了控制这个，$H_{\ell}(\cdot)$中包含的操作就增加了一个用来缩小特征层数的卷积$BN,ReLU,Conv(1\times1)，BN,ReLU,Conv(3\times3)$
，$1\times1$卷积把特征放大或者缩小到128，然后用$3\times3$在把特征缩小到12

不同层数的$DenseNet$参数表
![Z4V3qg.png](https://s2.ax1x.com/2019/07/13/Z4V3qg.png)

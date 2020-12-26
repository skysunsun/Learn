# [Receptive Field Block Net for Accurate and Fast Object Detection](https://arxiv.org/abs/1711.07767)

## 问题

**深度网络计算代价大，不能满足实时需求**

其中谈到几个相似网络的缺点

- inception：虽然有不同的卷积核，但是每个卷积核的中心是一样的。
- deeplab的aspp：特征与之前卷积层的特征的分辨率是一致的，并且与最初的卷积层相比，所得特征往往不那么鲜明。
- Deformable CNN：未考虑RF**离心率**(这个是什么东西？)的影响，并且没有突出最重要的信息。

# 网络

## 几个网络的一个可视化对比

![0bC1Nd.png](https://s1.ax1x.com/2020/10/16/0bC1Nd.png)

## RFB模块



作者在最新版的inception结构上做的改进


![0bPHij.png](https://s1.ax1x.com/2020/10/16/0bPHij.png)

![0bFFAg.png](https://s1.ax1x.com/2020/10/16/0bFFAg.png)
使用了$1\times1$卷积做了维度转换，使用了叠加的$3\times3$卷积代替$5\times5$卷积，同时使用了$1\times n$和$n\times1$的结构代替$n \times n$结构，以此来减少参数（但只用了一次挺奇怪的）

可以看到是在inception的基础上加了膨胀卷积，同时做了参数优化

>The kernel size and dilation have a similar positive functional relation as that of the size and eccentricity of pRFs in the visual cortex.

作者说这个和人类视觉的感受野对应上了？

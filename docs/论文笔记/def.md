

# [Deep Embedding Features for Salient Object Detection](https://drive.google.com/file/d/1l02_GtoMxRFy9IJifSjs-zjYOOQWoBfx/view)（深度嵌入特征）

## 针对问题

1. 池化和卷积等下采样操作极大地降低了初始图像的分辨率，降低了图像边界等细节。
2. 引入重载层来集成多级特性。这种过多的过程常常导致特性混乱，从而导致不正确的显著性检测结果。

## 架构

这篇论文的架构还是挺复杂的，有好几个块！
![VJnkQS.png](https://s2.ax1x.com/2019/06/03/VJnkQS.png)

### 初始显著性网络(ISN)：提供初始显著性预测和多尺度侧输出特征

文中选取了ResNet101作为基础框架。变化：

1. 最后一个块的步长设置为1(获取更大的特征图)
2. 选择最后两个块的输出作为侧边输出层(提高计算效率)(没看懂？？？？整体架构中每个块都有侧输出啊)
3. 将侧输出通过两个卷积层，其中包含256个内核。(减小特维数)将两个特征图分别输入一个含有1个核的卷积层中，向上采样至$64\times64$，得到初始预测图。

### 深度特征嵌入网络(FEN)：将ISN的预测和特征嵌入到度量空间中，对特征图中每个元素的空间重要性进行加权

[![VJK9v8.png](https://s2.ax1x.com/2019/06/03/VJK9v8.png)](https://imgchr.com/i/VJK9v8)
通过下采样和上采样把ISN每个块的输出全部变为$64\times64\times64$最后在连在一起形成综合特征图：
$$
F=C a t_{l=1}^{5}\left(\operatorname{Conv}\left(\text {Side}_{l}\right)\right) )
$$
设$S_{1}$是初步的显著性图，则反显著性图为：$1-S_{1}$代表背景特征，然后将每个像素映射到320维:
$$
\varphi_{m k}=\mu\left(s_{m k} ; \psi\right), k=0,1
$$
$\mathcal{S}_{m k}$为$S_{k}$在位置$m$处的值。$\varphi_{m 1}$和$\varphi_{m 0}$
分别为显著图和反显著性图中每个像素在位置$m$的嵌入向量，$\mu$和$\psi$表示嵌入操作及其参数。
$$
V\left(I_{m}\right)=\left|\operatorname{Dis}\left(\varphi_{m 1}, \mathbf{f}_{m}\right)-\operatorname{Dis}\left(\varphi_{m 0}, \mathbf{f}_{m}\right)\right|
$$
通过上式得到图像$I$在$m$处的注意特征。
$\mathrm{f}_{\mathrm{m}}$为位置$m$处综合特征向量。$\operatorname{Dis}(\cdot, \cdot)$为欧氏距离。
简单来说，是前景和整体的欧氏距离减去背景和整体的欧式距离的绝对值，这都是怎么想出来的？？？？

### 递归特征集成网络(RFIN)：将嵌入特征与剩余重构特征相结合，从深到浅的方式预测了一系列阶段显著性映射
[![VJtH76.png](https://s2.ax1x.com/2019/06/03/VJtH76.png)](https://imgchr.com/i/VJtH76)
主要用于细化细节区域，可以看到这里用了两个流的卷积然后再合并。最后为256个特征。然后融合ELM的输出，最后再来个SSP的反向修正，这里的$W_{i}$和$b$为卷积运算的权重和偏置，不知道为啥这里要这样写。$Conv$不是更简单
$$
\mathbf{P}^{\mathrm{i}}=\left\{\begin{array}{l}{W_{i} * \operatorname{Cat}\left(\left(\mathbf{E m}+\mathbf{R} \mathbf{F} \mathbf{R}^{l}\right), \mathbf{P}^{\mathbf{i}-1}\right)+b, i=2,3,4} \\ {W_{i} *\left(\mathbf{E m}+\mathbf{R} \mathbf{F} \mathbf{R}^{l}\right)+b, i=1}\end{array}\right.
$$

### 引导滤波细化网络(GFRN)：以原始的RGB图像和RFIN生成的最后一个显著性图作为输入，将RGB图像转化为制导图，对突出目标的边界进行细化。
[![VJtOhD.png](https://s2.ax1x.com/2019/06/03/VJtOhD.png)](https://imgchr.com/i/VJtOhD)
然而文中说还是有边界的问题，因此又加了个网路(GFRN)。
原始RGB图像和RFIN生成的显著性特征图是GFRN的输入。在给定一对输入的情况下，首先将卷积层作为变换函数来改变输入图像的维数。然后，利用均值滤波和线性模型，将$G$和$S$之间的重构误差最小化，计算出$A$和$b$。输出显著性映射$(O)$是通过以$A$、$b$和$G$为输入的线性变换来计算。
$$
O=A * G+b
$$

## 思考
### 好的地方

1. 运用到度量空间计算注意特征
2. 通过原图来细化边界

### 没看懂的地方

1. 我是觉得网络过于庞大了。感觉太过冗余
2. 而文中开篇就说了现在的网络运用多级特征，可能导致冗余，而文中的网络，用了好多的多级特征.......
3. 最后一个网络是没看懂，最下边的箭头是不是画反了。
4. 最后一个网络，前面废了这么大的劲，就为了算一个$A$和$b$，最后的输出由输入图通过一个线性模型得到。看的我是一脸的懵逼呀！
5. 网络的结构设计，感觉现在设计一个网络是拼想象力的时候了，怎么就想到这种网络了呢？全是实验解释，完全没有理论支撑呀！

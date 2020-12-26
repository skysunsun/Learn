# [deeplabv1](https://arxiv.org/pdf/1412.7062v3.pdf)

## 问题

分割结果粗糙

- 池化导致丢失信息

- 二是没有利用标签之间的概率关系

## 方法

使用了膨胀卷积

深度网络和CRF的级联

# [deeplabv2](https://arxiv.org/pdf/1606.00915.pdf)


## 问题

## 方法

aspp


# [deeplabv3](https://arxiv.org/pdf/1706.05587.pdf)

## 问题

- 连续的下采样虽然能让网络有更大的感受野学到更多的知识，但是分辨率的下降对于像素级的任务确实头疼

- 需要预测不同尺度的目标

作者盘点了当前的一些处理多尺度问题的网络结构

[![BebYIH.png](https://s1.ax1x.com/2020/10/25/BebYIH.png)](https://imgchr.com/i/BebYIH)

- 把输入图片缩放成不同尺度，经过同一个网络，最终融合多尺度下的物体信息。**但不能推广到大型的深度网络（计算资源有限）**
- 使用编解码结构，在decoder时融合encoder网络不同阶段的特征。**确实有效**
- 在原网络最后层增加额外的context模块。**额外肯定就有额外的计算量**
- 在原网络最后层添加并行结构—空间金字塔池化，获取不同尺度的物体信息


## 方法

作者在ResNet的基础上多加了几个Block并且每个块使用了不同膨胀率的膨胀卷积，以此获得更多的上下文信息

### 串行ASPP

[![BeOZdS.png](https://s1.ax1x.com/2020/10/25/BeOZdS.png)](https://imgchr.com/i/BeOZdS)

但是并不是膨胀率越大越好

[![BeXN0f.png](https://s1.ax1x.com/2020/10/25/BeXN0f.png)](https://imgchr.com/i/BeXN0f)

作者通过实验发现如果膨胀率太大，只有卷积核最中间的权重有效，会导致直接退化为$1 \times 1$卷积，这样就和初心获取更多的信息背道而驰了


### 并行ASPP

为了解决这个问题，作者在模型最后的特征映射上应用全局平均，将结果经过$1 \times 1$的卷积，再双线性上采样得到所需的空间维度

[![Bev9G4.png](https://s1.ax1x.com/2020/10/25/Bev9G4.png)](https://imgchr.com/i/Bev9G4)

deeplabv3重点探讨了空洞卷积的使用，同时改进了ASPP模块，便于更好的捕捉多尺度上下文。


# [deeplabv3+](https://arxiv.org/pdf/1802.02611.pdf)

## 问题

- 池化带来的细节丢失，边缘丢失
- 引文deeplab的aspp结构一般是在最后几层，最后几层一般特征比较多，这样会导致计算代价太大的（作者用resnet举了个例子）

## 方法

这篇论文是在deeplabv3上的改进，作者提到金字塔池化模块能够对多尺度信息进行编码融合，编码解码结构能够逐步恢复空间信息来捕获更清晰的边界；所以这篇论文主要是融合了这两种方法以提高模型的性能。

[![BedBz6.png](https://s1.ax1x.com/2020/10/25/BedBz6.png)](https://imgchr.com/i/BedBz6)

- 左边为deeplabv3的结构，可以看到这个上采样太粗暴了
- 中间为U-Net结构
- 右边为deeplabv3+的结构，直接在deeplabv3的基础上加了一个解码结构，这样上采样就没那么粗暴了，具体的结构如下

[![BeBVsK.png](https://s1.ax1x.com/2020/10/25/BeBVsK.png)](https://imgchr.com/i/BeBVsK)

考虑到计算代价太大的问题，也只是加了一个解码器

对于网络中一些通道的选择，以及解码器和编码器的那一层融合，作者作者都是通过做实验做出了说明

针对第二个计算代价太大的问题，作者在编码器部分使用Xception模型并融入了膨胀卷积




# [Non-local-U-Nets](https://www.aaai.org/Papers/AAAI/2020GB/AAAI-WangZ.5933.pdf)

U-Nets系列主要是用于医学图像的分割，这篇文章也不例外

## 问题

- 网络过深参数多会导致效率低下，而且网络深了下采样增多导致丢失更过的空间信息

- 之前的U-Nets只使用了局部信息（不管是卷积，池化，还是上采样都是），而对于重建图像，全局信息是很重要的

## 方法

![tMUlcQ.png](https://s1.ax1x.com/2020/05/30/tMUlcQ.png)

可以看到这里和我们看到的一般卷积不同多了一个$D$,主要是这篇文章作者使用的是$3D$卷积

**这里有一点和U-Nets不同的是，Encoder和Decoder的特征是相加的而不是叠加**作者提到这样有两点好处：

1. 不会增加特征层数，自然也不会增加参数
2. 这样可以看做是一个长距离的residual

当然这也有一个弊端就是：*特征没有以前丰富了*

以下为各个模块的具体信息
![tMdZJf.png](https://s1.ax1x.com/2020/05/30/tMdZJf.png)
可以看到作者整个网络全程都用了residual模块，下面分别看一下每一个模块

### a:input block

### b:down-sampling residual block 

### c:Global Aggregation Block(bottom block)

这个模块主要是要整个全局信息，**文中提到全连接层有整合全局信息的能力，但是容易过拟合**因此作者没用

这让我想起一个面试题
>为什么全连接层可以作为特征的heatmap

而且感觉这和[SENets](https://arxiv.org/pdf/1709.01507.pdf)使用全连接层的信息重构特征不谋而合

既然这个不行，作者就换了个方向，从$Transformer的self-attention$入手，当然这不是空穴来风，还是多看论文啊，作者参考的是2018的一篇论文[non-local neural networks for video classification](https://arxiv.org/pdf/1711.07971v1.pdf)

下面来具体看看这个模块吧

![tM0LZj.png](https://s1.ax1x.com/2020/05/30/tM0LZj.png)


作者使用$1\times1\times1$的步长为$1$卷积来计算$K,V$，而特征的输出取决于$Q$，所以对于$Q$的计算可以根据我们需要选择合适操作，这里的$QueryTransform_{C_{K}}(\cdot)$用于算出$C_k$个通道的特征，上采样的时候作者使用了$3\times3\times3$的步长为$2$反卷积来计算$Q$，$Unfold(\cdot)$主要是改变特征的形状：把$D \times H \times W \times C$转换成$(D \times H \times W) \times C$，同时可以看到作者还加入了$Dropout$防止过拟合。

### d:up-sampling residual block



## 总结一下

这篇文章主要是把$Transformer的self-attention$这个模块用到了整个卷积神经网络中,用这个模块去整合全局信息。但很吃显存

作者是把数据切片了(是这么称呼的吗)然后用了$Tianxp12G$的卡把实验跑完了

还没有跑过这个网络，但是那天试了一下$2D$的$self\_attention$，
输入：$8\times352\times352\times128$,结果要$40G$的显存，好吧!贫穷又一次阻碍了我的学术之路




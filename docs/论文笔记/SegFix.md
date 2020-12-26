# [SegFix: Model-Agnostic Boundary Reﬁnement for Segmentation]()

## 研究问题

- 主要针对分割边界预测不准问题

## 方法
[![rW3Hjx.png](https://s3.ax1x.com/2020/12/25/rW3Hjx.png)](https://imgchr.com/i/rW3Hjx)

>We propose a novel model-agnostic post-processing mechanism to reduce boundary errors by replacing labels of boundary pixels with the labels of corresponding interior pixels for a segmentation result.

有点迷，这句话到底是什么意思？？？不急，看看后面

从上面的模型结构看出是两个分支：一个边界；一个方向；然后融合

### 首先，使用卷积网络生成一个边界掩模

作者采用了HRNet做了一些小的改动

- 使用了$4 \times 4 $步长为2的反卷积

- 使用$1 \times 1 $卷积把最后的通道缩小为1

- 使用二进制交叉熵作为损失函数


### 然后从边界像素到内部像素的方向，然后沿着该方向预测内部像素（这是农村包围城市吗？？？？？）

对于偏移的预测，作者直接采用八方站位，而不是回归的方法

这里有个问题是八方站位怎么表示呢？请看作者的表演
[![rWd4U0.png](https://s3.ax1x.com/2020/12/25/rWd4U0.png)](https://imgchr.com/i/rWd4U0)

- 同样使用$1 \times 1 $卷积把最后的通道缩小为8

- 使用分类交叉熵作为损失函数

- 把方向map和边界map相乘，这样就只有边缘的地方有值了

- 最后使用偏移图对粗糙的分割图进行微调

大概是这个样子？

[![rWN7gH.png](https://s3.ax1x.com/2020/12/25/rWN7gH.png)](https://imgchr.com/i/rWN7gH)

上文中没有提到这个粗糙的分割图哪里来的，这里作者说可以用任何一个分割网络的分割图，那么本文提到的这个网络只是对别人的分割图进行微调，他只是生成了一个微调的offsetmap

$$
\hat L_p =  L_p+\Delta q
$$

这里又有个问题，如果边界太厚，那么偏移好像就没有意义（边界厚了把偏移盖住了）


作者提出了两种方法

1. 用缩放因子进行缩放

2. 迭代循环

### 关于G&T的生成

文中一个用三个监督，有两个监督是没有现成的（边界和八方）且看作者如何表演

[![rWBWbd.png](https://s3.ax1x.com/2020/12/25/rWBWbd.png)](https://imgchr.com/i/rWBWbd)

- 每个类别都生成一个二进制mask

- 使用距离转换计算distance map（融合Binary Map，这个距离代表到边界的距离？？然后根据阈值判断？？？（小于阈值的作为边界）阈值文中取了5）

>这个距离转换不知道怎么算的，文中提到的是另外一篇论文的算法

- 使用sobel算子计算八方图（颜色表示）

>We perform the Sobel ﬁlter (with kernel size 9×9) on the K distance maps independently to compute the corresponding K direction maps respectively. The Sobel ﬁlter based direction is in the range [0,360), and each direction points to the interior pixel (within the neighborhood) that is furthest away from the object boundary. We divide the entire direction range to m categories (or partitions) and then assign the direction of each pixel to the corresponding category.

每个方向都用sobel算子计算方向映射（sobel，怎么计算方向映射的？？？）一共$m$个类别，然后划分每个像素的类别就得到Direction Map


总结来看这篇论文主要是生成一个偏置对已经生成的分割图进行校正！
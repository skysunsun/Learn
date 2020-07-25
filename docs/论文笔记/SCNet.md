

# [Efficient saliency detection using convolutional neural networks with feature selection](https://www.sciencedirect.com/science/article/pii/S002002551830361X)

## 针对问题

1. 关于特征研究的空白
2. 不进行特征选择，这往往导致模型参数量大，运行时间长。

## 特征分析

> 哪些特征对显著性预测有用？哪些特征形式可以最有效地应用？以及如何选择和处理这些特征，这些问题都是有待解决和探索的？

基于这几个问题，作者首先对卷积得到的特征图进行了分析。文中分析了VGG-16在ImageNet上预训练的conv1_2,conv3_3,conv5_3这三个卷积块生成的特征图，使用了如下的评价函数：
$$
V_{k}=\sum_{i} \sum_{j}\left|\left(S_{k}-T\right)_{i j}\right|
$$
文中分析得出，低层的特征又许多背景噪声，深层特征可以很好的突出显著性物体而没有背景噪声。贴上作者的可视化结果(这里作者取了有最小V的特征图，在文章开头还有均值的，效果差不多)
![VHfhhF.png](https://s2.ax1x.com/2019/06/17/VHfhhF.png)
同时，作者用这个图进一步佐证了深层特征大多数都是有用的（但是并不是每一个都是有用的），而浅层的则相反
[![VHfx9e.png](https://s2.ax1x.com/2019/06/17/VHfx9e.png)](https://imgchr.com/i/VHfx9e)
特征分析得出的结论：
1. 卷积层特征图可用于显著性检测;
2. 层次越高，高级语义特征越多，层次越低，局部特征越丰富;
3. 选择特征图，可以更有效地促进显著性预测;
4. 大部分来自高层的特征图可以大致突出整个前台对象。

## 特征生成

文中基于小的V值进行选择，文中选取了V值最小的6个特征，由于没有特征没有规律可循，不得不计算每一个特征图的V值 **（大大加重了计算量）**
要计算V值就必须要有一个参照，文中用了$conv5_3$代替G&T(G&T不应该是手工制作的么？？)文中训练是把原图切分的，切成了224*224，然后通过滑窗的形式遍历整张图。
GT生成网络结构
![VH7Or4.png](https://s2.ax1x.com/2019/06/17/VH7Or4.png)
通过优化
$$
\underset{\theta_{G T}}{\arg \min } \frac{1}{m} \sum_{i=1}^{m}\left\|g_{i}^{c}-\psi\left(B_{i} | \theta_{G T}\right)\right\|_{2}^{2}+\alpha \sum_{k=1}^{2}\left\|W_{k}^{G T}\right\|_{F}^{2}
$$
来训练网络。

## 特征选择

将上面生成的特征输入SCnet（文中选了三个特征块的特征图，每个块6个特征图，所以输入SCnet的一共有18张特征图），文中提到一个问题是：初始化之后存在边界模糊的情况！为了保存边界信息，使用局部均值代替（这也是前面为什么要把整张图用滑窗的形式处理的原因吧）
SCnet作者画的特别的清楚，一看就懂
![VHL4yT.png](https://s2.ax1x.com/2019/06/17/VHL4yT.png)
这里用了Maxout这个函数而不是池化函数。文中是输出最大响应。感觉是个好东西呀！
同样通过优化下面这个函数来进行训练
$$
L\left(\theta_{\mathrm{SC}}\right)=\frac{1}{m} \sum_{i=1}^{m}\left\|g_{i}-\phi\left(\left\{M_{i}^{\mathrm{sel}}\right\} | \theta_{\mathrm{SC}}\right)\right\|_{2}^{2}+\lambda \sum_{k=1}^{2}\left\|W_{k}^{\mathrm{SC}}\right\|_{F}^{2}
$$
整体架构如下，可以说是很清楚了
![VHO0hR.png](https://s2.ax1x.com/2019/06/17/VHO0hR.png)

## 思考

1. 文中为什么要自己生成一个图代替G&T呢？我感觉这个是本文最大的BUG
2. 计算每个图的V值我觉得真的太耗时了
3. 这个是2018的论文，但是这个效果不是很好呀，而且耗时
4. 但是从特征选择这个出发点来看是很好的

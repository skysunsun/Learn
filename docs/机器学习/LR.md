假设给我们一堆样本，我们要对其进行二分类(0/1)，要么0，要么1，那如何怎么构建这个模型呢？而恰好有一个Sigmoid函数满足我们的要求
# Sigmoid函数及图像

$$σ(x)=\frac{1}{1+e^{-x}}$$

![ZaOsiR.png](https://s2.ax1x.com/2019/07/05/ZaOsiR.png)

可以看到，函数的定义域为$[-\infty,+\infty]$，值域为$(0,1)$,正好满足我们的要求，但是我们需要把样本映射到$-\infty$或者$+\infty$,这样才能更好的分类，这就是Logistic模型
# Logistic模型（参数化的Sigmoid函数）
$$h_{\theta}(x)=\frac{1}{1+e^{-\theta^{T} x}}$$
其中$\theta=\left(\theta_{0}, \theta_{1}, \cdots, \theta_{n}\right)$，$x=\left(1, x_{1},x_{2}, \cdots, x_{n}\right)$。这就是我们的模型，我们的目标就是要找到到一个合适的$\theta$，使得模型能够很好的分类。这就需要一个损失函数，然后使用梯度下降算法优化损失函数间接的优化模型。
# 损失函数

## 概率解释
LR模型主要用于解决二分类(0/1)问题，换个思路就成了：**预测值作为事件发生的概率。**

一个样本可以理解为发生的一次事件，样本生成的过程即事件发生的过程，对于0/1分类问题来讲，产生的结果有两种可能，符合伯努利试验的概率假设。因此，我们可以说样本的生成过程即为伯努利试验过程，产生的结果(0/1)服从伯努利分布，那么对于第$i$个样本，概率公式为：

$$\begin{aligned}
&P\left(y^{(i)}=1 | x^{(i)} ; \theta\right)=h_{\theta}\left(x^{(i)}\right)\\
&P\left(y^{(i)}=0 | x^{(i)} ; \theta\right)=1-h_{\theta}\left(x^{(i)}\right)
\end{aligned}$$
两个公式合并一下
$$P\left(y^{(i)} | x^{(i)} ; \theta\right)=\left(h_{\theta}\left(x^{(i)}\right)^{y(i)}\right)\left(1-h_{\theta}\left(x^{(i)}\right)\right)^{1-y(i)}$$
对于所有的样本，假设每条样本生成过程独立，在整个样本空间中（$N$个样本）的概率分布（即似然函数）为：
$$P(Y | X ; \theta)=\prod_{i=1}^{N}\left(h_{\theta}\left(x^{(i)}\right)^{y^{(i)}}\left(1-h_{\theta}\left(x^{(i)}\right)^{1-y^{(i)}}\right)\right)$$

> **似然函数：** 用于在已知某些观测所得到的结果时，对有关事物的性质的参数进行估计

> **最大似然函数：** 利用已知的样本分布，找到最有可能（即最大概率）导致这种分布的参数值；或者说什么样的参数才能使我们观测到目前这组数据的概率最大。

为了方便参数求解，对这个公式取对数，可得对数似然函数为：
$$\begin{aligned}
l(\theta)&=\sum_{i=1}^{N} \log P(Y | X ; \theta) \\
&=\sum_{i=1}^{N} y^{(i)} \log \left(h_{\theta}\left(x^{(i)}\right)\right)+\left(1-y^{(i)}\right) \log \left(1-h_{\theta}\left(x^{(i)}\right)\right)
\end{aligned}$$

这就是我们的**损失函数** ，然后使用梯度上升的方法(也可以取负使用梯度下降)，对参数进行更新：
$$\begin{aligned}
\frac{\partial}{\partial \theta_{j}} l(\theta)&=\left(y \frac{1}{h_{\theta}(x)}-(1-y) \frac{1}{1-h_{\theta}(x)}\right) \frac{\partial}{\partial \theta_{j}} h_{\theta}(x) \\
&=\left(\frac{y\left(1-h_{\theta}(x)\right)-(1-y) h_{\theta}(x)}{h_{\theta}(x)\left(1-h_{\theta}(x)\right)}\right) h_{\theta}(x)\left(1-h_{\theta}(x)\right) \frac{\partial}{\partial \theta_{j}} \theta^{T} x \\
&=\left(y-h_{\theta}(x)\right) x_{j}
\end{aligned}$$

最后，通过扫描样本，迭代更新参数：
$$\theta_{j}=\theta_{j}+a\left(y^{(i)}-h_{\theta}\left(x^{(i)}\right)\right) x_{j}^{(i)}$$


# 优点
1. 预测结果是界于0和1之间的概率；
2. 可以适用于连续性和类别性自变量；
3. 容易使用和解释；

# 缺点
1. 对模型中自变量多重共线性较为敏感，例如两个高度相关自变量同时放入模型，可能导致较弱的一个自变量回归符号不符合预期，符号被扭转。​需要利用因子分析或者变量聚类分析等手段来选择代表性的自变量，以减少候选变量之间的相关性；
2. 预测结果呈“S”型，因此从log(odds)向概率转化的过程是非线性的，在两端随着​log(odds)值的变化，概率变化很小，边际值太小，slope太小，而中间概率的变化很大，很敏感。 导致很多区间的变量变化对目标概率的影响没有区分度，无法确定阀值。

# 常见问题
线性函数的值越接近于正无穷大，概率值就越近1；反之，其值越接近于负无穷，概率值就越接近于0，这样的模型就是LR模型
LR本质上还是线性回归，只是特征到结果的映射过程中加了一层函数映射，即sigmoid函数，即先把特征线性求和，然后使用sigmoid函数将线性和约束至(0,1)之间，结果值用于二分或回归预测。

线性回归的应用场合大多是回归分析，一般不用在分类问题上，原因可以概括为以下两个：
1. 回归模型是连续型模型，即预测出的值都是连续值（实数值），非离散值；
2. 预测结果受样本噪声的影响比较大。

Logistic回归算法，名字虽带有回归，但其实是一个分类模型。主要用于二分类
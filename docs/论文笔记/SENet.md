

# [Squeeze-and-Excitation Networks](https://arxiv.org/pdf/1709.01507.pdf)（挤压和激励网络）

## 针对问题

1. 研究网络设计的另一个方面——通道之间的关系
2. 以前的方法认为通道关系可以被表示为具有局部接受域的与实例无关的函数的组合。

## SE结构

挤压激励块是一个计算单元，可以构造成任意给定的变换
$$
\mathbf{U}=\mathbf{F}_{t r}(\mathbf{X})\\
\mathbf{X} \in \mathbb{R}^{H^{\prime} \times W^{\prime} \times C^{\prime}}, \mathbf{U} \in \mathbb{R}^{H \times W \times C}
$$
卷积运算：$\mathbf{F}_{t r}$

卷积核：$\mathbf{V}=\left[\mathbf{v}_{1}, \mathbf{v}_{2}, \dots, \mathbf{v}_{C}\right]$

输出：$\mathbf{U}=\left[\mathbf{u}_{1}, \mathbf{u}_{2}, \dots, \mathbf{u}_{C}\right]$
$$
\mathbf{u}_{c}=\mathbf{v}_{c} * \mathbf{X}=\sum_{s=1}^{C^{\prime}} \mathbf{v}_{c}^{s} * \mathbf{x}^{s}
$$
卷积运算：*

$\mathbf{v}_{c}=\left[\mathbf{v}_{c}^{1}, \mathbf{v}_{c}^{2}, \ldots, \mathbf{v}_{c}^{C^{\prime}}\right]$

$\mathbf{X}=\left[\mathbf{x}^{1}, \mathbf{x}^{2}, \ldots, \mathbf{x}^{C^{\prime}}\right]$

二维空间核：$\mathbf{V}_{c}^{\mathcal{S}}$表示$\mathbf{V}_{c}$的一个单通道作用于$\mathbf{X}$的对应通道。

由于输出是通过对所有通道的求和产生的，所以通道依赖关系隐式地嵌入到$\mathbf{V}_{c}$中，但是与过滤器捕获的本地空间相关性纠缠在一起。因此，由卷积建模的信道关系本质上是局部的。SE块目标是确保该网络能够提高其对信息特性的敏感性，以便随后的转换能够最有效地利用这些特性，所以希望向它提供对全局信息的访问。因此通过显式地建立通道相互依赖的模型来实现这一点，从而在将滤波器响应输入下一个转换之前，按挤压和激励两个步骤重新校准滤波器响应。

![EuqpnI.png](https://s2.ax1x.com/2019/04/27/EuqpnI.png)

### 挤压

为了解决通道依赖性的问题，首先考虑输出功能中每个通道的信号。但是每个学习的过滤器利用本地接收字段操作，变换输出$\mathbf{U}$的每个单元不能利用该区域之外的上下文信息，因此将全局空间信息压缩到一个通道描述符中（通过使用全局平均池化生成通道统计数据来实现）。形式上，通过将$\mathbf{U}$缩小到其空间维度$H \times W$来生成统计量$\mathrm{z} \in \mathbb{R}^{C}$，使得z的第c个元素通过以下方式计算：
$$
z_{c}=\mathbf{F}_{s q}\left(\mathbf{u}_{c}\right)=\frac{1}{H \times W} \sum_{i=1}^{H} \sum_{j=1}^{W} u_{c}(i, j)
$$

### 激励

为了利用在挤压操作中聚合的信息，在此之后进行了第二个操作，其目的是完全捕获通道依赖关系。达到这一目的,该函数必须满足两个条件：

1. 它必须灵活(特别是,它必须有能力学习渠道之间的非线性相互作用)
2. 它必须学习一种非相互排斥的关系，因为希望确保可以强调多个通道(而不是强制执行一个热激活)。

为了满足这些条件，我们选择使用一个简单的门控机制与sigmoid激活:
$$
\mathbf{s}=\mathbf{F}_{e x}(\mathbf{z}, \mathbf{W})=\sigma(g(\mathbf{z}, \mathbf{W}))=\sigma\left(\mathbf{W}_{2} \delta\left(\mathbf{W}_{1} \mathbf{z}\right)\right)
$$
$\delta$是ReLU函数
$$\mathbf{W}_{1} \in \mathbb{R}^{\frac{C}{r} \times C}\\
\mathbf{W}_{2} \in \mathbb{R}^{C \times \frac{C}{r}}$$

为了限制模型的复杂性和辅助推广，通过在非线性周围形成两个完全连接（FC）层的瓶颈来参数化门控机制，即具有参数$\mathbf{W}_{1}$和减速比$r$和Relu的维数减少层，然后是具有参数$\mathbf{W}_{2}$的维度增加层。 通过使用激活重新调整转换输出$\mathbf{U}$来获得块的最终输出：
$$
\widetilde{\mathbf{x}}_{c}=\mathbf{F}_{\text {scale}}\left(\mathbf{u}_{c}, s_{c}\right)=s_{c} \cdot \mathbf{u}_{c}
$$
$\tilde{\mathbf{X}}=\left[\tilde{\mathbf{x}}_{1}, \widetilde{\mathbf{x}}_{2}, \ldots, \widetilde{\mathbf{x}}_{C}\right]$和$\mathbf{F}_{s c a l e}\left(\mathbf{u}_{c}, s_{c}\right)$是标量$S_{c}$与特征$\mathbf{u}_{c} \in \mathbb{R}^{H \times W}$之间的信道乘法。

[![EKWaX8.png](https://s2.ax1x.com/2019/04/27/EKWaX8.png)](https://imgchr.com/i/EKWaX8)

## 思考
### 好的地方

1. 文中说了全局信息对于实验结果的重要性
2. 通过自身产生的信息作为一种注意机制
3. 感觉和这个计算单元和残差有点像，而且很灵活，什么网络都能加
4. 而且作者做了大量的实验，这个块对于现在的分割、检测、分类都有很好的效果

### 没看懂的地方

1. 挤压和激励机制理论上为什么有用，文中也无法说明，只是用了实验来说明有效
2. 自己产生的信息作为一种注意机制，那为什么网络 就不自己学习呢？而是需要额外的运算

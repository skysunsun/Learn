

# [Dual Path Networks](https://arxiv.org/pdf/1707.01629v1.pdf)

## 研究问题

1. 探究$Resnet$的$Densenet$的优缺点
2. 怎么结合$Resnet$的$Densenet$的优点

## 短链接优劣

### 短连接更新的一般规则
![etf2se.png](https://s2.ax1x.com/2019/07/31/etf2se.png)

$h^{t}$表示递归神经网络在第$t$步的隐藏状态，用$k$作为当前步的指标。$x^{t}$表示第$t$步的输入。$f_{t}^{k}(\cdot)$为特征提取函数，该函数以隐藏状态为输入，输出提取的信息。$g^{k}(\cdot)$表示将收集到的信息转换为当前隐藏状态的转换函数
$$
h^{k}=g^{k}\left[\sum_{t=0}^{k-1} f_{t}^{k}\left(h^{t}\right)\right] \tag{1}
$$

文中说到，对于HORNN，权重是跨步共享的(没有看过这个网络不知道到底是个啥)。
$$
\forall t, k, f_{k-t}^{k}(\cdot) \equiv f_{t}(\cdot) \text { and } \forall k, g^{k}(\cdot) \equiv g(\cdot)\tag{1.1}
$$
对于Densenet,每一步都有自己的参数(因为是特征叠加)，这就意味着$f_{t}^{k}(\cdot)$ and $g^{k}(\cdot)$并没有共享，也就是$DenseNet$能够从之前的状态中提取新的信息。

对于$Resnet$文中说到如果$\forall t, k, f_{t}^{k}(\cdot) \equiv f_{t}(\cdot)$则$Resnet$是$DenseNet$的一种特殊情况。重写更新规则
$$
\begin{aligned} r^{k} & \triangleq \sum_{t=1}^{k-1} f_{t}\left(h^{t}\right)=r^{k-1}+f_{k-1}\left(h^{k-1}\right) \\ h^{k} &=g^{k}\left(r^{k}\right) \end{aligned} \tag{2}
$$
$$
r^{k}=r^{k-1}+f_{k-1}\left(h^{k-1}\right)=r^{k-1}+f_{k-1}\left(g^{k-1}\left(r^{k-1}\right)\right)=r^{k-1}+\phi^{k-1}\left(r^{k-1}\right)\tag{3}
$$
其中$\phi^{k}(\cdot)=f_{k}\left(g^{k}(\cdot)\right)$,可以看到公式3和公式1几乎是一样的

文中说到当$\forall k, \phi^{k}(\cdot) \equiv \phi(\cdot)$时（跟公式1.1类似，但是我确实是没看懂这个到底说了啥），$Resnet$就退化成了$RNN$，当$\phi^{k}(\cdot)$被共享了，则创建一个$Resnet$块。$Resnet$和$DenseNet$的计算衍生与公式1，所以作者说$Resnet$只不过是$DenseNet$的一种特殊情况。


通过这些分析作者得出两个结论：

1. 当$f_{t}^{k}(\cdot)$和$g^{k}(\cdot)$共享所有$k$时，剩余网络和密集连接网络都可以看作一个HORNN
2. 残差网络是密集连通网络，如果$\forall t, k, f_{t}^{k}(\cdot) \equiv f_{t}(\cdot)$。通过跨所有步骤共享$f_{t}^{k}(\cdot)$，$g^{k}(\cdot)$从给定的输出状态接收相同的特性，这就是特征的重用，从而减少了特性冗余。然而，这种信息共享策略使得残差网络难以探索新特性。相对而言，由于$f_{t}^{k}(\cdot)$不是跨步骤共享的，密集连接网络能够从以前的输出中探索新的信息。但是，不同的$g^{k}(\cdot)$可能会多次提取同一类型的特征，导致冗余度高。

神经网络到底提到了啥特征，我们也不知道，作者用了一句**可能**（好心酸啊）针对这两个问题，也就有了接下来的故事了

## 架构
![et4jCq.png](https://s2.ax1x.com/2019/07/31/et4jCq.png)
提出了一个简单的双路径结构，它在所有块上共享$f_{t}^{k}(\cdot)$，以享受重用具有低冗余的公共特性的好处，同时仍然保持紧密连接的路径，使网络在学习新特性时具有更大的灵活性。

$$x^{k} \triangleq \sum_{t=1}^{k-1} f_{t}^{k}\left(h^{t}\right) \tag{5}$$
$$y^{k} \triangleq \sum_{t=1}^{k-1} v_{t}\left(h^{t}\right)=y^{k-1}+\phi^{k-1}\left(y^{k-1}\right) \tag{6}$$
$$r^{k} \triangleq x^{k}+y^{k}\tag{7}$$
$$h^{k}=g^{k}\left(r^{k}\right)\tag{8}$$
公式5为密连的特征提取，公式6为残差的特征提取，然后把他们加起来，再用一个特征提取送入下一层

网络是用$Resnet$作为基础骨架，然后再加一个窄的$DenseNet$，但是从作者给出的参数图来看，参数少了，所以作者用的$Resnet$骨架和对比的骨架肯定不是一个骨架了，至于到底用了那个骨架还得看代码


两者提的特征相加，然后用相同的卷积计算（节约主要是这里吧），然后结尾再分开，回到自己的流上面，这个网络结构图看的我有点脑壳痛。。。。。。。

## 思考

两种网络的结合，然后还把参数降下来了，的确是篇好文章呀，但是刚开始的分析还是没怎么看懂，虽然大致明白作者想表达啥，哎！还是数学的锅！

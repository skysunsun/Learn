




# [Expectation-Maximization Attention Networks for Semantic Segmentation](https://arxiv.org/pdf/1907.13426.pdf)
我觉得这句话总结的挺好的
> Self-attention mechanism has been widely used for various tasks. It is designed to compute the representation of each position by a weighted sum of the features at all positions.

## 研究问题

1. 语义分割
2. 注意机制的计算花费问题

## 语义分割问题

文中分析了语义分割的难点在于实景的多样性，但是数据集却是受限制的（只有几类）



语义分割可以看作是将高维噪声空间中的数据点投影到一个紧凑的子空间中。其本质在于去噪这些变化和捕捉最重要的语义概念（对于语义分割的理解）

### 目前语义分割的方法

1. 全卷积神经网络（FCN）
2. DeepLab系列（膨胀卷积的使用）
3. PSPNet(金字塔池化)
4. GCN(大卷积核)
5. U-Net系列（融合高低层次特征）
6. 注意力机制

## EM算法

假设数据$X=\left\{{x}_{1}, {x}_{2}, \cdots, {x}_{N}\right\}$对应隐变量$Z=\left\{{z}_{1}, {z}_{2}, \cdots, {z}_{N}\right\}$

期望最大化（EM）算法旨在为隐变量模型寻找最大似然解，似然函数为$\ln p({X}, {Z} | {\theta})$
在E步中，根据已知$Z$的后验分布求出整个数据集的似然解
$$\mathcal{Q}\left(\boldsymbol{\theta}, \boldsymbol{\theta}^{\text {old }}\right)=\sum_{\boldsymbol{z}} p\left(\mathbf{Z} | \mathbf{X}, \boldsymbol{\theta}^{\text {old }}\right) \ln p(\mathbf{X}, \mathbf{Z} | \boldsymbol{\theta}) \tag1$$
在M步中，求出E步中最大的似然解
$$\boldsymbol{\theta}^{\text {new }}=\underset{\boldsymbol{\theta}}{\arg \max } \mathcal{Q}\left(\boldsymbol{\theta}, \boldsymbol{\theta}^{\text {old }}\right) \tag2$$
文中谈到EM算法已经被证明会收敛到局部最大值

### 高斯混合模型

其为EM算法的一种变种
$$
p\left(\mathbf{x}_{n}\right)=\sum_{k=1}^{K} z_{n k} \mathcal{N}\left(\mathbf{x}_{n} | \boldsymbol{\mu}_{k}, \mathbf{\Sigma}_{k}\right) \tag3
$$
这里把参数换为高斯核的均值和方差（$\theta:{\mu}_{k}, \mathbf{\Sigma}_{k}$）

则整个数据的似然计算公式为：
$$
\ln p(\mathbf{X}, \mathbf{Z} | \boldsymbol{\mu}, \boldsymbol{\Sigma})=\sum_{n=1}^{N} \ln \left[\sum_{k=1}^{K} z_{n k} \mathcal{N}\left(\mathbf{x}_{n} | \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)\right] \tag4
$$
其中$\sum_{k} z_{n k}=1$，$ z_{n k}$为第$k$个核的权重

对于E步的更新
$$
z_{n k}^{\mathrm{new}}=\frac{\mathcal{N}\left(\mathbf{x}_{n} | \boldsymbol{\mu}_{k}^{\mathrm{new}}, \mathbf{\Sigma}_{k}\right)}{\sum_{j=1}^{K} \mathcal{N}\left(\mathbf{x}_{n} | \boldsymbol{\mu}_{j}^{\mathrm{new}}, \mathbf{\Sigma}_{j}\right)}\tag5
$$
这不是$softmax$函数么。。。。。

对于M步的更新
$$
\begin{aligned} \boldsymbol{\mu}_{k}^{\text {new }} &=\frac{1}{N_{k}} \sum_{n=1}^{N} z_{n k}^{\text {new }} \mathbf{x}_{n} \\ \boldsymbol{\Sigma}_{k}^{\text {new }} &=\frac{1}{N_{k}} \sum_{n=1}^{N} z_{n k}^{\text {new }}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{k}^{\text {old }}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{k}^{\text {old }}\right)^{\top} \end{aligned} \tag7
$$
最后
$$
\mathbf{x}_{n}^{\mathrm{new}}=\sum_{k=1}^{K} z_{n k}^{\mathrm{new}} \boldsymbol{\mu}_{k}^{\mathrm{new}}\tag8
$$

## 非局部模型
$$
\mathbf{y}_{i}=\frac{1}{\mathcal{C}\left(\mathbf{x}_{i}\right)} \sum_{j} f\left(\mathbf{x}_{i}, \mathbf{x}_{j}\right) g\left(\mathbf{x}_{j}\right)\tag9
$$

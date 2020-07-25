# 支持向量机

考虑一个二分类问题，我需要寻找一个超平面把数据分为正类和负类，对于线性可分的数据集来说，这样的超平面$wx+b=0$有无穷多个（即感知机），但是几何间隔最大的分离超平面却是唯一的。SVM算法的目的就是求这个唯一的超平面

![eddfcc_1200x500.jpg](https://pic3.zhimg.com/v2-197913c461c1953c30b804b4a7eddfcc_1200x500.jpg)
## SVM求解过程
### 构造问题
**函数间隔：** 对于给定的训练数据集$T$和超平面$(w, b)$，定义超平面$(w, b)$关于样本点 $\left(x_{i}, y_{i}\right)$ 的函数间隔为
$$\hat{\gamma}_{i}=y_{i}\left(w \cdot x_{i}+b\right)$$
如果等比例的改变$w,b$会发现超平面没变但函数间隔变了，所以有了几何间隔

**几何间隔：** 对于给定的训练数据集$T$和超平面$(w, b)$，定义超平面$(w, b)$关于样本点 $\left(x_{i}, y_{i}\right)$ 的几何间隔为
$$
\gamma_{i}=\frac{w}{\|w\|} \cdot x_{i}+\frac{b}{\|w\|}
$$
**SVM的目的就是求几何间隔最大的分离超平面，可以转化为如下的约束优化问题**

$$\begin{array}{cl}
\max \limits_{w, b} & \gamma \\
\text { s.t. } & y_{i}(\frac{w}{\|w\|} \cdot x_{i}+\frac{b}{\|w\|}) \geqslant \gamma, \quad i=1,2, \cdots, N
\end{array}$$

考虑函数间隔和几何间隔的关系$\gamma=\frac{\hat{\gamma}}{\|\boldsymbol{w}\|}$，改写上面的公式
$$\begin{array}{ll}
\max \limits_{w,b} & \frac{\hat{\gamma}}{\|w\|} \\
\text { s.t. } & y_{i}\left(w \cdot x_{i}+b\right) \geqslant \hat{\gamma}, \quad i=1,2, \cdots, N
\end{array}$$

假设将$w$和$b$按比例改变为$\lambda w$和$\lambda b$，这时函数间隔成为$\lambda \hat\gamma$。函数间隔的这一改变对上面最优化问题的不等式约束没有影响，对目标函数的优化也没有影响，这样，就可以取$\gamma=1$。将$\gamma=1$代入上面的最优化问题，而最大化$\frac{1}{\|w\|}$和最小化$\frac{1}{2}{\|w\|}^2$是等价的，于是就得到下面的线性可分支持向量机学习的最优化问题：

$$\begin{array}{cl}
\min \limits_{w, b} & \frac{1}{2}{\|w\|}^2 \\
\text { s.t. } & y_{i}\left(w \cdot x_{i}+b\right)-1 \geqslant 0, \quad i=1,2, \cdots, N
\end{array}$$

构建拉格朗日函数，对每一个不等式引进拉格朗日乘子$\alpha_{i} \geqslant 0, i=1,2, \cdots, N$：
$$L(w, b, \alpha)=\frac{1}{2}\|w\|^{2}-\sum_{i=1}^{N} \alpha_{i} y_{i}\left(w \cdot x_{i}+b\right)+\sum_{i=1}^{N} \alpha_{i}$$
根据拉格朗日对偶性，原问题的对偶问题为极大极小问题
$$\max _{\alpha} \min _{w, b} L(w, b, \alpha)$$
- 先求极小值$\min\limits_{w, b} L(w, b, \alpha)$
将拉格朗日函数 $L(w,b, \alpha)$ 分别对 $w, b$ 求偏导数并令其等于 0
$$\begin{aligned}
\frac{\partial L}{\partial w}=& w-\sum_{i=1}^{N} \alpha_{i} y_{i} x_{i}=0 \Rightarrow w=\sum_{i=1}^{N} \alpha_{i} y_{i} x_{i} \\
\frac{\partial L}{\partial b}=&-\sum_{i=1}^{N} \alpha_{i} y_{i}=0 \Rightarrow \sum_{i=1}^{N} \alpha_{i} y_{i}=0
\end{aligned}$$
将$w$代入$L(w,b, \alpha)$ 
$$\begin{aligned} L(w, b, \alpha) &=\frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j}\left(x_{i} \cdot x_{j}\right)-\sum_{i=1}^{N} \alpha_{i} y_{i}\left(\left(\sum_{j=1}^{N} \alpha_{j} y_{j} x_{j}\right) \cdot x_{i}+b\right)+\sum_{i=1}^{N} \alpha_{i} \\ &=-\frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j}\left(x_{i} \cdot x_{j}\right)+\sum_{i=1}^{N} \alpha_{i} \end{aligned}$$
即 
$$\min _{w, b} L(w, b, \alpha)=-\frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j}\left(x_{i} \cdot x_{j}\right)+\sum_{i=1}^{N} \alpha_{i}$$
- 再求 $\min \limits_{w, b} L(w, b, \alpha)$ 对 $\alpha$ 的极大
$$
\begin{array}{ll}
\max \limits_{\alpha} & -\frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j}\left(x_{i} \cdot x_{j}\right)+\sum_{i=1}^{N} \alpha_{i} \\
\text { s.t. } & \sum_{i=1}^{N} \alpha_{i} y_{i}=0 \\
& \alpha_{i} \geqslant 0, \quad i=1,2, \cdots, N
\end{array}
$$
目标函数由求极大转换成求极小，就得到下面与之等价的对偶问题：
$$
\begin{array}{ll}
\min \limits_{\alpha} & \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j}\left(x_{i} \cdot x_{j}\right)-\sum_{i=1}^{N} \alpha_{i} \\
\text { s.t. } & \sum_{i=1}^{N} \alpha_{i} y_{i}=0 \\
& \alpha_{i} \geqslant 0, \quad i=1,2, \cdots, N
\end{array}
$$

### 求解问题
- 求得最优解 $\alpha^{*}=\left(\alpha_{1}^{*}, \alpha_{2}^{*}, \cdots, \alpha_{N}^{*}\right)^{\mathrm{T}}$
- 计算出$w$
$$
w^{*}=\sum_{i=1}^{N} \alpha_{i}^{*} y_{i} x_{i}
$$
- 计算$b$
并选择 $\alpha^{*}$ 的一个正分量 $\alpha_{j}^{*}>0,$ 计算
$$\begin{array}{cl}
y_{j}\left(w^{*} \cdot x_{j}+b^{*}\right)-1=0\\
y_{j}\left(w^{*} \cdot x_{j}+b^{*}\right)-y_{j}^{2}=0\\
b^{*}=y_{j}-\sum_{i=1}^{N} \alpha_{i}^{*} y_{i}\left(x_{i} \cdot x_{j}\right)
\end{array}$$


- 进而得到超平面
$$
w^{*} \cdot x+b^{*}=0
$$



## 对偶问题优点

1. 对偶问题更容易求解
2. 自然引入核函数,进而推广到非线性问题




# Boosting

Boosting则是一种集成学习模式，通过将多个单个决策树(弱学习器)进行线性组合构成一个强学习器的过程，
一个提升树模型可以描述为：
$$\begin{aligned}
&\hat{y}_{i}^{0}=0\\
&\hat{y}_{i}^{1}=f_{1}\left(x_{i}\right)=\hat{y}_{i}^{0}+f_{1}\left(x_{i}\right)\\
&\hat{y}_{i}^{2}=f_{1}\left(x_{i}\right)+f_{2}\left(x_{i}\right)=\hat{y}_{i}^{1}+f_{2}\left(x_{i}\right)\\
&...\\
&\hat{y}_{i}^{K}=\sum_{k=1}^{K} f_{k}\left(x_{i}\right)=\hat{y}_{i}^{k-1}+f_{k}\left(x_{i}\right)
\end{aligned}$$

我们的目标一般是求**目标值$y_i$与预测值$\hat y_i$之间的最小值**即：
$$\begin{aligned}
L^{(k)}&=\sum_{i=1}^{n} l\left(y_{i}, \hat{y}_{i}\right)\\
&=\sum_{i=1}^{n} l(y_i,\hat{y}_{i}^{k-1}+f_{k}(x_{i}))
\end{aligned}$$

如何去求解每一个模型就衍生出了不同方法



# AdaBoost

# 梯度提升决策树GBDT(Gradient Boosting Decision Tree)

大牛Freidman提出了用损失函数的负梯度来拟合本轮损失的近似值，进而拟合一个$Cart$回归树。
$$\hat{y}_{i}^{K}=\hat{y}_{i}^{k-1}+f_{k}\left(x_{i}\right)$$
在集成学习中要最小化损失函数
$$L^{(K)}=\sum_{i=1}^{n} l(y_i,\hat{y}_{i}^{k-1}+f_{k}(x_{i}))$$
回想下梯度下降的形式
$$\theta^{(k)}=\theta^{(k-1)}-\eta \frac{\partial L}{\partial \theta^{k-1}}$$
跟这棵树的形式$\hat{y}_{i}^{K}=\hat{y}_{i}^{k-1}+f_{k}\left(x_{i}\right)$基本一模一样，所以要求得最优的$f_k(x_i)$,直接对应一下就是
$$f_k(x_i)=-\eta\frac{\partial L(y_{i}, \hat{y}_{i}^{k-1}))}{\partial\hat{y}_{i}^{k-1}}$$
最后建成的树
$$\begin{aligned}
F(x)&=\hat{y}_{i}^{K}\\
&=\hat{y}_{i}^{k-1}+f_{k}\left(x_{i}\right)\\
&=\sum_{k=1}^{K} f_{k}\left(x_{i}\right)\\
&=-\eta\sum_{k=1}^{K}\frac{\partial L(y_{i}, \hat{y}_{i}^{k-1}))}{\partial\hat{y}_{i}^{k-1}}
\end{aligned}$$
也就是负梯度累加
## 算法流程：
1. 算法每次迭代生成一颗新的决策树;
2. 计算损失函数在每个训练样本点的负梯度生成新的决策树$f_k(x)$;
4. 把新生成的决策树$f_k(x)$加入$\hat y_i^k=\hat y_i^{k-1}+ f_{k}\left(x_{i}\right)$

# [XGBoost: A Scalable Tree Boosting System](https://www.kdd.org/kdd2016/papers/files/rfp0697-chenAemb.pdf)
然而一个好的模型，在偏差和方差上要有一个较好的平衡，损失函数代表了模型的偏差面，最小化损失函数，就相当于最小化模型的偏差，但同时要考虑模型的泛化能力即方差,所以要兼顾模型的方差，所以作者直接在损失函数中加入了正则项抑制模型复杂度的正则项，因此损失函数可以写成：
$$\begin{aligned}
L^{(k)}&=\sum_{i=1}^{n} l\left(y_{i}, \hat{y}_{i}\right)+\sum_{k=1}^{K} \Omega\left(f_{k}\right)\\
&=\sum_{i=1}^{n} l(y_i,\hat{y}_{i}^{k-1}+f_{k}(x_{i}))+\Omega(f_{k})+constant\tag 1
\end{aligned}$$
其中$\Omega$代表了基模型的复杂度，比如树的深度、叶子节点数等等。这里$\Omega\left(f_{k}\right)=\gamma T+\frac{1}{2} \lambda \sum_{j=1}^{T} w_{j}^{2}$，

泰勒公式二阶展开

$$f(x+\Delta x) \approx f(x)+f^{\prime}(x) \Delta x+\frac{1}{2} f^{\prime \prime}(x) \Delta x^{2}\tag2$$
把(1)式中的$\hat{y}_{i}^{k-1},f_k(x_i)$看成(2)式中的$x,\Delta x$：
$$L^{(k)}=\sum_{i=1}^{n}\left[l\left(y_{i}, \hat{y}_{i}^{k-1}\right)+{\hat{y}_{i}^{k-1}}'f_{k}\left(x_{i}\right)+\frac{1}{2}{\hat{y}_{i}^{k-1}}'' f_{k}^{2}\left(x_{i}\right)\right]+\Omega\left(f_{k}\right)+constant \tag3$$
令${\hat{y}_{i}^{k-1}}'=g_i，{\hat{y}_{i}^{k-1}}''=h_i$则


$$L^{(k)}=\sum_{i=1}^{n}\left[l\left(y_{i}, \hat{y}_{i}^{k-1}\right)+g_if_{k}\left(x_{i}\right)+\frac{1}{2}h_i f_{k}^{2}\left(x_{i}\right)\right]+\Omega\left(f_{k}\right)+constant \tag4$$

因为$\hat{y}_{i}^{k-1}$上一棵树已经算出来了，所以$l\left(y_{i}, \hat{y}_{i}^{k-1}\right)$为常数,(4)式可以写成：
$$\begin{aligned}
L^{(k)} &\approx \sum_{i=1}^{n}\left[g_{i} f_{k}\left(x_{i}\right)+\frac{1}{2} h_{i} f_{k}^{2}\left(x_{i}\right)\right]+\Omega\left(f_{k}\right) \\
&=\sum_{i=1}^{n}\left[g_{i} f_{k}\left(x_{i}\right)+\frac{1}{2} h_{i} f_{k}^{2}\left(x_{i}\right)\right]+\gamma T+\frac{1}{2} \lambda \sum_{j=1}^{T} w_{j}^{2} \\
&=\sum_{j=1}^{T}\left[\left(\sum_{i \in I_{j}} g_{i}\right) w_{j}+\frac{1}{2}\left(\sum_{i \in I_{j}} h_{i}+\lambda\right) w_{j}^{2}\right]+\gamma T
\end{aligned} \tag5$$

其中$G_{j}=\sum_{i \in I_{j}} g_{i}, H_{j}=\sum_{i \in I_{j}} h_{i}$，假设树的结构固定，令函数$L^{(k)}$ 对$w$的导数等于0(凸函数导数为0取极值), 即可求得叶子节点 $j$ 对应的值为:

$$w_{j}^{*}=-\frac{G_{j}}{H_{j}+\lambda}$$
把$w_{j}^{*}$带进去，此时，损失函数的值为:
$$L=-\frac{1}{2} \sum_{j=1}^{T} \frac{G_{j}^{2}}{H_{j}+\lambda}+\gamma T \tag6$$
那么分裂分裂之前的损失
$$-\frac{1}{2}\left[\frac{\left(G_{L}+G_{R}\right)^{2}}{H_{L}+H_{R}+\lambda}\right]+\gamma$$
分裂之后的损失：
$$-\frac{1}{2}\left[\frac{G_{L}^{2}}{H_{L}+\lambda}+\frac{G_{R}^{2}}{H_{R}+\lambda}\right]+2 \gamma$$
则对于损失函数来说，分裂后的收益是（这里假设是最小化损失函数，所以用分裂前-分裂后）：
$$\text {Gain}=\frac{1}{2}\left[\frac{G_{L}^{2}}{H_{L}+\lambda}+\frac{G_{R}^{2}}{H_{R}+\lambda}-\frac{\left(G_{L}+G_{R}\right)^{2}}{H_{L}+H_{R}+\lambda}\right]-\gamma \tag7$$
## 算法流程
1. 算法每次迭代生成一颗新的决策树 ;
2. 在每次迭代开始之前，计算损失函数在每个训练样本点的一阶导数$g_i$和二阶导数$h_i$;
3. 通过贪心策略生成新的决策树，通过式(7) 计算每个叶节点对应的预测值$w$
4. 把新生成的决策树$f_k(x)$加入$\hat y_i^k=\hat y_i^{k-1}+\eta f_{k}\left(x_{i}\right)$,$\eta$为学习率


# [LightGBM:A Highly Efficient Gradient Boosting Decision Tree](https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree.pdf)

对xgb的优化

1. 基于Histogram的决策树算法
2. 带深度限制的Leaf-wise的叶子生长策略
3. 直方图做差加速
4. 支持类别特征
5. Cache命中率优化
6. 基于直方图的稀疏特征多线程优化

# 区别
1. XGBoost生成CART树考虑了树的复杂度，GDBT未考虑，GDBT在树的剪枝步骤中考虑了树的复
杂度。
2. XGBoost是拟合上一轮损失函数的二阶导展开，GDBT是拟合上一轮损失函数的一阶导展开，因
此，XGBoost的准确性更高，且满足相同的训练效果，需要的迭代次数更少。
3. XGBoost与GDBT都是逐次迭代来提高模型性能，但是XGBoost在选取最佳切分点时可以开启多
线程进行，大大提高了运行速度。

4. 基于残差的gbdt在解决回归问题上不算是一个好的选择，一个比较明显的缺点就是对异常值过于敏感。

5. GBDT的非线性变换比较多，表达能力强，而且不需要做复杂的特征工程和特征变换。
6. GBDT是一个串行过程，不好并行化，而且计算复杂度高，同时不太适合高维稀疏特征；

7. xgb实现了分裂点寻找近似算法。
8. xgb利用了特征的稀疏性。
9. xgb数据事先排序并且以 block 形式存储，有利于并行计算。
10. xgb基于分布式通信框架 rabit，可以运行在 MPI 和 yarn 上。（最新已经不基于 rabit 了）
11. xgb实现做了面向体系结构的优化，针对 cache 和内存做了性能优化。
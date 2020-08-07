
**大数定律：** 样本均值收敛到总体均值

**中心极限定理：** 样本量足够大时，样本均值的分布慢慢变成正态分布

**条件概率：** 事件B发生条件下事件A发生的概率为$P(A|B)=\frac{P(AB)}{P(B)}$

**贝叶斯公式：** 贝叶斯公式是关于事件A和B的条件概率的一则定理：$P(B|A)=\frac{P(A|B)P(B)}{P(A)}$

**先验概率：** 在事件发生之前，根据以往的经验推测的与该事件相关的概率

**后验概率：** 在事件(试验)真正发生后，通过事件(试验)的结果可以修正先验概率，从而得到后验概率


若随机变量$X$和$Y$，$X$是因，$Y$是结果，那么$P(X)$ 叫做先验概率$prior$;$P(Y)$叫做$evidence$;$P(X|Y)$叫做后验概率$posterior$;$P(Y|X)$叫做似然$likelihood$

**我们可以看到，这里的似然和条件概率其实是一样的。但是两者还是有区别的:**


要看这个公式是似然还是概率，那么你需要看把那个量当做是变量。当你把$X$当做是变量，而$Y$是已经发生的常量的时候，它说的是似然，那么这个表达式说的是：在$X$（变量）的条件下$Y$已经发生这件事情的可能性。当你把$X$当做常量（已经确定了），而$Y$当做变量（即将要发生），它说的是条件概率，那么这个表达式说的是：在$X$的条件下$Y$将要发生的可能性。所以这个公式是一体两面，在计算的时候它们两个的值是相等的。

# 朴素贝叶斯
朴素贝叶斯法通过训练数据集学习联合概率分布 $P(X, Y)$ 。学习以下先验概率分布及条件概率分布。先概率分布
$$
P\left(Y=c_{k}\right), \quad k=1,2, \cdots, K
$$

条件概率分布
$$
P\left(X=x | Y=c_{k}\right)=P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} | Y=c_{k}\right), \quad k=1,2, \cdots, K
$$
进而得到联合概率分布$$\begin{aligned}
P\left(X=x, Y=C_{k}\right) &=P\left(Y=C_{k}\right) P\left(X=x | Y=C_{k}\right) \\
&=P\left(Y=C_{k}\right) P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)}=x_{n} | Y=C_{k}\right)
\end{aligned}$$

**因为条件概率分布 $P\left(X=x | Y=c_{k}\right)$ 有指数级数量的参数，其估计实际是不可行的。 所以朴素贝叶斯法对条件概率分布作了条件独立性的假设。由于这是一个较强的假设，朴素贝叶斯法也由此得名。** 
条件独立性假设是：
$$\begin{aligned}
P\left(X=x | Y=c_{k}\right) &=P\left(X^{(1)}=x^{(1)}, \cdots, X^{(n)}=x^{(n)} | Y=c_{k}\right) \\
&=\prod_{j=1}^{n} P\left(X^{(j)}=x^{(j)} | Y=c_{k}\right) \tag1
\end{aligned}$$

朴素贝叶斯法分类时，对给定的输入$x$，通过学习到的模型计算后验概率分布$P\left(Y=c_{k} | X=x\right),$ 将后检概率最大的类作为 $x$ 的类输出。根据贝叶斯公式得：
$$
P\left(Y=c_{k} | X=x\right)=\frac{P\left(X=x | Y=c_{k}\right) P\left(Y=c_{k}\right)}{ P\left(X=x\right)} \tag 2 
$$
因为$\sum_{k} P\left(Y={c_k}\right)=1$(类别概率总和为1),根据全概率公式有$P(X=x)=\sum_{k} P\left(X=x | Y=c_{k}\right) P\left(Y=c_{k}\right)$所以
$$
P\left(Y=c_{k} | X=x\right)=\frac{P\left(X=x | Y=c_{k}\right) P\left(Y=c_{k}\right)}{\sum_{k} P\left(X=x | Y=c_{k}\right) P\left(Y=c_{k}\right)} \tag 3
$$

将式 (1) 代入式 (3)，有
$$\begin{aligned}
P(Y=c_{k})|X=x)= \frac{P(Y=c_{k})\prod\limits_{j} P(X^{(j)}=x^{(j)} | Y=c_{k})}{\sum\limits_{k} P\left(Y=c_{k}\right) \prod\limits_{j} P\left(X^{(j)}=x^{(j)} | Y=c_{k}\right)}, \quad k=1,2, \cdots, K
\end{aligned}$$
这是朴素贝叶斯法分类的基本公式。于是，朴素贝叶斯分类器可表示为

$$
y=f(x)=\arg \max _{c_{k}} \frac{P\left(Y=c_{k}\right) \prod\limits_{j} P\left(X^{(j)}=x^{(j)} | Y=c_{k}\right)}{\sum_{k} P\left(Y=c_{k}\right) \prod\limits_{j} P\left(X^{(j)}=x^{(j)} | Y=c_{k}\right)} \tag 4
$$

注意到，在式 (4) 中分母对所有 $c_{k}$ 都是相同的，所以
$$
y=\arg \max _{c_{k}} P\left(Y=c_{k}\right) \prod_{j} P\left(X^{(j)}=x^{(j)} | Y=c_{k}\right)
$$
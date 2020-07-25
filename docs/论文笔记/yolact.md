
# [YOLACT Real-time Instance Segmentation](https://arxiv.org/pdf/1904.02689.pdf)

## 研究问题

1. 实时的实例分割
2. NMS

## 网络结构

![nRhlGQ.png](https://s2.ax1x.com/2019/09/16/nRhlGQ.png)
作者在FPN上做了改动，但是我们有看过FPN呀....（回头找来看看）

主要是在目标检测模型中加入Mask分支

1. FCN生成最原始的掩码
2. 原始掩码组合为最终的掩码

模型为什么速度慢？因为一般的网络是串行的？后面的必须等前面的，所以作者把后面那部分提前了（和前面那部分一起做并行），具体就是（卷积生成一组Mask，全连接层生成Mask系数）我怎么感觉有点Attention的味道

在生成初始的Mask部分，作者提到一个设计原则：

1. 更深的网络，效果更好
2. 分辨率高对小目标效果好

刚才提到作者是要在目标检测的基础上加上Mask分支，所以最后在算的时候同样加了Mask分支的计算（目标检测是（4个回归框+C个类别）这里为（4个回归框+C个类别+Mask系数））。
![nWs410.png](https://s2.ax1x.com/2019/09/16/nWs410.png)
这张图完美诠释了区别呀！

从最终的Mask减去初始的Mask（这部分，有点懵逼）

然后Mask和Mask系数相乘就得到最后的Mask了，之后加了个sigmoid函数，实例分割不是很多类么？加sigmoid？？


### 损失函数

损失函数是边框+类别+Mask的组合损失，其中Mask用到了BCE（按道理这里不是CE么？为啥是二分类交叉熵呀？）


>as the general consensus around instance segmentation is that because FCNs are translation invariant, the task needs translation variance added back in

![nWHQVs.png](https://s2.ax1x.com/2019/09/16/nWHQVs.png)

作者谈到因为FCN的变换不变性（相同输入会得到一样的结果）需要改变，FCIS和Msak R-CNN把这部分的处理放在了第二阶段，YOLACT则在第一部分就学习到了

通过零值的填充就改变了这个不变性（这个不是每个网络都有的么？？？）

上图的可视化说明了网络能够把一张图片分区（好像是这样啊，至少每个特征是不一样的）然后网络就能够区分了，而且学习到每个特征的系数


## Fast NMS(non maximum suppression)非极大值抑制

复习下NMS步骤：

在目标检测任务中，我们会生成很多的框，但是我们只需要一个框，这时就要用到NMS了

1. 将所有框的得分排序，选出得分最高的
2. 遍历其余的框，如果和当前最高分框的重叠面积(IOU)大于一定阈值，我们就将框删除。
3. 从未处理的框中继续选一个得分最高的，重复上述过程。

可以看到这个是个串行的过程，那么本文的fast体现在什么地方呢?

作者把第二步删除的框用于下一步的抑制（这样就可以并行第二步了）


感觉这篇文章就是把之前工作的一部分串行操作弄成了并行操作，这样肯定是可以提高效率的！而且这篇文章读下来感觉像在做考研阅读！

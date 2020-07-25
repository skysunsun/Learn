
# [V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation](https://arxiv.org/pdf/1606.04797.pdf)

## 研究问题

1. 医学3D图像分割
2. 数据中样本不平衡问题

## 网络结构

![nPKtaQ.png](https://s2.ax1x.com/2019/09/02/nPKtaQ.png)

这个网络使用的是3D卷积（瞅了半天才想起有个3D卷积），全程使用residual结构。卷积部分使用$5\times5\times5$的卷积核，下采样使用步长为2的$2\times2\times2$卷积核，每个卷积块之后同样是特征空间维度缩小一半，空间维度增加一倍；（文中谈到使用卷积代替maxpool能够节省内存，因为这样在反向传播中不用去找这个映射）
上采样使用的是使用步长为2的$2\times2\times2$反卷积，而从图中看，这部分的residual没有加之前的卷积的部分

类似U-Net的结构，使用了3D卷积和residual模块，而在卷积核的尺寸方面倒是有点意思，一般都是用的3，很少看到用2的，而且这个网络最后输出的是深度为2的特征图。

## Dice_Loss

目标太小，导致网络直接把目标预测为背景，针对这个问题，之前有样本权重损失，（即目标比背景更加重要，比如Focal_Loss），作者提出新的损失函数：
$$D=\frac{2 \sum_{i}^{N} p_{i} g_{i}}{\sum_{i}^{N} p_{i}^{2}+\sum_{i}^{N} g_{i}^{2}}$$
其中$N$为像素点，$p$为预测图，$g$为真值，这是个可导函数，对其求导：
$$
\frac{\partial D}{\partial p_{j}}=2\left[\frac{g_{j}\left(\sum_{i}^{N} p_{i}^{2}+\sum_{i}^{N} g_{i}^{2}\right)-2 p_{j}\left(\sum_{i}^{N} p_{i} g_{i}\right)}{\left(\sum_{i}^{N} p_{i}^{2}+\sum_{i}^{N} g_{i}^{2}\right)^{2}}\right]
$$
这样就不必去找数据中的正负样本的平衡点了

但是这个是如何平衡样本不均衡的呢？

### 我觉得是这样的

二分类问题，预测非零即一，从上面的函数中，我们可以看到，我们需要最大化D，就需要预测准确，如果预测不正确，那个点分子就为0了，这样就和我们要最大化D矛盾，所以预测准确，这样就能最大化D，每一个样本都是如此，就不必去考虑样本到底是怎么样的，到底是不是不均衡

最后，由于医学图像的数据的缺少，作者做了数据增强（随机转换）

## 代码

```python
import torch.nn as nn
import torch.nn.functional as F

class SoftDiceLoss(nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(SoftDiceLoss, self).__init__()
 
    def forward(self, logits, targets):
        num = targets.size(0)
        smooth = 1
        
        probs = F.sigmoid(logits)
        m1 = probs.view(num, -1)
        m2 = targets.view(num, -1)
        intersection = (m1 * m2)
 
        score = 2. * (intersection.sum(1) + smooth) / (m1.sum(1) + m2.sum(1) + smooth)
        score = 1 - score.sum() / num
        return score
```
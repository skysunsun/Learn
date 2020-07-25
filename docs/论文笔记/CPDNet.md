

# [Cascaded Partial Decoder for Fast and Accurate Salient Object Detection](https://arxiv.org/pdf/1904.08739.pdf)（级联部分解码器）

## 针对问题

1. 深层特征和浅层特征融合，效果提升不是很明显
2. 深层特征和浅层特征融合，加重了计算负担

## 模型结构

如作者所说，显著性检测本身就是一个数据的预处理阶段，这只是图像处理的基础，所以这个一步的操作必须要快。因为后面还有其他的操作等着处理。
![V60xxO.png](https://s2.ax1x.com/2019/06/10/V60xxO.png)
可以看到这个又是一个双流网络，文中用到了VGG-16的5个卷积块，先用3,4,5这三个块的特征融合输入到级联解码器生成$S_{i}$，然后把$S_{i}$输入全面注意模块生成$S_{h}$，然后用$S_{h}$结合另一个VGG-16的第三个，生成第四个卷积块，接着前向传生成第五个卷积块，最后结合3,4,5到级联解码器生成$S_{d}$。~~(文中说到双流网络不共享权重，而图是这样画的，不知道是不是和图中的一样共享前三个卷积的权重，后面的各自算自己的)~~
看了作者代码，确实是共享了前三块。后面的分开算。

### 损失函数
$$
\begin{array}{c}{L_{\text {total}}=L_{c e}\left(S_{i}, l | \Theta_{i}\right)+L_{c e}\left(S_{d}, l | \Theta_{d}\right)} \\   {\qquad L_{c e}(\Theta)=-\sum_{j=1}^{N} \sum_{c \in\{0,1\}} \delta\left(l^{j}=c\right) \log p\left(S^{j}=c | \Theta\right)}\end{array}
$$
其中$N$为图像中像素的个数，$\delta$是指标函数，$j$为像素坐标，$\Theta=\left\{\Theta_{i}, \Theta_{d}\right\}$是与显著性图$S=\left\{S_{i}, S_{d}\right\}$对应的参数集。

### 整体注意模块

这个模块的作用主要是**扩大初始显著图的覆盖范围**
$$
S_{h}=M A X\left(f_{\min -\max }\left(\operatorname{Conv}_{g}\left(S_{i}, k\right)\right), S_{i}\right)
$$
其中$C o n v_{g}$为K（文中取大小为32，标准差为4）个高斯核的卷积（偏置为0），$f_{m i n_{-} m a x}(\cdot)$为正则化，文中说到卷积会模糊显著性图，所以用了一个$MAX$函数。

### 级联解码器

由于是一个双流模型，所以文中想要加速运算，不然和其他的模型同样面对计算任务重的问题。受RFB(这个是个啥？)启发，设计了一个上下文模块，一共四个分支，每个分支用$1 \times 1$卷积把通道缩小到32，对于2,3,4个分支添加了两个膨胀卷积卷积大小分别为$(2 m-1) \times(2 m-1)$和$3 \times 3$，膨胀率为$(2 m-1)$。然后把这些输出连接起来，用$1 \times 1$卷积缩小通道数到32。设置$f_{L}^{c_{2}}=f_{L}^{c_{1}}$，对于$\left\{f_{i}^{c_{1}}, i<L\right\}$，通过如下公式得到$f_{i}^{c_{2}}$（文中把VGG-16第三个卷积块设置为优化块，即$l=3, L=5$）
$$
f_{i}^{c_{2}}=f_{i}^{c_{1}} \odot \Pi_{k=i+1}^{L} \operatorname{Conv}\left(U p\left(f_{k}^{c_{1}}\right)\right), i \in[l, \ldots, L-1]
$$
其中$U p(\cdot)$为上采样操作，$C o n v$是卷积核为$3 \times 3$卷积，$\prod$级联操作，$(\odot)$相乘操作.我们来算一下具体的$f_{i}^{c_{2}}$
$$
f_{3}^{c_{2}}=f_{3}^{c_{1}} \odot cat(Conv(U p(f_{4}^{c_{1}})),Conv(U p(f_{5}^{c_{1}})))\\
f_{4}^{c_{2}}=f_{4}^{c_{1}} \odot Conv(U p(f_{5}^{c_{1}}))\\
f_{5}^{c_{2}}=f_{5}^{c_{1}}
$$
~~看到这里完全是懵逼的状态，这和上面画的图一点都对不上，自闭了。。。。。。这是什么骚操作。感觉得把他的代码翻出来读一读。~~
贴上作者代码
```
import torch
import torch.nn as nn

from HolisticAttention import HA
from vgg import B2_VGG


class RFB(nn.Module):#主要是把卷积拆分，然后膨胀卷积
    def __init__(self, in_channel, out_channel):
        super(RFB, self).__init__()
        self.relu = nn.ReLU(True)
        self.branch0 = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 1),
        )
        self.branch1 = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 1),
            nn.Conv2d(out_channel, out_channel, kernel_size=(1, 3), padding=(0, 1)),
            nn.Conv2d(out_channel, out_channel, kernel_size=(3, 1), padding=(1, 0)),
            nn.Conv2d(out_channel, out_channel, 3, padding=3, dilation=3)
        )
        self.branch2 = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 1),
            nn.Conv2d(out_channel, out_channel, kernel_size=(1, 5), padding=(0, 2)),
            nn.Conv2d(out_channel, out_channel, kernel_size=(5, 1), padding=(2, 0)),
            nn.Conv2d(out_channel, out_channel, 3, padding=5, dilation=5)
        )
        self.branch3 = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 1),
            nn.Conv2d(out_channel, out_channel, kernel_size=(1, 7), padding=(0, 3)),
            nn.Conv2d(out_channel, out_channel, kernel_size=(7, 1), padding=(3, 0)),
            nn.Conv2d(out_channel, out_channel, 3, padding=7, dilation=7)
        )
        self.conv_cat = nn.Conv2d(4*out_channel, out_channel, 3, padding=1)
        self.conv_res = nn.Conv2d(in_channel, out_channel, 1)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                m.weight.data.normal_(std=0.01)
                m.bias.data.fill_(0)

    def forward(self, x):
        x0 = self.branch0(x)
        x1 = self.branch1(x)
        x2 = self.branch2(x)
        x3 = self.branch3(x)

        x_cat = torch.cat((x0, x1, x2, x3), 1)#级联
        x_cat = self.conv_cat(x_cat)#缩小特征通道

        x = self.relu(x_cat + self.conv_res(x))#这里怎么又算了一遍branch0??
        return x


class aggregation(nn.Module):#级联解码器
    def __init__(self, channel):
        super(aggregation, self).__init__()
        self.relu = nn.ReLU(True)

        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.conv_upsample1 = nn.Conv2d(channel, channel, 3, padding=1)
        self.conv_upsample2 = nn.Conv2d(channel, channel, 3, padding=1)
        self.conv_upsample3 = nn.Conv2d(channel, channel, 3, padding=1)
        self.conv_upsample4 = nn.Conv2d(channel, channel, 3, padding=1)
        self.conv_upsample5 = nn.Conv2d(2*channel, 2*channel, 3, padding=1)

        self.conv_concat2 = nn.Conv2d(2*channel, 2*channel, 3, padding=1)
        self.conv_concat3 = nn.Conv2d(3*channel, 3*channel, 3, padding=1)
        self.conv4 = nn.Conv2d(3*channel, 3*channel, 3, padding=1)
        self.conv5 = nn.Conv2d(3*channel, 1, 1)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                m.weight.data.normal_(std=0.01)
                m.bias.data.fill_(0)

    def forward(self, x1, x2, x3):#这里感觉上采样很严重呀！
        # x1: 1/16 x2: 1/8 x3: 1/4
        x1_1 = x1
        x2_1 = self.conv_upsample1(self.upsample(x1)) * x2
        x3_1 = self.conv_upsample2(self.upsample(self.upsample(x1))) \
               * self.conv_upsample3(self.upsample(x2)) * x3

        x2_2 = torch.cat((x2_1, self.conv_upsample4(self.upsample(x1_1))), 1)
        x2_2 = self.conv_concat2(x2_2)

        x3_2 = torch.cat((x3_1, self.conv_upsample5(self.upsample(x2_2))), 1)
        x3_2 = self.conv_concat3(x3_2)

        x = self.conv4(x3_2)
        x = self.conv5(x)

        return x


class CPD_VGG(nn.Module):
    def __init__(self, channel=32):
        super(CPD_VGG, self).__init__()
        self.vgg = B2_VGG()
        self.rfb3_1 = RFB(256, channel)
        self.rfb4_1 = RFB(512, channel)
        self.rfb5_1 = RFB(512, channel)
        self.agg1 = aggregation(channel)

        self.rfb3_2 = RFB(256, channel)
        self.rfb4_2 = RFB(512, channel)
        self.rfb5_2 = RFB(512, channel)
        self.agg2 = aggregation(channel)

        self.HA = HA()
        self.upsample = nn.Upsample(scale_factor=4, mode='bilinear', align_corners=False)

    def forward(self, x):#以vgg算RFB
        x1 = self.vgg.conv1(x)#公共部分
        x2 = self.vgg.conv2(x1)
        x3 = self.vgg.conv3(x2)

        x3_1 = x3#第一个
        x4_1 = self.vgg.conv4_1(x3_1)
        x5_1 = self.vgg.conv5_1(x4_1)
        x3_1 = self.rfb3_1(x3_1)
        x4_1 = self.rfb4_1(x4_1)
        x5_1 = self.rfb5_1(x5_1)
        attention = self.agg1(x5_1, x4_1, x3_1)#级联算fi2

        x3_2 = self.HA(attention.sigmoid(), x3)#加入注意机制
        #算第二部分
        x4_2 = self.vgg.conv4_2(x3_2)
        x5_2 = self.vgg.conv5_2(x4_2)
        x3_2 = self.rfb3_2(x3_2)
        x4_2 = self.rfb4_2(x4_2)
        x5_2 = self.rfb5_2(x5_2)
        detection = self.agg2(x5_2, x4_2, x3_2)

        return self.upsample(attention), self.upsample(detection)
```
还是看代码来的实在，之前把级联解码器和整个网络搞混了，级联解码器是一个单独的部分，这篇论文中最重要的部分，作者确没画图！！只是给了一个整体的架构，级联解码器部分给省略了。。。。

## 思考

1. RFB是个啥？又得补知识了，不然这个论文根本没法看。（看了代码好像就是卷积拆分，然后运用膨胀卷积）
2. 关于整体注意那个机制我觉得设计得挺好的。
3. 话说卷积卷积拆分真的这么高效么？回头试一试！

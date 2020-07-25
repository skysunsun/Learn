# 核心
**YOLO的核心思想就是将整张图作为网络的输入，直接在输出层回归bounding box的位置和bounding box的类别**
- 将一幅图像分成S×S个网络(grid cell)，输入网络
- 网络一顿骚操作输出SxSx5×B+C个向量
- 如果某个object的中心落在网格中，则这个网格就负责预测这个object (5×B+C),每个网格要预测B个bounding box，预测C个类别的概率,每个bounding box要预测(x, y, w, h)和confidence共5个值(confidence代表了所有预测的box含有object的置信度和box预测的准确度)
- 根据设置的阈值过滤boxes，滤掉分类置信度得分(class-specific confidence score)得分低的boxes，
- 对boxes进行NMS处理，就得到最终的检测结果。



## [yolov1](https://arxiv.org/pdf/1506.02640.pdf)

![tbj1Vs.png](https://s1.ax1x.com/2020/06/11/tbj1Vs.png)

### 妙就妙在这个损失函数的设计

![tbv779.png](https://s1.ax1x.com/2020/06/11/tbv779.png)

损失函数的设计目标就是让坐标（x,y,w,h），confidence，classification 这个三个方面达到很好的平衡。
简单的全部采用了平方误差损失(sum-squared error loss)来做这件事会有以下不足：
a) 8维的localization error和20维的classification error同等重要显然是不合理的；
b) 如果一个网格中没有object（一幅图中这种网格很多），那么就会将这些网格中的box的confidence push到0，相比于较少的有object的网格，这种做法是overpowering的，这会导致网络不稳定甚至发散。
c) 对不同大小的bbox预测中，相比于大bbox预测偏一点，小box预测偏一点更不能忍受。而平方误差损失(sum-squared error loss)中对同样的偏移loss是一样。
d) 一个网格预测多个bounding box，在训练时我们希望每个object（ground true box）只有一个bounding box专门负责（一个object 一个bbox）
解决方案如下：
a) 更重视8维的坐标预测，给这些损失前面赋予更大的loss weight, 记为 $\lambda_{coord}$ ,在pascal VOC训练中取5,对没有object的bbox的confidence loss，赋予小的loss weight，记为 $\lambda_{noobj}$ ，在pascal VOC训练中取0.5
b) 有object的bbox的confidence loss 和类别的loss 的loss weight正常取1
c) 作者用了一个比较取巧的办法，就是将box的width和height取平方根代替原本的height和width。 因为small bbox的横轴值较小，发生偏移时，反应到y轴上的loss 比 big box 要大
yolov1SumSquareErrorLoss
d) 具体做法是与ground true box（object）的IOU最大的bounding box 负责该ground true box(object)的预测。（个人理解：通过过滤和NMS，得到的IOU最大者偏移会更少一些，可以更快速的学习到正确位置）
### 缺点
- YOLO对相互靠的很近的物体，还有很小的群体,检测效果不好，这是因为一个网格中只预测了两个框，并且只属于一类。
- 对测试图像中，同一类物体出现的新的不常见的长宽比和其他情况下泛化能力偏弱。
- 由于损失函数的问题，定位误差是影响检测效果的主要原因。尤其是大小物体的处理上，还有待加强。


## [yolov2](https://arxiv.org/pdf/1612.08242v1.pdf)

![tqn7Y6.png](https://s1.ax1x.com/2020/06/11/tqn7Y6.png)

- 每个卷积层后添加了BN层，加速了网络的收敛。
- 跨连：在第16层开始分为两条路径，将低层的特征直接连接到高层，可提高模型性能。
![tquCff.png](https://s1.ax1x.com/2020/06/11/tquCff.png)
- 移除全连接层，使用卷积层预测框的偏移量，最终的输出向量中保存了原来的位置信息。
- 使用了Anchor Box的方法
- 有了预训练，预训练是在ImageNet上按分类的方式进行预训练160轮，使用SGD优化方法，初始学习率0.1，每次下降4倍，到0.0005时终止。除了训练224x224尺寸的图像外，还是用448x448尺寸的图片。
- 训练时去除Darknet的最后一个卷积层，并将网络结构修改为yolov2的网络，在VOC数据集上进行训练。训练使用的代价函数是MSE代价函数。
- 加入多尺度训练，训练时使用320~608尺寸的图像[320,352，….，608]。


## [yolov3](https://pjreddie.com/media/files/papers/YOLOv3.pdf)
![tqNCh4.jpg](https://s1.ax1x.com/2020/06/11/tqNCh4.jpg)

- 网络结构改变：网络的结构由Darknet-19变为Darknet-53。
- 多尺度预测：输出3层，每层 S × S个网格，分别为 13×13 ，26 ×26 ，52×52
- 小尺度：（13×13的feature map）网络接收一张（416×416）的图，经过5个步长为2的卷积来进行降采样(416 / 2ˆ5 = 13),输出（13×13×512），再经过7个卷积得到第一个特征图谱，在这个特征图谱上做第一次预测。
- 中尺度: （26×26的feature map）从小尺度中从后向前获得倒数第3个卷积层的输出，进行一次卷积一次x2上采样，将上采样特征(26×26×256)与第43个卷积特征(26×26×512)连接，输出(26×26×728),经过7个卷积得到第二个特征图谱(26×26×255)，在这个特征图谱上做第二次预测。
- 大尺度：（52×52的feature map）操作同中尺度,从后向前获得倒数第3个卷积层的输出，进行一次卷积一次x2上采样，将上采样特征与第26个卷积特征连接，经过7个卷积得到第三个特征图谱，在这个特征图谱上做第三次预测。输出（52×52×255）
好处：让网络同时学习到深层和浅层的特征，通过叠加浅层特征图特征到相邻通道，类似于FPN中的umsample+concat。这个方法把26x26x512的特征图叠加13x13x256的特征图，使模型有了细粒度特征,增加对小目标的识别能力
- anchor box:yolov3 anchor box一共有9个，由k-means聚类得到。在COCO数据集上，9个聚类是：（10×13）;（16×30）;（33×23）;（30×61）;（62×45）; （59×119）; （116×90）; （156×198）; （373×326）。不同尺寸特征图对应不同大小的先验框。
13×13尺度的anchor box [（116×90），（156×198），（373×326）]
26×26尺度的anchor box [（30×61），（62×45），（59×119）]
52×52尺度的anchor box [（10×13），（16×30），（33×23）]
原因：(越精细的grid cell就可以检测出越精细的物体)尺度越大，感受野越小，对小物体越敏感，所以选择小的anchor box
- 边框预测：预测tx ty tw th，使用sigmoid对Objectness和Classes confidence进行sigmoid得到0~1的概率，之所以用sigmoid取代之前版本的softmax，原因是softmax会扩大最大类别概率值而抑制其他类别概率值
yolo3regressorbox
![tqD6SS.png](https://s1.ax1x.com/2020/06/11/tqD6SS.png)
(tx,ty):目标中心点相对于该点所在网格左上角的偏移量，经过sigmoid归一化。即值属于【0,1】。如图约（0.3 , 0.4）
(cx,cy):该点所在网格的左上角距离最左上角相差的格子数。如图（1,1）
(pw,ph):anchor box 的边长
(tw,th):预测边框的宽和高
PS：最终得到的边框坐标值是bx,by,bw,bh.而网络学习目标是tx,ty,tw,th
损失函数LOSS：YOLO V3把YOLOV2中的Softmax loss变成Logistic loss

## tiny_yolov3
![tqNK4e.png](https://s1.ax1x.com/2020/06/11/tqNK4e.png)


## 参考

[https://luckmoonlight.github.io/2018/11/28/yoloV1yolov2yoloV3/](https://luckmoonlight.github.io/2018/11/28/yoloV1yolov2yoloV3/)

[https://bbs.cvmart.net/topics/2053](https://bbs.cvmart.net/topics/2053)
# 中文乱码问题
在画图之前加入如下代码：
```python
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
```
并且在有中文的地方加入`u`字符，比如
```python
plt.xlabel(u"这是x轴")
```

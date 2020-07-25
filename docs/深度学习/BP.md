

# 字母定义
$W_{j k}^{l}$是$l-1$层的第$k$个神经元到$l$层的第$j$个神经元的权重

$b_{j}^{l}$是$l$层的第$j$个神经元的偏置

$a_{j}^{l}$是$l$层的第$j$个神经元的激活值

$\sigma$是激活函数

$z_{j}^{l}$是第$l$层的第$j$个神经元的带权输入

$\delta_{j}^{l}$是第$l$层的第$j$个元素的误差

$\nabla_{a} C$是函数$C$对变量$a$求偏导，即梯度

# 前向传播
$$
a_{j}^{l}=\sigma\left(\sum_{k} w_{j k}^{l} a_{k}^{l-1}+b_{j}^{l}\right)
$$
这样写有点麻烦，于是把他们向量化

$W^{l}$是权值矩阵，第$j$行$k$列的元素是$W_{jk}^{l}$，$b^{l}$是偏置向量，第$j$行的元素是$b_{j}^{l}$,于是上面的式子可以写成
$$
a^{l}=\sigma\left(w^{l} a^{l-1}+b^{l}\right)
$$
进一步简化，定义
$$
z^{l} \equiv w^{l} a^{l-1}+b^{l}
$$
则上面的式子可以写成
$$
a^{l}=\sigma\left(z^{l}\right)
$$

# 反向传播

> 反向传播的核心是一个对代价函数$C$关于任何权重$w$和偏置$b$的偏导数 $\partial{C}/\partial{w}$和$\partial{C}/\partial{b}$的表达式。

为此我们定义
$$
\delta_{j}^{l} \equiv \frac{\partial C}{\partial z_{j}^{l}}
$$

## BP的四个基本方程

$$
\begin{array}{l}{\delta^{L}=\nabla_{a} C \odot \sigma^{\prime}\left(z^{L}\right)} \\ {\delta^{l}=\left(\left(w^{l+1}\right)^{T} \delta^{l+1}\right) \odot \sigma^{\prime}\left(z^{l}\right)} \\ {\frac{\partial C}{\partial b_{j}^{L}}=\delta_{j}^{l}} \\ {\frac{\partial C}{\partial w_{j k}^{l}}=a_{k}^{l-1} \delta_{j}^{l}}\end{array}
$$

## 证明

### 证明$\delta^{L}=\nabla_{a} C \odot \sigma^{\prime}\left(z^{L}\right)$
首先根据链式法则
$$
\delta_{j}^{L}=\sum_{k} \frac{\partial C}{\partial a_{k}^{L}} \frac{\partial a_{k}^{L}}{\partial z_{j}^{L}}
$$
由于第$k$个神经元的输出激活值$a_{k}^{l}$只依赖下标$k=j$时第$j$个神经元的输入$z_{j}^{l}$，所以上面的式子可以简化为
$$
\delta_{j}^{L}=\frac{\partial C}{\partial a_{j}^{L}} \frac{\partial a_{j}^{L}}{\partial z_{j}^{L}}
$$
根据我们的定义
$$a_{j}^{L}=\sigma\left(z_{j}^{L}\right)$$
所以上面的式子可以写成
$$
\delta_{j}^{L}=\frac{\partial C}{\partial a_{j}^{L}} \sigma^{\prime}\left(z_{j}^{L}\right)
$$
根据梯度运算符，所以最后的式子可以写成（只是写法不一样了而已）
$$
\delta_{j}^{L}=\nabla_{a} C \odot \sigma^{\prime}\left(z_{j}^{L}\right)
$$
进一步得
$$
\delta^{L}=\nabla_{a} C \odot \sigma^{\prime}\left(z^{L}\right)
$$

### 证明$\delta^{l}=\left(\left(w^{l+1}\right)^{T} \delta^{l+1}\right) \odot \sigma^{\prime}\left(z^{l}\right)$

由定义
$$
\delta_{j}^{l}=\frac{\partial C}{\partial z_{j}^{l}}
$$
根据链式法则，改写上面的式子为
$$
\frac{\partial C}{\partial z_{j}^{l+1}} \frac{\partial z_{j}^{l+1}}{\partial z_{j}^{l}}
$$
然后再把第一项写成定义的样子
$$
\frac{\partial z_{j}^{l+1}}{\partial z_{j}^{l}} \delta_{j}^{l+1}
$$
根据前向传播(为了好看，这里简化了，没有写求和的形式)
$$
z_{j}^{l+1}= w_{j}^{l+1} a_{j}^{l}+b^{l+1}=w_{ j}^{l+1} \sigma\left(z_{j}^{l}\right)+b^{l+1}
$$
所以上面式子的第一项可以写成
$$
\frac{\partial z^{l+1}}{\partial z_{j}^{l}}=w_{j}^{l+1} \sigma^{\prime}\left(z_{j}^{l}\right)
$$
把这个代入得证
$$
\delta_{j}^{l}= w_{j}^{l+1} \delta_{j}^{l+1} \sigma^{\prime}\left(z_{j}^{l}\right)
$$
写成我们想要的向量形式
$$
\delta^{l}=\left(\left(w^{l+1}\right)^{T} \delta^{l+1}\right) \odot \sigma^{\prime}\left(z^{l}\right)
$$

### 证明 $\frac{\partial C}{\partial b_{j}^{l}}=\delta_{j}^{l}$

由定义
$$\begin{array}{l}
z_{j}^{l}= w_{j}^{l} a^{l-1}+b_{j}^{l}\\
\delta_{j}^{l} \equiv \frac{\partial C}{\partial z_{j}^{l}}
\end{array}
$$
链式求导
$$
\frac{\partial C}{\partial b_{j}^{l}}=\frac{\partial C}{\partial z_{j}^{l}} \frac{\partial z_{j}^{l}}{\partial b_{j}^{l}}
$$
又因为偏置的系数为1，所以
$$
\frac{\partial z_{j}^{l}}{\partial b_{j}^{l}}=1
$$
***注意*** 在这里$b$是一个变量而不是一个常数
所以得证，写成向量形式
$$
\frac{\partial C}{\partial b^{l}}=\delta^{l}
$$

### 证明$\frac{\partial C}{\partial w_{j k}^{l}}=a_{k}^{l-1} \delta_{j}^{l}$

由定义
$$\begin{array}{l}
{z_{j}^{l}=\sum_{k} w_{j k}^{l} a_{k}^{l-1}+b_{j}^{l}} \\ 
{\delta_{j}^{l} \equiv \frac{\partial C}{\partial z_{j}^{l}}}
\end{array}
$$
所以
$$
\frac{\partial z_{j}^{l}}{\partial w_{j k}^{l}}=a_{k}^{l-1}
$$
根据链式法则
$$
\frac{\partial C}{\partial w_{j k}^{l}}=\frac{\partial C}{\partial z_{j}^{l}} \frac{\partial z_{j}^{l}}{\partial w_{j k}^{l}}=\delta_{j}^{l} a_{k}^{l-1}
$$
## 代码

```python
import numpy as np
class Network(object):
    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The "mini_batch" is a list of tuples "(x, y)", and "eta"
        is the learning rate."""
        #初始化
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        #更新梯度
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        #更新权重
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple "(nabla_b, nabla_w)" representing the
        gradient for the cost function C_x.  "nabla_b" and
        "nabla_w" are layer-by-layer lists of numpy arrays, similar
        to "self.biases" and "self.weights"."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)


    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
```

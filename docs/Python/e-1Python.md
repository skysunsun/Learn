

# Python相关

## 聊一下我最擅长的编程语言（Python），Python的特点？  

简单。Python遵循"简单、优雅、明确"的设计哲学。

高级。Python是一种高级语言，相对于c，牺牲了性能而提升了编程人员的效率。它使得程序员可以不用关注底层细节，而把精力全部放在编程上。

Python既支持面向过程，也支持面向对象。

可扩展。可以通过c、c++语言为python编写扩充模块。

免费和开源。Python是FLOSS(自由/开放源码软件)之一，允许自由的发布软件的备份、阅读和修改其源代码、将其一部分自由地用于新的自由软件中。

边编译边执行。Python是解释型语言，边编译边执行。

可移植。Python能运行在不同的平台上。

丰富的库。Python拥有许多功能丰富的库。

可嵌入性。Python可以嵌入到c、c++中，为其提供脚本功能。

## python是怎么做到跨平台的？

Python有不同的编译器，用cPython则把Python编译成Python bytecode然后在不同平台上运行。Python默认的是解释器是cpython。
而Jython则是把Python编译成java bytecode然后再利用java虚拟机来运行。所以可以在这里插入java语言，因为最后都是要编译成java bytecode来运行。

## Python列表的底层是如何实现的

在CPython中，列表被实现为**长度可变的数组**

从细节上看，Python中的列表是由对其它对象的引用组成的连续数组。指向这个数组的指针及其长度被保存在一个列表头结构中。这意味着，每次添加或删除一个元素时，由引用组成的数组需要该标大小（重新分配）。幸运的是，Python在创建这些数组时采用了指数分配，所以并不是每次操作都需要改变数组的大小。但是，也因为这个原因添加或取出元素的平摊复杂度较低。


列表和元组的区别是显然的：
列表是动态的，其大小可以该标 (重新分配)；
而元组是不可变的，一旦创建就不能修改。

list和tuple在c实现上是很相似的，对于元素数量大的时候，
都是一个数组指针，指针指向相应的对象，找不到tuple比list快的理由。
但对于小对象来说，tuple会有一个对象池，所以小的、重复的使用tuple还有益处的。

为什么要有tuple，还有很多的合理性。
实际情况中的确也有不少大小固定的列表结构，例如二维地理坐标等；
另外tuple也给元素天然地赋予了只读属性。


## Python深拷贝浅拷贝

直接赋值：其实就是对象的引用（别名）。

浅拷贝(copy)：拷贝父对象，不会拷贝对象的内部的子对象。

深拷贝(deepcopy)： copy 模块的 deepcopy 方法，完全拷贝了父对象及其子对象

## Python中`==`和`is`的区别

`==`是判断对象是否相等，是对两个对象的 value 进行比较，比较两个对象的值是否相等

`is`是判断对象是否相同，是对两个对象的 id 进行比较，比较两个对象的内存地址是否相等

## Python如何实现内存管理？有没有可能出现内存泄露的问题？

Python GC主要使用**引用计数**来跟踪和回收垃圾。在引用计数的基础上，通过**标记-清除**解决容器对象可能产生的循环引用问题。通过分代以空间换时间的方法提高垃圾回收效率

>引用计数：每个对象中都有ob-refcnt来做引用计数。当一个对象...,ob-refcnt就会增加，当引用的对象删除，那么ob-refcnt就会减少当ob-refcnt为零，就会释放该对象的内存空间

>标记清除：解决循环引用的问题。先按需分配，等到没有空闲内存的时候，从寄存器和程序栈上的引用出发，遍历所有对象和引用把所有能访问的打标记，最后将没有标记的对象释放掉

>分代技术：Python将内存根据对象的存活时间划分为不同的集合，每个集合称为一个代，Python将内存分为了3“代”，分别为年轻代（第0代）、中年代（第1代）、老年代（第2代），他们对应的是3个链表，它们的垃圾收集频率与对象的存活时间的增大而减小。新创建的对象都会分配在年轻代，年轻代链表的总数达到上限时，Python垃圾收集机制就会被触发，把那些可以被回收的对象回收掉，而那些不会回收的对象就会被移到中年代去，依此类推，老年代中的对象是存活时间最久的对象，甚至是存活于整个系统的生命周期内。

Python也会内存泄露，Python本身的垃圾回收机制无法回收重写了del的循环引用的对象.

程序员管理好每个python对象的引用，尽量在不需要使用对象的时候，断开所有引用,尽量少通过循环引用组织数据，可以改用weakref做弱引用或者用id之类的句柄访问对象,通过gc模块的接口可以检查出每次垃圾回收有哪些对象不能自动处理，再逐个逐个处理

## python中`+`和`join`的区别

在用"+"连接字符串时，结果会生成新的对象，用join时结果只是将原列表中的元素拼接起来，所以join效率比较高

## \*arg, \*\*kargs的用法

`*args`是可变位置参数，是一个元组，传入的参数会被放进元组里。

`**kwargs`是可变关键字参数，是一个字典，传入的参数以键值对的形式存放到字典里。

## Python中基本类型有哪些

int 整型 bool 布尔 strintg 字符串 list 列表 tuple 元组dict 字典

## 内置数据结构有哪些?,tuple与list有什么区别?

(tuple, list, dict, set)

**同**
1. 都是序列
2. 都可以存储任何数据类型
3. 可以通过索引访问

**不同**
元组是不可变的， 而列表是可变的(导致不能将列表用作字典中的key)

## 装饰器

装饰器本质上是一个 Python 函数或类，它可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能，装饰器的返回值也是一个函数/类对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景，装饰器是解决这类问题的绝佳设计。有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码到装饰器中并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。


```python
def add():
    print('xxxx')
def log(func):
    def wrapper():
        print('调用%s'%func.__name__)
        func()
    return wrapper
```
## 迭代器，生成器

迭代器：迭代就是循环。迭代器是可以被next() 函数调用并不断返回下一个值的对象称为迭代器。

生成器是通过一个或多个yield表达式构成的函数，每个一个生成器都是一个继承器（但是迭代器不一定是生成器）。

如果一个函数包含yield关键字，这个函数就会变成一个生成器。

生成器并不会一次返回所有结果，或者每次遇到yield关键字后返回相应结果，并保留函数当前的运行状态，等待下一次的调用。

由于生成器也是一个迭代器，那么它就应该支持next方法来获取下一个值。


## range和xrange区别，xrange通过什么关键字实现的？

range直接生成一个可迭代的list，xrange 生成器，省内存

xrange通过yield实现


## yield语句底层如何实现？

所以生成器对象每次执行结束都把字节码的偏移量记录下来，并把运行状态保存在PyFrameObject里，下一次运行时生成器时，python解释器直接按照偏移量寻找下一个字节码指令。


## Python的异常处理？

捕捉异常可以使用try/except语句。

try/except语句用来检测try语句块中的错误，从而让except语句捕获异常信息并处理。

如果你不想在异常发生时结束你的程序，只需在try里捕获它

try的工作原理是，当开始一个try语句后，Python就在当前程序的上下文中作标记，这样当异常出现时就可以回到这里，try子句先执行，接下来会发生什么依赖于执行时是否出现异常。

1. 如果当try后的语句执行时发生异常，Python就跳回到try并执行第一个匹配该异常的except子句，异常处理完毕，控制流就通过整个try语句（除非在处理异常时又引发新的异常）。
2. 如果在try后的语句里发生了异常，却没有匹配的except子句，异常将被递交到上层的try，或者到程序的最上层（这样将结束程序，并打印默认的出错信息）。
3. 如果在try子句执行时没有发生异常，Python将执行else语句后的语句（如果有else的话），然后控制流通过整个try语句。

使用raise语句自己触发异常

用户自定义异常

## 猴子补丁

属性在运行时的动态替换，叫做猴子补丁（Monkey Patch）

## Python中的`__new__`和`__init__`的区别

`__new__`和`__init__`的主要区别在于：`__new__`是用来创造一个类的实例的（constructor），而`__init__`是用来初始化一个实例的（initializer）。


`__new__`： 对象的创建，是一个静态方法，第一个参数是`cls`。(想想也是，不可能是`self`，对象还没创建，哪来的`self`)

`__init__ `： 对象的初始化， 是一个实例方法，第一个参数是`self`。

`__call__` ： 对象可`call`，注意不是类，是对象。`__call__()`的作用是使实例能够像函数一样被调用，同时不影响实例本身的生命周期（__call__()不影响一个实例的构造和析构）。但是`__call__()`可以用来改变实例的内部成员的值。

```python
class Entity:
'''调用实体来改变实体的位置。'''

def __init__(self, size, x, y):
    self.x, self.y = x, y
    self.size = size

def __call__(self, x, y):
    '''改变实体的位置'''
    self.x, self.y = x, y

e = Entity(1, 2, 3) // 创建实例
e(4, 5) //实例可以象函数那样执行，并传入x y值，修改对象的x y 
```


## import一个包时过程是怎么样的？


大型Python程序以模块module和包package的形式组织。

模块：就是一些.py文件，可以包含函数、变量、类等符号；

包：由模块及子包组成

第一次导入一个模块，会执行这个模块

可以通过修改模块module的__all__列表，来改变from module import * 时的效果

导入一个包，其实就是导入包的__init__.py模块

如果包的__init__.py模块为空，那么import package这样的语句是不能使用包当中的任何模块的

如果包的__init__.py模块为空，那我们只能使用import package.module或者from package import module这样的导入方式

__init__.py也是个模块，其实也可以在__init__.py中直接定义函数fun，那样import package就可以直接用package.fun这个函数了是吧。但是我们一般不会这么干，这样会使__init__.py文件太乱

__init__.py也是个模块，那也可以在这个模块中导入其他模块，这样import package时，就能直接使用一些符号了。

__init__.py也是个模块，也可以定义__all__列表变量，控制from package import * 的作用。




## 菱形继承

在多层继承和多继承同时使用的情况下，就会出现复杂的继承关系，多重多继承。

其中，就会出现菱形继承。
```python
class A():
    def __init__(self):
        print('init A...')
        print('end A...')

class B(A):
    def __init__(self):
        print('init B...')
        A.__init__(self)
        print('end B...')

class C(A):
    def __init__(self):
        print('init C...')
        A.__init__(self)
        print('end C...')

class D(B, C):
    def __init__(self):
        print('init D...')
        B.__init__(self)
        C.__init__(self)
        print('end D...')

if __name__ == '__main__':
    D()
```
可以使用super()避免顶层父类中的某个方法被多次调用
```python
class A():
    def __init__(self):
        print('init A...')
        print('end A...')

class B(A):
    def __init__(self):
        print('init B...')
        super(B, self).__init__()
        print('end B...')

class C(A):
    def __init__(self):
        print('init C...')
        super(C, self).__init__()
        print('end C...')

class D(B, C):
    def __init__(self):
        print('init D...')
        super(D, self).__init__()
        print('end D...')

if __name__ == '__main__':
    D()
```

## Python语言中的异步

asyncio 是用来编写并发代码的库，使用 async/await 语法。

asyncio 被用作多个提供高性能 Python 异步框架的基础，包括网络和网站服务，数据库连接库，分布式任务队列等等。

asyncio 往往是构建 IO 密集型和高层级 结构化 网络代码的最佳选择。

asyncio 提供一组 高层级 API 用于:

并发地 运行 Python 协程 并对其执行过程实现完全控制;

执行 网络 IO 和 IPC;

控制 子进程;

通过 队列 实现分布式任务;

同步 并发代码;

此外，还有一些 低层级 API 以支持 库和框架的开发者 实现:

创建和管理 事件循环，以提供异步 API 用于 网络化, 运行 子进程，处理 OS 信号 等等;

使用 transports 实现高效率协议;

通过 async/await 语法 桥接 基于回调的库和代码。


## Python里的eval

将字符串str当成有效的表达式来求值并返回计算结果

1. 计算字符串中有效的表达式，并返回结果

2. 将字符串转成相应的对象（如list、tuple、dict和string之间的转换）

3. 将利用反引号转换的字符串再反转回对象


## 设计并实现字典，常用操作，get， set， delete
```python
def new(num_buckets=256):
    """Initializes a Map with the given number of buckets."""
    aMap = []
    for i in range(0, num_buckets):
        aMap.append([])
    return aMap

def hash_key(aMap, key):
    """Given a key this will create a number and then convert it to
    an index for the aMap's buckets."""
    return hash(key) % len(aMap)

def get_bucket(aMap, key):
    """Given a key, find the bucket where it would go."""
    bucket_id = hash_key(aMap, key)
    return aMap[bucket_id]

def get_slot(aMap, key, default=None):
    """
    Returns the index, key, and value of a slot found in a bucket.
    Returns -1, key, and default (None if not set) when not found.
    """
    bucket = get_bucket(aMap, key)

    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return i, k, v

    return -1, key, default

def get(aMap, key, default=None):
    """Gets the value in a bucket for the given key, or the default."""
    i, k, v = get_slot(aMap, key, default=default)
    return v

def set(aMap, key, value):
    """Sets the key to the value, replacing any existing value."""
    bucket = get_bucket(aMap, key)
    i, k, v = get_slot(aMap, key)

    if i >= 0:
        # the key exists, replace it
        bucket[i] = (key, value)
    else:
        # the key does not, append to create it
        bucket.append((key, value))

def delete(aMap, key):
    """Deletes the given key from the Map."""
    bucket = get_bucket(aMap, key)

    for i in xrange(len(bucket)):
        k, v = bucket[i]
        if key == k:
            del bucket[i]
            break

def list(aMap):
    """Prints out what's in the Map."""
    for bucket in aMap:
        if bucket:
            for k, v in bucket:
                print k, v
```

## 简述with方法打开处理文件帮我我们做了什么？

打开文件在进行读写的时候可能会出现一些异常状况，如果按照常规的f.open

　　写法，我们需要try,except,finally，做异常判断，并且文件最终不管遇到什么情况，都要执行finally f.close()关闭文件，with方法帮我们实现了finally中f.close

## flask和Django区别



## 实现list

## python反射

通过字符串映射object对象的方法或者属性

```python
hasattr(obj,name_str): 判断objec是否有name_str这个方法或者属性
getattr(obj,name_str): 获取object对象中与name_str同名的方法或者函数
setattr(obj,name_str,value): 为object对象设置一个以name_str为名的value方法或者属性
delattr(obj,name_str): 删除object对象中的name_str方法或者属性
```

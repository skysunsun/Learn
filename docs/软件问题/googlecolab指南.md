

直接Google搜索colab里面有详细的文档介绍怎么使用
*Google可能需要梯子*
下面主要记录下如何加载云盘

## 加载云盘

1. 输入如下代码：
```
!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

```
这个会弹两个链接，需要你点链接，点了之后认证，然后会给你一个密码，复制到colab notebook的输入框中，完成验证

看网上好多说直接复制链接到输入框。。。。。。
这个直接报错

2. 指定Google Drive云端硬盘的根目录，名为drive

`!mkdir -p drive`

`!google-drive-ocamlfuse drive`

3. 此处为google drive中的文件路径,drive为之前指定的工作根目录，要加上
```
import os
os.chdir("drive/Colab Notebooks")
```

4. 把你要用的文件拷进Colab Notebooks,当然你也可以加载其他的文件夹

5. 查看文件夹下有哪些文件

`!ls`

大功告成


还有就是在这个文件夹下只能用相对路劲，绝对路径好像会报错


## 其他的问题

看网上说这个只能存在12个小时，反正谷歌也说了，一定时间强制回收，没说多久

## 关于本地连接

这个Google有详细说明，有个问题是你得允许他访问你的cookie，不然连不上

但是我就没搞懂这个功能到底干嘛用的？

只是为了访问本地文件？有了jupyter Notebook 还用colab notebook干嘛？又不能用GPU 感觉这个确实是没什么用。。。可能我理解得也有问题

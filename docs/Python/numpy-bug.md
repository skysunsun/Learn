
# numpy问题

## 报错
```
in numpy.import_array
ImportError: numpy.core.multiarray failed to import
```
这个问题可能有两个原因
1. 你用conda装了一个numpy,又用pip装了一个numpy。导致冲突，你卸载一个就行了；比如：
`conda uninstall numpy`
2. numpy 版本太低，导致不兼容，更新一下
`pip install -U numpy`

# pandas操作
## read_csv()参数说明（逗号分割）

1. filepath_or_buffer : str，pathlib。str, pathlib.Path, py._path.local.LocalPath or any object with a read() method (such as a file handle or StringIO)
可以是URL，可用URL类型包括：http, ftp, s3和文件。对于多文件正在准备中
本地文件读取实例：:/localhost/path/to/table.csv

2. sep : str, default ‘,’
指定分隔符。如果不指定参数，则会尝试使用逗号分隔。分隔符长于一个字符并且不是‘\s+’,将使用python的语法分析器。并且忽略数据中的逗号。正则表达式例子：'\r\t'

3. delimiter : str, default None
定界符，备选分隔符（如果指定该参数，则sep参数失效）

4. delim_whitespace : boolean, default False.
指定空格(例如’ ‘或者’ ‘)是否作为分隔符使用，等效于设定sep='\s+'。如果这个参数设定为Ture那么delimiter 参数失效。

5. header : int or list of ints, default ‘infer’
指定行数用来作为列名，数据开始行数。如果文件中没有列名，则默认为0，否则设置为None。如果明确设定header=0 就会替换掉原来存在列名。header参数可以是一个list例如：[0,1,3]，这个list表示将文件中的这些行作为列标题（意味着每一列有多个标题），介于中间的行将被忽略掉（例如本例中的2；本例中的数据1,2,4行将被作为多级标题出现，第3行数据将被丢弃，dataframe的数据从第5行开始。）

**注意：如果skip_blank_lines=True那么header参数忽略注释行和空行，所以header=0表示第一行数据而不是文件的第一行。**

6. names : array-like, default None
用于结果的列名列表，如果数据文件中没有列标题行，就需要执行header=None。默认列表中不能出现重复，除非设定参数mangle_dupe_cols=True。

7. index_col : int or sequence or False, default None
用作行索引的列编号或者列名，如果给定一个序列则有多个行索引。
如果文件不规则，行尾有分隔符，则可以设定index_col=False 来是的pandas不适用第一列作为行索引。

8. usecols : array-like, default None
返回一个数据子集，该列表中的值必须可以对应到文件中的位置（数字可以对应到指定的列）或者是字符传为文件中的列名。例如：usecols有效参数可能是 [0,1,2]或者是 [‘foo’, ‘bar’, ‘baz’]。使用这个参数可以加快加载速度并降低内存消耗。

9. as_recarray : boolean, default False
不赞成使用：该参数会在未来版本移除。请使用pd.read_csv(...).to_records()替代。
返回一个Numpy的recarray来替代DataFrame。如果该参数设定为True。将会优先squeeze参数使用。并且行索引将不再可用，索引列也将被忽略。

10. squeeze : boolean, default False
如果文件值包含一列，则返回一个Series

11. prefix : str, default None
在没有列标题时，给列添加前缀。例如：添加‘X’ 成为 X0, X1, ...

12. mangle_dupe_cols : boolean, default True
重复的列，将‘X’...’X’表示为‘X.0’...’X.N’。如果设定为false则会将所有重名列覆盖。

13. dtype : Type name or dict of column -> type, default None
每列数据的数据类型。例如 {‘a’: np.float64, ‘b’: np.int32}

14. engine : {‘c’, ‘python’}, optional
Parser engine to use. The C engine is faster while the python engine is currently more feature-complete.
使用的分析引擎。可以选择C或者是python。C引擎快但是Python引擎功能更加完备。

15. converters : dict, default None
列转换函数的字典。key可以是列名或者列的序号。

16. true_values : list, default None
Values to consider as True

17. false_values : list, default None
Values to consider as False

18. skipinitialspace : boolean, default False
忽略分隔符后的空白（默认为False，即不忽略）.

19. skiprows : list-like or integer, default None
需要忽略的行数（从文件开始处算起），或需要跳过的行号列表（从0开始）。

20. skipfooter : int, default 0
从文件尾部开始忽略。 (c引擎不支持)

21. skip_footer : int, default 0
不推荐使用：建议使用skipfooter ，功能一样。

22. nrows : int, default None
需要读取的行数（从文件头开始算起）。

23. na_values : scalar, str, list-like, or dict, default None
一组用于替换NA/NaN的值。如果传参，需要制定特定列的空值。默认为‘1.#IND’, ‘1.#QNAN’, ‘N/A’, ‘NA’, ‘NULL’, ‘NaN’, ‘nan’`.

24. keep_default_na : bool, default True
如果指定na_values参数，并且keep_default_na=False，那么默认的NaN将被覆盖，否则添加。

25. na_filter : boolean, default True
是否检查丢失值（空字符串或者是空值）。对于大文件来说数据集中没有空值，设定na_filter=False可以提升读取速度。

26. verbose : boolean, default False
是否打印各种解析器的输出信息，例如：“非数值列中缺失值的数量”等。

27. skip_blank_lines : boolean, default True
如果为True，则跳过空行；否则记为NaN。

28. parse_dates : boolean or list of ints or names or list of lists or dict, default False
boolean. True -> 解析索引
list of ints or names. e.g. If [1, 2, 3] -> 解析1,2,3列的值作为独立的日期列；
list of lists. e.g. If [[1, 3]] -> 合并1,3列作为一个日期列使用
dict, e.g. {‘foo’ : [1, 3]} -> 将1,3列合并，并给合并后的列起名为"foo"

29. infer_datetime_format : boolean, default False
如果设定为True并且parse_dates 可用，那么pandas将尝试转换为日期类型，如果可以转换，转换方法并解析。在某些情况下会快5~10倍。

30. keep_date_col : boolean, default False
如果连接多列解析日期，则保持参与连接的列。默认为False。

31. date_parser : function, default None
用于解析日期的函数，默认使用dateutil.parser.parser来做转换。Pandas尝试使用三种不同的方式解析，如果遇到问题则使用下一种方式。
1.使用一个或者多个arrays（由parse_dates指定）作为参数；
2.连接指定多列字符串作为一个列作为参数；
3.每行调用一次date_parser函数来解析一个或者多个字符串（由parse_dates指定）作为参数。

32. dayfirst : boolean, default False
DD/MM格式的日期类型

33. iterator : boolean, default False
返回一个TextFileReader 对象，以便逐块处理文件。

34. chunksize : int, default None
文件块的大小， See IO Tools docs for more informationon iterator and chunksize.

35. compression : {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default ‘infer’
直接使用磁盘上的压缩文件。如果使用infer参数，则使用 gzip, bz2, zip或者解压文件名中以‘.gz’, ‘.bz2’, ‘.zip’, or ‘xz’这些为后缀的文件，否则不解压。如果使用zip，那么ZIP包中国必须只包含一个文件。设置为None则不解压。
新版本0.18.1版本支持zip和xz解压

36. thousands : str, default None
千分位分割符，如“，”或者“."

37. decimal : str, default ‘.’
字符中的小数点 (例如：欧洲数据使用’，‘).

38. float_precision : string, default None
Specifies which converter the C engine should use for floating-point values. The options are None for the ordinary converter, high for the high-precision converter, and round_trip for the round-trip converter.
指定

39. lineterminator : str (length 1), default None
行分割符，只在C解析器下使用。

40. quotechar : str (length 1), optional
引号，用作标识开始和解释的字符，引号内的分割符将被忽略。

41. quoting : int or csv.QUOTE_* instance, default 0
控制csv中的引号常量。可选 QUOTE_MINIMAL (0), QUOTE_ALL (1), QUOTE_NONNUMERIC (2) or QUOTE_NONE (3)

42. doublequote : boolean, default True
双引号，当单引号已经被定义，并且quoting 参数不是QUOTE_NONE的时候，使用双引号表示引号内的元素作为一个元素使用。

43. escapechar : str (length 1), default None
当quoting 为QUOTE_NONE时，指定一个字符使的不受分隔符限值。

44. comment : str, default None
标识着多余的行不被解析。如果该字符出现在行首，这一行将被全部忽略。这个参数只能是一个字符，空行（就像skip_blank_lines=True）注释行被header和skiprows忽略一样。例如如果指定comment='#' 解析‘#empty\na,b,c\n1,2,3’ 以header=0 那么返回结果将是以’a,b,c'作为header。

45. encoding : str, default None
指定字符集类型，通常指定为'utf-8'. List of Python standard encodings

46. dialect : str or csv.Dialect instance, default None
如果没有指定特定的语言，如果sep大于一个字符则忽略。具体查看csv.Dialect 文档

47. tupleize_cols : boolean, default False
Leave a list of tuples on columns as is (default is to convert to a Multi Index on the columns)

49. error_bad_lines : boolean, default True
如果一行包含太多的列，那么默认不会返回DataFrame ，如果设置成false，那么会将改行剔除（只能在C解析器下使用）。

50. warn_bad_lines : boolean, default True
如果error_bad_lines =False，并且warn_bad_lines =True 那么所有的“bad lines”将会被输出（只能在C解析器下使用）。

51. low_memory : boolean, default True
分块加载到内存，再低内存消耗中解析。但是可能出现类型混淆。确保类型不被混淆需要设置为False。或者使用dtype 参数指定类型。注意使用chunksize 或者iterator 参数分块读入会将整个文件读入到一个Dataframe，而忽略类型（只能在C解析器中有效）

## 根据 Pandas 中列的值从DataFrame中选择行

1. 要选择列的值等于某个值"some_value"的行，请使用==：
`df.loc[df['column_name'] == some_value]`
2. 要选择列值不等于some_value的行，请使用!=：
`df.loc[df['column_name'] != some_value]`
3. 要选择列值在链表some_values中的行，请使用isin：
`df.loc[df['column_name'].isin(some_values)]`
4. 将多个条件与&组合使用：
`df.loc[(df['column_name'] == some_value) & df['other_column'].isin(some_values)]`

5. isin返回一个布尔序列，因此要选择其值不在some_values中的行，使用~取反布尔序列：
`df.loc[~df['column_name'].isin(some_values)]`


## pandas 更改列名
如果需要重命名所有的列，可以重新给df.columns 赋值 df.columns = ['new_col_1', 'new_col_1', ..., 'new_col_n'].

如果只需要改变某一列或几列的列名，则可以使用rename函数。df = df.rename(columns={'old_col_1': 'new_col_1'})。

以上两种方法也适用于index的修改，只需把columns改成index即可。

 ## pandas调整列顺序
 `df = df[['user_id','book_id','rating','mark_date']]`
 想怎么调怎么调，比如要保存部分列，就不用drop()了

 ## dataframe 按条件替换某一列中的值
 `data.loc[data['Y'] == 'T'] = 1`
## dataframe 按根据某列值更改另一列
 `
df.loc[df.a>=2,'b'] = 'new_data'`
 ## pandas值替换函数
 `df.replace(to_replace, value)`
 ## pandas多值判断生成新列
 ```
import numpy as np
import pandas as pd

data = {'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Chongqing'],
       'year': [2016,2016,2015,2017,2016, 2016],
       'population': [2100, 2300, 1000, 700, 500, 500]}
frame = pd.DataFrame(data, columns = ['year', 'city', 'population', 'debt'])

def function(a, b):
	if 'ing' in a and b == 2016:
		return 1
	else:
		return 0
print(frame, '\n')
frame['test'] = frame.apply(lambda x: function(x.city, x.year), axis = 1)
```
单值判断

`df['涨跌']=d['p_change'].apply(lambda x: '涨' if x>0 else ('跌' if x<0 else '平' ))`
 ## panda时间运算
 当前时间加上某一天
 ```
 import datetime
 from datetime import timedelta
 df['data']+timedelta(days=1)

 ```

 ## 按行读取csv
 ```
 import csv
with open("test.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    #这里不需要readlines
    for line in reader:
        print line
  ```

  ## pandas 统计函数

1. 统计个数count

`test_data.x1.count()`

2. 统计不重复值个数nunique

`test_data.x1.nunique()`

3. 筛选不重复值

`test_data.x1.unique()`


## pandas统计列里某值出现的次数
`p.groupby(['name']).size()['q']`

## pandas统计某列值的个数
`zero_col_count = dict(df[0].value_counts())`

## pandas Nan值判断

```
import math
a=float("nan")
if math.isnan(a):
    print("是nan")
else:
    print("不是nan")
```
## pandas字符长度
`test['contentLen2'] = test['content'].str.len()`

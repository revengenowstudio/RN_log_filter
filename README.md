# RN_log_filter - 复仇时刻log处理工具
此工具用于处理复仇时刻客户端生成client.log，处理后产生的hash结果可用于比较

## 使用方法

- 若首次使用此软件，请先运行一次RN——log_filter.exe，软件会在其根目录自动生成“log_input1”“log_input2”两个文件夹
- 比对用法
    - 请将要对比的client.log分别放置在“log_input1”、“log_input2”中
    - 然后运行程序，软件处理完毕后根目录下会生成一个differ_result.txt，此文件中会包含比对结果

- 只处理单个log
    - 将client.log放置在“log_input1”、“log_input2”任意一个文件夹即可，然后运行程序，即可在对应的文件夹下看见log_result.txt



## 功能
- [x] 提取log中的hash值并去重以及排序
- [x] 黑名单功能，黑名单中的内容不会在result中出现
- [x] diff功能，读取两份log并自动处理并比较，输出有差异的结果

# RN_log_filter - 复仇时刻log处理工具
此工具用于处理复仇时刻客户端生成client.log，处理后产生的hash结果可用于比较

## 使用方法
- 请将client.log放置在软件根目录下
- 然后运行程序，根目录下会生成一个log_result.txt


## 功能
- [x] 提取log中的hash值并去重以及排序
- [ ] 黑名单功能，黑名单中的内容不会在result中出现
- [ ] diff功能，读取两份log并自动处理并比较，输出有差异的结果

进程守护思路：
1. 通过判断cpu 和内存占用率 然后决定是否要开始kill 程序
2. kill 程序 需要获取到pid   pid可通过 指定查找程序 name & 程序所在目录


下面需要做的测试： 使用 taskkill  mongodb 是否影响数据库
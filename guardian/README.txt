监控思路：
1. 通过判断cpu 和内存占用率 然后决定是否要开始kill 程序
2. kill 程序 需要获取到pid   pid可通过 指定查找程序 name & 程序所在目录



win下 tasklisst查看 程序pid  taskkill /pid /f 杀死程序
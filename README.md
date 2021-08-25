# 一种结合动态链接库信息的崩溃输入分类方法

A crash inputs classification algorithm combined with dynamic link library information



## 描述

* 本工具是论文《一种结合动态链接库信息的崩溃输入分类方法》的开源项目，包括实验源码、涉及工具及论文中实验的结果。
* 本工具的实验环境和实验结果所对应的环境为Ubuntu 14.04, Python 3.4。经测试，本工具在系统Ubuntu 16.04、Ubuntu 18.04中均可使用。

## 使用说明

### 安装前准备：pwndbg

本工具使用了开源工具pwndbg，用以对程序运行中的动态链接库进行识别。详细说明及安装方法参见：https://github.com/pwndbg/pwndbg

注意：**安装pwndbg后，将覆盖系统中原有gdb。安装后，使用gdb时将直接唤出pwndbg**

### 工具安装

```
git clone https://github.com/wehann/Crash_Inputs_Classification
```

### 文件说明

* codes/：本工具的运行代码，程序将由main.py启动，设定一些变量后在start.py中进行分析。在start.py中文件运行的过程中，程序会将classifier.py加载，并进行gdb分析。
* configs/：本工具在运行过程中将要读取的配置，格式可参照"configs/config_test.json"文件。在json的每个条目中，需指定待测项目的项目名、可执行文件的路径、运行指令和存放了待分类的测试用例的目录路径。默认状态下，工具将读取configs/configs.json文件，如需更改，可在main.py中配置。
* tools/：本工具在执行过程中使用了基于qemu实现的trace追踪工具找出待测程序中用户代码的起始地址与结束地址，tools目录中的两个文件对应了分析32-bit二进制文件和64-bit二进制文件的工具。
* runtime/：本工具在执行时将在runtime目录中保存运行时需记录的过程信息，主要为一些log和分析结果信息。
* results/：存放了论文中RQ1和RQ2的实验结果

### 工具使用

1. 配置configs.json文件
2. cd codes/
3. python main.py

## 相关工具

论文在对比实验中提到了3种相关工具：Semantic Crash Bucketing、Honggfuzz和CERT BFF，其实验结果均在results目录下。

链接：

* Semantic Crash Bucketing: https://github.com/squaresLab/SemanticCrashBucketing
* Honggfuzz:  https://github.com/google/Honggfuzz
* CERT BFF: https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=507974

## 论文中的RQ1与RQ2的项目下载地址
* RQ1：
（包含于SemanticCrashBucketing的开源项目，https://github.com/squaresLab/SemanticCrashBucketing 中）

* RQ2:
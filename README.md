### 本项目在原项目的基础上添加了批量下载和查询功能
### 查询标准文件以便于下载的方式批量输出
使用方式为子命令 `openstd_spider search`

```
Usage: openstd_spider search [OPTIONS] [KEYWORD]

 搜索 浏览标准文件列表

 Arguments
 keyword      [KEYWORD]  关键字

 Options
 --ps              INTEGER RANGE [10<=x<=50]  每页条数
 --pn      -p      INTEGER RANGE [x>=1]       页码
 --status  -s      [现行|即将实施|废止]       标准状态
 --type    -t      [GB|GBT|GBZ]               标准类型
 --json    -j                                 json格式输出
 --all                                        查询全部
 --max             RANGE[10<=100000]          查询数量上限,默认10w
 --simple > xxx.txt                           查询编号简单输出到xxx.txt，便于批量下载
 --help                                       Show this message and exit.

搜索全部GBT标准并存到GBT.txt文件中
openstd_spider search -t GBT -all -simple > GBT.txt

```


### 下载标准 pdf 文件

使用方式为子命令 `openstd_spider download`

```
Usage: openstd_spider download [OPTIONS] TARGET

 下载标准文件PDF

 Arguments
 *    target      TEXT  标准编号或url [required]

 Options
 --detail   -d            是否展示详细元数据
 --preview                强制下载预览版本
 --output   -o      PATH  下载路径或文件
 --help                   Show this message and exit.

少量批量下载使用标准编号并列
openstd_spider download "GB/T 10781.5-2025" "GB/T 4354-2025" "GB/T 5844-2025"

大量批量下载读取文本文件获得下载目录
openstd_spider download-from-file xxx.txt
```

```bash

```
### 🔨Building

克隆项目源码（可选）

```bash
git clone https://github.com/cyathea-zkx/OpenSTD_Spider.git
```

或从 Release 中下载源码包

安装项目依赖，请确保已经安装 pdm

```bash
pdm install
```

打包构建项目

```bash
pdm build
```

安装构建包到全局（可选）

```bash
pip install dist/openstd_spider-xxx.whl
```


## ⚠️Disclaimers

本项目以 GPL-3.0 License 作为开源协议，这意味着你需要遵守相应的规则

本项目仅适用于学习研究，任何人不得以此用于盈利

使用本项目造成的任何后果与本人无关

# OpenSTD_Spider

国家标准全文公开系统下载工具

OpenSTD_Spider 是一个用于下载国家标准委“[国家标准全文公开系统](https://openstd.samr.gov.cn/bzgk/gb/)”公开标准文件的工具，集成搜索、元数据查询、PDF 下载三个功能，可以使用 CLI 调用，也可作为库通过 API 接口供其他程序调用。

本项目下载及输出的内容均从“[国家标准全文公开系统](https://openstd.samr.gov.cn/bzgk/gb/)”网站上获取，使用其输出内容必须遵守相关规定，以及国家标准和国际标准的版权。

## 🚀Quick Start

需要 Python 版本 >= 3.10

TODO: 通过 PyPi 安装

也可以通过[源代码构建](#🔨Building)

## 💻Usage

### 搜索公开标准列表

使用方式为子命令 `openstd_spider search`

浏览最新公开的标准文件

```bash
openstd_spider search
```

也可以通过关键字或标准编号搜索

```bash
# 搜索标准编号
openstd_spider search 'GB 18030'
# 搜索关键字
openstd_spider search '电动自行车'
```

输出的表格底部会显示索引信息，可使用`-p`参数翻页

### 查询标准元数据

使用方式为子命令 `openstd_spider info`

元数据包含标准编号、中英文名称、分类编号、发布及实施日期、主管及归口单位等。

通过精确的标准编号（非精确的标准编号最多一个匹配项）或页面的 URL 可以进行查询。

```bash
# 通过精确标准编号查询
openstd_spider info 'GB 18030-2022'
# 通过页面 URL 查询
openstd_spider info 'https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=72969DAA3DA5795AD2163528FF57166C'
```

### 下载标准 pdf 文件

使用方式为子命令 `openstd_spider download`

标准文件有两种公开方式，分别是仅允许预览和允许下载，这两种方式均可进行 PDF 文件下载，优先以直接下载方式下载，使用预览方式下载将无任何目录索引及可复制文本。

对于禁止预览和下载的标准文件，本项目无法下载。

通过精确的标准编号（非精确的标准编号最多一个匹配项）或页面的 URL 可以进行下载。

```bash
# 通过精确标准编号查询
openstd_spider download 'GB 18030-2022'
# 通过页面 URL 查询
openstd_spider download 'https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=72969DAA3DA5795AD2163528FF57166C'
```

默认情况下 PDF 文件将下载到当前目录，并以标准编号命名，也可加`-o`参数指定输出路径或文件名。

## ✨Features

- 集成搜索、元数据查询、PDF 下载三个功能，通过子命令进行调用
- 元数据查询和 PDF 下载支持自动识别 URL 或标准编号
- 查询结果及下载状态以 TUI 方式在终端显示
- 自动识别下载时的人机验证码
- 预览方式下载自动拼接打乱的图块，并将图片生成 pdf 文件

## 🔌API

不仅可以通过 CLI 方式使用，也可以集成进其他项目，通过 API 调用

TODO: API 调用 Demo 及说明

## 🔨Building

克隆项目源码（可选）

```bash
git clone https://github.com/SocialSisterYi/OpenSTD_Spider
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

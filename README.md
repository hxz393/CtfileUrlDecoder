# 工具介绍

CtfileUrlDecoder 是一个批量解析城通网盘下载地址的工具。通过批量解析出直连下载地址，省去在浏览器访问、输入提取码、点击下载的重复步骤，节约人力时间。

界面预览：

![最新版本截图](https://raw.githubusercontent.com/hxz393/CtfileUrlDecoder/main/capture/ui.jpg)



## 使用限制

使用前须知条件如下：

1. **必须要有城通会员**。非会员只能单任务下载，且下载速度限制在 80KB/s，解析出来也没意义。
2.  **只支持单文件链接类型。**例如：https://url99.ctfile.com/f/13660000-723149000-b1800a?p=1230。旧城通网盘链接支持有限，文件夹链接可到页面获取批量下载地址。
3.  **城通有请求速度限制。**持续解析 400 条以上，会出现解析失败，需要等 2~5 分钟方可继续。可以设置请求间隔时间，来保持长时间作业。
4.  **下载地址有时效。**解析出来的下载地址有效时间为 12 个小时，超过时间未下载请重新解析下载地址。



## 下载地址

软件下载方式：

- 方式一：到 [release](https://github.com/hxz393/CtfileUrlDecoder/releases) 页面下载最新版的可执行文件，文件名为 `CtfileUrlDecoder.exe` ，下载完毕可直接打开使用。
- 方式二：[百度网盘](https://pan.baidu.com/s/1RK7uBqaqgqJHLJbadXI48g?pwd=6666)分流下载。

下载的压缩包，需要解压缩后运行可执行文件，否则配置将不会保存。



## 自行打包

手动编译需要事先安装好 `Python 3.10` 以上版本、`PyQT 5.15` 以上版本和 `pyinstaller` 软件包。其他依赖报缺啥装啥。

编译步骤如下：

1. 在安装有 `Git` 的主机上克隆项目。命令如下：

   ```sh
   git clone https://github.com/hxz393/CtfileUrlDecoder.git
   ```

   或者在 [项目主页](https://github.com/hxz393/CtfileUrlDecoder) 点击绿色`<> Code` 按钮选择 `Download ZIP` 选项，[下载](https://github.com/hxz393/CtfileUrlDecoder/archive/refs/heads/main.zip) 源码压缩包。下载完毕后用压缩软件或命令工具解压缩。

2. 使用命令切换到项目路径下面。

   例如在 Windows 系统下面，打开 `CMD` 命令提示符，输入：

   ```sh
   cd B:\git\CtfileUrlDecoder
   B:
   ```

   在 Linux 系统下面，通用使用 `cd` 命令切换到项目路径下面：

   ```sh
   cd /root/CtfileUrlDecoder
   ```

   如果使用 `PyCharm` 作为 IDE，可以直接在自带的终端栏目输入下面打包命令。

3. 使用 `pyinstaller` 命令编译打包成可执行文件：

   ```sh
   pyinstaller -F -w -i media/main.ico --add-data 'media/;media' CtfileUrlDecoder.py
   ```

   如果过程没有报错，可执行文件会生成到 `dist` 目录下面。



## 开源许可

本软件采用 [GPL-3.0 license](https://github.com/hxz393/BrutalityExtractor/blob/main/LICENSE) 源授权许可协议，若违背开源社区的基本准则，将开源项目据为私有用于商业用途，属于侵权行为，本人将追究法律责任。



# 工具使用

首次运行，需要手动获取城通网盘用户令牌（token），之后可以长期使用。用户令牌和电脑绑定，同个帐号不同电脑生成的令牌不同。如果在别地登录了帐号，本地保存的令牌会无法使用，可以重新在浏览器上登录城通网盘来激活。

## 获取令牌

请用 Chrome 浏览器，严格按照下面步骤执行：

1. 打开城通网盘[地址](https://www.ctfile.com/)，点击立即登录，输入会员帐号密码成功登录。

2. 打开一个旧版城通网盘链接，例如：https://u062.com/file/14797164-237412331。此时右上角会显示注册登录按钮。

3. 点击右上角登录，页面会自动跳转到已登录状态，不需要重新输入帐号密码。

4. 按 `F12` 打开开发者工具，刷新页面，等待页面加载完成。

5. 在网络标签页点击第一条请求，在右侧请求标头中，找到 `cookie` 字段，值类似于 `tempToken=88mxm7eue7y73j6y2h33f`。其中 `tempToken=` 后面的 22 位字符串就是我们需要的令牌。示例图如下：

   ![最新版本截图](https://raw.githubusercontent.com/hxz393/CtfileUrlDecoder/main/capture/get_token.jpg)

将令牌填入到工具的 `设置>基本>帐号 token` 中，点击确定保存。



## 运行解析

设置好令牌后，可以将要解析的城通网盘地址，粘贴到左边输入框。链接格式为：

```sh
https://url01.ctfile.com/f/34628125-771711816-13fa54 0000
```

或者：

```sh
https://url01.ctfile.com/f/13660405-878244288-582bbf?p=AA00
```

也可以通过文件或工具栏中的打开按钮，选择全是链接的文本文件。一行一个链接。

如果要解析的链接过多，请适当调大设置中的请求延迟时间，来降低被临时封禁的机率。



## 添加下载

城通网盘地址解析完毕后，可以筛选掉失败链接，再把下载链接加入到下载工具批量下载。或者保存解析出的下载链接到文本文件，供稍后使用。



# 常见问题

暂无。欢迎所有形式的贡献，包括但不限于提交问题、改进代码、提供使用反馈等。



# 更新日志

为避免更新日志过长，只保留最近更新日志。

## 版本 v1.0.0（2023.07.02）

发布第一个版本。
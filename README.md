# 简介
这是一个由杜赛开发的博客网站Django项目。

Python==3.6, Django==2.0, Bootstrap==4.0

网站链接在这里：[杜赛的个人网站](https://www.dusaiphoto.com)

包含博客、教程、读书、照片墙几个板块。

作者是一个光学工程师，编程是业余爱好。

这也是我写的第一个Django项目，欢迎各位前辈提出宝贵的意见。

有问题请联系作者：dusaiphoto@foxmail.com

# 使用方法
- 安装`requirements.txt`中的依赖项
- 修改`dusainet2/settings.py`中的所有需要账号密码的部分

# 注意事项：
静态文件layui.css/layui.min.css和editormd.css/editormd.min.css均有更改
- .editormd-preview-container, .editormd-html-preview修改了font-size和padding
- layui.css 删除了 .layui li; 增加了 .layui-fixbar li 中的 list-style-type

# 更新日志：
## 2018.12.09
- 优化代码结构及注释

## 2018.09.17
- 增加文章/评论API
- 表现优化

## 2018.09.13
- 常规表现优化
- 评论功能优化


## 2018.08.31
- 网站全面升级为https安全连接
- 优化多处页面显示效果
- 修复文章目录鼠标悬停显示bug


## 2018.08.29
- 重新解决文章正文偏右bug
- 增加404、500页面
- 优化搜索界面


## 2018.08.27
- 修改了介绍
- article-list显示优化
- editor.md代码块无法空行问题修复
- footer增加邮件联系图标
- 修复了固定块的显示问题
- 修复首页文章内容中链接不能正确换行
- 读书板块正文的移动端优化
- 修改了文章正文、目录等多处的样式
- 使用生产环境的引入（主要是editormd.min.css和editormd.preview.min.css）
- echarts/leaflet静态资源cdn加速；


## 2018.08.23
- 去除editor.md代码块的序号
- 修复图库上传图片 500 错误


## 2018.08.22
- 删除urls中jet需要的谷歌引入
- 修正有序列表在md中无法正确显示的问题
- 修正读书文章详情中作者错误问题
- 优化article-list显示
- 增加‘奶茶小筑’adv


## 2018.08.21
- 修正下一篇教程文章错误的bug
- 修正读书版块作者错误
- 优化读书响应式布局
- 增加济南斯派克adv
- 优化微博登录窗口显示
- 读书的书籍图片boxshadow去除
- 优化sm端adv显示

## 2018.08.20
- 图库改倒序
- 添加教程副标题
- 增加图库分页

## 2018.08.15
- 网站上线

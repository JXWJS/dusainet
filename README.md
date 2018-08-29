# 简介
这是一个由杜赛开发的博客网站Django项目。

网站链接在这里：[杜赛的个人网站](http://www.dusaiphoto.com)

里面包含博客、教程、读书、照片墙几个板块功能。

作者是一个光学工程师，编程是业余爱好。这也是我写的第一个Django项目，欢迎各位前辈提出宝贵的意见。

作者邮箱：dusaiphoto@foxmail.com

# 注意事项：
layui.css/layui.min.css和editormd.css/editormd.min.css均有更改
- .editormd-preview-container, .editormd-html-preview修改了font-size和padding
- layui.css 删除了 .layui li; 增加了 .layui-fixbar li 中的 list-style-type

# 更新日志：
## 2018.08.29
1. 重新解决文章正文偏右bug
2. 增加404、500页面
3. 优化搜索界面


## 2018.08.27
1. 修改了介绍
2. article-list显示优化
3. editor.md代码块无法空行问题修复
4. footer增加邮件联系图标
5. 修复了固定块的显示问题
6. 修复首页文章内容中链接不能正确换行
7. 读书板块正文的移动端优化
8. 修改了文章正文、目录等多处的样式
9. 使用生产环境的引入（主要是editormd.min.css和editormd.preview.min.css）
10. echarts/leaflet静态资源cdn加速；

## 2018.08.23
1. 去除editor.md代码块的序号
2. 修复图库上传图片 500 错误


## 2018.08.22
1. 删除urls中jet需要的谷歌引入
2. 修正有序列表在md中无法正确显示的问题
3. 修正读书文章详情中作者错误问题
4. 优化article-list显示
5. 增加‘奶茶小筑’adv


## 2018.08.21
1. 修正下一篇教程文章错误的bug
2. 修正读书版块作者错误
3. 优化读书响应式布局
4. 增加济南斯派克adv
5. 优化微博登录窗口显示
6. 读书的书籍图片boxshadow去除
7. 优化sm端adv显示

## 2018.08.20
1. 图库改倒序
2. 添加教程副标题
3. 增加图库分页

## 2018.08.15
1. 博客网站上线

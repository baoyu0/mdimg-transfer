---
title: test1
slug: test1
cover: ""
categories: []
tags: []
halo:
  site: https://jia.baoyu2023.top
  name: 3c93e483-91d5-4119-84c7-0c06d89b3aea
  publish: true
---

这个时候，`#AI 画画` 就会变成 `#AI` 的子集。

当你点进 `#AI` 这个 Supertag，你会看到 `#AI 画画` 的笔记节点也包含在其中。但当你点进 `#AI 画画` 这个 Supertag，则会发现只有带有 `#AI 画画` 这个标签的笔记节点才会出现。

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Supertag 的继承不止是类似 flomo 的多级标签嵌套，不是只能起到一个层级分类的效果，Supertag 继承的还有字段的选项值，这样一来不仅无需重复创建字段，连字段内的选项值也无需再次设置了。

并且 Tana 还有一个非常好用的快捷键 `Ctrl+E` ，在任意节点中可以唤出**临时输入窗口（Quick add）**，你可以在这个窗口输入任意笔记内容，并打上特定的标签，然后将其添加到当天的 Daily Note 中，从而**避免从当前的节点中跳出，以至于打断心流**。

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

你现在所看到的 **Supertag 只是 Tana 一切复杂功能的载体**，它不仅仅只是起到一个打标签和赋予结构化数据模板的功能，还有更多更加强大的用法，会在后面的内容逐一揭晓。

# 1- 动态搜索带来安全感

依然是单一颗粒度带来的优势，Tana 完善的动态搜索功能，能让你放心地在任何地方写下任何一条笔记。

首先我们可以将 Supertag 视作一种搜索，**任何地方的节点都会被同一个标签聚合在一起**，这样一来，你可以确信自己随手写下的 `#灵感` 有了一个最终的归处；你匆忙设定的 `#任务` 就算再怎么拖延，总有被重新拉起的那天；你认真记录的 `#电影` 和 `#书籍`，你买的 `#数码产品`，你正为之努力的 `#愿望清单` 都会被 Tana 用 Supertag 认真地收藏在一起，这就是动态搜索所能带来的第一份安全感。

在这个记录的过程中，**我们不用像 Notion 那样，总需要先找到那一个数据库才可以开始记录**，使用 Supertag 就能将这个节点「**发送**」到目标位置。

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

其次，**Tana 构建了一套极其丰富的动态搜索框架**，可以说是我用过的众多笔记软件之最。

不仅命令丰富，而且**搜索逻辑是可视化的**，比起 Obsidian 的 Dataview，Tana 更加易用，不用手搓代码，内置的命令提示不说详尽彻底，至少也能给每一个命令写几句简单说明。

这里唯一的缺点就是，Tana 同样并不支持中文界面，因此你很可能迷失在这些搜索命令上。

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

让我们先从最简单的搜索命令开始，假如我想搜索「**所有未完成的任务**」，该怎么做呢？首先输入一个问号 `?`，然后点击 Create search node，就可以打开搜索面板：

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

接下来我们直接在输入框内搜索 `#Task` ，以及内置的命令 `NOT DONE`，就可以将整个笔记库内所有未完成的任务搜索出来，很符合直觉，虽然前提是你得先知道有 `NOT DONE` 这样一个命令的存在。

![图片](https://mp.weixin.qq.com/s/www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate(-249.000000,%20-126.000000)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

接下来让我们增加一点难度，我想搜索「最近三天完成的任务，并且属于项目 A，且优先级为 P1；**或者**最近三天创建的任务，并且没有设置截止日期」。

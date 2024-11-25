# 1- 最强 AI 大纲笔记软件，Tana 能否超越 Notion

## 1.1- 本文太长，建议在电脑端阅读。加入 [知识星球](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247494690&idx=1&sn=0489b0a78f5f487e5cff4422e0e4edeb&chksm=e9a15bb9ded6d2af8d0016fb8b263337752f745b737577bd2e81e9fc5cadb5e766e480488e0c&scene=21#wechat_redirect)，可获得更好的阅读体验

## 1.2- 前言

使用 Tana 的第 1 个小时，我确信这将会是一款非常有趣的产品。

第一天，我察觉到它具有与 Notion 数据库相仿的潜力，也体验到了比 Logseq 更丝滑的大纲体验，以及比 Roam Research 更好看、更有质感的 UI 设计。第一个礼拜，我惊讶于这样一款完成度如此之高、AI 功能强大、搜索命令（Query）相当完善的产品，竟然还处在 Beta 阶段。

第十四天，我已经在 Tana 中构建了一个相对完整的笔记框架，并觉得就这么 **All in Tana** 似乎也不错。我想一定有人会问我，作为一名忠实的 Notion 拥趸，并且还是 [Notion 课程](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247499247&idx=1&sn=511360fe3a924daf67663f00ec5d16e0&chksm=e9a14a74ded6c36206183870761620a84be4ec978dadd1d254112b84401fef9b32a64af8a95c&scene=21#wechat_redirect) 的作者，我是不是要放弃 Notion 了？

直到今天，我确信自己对 Tana 已经有了基本的认知，足够向各位分享一些微薄的心得体会了，终于才写下这篇分享，希望能带你认识 Tana 究竟是怎样的一款工具。

它的好、它的坏，我将一并呈现于你。它该怎么上手、它能怎么用、它究竟适合谁、它能否真的替代 Notion 或者 Logseq、Obsidian 等工具，以及**如何更快地获得 Tana 的邀请资格**，这些问题看完全文你一定会有答案。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/a77b7268-d04b-42fb-b89d-ac3e2344eb74.png)

对了，这篇长文是用 Obsidian 写的，**很遗憾 Tana 并不支持 Markdown，也完全不适合用来写长文**，这是它众多缺点中的第一个。

## 1.3- Tana 的基础认知

### 1.3.1- 因何而特别

丝滑的大纲体验，加上细节之处相当优雅的动效设计，使得 Tana 能最快让人收获「**有审美、有质感**」的第一印象。然后接下来还会有数次惊呼「这也行？」的时刻，随着体验的逐步加深而解锁。

对我来说，这几次分别是：

1. 1\. 在体会到了 Supertag 的应用场景之广后
2. 2\. 在发现了 Tana 对 AI 工作流的理解之深后
3. 3\. 在创建了一个又一个条件苛刻的全局搜索命令后
4. 4\. 在使用各种命令按钮一键执行了复杂的工作流后
5. 5\. 在感受到 Tana 在移动端的便利性之后
6. 6\. 在与 Readwise 高效联动并获得了满足感之后

还有更多瞬间无法一一列举，我会在后面的内容里逐步为你揭开 Tana 的更多优秀特性，以及或许会将你劝退的诸多缺点。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/cb7017df-fc81-4863-b52e-a00e8522d94f.gif)

### 1.3.2- 一切都是节点

作为一款大纲笔记软件，Tana 中的一切都是节点，也就是说只有节点（Node）这一个笔记颗粒度，没有再单独划分文件夹之类的概念。如何理解，如何使用？

首先和所有的大纲笔记一样，Tana 的每一个节点都可以进入和退出（zoom in & out），还可以将任意节点以窗口形式左右或者上下并排放置，但目前还不能像 Obsidian 那样随意地上下拖动，也不支持多开窗口，因此自由度虽然有，但不多。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/82bb477d-7251-4f4d-86c9-9a3f542c76ac.gif)

一个能够很好地体现「**节点是唯一的笔记单位**」的特征是，你可以**为每一个大纲节点单独设置图标和封面**，就像 Notion 中的一个个独立笔记页里的 Icon 和 Banner。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/6dcbb704-e84d-4dfb-a3bb-fc19e76eb20e.jpeg)

并且每一个节点都带有一系列的元数据，如下图所示

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/a7b41407-ecf1-49df-b643-b89f3d4be968.png)

这意味着，你在 Tana 中创建的**每一个大纲节点，都至少带有 13 个隐藏的元数据**，然后我们可以手动选择这个节点要显示哪一些元数据。

例如受这篇文章（*https://muki.tw/tana-life-log/*）的启发，我开始尝试记录 Life Log 这个东西。虽然我经常一天到晚忙到没边，但精力过于分散，因而很难具体地回想起自己这一天到底都做了什么，导致每天睡觉前总会在身心俱疲中感到空虚。

所以我在 Tana 中创建了 Life Log 这个模块，并选择开启 `Created Time` 这个元数据，然后在 Life Log 这个主节点之下的所有子节点，一旦创建就会自动显示创建的时间戳，这样就可以让我对自己在什么时间做了什么事有一个大概的印象。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/6e1d72e5-b3ce-4678-bb86-c35ea3c2482a.gif)

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/d753ba70-6654-4c33-8417-9413c02676b5.jpeg)

**我企图通过这种方式来重新获得对生活的掌控感**，目前感觉还算不错，因为我只需要忠实记录「刚才做了什么」就好，大纲节点的时间戳会在我分心玩乐的时候，给我迎头痛击，让我赶紧回到工作上。

然后在一天结束后，我还可以让 Tana AI 一键将这一天鸡零狗碎的事**自动分类**成工作、生活以及娱乐三个大的类别，具体怎么实现会在文章后面细聊。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/95fc528a-a474-4cda-b3ea-8146bbe54211.png)

节点是唯一细粒度的另一个重要用法，体现在你想引用某段笔记时。

在 Obsidian 中，一般我们只能引用一篇文章的标题，或者文章内某个段落的大标题，如果你想引用「**具体的某个段落**」是很麻烦的一件事。而 Notion 虽然具备块引用功能，但你无法直接通过搜索的方式做到，你需要先定位到这个块的页面，然后手动复制块的链接，再回到目的地粘贴并提及（Mention）才行。

但因为 Tana 只有节点（Node）这一个笔记单位，所以你可以在任意地方，直接使用符号 `@` 来搜索并引用笔记库内的任意节点。引用之后的节点就像 Notion 的 synced block 或者 Logseq 的 embed block 一样，**一处修改、处处同步**。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/71ca2215-00e9-4ff4-b4da-9b0d82f799e6.png)

值得一提的是，**Tana 的中文搜索效果在一众外国产品中，竟然意外的准确**，对中文分词的支持度非常高。

现在，当某个节点被引用了，它的右侧就会显示被引用的次数，左键点击这个数字，还可以展开所有引用过它的节点：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/0ded6247-3d69-474d-8f9d-d770ae05a135.png)

如果你引用了某个节点，还可以 Shift+ 左键点击，就可以直接在下方**完整地打开这个节点**，然后直接对原节点进行查看或者编辑的动作，非常便利。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/9fd89479-78bd-4ad7-8a6a-b6e0492a15b0.gif)

最后，Tana 虽然也有侧边栏目录结构，但它不是 Obsidian 那样的侧边栏文件夹（文件夹只能起到收容文档的作用），它依然是一个个放置在侧边栏的节点（Node）。

所以，如果你是第一次使用 Tana 的用户，当你产生了「**笔记到底要放在哪里**」的疑问时，我的首要建议是，先把侧边栏节点当成文件夹，然后创建几个你常用的笔记类型，如此能帮助你更快地熟悉这款产品，而不至于迷失在各种功能里，却写不下几行笔记。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/7c3955c2-1925-441b-a286-34396ff6dddf.jpeg)

等到你足够熟悉 Tana 的功能，你会发现，尽管 Tana 只有节点这一种笔记单位，但它的上限真的非常高，因为还有节点视图（view）这一个功能，可以将大纲节点转化为我最喜欢的侧边栏目录（Side menu) 的效果。

光是这一点，就足以将 Tana 与其他大纲笔记很好地区分开来。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/53b44435-649c-478c-9f8a-850f4d15265b.gif)

秩序从混乱中生长

现在我们已经知道，Tana 的笔记就是由一个个节点构成的，并且因为有了侧边栏目录功能，所以我们完全可以将父节点当成是一个文件夹，而子节点则是文件夹之中的一个个文件。

实际上这么使用完全没有问题，我认为不论再怎么自由的信息结构都少不了**树状目录**的帮助，这一定是对大多数人来说最容易上手的信息管理模式。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/575d8ade-256c-4c72-b2d3-3ba529e7a5a4.jpeg)

但 Tana 有两个更自由的模块，分别叫 Inbox 和 Daily Note，它们可以帮助你实现「**先记录，再分类**」的需求。如果你用过的笔记软件不在少数，那么应该对这两个概念不陌生。

每天打开 Tana，首先呈现给你的是**以当天日期作为标题的页面**，你可以在这个页面记录任何你想记录的东西。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/7ace12f3-837a-43f3-93cd-e297de218d80.jpeg)

但如果所有内容都记录在 Daily Note 中，时间一长必然会有很多重要的想法、任务、灵感或者待办事项等，遗失在每一天的日记里。例如 Heptabase 虽然也有 Journal 功能，但因为目前不支持行级标签，所以很多时候我并不会选择在 Journal 中记录碎片信息，因为太容易忘记和遗失。

所以 Tana 带来了**超越传统标签功能的 Supertag**，它为每一个笔记节点带来了近似 Notion 数据库的特性。使用方法也很简单，就像过去任何一次打标签一样，在笔记节点上使用符号 `#` 即可：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/54245f5a-0e14-4366-8b1a-164d9cbebc77.png)

接下来只要我点击这个标签 `#硬件数码`，所有被打上同一个标签的节点，都会被汇总到一起，并以列表（List）的默认形式呈现，如下图所示。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/cc534c52-af38-4891-95fb-ec3bc9d48299.jpeg)

这就是 Supertag 的第一个特性，也是最基本的特性，即可以**一键聚合任意位置带有相同标签的笔记节点**。但这和其他具备标签功能的笔记软件相比，似乎没有太大的特殊之处?

幕布也可以对每个节点打标签，但点击标签后只能在当前文档范围内进行索引和过滤；Obsidian 具备标签索引用，但标签只能对文档层级进行过滤；Logseq 具备标签索引，但 `#Tag` 和 `[[Tag]]` 是等价的，并且结构化管理的手段较弱，不如 Tana 易用。

Hetpabase 的标签用法某种程度上与 Tana 更加相似，只不过 Tana 聚合的是任意位置的「节点」，而 Heptabase 聚合的则是任意白板中的「卡片」。你可以阅读 [这篇文章](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247499166&idx=1&sn=fb287c99bcee7f720615f078625e47ab&chksm=e9a14a05ded6c313795eb6099c936380f38684661dc4114e6d581766e8719c8836c6adc0058e&scene=21#wechat_redirect)，了解关于 Heptabase 的更多介绍。

Supertag 的第二个特性是，你可以为任意节点设置固定的字段值（Field），这个字段的概念类似 Notion 的字段（Property）。

例如，我可以为 `#硬件数码` 这个标签设置以下几个默认字段：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/2db8cae1-cdfb-4d8d-8901-70e9224d5ee9.png)

那么当我给任意笔记节点打上这个标签，这个节点下方就会出现这些字段让你填写。所以我们也可以将 Supertag 理解成大纲节点的一种内容模板。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/1ef62eaa-86a4-4020-ad14-a8b22081000c.gif)

当然你也可以提前为这些字段设置默认的值，例如将 `#Task` 的 Status 设置为默认的 To-do。

Supertag 描述的是这个节点的本质「是什么」，而字段（Field）描述的则是这个节点的属性「有什么」，即这条信息有哪些最基本的构成要素或者特征。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/c96b093e-faf0-4192-853c-2f63151f825a.png)

如果你用过 Anytype 的话，Supertag 类似 Anytype 中的对象（Object），而 Field 则类似 Anytype 中的 Relation，你可以阅读 [这篇文章](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247500420&idx=1&sn=083542e6d1e7d8cdf058f34a5f9a304f&chksm=e9a1751fded6fc09763fdeeb4bb15e4d4a59cccfaa77da27c32a17046fb5c6f1c713c8ba3df2&scene=21#wechat_redirect)，了解关于 Anytype 的相关内容。

但这里有个很关键的区别在于，当你在 Anytype 中修改了对象的 Relation，这些修改无法追溯到先前已经创建的对象，在我看来这是个比较大的缺陷。而 Tana 的 Supertag 不论是添加还是删除 Field，都会对所有带有相同 Supertag 的节点生效。

例如下图，我在右侧的 `#TEST` 这个 Supertag 中添加了一个新的字段「日程日期」，可以看到左侧已经创建的「测试」节点立刻就新增了这个字段。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/3a7794f8-ec56-4026-999a-b4fb30e8f67c.gif)

并且 Tana 的一个节点不止可以拥有一种定义（Supertag），只要你想，你可以打上任意多个 Supertag，并让这个节点拥有不同 Supertag 所预设的不同字段。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/75e6ab0d-3e31-4792-85c6-0bb727e93819.png)

现在 Tana 的节点在 Supertag 的帮助下有了类似 Notion 的字段和列表视图，更进一步的，它也可以拥有像 Notion 一样的表格、画廊或者日历视图，你可以自由地在不同视图（View）之间切换。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/913336aa-52f2-40ff-ba07-b5a800005c7b.gif)

再举个例子，我可以在任意位置创建任务节点并赋予它 `#Task` 的标签，只要点击 `#Task` 这个标签按钮，就可以集中管理整个笔记库内的所有任务了：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/42168a70-e184-404b-a053-084ff674c998.gif)

当然要想获得精确的过滤和分组效果，就需要提前设置好各种字段（Field）与分组条件，这点跟 Notion 的数据库是一样的。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/3a8de956-4a91-47b0-a739-9815db15e8f7.png)

同时，Tana 的 Supertag 还具有「继承」的功能。

例如 `#同事` 或 `#朋友` 可以继承 `#联系人` 的字段，`#文章` 或者 `#视频` 可以继承 `#作品` 的字段， `#工具` 或者 `#网站` 可以继承 `#资源` 的字段。

如何理解和使用呢？让我来举个简单的例子。

起初你只是对 AI 这个庞大的主题感兴趣，所以你创建了一个名为 `#AI` 的 Supertag，基于你的理解，你认为在这个 Supertag 中至少要具备以下几个字段：

- • **描述**：对笔记内容的简要说明。
- • **应用领域**：AI 技术应用的具体领域，如医疗、教育、艺术等。
- • **技术类型**：涉及的 AI 技术类型，如机器学习、深度学习、自然语言处理等。
- • **发展趋势**：当前 AI 技术的发展趋势和前沿动态。
- • **挑战与问题**：AI 技术面临的挑战和需要解决的问题。
- • **相关资源**：参考的文章、论文、视频等资源链接。

所以你很自然地在 `#AI` 这个 Supertag 中设置了这几个字段（Field）：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/84ac9826-d9a9-4a9f-885c-c3b4806a7e76.png)

例如：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/5e237b8c-c566-467c-8ac9-33390ae11419.jpeg)

但是随着涉猎的加深，单一标签所覆盖的范围实在太大，你需要范围更窄的标签来划分不同细分领域的内容，于是你又相继创建了 `#AI 画画`、`#AI 搜索` 、`#AI 写作` 等标签。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/6b513afa-fa5b-40f2-9c23-90b04668a284.png)

这个时候你发现，`#AI 画画` 需要有「绘画工具」、「风格类型」、「算法模型」等字段需要新增

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/303ac594-5be8-4e96-ad97-b51aeaa26df4.png)

但同时也需要 `#AI` 这个 Supertag 所拥有的「应用领域」、「发展趋势」、「挑战与问题」等字段。这个时候就可以用到 Tana 的继承功能，只需要让 `#AI 画画` 继承（Extend from） `#AI` 已经设定好的字段即可。

如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/caa8acac-8e0f-40d7-b04c-bd9e2a5a6c7f.gif)

继承结果如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/b05ecf9f-8d29-43ac-a431-2567a2da8e31.png)

这个时候，`#AI 画画` 就会变成 `#AI` 的子集。

当你点进 `#AI` 这个 Supertag，你会看到 `#AI 画画` 的笔记节点也包含在其中。但当你点进 `#AI 画画` 这个 Supertag，则会发现只有带有 `#AI 画画` 这个标签的笔记节点才会出现。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Supertag 的继承不止是类似 flomo 的多级标签嵌套，不是只能起到一个层级分类的效果，Supertag 继承的还有字段的选项值，这样一来不仅无需重复创建字段，连字段内的选项值也无需再次设置了。

并且 Tana 还有一个非常好用的快捷键 `Ctrl+E` ，在任意节点中可以唤出**临时输入窗口（Quick add）**，你可以在这个窗口输入任意笔记内容，并打上特定的标签，然后将其添加到当天的 Daily Note 中，从而**避免从当前的节点中跳出，以至于打断心流**。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

你现在所看到的 **Supertag 只是 Tana 一切复杂功能的载体**，它不仅仅只是起到一个打标签和赋予结构化数据模板的功能，还有更多更加强大的用法，会在后面的内容逐一揭晓。

### 1.3.3- 动态搜索带来安全感

依然是单一颗粒度带来的优势，Tana 完善的动态搜索功能，能让你放心地在任何地方写下任何一条笔记。

首先我们可以将 Supertag 视作一种搜索，**任何地方的节点都会被同一个标签聚合在一起**，这样一来，你可以确信自己随手写下的 `#灵感` 有了一个最终的归处；你匆忙设定的 `#任务` 就算再怎么拖延，总有被重新拉起的那天；你认真记录的 `#电影` 和 `#书籍`，你买的 `#数码产品`，你正为之努力的 `#愿望清单` 都会被 Tana 用 Supertag 认真地收藏在一起，这就是动态搜索所能带来的第一份安全感。

在这个记录的过程中，**我们不用像 Notion 那样，总需要先找到那一个数据库才可以开始记录**，使用 Supertag 就能将这个节点「**发送**」到目标位置。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

其次，**Tana 构建了一套极其丰富的动态搜索框架**，可以说是我用过的众多笔记软件之最。

不仅命令丰富，而且**搜索逻辑是可视化的**，比起 Obsidian 的 Dataview，Tana 更加易用，不用手搓代码，内置的命令提示不说详尽彻底，至少也能给每一个命令写几句简单说明。

这里唯一的缺点就是，Tana 同样并不支持中文界面，因此你很可能迷失在这些搜索命令上。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

让我们先从最简单的搜索命令开始，假如我想搜索「**所有未完成的任务**」，该怎么做呢？首先输入一个问号 `?`，然后点击 Create search node，就可以打开搜索面板：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

接下来我们直接在输入框内搜索 `#Task` ，以及内置的命令 `NOT DONE`，就可以将整个笔记库内所有未完成的任务搜索出来，很符合直觉，虽然前提是你得先知道有 `NOT DONE` 这样一个命令的存在。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

接下来让我们增加一点难度，我想搜索「最近三天完成的任务，并且属于项目 A，且优先级为 P1；**或者**最近三天创建的任务，并且没有设置截止日期」。

让我们先来分解一下这个搜索需求：

**条件一：**

- • 是一个任务
- • 最近三天内被完成
- • 属于项目 A
- • 优先级为 P1

或者

**条件二：**

- • 是一个任务
- • 最近三天内被创建
- • 没有设置截止日期

这个搜索命令如下图所示，可以看到最左边的是一个绿色的 `OR` 命令，表示蓝色和粉色只需要满足其中一个即可。再具体看到蓝色或粉色部分，左边开始是一个 `AND` 命令，表示 `AND` 右边的所有命令都需要同时满足才行。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这个时候你可以看到搜索框的最下方有一行系统提取出的搜索命令，你可以对照检查是否符合需求，或者点击右下角的 Run once 命令，测试这个搜索命令是否可以正确执行，确定无误后再点击右下角的 Done 按钮，就可以保存这个搜索命令。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

现在让我们再次对动态搜索命令提高要求，我的需求是，**在整个笔记库内**搜索：

1. 1\. 属于项目 A 或项目 B 的任务
2. 2\. 优先级为 P1 或 P2
3. 3\. 截止日期在未来一周内
4. 4\. 但不包括已完成的任务
5. 5\. 也不包括指派给小明的任务

整个搜索命令包含了 AND、OR 和 NOT 等命令逻辑，如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

构建完毕的动态搜索命令只会在**展开节点时执行搜索**，所以不用担心动态搜索一直占用系统资源。然后你也可以将搜索结果切换到表格、画廊或者日历视图，以获得更好的阅读效果。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在搜索结果中，你可以点击并进入任意一个笔记节点，然后查看更详细的笔记内容

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

也可以将这个搜索节点（Search node) 复制并粘贴到任意地方，就像 Notion 创建镜像数据库一样。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

尽管 Notion 的数据库也能构建相当复杂的分组过滤效果，但其过滤的对象仅限于当前的数据库，无法扩展到整个笔记空间。而 Tana 的搜索范围则可以覆盖到整个笔记库的所有笔记节点，并且很重要的一个特性是，**在 Tana 中，我们是可以搜索特定字段或者字段的值的**。

什么意思，有什么意义？

假设在 Notion 中，你在多个互相独立的数据库中都创建了 Status 这个字段，现在你想筛选出所有数据库中，所有 Status 是 In Progress 的页面，然后统一用日历视图进行管理，Notion 能不能做到？

或者，你用**不同的数据库**来管理购买的数码产品、收藏看过的电影电视剧、记录游玩过的地方，现在你想创建一个数据库，用来实现「人生的动态轨迹」这一个需求，以时间线的方式来汇总每天都做了什么事情，Notion 能不能做到？

答案是都不能，虽然 Notion 有 Home 视图，但我认为依然是不可用的状态。但在 Tana 中，你只需要在搜索框内输入这样一串命令，所有包含了 Status 这个字段并且值是 In Progress 的节点就都会出现了：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

我还可以在搜索框内，将搜索条件设置为：

- • 拥有「备注」这个文本字段
- • 并且字段的值包含「重要」这个关键词（**也支持正则表达式**）

或者将搜索条件设定为：

- • 是否包含了字段？
- • 是否包含某个字段？
- • 某个字段是不是空值？
- • 是否包含标签？
- • 是否包含图片、音频、视频等元素？
- • 是不是一个搜索节点？
- • 是不是一个命令节点？
- • 是不是被设置为在线发布状态？

或者：

- • 限定创建的时间范围（Created time）
- • 限定完成的时间范围（Done time）
- • 限定编辑的时间范围（Last Edited time）

并且当你点击某个字段的值，你会发现所有用过这个值的节点，也都会被全部罗列出来，这也是「**Tana 的一切都是节点**」的最好体现。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

我必须得再次强调，Tana 的搜索自由度实在是我目前用过最丰富、最全面的一款产品，只要符合搜索条件，不论放在哪个犄角旮旯都可以被找到，这就是笔记软件所能带来的某种安全感。

但是高自由度也会带来高门槛，虽然 Tana 的搜索查询比 Logseq 的 Query 或者 Obsidian 的 Dataview 好用，但论易用度还是远不如 Notion 打磨了这么久的数据库。

当然本文仅能对 Tana 最基本的搜索命令做简单介绍，无法覆盖其完整能力的十分之一，你可以在这份官方文档（*https://tana.inc/docs/search-nodes*）中查看关于 Search Node 的更多介绍。

### 1.3.4- AI 命令是真正的护城河

Supertag 虽然是 Tana 的重头戏，但我觉得模仿 Supertag 的门槛并不算特别高，甚至会让人乍一看觉得它只是 Notion Database 的模仿者。而 Obsidian 的 Properties 也能在某种程度上实现这一功能，再加上 Dataview 插件的加持，让不少用户继续高呼「Obsidian 就是最强笔记软件」似乎也不算过分。

然而深度体验之后，**我觉得 Tana 的 AI ，以及配合各种命令（command node）所构筑的工作流才是它真正的护城河**。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

首先和 Notion 一样，在 Tana 的任意一个空白节点中**按下空格键**，就可以唤出 AI 问答窗口，然后输入任意问题，让 Tana AI 进行回答，并且回答的速度非常快。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**你也可以使用 @ 符号，快速引用任意一个笔记节点**，然后让 Tana AI 根据这个节点的内容进行回答。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Tana AI 还支持文生图功能，并且使用的是 DALL-E 模型

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

生成的图片效果如下

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

除此之外，Tana AI 还可以批量选中笔记节点，然后用「**Generate icon**」命令让 AI 为这个节点生成一个匹配其内容的 Emoji 图标，让这些节点更加醒目和好看。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

还可以让 Tana AI 根据当前节点的内容，生成一个 Banner 图（当然也可以自定义 Prompt）。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

除了可以在大纲节点层面使用 AI，Tana 和 Notion AI 一样也支持在字段层面使用自定义的 Prompt。

先别管为什么要让 AI 来写，假设我需要在笔记库中为这些玩过的游戏写一篇游玩心得，大概意思如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后我们可以在「游玩心得」这个字段（Field）中，设置一个自定义的 Prompt，让 Tana 根据现有的字段信息，进行 AI 创作：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

生成的效果如下图所示，只要你给的 Prompt 足够清晰，很多时候 Tana AI 都能给出符合需求的答案。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

当然如果 Tana 的 AI 只能做到以上这些，那它并不能和其他产品划分界限。Tana 的 AI 必须要和它的命令节点（Command node）搭配，才能发挥最强的效果。

我们还是先从 Notion 的 Button 开始讲起，它可以封装一系列复杂的动作组合，不过动作的对象是页面和数据库字段，且执行的动作类型比较有限，例如创建和打开页面，以及修改字段的值等基础操作。

你可以阅读这篇文章（*https://sspai.com/post/81971*），了解关于 Button 的详细介绍。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Notion Button 的遗憾有这 4 个：

1. 1\. 无法全局调用，只能在特定位置点击按钮
2. 2\. 无法全局应用，只能对特定的页面或数据库生效
3. 3\. 无法移动页面
4. 4\. 无法调用 Notion AI 参与工作

而 Tana 再一次受益于「**一切都是节点**」的这个特性，使得**命令本身就是一个节点**，同时这个节点可以在任意地方被调用，也可以对任意节点发挥效果。并且命令节点（command node ）内置了超过 30 个命令，不同命令可以组合在一起，创建出不同的工作流。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

首先，Notion Button 具有的基础命令类型 Tana 都有，例如

- • 编辑字段属性
- • 插入新的节点
- • 创建新的页面（节点）
- • 打开页面（节点）或链接

例如我可以在 `#Project#` 这个 Supertag 中，创建三个按钮，用来快速地更改当前项目的优先级

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

命令点击效果如下：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

我也可以将「插入字段」这个动作绑定在特定的 Supertag 中，这样就可以在需要的时候再点击按钮，因为有时候可能并不需要将所有字段都显示出来。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

同时我们也可以将特定的 AI 命令（Prompt）封装在某个动作按钮中。

假设我经常记录灵感、想法、研究方案，或者记录任何存在大量思考或反思空间的笔记，如下图这些（AI 生成案例）：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

那么我可以创建一个包含了特定 Prompt 的 AI 命令，如「**生成 3 个赞同观点与反对观点**」

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

创建完毕后，这个命令就可以在 Tana 的任意地方被调用。

方法也很简单，对需要提问的节点使用全局快捷键 `Ctrl+K` ，然后搜索并点击创建好的 AI 问答命令，就可以让 AI 根据选中的节点生成 Prompt 指定的内容：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

上面这个例子少了一些便利性，因为每次都需要使用 `Ctrl+K` 命令来唤出搜索框，然后再去检索那些提前创建好的命令。假以时日，当这些命令越来越多，你甚至可能会忘记自己都创建过哪些命令。

所以 Tana 提供了一个非常强大的功能，我可以将「生成 3 个赞成与反对意见」的命令，与 `#观点` 这个 Supertag 进行绑定，只要我在任意节点上添加了 `#观点` 标签，这个命令按钮就将自动出现，然后点击就可执行。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

具体效果如下：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

如此一来，我们就将命令与 Supertag 绑定在了一起，现在 Supertag 既能定义当前的节点，又能为当前节点带来高度自定义的命令按钮。

但即便是这样，添加完标签后还是需要再手动点击一次按钮，有没有更加便利的方法，让我们添加完 Supertag 之后就自动执行这个命令呢？

当然是有的，Tana 的 Trigger on added 功能就可以实现这个需求。只要将这个创建好的命令复制（Ctrl+C）然后粘贴（Ctrl+V）到下图所示的框内：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

那么当你添加了这个 Supertag，就会同时**自动激活**这个 AI 命令

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

另外，有 「Trigger on added」的话，自然也有「Trigger on removed」，限于篇幅本文就不再进一步展开了。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

最后 Tana AI 的高度可定制不仅体现在 Prompt 上，我们还可以指定 Tana 要使用哪一种 GPT 模型，可以添加自己的 API Key、或者是设置 AI 的 Temperature

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

并且还提供了一个可供测试 AI Prompt 的实验台，可以更便捷地测试 Prompt 的效果、调整 temperature，或者查看 Token 数等：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

下图罗列了 Tana 的更多的命令，我会在后面的实操案例中继续展开介绍。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.3.5- 移动端的雏形

Tana 目前虽然有移动端，但只支持信息的快速录入，而不支持在移动端上查看或者编辑笔记，功能完整的移动端仍在开发中，是 Tana 团队今年的工作重点。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

不过现阶段的移动端叫 Tana Capture，顾名思义就是暂时只支持快速捕捉功能。

它将文字、音频、照片以及扫描等信息的录入单独做了一个按钮，我个人非常喜欢这样的设计，因为我个人从来不用手机端处理重度的文字信息，只要能有一个快捷的输入窗口就足够了，而 Tana 在这点上就做得就已经足够可用。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

以语音信息速录为例，当我在手机上录完语音，Tana 桌面端就会在当天的 Daily Note 中将这段语音转录成文本，且根据语音内容自动生成标题和摘要

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

展开这个语音节点后，会看到原始的语音片段，以及转录后的完整文本

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

从 Original 切换到 Items 这个标签后，还可以看到 Tana AI 将语音中可能存在的待办事项提取了出来，并自动打上了 `#Task` 的标签

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

另外目前通过 TestFlight 的方式，也可以提前在 iPhone 客户端上下载功能更完整的 Tana 移动端测试版，目前已经可以浏览所有的笔记节点，但暂不支持编辑节点，加载速度也相当慢，只能说还有很大的优化空间了。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.3.6- 一个理想笔记系统的雏形

一个理想的笔记系统必定千人千面，但不论是谁、不论哪种笔记需求，在我看来一个**合格的笔记系统**至少需要以下几个基础特性：

1. 1\. 快速录入
2. 2\. 高效分类
3. 3\. 精准搜索
4. 4\. 易于回顾

通过移动端、Daily Note 和 Supertag，Tana 实现了快速录入和高效分类的基础需求；通过丰富的搜索指令，又可以遍历整个笔记库，然后找到任何你需要的信息。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

但这显然离大部分人期望的「理想的笔记系统」有一段距离。我们需要更多的自动化，**让笔记在你需要的时候自动出现**；我们需要更多的 AI 智能，能够让打标签这样的繁杂任务自动实现；我们需要更开放的接口，让外部的信息可以更自由地与笔记系统内部信息进行交互。

所以，现阶段的 Tana 能做到哪些，以及做到了什么程度？

首先，Supertag 本身就是一种模板，所以我们可以设置默认的字段和字段值，例如我可以在 `#day` 这个 Supertag 中设置固定的日记字段，这样一来每天打开 Daili Note 界面，就可以快速地在日记模板中写日记：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在**将 Tana 与稍后读软件 Readwise 进行关联之后**，我还可以在 `#day` 中添加下图所示的字段：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后在这个字段中开启 Auto-initialize 中的 `to random node with this supertag` 功能

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这样一来当你每天打开 Daily Note 页面，就会自动随机刷新出 4 条你通过 Readwise 保存的文章，或者通过 Readwise 标记的文章高亮段落（当然条数也可自定义）。

如此一来，就可以让你在 Tana 中有更多的机会与「曾经认为重要的内容」重逢。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

另外 Tana 还有一个叫 Related Content 的功能，能够允许你在侧边（或底部）放置任何你希望呈现的内容。例如，当你**将 Tana 与谷歌日历关联之后**，你就可以在 Daily Note 中查看谷歌日历创建的日程：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

你也可以直接将符合条件的任务（`#Task`）直接拖动到时间线上，并且可以随意拖动时间线以修改任务的时间范围：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

还可以在 related content 位置创建一个搜索节点，搜索对象是所有未被完成的任务：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后将这个动态搜索节点放在 Daily Note 的底部，这样就可以在你每天打开 Tana 的时候，提醒你还有哪些任务未完成。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

所有的 Supertag 都可以具备 Related Content 这个功能，所以不止可以在 Daily Note 中设置快捷入口，还有以下案例供你参考。

例如在 `#作者` 节点中自动显示这名作者写过的书，或者在 `#项目` 中显示它所包含的 `#子任务`。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

你也可以在 `#选题` 的 Related Content 中，显示与当前选题相关联的 `#想法` 或者 `#待办` ，当然前提是你需要能够设置准确的搜索节点才行。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这有点像在 Notion 中使用 Relation 字段来构建页面之间的关联，但 Tana Related Content 的特点在于，它的检索范围是整个笔记库，检索的条件更加丰富，并且只要符合条件就自动关联，而 Notion 的 Relation 是限定在某个特定的数据库，并且需要手动选择以创建关联。

Tana 的 Supertag 既是一种结构化的内容模板，也是一道让不同信息可以更加自由沟通的桥梁，它不一定适合所有人，但对于我这样既喜欢大纲的灵活性，又需要 Notion Database 结构化管理能力的人，Tana 确实找到了一个潜力巨大的解法。

## 1.4- Tana AI 命令的基础应用案例

我个人使用 Tana 仅一月有余，且篇幅有限，很遗憾无法将它的所有特性都介绍完毕，接下来也仅能陈列一些简单的应用案例供你参考，但 Tana 远比本文肤浅的介绍来得强大，如果你不排斥大纲形式的笔记工具，我认为这款工具是值得一试的。

### 1.4.1- 用 AI 优化 Prompt

Open AI 在它的 Playground 推出了一个帮你优化 Prompt 的功能，简单来说就是用「提示词」将你的提示词变得更完善，让指令更清晰，让答案更准确，更符合预期，具体可见 @宝玉 XP 的 这个帖子（https://weibo.com/1727858283/OB3CC2uLw）：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

现在我将这段提示词全文复制后，直接放到 Tana 的 AI 命令中，是的 Tana AI 可以容纳至少数千 Token 长度的 Prompt

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后将这个 AI 命令绑定在 `#Prompt` 这个 Supertag 上，这样一来我就可以通过添加 `#Prompt` 的标签来快速生成一串经过 AI 优化后的提示词了。

效果如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.4.2- 与 Youtube 视频对话

Tana 内置了一个名为 `Get Youtube captions` 的命令，可以一键将 Youtube 视频的字幕扒下来

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

以我的这期视频（*https://www.youtube.com/watch?v=z-Q2YnvBN0c*）为例，字幕结果如下

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后你就可以右键点击这个字幕字段，并选择 AI Chat，然后就可以对这个视频进行对话或提问了：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.4.3- 博客文章生成器

**背景描述**

1. 1\. 有写文章、发博客的需求
2. 2\. 需要对文章进行 SEO 优化，即需要根据文章生成 SEO 标题、摘要、关键词等内容
3. 3\. 需要根据文章生成相应的封面配图

在我的 Notion 课程（*https://sspai.com/series/303/list*）文章评论区下，有非常多的读者提问，我也做出了各种各样的回答。现在我希望让 AI 根据我与读者的对话内容，自动创建一篇 Notion 技巧短文，然后放到博客上进行分发。

例如：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

现在，我可以在 Tana 的任意位置创建一个节点，然后打上我事先设置好的标签 `#AI Post` ，然后 Tana 就会生成几个我事先绑定在这个标签上的 AI 按钮：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

点开这个笔记节点，会发现这个节点下已经提前设置好了相关的字段

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后我会手动将评论区的读者问题，以及我的回答复制粘贴到相应的字段下

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

接下来，点击「生成文章」这个按钮，Tana AI 就会根据我事先设置好的提示词，将我提供的问题和答案改写成一篇文章：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后继续点击按钮，让 Tana 根据这篇生成的短文内容，来生成相应的 SEO 关键词：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

再让 Tana AI 根据生成的短文，提供合适的封面描述词

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

最后让 Tana AI 调用 DALL-E 模型，根据封面描述词来创建一张博客文章封面：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

完整的效果如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.4.4- 将日常记录分类

前文我提到过，我尝试用记录 Life Log 的方式来更好地获得生活的掌控感，但是记录的条目一多，有时反而会觉得更加混乱，因为没有分类、没有主次

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

所以我在 `#Life Log` 这个标签上绑定了一个 AI 命令，要求 Tana 将我每天做的事情分成 3 个类别，同时重复的事件不重复记录，而是用 X1、X2 的形式来表达：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

顺便一提，这有点像是 Arc 浏览器的标签 Tidy 功能。

### 1.4.5- 工作周报生成

假设我在 Tana 中，用 `#日报` 来生成每天的日报模板，并填写具体的日报内容

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后在日历视图中更直观地查看和管理

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

接下来我可以在「工作周报」这个节点中，创建一个搜索命令，搜索的结果是「展示本周创建的所有日报」，如下图所示：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后在 `#周报` 这个 Supertag 中创建一个 AI 命令，用来一键总结本周日报的所有内容：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

点击按钮的效果如下：

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

篇幅有限，本文无法再列举更多案例，但可以认为，Tana AI 适用于几乎所有需要用到 AI 来辅助的工作流，它可以使用更长的 Prompt 来提问，只要你的命令足够清晰，它所返回的答案将有很大概率符合你的需求。

## 1.5- Tana 的不足

虽然前面列举了 Tana 的种种用法，甚至不吝溢美之词夸赞各种特性，但要知道这个世界并不可能存在一款完美的笔记软件，Tana 同样有很多不足，在很多地方存在限制和妥协，我认为在你花时间尝试之前，有必要先知道以下这些事情。

### 1.5.1- 空间与资费

作为一款需要完全在线使用的云笔记工具，Tana 如果没有付费订阅， 将仅提供 500MB 的存储空间，且单个附件限制 5MB 大小。与此同时，Notion 免费用户虽然也限制 5MB 的单个附件大小，但 Notion 的**总容量是不设上限的**。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

就算你每个月花了 18 美元订阅了 Tana Core（年订阅则为每月 14 美元），也仅仅能获得 10G 的存储空间。虽然大纲笔记很少需要用到太大的空间（我的 Logseq 记了两年笔记也不过 1 G 大小），因为通常都只用来记录纯文本的笔记节点，但 10G 还是显得过于「小巧」了。

唯一的好消息是，Tana 的 18 美元订阅还包含了 AI 功能，就我个人体感而言，每个月 5000 的 AI 点数不太可能会用得完。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.5.2- 没有中文

这是一款只有英文界面的在线笔记工具，并且各种功能设置界面与传统笔记有巨大区别，如果你英文阅读能力不佳，那么你将不太可能在 Tana 中获得好的使用体验。

除此之外，Supertag 的各种设置选项、Command node 的内置命令、Search node 里的搜索指令都有一大串的英文，你需要在 Tana 的英文官方教程里来回翻找，甚至需要借助翻译软件，才能够明白指令的用途和用法。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.5.3- 学习曲线陡峭、社区内容贫瘠

学会使用 Supertag 只是入门 Tana 的第一步，一旦你开始探索「搜索节点」和「AI 命令」，仅靠 Tana 内部的简单提示，不太可能让你学会它的完整用法，因为缺少最关键的一环：如何将不同的功能用符合语法逻辑的方式组合在一起。

所以你需要开始翻阅 Tana 的官方文档，在 Youtube 搜索各种视频教程，但又因为 Tana 的用户人数实在不够多，讨论热度太低，所以分享教程的用户也很少，所以很多时候都得打开各种翻译软件来自学官方文档。

或者换个方式表达，在 Notion 社区内容如此丰富的前提下，如果你依然觉得 Notion 是一款相当难上手的笔记工具，那么 Tana 只会更复杂、更难上手。或者回忆一下你在 Obsidian 学习 Dataview 插件的历程，你还想再来折腾一遍吗？

于是到了某个节点你必然会产生这样一种反思：**花这么多少去学习一款笔记软件的用法，真的值得吗**？

所以我的建议是，如果你要尝试使用 Tana，首先确认自己有一定的英文阅读能力，其次需要具备足够的耐心来研究和试错，并在业余闲暇时间再做尝试，不要一开始就将其当成一款主力笔记工具来使用。

### 1.5.4- 导出格式受限

截至目前，Tana 只能导出 JSON 这一种通用格式，但对一般用户来说，就算能导出 JSON 文件也没用，因为根本看不懂。

作为一款完全在线的笔记工具，Tana 在数据的自主性上并不能给你充足的信心。我认为 Tana 最少也需要能像 Workflowy 那样导出 OPML 格式，这样至少能让我们将有限的笔记导入到幕布或者其他大纲笔记中。

但即便如此，Supertag 独特的信息结构势必不可能有另一款笔记软件能够承接，就像 Notion 的数据一旦导出，就很难再放回 Notion 本体一样。

所以如果你本身更中意 Logseq 或者 Obsidian 这样的纯本地笔记工具，如果你一定要能亲眼看到存储在本地的一个个 MD 文档才会有安全感的话， 那么 Tana 将完全不适合你。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 1.5.5- 大纲天然的局限性

大纲笔记在快速记录信息时有其独特的优势，比如整齐的排版和较小的记录压力。每次只需写下一个小点，不必像文档笔记那样写满整段，写起来更轻松，然而这种方式也存在一些问题。

在大纲笔记中，内容往往是分散的、独立的小点，因为不需要花时间考虑连接词和过渡句，书写的内容在起承转合上可能有所缺失，这使得大纲内容无法直接输出为连贯的文档，缺乏各个节点之间的衔接，阅读性会受到很大的影响。

大纲的每个节点都是对其下子节点的高度概括，自己对主节点的理解可能很清晰，但对读者来说可能缺乏必要的背景信息。相比之下，文档笔记要求内容以段落形式呈现，具有连贯的逻辑顺序。每一段都是一个完整的观点，需要考虑前后段落的衔接，符合阅读习惯。虽然写起来可能更累，但最终的内容更适合直接用于阅读和分享。

另外，大纲笔记的软件特性，使得内容组织上可能相对松散。虽然可以折叠段落，方便查看全文结构，也容易对自己写了多少内容产生成就感，但这并不意味着内容的深度和质量得到了保证，在需要生成连贯、完整的文档时，必然会带来额外的工作量。

![图片](https://pub-7527271c203848268f3702478ed765fc.r2.dev/e64854c3-aaed-4ad4-95ed-e93b586f5c12.html; charset=UTF-8)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 1.6- 对比其他笔记软件

以下对比完全主观，仅能代表我个人在笔记习惯上的偏好。并且不同产品的功能太多，必然无法一一对比，因此只能有针对性地挑一些我认为有可能产生对比的需求或场景来简要说说。

### 1.6.1- Notion

虽然 Tana 与 Notion 在本质上是完全不同的两款产品，但一定有人会问，Tana 的 Supertag 所构建的类似数据库的视图能替代 Notion 吗？这个问题需要分两种情况。

首先，如果你的数据库记录的是**任务、项目、流程、碎片灵感、思考、日记**等类型的信息，那么我认为 Tana 是可以有限地替代 Notion 的。这类笔记一般不会涉及到太过复杂的数据记录，对数据计算的要求较低，Tana 的 Supertag 完全有能力将这类笔记组织和管理好，通过设置不同的字段，然后对其进行分组、过滤、筛选，或者创建不同的视图等，我认为足够满足一般的笔记需求。

但如果你在 Notion 中记录的是电影、游戏、摄影摄像、游戏、图书馆里等需要用到大量的图片的内容，或者如果你在 Notion 中对**函数公式、Automation、通知提醒、分栏排版以及第三方应用联动**有刚需的话，那么 Tana 将不适合你。

说起来将 Tana 与 Notion 这样的庞然大物放在一起对比，其实已经有点不公平了，Notion 毕竟是 Notion，能完全替代它的产品并不存在。

但如果你不排斥大纲形式的笔记，也有一定的动手和研究能力，那么我认为是可以尝试一下的 Tana 的，因为它的录入速度要远快于 Notion，打开就可以记录，而 Notion 在各种场景下常常都需要先找到那一个特定的数据库，然后才能开始记录。

### 1.6.2- Logseq

Tana 与 Logseq 相比有哪些优劣势？

Logseq 的开发进度已经严重落后各大飞速发展的笔记产品，虽然数据库版本正在开发中，但速度还是太慢了。所以本文仅以 Logseq 当前的 MD 版本来看，它相比 Tana 存在的优势有以下几点，按照对我个人的重要程度排序：

1. 1\. 完全本地离线
2. 2\. 支持双向链接
3. 3\. 支持 PDF 阅读与标记
4. 4\. 支持 Markdown
5. 5\. 支持插件系统
6. 6\. 有白板
7. 7\. 有闪卡功能

以上功能除了双向链接之外，Tana 都不具备。所以如果你看中这些特性的话，那么 Tana 完全替代不了 Logseq。

但如果你在 Logseq 中更看重的是双向链接、块引用、块嵌入等**基础的双链功能**，那么我认为 Tana 在这些功能上的每一个细节、功能用法的灵活度、从这些功能衍生出来的应用场景、以及整体的设计审美都完胜 Logseq。

### 1.6.3- Obsidian

Obsidian 和 Tana 其实不存在替代关系，但可以成为互补关系。我在前面的大纲的局限性已经提到，大纲类型的笔记工具都不适合用来进行长篇写作，并且 Tana 作为纯在线的笔记工具，同时缺乏有效的导出手段，所以无法让人放心地将它当成严肃创作的工具。

所以如果你已经习惯了 Obsidian 的各种功能和用法，那么我认为没有必要切换到 Tana，因为并不能很直观地带来效率上的提升。但如果你希望尝试一款具有双链功能的大纲笔记，在你因为各种原因想放弃 Obsidian 的时候，再考虑 Tana 也不迟。

## 1.7- 结论

好的审美是一种相当稀有的特质，功能不够多、BUG 不够少都不是问题，我相信只要给够时间，总能慢慢变好。但没有审美的产品随着时间的增长和功能的增多，只会越来越糟糕、越来越混乱。

而坚定的产品理念、统一的功能逻辑则决定了一款产品的灵魂，也决定了后续的开发方向，那些还停留在基础实践层面的笔记工具，或者还只会抄抄捡捡的模仿者们，将无法确信自己的开发方向是否正确，只能通过市场来验证每一次的「模仿和试错」，永远也无法走在自己的道路上。

所以在我看来，Tana 是这样一款有足够审美的大纲笔记软件，有相当明确的开发理念，有较为强大的产品开发能力。在这一个月的使用过程中，我能感受到产品经理和设计师为了让整个工具变得更好用和更好看所花的各种心思，也能感受到程序开发为了实现各种功能逻辑所付出的心血。

这是一款好的产品，但也是一款相当难上手的产品，它有各种各样的缺点，但并不妨碍我对它的喜欢。因为我非常明白，这个世界并不存在一款完美的笔记软件，你要做的不是削足适履，必须用一款笔记工具来强迫实现 all in one 的需求，然后委屈了自己的各种习惯。你应该集各家之长，谁好用、谁在哪个地方有特长，就用它来解决具体的问题。

毕竟笔记软件只是工具，思考和创造才是最终目的。

当然如果你对大纲笔记和 AI 感兴趣的话，试一试 Tana 也无妨。目前需要在 Tana 的官网上填写你自己的邮箱，然后才能等待 Tana 给你发放激活资格。但你也可以在 Tana 的 Slack 频道发一段自我介绍，能更快地获得产品体验资格。

## 1.8- 往期推荐

1. [Logseq 的 5 种用法](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247485390&idx=1&sn=ed36284d8d7b1dcfce1e8208d84f6c83&chksm=e9a2b055ded539431644663a24418447f6bc85fffcd7dd23122428351d94a307b55cae479671&scene=21#wechat_redirect) [🔗](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247485390&idx=1&sn=ed36284d8d7b1dcfce1e8208d84f6c83&chksm=e9a2b055ded539431644663a24418447f6bc85fffcd7dd23122428351d94a307b55cae479671&scene=21#wechat_redirect)
2. [Obsidian 的 8 种用法](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247487978&idx=1&sn=8f2e8aa7357bf3659079e69c1902bbcb&chksm=e9a2a671ded52f6753f32c4d8c660873493aa86dcd60b525cb339cdc0c9e41899a05322d7841&scene=21#wechat_redirect) [🔗](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247487978&idx=1&sn=8f2e8aa7357bf3659079e69c1902bbcb&chksm=e9a2a671ded52f6753f32c4d8c660873493aa86dcd60b525cb339cdc0c9e41899a05322d7841&scene=21#wechat_redirect)
3. [Heptabase 系统测评](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247499166&idx=1&sn=fb287c99bcee7f720615f078625e47ab&chksm=e9a14a05ded6c313795eb6099c936380f38684661dc4114e6d581766e8719c8836c6adc0058e&scene=21#wechat_redirect) [🔗](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247499166&idx=1&sn=fb287c99bcee7f720615f078625e47ab&chksm=e9a14a05ded6c313795eb6099c936380f38684661dc4114e6d581766e8719c8836c6adc0058e&scene=21#wechat_redirect)
4. [Anytype 系统测评](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247500420&idx=1&sn=083542e6d1e7d8cdf058f34a5f9a304f&chksm=e9a1751fded6fc09763fdeeb4bb15e4d4a59cccfaa77da27c32a17046fb5c6f1c713c8ba3df2&scene=21#wechat_redirect) [🔗](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247500420&idx=1&sn=083542e6d1e7d8cdf058f34a5f9a304f&chksm=e9a1751fded6fc09763fdeeb4bb15e4d4a59cccfaa77da27c32a17046fb5c6f1c713c8ba3df2&scene=21#wechat_redirect)
5. [Notion 中文版来了](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247499476&idx=1&sn=4a626ce1a3f2819308a9eddb5162b568&chksm=e9a1494fded6c0591505ee3e3797c8d12ab6fb9370ebe4fc73085c60218b8262fe470bdb5d5c&scene=21#wechat_redirect) [🔗](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247499476&idx=1&sn=4a626ce1a3f2819308a9eddb5162b568&chksm=e9a1494fded6c0591505ee3e3797c8d12ab6fb9370ebe4fc73085c60218b8262fe470bdb5d5c&scene=21#wechat_redirect)
6. [Notion 离线模式前瞻](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247500649&idx=1&sn=63ede9a6c01cb34ddf0505dc9186a13f&chksm=e9a174f2ded6fde46ef998e0eceac577ff56be264ca7f616bffac5479e327cf453a6155241ad&scene=21#wechat_redirect) [🔗](http://mp.weixin.qq.com/s?__biz=MzI0ODIyNjU0OA==&mid=2247500649&idx=1&sn=63ede9a6c01cb34ddf0505dc9186a13f&chksm=e9a174f2ded6fde46ef998e0eceac577ff56be264ca7f616bffac5479e327cf453a6155241ad&scene=21#wechat_redirect)

笔记软件全测评计划：https://sourl.cn/Bn7fpH

欢迎你分享本文，让更多人看到，让我的创作可以发挥更大的价值，谢谢大家的关注和支持。

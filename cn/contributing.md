# 为Laravel做贡献 

- [简介](#introduction)
- [Pull Requests](#pull-requests)
- [编码指南](#coding-guidelines)

<a name="introduction"></a>
## 简介

Laravel是免费、开源的软件，这意味着任何人都可以为其开发和进步贡献力量。Laravel源代码目前托管在[Github](http://github.com)上，Github提供非常容易的途径fork项目和合并你的贡献。

<a name="pull-requests"></a>
## Pull Requests

pull request 的处理过程对于新特性和bug是不一样的。在你发起一个新特性的pull request之前，你应该先创建一个带有`[Proposal]`标题的issue。这个proposal应当描述这个新特性，以及实现方法。提议将会被审查，有可能会被采纳，也有可能会被拒绝。当一个提议被采纳，将会创建一个实现新特性的pull request。没有遵循上述指南的pull request将会被立即关闭。

为bug创建的Pull requests不需要创建建议issue。如果你有解决bug的办法，请详细描述你的解决方案。。

### 提交新特性

如果你希望Laravel中出现某个新特性，你可以在Github中创建一个带有`[Request]`标题的issue。该建议将会被核心代码贡献者审查。

<a name="coding-guidelines"></a>
## 编码指南

Laravel 遵循 [PSR-0](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md) 和 [PSR-1](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-1-basic-coding-standard.md) 编码标准. 除了上述这些标准，下面还列出了一些其他一些应当遵循的编码标准：

- 命名空间的声明应该和`<?php`在同一行。
- 类定义开始的 `{` 应当和类名在同一行。
- 函数和控制结构开始的 `{` 应该放在单独一行。
- 接口（interface）命名应该添加 `Interface` 做为后缀 (`FooInterface`)

译者：王赛  [（Bootstrap中文网）](http://www.bootcss.com)
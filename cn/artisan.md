# Artisan CLI

- [简介](#introduction)
- [用法](#usage)

<a name="introduction"></a>
## 简介

Artisan是Laravel中自带的命令行工具的名称。它提供了一些开发过程中有用的命令用。它是基于强大的Symfony Console 组件开发的。

<a name="usage"></a>
## 用法

执行 `list` 命令可以列出所有可用的Artisan命令：

**列出所有可用的命令**

	php artisan list

每个命令都包含有 "help" 信息，用以提供此命令所允许的参数和选项。只需在命令前边添加 `help` 即可：

**查看某个命令的帮助文档**

	php artisan help migrate

通过指定 `--env` 选项，你可以指定命令执行时的配置环境：

**指定配置环境**

	php artisan migrate --env=local

你可以使用 `--version` 选项查看当前安装的Laravel的版本：

**显示当前的Laravel版本**

	php artisan --version

译者：王赛  [（Bootstrap中文网）](http://www.bootcss.com)

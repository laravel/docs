# Artisan 命令列工具

- [簡介](#introduction)
- [用法](#usage)

<a name="introduction"></a>
## 簡介

Artisan 是 Laravel 內建的命令列工具，它提供了一些有用的指令協助您開發，它是由強大的 Symfony Console 元件所驅動。
<a name="usage"></a>
## 用法

#### 列出所有可用的指令

要查看所有可用的 Artisan 指令，您可以使用 `list` 這個指令:

	php artisan list

#### 查看指令的使用指南

每一個指令都包含一個 "使用指南" ，它顯示並描述這個指令能夠接受哪些參數和選項。要進入使用指南只需要在指令名稱前面加上 `help`即可:


	php artisan help migrate

#### 指定配置環境

您可以指定配置環境，只要在執行指令時加上 `--env` 即可切換所指定的配置環境:

	php artisan migrate --env=local

#### 檢視目前的 Laravel 版本

使用 `--version` 選項，您可以檢視目前所使用的 Laravel 版本:

	php artisan --version

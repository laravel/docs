# 在地化

- [介绍](#introduction)
- [语言档](#language-files)
- [基本用法](#basic-usage)
- [复数](#pluralization)
- [验证在地化](#validation)
- [覆写套件的语言档](#overriding-package-language-files)

<a name="introduction"></a>
## 介绍

Laravel 的 `Lang` facade 提供方便的方法来取得多种语言的字串，让你简单地在应用进程里支持多种语言。

<a name="language-files"></a>
## 语言档

语言字串保存在 `resources/lang` 文档夹的文档里。在这个文档夹里应该要给每一个应用进程支持的语言一个子文档夹。

	/resources
		/lang
			/en
				messages.php
			/es
				messages.php

#### 语言档范例

语言档简单地回传键跟字串的数组。例如：

	<?php

	return array(
		'welcome' => 'Welcome to our application'
	);

#### 在执行时变换默认语言

应用进程的默认语言被保存在 `config/app.php` 设置档。你可以在任何时候用 `App::setLocale` 方法变换现行语言：

	App::setLocale('es');

#### 设置备用语言

你也可以设置「备用语言」，它将会在当现行语言没有给定的语句时被使用。就像默认语言，备用语言也可以在 `config/app.php` 设置档设置：

	'fallback_locale' => 'en',

<a name="basic-usage"></a>
## 基本用法

#### 从语言档取得句子

	echo Lang::get('messages.welcome');

传递给 `get` 方法的字串的第一个部分是语言档的名称，第二个部分是应该被取得的句子的名称。

> **注意：** 如果语句不存在， `get` 方法将会回传键的名称。

你也可以使用 `trans` 辅助方法，它是 `Lang::get` 方法的别名。

	echo trans('messages.welcome');

#### 在句子中做替代

你也可以在语句中定义占位符：

	'welcome' => 'Welcome, :name',

接着，传递替代用的第二个参数给 `Lang::get` 方法：

	echo Lang::get('messages.welcome', array('name' => 'Dayle'));

#### 判断语言档是否有指定的句子

	if (Lang::has('messages.welcome'))
	{
		//
	}

<a name="pluralization"></a>
## 复数

复数是个复杂的问题，不同语言对于复数有很多种复杂的规则。你可以简单地在你的语言档里管理它。你可以用「管道」字符区分字串的单数和复数形态：

	'apples' => 'There is one apple|There are many apples',

接着你可以用 `Lang::choice` 方法取得语句：

	echo Lang::choice('messages.apples', 10);

你也可以提供一个地区参数来指定语言。举个例，如果你想要使用俄语 (ru)：

	echo Lang::choice('товар|товара|товаров', $count, array(), 'ru');

因为 Laravel 的翻译器由 Symfony 翻译组件提供，你也可以很容易地建立更明确的复数规则：

	'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',


<a name="validation"></a>
## 验证

要验证在地化的错误和消息，可以看一下<a href="/docs/5.0/validation#localization">验证的文档</a>.

<a name="overriding-package-language-files"></a>
## 覆写套件的语言档

许多套件附带它们自有的语句。你可以借由放置文档在 `resources/lang/packages/{locale}/{package}` 文档夹来覆写它们，而不是改变套件的核心文档来调整这些句子。所以，举个例子，如果你需要覆写 `skyrim/hearthfire` 套件在 `messages.php` 的英文语句，你可以放置语言档在： `resources/lang/packages/en/hearthfire/messages.php`。你可以只定义你想要覆写的语句在这个文档里，任何你没有覆写的语句将会仍从套件的语言档加载。

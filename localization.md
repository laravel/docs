# 在地化

- [介紹](#introduction)
- [語言檔](#language-files)
- [基本用法](#basic-usage)
- [複數](#pluralization)
- [驗證在地化](#validation)
- [覆寫套件的語言檔](#overriding-package-language-files)

<a name="introduction"></a>
## 介紹

Laravel 的 `Lang` facade 提供方便的方法來取得多種語言的字串，讓你簡單地在應用程式裡支援多種語言。

<a name="language-files"></a>
## 語言檔

語言字串儲存在 `resources/lang` 資料夾的檔案裡。在這個資料夾裡應該要給每一個應用程式支援的語言一個子資料夾。

	/resources
		/lang
			/en
				messages.php
			/es
				messages.php

#### 語言檔範例

語言檔簡單地回傳鍵跟字串的陣列。例如：

	<?php

	return array(
		'welcome' => 'Welcome to our application'
	);

#### 在執行時變換預設語言

應用程式的預設語言被儲存在 `config/app.php` 設定檔。你可以在任何時候用 `App::setLocale` 方法變換現行語言：

	App::setLocale('es');

#### 設定備用語言

你也可以設定「備用語言」，它將會在當現行語言沒有給定的語句時被使用。就像預設語言，備用語言也可以在 `config/app.php` 設定檔設定：

	'fallback_locale' => 'en',

<a name="basic-usage"></a>
## 基本用法

#### 從語言檔取得句子

	echo Lang::get('messages.welcome');

傳遞給 `get` 方法的字串的第一個部分是語言檔的名稱，第二個部分是應該被取得的句子的名稱。

> **注意：** 如果語句不存在， `get` 方法將會回傳鍵的名稱。

你也可以使用 `trans` 輔助方法，它是 `Lang::get` 方法的別名。

	echo trans('messages.welcome');

#### 在句子中做替代

你也可以在語句中定義佔位符：

	'welcome' => 'Welcome, :name',

接著，傳遞替代用的第二個參數給 `Lang::get` 方法：

	echo Lang::get('messages.welcome', array('name' => 'Dayle'));

#### 判斷語言檔是否有指定的句子

	if (Lang::has('messages.welcome'))
	{
		//
	}

<a name="pluralization"></a>
## 複數

複數是個複雜的問題，不同語言對於複數有很多種複雜的規則。你可以簡單地在你的語言檔裡管理它。你可以用「管道」字元區分字串的單數和複數形態：

	'apples' => 'There is one apple|There are many apples',

接著你可以用 `Lang::choice` 方法取得語句：

	echo Lang::choice('messages.apples', 10);

你也可以提供一個地區參數來指定語言。舉個例，如果你想要使用俄語 (ru)：

	echo Lang::choice('товар|товара|товаров', $count, array(), 'ru');

因為 Laravel 的翻譯器由 Symfony 翻譯元件提供，你也可以很容易地建立更明確的複數規則：

	'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',


<a name="validation"></a>
## 驗證

要驗證在地化的錯誤和訊息，可以看一下<a href="/docs/5.0/validation#localization">驗證的文件</a>.

<a name="overriding-package-language-files"></a>
## 覆寫套件的語言檔

許多套件附帶它們自有的語句。你可以借由放置檔案在 `resources/lang/packages/{locale}/{package}` 資料夾來覆寫它們，而不是改變套件的核心檔案來調整這些句子。所以，舉個例子，如果你需要覆寫 `skyrim/hearthfire` 套件在 `messages.php` 的英文語句，你可以放置語言檔在： `resources/lang/packages/en/hearthfire/messages.php`。你可以只定義你想要覆寫的語句在這個檔案裡，任何你沒有覆寫的語句將會仍從套件的語言檔載入。

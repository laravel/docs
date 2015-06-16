# 在地化

- [簡介](#introduction)
- [基本用法](#basic-usage)
	- [Pluralization](#pluralization)
- [Overriding Vendor Language Files](#overriding-package-language-files)

<a name="introduction"></a>
## 簡介

Laravel 的在地化功能提供方便的方法來取得多語系的字串，讓你的網站可以簡單的支援多語系。

語系檔存放在 `resources/lang` 資料夾的檔案裡。在此資料夾內，應該要有網站支援的語系並對應到每一個子目錄。：

	/resources
		/lang
			/en
				messages.php
			/es
				messages.php

語系檔簡單地回傳鍵值和字串陣列，例如：

	<?php

	return [
		'welcome' => 'Welcome to our application'
	];

#### 切換語系
網站的預設語系儲存在 `config/app.php` 設定檔。您可以在任何時後使用 `App` facade 的 `setLocale` 方法動態地變換現行語系：

	Route::get('welcome/{locale}', function ($locale) {
		App::setLocale($locale);

		//
	});

您也可以設定 "備用語系"，它將會在當現行語言沒有給定的語句時被使用。就像預設語言，備用語言也可以在 `config/app.php` 設定檔設定：

	'fallback_locale' => 'en',

<a name="basic-usage"></a>
## 基本用法

您可以使用 `trans` 輔助函式來取得語系字串， The `trans` method accepts the file and key of the language line as its first argument. For example, let's retrieve the language line `welcome` in the `resources/lang/messages.php` language file:

	echo trans('messages.welcome');

當然，若您使用 [Blade 樣版引擎](/docs/{{version}}/blade), 您可以使用 `{{ }}` 來輸出語言列：

	{{ trans('messages.welcome') }}

If the specified language line does not exist, the `trans` function will simply return the language line key. So, using the example above, the `trans` function would return `messages.welcome` if the language line does not exist.

#### Replacing Parameters In Language Lines

If you wish, you may define place-holders in your language lines. All place-holders are prefixed with a `:`. For example, you may define a welcome message with a place-holder name:

	'welcome' => 'Welcome, :name',

To replace the place-holders when retrieving a language line, pass an array of replacements as the second argument to the `trans` function:

	echo trans('messages.welcome', ['name' => 'Dayle']);

<a name="pluralization"></a>
### Pluralization

Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization. By using a "pipe" character, you may distinguish a singular and plural form of a string:

	'apples' => 'There is one apple|There are many apples',

Then, you may then use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the language line is returned:

	echo trans_choice('messages.apples', 10);

Since the Laravel translator is powered by the Symfony Translation component, you may create even more complex pluralization rules:

	'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',

<a name="overriding-package-language-files"></a>
## Overriding Package Language Files

Some packages may ship with their own language files. Instead of hacking the package's core files to tweak these lines, you may override them by placing your own files in the `resources/lang/vendor/{package}/{locale}` directory.

So, for example, if you need to override the English language lines in `messages.php` for a package named `skyrim/hearthfire`, you would place a language file at: `resources/lang/vendor/hearthfire/en/messages.php`. In this file you should only define the language lines you wish to override. Any language lines you don't override will still be loaded from the package's original language files.

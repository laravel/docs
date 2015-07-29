# 在地化

- [簡介](#introduction)
- [基本用法](#basic-usage)
    - [複數](#pluralization)
- [覆寫套件的語言檔](#overriding-vendor-language-files)

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

您可以使用 `trans` 輔助函式來取得語系字串，`trans` 函式的第一個參數接受檔名和鍵值名稱，例如，從 `resources/lang/messages.php` 語言檔取得名稱為 `welcome` 的句子：

    echo trans('messages.welcome');

當然，若您使用 [Blade 樣版引擎](/docs/{{version}}/blade), 您可以使用 `{{ }}` 來輸出句子：

    {{ trans('messages.welcome') }}

如果句子不存在， `trans` 方法將會回傳鍵值的名稱，如上範例會回傳 `messages.welcome` 。

#### 在句子中做替代

如果需要，你也可以在語系檔中定義佔位符，佔位符使用 `:` 開頭，例如，您可以定義一則歡迎訊息的佔位符：

    'welcome' => 'Welcome, :name',

接著，傳入替代用的第二個參數給 `trans` 方法：

    echo trans('messages.welcome', ['name' => 'Dayle']);

<a name="pluralization"></a>
### 複數

複數是個複雜的問題，不同語言對於複數有不同的規則，使用 "管線" 字元，可以區分單複數字串格式：

    'apples' => 'There is one apple|There are many apples',

接著，可以使用 `trans_choice` 方法來設定總數，例如，當總數大於一將會取得複數句子：

    echo trans_choice('messages.apples', 10);

由於 Laravel 的翻譯器是來自於 Symfony 翻譯套件，您甚至可以使用更複雜的複數規則：

    'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',

<a name="overriding-vendor-language-files"></a>
## 覆寫套件的語言檔

部分套件帶有自己的語系檔，您可以藉由放置檔案在 `resources/lang/vendor/{package}/{locale}` 來複寫它們，而不是直接修改套件的核心檔案。

例如，您需要複寫 `skyrim/hearthfire` 套件的英文語系檔 `messages.php`，您需要把檔案放置在 `resources/lang/vendor/hearthfire/en/messages.php`。這個檔案內，只要去定義需要覆寫的語句，任何沒有覆寫的語句將會仍從套件的語言檔載入。

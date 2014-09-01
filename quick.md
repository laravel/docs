# Laravel 快速入門

- [安裝](#installation)
- [本地開發環境](#local-development-environment)
- [路由](#routing)
- [建立視圖](#creating-a-view)
- [建立遷移資料](#creating-a-migration)
- [Eloquent ORM](#eloquent-orm)
- [顯示資料](#displaying-data)
- [部署應用](#deploying-your-application)

<a name="installation"></a>
## 安裝

### 透過 Laravel 安裝器

首先，下載 [Laravel 安裝器 PHAR 包](http://laravel.com/laravel.phar)。為使用上方便，將檔案搬移至 `/usr/local/bin` 並改名為 `laravel`。安裝完成後，只要執行 `laravel new` 命令即可以創立一個全新的 laravel 專案在你指定的目錄下。例如：`laravel new blog` 將會建立一個名為 `blog` 的目錄，所需之相依套件的全新 laravel 專案安裝其內。這個安裝方式將會比透過 Composer 快許多。

### 透過 Composer

Laravel 框架使用 [composer](http://getcomposer.org) 來執行安裝及相依性管理。如果還沒有安裝它的話，請先從[安裝 Composer](http://getcomposer.org/doc/00-intro.md)開始吧。

安裝之後，你可以透過命令列模式執行下列指令來安裝 Laravel：

	composer create-project laravel/laravel your-project-name --prefer-dist

這個指令會下載並安裝一份乾淨的 Laravel 在你目前所在目錄的 `your-project-name` 的新建目錄中。


如果你想要直接從 [Github 上的 Laravel Respoitory](https://github.com/laravel/laravel/archive/master.zip) 手動下載 Laravel 也是可以的。只要在解壓後的目錄最頂層，執行 `composer install` 即可，這個指令會把框架相依的資源下載安裝好。

### 權限設定

在安裝 Laravel 之後，你需要讓網頁伺服器有寫入 `app/storage` 目錄的權限。詳情請見 [安裝過程](/docs/installation) 文件說明。

### 運行 Laravel

一般而言，你需要網頁伺服器（如: Apache 或是 Nginx）來運行你的 Laravel 應用。如果你是使用 PHP 5.4 以上版本，那可以使用 PHP 內建的開發伺服器，你只需要使用 Artisan 命令 `serve`：

	php artisan serve

<a name="directories"></a>
### 目錄結構

安裝完框架後，可以來了解熟悉一下專案的目錄結構。`app` 目錄裡面包含了 `views（視圖）`, `controllers（控制器）`, 還有 `models（模型）` 等目錄。你的應用程式大多數的程式碼都會在這個目錄中。你也會發現 `app/config` 這個目錄，設定檔多存在在這目錄之中。

<a name="local-development-environment"></a>
## 本地開發環境

過去你要在本機上設定本地的 PHP 開發環境是讓人頭痛的事情。要安裝正確的 PHP 版本、必須的套件，還有所需的元件是廢時耗力的。為了解決這狀況，使用 [Laravel Homestead](/docs/homestead) 吧。Homestead 是以 Laravel 和 [Vagrant](http://vagrantup.com) 所設計的虛擬機器。而 Homestead Vagrant 封裝預載建立完整 PHP 應用所需的所有軟體。如此一來你可以在瞬間創建一個虛擬化、獨立不受干擾的開發環境。下面列出包裝在 Homestead 裏的軟體：

- Nginx
- PHP 5.5
- MySQL
- Redis
- Memcached
- Beanstalk

不用擔心，即使 "虛擬化" 聽起來複雜，但這是無痛的。VirtualBox 和 Vagrant 是 Homestead 的相依軟體，你需要先安裝他們。兩個軟體都有各平台的簡單圖形化安裝介面。請參閱 [Homestead 文件](/docs/homestead) 進行了解。

<a name="routing"></a>
## 路由

一開始，我們先創建第一個路由。在 Laravel 中，最簡單的路由是封閉性路由。打開 `app/routes.php` 檔案，並且增加下面的路由在檔案的最下方：

	Route::get('users', function()
	{
		return 'Users!';
	});

現在，你在你瀏覽器中輸入 `/users`，你應該會看到頁面出現 `Users!`。很好！你已經建立了你的第一個路由。

路由也可以指向一個控制器類別。例如：

	Route::get('users', 'UserController@getIndex');

這個路由告訴框架 `/users` 路由的請求應該使用 `UserController` 類別的 `getIndex` 方法。查看更多控制器路由的資訊，請查閱 [控制器文件](/docs/controllers)。

<a name="creating-a-view"></a>
## 建立視圖

接下來，我們要創建試圖來顯示我們的用戶資料。視圖以 HTML 代碼存放在 `app/views` 的目錄中。我們來存放兩個視圖進目錄中： `layout.blade.php` 和 `user.blade.php`。首先，我們先來建立 `layout.blade.php` 檔案：

	<html>
		<body>
			<h1>Laravel Quickstart</h1>

			@yield('content')
		</body>
	</html>

接下來，我們建立 `users.blade.php` 視圖：

	@extends('layout')

	@section('content')
		Users!
	@stop

這裡有些語法或許讓你感到陌生。因為我們使用的是 Laravel 的模板系統：Blade。Blade 非常快，僅需要少量的正規表示式來幫你的模板編譯成 PHP 代碼。Blade 提供了強大的功能，例如模板的繼承，還有一些常用的 PHP 控制結構語法，如 `if` 和 `for`。更多資訊請查閱 [Blade 文件](/docs/templates)。

現在，我們已經有了自己的視圖，讓我們回到 `/users` 路由。我們改用視圖來替代顯示出 `Users!`：

	Route::get('users', function()
	{
		return View::make('users');
	});

太棒了！現在你已經成功地建立了一個繼承自 layout 的簡單視圖。接下來，我們開始到資料庫層。

<a name="creating-a-migration"></a>
## 建立遷移檔

我們使用 Laravel 的遷移(migration)系統來建立資料表以保存我們的資料。遷移記錄著資料庫的改變歷程，這讓團隊成員間的資訊分享更為簡單。

首先，我們要設定資料庫連接。你可以在 `app/config/database.php` 檔案配置所有的資料庫連接資訊。預設中，Laravel 使用 MySQL，所以你必須將資料庫連接的機密資訊填入其中。你也可以更改 `driver` 選項為 `sqlite`，如此他就會使用放置在 `app/database` 裡的 SQLite 資料庫。

接下來，我們來創建遷移檔，我們使用 [Artisan CLI](/docs/artisan)。在專案的根目錄下，在終端裡執行下列指令：

	php artisan migrate:make create_users_table

然後，在 `app/database/migrations` 目錄下找到產生的遷移檔。檔案中有一個包含了兩個方法 `up` 和 `down` 的類別。在 `up` 方法中，你必須表明你要對你的資料表做哪些更動，而在 `down` 的方法裡，你只要回復這些更動。 

我們定義一個遷移檔如下：

	public function up()
	{
		Schema::create('users', function($table)
		{
			$table->increments('id');
			$table->string('email')->unique();
			$table->string('name');
			$table->timestamps();
		});
	}

	public function down()
	{
		Schema::drop('users');
	}

然後我們從終端裡透過 `migrate` 指令來執行遷移動作。在專案的根目錄裡執行下列指令：

	php artisan migrate

如果你想回復遷移，你可以執行 `migrate:rollback` 指令。現在我們已經建好了資料表了，開始放些資料進去吧。

<a name="eloquent-orm"></a>
## Eloquent ORM

Laravel 提供了很棒的 ORM：Eloquent。如果你曾經使用過 Ruby on Rails 框架，那你將會覺得 Eloquent 很熟悉，因為它遵循 ActiveRecord ORM 風格的資料庫互動模式。

首先，我們先來定義一個模型(model)。一個 Eloquent 模型可以用來查詢關聯的資料表，以及表內的某一行。別擔心，我們很快就會了解了。模型通常存放在 `app/models` 目錄中。讓我們先來在這目錄裡定義一個 `User.php` 的模型檔如下：

	class User extends Eloquent {}

注意，我們並未告訴 Eloquent 使用哪個表。Eloquent 有多種慣例，一種就是使用模型的複數形態作為該模型的資料表名稱，非常方便。

使用你喜歡的資料庫管理工具，插入幾筆資料到 `users` 資料表，我們將使用 Eloquent 來取得這些資料並且傳遞到視圖當中。

現在我們修改我們的 `/users` 路由，如下：

	Route::get('users', function()
	{
		$users = User::all();

		return View::make('users')->with('users', $users);
	});

我們來看看這個路由。首先，`User` 模型裡的 `all` 方法會將 `users` 表裡取得所有的記錄。接下來，我們透過 `with` 方法將這些記錄傳遞到視圖裡。`with` 方法接受一個鍵和一個值，如此該鍵值就可以在視圖中被使用了。

<a name="displaying-data"></a>
## 顯示資料

現在，我們視圖中已經可以存取到 `users` 類別了，我們可以顯示出來，如下：

	@extends('layout')

	@section('content')
		@foreach($users as $user)
			<p>{{ $user->name }}</p>
		@endforeach
	@stop

你會發現沒有看到任何 `echo` 語句。當使用 Blade 時，你可以使用兩個大括號來輸出資料。很容易的，你應該可以透過 `/users` 路由來看到你的用戶資料。

這僅僅只是開始。在本系列教學中，你已經了解了 Laravel 基礎部分，但是還有更多令人興奮的東西等著你學習。繼續閱讀文件且更深入的了解 [Eloquent](/docs/eloquent) 和 [Blade](/docs/templates) 的強大特性。或許，你也更有興趣去了解 [隊列](/docs/queues) 和 [單元測試](/docs/testing)。也或許，你更想要了解 [IoC Container] 來展現實力，選擇在你。

<a name="deploying-your-application"></a>
## 部署應用程式

Laravel 的其中一個目標就是讓 PHP 應用程式開發從下載到部署都輕鬆化，而 [Laravel Forge](https://forge.laravel.com) 提供了一個簡單的方式去部署你的 Laravel 應用到快速的服務器上。Forge 可以設定並供應在 DigitalOcean、 Linode、Rackspace 和 Amazon EC2 上的機器群。如同 Homestead 一樣，所有必須的最新版軟體都已安裝在內：Nginx、PHP 5.5、MySQL、Postgres、Redis、Memcached 等等。Forge 的 “快速部署” 可以讓你在每次發布更新至 Github 或是 Bitbucket 時自動部署應用。

更重要的是，Forge 能幫助你設定 queue workers、SSL、Cron jobs、子網域等等。更多的資訊請參閱 [Forge 網站](https://forge.laravel.com)。

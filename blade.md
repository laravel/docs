# Blade 模板

- [簡介](#introduction)
- [模板繼承（ template inheritance ）](#template-inheritance)
	- [定義視圖輸出](#defining-a-layout)
	- [繼承視圖輸出](#extending-a-layout)
- [顯示資料](#displaying-data)
- [控制語法](#control-structures)
- [服務注入](#service-injection)
- [模板擴充](#extending-blade)

<a name="introduction"></a>
## 簡介

Blade is the simple, yet powerful templating engine provided with Laravel. Unlike other popular PHP templating engines, Blade does not restrict you from using plain PHP code in your views. All Blade views are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade view files use the `.blade.php` file extension and are typically stored in the `resources/views` directory.

Blade 是 Laravel 所提供的一個簡單且強大的模板引擎。相較於其它知名的 PHP 模板引擎， Blade 並不會限制你必須在視圖中使用 PHP 程式碼。在 Blade 被修改之前，所有的視圖都會被編譯為普通的 PHP 程式碼並置入快取，這代表著 Blade 視圖基本上對於整個應用程式而言並不會增加太多負擔。Blade 視圖檔案使用 `.blade.php` 做為副檔名，並存在 `resources/views` 資料夾。

<a name="template-inheritance"></a>
## 模板繼承（ template inheritance ）

<a name="defining-a-layout"></a>
### 定義視圖輸出

Two of the primary benefits of using Blade are _template inheritance_ and _sections_. To get started, let's take a look at a simple example. First, we will examine a "master" page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view:

Blade 視圖的兩個主要優點是 _模板繼承（ template inheritance）_ 與 _區塊（ sections ）_。先從下面的 Blade 視圖範例開始。首先，我們確認一下 "master" 頁面輸出：由於大多數的網頁應用程式在不同頁面都保持著相同的佈局方式，用以下方式即可定義單一 Blade 視圖輸出。

	<!-- 檔案儲存於 resources/views/layouts/master.blade.php -->

	<html>
		<head>
			<title>App Name - @yield('title')</title>
		</head>
		<body>
			@section('sidebar')
				This is the master sidebar.
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

As you can see, this file contains typical HTML mark-up. However, take note of the `@section` and `@yield` directives. The `@section` directive, as the name implies, defines a section of content, while the `@yield` directive is used to display the contents of a given section.

Now that we have defined a layout for our application, let's define a child page that inherits the layout.

正如你所見，這個檔案包含了傳統的 HTML 語法。然而，我們可以見到 `@section` 與 `@yield` 兩個有異於 HTML 語法的指令。正如其名， `@section` 指令定義一個內容區塊，而 `@yield` 指令則輸出一個已經被定義的區塊。

現在，我們已經定義了 Web 應用程式的基本輸出，以下就使用模板繼承的方式建立一個子頁面。

<a name="extending-a-layout"></a>
### Extending A Layout

When defining a child page, you may use the Blade `@extends` directive to specify which layout the child page should "inherit". Views which `@extends` a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`:

當我們建立了一個子頁面後，你可以使用 `@extends` 指令進行模板繼承，在模板繼承之下， `@section` 的內容會覆蓋原本頁面的 `@yield` 內容：

	<!-- 儲存於 resources/views/layouts/child.blade.php -->

	@extends('layouts.master')

	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@endsection

	@section('content')
		<p>This is my body content.</p>
	@endsection

In this example, the `sidebar` section is utilizing the `@@parent` directive to append (rather than overwriting) content to the layout's sidebar. The `@@parent` directive will be replaced by the content of the layout when the view is rendered.

Of course, just like plain PHP views, Blade views may be returned from routes using the global `view` helper function:

在這個範例下， `sidebar` 區塊利用了 `@@parent` 指令顯示原本頁面（ master.blade.php ）的內容，而不會去覆寫原本頁面的內容。 `@@parent` 指令將會在內容呈現時被置換於視圖中。

當然，就像一般的 PHP 視圖， Blade 視圖可以在 routes 中使用 `view` 函式顯示：

	Route::get('blade', function () {
		return view('child');
	});

> **譯註：** `view` 函式是 Laravel 所提供的全域函式，可應用於控制器與路由。


<a name="displaying-data"></a>
## 顯示資料

You may display data passed to your Blade views by wrapping the variable in "curly" braces. For example, given the following route:

你可能會需要傳送某些資料給視圖，此時可以使用 `view` 函式的第二參數。
舉例而言，如同以下的路由：

	Route::get('greeting', function () {
		return view('welcome', ['name' => 'Samantha']);
	});

You may display the contents of the `name` variable like so:

你可以用以下方式顯示陣列中的鍵（ key ）為 `name` 的值（ value ）：

	Hello, {{ $name }}.

Of course, you are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement:

當然，也不是一定只能顯示從 routes 傳送過來的資料。你可以用以下方式代入 PHP 原有的函式，或是任何你希望被 `echo` 出來的 PHP 指令或字串：

	The current UNIX timestamp is {{ time() }}.

> **Note:** Blade `{{ }}` statements are automatically send through PHP's `htmlentities` function to prevent XSS attacks.

> **注意：** 在 Blade 視圖中， `{{}}` 已經自動以 PHP 既有的 `htmlentites` 函式防禦 XSS 攻擊手法。


#### Blade 與 JavaScript 框架配合使用

Since many JavaScript frameworks also use "curly" braces to indicate a given expression  should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example:

自從有許多 JavaScript 框架也使用 `{{}}` 來顯示資料或敘述，你可以使用 `@` 符號避免 Blade 解析引擎針對 `{{}}`的轉義：

	<h1>Laravel</h1>

	Hello, @{{ name }}.

In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to instead by rendered by your JavaScript framework.

在這個範例中， `@` 符號會被忽略，並會在瀏覽器上直接輸出 `{{ name }}`，如此以來，便可讓其它 JavaScript 框架所應用。

#### 確認資料是否存在

Sometimes you may wish to echo a variable, but you aren't sure if the variable has been set. We can express this in verbose PHP code like so:

有時候你想要印出一個變數，但你並不確定這個變數是否存在。我們可以用以下的 PHP 程式確定變數是否存在並印出：

	{{ isset($name) ? $name : 'Default' }}

However, instead of writing a ternary statement, Blade provides you with the following convenient short-cut:

然而，若不想使用三元運算子， Blade 模板也提供了較簡潔的方法：

	{{ $name or 'Default' }}

In this example, if the `$name` variable exists, its value will be displayed. However, if it does not exist, the word `Default` will be displayed.

在這個範例中，如果 `$name` 這個變數存在，它將會被顯示；然而，如果這個變數不存在，便會顯示 `Default`。

#### 顯示 HTML 原始資料

By default, Blade `{{ }}` statements are automatically send through PHP's `htmlentities` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax:

在預設情況下， Blade 模板中的 `{{}}` 敘述將會自動套用 PHP 的 `htmlentities` 函式，以避免 XSS 攻擊。如你想要印出任何未被 `htmlentities` 處理過的資料，可以使用下列的方式：

	Hello, {!! $name !!}.

> **Note:** Be very careful when echoing content that is supplied by users of your application. Always use the double curly brace syntax to escape any HTML entities in the content.

> **注意：** 請非常小心處理要任何有可能出現在程式中的字串，在未經過 HTML 過濾之前，可能會造成嚴重的安全性問題。

> **譯註：** 在程式中你可能會應用到 `nl2br()` 進行 textarea 的字串分行處理，你可以使用 `{!! nl2br(e($contents)) !!}` 解決這個問題


<a name="control-structures"></a>
## 控制語法

In addition to template inheritance and displaying data, Blade also provides convenient short-cuts for common PHP control structures, such as conditional statements and loops. These short-cuts provide a very clean, terse way of working with PHP control structures, while also remaining familiar to their PHP counterparts.

除了模板繼承與顯示資料功能以外， Blade 也提供了方便、簡潔的 PHP 控制敘述，像是條件分歧（ if/else ）或是迴圈。在撰寫控制敘述時，這些指令將有助於寫出簡潔且可讀性高的 Blade 頁面：

#### If 敘述

You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts:

你可以利用 `@if`、`@elseif`、`@else`及`@endif` 指令進行條件分歧判斷與執行： 

	@if (count($records) === 1)
		有一條記錄		
	@elseif (count($records) > 1)
		有多條記錄
	@else
		沒有記錄
	@endif

For convenience, Blade also provides an `@unless` directive:

為了方便， Blade 也提供了 `@unless` 指令，以達成 if not 作用：

	@unless (Auth::check())
		你尚未登入
	@endunless
	
> **譯註：** Blade 尚未提供 `switch` 敘述的使用，若有 `switch` 使用需要者，需要自行撰寫。

#### 迴圈

In addition to conditional statements, Blade provides simple directives for working with PHP's supported loop structures. Again, each of these directives functions identically to their PHP counterparts:

除了條件分歧控制以外， Blade 也提供了簡易迴圈使用方式。 

	@for ($i = 0; $i < 10; $i++)
		The current value is {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>This is user {{ $user->id }}</p>
	@endforeach

	@forelse ($users as $user)
		<li>{{ $user->name }}</li>
	@empty
		<p>No users</p>
	@endforelse

	@while (true)
		<p>I'm looping forever.</p>
	@endwhile

#### 引入（ include ）子視圖

Blade's `@include` directive, allows you to easily include a Blade view from within an existing view. All variables that are available to the parent view will be made available to the included view:

Blade 模板中的 `@include` 指令，允使開發者簡單地引入一個已存在的其它 Blade 模板。所有的變數都被允許引入於視圖。

	<!-- 儲存於 resource/views/layouts/form.blade.php -->
	<div>
		@include('shared.errors')

		<form>
			<!-- Form Contents -->
		</form>
	</div>

	<!-- 儲存於 resource/views/shared/errors.blade.php -->
	@if( isset($error) )
		<div class="errors alert">
			哎呀，好像哪裡出錯了 OAO!<br>
			{{ $error }}
		</div>
	@endif

Even though the included view will inherit all data available in the parent view, you may also pass an array of extra data to the included view:

在引入頁面時，可以傳送特定資料給被引入的頁面：

	@include('view.name', ['error' => '你忘記輸入帳號囉'])
	
> **譯註：** 這邊為了更容易看懂引入的邏輯與使用方式，所以我新增了 errors.blade.php 範例。

#### 註解

Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application:

Blade 同時也允許定義註解在頁面中。然而，有異於 HTML 的註解， Blade 的註解並不會被放在 HTML 中：

	{{-- This comment will not be present in the rendered HTML --}}

<a name="service-injection"></a>
## Service Injection

The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/{{version}}/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class / interface name of the service you wish to resolve:

`@inject` 指令可以取出 Laravel 的 [服務容器](/docs/{{version}}/container)。在 `@inject` 的第一個參數表示在這個頁面中，這個服務容器所代表的變數名；第二個參數表示這個服務容器中的解析位置：

	@inject('metrics', 'App\Services\MetricsService')

	<div>
		Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
	</div>

<a name="extending-blade"></a>
## 繼承擴充

Blade even allows you to define your own custom directives. You can use the `directive` method to register a directive. When the Blade compiler encounters the directive, it calls the provided callback with its parameter.

The following example creates a `@datetime($var)` directive which formats a given `$var`:

Blade 模板允許客製化指令。你可以使用 `directive` 方法註冊指令。當 Blade 的指令被編譯時，將會呼叫它的提供者回傳它的參數。

以下範例將會建立一個以 `$var` 為格式的 `@datetime($var)` 指令：

	<?php

	namespace App\Providers;

	use Blade;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Blade::directive('datetime', function($expression) {
				return "<?php echo with{$expression}->format('m/d/Y H:i'); ?>";
			});
		}

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

As you can see, Laravel's `with` helper function was used in this directive. The `with` helper simply returns the object / value it is given, allowing for convenient method chaining. The final PHP generated by this directive will be:

誠如你所見， Laravel 的 `with` 函式被用在這個指令中。 `with` 函式會簡單地回傳其中的 物件 / 值，並允許以方法串接。最後將會產生如以下的 PHP 指令：

	<?php echo with($var)->format('m/d/Y H:i'); ?>



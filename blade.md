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

Blade 模板是 Laravel 所提供的簡單且強大的模板引擎。相較於其它知名的 PHP 模板引擎， Blade 並不會限制你必須在視圖中使用 PHP 程式碼。在 Blade 被修改之前，所有的視圖都會被轉換（ compiled ）為普通的 PHP 程式碼並產生快取，這代表著 Blade 視圖基本上對於整個系統而言並不會增加太多負擔。Blade 視圖檔案使用 `.blade.php` 做為副檔名，並儲存於 `resources/views` 資料夾。

<a name="template-inheritance"></a>
## 模板繼承（ template inheritance ）

<a name="defining-a-layout"></a>
### 定義視圖輸出

Blade 模板具有兩個主要優點： _模板繼承（ template inheritance）_ 與 _區塊（ sections ）_。從下面的 Blade 模板範例開始：首先，我們確認一下 "master" 這個頁面的輸出，由於大多數的網頁應用程式在不同頁面都保持著相同的佈局方式，用以下方式即可定義單一 Blade 模板輸出。

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


正如你所見，這個檔案包含了傳統的 HTML 語法。然而，我們可以見到 `@section` 與 `@yield` 兩個有異於 HTML 語法的指令。正如其名， `@section` 指令定義一個內容區塊，而 `@yield` 指令則輸出一個已經被定義的區塊。

現在，我們已經定義了這個應用程式的基本輸出，以下就使用模板繼承的方式建立一個子頁面。

<a name="extending-a-layout"></a>
### 繼承視圖輸出

當建立了一個子頁面後，便可以使用 `@extends` 指令進行模板繼承。在模板繼承之後， `@section` 的內容會覆蓋原本頁面的 `@yield` 內容：

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


在這個範例中， `sidebar` 區塊利用了 `@@parent` 指令顯示原本頁面（ master.blade.php ）的內容，而不會去覆寫原本頁面的內容。 `@@parent` 指令會將父頁面的內容呈現於視圖中。

當然，就像一般的 PHP 視圖， Blade 視圖可以在 routes 中使用 `view` 函式顯示：

	Route::get('blade', function () {
		return view('child');
	});

> **譯註：** `view` 函式是 Laravel 所提供的全域函式，常應用於控制器與路由。


<a name="displaying-data"></a>
## 顯示資料

你可能會需要傳送某些資料給視圖，此時可以使用 `view` 函式的第二參數。
舉例而言，就像以下的路由設定：

	Route::get('greeting', function () {
		return view('welcome', ['name' => 'Samantha']);
	});

你可以用以下方式顯示陣列中的索引（ key ）為 `name` 的值（ value ）：

	Hello, {{ $name }}.

當然，也不是一定只能顯示從 routes 傳送過來的資料。你可以用以下方式代入 PHP 原有的函式，或是任何你希望被印出的 PHP 指令或字串：

	The current UNIX timestamp is {{ time() }}.

> **注意：** 在 Blade 視圖中， `{{ }}` 已經自動以 PHP 既有的 `htmlentites` 函式防禦 XSS 攻擊手法。


#### Blade 與 JavaScript 框架配合使用

自從有許多 JavaScript 框架也使用 `{{ }}` 來顯示資料或敘述，你可以使用 `@` 符號避免 Blade 解析引擎針對 `{{ }}`的轉義：

	<h1>Laravel</h1>

	Hello, @{{ name }}.

在這個範例中， `@` 符號會被忽略，並會在瀏覽器上直接輸出 `{{ name }}`，如此以來，便可讓其它 JavaScript 框架所應用。

#### 確認資料是否存在

有時候你想要印出一個變數，但你並不確定這個變數是否存在。我們可以用以下的 PHP 程式確定變數是否存在並印出：

	{{ isset($name) ? $name : 'Default' }}
然而，若不習慣使用三元運算子， Blade 模板也提供了較簡潔的方法：

	{{ $name or 'Default' }}

在這個範例中，如果 `$name` 這個變數存在，它將會被印出；然而，如果這個變數不存在，便會印出 `Default`。

#### 顯示 HTML 原始資料

在預設情況下， Blade 模板中的 `{{ }}` 敘述將會自動套用 PHP 的 `htmlentities` 函式，以避免 XSS 攻擊。如你想要印出任何未被 `htmlentities` 處理過的資料，可以使用下列的方式：

	Hello, {!! $name !!}.

> **注意：** 請非常小心處理要任何有可能出現在程式中的字串，在未經過 HTML 過濾之前，可能會造成嚴重的安全性問題。

> **譯註：** 在程式中你可能會應用到 `nl2br()` 進行 textarea 的字串分行處理，你可以使用 `{!! nl2br(e($contents)) !!}` 解決這個問題


<a name="control-structures"></a>
## 控制語法

除了模板繼承與顯示資料功能以外， Blade 也提供了方便、簡潔的 PHP 控制敘述，像是條件分歧（ if/else ）或是迴圈。在撰寫控制敘述時，這些指令將有助於寫出簡潔且可讀性高的 Blade 頁面：

#### If 敘述

你可以利用 `@if`、`@elseif`、`@else`及`@endif` 指令進行條件分歧判斷與執行：

	@if (count($records) === 1)
		有一條記錄
	@elseif (count($records) > 1)
		有多條記錄
	@else
		沒有記錄
	@endif

為了方便， Blade 也提供了 `@unless` 指令，以達成 if not 作用：

	@unless (Auth::check())
		你尚未登入
	@endunless

> **譯註：** Blade 尚未提供 `switch` 敘述的使用，若有 `switch` 使用需要者，需要自行撰寫。

#### 迴圈

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

在引入頁面時，可以傳送特定資料給被引入的頁面：

	@include('view.name', ['error' => '你忘記輸入帳號囉'])

> **譯註：** 這邊為了更容易看懂引入的邏輯與使用方式，所以新增了 errors.blade.php 範例。

#### 註解

Blade 同時也允許在頁面中定義註解。然而，有異於 HTML 的註解， Blade 的註解並不會被顯示於在 HTML 內：

	{{-- This comment will not be present in the rendered HTML --}}

<a name="service-injection"></a>
## 服務注入

`@inject` 指令可以取出 Laravel 的 [服務容器](/docs/{{version}}/container)。在 `@inject` 的第一個參數表示在這個頁面中，這個服務容器在頁面所代表的變數名；第二個參數表示這個服務容器中的解析位置：

	@inject('metrics', 'App\Services\MetricsService')

	<div>
		Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
	</div>

<a name="extending-blade"></a>
## 模板擴充

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

誠如你所見， Laravel 的 `with` 函式被用在這個指令中。 `with` 函式會簡單地回傳其中的 物件 / 值，並允許以方法串接。最後將會產生如以下的 PHP 指令：

	<?php echo with($var)->format('m/d/Y H:i'); ?>



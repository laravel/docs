# Blade 模板

- [簡介](#introduction)
- [模板繼承](#template-inheritance)
	- [定義頁面佈局](#defining-a-layout)
	- [繼承頁面佈局](#extending-a-layout)
- [顯示資料](#displaying-data)
- [控制語法](#control-structures)
- [服務注入](#service-injection)
- [模板擴充](#extending-blade)

<a name="introduction"></a>
## 簡介

Blade 模板是 Laravel 所提供的簡單且強大的模板引擎。相較於其它知名的 PHP 模板引擎， Blade 並不會限制你必須在視圖中使用 PHP 程式碼。在 Blade 被修改之前，所有的視圖都會被轉換為普通的 PHP 程式碼並產生快取，這代表著 Blade 視圖基本上對於整個系統而言並不會增加太多負擔。Blade 視圖檔案使用 `.blade.php` 做為副檔名，並儲存於 `resources/views` 資料夾。

<a name="template-inheritance"></a>
## 模板繼承

<a name="defining-a-layout"></a>
### 定義頁面佈局

使用 Blade 模板的兩個主要優點為_模板繼承_與_區塊_。從下方的 Blade 模板範例開始。首先，我們確認一下「master」的頁面佈局。由於大多數的網頁應用程式在不同頁面都保持著相同的佈局方式，用以下方式即可簡單的將佈局定義為單一的 Blade 模板視圖。

	<!-- 檔案儲存於 resources/views/layouts/master.blade.php -->

	<html>
		<head>
			<title>應用程式名稱 - @yield('title')</title>
		</head>
		<body>
			@section('sidebar')
				這是 master 的側邊欄。
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

如你所見，這個檔案包含了傳統的 HTML 語法。不過，請注意 `@section` 與 `@yield` 指令。正如其名， `@section` 指令定義一個內容區塊，而 `@yield` 指令則輸出一個已經被定義的區塊。

現在，我們已經定義了這個應用程式的佈局，讓我們來定義一個繼承此佈局的子頁面。

<a name="extending-a-layout"></a>
### 繼承頁面佈局

當定義了一個子頁面後，便可以使用 Blade 的 `@extends` 指令指定子頁面必須進行「繼承」。當視圖 `@extends（繼承）` Blade 的佈局之後，即可使用 `@section` 指令將內容注入於佈局的區塊中。切記，如上述範例，這些區塊中內容都會使用 `@yield` 被顯示在佈局中：

	<!-- 儲存於 resources/views/layouts/child.blade.php -->

	@extends('layouts.master')

	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>這邊會附加在 master 的側邊欄。</p>
	@endsection

	@section('content')
		<p>這是我的主要內容。</p>
	@endsection

在這個範例中， `sidebar` 區塊利用了 `@@parent` 指令增加（而不是覆蓋）內容至佈局的側邊欄。`@@parent` 指令會在視圖輸出時置換成佈局的內容。

當然，就像一般的 PHP 視圖， Blade 視圖可以在路由中使用全域的 `view` 輔助函式回傳：

	Route::get('blade', function () {
		return view('child');
	});

<a name="displaying-data"></a>
## 顯示資料

你可以使用「花」括號包住變數以顯示傳遞至 Blade 視圖的資料。舉例而言，就像以下的路由設定：

	Route::get('greeting', function () {
		return view('welcome', ['name' => 'Samantha']);
	});

你可以用以下方式顯示變數名字的內容：

	Hello, {{ $name }}.

當然，也不是一定只能顯示傳遞至視圖的變數內容。你也可以顯示 PHP 函示的結果。事實上，你可以放置任何你需要的的 PHP 程式碼至一個 Blade 顯示語法：

	目前 UNIX 的時間戳記為 {{ time() }}。

> **注意：**Blade 的 `{{ }}` 語法已經自動以 PHP 既有的 `htmlentites` 函式防禦 XSS 攻擊手法。

#### Blade 與 JavaScript 框架

由於許多 JavaScript 框架也使用「花」括號在瀏覽器中顯示給定的表達式，你可以使用 `@` 符號告知 Blade 渲染引擎對於該表達式應維持不變。舉個例子：

	<h1>Laravel</h1>

	Hello, @{{ name }}.

在這個範例中，`@` 符號會被 Blade 移除。而且，Blade 引擎不會改變 `{{ name }}` 表達式，如此以來便可讓其它 JavaScript 框架所應用。

#### 確認資料是否存在

有時候你想要印出一個變數，但你並不確定這個變數是否存在。我們可以用以下的 PHP 程式確定變數是否存在並印出：

	{{ isset($name) ? $name : 'Default' }}

不過，Blade 提供了較簡潔的方法替代三元運算子表示式：

	{{ $name or 'Default' }}

在這個範例中，如果 `$name` 這個變數存在，它將會被顯示出來。但是，如果這個變數不存在，便會顯示 `Default`。

#### 顯示未跳脫的資料

在預設情況下，Blade 模板中的 `{{ }}` 敘述將會自動套用 PHP 的 `htmlentities` 函式，以避免 XSS 攻擊。如果你不希望你的資料被跳脫，可以使用下列的語法：

	Hello, {!! $name !!}.

> **注意：**請非常小心處理要任何有可能出現在程式中的字串，在未經過 HTML 過濾之前，可能會造成嚴重的安全性問題。

<a name="control-structures"></a>
## 控制結構

除了模板繼承與顯示資料功能以外， Blade 也提供了方便、簡潔的 PHP 控制敘述，像是條件分歧（ if/else ）或是迴圈。在撰寫控制敘述時，這些指令將有助於寫出簡潔且可讀性高的 Blade 頁面：

#### If 陳述式

你可以使用 `@if`、`@elseif`、`@else` 及 `@endif` 指令建構 `if` 陳述式。這些指令的功能同等於於他們在 PHP 中的運作模式：

	@if (count($records) === 1)
		我有一條記錄！
	@elseif (count($records) > 1)
		我有多條記錄！
	@else
		我沒有任何記錄！
	@endif

為了方便，Blade 也提供了 `@unless` 指令：

	@unless (Auth::check())
		你尚未登入
	@endunless

#### 迴圈

除了條件陳述式外， Blade 也提供了簡易指令使用 PHP 支援的迴圈結構。

	@for ($i = 0; $i < 10; $i++)
		目前的值為 {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>此使用者為 {{ $user->id }}</p>
	@endforeach

	@forelse ($users as $user)
		<li>{{ $user->name }}</li>
	@empty
		<p>沒有使用者</p>
	@endforelse

	@while (true)
		<p>我永遠都在跑迴圈。</p>
	@endwhile

#### 引入子視圖

Blade 的 `@include` 指令，允使你簡單地引入一個已存在的 Blade 視圖。所有父視圖的變數在被引入的視圖中都是可用的。

	<div>
		@include('shared.errors')

		<form>
			<!-- 表單內容 -->
		</form>
	</div>

儘管被引入的視圖會繼承父視圖中的所有資料，你也可以傳遞額外資料的陣列至被引入的頁面：

	@include('view.name', ['some' => 'data'])

#### 註解

Blade 同時也允許在頁面中定義註解。然而，有異於 HTML 的註解， Blade 的註解並不會被顯示於在 HTML 內：

	{{-- 此註解將不會出現在渲染後的 HTML --}}

<a name="service-injection"></a>
## 服務注入

`@inject` 指令可以取出 Laravel [服務容器](/docs/{{version}}/container)中的服務。傳遞給 `@inject` 的第一個參數為替換該服務的變數名稱，而第二個參數為服務的類別或是介面的名稱：

	@inject('metrics', 'App\Services\MetricsService')

	<div>
		每月收入：{{ $metrics->monthlyRevenue() }}。
	</div>

<a name="extending-blade"></a>
## 模板擴充

Blade 模板允許客製化指令。你可以使用 `directive` 方法註冊指令。當 Blade 編譯器遇到該指令時，將會帶參數呼叫被提供的回呼。

以下範例將會建立一個給定的 `$var` 格式化的 `@datetime($var)` 指令：

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

如你所見， Laravel 的 `with` 輔助函式被用在這個指令中。`with` 輔助函式會簡單地回傳其中的 物件或值，並允許使用簡便的方法鏈結。最後此指令將會產生如以下的 PHP：

	<?php echo with($var)->format('m/d/Y H:i'); ?>



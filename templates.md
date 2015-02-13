# 模板

- [Blade 模板](#blade-templating)
- [其他 Blade 控制語法結構](#other-blade-control-structures)
- [擴展 Blade](#extending-blade)

<a name="blade-templating"></a>
## Blade 模板

Blade 是 Laravel 所提供的一個簡單卻又非常強大的模板引擎。不像控制器頁面佈局，Blade 是使用 _模板繼承_(template inheritance) 和 _區塊_(sections)。所有的 Blade 模板字尾名都要命名為 `.blade.php`。

#### 定義一個 Blade 頁面佈局

	<!-- Stored in resources/views/layouts/master.blade.php -->

	<html>
		<body>
			@section('sidebar')
				This is the master sidebar.
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

#### 在檢視模板中使用 Blade 頁面佈局

	@extends('layouts.master')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

請注意 如果檢視 `繼承(extend)` 了一個 Blade 頁面佈局會將頁面佈局中定義的區塊用檢視的所定義的區塊重寫。如果想要將頁面佈局中的區塊內容也能在繼承此佈局的檢視中呈現，那就要在區塊中使用 `@@parent` 語法指令，通過這種方式可以把內容附加到頁面佈局中，我們會在側邊欄區塊或者頁尾區塊看到類似的使用。

有時候，如您不確定這個區塊內容有沒有被定義，您可能會想要傳一個預設的值給 @yield。您可以傳入第二個參數作為預設值給 @yield：

	@yield('section', 'Default Content')

<a name="other-blade-control-structures"></a>
## 其他 Blade 控制語法結構

#### 在 Blade 檢視中列印（Echoing）資料

	Hello, {{ $name }}.

	The current UNIX timestamp is {{ time() }}.

#### 檢查資料是否存在後再列印資料

有時候您想要列印一個變數，但您不確定這個變數是否存在，通常情況下，您會想要這樣寫：:

	{{ isset($name) ? $name : 'Default' }}

	然而，除了寫這種三元運算符語法之外，Blade 讓您可以使用下面這種更簡便的語法：

	{{ $name or 'Default' }}

#### 使用花括號顯示文字

如果您需要顯示的一個字元串剛好被花括號包起來，您可以在花括號之前加上 @ 符號字首來跳出 Blade 引擎的解析：

	@{{ This will not be processed by Blade }}

如果您不想資料被轉義, 也可以使用如下語法：

	Hello, {!! $name !!}.

> **特別注意:** 在您的應用程式列印使用者所提供的內容時要非常小心。請記得永遠使用雙重花括號來轉義內容中的 HTML 實體字元串。

#### If 聲明

	@if (count($records) === 1)
		I have one record!
	@elseif (count($records) > 1)
		I have multiple records!
	@else
		I don't have any records!
	@endif

	@unless (Auth::check())
		You are not signed in.
	@endunless

#### 迴圈

	@for ($i = 0; $i < 10; $i++)
		The current value is {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>This is user {{ $user->id }}</p>
	@endforeach

	@forelse($users as $user)
	  	<li>{{ $user->name }}</li>
	@empty
	  	<p>No users</p>
	@endforelse

	@while (true)
		<p>I'm looping forever.</p>
	@endwhile

#### 載入子檢視

	@include('view.name')

您也可以通過傳入陣列的形式將資料傳遞給載入的子檢視：

	@include('view.name', ['some' => 'data'])

#### 重寫區塊

如果想要重寫掉前面區塊中的內容，您可以使用 `overwrite` 聲明：

	@extends('list.item.container')

	@section('list.item.content')
		<p>This is an item of type {{ $item->type }}</p>
	@overwrite

#### 顯示語言行

	@lang('language.line')

	@choice('language.line', 1)

#### 註釋

	{{-- This comment will not be in the rendered HTML --}}

<a name="extending-blade"></a>
## 擴展 Blade

Blade 甚至允許你定義自己的控制語法結構。 當一個 Blade 檔案被編譯時， 每一個自定義的擴展語法會與檢視內容一起被呼叫， 您可以做任何的操作, 簡單如 `str_replace` 以及更為複雜的正則表示式。

Blade 的編譯器帶有一些輔助方法 `createMatcher` 及 `createPlainMatcher`，這些輔助方法可以產生您需要的表示式來幫助您構建自己的自定義擴展語法。

其中 `createPlainMatcher` 方法是用在沒有參數的語法指令如 `@endif` 及 `@stop` 等， 而 `createMatcher` 方法是用在帶參數的語法指令中。

下面的例子創建了一個 `@datetime($var)` 語法命令, 這個命令只是簡單的對 `$var` 呼叫 `->format()` 方法：

	Blade::extend(function($view, $compiler)
	{
		$pattern = $compiler->createMatcher('datetime');

		return preg_replace($pattern, '$1<?php echo $2->format(\'m/d/Y H:i\'); ?>', $view);
	});

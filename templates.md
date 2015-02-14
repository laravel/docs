# 模板

- [Blade 模板](#blade-templating)
- [其他 Blade 控制語法結構](#other-blade-control-structures)
- [擴展 Blade](#extending-blade)

<a name="blade-templating"></a>
## Blade 模板

Blade 是 Laravel 所提供的一個簡單卻又非常強大的模板引擎。不像控制器頁面佈局，Blade 是使用 _模板繼承_（ template inheritance ）和 _區塊_（ sections ）。所有的 Blade 模板命名都要以 `.blade.php` 結尾。

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

#### 使用 Blade 頁面佈局

	@extends('layouts.master')

	@section('sidebar')
		@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

請注意，`extend` Blade 頁面佈局的視圖，只是覆寫頁面佈局中定義的 section。如果在繼承的頁面裡，想顯示原本頁面佈局中 section 裡的內容，那就要在 section 中使用 `@parent`  語法，把內容附加到頁面佈局中，像是側邊欄區塊或者頁尾區塊。

在某些時候，像是不確定 section 有沒有被定義，你可能會想要傳一個預設的值給 `@yield`。可以傳入第二個參數作為預設值：

	@yield('section', 'Default Content')

<a name="other-blade-control-structures"></a>
## 其他 Blade 控制語法結構

#### 印出資料

	Hello, {{ $name }}.

	The current UNIX timestamp is {{ time() }}.

#### 確認資料存在才印出

有時候您想要印出一個變數，但您不確定這個變數是否存在，基本上，你會想要這樣做：

	{{ isset($name) ? $name : 'Default' }}

	然而，比起使用三元運算子，Blade 讓您可以使用下面這種更簡便的語法：

	{{ $name or 'Default' }}

#### 使用大括號顯示文字

如果需要顯示一個被大括號包起來的字串，您可以在大括號之前加上 `@` 符號跳脫 Blade 的解析：

	@{{ This will not be processed by Blade }}

如果您不想資料被轉義, 也可以使用如下語法：

	Hello, {!! $name !!}.

> **注意:** 在應用程式裡印出使用者所提供的內容時要非常小心。請記得永遠使用三重大括號來轉義內容中的 HTML 字碼。

#### If 語法

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

#### 載入子視圖

	@include('view.name')

您也可以傳入陣列資料傳遞到載入的子視圖：

	@include('view.name', ['some' => 'data'])

#### 覆寫區塊

如果想要重寫掉前面區塊中的內容，您可以使用 `overwrite` 語法：

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

Blade 甚至允許你定義自己的控制語法結構。 當一個 Blade 檔案被編譯時，每一個自定義的擴展語法會與視圖一起被呼叫， 您可以做任何的操作, 簡單的從 `str_replace` 或甚至是複雜的正則表示式。

Blade 的編譯器帶有一些輔助方法 `createMatcher` 及 `createPlainMatcher`，這些輔助方法可以產生您需要的表示式來幫助您構建自己的自定義擴展語法。

`createPlainMatcher` 方法是用在沒有參數的語法指令如 `@endif` 及 `@stop` 等， 而 `createMatcher` 方法是用在帶參數的語法指令中。

下面的例子創建了一個 `@datetime($var)` 語法, 簡單的對 `$var` 呼叫 `->format()` 方法：

	Blade::extend(function($view, $compiler)
	{
		$pattern = $compiler->createMatcher('datetime');

		return preg_replace($pattern, '$1<?php echo $2->format(\'m/d/Y H:i\'); ?>', $view);
	});

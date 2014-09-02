# 模板

- [控制器版面佈局](#controller-layouts)
- [Blade 模板](#blade-templating)
- [其他 Blade 控制語法結構](#other-blade-control-structures)
- [擴展 Blade](#extending-blade)

<a name="controller-layouts"></a>
## 控制器版面佈局

在 Laravel 中使用模板的其中一個方法就是利用控制器中的 `layout` 版面佈局屬性。藉由指定控制器中的 `layout` 屬性值，被指定使用的視圖將會被自動創建出來，並作為控制器中動作的回應。

#### 在控制器中定義一個版面佈局

	class UserController extends BaseController {

		/**
		 * The layout that should be used for responses.
		 */
		protected $layout = 'layouts.master';

		/**
		 * Show the user profile.
		 */
		public function showProfile()
		{
			$this->layout->content = View::make('user.profile');
		}

	}

<a name="blade-templating"></a>
## Blade 模板

Blade 是 Laravel 所提供的一個簡單卻又非常強大的模板引擎。與制器版面佈局不同的地方在於 Blade 是使用 _模板繼承（template inheritance）_ 及 _區塊（sections）_ 來創建出視圖。所有的 Blade 模板的副檔名都要命名為 `.blade.php`。

#### 定義一個 Blade 版面佈局

	<!-- Stored in app/views/layouts/master.blade.php -->

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

#### 在視圖模板中使用 Blade 版面佈局

	@extends('layouts.master')

	@section('sidebar')
		@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

請注意在視圖中 `extend` 一個 Blade 版面佈局會直接將版面佈局中定義的區塊部分用視圖的區塊部份覆寫掉。如果想要將版面佈局中的區塊內容也能在繼承此版面佈局的視圖中呈現，那就要在區塊中使用 `@parent` 語法，這樣就可以讓你將視圖的區塊內容附加到版面佈局區塊的內容，而不會是用覆寫的方式。我們可能會在側邊欄區塊或是頁尾區塊使用類似的技巧。

有時候，像是你不確定這個區塊內容有沒有被定義，你可能會想要傳一個預設的內容給 `@yield`。你可以使用第二個參數傳入一個預設值給 `@yield`：

	@yield('section', 'Default Content');

<a name="other-blade-control-structures"></a>
## 其他 Blade 控制語法結構

#### 在 Blade 視圖中印出（Echoing）資料

	Hello, {{{ $name }}}.

	The current UNIX timestamp is {{{ time() }}}.

#### 檢查資料是否存在後再印出資料

有時候你想要印出一個變數，但你不確定這個變數有沒有被設定，基本上，你會想要這樣寫：

	{{{ isset($name) ? $name : 'Default' }}}

然而，除了寫這種三元敘述語法之外，Blade 讓你可以使用下面這種更簡便的語法：

	{{{ $name or 'Default' }}}

#### 使用花括號顯示文字

如果你需要顯示一串字串剛好被花刮號包起來，你可以在花刮號之前加上 `@` 符號前綴來跳脫 Blade 引擎的行為：

	@{{ This will not be processed by Blade }}

當然，所有使用者所提供的資料應該都要被處理過以避免一些安全性問題。所以你可以使用三重花刮號來跳脫使用者輸入的危險字元：

	Hello, {{{ $name }}}.

如果你希望印出使用者輸入的原生文字而不希望跳脫這些字元，你可以使用雙重花刮號來印出原生文字：

	Hello, {{ $name }}.

> **特別注意：** 在你的應用程式印出使用者所提供的內容時要非常小心！請記得永遠使用三重花刮號的語法來跳脫內容中的 HTML 字元實體。

#### If 敘述語法

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

#### 包含子視圖

	@include('view.name')

你可以利用傳陣列的方式將資料傳給包含進來的子視圖：

	@include('view.name', array('some'=>'data'))

#### 覆寫區塊

在預設的情況中，區塊的內容會附加進去之前的同一個區塊內容裡，如果想要覆寫掉前面區塊中的內容，你可以使用 `overwrite` 敘述語法：

	@extends('list.item.container')

	@section('list.item.content')
		<p>This is an item of type {{ $item->type }}</p>
	@overwrite

#### 顯示語言行

	@lang('language.line')

	@choice('language.line', 1);

#### 註解

	{{-- This comment will not be in the rendered HTML --}}

<a name="extending-blade"></a>
## 擴展 Blade

Blade 甚至讓你可以定義自己的客製化控制語法結構。當一個 Blade 檔案被編譯時，每一個客製化擴展語法會與視圖內容一起被呼叫，讓你可以做任何像是單純的 `str_replace` 操作至更為複雜的正規表達式操作。

Blade 的編譯器帶有一些輔助方法 `createMatcher` 及 `createPlainMatcher`，這些輔助方法可以產生你需要的表達式幫助你建制自己的客製化擴展語法。

其中 `createPlainMatcher` 方法是用在沒有參數的語法指令像是 `@endif` 及 `@stop` 等，而 `createMatcher` 方法是用在有參數的語法指令。

下面的例子創建了一個 `@datetime($var)` 語法指令，這個指令單純是讓 `$var` 呼叫 `->format()`：

	Blade::extend(function($view, $compiler)
	{
		$pattern = $compiler->createMatcher('datetime');

		return preg_replace($pattern, '$1<?php echo $2->format(\'m/d/Y H:i\'); ?>', $view);
	});

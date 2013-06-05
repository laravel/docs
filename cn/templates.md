# 模板

- [控制器布局](#controller-layouts)
- [Blade模板](#blade-templating)
- [其他 Blade模板 控制结构](#other-blade-control-structures)

<a name="controller-layouts"></a>
## 控制器布局

在Laravel框架中使用模板的一种方法就是通过控制器布局。通过在控制器中指定 `layout` 属性，对应的视图会被创建并且作为请求的默认返回数据。

**在控制器中定义一个布局**

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
## Blade模板

Blade是Laravel框架下的一种简单又强大的模板引擎。 
不同于控制器布局，Blade模板引擎由模板继承和模板片段驱动。所有的Blade模板文件必须使用Blade `.blade.php` 文件扩展名。


**定义一个Blade布局**

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

**使用一个Blade布局**

	@extends('layouts.master')

	@section('sidebar')
		@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

注意一个Blade布局的扩展视图简单地在布局中替换了模板片段。通过在模板片段中使用 `@parent` 指令，布局的内容可以被包含在一个子视图中，这样你就可以在布局片段中添加诸如侧边栏、底部信息的内容。

<a name="other-blade-control-structures"></a>
## 其他 Blade模板 控制结构

**输出数据**

	Hello, {{ $name }}.

	The current UNIX timestamp is {{ time() }}.

你可以使用三联大括号语法来避免输出：

	Hello, {{{ $name }}}.

**If 声明**

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

**循环**

	@for ($i = 0; $i < 10; $i++)
		The current value is {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>This is user {{ $user->id }}</p>
	@endforeach

	@while (true)
		<p>I'm looping forever.</p>
	@endwhile

**包含子视图**

	@include('view.name')

**输出多语言（Language Lines）**

	@lang('language.line')

	@choice('language.line', 1);

**注释**

	{{-- This comment will not be in the rendered HTML --}}

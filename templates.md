# Templates

- [Blade Templating](#blade-templating)
- [Other Blade Control Structures](#other-blade-control-structures)

<a name="blade-templating"></a>
## Blade Templating

Blade is a simple, yet powerful templating engine provided with Laravel. Unlike controller layouts, Blade is driven by _template inheritance_ and _sections_. All Blade templates should use the `.blade.php` extension.

#### Defining A Blade Layout

	<!-- Stored in resources/views/layouts/master.blade.php -->

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

#### Using A Blade Layout

	@extends('layouts.master')
	
	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@stop

	@section('content')
		<p>This is my body content.</p>
	@stop

Note that views which `extend` a Blade layout simply override sections from the layout. Content of the layout can be included in a child view using the `@@parent` directive in a section, allowing you to append to the contents of a layout section such as a sidebar or footer.

Sometimes, such as when you are not sure if a section has been defined, you may wish to pass a default value to the `@yield` directive. You may pass the default value as the second argument:

	@yield('section', 'Default Content')

<a name="other-blade-control-structures"></a>
## Other Blade Control Structures

#### Echoing Data

	Hello, {{ $name }}.

	The current UNIX timestamp is {{ time() }}.

#### Echoing Data After Checking For Existence

Sometimes you may wish to echo a variable, but you aren't sure if the variable has been set. Basically, you want to do this:

	{{ isset($name) ? $name : 'Default' }}

However, instead of writing a ternary statement, Blade allows you to use the following convenient short-cut:

	{{ $name or 'Default' }}

#### Displaying Raw Text With Curly Braces

If you need to display a string that is wrapped in curly braces, you may escape the Blade behavior by prefixing your text with an `@` symbol:

	@{{ This will not be processed by Blade }}

If you don't want the data to be escaped, you may use the following syntax:

	Hello, {!! $name !!}.

> **Note:** Be very careful when echoing content that is supplied by users of your application. Always use the double curly brace syntax to escape any HTML entities in the content.

#### If Statements

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

#### Loops

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

#### Including Sub-Views

	@include('view.name')

You may also pass an array of data to the included view:

	@include('view.name', ['some' => 'data'])

#### Overwriting Sections

To overwrite a section entirely, you may use the `overwrite` statement:

	@extends('list.item.container')

	@section('list.item.content')
		<p>This is an item of type {{ $item->type }}</p>
	@overwrite

#### Displaying Language Lines

	@lang('language.line')

	@choice('language.line', 1)

#### Comments

	{{-- This comment will not be in the rendered HTML --}}


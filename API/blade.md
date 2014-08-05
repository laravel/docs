# Blade

Blade is Laravel's templating language.

- [Yield](#yield)
- [If, else, endif](#if-else)
- [Sections](#sections)

___

<a name="yield"></a>

### @yield

The `yield` keyword word means yield, or make way, for the content specified. It tells Laravel where to put the desired content. It works like `include` in straight PHP.

*This keyword does not require `{{ }}` (curly braces), but does require an `@` before it.*

#### Example

    @yield('content')

___

<a name="if-else"></a>

### @if @else @endif

The `if`, `else` and `endif` commands form the if/else conditionals. The `if` and `endif` commands are both required.

*This keyword does not require `{{ }}` (curly braces), but does require an `@` before it.*

#### Example

	@if(Auth::user())
		<li>{{ Auth::user()->username }}</li>
	@else
		<li>{{ HTML::link('login', 'Login') }}
	@endif


### @extends

The extends keyword tells Laravel what other content a page will inherit, such as style or layout. It can be used to apply a certain master layout to a page, the `@section` is use to define it's unique parts

#### Example

	@extends('master')

___

<a name="sections"></a>

### @section and @stop

The `section` keyword lets you define and name content that Laravel will use in constructing your pages. The names of the sctions can be placed on a layout with `@yield`.

*This keyword does not require `{{ }}` (curly braces), but does require an `@` before it.*

#### Example

	@section('content')
		// your section's great content
	@stop


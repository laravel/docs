# Blade Templates

- [Introduction](#introduction)
- [Template Inheritance](#template-inheritance)
    - [Defining A Layout](#defining-a-layout)
    - [Extending A Layout](#extending-a-layout)
- [Displaying Data](#displaying-data)
    - [Blade & JavaScript Frameworks](#blade-and-javascript-frameworks)
- [Control Structures](#control-structures)
    - [If Statements](#if-statements)
    - [Switch Statements](#switch-statements)
    - [Loops](#loops)
    - [The Loop Variable](#the-loop-variable)
    - [Comments](#comments)
    - [PHP](#php)
    - [The `@once` Directive](#the-once-directive)
- [Forms](#forms)
    - [CSRF Field](#csrf-field)
    - [Method Field](#method-field)
    - [Validation Errors](#validation-errors)
- [Components](#components)
    - [Displaying Components](#displaying-components)
    - [Passing Data To Components](#passing-data-to-components)
    - [Managing Attributes](#managing-attributes)
    - [Slots](#slots)
    - [Inline Component Views](#inline-component-views)
    - [Anonymous Components](#anonymous-components)
- [Including Subviews](#including-subviews)
    - [Rendering Views For Collections](#rendering-views-for-collections)
- [Stacks](#stacks)
- [Service Injection](#service-injection)
- [Extending Blade](#extending-blade)
    - [Custom If Statements](#custom-if-statements)

<a name="introduction"></a>
## Introduction

Blade is the simple, yet powerful templating engine provided with Laravel. Unlike other popular PHP templating engines, Blade does not restrict you from using plain PHP code in your views. In fact, all Blade views are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade view files use the `.blade.php` file extension and are typically stored in the `resources/views` directory.

<a name="template-inheritance"></a>
## Template Inheritance

<a name="defining-a-layout"></a>
### Defining A Layout

Two of the primary benefits of using Blade are _template inheritance_ and _sections_. To get started, let's take a look at a simple example. First, we will examine a "master" page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view:

    <!-- Stored in resources/views/layouts/app.blade.php -->

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

<a name="extending-a-layout"></a>
### Extending A Layout

When defining a child view, use the Blade `@extends` directive to specify which layout the child view should "inherit". Views which extend a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`:

    <!-- Stored in resources/views/child.blade.php -->

    @extends('layouts.app')

    @section('title', 'Page Title')

    @section('sidebar')
        @@parent

        <p>This is appended to the master sidebar.</p>
    @endsection

    @section('content')
        <p>This is my body content.</p>
    @endsection

In this example, the `sidebar` section is utilizing the `@@parent` directive to append (rather than overwriting) content to the layout's sidebar. The `@@parent` directive will be replaced by the content of the layout when the view is rendered.

> {tip} Contrary to the previous example, this `sidebar` section ends with `@endsection` instead of `@show`. The `@endsection` directive will only define a section while `@show` will define and **immediately yield** the section.

The `@yield` directive also accepts a default value as its second parameter. This value will be rendered if the section being yielded is undefined:

    @yield('content', View::make('view.name'))

Blade views may be returned from routes using the global `view` helper:

    Route::get('blade', function () {
        return view('child');
    });

<a name="displaying-data"></a>
## Displaying Data

You may display data passed to your Blade views by wrapping the variable in curly braces. For example, given the following route:

    Route::get('greeting', function () {
        return view('welcome', ['name' => 'Samantha']);
    });

You may display the contents of the `name` variable like so:

    Hello, {{ $name }}.

> {tip} Blade `{{ }}` statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks.

You are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement:

    The current UNIX timestamp is {{ time() }}.

#### Displaying Unescaped Data

By default, Blade `{{ }}` statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax:

    Hello, {!! $name !!}.

> {note} Be very careful when echoing content that is supplied by users of your application. Always use the escaped, double curly brace syntax to prevent XSS attacks when displaying user supplied data.

#### Rendering JSON

Sometimes you may pass an array to your view with the intention of rendering it as JSON in order to initialize a JavaScript variable. For example:

    <script>
        var app = <?php echo json_encode($array); ?>;
    </script>

However, instead of manually calling `json_encode`, you may use the `@json` Blade directive. The `@json` directive accepts the same arguments as PHP's `json_encode` function:

    <script>
        var app = @json($array);

        var app = @json($array, JSON_PRETTY_PRINT);
    </script>

> {note} You should only use the `@json` directive to render existing variables as JSON. The Blade templating is based on regular expressions and attempts to pass a complex expression to the directive may cause unexpected failures.

#### HTML Entity Encoding

By default, Blade (and the Laravel `e` helper) will double encode HTML entities. If you would like to disable double encoding, call the `Blade::withoutDoubleEncoding` method from the `boot` method of your `AppServiceProvider`:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Blade::withoutDoubleEncoding();
        }
    }

<a name="blade-and-javascript-frameworks"></a>
### Blade & JavaScript Frameworks

Since many JavaScript frameworks also use "curly" braces to indicate a given expression should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example:

    <h1>Laravel</h1>

    Hello, @{{ name }}.

In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to instead be rendered by your JavaScript framework.

The `@` symbol may also be used to escape Blade directives:

    {{-- Blade --}}
    @@json()

    <!-- HTML output -->
    @json()

#### The `@verbatim` Directive

If you are displaying JavaScript variables in a large portion of your template, you may wrap the HTML in the `@verbatim` directive so that you do not have to prefix each Blade echo statement with an `@` symbol:

    @verbatim
        <div class="container">
            Hello, {{ name }}.
        </div>
    @endverbatim

<a name="control-structures"></a>
## Control Structures

In addition to template inheritance and displaying data, Blade also provides convenient shortcuts for common PHP control structures, such as conditional statements and loops. These shortcuts provide a very clean, terse way of working with PHP control structures, while also remaining familiar to their PHP counterparts.

<a name="if-statements"></a>
### If Statements

You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts:

    @if (count($records) === 1)
        I have one record!
    @elseif (count($records) > 1)
        I have multiple records!
    @else
        I don't have any records!
    @endif

For convenience, Blade also provides an `@unless` directive:

    @unless (Auth::check())
        You are not signed in.
    @endunless

In addition to the conditional directives already discussed, the `@isset` and `@empty` directives may be used as convenient shortcuts for their respective PHP functions:

    @isset($records)
        // $records is defined and is not null...
    @endisset

    @empty($records)
        // $records is "empty"...
    @endempty

#### Authentication Directives

The `@auth` and `@guest` directives may be used to quickly determine if the current user is authenticated or is a guest:

    @auth
        // The user is authenticated...
    @endauth

    @guest
        // The user is not authenticated...
    @endguest

If needed, you may specify the [authentication guard](/docs/{{version}}/authentication) that should be checked when using the `@auth` and `@guest` directives:

    @auth('admin')
        // The user is authenticated...
    @endauth

    @guest('admin')
        // The user is not authenticated...
    @endguest

#### Section Directives

You may check if a section has content using the `@hasSection` directive:

    @hasSection('navigation')
        <div class="pull-right">
            @yield('navigation')
        </div>

        <div class="clearfix"></div>
    @endif

You may use the `sectionMissing` directive to determine if a section does not have content:

    @sectionMissing('navigation')
        <div class="pull-right">
            @include('default-navigation')
        </div>
    @endif

#### Environment Directives

You may check if the application is running in the production environment using the `@production` directive:

    @production
        // Production specific content...
    @endproduction

Or, you may determine if the application is running in a specific environment using the `@env` directive:

    @env('staging')
        // The application is running in "staging"...
    @endenv
    
    @env(['staging', 'production'])
        // The application is running in "staging" or "production"...
    @endenv

<a name="switch-statements"></a>
### Switch Statements

Switch statements can be constructed using the `@switch`, `@case`, `@break`, `@default` and `@endswitch` directives:

    @switch($i)
        @case(1)
            First case...
            @break

        @case(2)
            Second case...
            @break

        @default
            Default case...
    @endswitch

<a name="loops"></a>
### Loops

In addition to conditional statements, Blade provides simple directives for working with PHP's loop structures. Again, each of these directives functions identically to their PHP counterparts:

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

> {tip} When looping, you may use the [loop variable](#the-loop-variable) to gain valuable information about the loop, such as whether you are in the first or last iteration through the loop.

When using loops you may also end the loop or skip the current iteration:

    @foreach ($users as $user)
        @if ($user->type == 1)
            @continue
        @endif

        <li>{{ $user->name }}</li>

        @if ($user->number == 5)
            @break
        @endif
    @endforeach

You may also include the condition with the directive declaration in one line:

    @foreach ($users as $user)
        @continue($user->type == 1)

        <li>{{ $user->name }}</li>

        @break($user->number == 5)
    @endforeach

<a name="the-loop-variable"></a>
### The Loop Variable

When looping, a `$loop` variable will be available inside of your loop. This variable provides access to some useful bits of information such as the current loop index and whether this is the first or last iteration through the loop:

    @foreach ($users as $user)
        @if ($loop->first)
            This is the first iteration.
        @endif

        @if ($loop->last)
            This is the last iteration.
        @endif

        <p>This is user {{ $user->id }}</p>
    @endforeach

If you are in a nested loop, you may access the parent loop's `$loop` variable via the `parent` property:

    @foreach ($users as $user)
        @foreach ($user->posts as $post)
            @if ($loop->parent->first)
                This is first iteration of the parent loop.
            @endif
        @endforeach
    @endforeach

The `$loop` variable also contains a variety of other useful properties:

Property  | Description
------------- | -------------
`$loop->index`  |  The index of the current loop iteration (starts at 0).
`$loop->iteration`  |  The current loop iteration (starts at 1).
`$loop->remaining`  |  The iterations remaining in the loop.
`$loop->count`  |  The total number of items in the array being iterated.
`$loop->first`  |  Whether this is the first iteration through the loop.
`$loop->last`  |  Whether this is the last iteration through the loop.
`$loop->even`  |  Whether this is an even iteration through the loop.
`$loop->odd`  |  Whether this is an odd iteration through the loop.
`$loop->depth`  |  The nesting level of the current loop.
`$loop->parent`  |  When in a nested loop, the parent's loop variable.

<a name="comments"></a>
### Comments

Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application:

    {{-- This comment will not be present in the rendered HTML --}}

<a name="php"></a>
### PHP

In some situations, it's useful to embed PHP code into your views. You can use the Blade `@php` directive to execute a block of plain PHP within your template:

    @php
        //
    @endphp

> {tip} While Blade provides this feature, using it frequently may be a signal that you have too much logic embedded within your template.

<a name="the-once-directive"></a>
### The `@once` Directive

The `@once` directive allows you to define a portion of the template that will only be evaluate once per rendering cycle. This may be useful for pushing a given piece of JavaScript into the page's header using [stacks](#stacks). For example, if you are rendering a given [component](#components) within a loop, you may wish to only push the JavaScript to the header the the first time the component is rendered:

    @once
        @push('scripts')
            <script>
                // Your custom JavaScript...
            </script>
        @endpush
    @endonce

<a name="forms"></a>
## Forms

<a name="csrf-field"></a>
### CSRF Field

Anytime you define an HTML form in your application, you should include a hidden CSRF token field in the form so that [the CSRF protection](https://laravel.com/docs/{{version}}/csrf) middleware can validate the request. You may use the `@csrf` Blade directive to generate the token field:

    <form method="POST" action="/profile">
        @csrf

        ...
    </form>

<a name="method-field"></a>
### Method Field

Since HTML forms can't make `PUT`, `PATCH`, or `DELETE` requests, you will need to add a hidden `_method` field to spoof these HTTP verbs. The `@method` Blade directive can create this field for you:

    <form action="/foo/bar" method="POST">
        @method('PUT')

        ...
    </form>

<a name="validation-errors"></a>
### Validation Errors

The `@error` directive may be used to quickly check if [validation error messages](/docs/{{version}}/validation#quick-displaying-the-validation-errors) exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message:

    <!-- /resources/views/post/create.blade.php -->

    <label for="title">Post Title</label>

    <input id="title" type="text" class="@error('title') is-invalid @enderror">

    @error('title')
        <div class="alert alert-danger">{{ $message }}</div>
    @enderror

You may pass [the name of a specific error bag](/docs/{{version}}/validation#named-error-bags) as the second parameter to the `@error` directive to retrieve validation error messages on pages containing multiple forms:

    <!-- /resources/views/auth.blade.php -->

    <label for="email">Email address</label>

    <input id="email" type="email" class="@error('email', 'login') is-invalid @enderror">

    @error('email', 'login')
        <div class="alert alert-danger">{{ $message }}</div>
    @enderror

<a name="components"></a>
## Components

Components and slots provide similar benefits to sections and layouts; however, some may find the mental model of components and slots easier to understand. There are two approaches to writing components: class based components and anonymous components.

To create a class based component, you may use the `make:component` Artisan command. To illustrate how to use components, we will create a simple `Alert` component. The `make:component` command will place the component in the `App\View\Components` directory:

    php artisan make:component Alert

The `make:component` command will also create a view template for the component. The view will be placed in the `resources/views/components` directory.

#### Manually Registering Package Components

When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory.

However, if you are building a package that utilizes Blade components, you will need to manually register your component class and its HTML tag alias. You should typically register your components in the `boot` method of your package's service provider:

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     */
    public function boot()
    {
        Blade::component('package-alert', AlertComponent::class);
    }

Once your component has been registered, it may be rendered using its tag alias:

    <x-package-alert/>

<a name="displaying-components"></a>
### Displaying Components

To display a component, you may use a Blade component tag within one of your Blade templates. Blade component tags start with the string `x-` followed by the kebab case name of the component class:

    <x-alert/>

    <x-user-profile/>

If the component class is nested deeper within the `App\View\Components` directory, you may use the `.` character to indicate directory nesting. For example, if we assume a component is located at `App\View\Components\Inputs\Button.php`, we may render it like so:

    <x-inputs.button/>

<a name="passing-data-to-components"></a>
### Passing Data To Components

You may pass data to Blade components using HTML attributes. Hard-coded, primitive values may be passed to the component using simple HTML attributes. PHP expressions and variables should be passed to the component via attributes that are prefixed with `:`:

    <x-alert type="error" :message="$message"/>

You should define the component's required data in its class constructor. All public properties on a component will automatically be made available to the component's view. It is not necessary to pass the data to the view from the component's `render` method:

    <?php

    namespace App\View\Components;

    use Illuminate\View\Component;

    class Alert extends Component
    {
        /**
         * The alert type.
         *
         * @var string
         */
        public $type;

        /**
         * The alert message.
         *
         * @var string
         */
        public $message;

        /**
         * Create the component instance.
         *
         * @param  string  $type
         * @param  string  $message
         * @return void
         */
        public function __construct($type, $message)
        {
            $this->type = $type;
            $this->message = $message;
        }

        /**
         * Get the view / contents that represent the component.
         *
         * @return \Illuminate\View\View|\Closure|string
         */
        public function render()
        {
            return view('components.alert');
        }
    }

When your component is rendered, you may display the contents of your component's public variables by echoing the variables by name:

    <div class="alert alert-{{ $type }}">
        {{ $message }}
    </div>

#### Casing

Component constructor arguments should be specified using `camelCase`, while `kebab-case` should be used when referencing the argument names in your HTML attributes. For example, given the following component constructor:

    /**
     * Create the component instance.
     *
     * @param  string  $alertType
     * @return void
     */
    public function __construct($alertType)
    {
        $this->alertType = $alertType;
    }

The `$alertType` argument may be provided like so:

    <x-alert alert-type="danger" />

#### Component Methods

In addition to public variables being available to your component template, any public methods on the component may also be executed. For example, imagine a component that has a `isSelected` method:

    /**
     * Determine if the given option is the current selected option.
     *
     * @param  string  $option
     * @return bool
     */
    public function isSelected($option)
    {
        return $option === $this->selected;
    }

You may execute this method from your component template by invoking the variable matching the name of the method:

    <option {{ $isSelected($value) ? 'selected="selected"' : '' }} value="{{ $value }}">
        {{ $label }}
    </option>

#### Using Attributes & Slots Inside The Class

Blade components also allow you to access the component name, attributes, and slot inside the class's render method. However, in order to access this data, you should return a Closure from your component's `render` method. The Closure will receive a `$data` array as its only argument:

    /**
     * Get the view / contents that represent the component.
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return function (array $data) {
            // $data['componentName'];
            // $data['attributes'];
            // $data['slot'];

            return '<div>Component content</div>';
        };
    }

The `componentName` is equal to the name used in the HTML tag after the `x-` prefix. So `<x-alert />`'s `componentName` will be `alert`. The `attributes` element will contain all of the attributes that were present on the HTML tag. The `slot` element is a `Illuminate\Support\HtmlString` instance with the contents of the slot from the component.

#### Additional Dependencies

If your component requires dependencies from Laravel's [service container](/docs/{{version}}/container), you may list them before any of the component's data attributes and they will automatically be injected by the container:

    use App\AlertCreator

    /**
     * Create the component instance.
     *
     * @param  \App\AlertCreator  $creator
     * @param  string  $type
     * @param  string  $message
     * @return void
     */
    public function __construct(AlertCreator $creator, $type, $message)
    {
        $this->creator = $creator;
        $this->type = $type;
        $this->message = $message;
    }

<a name="managing-attributes"></a>
### Managing Attributes

We've already examined how to pass data attributes to a component; however, sometimes you may need to specify additional HTML attributes, such as `class`, that are not part of the data required for a component to function. Typically, you want to pass these additional attributes down to the root element of the component template. For example, imagine we want to render an `alert` component like so:

    <x-alert type="error" :message="$message" class="mt-4"/>

All of the attributes that are not part of the component's constructor will automatically be added to the component's "attribute bag". This attribute bag is automatically made available to the component via the `$attributes` variable. All of the attributes may be rendered within the component by echoing this variable:

    <div {{ $attributes }}>
        <!-- Component Content -->
    </div>

> {note} Echoing variables (`{{ $attributes }}`) or using directives such as `@env` directly on a component is not supported at this time.

#### Default / Merged Attributes

Sometimes you may need to specify default values for attributes or merge additional values into some of the component's attributes. To accomplish this, you may use the attribute bag's `merge` method:

    <div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
        {{ $message }}
    </div>

If we assume this component is utilized like so:

    <x-alert type="error" :message="$message" class="mb-4"/>

The final, rendered HTML of the component will appear like the following:

    <div class="alert alert-error mb-4">
        <!-- Contents of the $message variable -->
    </div>

#### Filtering Attributes

You may filter attributes using the `filter` method. This method accepts a Closure which should return `true` if you wish to retain the attribute in the attribute bag:

    {{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}

For convenience, you may use the `whereStartsWith` method to retrieve all attributes whose keys begin with a given string:

    {{ $attributes->whereStartsWith('wire:model') }}

Using the `first` method, you may render the first attribute in a given attribute bag:

    {{ $attributes->whereStartsWith('wire:model')->first() }}

<a name="slots"></a>
### Slots

Often, you will need to pass additional content to your component via "slots". Let's imagine that an `alert` component we created has the following markup:

    <!-- /resources/views/components/alert.blade.php -->

    <div class="alert alert-danger">
        {{ $slot }}
    </div>

We may pass content to the `slot` by injecting content into the component:

    <x-alert>
        <strong>Whoops!</strong> Something went wrong!
    </x-alert>

Sometimes a component may need to render multiple different slots in different locations within the component. Let's modify our alert component to allow for the injection of a "title":

    <!-- /resources/views/components/alert.blade.php -->

    <span class="alert-title">{{ $title }}</span>

    <div class="alert alert-danger">
        {{ $slot }}
    </div>

You may define the content of the named slot using the `x-slot` tag. Any content not within a `x-slot` tag will be passed to the component in the `$slot` variable:

    <x-alert>
        <x-slot name="title">
            Server Error
        </x-slot>

        <strong>Whoops!</strong> Something went wrong!
    </x-alert>

#### Scoped Slots

If you have used a JavaScript framework such as Vue, you may be familiar with "scoped slots", which allow you to access data or methods from the component within your slot. You may achieve similar behavior in Laravel by defining public methods or properties on your component and accessing the component within your slot via the `$component` variable:

    <x-alert>
        <x-slot name="title">
            {{ $component->formatAlert('Server Error') }}
        </x-slot>

        <strong>Whoops!</strong> Something went wrong!
    </x-alert>

<a name="inline-component-views"></a>
### Inline Component Views

For very small components, it may feel cumbersome to manage both the component class and the component's view template. For this reason, you may return the component's markup directly from the `render` method:

    /**
     * Get the view / contents that represent the component.
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return <<<'blade'
            <div class="alert alert-danger">
                {{ $slot }}
            </div>
        blade;
    }

#### Generating Inline View Components

To create a component that renders an inline view, you may use the `inline` option when executing the `make:component` command:

    php artisan make:component Alert --inline

<a name="anonymous-components"></a>
### Anonymous Components

Similar to inline components, anonymous components provide a mechanism for managing a component via a single file. However, anonymous components utilize a single view file and have no associated class. To define an anonymous component, you only need to place a Blade template within your `resources/views/components` directory. For example, assuming you have defined a component at `resources/views/components/alert.blade.php`:

    <x-alert/>

You may use the `.` character to indicate if a component is nested deeper inside the `components` directory. For example, assuming the component is defined at `resources/views/components/inputs/button.blade.php`, you may render it like so:

    <x-inputs.button/>

#### Data Properties / Attributes

Since anonymous components do not have any associated class, you may wonder how you may differentiate which data should be passed to the component as variables and which attributes should be placed in the component's [attribute bag](#managing-attributes).

You may specify which attributes should be considered data variables using the `@props` directive at the top of your component's Blade template. All other attributes on the component will be available via the component's attribute bag. If you wish to give a data variable a default value, you may specify the variable's name as the array key and the default value as the array value:

    <!-- /resources/views/components/alert.blade.php -->

    @props(['type' => 'info', 'message'])

    <div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
        {{ $message }}
    </div>

<a name="including-subviews"></a>
## Including Subviews

Blade's `@include` directive allows you to include a Blade view from within another view. All variables that are available to the parent view will be made available to the included view:

    <div>
        @include('shared.errors')

        <form>
            <!-- Form Contents -->
        </form>
    </div>

Even though the included view will inherit all data available in the parent view, you may also pass an array of extra data to the included view:

    @include('view.name', ['some' => 'data'])

If you attempt to `@include` a view which does not exist, Laravel will throw an error. If you would like to include a view that may or may not be present, you should use the `@includeIf` directive:

    @includeIf('view.name', ['some' => 'data'])

If you would like to `@include` a view if a given boolean expression evaluates to `true`, you may use the `@includeWhen` directive:

    @includeWhen($boolean, 'view.name', ['some' => 'data'])

If you would like to `@include` a view if a given boolean expression evaluates to `false`, you may use the `@includeUnless` directive:

    @includeUnless($boolean, 'view.name', ['some' => 'data'])

To include the first view that exists from a given array of views, you may use the `includeFirst` directive:

    @includeFirst(['custom.admin', 'admin'], ['some' => 'data'])

> {note} You should avoid using the `__DIR__` and `__FILE__` constants in your Blade views, since they will refer to the location of the cached, compiled view.

#### Aliasing Includes

If your Blade includes are stored in a subdirectory, you may wish to alias them for easier access. For example, imagine a Blade include that is stored at `resources/views/includes/input.blade.php` with the following content:

    <input type="{{ $type ?? 'text' }}">

You may use the `include` method to alias the include from `includes.input` to `input`. Typically, this should be done in the `boot` method of your `AppServiceProvider`:

    use Illuminate\Support\Facades\Blade;

    Blade::include('includes.input', 'input');

Once the include has been aliased, you may render it using the alias name as the Blade directive:

    @input(['type' => 'email'])

<a name="rendering-views-for-collections"></a>
### Rendering Views For Collections

You may combine loops and includes into one line with Blade's `@each` directive:

    @each('view.name', $jobs, 'job')

The first argument is the view partial to render for each element in the array or collection. The second argument is the array or collection you wish to iterate over, while the third argument is the variable name that will be assigned to the current iteration within the view. So, for example, if you are iterating over an array of `jobs`, typically you will want to access each job as a `job` variable within your view partial. The key for the current iteration will be available as the `key` variable within your view partial.

You may also pass a fourth argument to the `@each` directive. This argument determines the view that will be rendered if the given array is empty.

    @each('view.name', $jobs, 'job', 'view.empty')

> {note} Views rendered via `@each` do not inherit the variables from the parent view. If the child view requires these variables, you should use `@foreach` and `@include` instead.

<a name="stacks"></a>
## Stacks

Blade allows you to push to named stacks which can be rendered somewhere else in another view or layout. This can be particularly useful for specifying any JavaScript libraries required by your child views:

    @push('scripts')
        <script src="/example.js"></script>
    @endpush

You may push to a stack as many times as needed. To render the complete stack contents, pass the name of the stack to the `@stack` directive:

    <head>
        <!-- Head Contents -->

        @stack('scripts')
    </head>

If you would like to prepend content onto the beginning of a stack, you should use the `@prepend` directive:

    @push('scripts')
        This will be second...
    @endpush

    // Later...

    @prepend('scripts')
        This will be first...
    @endprepend

<a name="service-injection"></a>
## Service Injection

The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/{{version}}/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class or interface name of the service you wish to resolve:

    @inject('metrics', 'App\Services\MetricsService')

    <div>
        Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
    </div>

<a name="extending-blade"></a>
## Extending Blade

Blade allows you to define your own custom directives using the `directive` method. When the Blade compiler encounters the custom directive, it will call the provided callback with the expression that the directive contains.

The following example creates a `@datetime($var)` directive which formats a given `$var`, which should be an instance of `DateTime`:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Blade::directive('datetime', function ($expression) {
                return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
            });
        }
    }

As you can see, we will chain the `format` method onto whatever expression is passed into the directive. So, in this example, the final PHP generated by this directive will be:

    <?php echo ($var)->format('m/d/Y H:i'); ?>

> {note} After updating the logic of a Blade directive, you will need to delete all of the cached Blade views. The cached Blade views may be removed using the `view:clear` Artisan command.

<a name="custom-if-statements"></a>
### Custom If Statements

Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade provides a `Blade::if` method which allows you to quickly define custom conditional directives using Closures. For example, let's define a custom conditional that checks the current application cloud provider. We may do this in the `boot` method of our `AppServiceProvider`:

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::if('cloud', function ($provider) {
            return config('filesystems.default') === $provider;
        });
    }

Once the custom conditional has been defined, we can easily use it on our templates:

    @cloud('digitalocean')
        // The application is using the digitalocean cloud provider...
    @elsecloud('aws')
        // The application is using the aws provider...
    @else
        // The application is not using the digitalocean or aws environment...
    @endcloud

    @unlesscloud('aws')
        // The application is not using the aws environment...
    @endcloud

# Blade Templates

- [Introduction](#introduction)
- [Displaying Data](#displaying-data)
    - [HTML Entity Encoding](#html-entity-encoding)
    - [Blade & JavaScript Frameworks](#blade-and-javascript-frameworks)
- [Blade Directives](#blade-directives)
    - [If Statements](#if-statements)
    - [Switch Statements](#switch-statements)
    - [Loops](#loops)
    - [The Loop Variable](#the-loop-variable)
    - [Conditional Classes](#conditional-classes)
    - [Including Subviews](#including-subviews)
    - [The `@once` Directive](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [Comments](#comments)
- [Components](#components)
    - [Rendering Components](#rendering-components)
    - [Passing Data To Components](#passing-data-to-components)
    - [Component Attributes](#component-attributes)
    - [Reserved Keywords](#reserved-keywords)
    - [Slots](#slots)
    - [Inline Component Views](#inline-component-views)
    - [Anonymous Components](#anonymous-components)
    - [Dynamic Components](#dynamic-components)
    - [Manually Registering Components](#manually-registering-components)
- [Building Layouts](#building-layouts)
    - [Layouts Using Components](#layouts-using-components)
    - [Layouts Using Template Inheritance](#layouts-using-template-inheritance)
- [Forms](#forms)
    - [CSRF Field](#csrf-field)
    - [Method Field](#method-field)
    - [Validation Errors](#validation-errors)
- [Stacks](#stacks)
- [Service Injection](#service-injection)
- [Extending Blade](#extending-blade)
    - [Custom Echo Handlers](#custom-echo-handlers)
    - [Custom If Statements](#custom-if-statements)

<a name="introduction"></a>
## Introduction

Blade is the simple, yet powerful templating engine that is included with Laravel. Unlike some PHP templating engines, Blade does not restrict you from using plain PHP code in your templates. In fact, all Blade templates are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade template files use the `.blade.php` file extension and are typically stored in the `resources/views` directory.

Blade views may be returned from routes or controller using the global `view` helper. Of course, as mentioned in the documentation on [views](/docs/{{version}}/views), data may be passed to the Blade view using the `view` helper's second argument:

    Route::get('/', function () {
        return view('greeting', ['name' => 'Finn']);
    });

> {tip} Before digging deeper into Blade, make sure to read the Laravel [view documentation](/docs/{{version}}/views).

<a name="displaying-data"></a>
## Displaying Data

You may display data that is passed to your Blade views by wrapping the variable in curly braces. For example, given the following route:

    Route::get('/', function () {
        return view('welcome', ['name' => 'Samantha']);
    });

You may display the contents of the `name` variable like so:

    Hello, {{ $name }}.

> {tip} Blade's `{{ }}` echo statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks.

You are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement:

    The current UNIX timestamp is {{ time() }}.

<a name="rendering-json"></a>
#### Rendering JSON

Sometimes you may pass an array to your view with the intention of rendering it as JSON in order to initialize a JavaScript variable. For example:

    <script>
        var app = <?php echo json_encode($array); ?>;
    </script>

However, instead of manually calling `json_encode`, you may use the `@json` Blade directive. The `@json` directive accepts the same arguments as PHP's `json_encode` function. By default, the `@json` directive calls the `json_encode` function with the `JSON_HEX_TAG`, `JSON_HEX_APOS`, `JSON_HEX_AMP`, and `JSON_HEX_QUOT` flags:

    <script>
        var app = @json($array);

        var app = @json($array, JSON_PRETTY_PRINT);
    </script>

> {note} You should only use the `@json` directive to render existing variables as JSON. The Blade templating is based on regular expressions and attempts to pass a complex expression to the directive may cause unexpected failures.

<a name="html-entity-encoding"></a>
### HTML Entity Encoding

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

<a name="displaying-unescaped-data"></a>
#### Displaying Unescaped Data

By default, Blade `{{ }}` statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax:

    Hello, {!! $name !!}.

> {note} Be very careful when echoing content that is supplied by users of your application. You should typically use the escaped, double curly brace syntax to prevent XSS attacks when displaying user supplied data.

<a name="blade-and-javascript-frameworks"></a>
### Blade & JavaScript Frameworks

Since many JavaScript frameworks also use "curly" braces to indicate a given expression should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example:

    <h1>Laravel</h1>

    Hello, @{{ name }}.

In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to be rendered by your JavaScript framework.

The `@` symbol may also be used to escape Blade directives:

    {{-- Blade template --}}
    @@json()

    <!-- HTML output -->
    @json()

<a name="the-at-verbatim-directive"></a>
#### The `@verbatim` Directive

If you are displaying JavaScript variables in a large portion of your template, you may wrap the HTML in the `@verbatim` directive so that you do not have to prefix each Blade echo statement with an `@` symbol:

    @verbatim
        <div class="container">
            Hello, {{ name }}.
        </div>
    @endverbatim

<a name="blade-directives"></a>
## Blade Directives

In addition to template inheritance and displaying data, Blade also provides convenient shortcuts for common PHP control structures, such as conditional statements and loops. These shortcuts provide a very clean, terse way of working with PHP control structures while also remaining familiar to their PHP counterparts.

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

<a name="authentication-directives"></a>
#### Authentication Directives

The `@auth` and `@guest` directives may be used to quickly determine if the current user is [authenticated](/docs/{{version}}/authentication) or is a guest:

    @auth
        // The user is authenticated...
    @endauth

    @guest
        // The user is not authenticated...
    @endguest

If needed, you may specify the authentication guard that should be checked when using the `@auth` and `@guest` directives:

    @auth('admin')
        // The user is authenticated...
    @endauth

    @guest('admin')
        // The user is not authenticated...
    @endguest

<a name="environment-directives"></a>
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

<a name="section-directives"></a>
#### Section Directives

You may determine if a template inheritance section has content using the `@hasSection` directive:

```html
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

You may use the `sectionMissing` directive to determine if a section does not have content:

```html
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

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

When using loops you may also end the loop or skip the current iteration using the `@continue` and `@break` directives:

    @foreach ($users as $user)
        @if ($user->type == 1)
            @continue
        @endif

        <li>{{ $user->name }}</li>

        @if ($user->number == 5)
            @break
        @endif
    @endforeach

You may also include the continuation or break condition within the directive declaration:

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
                This is the first iteration of the parent loop.
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

<a name="conditional-classes"></a>
### Conditional Classes

The `@class` directive conditionally compiles a CSS class string. The directive accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list:

    @php
        $isActive = false;
        $hasError = true;
    @endphp

    <span @class([
        'p-4',
        'font-bold' => $isActive,
        'text-gray-500' => ! $isActive,
        'bg-red' => $hasError,
    ])></span>

    <span class="p-4 text-gray-500 bg-red"></span>

<a name="including-subviews"></a>
### Including Subviews

> {tip} While you're free to use the `@include` directive, Blade [components](#components) provide similar functionality and offer several benefits over the `@include` directive such as data and attribute binding.

Blade's `@include` directive allows you to include a Blade view from within another view. All variables that are available to the parent view will be made available to the included view:

```html
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

Even though the included view will inherit all data available in the parent view, you may also pass an array of additional data that should be made available to the included view:

    @include('view.name', ['status' => 'complete'])

If you attempt to `@include` a view which does not exist, Laravel will throw an error. If you would like to include a view that may or may not be present, you should use the `@includeIf` directive:

    @includeIf('view.name', ['status' => 'complete'])

If you would like to `@include` a view if a given boolean expression evaluates to `true` or `false`, you may use the `@includeWhen` and `@includeUnless` directives:

    @includeWhen($boolean, 'view.name', ['status' => 'complete'])

    @includeUnless($boolean, 'view.name', ['status' => 'complete'])

To include the first view that exists from a given array of views, you may use the `includeFirst` directive:

    @includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])

> {note} You should avoid using the `__DIR__` and `__FILE__` constants in your Blade views, since they will refer to the location of the cached, compiled view.

<a name="rendering-views-for-collections"></a>
#### Rendering Views For Collections

You may combine loops and includes into one line with Blade's `@each` directive:

    @each('view.name', $jobs, 'job')

The `@each` directive's first argument is the view to render for each element in the array or collection. The second argument is the array or collection you wish to iterate over, while the third argument is the variable name that will be assigned to the current iteration within the view. So, for example, if you are iterating over an array of `jobs`, typically you will want to access each job as a `job` variable within the view. The array key for the current iteration will be available as the `key` variable within the view.

You may also pass a fourth argument to the `@each` directive. This argument determines the view that will be rendered if the given array is empty.

    @each('view.name', $jobs, 'job', 'view.empty')

> {note} Views rendered via `@each` do not inherit the variables from the parent view. If the child view requires these variables, you should use the `@foreach` and `@include` directives instead.

<a name="the-once-directive"></a>
### The `@once` Directive

The `@once` directive allows you to define a portion of the template that will only be evaluated once per rendering cycle. This may be useful for pushing a given piece of JavaScript into the page's header using [stacks](#stacks). For example, if you are rendering a given [component](#components) within a loop, you may wish to only push the JavaScript to the header the first time the component is rendered:

    @once
        @push('scripts')
            <script>
                // Your custom JavaScript...
            </script>
        @endpush
    @endonce

<a name="raw-php"></a>
### Raw PHP

In some situations, it's useful to embed PHP code into your views. You can use the Blade `@php` directive to execute a block of plain PHP within your template:

    @php
        $counter = 1;
    @endphp

<a name="comments"></a>
### Comments

Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application:

    {{-- This comment will not be present in the rendered HTML --}}

<a name="components"></a>
## Components

Components and slots provide similar benefits to sections, layouts, and includes; however, some may find the mental model of components and slots easier to understand. There are two approaches to writing components: class based components and anonymous components.

To create a class based component, you may use the `make:component` Artisan command. To illustrate how to use components, we will create a simple `Alert` component. The `make:component` command will place the component in the `App\View\Components` directory:

    php artisan make:component Alert

The `make:component` command will also create a view template for the component. The view will be placed in the `resources/views/components` directory. When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory, so no further component registration is typically required.

You may also create components within subdirectories:

    php artisan make:component Forms/Input

The command above will create an `Input` component in the `App\View\Components\Forms` directory and the view will be placed in the `resources/views/components/forms` directory.

<a name="manually-registering-package-components"></a>
#### Manually Registering Package Components

When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory.

However, if you are building a package that utilizes Blade components, you will need to manually register your component class and its HTML tag alias. You should typically register your components in the `boot` method of your package's service provider:

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     */
    public function boot()
    {
        Blade::component('package-alert', Alert::class);
    }

Once your component has been registered, it may be rendered using its tag alias:

    <x-package-alert/>

Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace:

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

This will allow the usage of package components by their vendor namespace using the `package-name::` syntax:

    <x-nightshade::calendar />
    <x-nightshade::color-picker />

Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation.

<a name="rendering-components"></a>
### Rendering Components

To display a component, you may use a Blade component tag within one of your Blade templates. Blade component tags start with the string `x-` followed by the kebab case name of the component class:

    <x-alert/>

    <x-user-profile/>

If the component class is nested deeper within the `App\View\Components` directory, you may use the `.` character to indicate directory nesting. For example, if we assume a component is located at `App\View\Components\Inputs\Button.php`, we may render it like so:

    <x-inputs.button/>

<a name="passing-data-to-components"></a>
### Passing Data To Components

You may pass data to Blade components using HTML attributes. Hard-coded, primitive values may be passed to the component using simple HTML attribute strings. PHP expressions and variables should be passed to the component via attributes that use the `:` character as a prefix:

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

```html
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
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

The `$alertType` argument may be provided to the component like so:

    <x-alert alert-type="danger" />

<a name="escaping-attribute-rendering"></a>
#### Escaping Attribute Rendering

Since some JavaScript frameworks such as Alpine.js also use colon-prefixed attributes, you may use a double colon (`::`) prefix to inform Blade that the attribute is not a PHP expression. For example, given the following component:

    <x-button ::class="{ danger: isDeleting }">
        Submit
    </x-button>

The following HTML will be rendered by Blade:

    <button :class="{ danger: isDeleting }">
        Submit
    </button>

<a name="component-methods"></a>
#### Component Methods

In addition to public variables being available to your component template, any public methods on the component may be invoked. For example, imagine a component that has an `isSelected` method:

    /**
     * Determine if the given option is the currently selected option.
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

<a name="using-attributes-slots-within-component-class"></a>
#### Accessing Attributes & Slots Within Component Classes

Blade components also allow you to access the component name, attributes, and slot inside the class's render method. However, in order to access this data, you should return a closure from your component's `render` method. The closure will receive a `$data` array as its only argument. This array will contain several elements that provide information about the component:

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

            return '<div>Components content</div>';
        };
    }

The `componentName` is equal to the name used in the HTML tag after the `x-` prefix. So `<x-alert />`'s `componentName` will be `alert`. The `attributes` element will contain all of the attributes that were present on the HTML tag. The `slot` element is an `Illuminate\Support\HtmlString` instance with the contents of the component's slot.

The closure should return a string. If the returned string corresponds to an existing view, that view will be rendered; otherwise, the returned string will be evaluated as an inline Blade view.

<a name="additional-dependencies"></a>
#### Additional Dependencies

If your component requires dependencies from Laravel's [service container](/docs/{{version}}/container), you may list them before any of the component's data attributes and they will automatically be injected by the container:

    use App\Services\AlertCreator

    /**
     * Create the component instance.
     *
     * @param  \App\Services\AlertCreator  $creator
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

<a name="hiding-attributes-and-methods"></a>
#### Hiding Attributes / Methods

If you would like to prevent some public methods or properties from being exposed as variables to your component template, you may add them to an `$except` array property on your component:

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
         * The properties / methods that should not be exposed to the component template.
         *
         * @var array
         */
        protected $except = ['type'];
    }

<a name="component-attributes"></a>
### Component Attributes

We've already examined how to pass data attributes to a component; however, sometimes you may need to specify additional HTML attributes, such as `class`, that are not part of the data required for a component to function. Typically, you want to pass these additional attributes down to the root element of the component template. For example, imagine we want to render an `alert` component like so:

    <x-alert type="error" :message="$message" class="mt-4"/>

All of the attributes that are not part of the component's constructor will automatically be added to the component's "attribute bag". This attribute bag is automatically made available to the component via the `$attributes` variable. All of the attributes may be rendered within the component by echoing this variable:

    <div {{ $attributes }}>
        <!-- Component content -->
    </div>

> {note} Using directives such as `@env` within component tags is not supported at this time. For example, `<x-alert :live="@env('production')"/>` will not be compiled.

<a name="default-merged-attributes"></a>
#### Default / Merged Attributes

Sometimes you may need to specify default values for attributes or merge additional values into some of the component's attributes. To accomplish this, you may use the attribute bag's `merge` method. This method is particularly useful for defining a set of default CSS classes that should always be applied to a component:

    <div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
        {{ $message }}
    </div>

If we assume this component is utilized like so:

    <x-alert type="error" :message="$message" class="mb-4"/>

The final, rendered HTML of the component will appear like the following:

```html
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### Conditionally Merge Classes

Sometimes you may wish to merge classes if a given condition is `true`. You can accomplish this via the `class` method, which accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list:

    <div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
        {{ $message }}
    </div>

If you need to merge other attributes onto your component, you can chain the `merge` method onto the `class` method:

    <button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
        {{ $slot }}
    </button>

> {tip} If you need to conditionally compile classes on other HTML elements that shouldn't receive merged attributes, you can use the [`@class` directive](#conditional-classes).

<a name="non-class-attribute-merging"></a>
#### Non-Class Attribute Merging

When merging attributes that are not `class` attributes, the values provided to the `merge` method will be considered the "default" values of the attribute. However, unlike the `class` attribute, these attributes will not be merged with injected attribute values. Instead, they will be overwritten. For example, a `button` component's implementation may look like the following:

    <button {{ $attributes->merge(['type' => 'button']) }}>
        {{ $slot }}
    </button>

To render the button component with a custom `type`, it may be specified when consuming the component. If no type is specified, the `button` type will be used:

    <x-button type="submit">
        Submit
    </x-button>

The rendered HTML of the `button` component in this example would be:

    <button type="submit">
        Submit
    </button>

If you would like an attribute other than `class` to have its default value and injected values joined together, you may use the `prepends` method. In this example, the `data-controller` attribute will always begin with `profile-controller` and any additional injected `data-controller` values will be placed after this default value:

    <div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
        {{ $slot }}
    </div>

<a name="filtering-attributes"></a>
#### Retrieving & Filtering Attributes

You may filter attributes using the `filter` method. This method accepts a closure which should return `true` if you wish to retain the attribute in the attribute bag:

    {{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}

For convenience, you may use the `whereStartsWith` method to retrieve all attributes whose keys begin with a given string:

    {{ $attributes->whereStartsWith('wire:model') }}

Conversely, the `whereDoesntStartWith` method may be used to exclude all attributes whose keys begin with a given string:

    {{ $attributes->whereDoesntStartWith('wire:model') }}

Using the `first` method, you may render the first attribute in a given attribute bag:

    {{ $attributes->whereStartsWith('wire:model')->first() }}

If you would like to check if an attribute is present on the component, you may use the `has` method. This method accepts the attribute name as its only argument and returns a boolean indicating whether or not the attribute is present:

    @if ($attributes->has('class'))
        <div>Class attribute is present</div>
    @endif

You may retrieve a specific attribute's value using the `get` method:

    {{ $attributes->get('class') }}

<a name="reserved-keywords"></a>
### Reserved Keywords

By default, some keywords are reserved for Blade's internal use in order to render components. The following keywords cannot be defined as public properties or method names within your components:

<div class="content-list" markdown="1">
- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`
</div>

<a name="slots"></a>
### Slots

You will often need to pass additional content to your component via "slots". Component slots are rendered by echoing the `$slot` variable. To explore this concept, let's imagine that an `alert` component has the following markup:

```html
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

We may pass content to the `slot` by injecting content into the component:

```html
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

Sometimes a component may need to render multiple different slots in different locations within the component. Let's modify our alert component to allow for the injection of a "title" slot:

```html
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

You may define the content of the named slot using the `x-slot` tag. Any content not within an explicit `x-slot` tag will be passed to the component in the `$slot` variable:

```html
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="scoped-slots"></a>
#### Scoped Slots

If you have used a JavaScript framework such as Vue, you may be familiar with "scoped slots", which allow you to access data or methods from the component within your slot. You may achieve similar behavior in Laravel by defining public methods or properties on your component and accessing the component within your slot via the `$component` variable. In this example, we will assume that the `x-alert` component has a public `formatAlert` method defined on its component class:

```html
<x-alert>
    <x-slot name="title">
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
#### Slot Attributes

Like Blade components, you may assign additional [attributes](#component-attributes) to slots such as CSS class names:

```html
<x-card class="shadow-sm">
    <x-slot name="heading" class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot name="footer" class="text-sm">
        Footer
    </x-slot>
</x-card>
```

To interact with slot attributes, you may access the `attributes` property of the slot's variable. For more information on how to interact with attributes, please consult the documentation on [component attributes](#component-attributes):

```php
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```

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

<a name="generating-inline-view-components"></a>
#### Generating Inline View Components

To create a component that renders an inline view, you may use the `inline` option when executing the `make:component` command:

    php artisan make:component Alert --inline

<a name="anonymous-components"></a>
### Anonymous Components

Similar to inline components, anonymous components provide a mechanism for managing a component via a single file. However, anonymous components utilize a single view file and have no associated class. To define an anonymous component, you only need to place a Blade template within your `resources/views/components` directory. For example, assuming you have defined a component at `resources/views/components/alert.blade.php`, you may simply render it like so:

    <x-alert/>

You may use the `.` character to indicate if a component is nested deeper inside the `components` directory. For example, assuming the component is defined at `resources/views/components/inputs/button.blade.php`, you may render it like so:

    <x-inputs.button/>

<a name="data-properties-attributes"></a>
#### Data Properties / Attributes

Since anonymous components do not have any associated class, you may wonder how you may differentiate which data should be passed to the component as variables and which attributes should be placed in the component's [attribute bag](#component-attributes).

You may specify which attributes should be considered data variables using the `@props` directive at the top of your component's Blade template. All other attributes on the component will be available via the component's attribute bag. If you wish to give a data variable a default value, you may specify the variable's name as the array key and the default value as the array value:

    <!-- /resources/views/components/alert.blade.php -->

    @props(['type' => 'info', 'message'])

    <div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
        {{ $message }}
    </div>

Given the component definition above, we may render the component like so:

    <x-alert type="error" :message="$message" class="mb-4"/>

<a name="dynamic-components"></a>
### Dynamic Components

Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable:

    <x-dynamic-component :component="$componentName" class="mt-4" />

<a name="manually-registering-components"></a>
### Manually Registering Components

> {note} The following documentation on manually registering components is primarily applicable to those who are writing Laravel packages that include view components. If you are not writing a package, this portion of the component documentation may not be relevant to you.

When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory.

However, if you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider:

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    /**
     * Bootstrap your package's services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::component('package-alert', AlertComponent::class);
    }

Once your component has been registered, it may be rendered using its tag alias:

    <x-package-alert/>

#### Autoloading Package Components

Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace:

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

This will allow the usage of package components by their vendor namespace using the `package-name::` syntax:

    <x-nightshade::calendar />
    <x-nightshade::color-picker />

Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation.

<a name="building-layouts"></a>
## Building Layouts

<a name="layouts-using-components"></a>
### Layouts Using Components

Most web applications maintain the same general layout across various pages. It would be incredibly cumbersome and hard to maintain our application if we had to repeat the entire layout HTML in every view we create. Thankfully, it's convenient to define this layout as a single [Blade component](#components) and then use it throughout our application.

<a name="defining-the-layout-component"></a>
#### Defining The Layout Component

For example, imagine we are building a "todo" list application. We might define a `layout` component that looks like the following:

```html
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```

<a name="applying-the-layout-component"></a>
#### Applying The Layout Component

Once the `layout` component has been defined, we may create a Blade view that utilizes the component. In this example, we will define a simple view that displays our task list:

```html
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

Remember, content that is injected into a component will be supplied to the default `$slot` variable within our `layout` component. As you may have noticed, our `layout` also respects a `$title` slot if one is provided; otherwise, a default title is shown. We may inject a custom title from our task list view using the standard slot syntax discussed in the [component documentation](#components):

```html
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot name="title">
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

Now that we have defined our layout and task list views, we just need to return the `task` view from a route:

    use App\Models\Task;

    Route::get('/tasks', function () {
        return view('tasks', ['tasks' => Task::all()]);
    });

<a name="layouts-using-template-inheritance"></a>
### Layouts Using Template Inheritance

<a name="defining-a-layout"></a>
#### Defining A Layout

Layouts may also be created via "template inheritance". This was the primary way of building applications prior to the introduction of [components](#components).

To get started, let's take a look at a simple example. First, we will examine a page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view:

```html
<!-- resources/views/layouts/app.blade.php -->

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
```

As you can see, this file contains typical HTML mark-up. However, take note of the `@section` and `@yield` directives. The `@section` directive, as the name implies, defines a section of content, while the `@yield` directive is used to display the contents of a given section.

Now that we have defined a layout for our application, let's define a child page that inherits the layout.

<a name="extending-a-layout"></a>
#### Extending A Layout

When defining a child view, use the `@extends` Blade directive to specify which layout the child view should "inherit". Views which extend a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`:

```html
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

In this example, the `sidebar` section is utilizing the `@@parent` directive to append (rather than overwriting) content to the layout's sidebar. The `@@parent` directive will be replaced by the content of the layout when the view is rendered.

> {tip} Contrary to the previous example, this `sidebar` section ends with `@endsection` instead of `@show`. The `@endsection` directive will only define a section while `@show` will define and **immediately yield** the section.

The `@yield` directive also accepts a default value as its second parameter. This value will be rendered if the section being yielded is undefined:

    @yield('content', 'Default content')

<a name="forms"></a>
## Forms

<a name="csrf-field"></a>
### CSRF Field

Anytime you define an HTML form in your application, you should include a hidden CSRF token field in the form so that [the CSRF protection](/docs/{{version}}/csrf) middleware can validate the request. You may use the `@csrf` Blade directive to generate the token field:

```html
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### Method Field

Since HTML forms can't make `PUT`, `PATCH`, or `DELETE` requests, you will need to add a hidden `_method` field to spoof these HTTP verbs. The `@method` Blade directive can create this field for you:

```html
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### Validation Errors

The `@error` directive may be used to quickly check if [validation error messages](/docs/{{version}}/validation#quick-displaying-the-validation-errors) exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message:

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title" type="text" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

Since the `@error` directive compiles to an "if" statement, you may use the `@else` directive to render content when there is not an error for an attribute:

```html
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email" type="email" class="@error('email') is-invalid @else is-valid @enderror">
```

You may pass [the name of a specific error bag](/docs/{{version}}/validation#named-error-bags) as the second parameter to the `@error` directive to retrieve validation error messages on pages containing multiple forms:

```html
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email" type="email" class="@error('email', 'login') is-invalid @enderror">

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
## Stacks

Blade allows you to push to named stacks which can be rendered somewhere else in another view or layout. This can be particularly useful for specifying any JavaScript libraries required by your child views:

```html
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

You may push to a stack as many times as needed. To render the complete stack contents, pass the name of the stack to the `@stack` directive:

```html
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

If you would like to prepend content onto the beginning of a stack, you should use the `@prepend` directive:

```html
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
## Service Injection

The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/{{version}}/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class or interface name of the service you wish to resolve:

```html
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

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

<a name="custom-echo-handlers"></a>
### Custom Echo Handlers

If you attempt to "echo" an object using Blade, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library.

In these cases, Blade allows you to register a custom echo handler for that particular type of object. To accomplish this, you should invoke Blade's `stringable` method. The `stringable` method accepts a closure. This closure should type-hint the type of object that it is responsible for rendering. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class:

    use Illuminate\Support\Facades\Blade;
    use Money\Money;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::stringable(function (Money $money) {
            return $money->formatTo('en_GB');
        });
    }

Once your custom echo handler has been defined, you may simply echo the object in your Blade template:

```html
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### Custom If Statements

Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade provides a `Blade::if` method which allows you to quickly define custom conditional directives using closures. For example, let's define a custom conditional that checks the configured default "disk" for the application. We may do this in the `boot` method of our `AppServiceProvider`:

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::if('disk', function ($value) {
            return config('filesystems.default') === $value;
        });
    }

Once the custom conditional has been defined, you can use it within your templates:

```html
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```

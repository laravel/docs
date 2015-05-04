# Laravel Elixir

- [Introduction](#introduction)
- [Installation & Setup](#installation)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Scripts](#working-with-scripts)
- [Versioning / Cache Busting](#versioning-and-cache-busting)
- [Running PHP Test Suites](#running-php-test-suites)
- [Running Elixir](#running-elixir)
- [Calling Existing Gulp Tasks](#calling-existing-gulp-tasks)
- [Defining Custom Elixir Extensions](#defining-custom-elixir-extensions)

<a name="introduction"></a>
## Introduction

Laravel Elixir provides a clean, fluent API for defining basic [Gulp](http://gulpjs.com) tasks for your Laravel application. Elixir supports several common CSS and JavaScript pre-processors, and even testing tools.

If you've ever been confused about how to get started with Gulp and asset compilation, you will love Laravel Elixir. However, you are not required to use it while developing your application. You are free to use any asset pipeline tool you wish, or even none at all.

<a name="installation"></a>
## Installation & Setup

### Installing Node

Before triggering Elixir, you must first ensure that Node.js is installed on your machine.

    node -v

By default, Laravel Homestead includes everything you need; however, if you aren't using Vagrant, then you can easily install Node by visiting [their download page](http://nodejs.org/download/).

### Gulp

Next, you'll want to pull in [Gulp](http://gulpjs.com) as a global NPM package:

    npm install --global gulp

### Laravel Elixir

The only remaining step is to install Elixir! Within a fresh installation of Laravel, you'll find a `package.json` file in the root. Think of this like your `composer.json` file, except it defines Node dependencies instead of PHP. You may install the dependencies it references by running:

	npm install

<a name="working-with-stylesheets"></a>
## Working With Stylesheets

Now that you've installed Elixir, you'll be compiling and concatenating in no time! The `gulpfile.js` file in your project's root directory contains all of your Elixir tasks.

Elixir tasks can be chained together to define exactly how your assets should be compiled.

#### Compile Less

```javascript
elixir(function(mix) {
	mix.less("app.less");
});
```

In the example above, Elixir assumes that your Less files are stored in `resources/assets/less`. By default, this task will place the compiled CSS in `public/css/app.css`.

#### Compile Multiple Less Files

You may also combine multiple Less files into a single CSS file:

```javascript
elixir(function(mix) {
	mix.less([
		'app.less',
		'something-else.less'
	]);
});
```

#### Compile Sass

Of course, some developers prefer Sass to Less. With Elixir, compiling Sass is just as easy. Assuming your Sass files are stored at `resources/assets/sass`:

```javascript
elixir(function(mix) {
	mix.sass("app.sass");
});
```

Under the hood, Elixir uses the LibSass library for compilation. In some instances, it may be advantageous to leverage the Ruby version which, though slower, is more feature rich. Assuming that you have both Ruby and the Sass gem installed (`gem install sass`), you may enable Ruby-mode like so:

```javascript
elixir(function(mix) {
	mix.rubySass("app.sass");
});
```

#### Combine Plain Stylesheets

If you would just like to combine some plain CSS stylesheets into a single file, you may use the `styles` method. Paths passed to this method are relative to the `resources/assets/css` directory:

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	]);
});
```

Of course, you may also output the resulting file to a custom location:

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	], 'public/build/css/everything.css');
});
```

#### Combine All Stylesheets in a Directory

Instead of specifying each CSS file to combine, you may use the `stylesIn` method to specify that an entire directory should be combined into a single file:

```javascript
elixir(function(mix) {
	mix.stylesIn("public/css");
});
```

#### Source Maps

Source maps are enabled out of the box. As such, for each file that is compiled, you'll find a companion `*.css.map` file in the same directory. This mapping allows you to trace your compiled stylesheet selectors back to your original Sass or Less while debugging.

If you do not want source maps generated for your CSS, you may disable them using a simple configuration option:

```javascript
elixir.config.sourcemaps = false;

elixir(function(mix) {
	mix.sass("app.scss");
});
```

<a name="working-with-scripts"></a>
## Working With Scripts

#### Compile CoffeeScript

Assuming that your CoffeeScript files are stored in `resources/assets/coffee`:

```javascript
elixir(function(mix) {
	mix.coffee();
});
```

The compiled JavaScript, along with its companion source map, will be placed in `public/js/app.js`.

#### Compile Less and CoffeeScript

Of course, Elixir methods may be chained, allowing you to compile both Less and Coffeescript:

```javascript
elixir(function(mix) {
    mix.less("app.less")
       .coffee();
});
```

#### Combine Scripts

If you have multiple JavaScript files that you would like to combine into a single file, you may use the `scripts` method. Again, this assumes all paths are relative to the `resources/assets/js` directory:

```javascript
elixir(function(mix) {
	mix.scripts([
		"jquery.js",
		"app.js"
	]);
});
```

The resulting file will be placed in `public/js/all.js`.

#### Combine All Scripts In A Directory

Of course, you may also instruct Elixir to combine all of the scripts in a given directory:

```javascript
elixir(function(mix) {
	mix.scriptsIn("public/js/some/directory");
});
```

Again, the resulting file will be placed in `public/js/all.js`.

#### Combine Multiple Sets of Scripts

If you would like to combine multiple sets of scripts into different files, you may make multiple calls to the `scripts` method. The second argument given to the method will determine the resulting file name for each concatenation:

```javascript
elixir(function(mix) {
    mix.scripts(['jquery.js', 'main.js'], 'public/js/main.js')
       .scripts(['forum.js', 'threads.js'], 'public/js/forum.js');
});
```

#### Using Browserify

Want to require modules in the browser? Hoping to use EcmaScript 6 sooner than later? Need a built-in JSX transformer? If so, [Browserify](http://browserify.org/), along with the `browserify` Elixir task, will handle the job nicely.

This task assumes that your scripts are stored in `resources/assets/js`:

```javascript
elixir(function(mix) {
	mix.browserify('index.js');
});
```

The resulting file will be placed in `public/js/bundle.js`.

<a name="versioning-and-cache-busting"></a>
## Versioning / Cache Busting

Many developers suffix their compiled assets with a timestamp or unique token to force browsers to load the fresh assets instead of serving stale copies of the code. Elixir can handle this for you using the `version` method:

```javascript
elixir(function(mix) {
	mix.version("css/all.css");
});
```

This will append a unique hash to the filename, allowing for cache-busting. For example, the generated file name will look something like: `all-16d570a7.css`.

Then, within your [Laravel views](/docs/{{version}}/views), you may use the `elixir` function to load the appropriately hashed asset:

	<link rel="stylesheet" href="{{ elixir("css/all.css") }}">

The `elixir` function will automatically determine the name of the hashed file.

#### Versioning Multiple Files

You may also pass an array to the `version` method to version multiple files:

```javascript
elixir(function(mix) {
	mix.version(["css/all.css", "js/app.js"]);
});
```

	<link rel="stylesheet" href="{{ elixir("css/all.css") }}">

	<script src="{{ elixir("js/app.js") }}"></script>

<a name="running-php-test-suites"></a>
## Running PHP Test Suites

You may even instruct Elixir to run your PHP test suites using the `phpUnit` and `phpSpec` methods:

#### Trigger PHPUnit Tests

```javascript
elixir(function(mix) {
	mix.less("app.less")
	   .phpUnit();
});
```

#### Trigger PHPSpec Tests

```javascript
elixir(function(mix) {
	mix.less("app.less")
	   .phpSpec();
});
```

<a name="running-elixir"></a>
## Running Elixir

Now that you've told Elixir which tasks to execute, you may trigger Gulp from the command line.

> **Note:** All tasks will assume a development environment and will not run minification. For production, use `gulp --production`.

#### Execute All Registered Tasks Once

	gulp

#### Watch Assets For Changes

Since it is inconvenient to run the `gulp` command on your terminal after every change to your assets, you may use the `gulp watch` command. This command will continue running in your terminal and watch your assets for any changes. When changes occur, new files will automatically be compiled.

	gulp watch

#### Only Compile Scripts

	gulp scripts

#### Only Compile Styles

	gulp styles

#### Watch Tests And PHP Classes for Changes

If you are using Elixir to trigger your PHP test suite, you may use the `gulp tdd` command, which servers a similar purpose to `gulp watch`. The `tdd` command will monitor all of your PHP files for changes, and re-run your test suite when a change occurs.

	gulp tdd

<a name="calling-existing-gulp-tasks"></a>
## Calling Existing Gulp Tasks

Sometimes, you'll want to hook your own Gulp tasks into Elixir. As an example, imagine that you have a Gulp task that simply speaks a bit of text when called:

```javascript
gulp.task("speak", function() {
	var message = "Tea...Earl Grey...Hot";

	gulp.src("").pipe(shell("say " + message));
});
```

From the command line, you may, of course, call `gulp speak` to trigger the task. However, if you wish to call the task from Elixir, use the `mix.task` method:

```javascript
elixir(function(mix) {
    mix.task('speak');
});
```

Now, each time you run Gulp, your custom `speak` task will be run as well as any other Elixir tasks that you've mixed in.

#### Custom Watchers

To register a watcher, so that your custom tasks will be re-triggered each time one or more files are modified, you may pass a regular expression as the second argument to the `task` method:

```javascript
elixir(function(mix) {
    mix.task('speak', 'app/**/*.php');
});
```

By passing this second argument, we've instructed Elixir to re-trigger the "speak" task each time a PHP file in the "app/" directory is saved.

<a name="defining-custom-elixir-extensions"></a>
## Defining Custom Elixir Extensions

For even more flexibility, you can create full Elixir extensions, allowing you to pass arguments to your custom tasks. Using the previous "speak" example, you could write an extension like so:

```javascript
// In elixir-extensions.js...

var gulp = require("gulp");
var shell = require("gulp-shell");
var elixir = require("laravel-elixir");

elixir.extend("speak", function(message) {

	gulp.task("speak", function() {
		gulp.src("").pipe(shell("say " + message));
	});

	return this.queueTask("speak");

 });
```

Notice that we `extend` Elixir's API by passing the task name that we will reference within our Gulpfile, as well as a callback function that will create the Gulp task.

If you want your custom task to be monitored, you may register a watcher:

```javascript
this.registerWatcher("speak", "app/**/*.php");

return this.queueTask("speak");
```

In this example, when any file that matches the regular expression `app/**/*.php` is modified, the `speak` task will be triggered.

That's it! You may either place this at the top of your Gulpfile, or instead extract it to a custom tasks file. For example, if you place your extensions in `elixir-extensions.js`, you may require the file like so:

```javascript
var elixir = require("laravel-elixir");

require("./elixir-tasks")

elixir(function(mix) {
	mix.speak("Tea, Earl Grey, Hot");
});
```

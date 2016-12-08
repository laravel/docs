# Laravel Elixir

- [Introduction](#introduction)
- [Installation & Setup](#installation)
- [Usage](#usage)
- [Gulp](#gulp)
- [Extensions](#extensions)

<a name="introduction"></a>
## Introduction

Laravel Elixir provides a clean, fluent API for defining basic [Gulp](http://gulpjs.com) tasks for your Laravel application. Elixir supports several common CSS and JavaScript pre-processors, and even testing tools.

If you've ever been confused about how to get started with Gulp and asset compilation, you will love Laravel Elixir!

<a name="installation"></a>
## Installation & Setup

### Installing Node

Before triggering Elixir, you must first ensure that Node.js is installed on your machine.

    node -v

By default, Laravel Homestead includes everything you need; however, if you aren't using Vagrant, then you can easily install Node by visiting [their download page](http://nodejs.org/download/). Don't worry, it's quick and easy!

### Gulp

Next, you'll want to pull in [Gulp](http://gulpjs.com) as a global NPM package like so:

    npm install --global gulp

### Laravel Elixir

The only remaining step is to install Elixir! With a new install of Laravel, you'll find a `package.json` file in the root. Think of this like your `composer.json` file, except it defines Node dependencies instead of PHP. You may install the dependencies it references by running:

	npm install

<a name="usage"></a>
## Usage

Now that you've installed Elixir, you'll be compiling and concatenating in no time! The `gulpfile.js` file in your project's root directory contains all of your Elixir tasks.

#### Compile Less

```javascript
elixir(function(mix) {
	mix.less("app.less");
});
```

In the example above, Elixir assumes that your Less files are stored in `resources/assets/less`.

#### Compile Multiple Less Files

```javascript
elixir(function(mix) {
	mix.less([
		'app.less',
		'something-else.less'
	]);
});
```

#### Compile Sass

```javascript
elixir(function(mix) {
	mix.sass("app.scss");
});
```

This assumes that your Sass files are stored in `resources/assets/sass`.

By default, Elixir, underneath the hood, uses the LibSass library for compilation. In some instances, it might prove advantageous to instead leverage the Ruby version, which, though slower, is more feature rich. Assuming that you have both Ruby and the Sass gem installed (`gem install sass`), you may enable Ruby-mode, like so:

```javascript
elixir(function(mix) {
	mix.rubySass("app.sass");
});
```

#### Compile Without Source Maps

```javascript
elixir.config.sourcemaps = false;

elixir(function(mix) {
	mix.sass("app.scss");
});
```

Source maps are enabled out of the box. As such, for each file that is compiled, you'll find a companion `*.css.map` file in the same directory. This mapping allows you to, when debugging, trace your compiled stylesheet selectors  back to your original Sass or Less partials! Should you need to disable this functionality, however, the code sample above will do the trick.

#### Compile CoffeeScript

```javascript
elixir(function(mix) {
	mix.coffee();
});
```

This assumes that your CoffeeScript files are stored in `resources/assets/coffee`.

#### Compile All Less and CoffeeScript

```javascript
elixir(function(mix) {
    mix.less()
       .coffee();
});
```

#### Trigger PHPUnit Tests

```javascript
elixir(function(mix) {
	mix.phpUnit();
});
```

#### Trigger PHPSpec Tests

```javascript
elixir(function(mix) {
	mix.phpSpec();
});
```

#### Combine Stylesheets

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	]);
});
```

Paths passed to this method are relative to the `resources/assets/css` directory.

#### Combine Stylesheets and Save to a Custom Directory

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	], 'public/build/css/everything.css');
});
```

#### Combine Stylesheets From A Custom Base Directory

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	], 'public/build/css/everything.css', 'public/css');
});
```

The third argument to both the `styles` and `scripts` methods determines the relative directory for all paths passed to the methods.

#### Combine All Styles in a Directory

```javascript
elixir(function(mix) {
	mix.stylesIn("public/css");
});
```

#### Combine Scripts

```javascript
elixir(function(mix) {
	mix.scripts([
		"jquery.js",
		"app.js"
	]);
});
```

Again, this assumes all paths are relative to the `resources/assets/js` directory.

#### Combine All Scripts in a Directory

```javascript
elixir(function(mix) {
	mix.scriptsIn("public/js/some/directory");
});
```

#### Combine Multiple Sets of Scripts

```javascript
elixir(function(mix) {
    mix.scripts(['jquery.js', 'main.js'], 'public/js/main.js')
       .scripts(['forum.js', 'threads.js'], 'public/js/forum.js');
});
```

#### Version / Hash A File

```javascript
elixir(function(mix) {
	mix.version("css/all.css");
});
```

This will append a unique hash to the filename, allowing for cache-busting. For example, the generated file name will look something like: `all-16d570a7.css`.

Within your views, you may use the `elixir()` function to load the appropriately hashed asset. Here's an example:

    <link rel="stylesheet" href="{{ elixir("css/all.css") }}">

Behind the scenes, the `elixir()` function will determine the name of the hashed file that should be included. Don't you feel the weight lifting off your shoulders already?

You may also pass an array to the `version` method to version multiple files:

```javascript
elixir(function(mix) {
	mix.version(["css/all.css", "js/app.js"]);
});
```

    <link rel="stylesheet" href="{{ elixir("css/all.css") }}">
    <script src="{{ elixir("js/app.js") }}"></script>

#### Copy a File to a New Location

```javascript
elixir(function(mix) {
	mix.copy('vendor/foo/bar.css', 'public/css/bar.css');
});
```

#### Copy an Entire Directory to a New Location

```javascript
elixir(function(mix) {
	mix.copy('vendor/package/views', 'resources/views');
});
```

#### Trigger Browserify

```javascript
elixir(function(mix) {
	mix.browserify('index.js');
});
```

Want to require modules in the browser? Hoping to use EcmaScript 6 sooner than later? Need a built-in JSX transformer? If so, [Browserify](http://browserify.org/), along with the `browserify` Elixir task, will handle the job nicely.

This task assumes that your scripts are stored in `resources/assets/js`, though you're free to override the default.

#### Method Chaining

Of course, you may chain almost all of Elixir's methods together to build your recipe:

```javascript
elixir(function(mix) {
    mix.less("app.less")
       .coffee()
       .phpUnit()
       .version("css/bootstrap.css");
});
```

<a name="gulp"></a>
## Gulp

Now that you've told Elixir which tasks to execute, you only need to trigger Gulp from the command line.

#### Execute All Registered Tasks Once

	gulp

#### Watch Assets For Changes

	gulp watch

#### Only Compile Scripts

	gulp scripts

#### Only Compile Styles

	gulp styles

#### Watch Tests And PHP Classes for Changes

	gulp tdd

> **Note:** All tasks will assume a development environment, and will exclude minification. For production, use `gulp --production`.

<a name="extensions"></a>
## Custom Tasks and Extensions

Sometimes, you'll want to hook your own Gulp tasks into Elixir. Perhaps you have a special bit of functionality that you'd like Elixir to mix and watch for you. No problem!

As an example, imagine that you have a general task that simply speaks a bit of text when called.

```javascript
gulp.task("speak", function() {
	var message = "Tea...Earl Grey...Hot";

	gulp.src("").pipe(shell("say " + message));
});
```

Easy enough. From the command line, you may, of course, call `gulp speak` to trigger the task. To add it to Elixir, however, use the `mix.task()` method:

```javascript
elixir(function(mix) {
    mix.task('speak');
});
```

That's it! Now, each time you run Gulp, your custom "speak" task will be executed alongside any other Elixir tasks that you've mixed in. To additionally register a watcher, so that your custom tasks will be re-triggered each time one or more files are modified, you may pass a regular expression as the second argument.

```javascript
elixir(function(mix) {
    mix.task('speak', 'app/**/*.php');
});
```

By adding this second argument, we've instructed Elixir to re-trigger the "speak" task each time a PHP file in the "app/" directory is saved.


For even more flexibility, you can create full Elixir extensions. Using the previous "speak" example, you may write an extension, like so:

```javascript
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

Notice that we `extend` Elixir's API by passing the name that we will reference within our Gulpfile, as well as a callback function that will create the Gulp task.

As before, if you want your custom task to be monitored, then register a watcher.

```javascript
this.registerWatcher("speak", "app/**/*.php");
```

This lines designates that when any file that matches the regular expression, `app/**/*.php`, is modified, we want to trigger the `speak` task.

That's it! You may either place this at the top of your Gulpfile, or instead extract it to a custom tasks file. If you choose the latter approach, simply require it into your Gulpfile, like so:

```javascript
require("./custom-tasks")
```

You're done! Now, you can mix it in.

```javascript
elixir(function(mix) {
	mix.speak("Tea, Earl Grey, Hot");
});
```

With this addition, each time you trigger Gulp, Picard will request some tea.

# Laravel Quickstart

- [Installation](#installation)
- [Local Development Environment](#local-development-environment)
- [Routing](#routing)
- [Creating A View](#creating-a-view)
- [Creating A Migration](#creating-a-migration)
- [Eloquent ORM](#eloquent-orm)
- [Displaying Data](#displaying-data)
- [Next Steps](#next-steps)
- [Deploying Your Application](#deploying-your-application)

<a name="installation"></a>
## Installation

There's more than one way to install Laravel. Via installer, Composer or download.

### Via Laravel Installer

The Laravel Installer is a simple command-line tool used to build the Laravel environment on your system. It's helpful for creating multiple Laravel projects without heving to go to the web for files each time, and is faster than Composer. To use it on **Mac and Linux**,

1. Download the [Laravel installer](http://laravel.com/laravel.phar). 

2. Rename the file to `laravel` and move it to `/usr/local/bin`. 

3. Open Terminal and enter `laravel new`, followed by a directory, create a fresh Laravel installation. For instance, `laravel new blog` would create a directory named `blog` containing a fresh Laravel installation with all dependencies installed.

### Via Composer Create-Project

You may also install Laravel by issuing the Composer `create-project` command in your terminal:

	composer create-project laravel/laravel --prefer-dist

### Via Download

Laravel files can be downloaded manually, but you must still use Composer to get the dependencies (or manually get them yourself). This method also requires Git.

1. Make sure Composer is installed (see Install Composer above).

2. Download the [latest version](https://github.com/laravel/laravel/archive/master.zip) of Laravel and extract it to your project folder. 

3. In the root of your Laravel project, run `php composer install` (or `composer install`) to install all of the framework's dependencies.

4. If you want to update the Laravel framework, run `php composer update`

### Permissions

After installing Laravel, you may need to grant the web server write permissions to the `app/storage` directories. See the [Installation](/docs/installation) documentation for more details on configuration.

### Serving Laravel

Typically, you may use a web server such as Apache or Nginx to serve your Laravel applications. If you are on PHP 5.4+ and would like to use PHP's built-in development server, you may use the `serve` Artisan command:

	php artisan serve

<a name="directories"></a>
### Directory Structure

After instalatoin, take a look around to familiarize yourself with the directory structure. 

The `app` directory will contain most of your project and contains folders such as `views`, `controllers`, and `models`. You may also wish to explore the `app/config` directory and the [configuration](/docs/configuration) options.

<a name="local-development-environment"></a>
## Local Development Environment

Laravel provides the optional [Laravel Homestead](/docs/homestead) virtual machine, designed to take frustration out of managing servers and dependencies. Homestead uses [Vagrant](http://vagrantup.com) and is pre-packaged with all required software, taking seconds to deploy. It includes:

- Nginx
- PHP 5.5
- MySQL
- Redis
- Memcached
- Beanstalk

Both Homestead's dependencies, VirtualBox and Vagrant, include simple, graphical installers for all popular operating systems. Check out the [Homestead documentation](/docs/homestead) to get started.

<a name="routing"></a>
## Routing

Routing lets you define what happens when users visit a certain URL. In Laravel, the simplest route is a route to a Closure. Open the `app/routes.php` file and add the following route to the bottom of the file:

	Route::get('users', function()
	{
		return 'Users!';
	});

Visit `http://your-project.tld/users` in your web browser, replacing `your-project.tld` with your actual website/local URL, and you should see `Users!` displayed as the response.

In this document, we'll abbreviate routes like this to just `/users`.

Routes can also be attached to controller classes. For example:

	Route::get('users', 'UserController@getIndex');

This route informs the framework that requests to the `/users` route should call the `getIndex` method on the `UserController` class. For more information on controller routing, check out the [controller documentation](/docs/controllers).

<a name="creating-a-view"></a>
## Creating A View

A view is an output of data and where you'll put most of your "front-end" code, mostly HTML. We're going to create two new views in the `app/views` directory: `layout.blade.php` and `users.blade.php`. First, in your `layout` view, enter:

	<html>
		<body>
			<h1>Laravel Quickstart</h1>

			@yield('content')
		</body>
	</html>

Next, in your `users` view:

	@extends('layout')

	@section('content')
		Users!
	@stop

This uses Laravel's templating system: Blade. Blade provides template inheritance, as well as some syntax sugar on typical PHP control structures such as `if` and `for`. Check out the [Blade documentation](/docs/templates) for more details.

Now let's return it from our `/users` route. Instead of returning `Users!` from the route, return the view instead:

	Route::get('users', function()
	{
		return View::make('users');
	});

Now you have setup a simple view that extends a layout. Next, let's start working on our database layer.

<a name="creating-a-migration"></a>
## Creating A Migration

To create a table to hold our data, we'll use the Laravel migration system. Migrations let you expressively define modifications to your database, and easily share them with the rest of your team.

First, let's configure a database connection. You may configure all of your database connections from the `app/config/database.php` file. By default, Laravel is configured to use MySQL, and you will need to supply connection credentials within the database configuration file. If you wish, you may change the `driver` option to `sqlite` and it will use the SQLite database included in the `app/database` directory.

Next, to create the migration, we'll use the [Artisan CLI](/docs/artisan). From the root of your project, run the following from your terminal:

	php artisan migrate:make create_users_table

Next, find the generated migration file in the `app/database/migrations` folder. This file contains a class with two methods: `up` and `down`. In the `up` method, you should make the desired changes to your database tables, and in the `down` method you simply reverse them.

Let's define a migration that looks like this:

	public function up()
	{
		Schema::create('users', function($table)
		{
			$table->increments('id');
			$table->string('email')->unique();
			$table->string('name');
			$table->timestamps();
		});
	}

	public function down()
	{
		Schema::drop('users');
	}

Next, we can run our migrations from our terminal using the `migrate` command. Simply execute this command from the root of your project:

	php artisan migrate

If you wish to rollback a migration, you may issue the `migrate:rollback` command. Now that we have a database table, let's start pulling some data!

<a name="eloquent-orm"></a>
## Eloquent ORM

Laravel comes with a superb ORM: Eloquent, which is similar to the Ruby on Rails ORM, ActiveRecord.

An Eloquent model can be used to query an associated database table, as well as represent a given row within that table. Models are typically stored in the `app/models` directory. You define a `User.php` model like so:

	class User extends Eloquent {}

We do not have to tell Eloquent which table to use. Eloquent will automaiclay use the plural form of the model name as the table. 

Using your preferred database administration tool, insert a few rows into your `users` table, and use Eloquent to retrieve them and pass them to our view.

Now modify your `/users` route to look like this:

	Route::get('users', function()
	{
		$users = User::all();

		return View::make('users')->with('users', $users);
	});

Here, the `all` method on the `User` model will retrieve all of the rows in the `users` table. Next, it passes these records to the view via the `with` method, which accepts a key and value. The next section tells how to use the data in a view. 

<a name="displaying-data"></a>
## Displaying Data

Now that `users` are available to our view, we can display them:

	@extends('layout')

	@section('content')
		@foreach($users as $user)
			<p>{{ $user->name }}</p>
		@endforeach
	@stop

There are no `echo` statements. With Blade, you may echo data by putting it in double curly braces. Navigate to the `/users` route in your web browser and see the names of your users displayed.

<a name="next-steps"></a>

This tutorial showed the basics of Laveral, but there's much more.

See [Configuration](/docs/configuration) for important information on settgin up Laravel.


Keep reading the documentation to dig deeper into [Eloquent](/docs/eloquent) and [Blade](/docs/templates). There's also [Queues](/docs/queues), [Unit Testing](/docs/testing) and [IoC Containers](/docs/ioc).



<a name="deploying-your-application"></a>
## Deploying Your Application

[Laravel Forge](https://forge.laravel.com) provides a simple way to deploy your Laravel applications onto blazing fast servers. Forge can configure and provision servers on DigitalOcean, Linode, Rackspace, and Amazon EC2. Like Homestead, all of the latest are included: Nginx, PHP 5.5, MySQL, Postgres, Redis, Memcached, and more. Forge "Quick Deploy" can even deploy your code for you each time you push changes out to Github or Bitbucket!

On top of that, Forge can help you configure queue workers, SSL, Cron jobs, sub-domains, and more. For more information, visit the [Forge website](https://forge.laravel.com).

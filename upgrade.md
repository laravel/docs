# Upgrade Guide

- [Upgrading To 5.0 From 4.2](#upgrade-5.0)
- [Upgrading To 4.2 From 4.1](#upgrade-4.2)
- [Upgrading To 4.1.29 From <= 4.1.x](#upgrade-4.1.29)
- [Upgrading To 4.1.26 From <= 4.1.25](#upgrade-4.1.26)
- [Upgrading To 4.1 From 4.0](#upgrade-4.1)

<a name="upgrade-5.0"></a>
## Upgrading To 5.0 From 4.2

### Fresh Install, Then Migrate

The recommended method of upgrading is to create a new Laravel `5.0` install and then to copy your `4.2` site's unique application files--controllers, routes, commands, assets, and domain code--into it.

To start, [install a new Laravel 5 application](/docs/master/installation) into a fresh directory in your local environment.

The remaining steps are to find all of the application-specific code from your `4.2` site and move it to your `5.0` site.

### PSR-4 namespace

If you already have a top-level PSR-0/4 namespace set up, or if you intend to set one up, use `artisan app:name` to set an [application namespace](/docs/master/structure#namespacing-your-application):

```bash
php artisan app:name SocialNet
```

> **Note**: This upgrade guide will reference the `App` namespace in any directions; if you've already set `app:name`, replace `App` in the examples with your own app's namespace instead.

Laravel 5's `app:name` namespacing presumes that the top level of your application's domain code will be the `app` folder. So, if you had a folder in your `4.2` application that was mapped to your PSR-0/4 namespace (e.g. an `app/SocialNet` folder that was mapped to the `SocialNet` namespace), move all of its folders and files to the `app` folder.

### Composer dependencies

Copy your `4.2` app's `composer.json` dependencies into the `5.0` app's composer.json (or require them one-by-one with `composer require`).

Now, run `composer update`.

### Artisan Commands

Move all of your command classes from `4.2`'s `app/commands` directory to `5.0`'s `app/Console/Commands`.

Either [namespace your commands](#namespace-artisan-commands), or add the `app/Console/Commands` directory to the `composer.json` classmap autoloader.

Copy your list of artisan commands from `start/artisan.php` into `app/Console/Kernel.php`'s `$commands` array.

### Controllers

Move all of your controller classes from `4.2`'s' `app/controllers` directory to `5.0`'s `app/Http/Controllers`.

Either [namespace your controllers](#namespace-controllers) or remove the namespace from the abstract `app/Http/Controllers/Controller.php`, add the `app/Http/Controllers` directory to the `composer.json` classmap autoloader, and update `app/Providers/RouteServiceProvider.php`'s `$namespace` property to `null`.

### Database Migrations & Seeds

Move all of your migration classes from `4.2`'s `app/database/migrations` directory to `5.0`'s `database/migrations` and all of your seed classes from `app/database/seeds` to `database/seeds`.

Delete the `2014_10_12_00000_create_users_table` migration, since you should already have the users table in your database.

### Filters

Copy your filter bindings from `app/filters.php` and place them into the `boot()` method of `app/Providers/RouteServiceProvider.php`. Add `use Illuminate\Support\Facades\Route;` in `app/Providers/RouteServiceProvider.php` in order to continue using the `Route` Facade.

You don't need to move over any of the filters that come in by default; they're all here, but now as Middleware. Edit any routes in `routes.php` that call the native Laravel filters (e.g. `['before' => 'auth']`) and change them to reference them as middleware (e.g. `['middleware' => 'auth'].`) You can still bind your own custom filters using `before` and `after`.

### Language files

Move your language files from `4.2`'s `app/lang` directory to `5.0`'s `resources/lang`.

### Models

If your `4.2` application relies on the `app/models` folder for autoloading, create an `app/models` directory in the `5.0` install and add it to `composer.json`'s classmap autoloader.

Note that the `User.php` that comes with Laravel 5 lives in the `app` directory, which means it's namespaced `app\User`.

Update any models using the `SoftDeletingTrait` to use `SoftDeletes`.

### Routes

Move `app/routes.php` to `app/Http/routes.php`.

### Global bindings

If you have any bindings in `start/global.php`, start by moving them all to the `register()` method of `App\Providers\AppServiceProvider`. However, the best practice is to perform bindings in Service Providers specific to the context that is being bound for.

### Tests

Move your tests from `4.2`'s `app/tests` directory to `5.0`'s `tests`.

### Views

Move your views from `4.2`'s `app/views` directory to `5.0`'s `resources/views`.

### Namespacing controllers and commands

<a name="namespace-controllers"></a>
#### Namespacing controllers

If your controllers weren't namespaced in your `4.2` codebase, you can either bring them in with no namespace, or add namespaces to them.

If you want to add namespaces, edit each controller and add `App\Http\Controllers` as its namespace.

If you want to go without, edit `app/Providers/RouteServiceProvider.php` and set its `$namespace` property equal to `null`. Then edit the `map()` method in that same file to be *just* this line (replace the entire `$this->loadRoutesFrom` line):

```php
    include app_path('Http/routes.php');
```

Finally, add the controllers directory to `composer.json`'s classmap autoloader. 

> **Note**: If you namespace your controllers, **all of your internal facade calls will fail**; facades are imported at the top of the namespace. If you see something like `Class 'App\Http\Controllers\Auth' not found.`, you need to either `use Auth`, `use Session`, etc. at the top of the controller, or prepend `\` to each inline facade use (e.g. convert `Session::flash('stuff', 'other stuff');` to `\Session::flash('stuff', 'other stuff');`.)

<a name="namespace-artisan-commands"></a>
#### Namespacing Artisan commands

Just like controllers, you can either namespace all of your imported commands so they're autoloaded by PSR-4, or you can add the `app/Console/Commands` directory to `composer.json`'s classmap autoloader.

### Configuration

### Migrating environment-specific files

Copy the new `5.0` `.env.example` file `.env`, which is the `5.0` equivalent of `.env.php`. Set any appropriate values there, like your `APP_ENV` (the environment name--for example, "local" or "production"), `APP_KEY` (your encryption key), your database credentials, and your cache and session drivers.

Additionally, copy any custom values you had in your `4.2`'s `.env.php` file and place them in both `.env` (the real value) and `.env.example` (a sample instructional value).

### Config files

Laravel 5.0 no longer uses `app/config/environmentName/` directories to provide specific configuration files for the given environment. Instead, move any configuration values that vary by environment into `.env`, and then access them in your configuration files using `env('keyNameHere', 'default fallback value here')`.

Set the config files in the `config/` directory to represent either the values that are consistent across all of your environments, or set them to use `env()` to load varying values. If you add more keys to `.env` to account for this, remember to add them to `.env.example` as well.

### Auth & Users

Either delete your old `Auth` model and just use the new one (the easiest option), or follow these instructions:

**Delete the following from your `use` block:**
```php
use Illuminate\Auth\UserInterface;
use Illuminate\Auth\Reminders\RemindableInterface;
```

**Add the following to your `use` block:**
```php
use Illuminate\Auth\Authenticatable;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;
```

**Remove the UserInterface and RemindableInterface interfaces**

**Mark it as implementing the following interfaces:**
```php
implements AuthenticatableContract, CanResetPasswordContract
```

**Include the following *within the class declaration, to use them as traits*:**
```php
use Authenticatable, CanResetPassword;
```

Either change the namespace of your `User` model to  your app namespace, or change the `"model"` property in `config/auth.php` to the correct namespace (e.g. `User` instead of `SocialNet\User`).

Finally, if you're using your own User model, you can delete `app/user.php`.

### Bootstrap directory

If you’ve made any customizations to files in the `bootstrap` directory—and if you made any, it was likely only `start.php`—you’ll want to move them over. Note that `detectEnvironment` behaves differently in Laravel 5--an application's current environment string is now entirely defined by the `APP_ENV` value of the `.env` file.

### Public directory

Copy your `4.2` application's public assets from the `4.2` `public` directory to the `5.0` `public` directory. Be sure to keep the `5.0` version of `index.php`.

### Loose files

Copy in any loose files in your project--for example, `.scrutinizer.yml` or `bower.json` in the top level, or your Sass or Less directories, or anything else--into your new application at the appropriate location.

### Form & HTML Helpers

If you're using Form or Html helpers, you'll see an error stating `class 'Form' not found` or `class 'Html' not found`. To fix this, `composer require` `"illuminate/html": "~5.0"`.

You'll also need to get the Form and Html Facades and Service Srovider working. Edit `config/app.php`, and add this line to the 'providers' array:

```php
    'Illuminate\Html\HtmlServiceProvider',
```

And add these lines to the 'aliases' array:

```php
        'Form'      => 'Illuminate\Html\FormFacade',
        'Html'      => 'Illuminate\Html\HtmlFacade',
```

### Change Blade tags

The best way to handle the changes to Blade's tags is to search through anywhere in your site you *know* you need to allow HTML (for example, if you're using HTML or Form helpers) and replace `{{` with `{!!` and `}}` with `!!}`. Otherwise, allow Laravel to auto-escape all of your output by default.

However, if for some reason you *need* to use the old Blade syntax, you can define that. Just add the following lines at the bottom of `AppServiceProvider@register()`:

```php
		\Blade::setRawTags('{{', '}}');
		\Blade::setContentTags('{{{', '}}}');
		\Blade::setEscapedContentTags('{{{', '}}}');
```

Note that if you change the raw tags this way, your comments with `{{--` will no longer work.

### Beanstalk Queuing

Laravel 5.0 now requires `"pda/pheanstalk": "~3.0"` instead of `"pda/pheanstalk": "~2.1"` that Laravel 4.2 required.

### Global CSRF

By default, [CSRF protection](/docs/routing#csrf-protection) is enabled on all routes. If you'd like to disable this, or only manually enable it on certain routes, remove this line from `App\Http\Kernel`'s `$middleware` array:

```php
		'Illuminate\Foundation\Http\Middleware\VerifyCsrfToken',
```

If you want to use it elsewhere, add this line to `$routeMiddleware`:

```php
	'csrf' => 'Illuminate\Foundation\Http\Middleware\VerifyCsrfToken',
```

Now you can [add this to any route](/docs/master/middleware#registering-middleware) using `['middleware' => 'csrf']` on the route.

### CacheManager

If your application code was injecting `Illuminate\Cache\CacheManager` to get a non-facade version of Laravel's cache, change it to inject `Illuminate\Cache\Repository`.

### Eloquent caching through `remember()` no longer available

Eloquent no longer provides the `remember()` method for caching queries. You now are responsible for caching your queries manually.

### Pagination

Replace any calls to `$paginator->links()` with `$paginator->render()`.

### Remote

The Remote component has been deprecated.

### Workbench

The Workbench component has been deprecated.

<a name="upgrade-4.2"></a>
## Upgrading To 4.2 From 4.1

### PHP 5.4+

Laravel 4.2 requires PHP 5.4.0 or greater.

### Encryption Defaults

Add a new `cipher` option in your `app/config/app.php` configuration file. The value of this option should be `MCRYPT_RIJNDAEL_256`.

	'cipher' => MCRYPT_RIJNDAEL_256

This setting may be used to control the default cipher used by the Laravel encryption facilities.

> **Note:** In Laravel 4.2, the default cipher is `MCRYPT_RIJNDAEL_128` (AES), which is considered to be the most secure cipher. Changing the cipher back to `MCRYPT_RIJNDAEL_256` is required to decrypt cookies/values that were encrypted in Laravel <= 4.1

### Soft Deleting Models Now Use Traits

If you are using soft deleting models, the `softDeletes` property has been removed. You must now use the `SoftDeletingTrait` like so:

	use Illuminate\Database\Eloquent\SoftDeletingTrait;

	class User extends Eloquent {
		use SoftDeletingTrait;
	}

You must also manually add the `deleted_at` column to your `dates` property:

	class User extends Eloquent {
		use SoftDeletingTrait;

		protected $dates = ['deleted_at'];
	}

The API for all soft delete operations remains the same.

> **Note:** The `SoftDeletingTrait` can not be applied on a base model. It must be used on an actual model class.

### View / Pagination Environment Renamed

If you are directly referencing the `Illuminate\View\Environment` class or `Illuminate\Pagination\Environment` class, update your code to reference `Illuminate\View\Factory` and `Illuminate\Pagination\Factory` instead. These two classes have been renamed to better reflect their function.

### Additional Parameter On Pagination Presenter

If you are extending the `Illuminate\Pagination\Presenter` class, the abstract method `getPageLinkWrapper` signature has changed to add the `rel` argument:

	abstract public function getPageLinkWrapper($url, $page, $rel = null);

### Iron.Io Queue Encryption

If you are using the Iron.io queue driver, you will need to add a new `encrypt` option to your queue configuration file:

    'encrypt' => true

<a name="upgrade-4.1.29"></a>
## Upgrading To 4.1.29 From <= 4.1.x

Laravel 4.1.29 improves the column quoting for all database drivers. This protects your application from some mass assignment vulnerabilities when **not** using the `fillable` property on models. If you are using the `fillable` property on your models to protect against mass assignment, your application is not vulnerable. However, if you are using `guarded` and are passing a user controlled array into an "update" or "save" type function, you should upgrade to `4.1.29` immediately as your application may be at risk of mass assignment.

To upgrade to Laravel 4.1.29, simply `composer update`. No breaking changes are introduced in this release.

<a name="upgrade-4.1.26"></a>
## Upgrading To 4.1.26 From <= 4.1.25

Laravel 4.1.26 introduces security improvements for "remember me" cookies. Before this update, if a remember cookie was hijacked by another malicious user, the cookie would remain valid for a long period of time, even after the true owner of the account reset their password, logged out, etc.

This change requires the addition of a new `remember_token` column to your `users` (or equivalent) database table. After this change, a fresh token will be assigned to the user each time they login to your application. The token will also be refreshed when the user logs out of the application. The implications of this change are: if a "remember me" cookie is hijacked, simply logging out of the application will invalidate the cookie.

### Upgrade Path

First, add a new, nullable `remember_token` of VARCHAR(100), TEXT, or equivalent to your `users` table.

Next, if you are using the Eloquent authentication driver, update your `User` class with the following three methods:

	public function getRememberToken()
	{
		return $this->remember_token;
	}

	public function setRememberToken($value)
	{
		$this->remember_token = $value;
	}

	public function getRememberTokenName()
	{
		return 'remember_token';
	}

> **Note:** All existing "remember me" sessions will be invalidated by this change, so all users will be forced to re-authenticate with your application.

### Package Maintainers

Two new methods were added to the `Illuminate\Auth\UserProviderInterface` interface. Sample implementations may be found in the default drivers:

	public function retrieveByToken($identifier, $token);

	public function updateRememberToken(UserInterface $user, $token);

The `Illuminate\Auth\UserInterface` also received the three new methods described in the "Upgrade Path".

<a name="upgrade-4.1"></a>
## Upgrading To 4.1 From 4.0

### Upgrading Your Composer Dependency

To upgrade your application to Laravel 4.1, change your `laravel/framework` version to `4.1.*` in your `composer.json` file.

### Replacing Files

Replace your `public/index.php` file with [this fresh copy from the repository](https://github.com/laravel/laravel/blob/master/public/index.php).

Replace your `artisan` file with [this fresh copy from the repository](https://github.com/laravel/laravel/blob/master/artisan).

### Adding Configuration Files & Options

Update your `aliases` and `providers` arrays in your `app/config/app.php` configuration file. The updated values for these arrays can be found [in this file](https://github.com/laravel/laravel/blob/master/app/config/app.php). Be sure to add your custom and package service providers / aliases back to the arrays.

Add the new `app/config/remote.php` file [from the repository](https://github.com/laravel/laravel/blob/master/app/config/remote.php).

Add the new `expire_on_close` configuration option to your `app/config/session.php` file. The default value should be `false`.

Add the new `failed` configuration section to your `app/config/queue.php` file. Here are the default values for the section:

	'failed' => array(
		'database' => 'mysql', 'table' => 'failed_jobs',
	),

**(Optional)** Update the `pagination` configuration option in your `app/config/view.php` file to `pagination::slider-3`.

### Controller Updates

If `app/controllers/BaseController.php` has a `use` statement at the top, change `use Illuminate\Routing\Controllers\Controller;` to `use Illuminate\Routing\Controller;`.

### Password Reminders Updates

Password reminders have been overhauled for greater flexibility. You may examine the new stub controller by running the `php artisan auth:reminders-controller` Artisan command. You may also browse the [updated documentation](/docs/security#password-reminders-and-reset) and update your application accordingly.

Update your `app/lang/en/reminders.php` language file to match [this updated file](https://github.com/laravel/laravel/blob/master/app/lang/en/reminders.php).

### Environment Detection Updates

For security reasons, URL domains may no longer be used to detect your application environment. These values are easily spoofable and allow attackers to modify the environment for a request. You should convert your environment detection to use machine host names (`hostname` command on Mac, Linux, and Windows).

### Simpler Log Files

Laravel now generates a single log file: `app/storage/logs/laravel.log`. However, you may still configure this behavior in your `app/start/global.php` file.

### Removing Redirect Trailing Slash

In your `bootstrap/start.php` file, remove the call to `$app->redirectIfTrailingSlash()`. This method is no longer needed as this functionality is now handled by the `.htaccess` file included with the framework.

Next, replace your Apache `.htaccess` file with [this new one](https://github.com/laravel/laravel/blob/master/public/.htaccess) that handles trailing slashes.

### Current Route Access

The current route is now accessed via `Route::current()` instead of `Route::getCurrentRoute()`.

### Composer Update

Once you have completed the changes above, you can run the `composer update` function to update your core application files! If you receive class load errors, try running the `update` command with the `--no-scripts` option enabled like so: `composer update --no-scripts`.

### Wildcard Event Listeners

The wildcard event listeners no longer append the event to your handler functions parameters. If you require finding the event that was fired you should use `Event::firing()`.

# Guia de Atualização

- [Atualizando para 5.1.0](#upgrade-5.1.0)
- [Atualizando para 5.0.16](#upgrade-5.0.16)
- [Atualizando para 5.0 From 4.2](#upgrade-5.0)
- [Atualizando para 4.2 From 4.1](#upgrade-4.2)
- [Atualizando para 4.1.29 From <= 4.1.x](#upgrade-4.1.29)
- [Atualizando para 4.1.26 From <= 4.1.25](#upgrade-4.1.26)
- [Atualizando para 4.1 From 4.0](#upgrade-4.1)

<a name="upgrade-5.1.0"></a>
## Atualizando para 5.1.0

#### Tempo Estimado: Menos de 1 Hora

### Atualize o `bootstrap/autoload.php`

Atualize a variável `$compiledPath` em `bootstrap/autoload.php` para o seguinte:

	$compiledPath = __DIR__.'/cache/compiled.php';

### Crie o Diretório `bootstrap/cache`

Dentro do seu diretório `bootstrap` crie o diretório `cache` (`bootstrap/cache`) e adicione o arquivo `.gitignore` nesse diretório com o seguinte conteúdo:

	*
	!.gitignore

Esse diretório deve ter permissão de escrita, e será usado para guardar os arquivos de otimização temporários do framework como `compiled.php`, `routes.php`, `config.php`, e `services.json`.

### Autenticação

Se você está usando o controller `AuthController` que usa a trait `AuthenticatesAndRegistersUsers`, você precisará fazer algumas mudanças em como usuários são validados e criados.

Primeiro, você não precisa mais passar as intâncias de `Guard` e `Registrar` para o construtor. Você pode remover essas dependencias inteiramente do construtor do seu controller.

Segundo, a classe `App\Services\Registrar` usada no Laravel 5.0 não é mais necessária. Você pode simplesmente copiar e colar os métodos `validator` e `create` dessa classe para o controller `AuthController`. Nenhuma mudança precisa ser feita para esses métodos; Entetanto, você pode se certificar de importar o facade `Validator` e o model `User` no topo do arquivo `AuthController`.

#### Password Controller

O controller `PasswordController` não necessita mais de nenhuma dependência em seu construtor. Você pode remover as dependências que foram requeridas no 5.0.

### Validação

Se você está sobrescrevendo o método `formatValidationErrors` no seu controller base, você deve agora indicar o tipo do contrato `Illuminate\Contracts\Validation\Validator` ao invés de uma instância concreta de `Illuminate\Validation\Validator`.

Da mesma forma, se você está sobrescrevendo o método `formatErrors` na sua classe base de Form Request, você deve agora indicar o tipo do contrato `Illuminate\Contracts\Validation\Validator` ao invés de uma instância concreta de `Illuminate\Validation\Validator`.

### Eloquent

#### O Método `create`

O método `create` do eloquent agora pode ser chamado sem parâmetros. Se você está sobrescrevendo esse método em seus próprios models, configure o valor padrão do parâmetro `$attributes` para um array:

	public static function create(array $attributes = [])
	{
		// Your custom implementation
	}

#### O Método `find`

Se você está sobrescrevendo o método `find` em seus próprios models e chamando `parent::find()` dentro do seu método, você deve agora alterá-lo para chamar o método `find` do Eloquent Query Builder:

	public static function find($id, $columns = ['*'])
	{
		$model = static::query()->find($id, $columns);

		// ...

		return $model;
	}

#### Formatando Datas

Anteriormente, o formato das suas datas para os campos Eloquent poderia ser modificado sobrescrevendo o método `getDateFormat` no seu model. Isso ainda é possível; entretanto, para maior conveniencia você pode simplesmente especificar a propriedade `$dateFormat` no model ao invés de sobrescrever o método.

O formato da data agora também é aplicado quando serializa o model para um `array` ou JSON. Isso pode alterar o formato dos campos de data do JSON serializado quando você migrar do Laravel 5.0 para 5.1. Para configurar um formato específico de data para models serializados, você pode sobrescrever o método `serializeDate(DateTime $date)` do seu model. Esse método permite a você controlar o formato da data serializada do Eloquent sem alterar o formato armazenado.

### A Classe Collection

#### O Método `sortBy`:

O método `sortBy` agora retorna uma nova instância de `Collection` ao invés de modificar a collection existente:

	$collection = $collection->sortBy('name');

#### O Método `groupBy`

O método `groupBy` agora retorna uma instância de `Collection` para cada item na `Collection` pai. Se você gostaria de conveter todos os itens de volta para um array, você pode usar o método `map`:

	$collection->groupBy('type')->map(function($item)
	{
		return $item->all();
	});

#### O Método `lists`

O método `lists` agora retorna uma instância de `Collection` para Eloquent Querys. Se você gostaria de converter a `Collection` em um array, use o método  `all`:

	$collection->lists('id')->all();

### Commandos & Handlers

O diretório `app/Commands` foi renomeado para `app/Jobs`. Entretanto, você não é obrigado a mover todos os seus comandos para o novo local, você pode continuar usando os comandos Artisan `make:command` e `handler:command` para gerar suas classes.

Da mesma forma, o diretório `app/Handlers` foi renomeado para `app/Listeners` e agora só contém Event Listeners. Entretanto, você não é obrigado a mover ou renomear seus comandos e Event Handlers existentes, e você ainda pode continar a usar o comando Artisan `handler:event` para gerar Event Handlers.

Para manter compatibilidade com sua aplicação Laravel 5.0, você pode atualizar sua aplicação para o Laravel 5.1 e aos poucos ir atualizando seus eventos e comandos para suas novas localizações quando for conveniente para você ou sua equipe.

### Testes

Adicione a propriedade protegida `$baseUrl` para o arquivo `tests/TestCase.php`

	protected $baseUrl = 'http://localhost';

### Amazon Web Services SDK

Se você está usando os drivers AWS SQS Queue ou o AWS SES E-mail, você pode atualizar sua instalação do AWS PHP SDK para a versão 3.0.

Se você está usando o driver Amazon S3 Filesystem, você precisará atualizar o pacote correspondente ao Flysystem via Composer:

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`

### Depreciações

As seguintes características do Laravel estão depreciadas e serão removidas completamente com a versão do Laravel 5.2 em Dezembro de 2015:

<div class="content-list" markdown="1">
- Route filters estão depreciados por casoa dos [middlewares](/docs/{{version}}/middleware).
- O contrato `Illuminate\Contracts\Routing\Middleware` está depreciado. Nenhum contrato é obrigatório no seu middleware. Em adição, o contrato `TerminableMiddleware` também está depreciado. Ao invés de implementar essa interface, você simplesmente pode definir o método `terminate` no seu middleware.
- O contrato `Illuminate\Contracts\Queue\ShouldBeQueued` está depreciado em favor de `Illuminate\Contracts\Queue\ShouldQueue`.
- Iron.io "push queues" está depreciado em favor das típicas filas Iron.io e [queue listeners](/docs/{{version}}/queues#running-the-queue-listener).
- A trait `Illuminate\Foundation\Bus\DispatchesCommands`  está depreciada e foi renomeada para `Illuminate\Foundation\Bus\DispatchesJobs`.
- `Illuminate\Container\BindingResolutionException` está depreciado e foi movido para `Illuminate\Contracts\Container\BindingResolutionException`.
- O método do Service Container `bindShared` está depreciado em favor do método `singleton`.
- O método `pluck` do Eloquent e Query Builder estão depreciados e foram renomeados para `value`.
- O método `fetch` da instância de `Collection` está depreciado em favor do método `pluck`.
- A função utilitária `array_fetch` está depreciado em favor do utilitário `array_pluck`.
</div>

<a name="upgrade-5.0.16"></a>
## Upgrading To 5.0.16

In your `bootstrap/autoload.php` file, update the `$compiledPath` variable to:

	$compiledPath = __DIR__.'/../vendor/compiled.php';

<a name="upgrade-5.0"></a>
## Upgrading To 5.0 From 4.2

### Fresh Install, Then Migrate

The recommended method of upgrading is to create a new Laravel `5.0` install and then to copy your `4.2` site's unique application files into the new application. This would include controllers, routes, Eloquent models, Artisan commands, assets, and other code specific to your application.

To start, [install a new Laravel 5 application](/docs/{{version}}/installation) into a fresh directory in your local environment. We'll discuss each piece of the migration process in further detail below.

### Composer Dependencies & Packages

Don't forget to copy any additional Composer dependencies into your 5.0 application. This includes third-party code such as SDKs.

Some Laravel-specific packages may not be compatible with Laravel 5 on initial release. Check with your package's maintainer to determine the proper version of the package for Laravel 5. Once you have added any additional Composer dependencies your application needs, run `composer update`.

### Namespacing

By default, Laravel 4 applications did not utilize namespacing within your application code. So, for example, all Eloquent models and controllers simply lived in the "global" namespace. For a quicker migration, you can simply leave these classes in the global namespace in Laravel 5 as well.

### Configuration

#### Migrating Environment Variables

Copy the new `.env.example` file to `.env`, which is the `5.0` equivalent of the old `.env.php` file. Set any appropriate values there, like your `APP_ENV` and `APP_KEY` (your encryption key), your database credentials, and your cache and session drivers.

Additionally, copy any custom values you had in your old `.env.php` file and place them in both `.env` (the real value for your local environment) and `.env.example` (a sample instructional value for other team members).

For more information on environment configuration, view the [full documentation](/docs/{{version}}/installation#environment-configuration).

> **Note:** You will need to place the appropriate `.env` file and values on your production server before deploying your Laravel 5 application.

#### Configuration Files

Laravel 5.0 no longer uses `app/config/{environmentName}/` directories to provide specific configuration files for a given environment. Instead, move any configuration values that vary by environment into `.env`, and then access them in your configuration files using `env('key', 'default value')`. You will see examples of this in the `config/database.php` configuration file.

Set the config files in the `config/` directory to represent either the values that are consistent across all of your environments, or set them to use `env()` to load values that vary by environment.

Remember, if you add more keys to `.env` file, add sample values to the `.env.example` file as well. This will help your other team members create their own `.env` files.

### Routes

Copy and paste your old `routes.php` file into your new `app/Http/routes.php`.

### Controllers

Next, move all of your controllers into the `app/Http/Controllers` directory. Since we are not going to migrate to full namespacing in this guide, add the `app/Http/Controllers` directory to the `classmap` directive of your `composer.json` file. Next, you can remove the namespace from the abstract `app/Http/Controllers/Controller.php` base class. Verify that your migrated controllers are extending this base class.

In your `app/Providers/RouteServiceProvider.php` file, set the `namespace` property to `null`.

### Route Filters

Copy your filter bindings from `app/filters.php` and place them into the `boot()` method of `app/Providers/RouteServiceProvider.php`. Add `use Illuminate\Support\Facades\Route;` in the `app/Providers/RouteServiceProvider.php` in order to continue using the `Route` Facade.

You do not need to move over any of the default Laravel 4.0 filters such as `auth` and `csrf`; they're all here, but as middleware. Edit any routes or controllers that reference the old default filters (e.g. `['before' => 'auth']`) and change them to reference the new middleware (e.g. `['middleware' => 'auth'].`)

Filters are not removed in Laravel 5. You can still bind and use your own custom filters using `before` and `after`.

### Global CSRF

By default, [CSRF protection](/docs/{{version}}/routing#csrf-protection) is enabled on all routes. If you'd like to disable this, or only manually enable it on certain routes, remove this line from `App\Http\Kernel`'s `middleware` array:

	'App\Http\Middleware\VerifyCsrfToken',

If you want to use it elsewhere, add this line to `$routeMiddleware`:

	'csrf' => 'App\Http\Middleware\VerifyCsrfToken',

Now you can add the middleware to individual routes / controllers using `['middleware' => 'csrf']` on the route. For more information on middleware, consult the [full documentation](/docs/{{version}}/middleware).

### Eloquent Models

Feel free to create a new `app/Models` directory to house your Eloquent models. Again, add this directory to the `classmap` directive of your `composer.json` file.

Update any models using `SoftDeletingTrait` to use `Illuminate\Database\Eloquent\SoftDeletes`.

#### Eloquent Caching

Eloquent no longer provides the `remember` method for caching queries. You now are responsible for caching your queries manually using the `Cache::remember` function. For more information on caching, consult the [full documentation](/docs/{{version}}/cache).

### User Authentication Model

To upgrade your `User` model for Laravel 5's authentication system, follow these instructions:

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

**Remove the UserInterface and RemindableInterface interfaces.**

**Mark the class as implementing the following interfaces:**

```php
implements AuthenticatableContract, CanResetPasswordContract
```

**Include the following traits within the class declaration:**

```php
use Authenticatable, CanResetPassword;
```

**If you used them, remove `Illuminate\Auth\Reminders\RemindableTrait`  and `Illuminate\Auth\UserTrait` from your use block and your class declaration.**

### Cashier User Changes

The name of the trait and interface used by [Laravel Cashier](/docs/{{version}}/billing) has changed. Instead of using `BillableTrait`, use the `Laravel\Cashier\Billable` trait. And, instead of `Laravel\Cashier\BillableInterface` implement the `Laravel\Cashier\Contracts\Billable` interface instead. No other method changes are required.

### Artisan Commands

Move all of your command classes from your old `app/commands` directory to the new `app/Console/Commands` directory. Next, add the `app/Console/Commands` directory to the `classmap` directive of your `composer.json` file.

Then, copy your list of Artisan commands from `start/artisan.php` into the `command` array of the `app/Console/Kernel.php` file.

### Database Migrations & Seeds

Delete the two migrations included with Laravel 5.0, since you should already have the users table in your database.

Move all of your migration classes from the old `app/database/migrations` directory to the new `database/migrations`. All of your seeds should be moved from `app/database/seeds` to `database/seeds`.

### Global IoC Bindings

If you have any [service container](/docs/{{version}}/container) bindings in `start/global.php`, move them all to the `register` method of the `app/Providers/AppServiceProvider.php` file. You may need to import the `App` facade.

Optionally, you may break these bindings up into separate service providers by category.

### Views

Move your views from `app/views` to the new `resources/views` directory.

### Blade Tag Changes

For better security by default, Laravel 5.0 escapes all output from both the `{{ }}` and `{{{ }}}` Blade directives. A new `{!! !!}` directive has been introduced to display raw, unescaped output. The most secure option when upgrading your application is to only use the new `{!! !!}` directive when you are **certain** that it is safe to display raw output.

However, if you **must** use the old Blade syntax, add the following lines at the bottom of `AppServiceProvider@register`:

```php
\Blade::setRawTags('{{', '}}');
\Blade::setContentTags('{{{', '}}}');
\Blade::setEscapedContentTags('{{{', '}}}');
```

This should not be done lightly, and may make your application more vulnerable to XSS exploits. Also, comments with `{{--` will no longer work.

### Translation Files

Move your language files from `app/lang` to the new `resources/lang` directory.

### Public Directory

Copy your application's public assets from your `4.2` application's `public` directory to your new application's `public` directory. Be sure to keep the `5.0` version of `index.php`.

### Tests

Move your tests from `app/tests` to the new `tests` directory.

### Misc. Files

Copy in any other files in your project. For example, `.scrutinizer.yml`, `bower.json` and other similar tooling configuration files.

You may move your Sass, Less, or CoffeeScript to any location you wish. The `resources/assets` directory could be a good default location.

### Form & HTML Helpers

If you're using Form or HTML helpers, you will see an error stating `class 'Form' not found` or `class 'Html' not found`. The Form and HTML helpers have been deprecated in Laravel 5.0; however, there are community-driven replacements such as those maintained by the [Laravel Collective](http://laravelcollective.com/docs/{{version}}/html).

For example, you may add `"laravelcollective/html": "~5.0"` to your `composer.json` file's `require` section.

You'll also need to add the Form and HTML facades and service provider. Edit `config/app.php` and add this line to the 'providers' array:

	'Collective\Html\HtmlServiceProvider',

Next, add these lines to the 'aliases' array:

	'Form' => 'Collective\Html\FormFacade',
	'Html' => 'Collective\Html\HtmlFacade',

### CacheManager

If your application code was injecting `Illuminate\Cache\CacheManager` to get a non-Facade version of Laravel's cache, inject `Illuminate\Contracts\Cache\Repository` instead.

### Pagination

Replace any calls to `$paginator->links()` with `$paginator->render()`.

Replace any calls to `$paginator->getFrom()` and `$paginator->getTo()` with `$paginator->firstItem()` and `$paginator->lastItem()` respectively.

Remove the "get" prefix from calls to `$paginator->getPerPage()`, `$paginator->getCurrentPage()`, `$paginator->getLastPage()` and `$paginator->getTotal()` (e.g. `$paginator->perPage()`).

### Beanstalk Queuing

Laravel 5.0 now requires `"pda/pheanstalk": "~3.0"` instead of `"pda/pheanstalk": "~2.1"`.

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

Replace your `public/index.php` file with [this fresh copy from the repository](https://github.com/laravel/laravel/blob/v4.1.0/public/index.php).

Replace your `artisan` file with [this fresh copy from the repository](https://github.com/laravel/laravel/blob/v4.1.0/artisan).

### Adding Configuration Files & Options

Update your `aliases` and `providers` arrays in your `app/config/app.php` configuration file. The updated values for these arrays can be found [in this file](https://github.com/laravel/laravel/blob/v4.1.0/app/config/app.php). Be sure to add your custom and package service providers / aliases back to the arrays.

Add the new `app/config/remote.php` file [from the repository](https://github.com/laravel/laravel/blob/v4.1.0/app/config/remote.php).

Add the new `expire_on_close` configuration option to your `app/config/session.php` file. The default value should be `false`.

Add the new `failed` configuration section to your `app/config/queue.php` file. Here are the default values for the section:

	'failed' => [
		'database' => 'mysql', 'table' => 'failed_jobs',
	],

**(Optional)** Update the `pagination` configuration option in your `app/config/view.php` file to `pagination::slider-3`.

### Controller Updates

If `app/controllers/BaseController.php` has a `use` statement at the top, change `use Illuminate\Routing\Controllers\Controller;` to `use Illuminate\Routing\Controller;`.

### Password Reminders Updates

Password reminders have been overhauled for greater flexibility. You may examine the new stub controller by running the `php artisan auth:reminders-controller` Artisan command. You may also browse the [updated documentation](/docs/security#password-reminders-and-reset) and update your application accordingly.

Update your `app/lang/en/reminders.php` language file to match [this updated file](https://github.com/laravel/laravel/blob/v4.1.0/app/lang/en/reminders.php).

### Environment Detection Updates

For security reasons, URL domains may no longer be used to detect your application environment. These values are easily spoofable and allow attackers to modify the environment for a request. You should convert your environment detection to use machine host names (`hostname` command on Mac, Linux, and Windows).

### Simpler Log Files

Laravel now generates a single log file: `app/storage/logs/laravel.log`. However, you may still configure this behavior in your `app/start/global.php` file.

### Removing Redirect Trailing Slash

In your `bootstrap/start.php` file, remove the call to `$app->redirectIfTrailingSlash()`. This method is no longer needed as this functionality is now handled by the `.htaccess` file included with the framework.

Next, replace your Apache `.htaccess` file with [this new one](https://github.com/laravel/laravel/blob/v4.1.0/public/.htaccess) that handles trailing slashes.

### Current Route Access

The current route is now accessed via `Route::current()` instead of `Route::getCurrentRoute()`.

### Composer Update

Once you have completed the changes above, you can run the `composer update` function to update your core application files! If you receive class load errors, try running the `update` command with the `--no-scripts` option enabled like so: `composer update --no-scripts`.

### Wildcard Event Listeners

The wildcard event listeners no longer append the event to your handler functions parameters. If you require finding the event that was fired you should use `Event::firing()`.

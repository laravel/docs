# Upgrade Guide

- [Upgrading To 7.0 From 6.x](#upgrade-7.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">
- [Authentication Scaffolding](#authentication-scaffolding)
- [Date Serialization](#date-serialization)
- [Symfony 5 Related Upgrades](#symfony-5-related-upgrades)
</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">
- [Blade Components & "Blade X"](#blade-components-and-blade-x)
- [CORS Support](#cors-support)
- [Factory Types](#factory-types)
- [Markdown Mail Template Updates](#markdown-mail-template-updates)
- [The `Blade::component` Method](#the-blade-component-method)
- [The `assertSee` Assertion](#assert-see)
- [The `different` Validation Rule](#the-different-rule)
- [Unique Route Names](#unique-route-names)
</div>

<a name="upgrade-7.0"></a>
## Upgrading To 7.0 From 6.x

#### Estimated Upgrade Time: 15 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Symfony 5 Required

**Likelihood Of Impact: High**

Laravel 7 upgraded its underlying Symfony components to the 5.x series, which is now also the new minimum compatible version.

### PHP 7.2.5 Required

**Likelihood Of Impact: Low**

The new minimum PHP version is now 7.2.5.

<a name="updating-dependencies"></a>
### Updating Dependencies

Update the following dependencies in your `composer.json` file:

- `laravel/framework` to `^7.0`
- `nunomaduro/collision` to `^4.1`
- `phpunit/phpunit` to `^8.5`
- `laravel/tinker` to `^2.0`
- `facade/ignition` to `^2.0`

The following first-party packages have new major releases to support Laravel 7. If there are any, read through their individual upgrade guides before upgrading:

- [Browser Kit Testing v6.0](https://github.com/laravel/browser-kit-testing/blob/master/UPGRADE.md)
- [Envoy v2.0](https://github.com/laravel/envoy/blob/master/UPGRADE.md)
- [Horizon v4.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Nova v3.0](https://nova.laravel.com/releases)
- [Passport v9.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Scout v8.0](https://github.com/laravel/scout/blob/master/UPGRADE.md)
- [Telescope v3.0](https://github.com/laravel/telescope/releases)
- [Tinker v2.0](https://github.com/laravel/tinker/blob/2.x/CHANGELOG.md)
- UI v2.0 (No changes necessary)

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 7 support.

<a name="symfony-5-related-upgrades"></a>
### Symfony 5 Related Upgrades

**Likelihood Of Impact: High**

Laravel 7 utilizes the 5.x series of the Symfony components. Some minor changes to your application are required to accommodate this upgrade.

First, the `report`, `render`, `shouldReport`, and `renderForConsole` methods of your application's `App\Exceptions\Handler` class should accept instances of the `Throwable` interface instead of `Exception` instances:

    use Throwable;

    public function report(Throwable $exception);
    public function shouldReport(Throwable $exception);
    public function render($request, Throwable $exception);
    public function renderForConsole($output, Throwable $exception);

Next, please update your `session` configuration file's `secure` option to have a fallback value of `null`:

    'secure' => env('SESSION_SECURE_COOKIE', null),

Symfony Console, which is the underlying component that powers Artisan, expects all commands to return an integer. Therefore, you should ensure that any of your commands which return a value are returning integers:

    public function handle()
    {
        // Before...
        return true;

        // After...
        return 0;
    }

### Authentication

<a name="authentication-scaffolding"></a>
#### Scaffolding

**Likelihood Of Impact: High**

All authentication scaffolding has been moved to the `laravel/ui` repository. If you are using Laravel's authentication scaffolding, you should install the `^2.0` release of this package and the package should be installed in all environments. If you were previously including this package in the `require-dev` portion of your application's `composer.json` file, you should move it to the `require` section:

    composer require laravel/ui "^2.0"

#### The `TokenRepositoryInterface`

**Likelihood Of Impact: Low**

A `recentlyCreatedToken` method has been added to the `Illuminate\Auth\Passwords\TokenRepositoryInterface` interface. If you are writing a custom implementation of this interface, you should add this method to your implementation.

### Blade

<a name="the-blade-component-method"></a>
#### The `component` Method

**Likelihood Of Impact: Medium**

The `Blade::component` method has been renamed to `Blade::aliasComponent`. Please update your calls to this method accordingly.

<a name="blade-components-and-blade-x"></a>
#### Blade Components & "Blade X"

**Likelihood Of Impact: Medium**

Laravel 7 includes first-party support for Blade "tag components". If you wish to disable Blade's built-in tag component functionality, you may call the `withoutComponentTags` method from the `boot` method of your `AppServiceProvider`:

    use Illuminate\Support\Facades\Blade;

    Blade::withoutComponentTags();

### Eloquent

#### The `addHidden` / `addVisible` Methods

**Likelihood Of Impact: Low**

The undocumented `addHidden` and `addVisible` methods have been removed. Instead, please use the `makeHidden` and `makeVisible` methods.

#### The `booting` / `booted` Methods

**Likelihood Of Impact: Low**

The `booting` and `booted` methods have been added to Eloquent to provide a place to conveniently define any logic that should execute during the model "boot" process. If you already have model methods with these names, you will need to rename your methods so they do not conflict with the newly added methods.

<a name="date-serialization"></a>
#### Date Serialization

**Likelihood Of Impact: High**

Laravel 7 uses a new date serialization format when using the `toArray` or `toJson` method on Eloquent models. To format dates for serialization, the framework now uses Carbon's `toJSON` method, which produces an ISO-8601 compatible date including timezone information and fractional seconds. In addition, this change provides better support and integration with client-side date parsing libraries.

Previously, dates would be serialized to a format like the following: `2019-12-02 20:01:00`. Dates serialized using the new format will appear like: `2019-12-02T20:01:00.283041Z`. Please note that ISO-8601 dates are always expressed in UTC.

If you would like to keep using the previous behavior you can override the `serializeDate` method on your model:

    use DateTimeInterface;

    /**
     * Prepare a date for array / JSON serialization.
     *
     * @param  \DateTimeInterface  $date
     * @return string
     */
    protected function serializeDate(DateTimeInterface $date)
    {
        return $date->format('Y-m-d H:i:s');
    }

> {tip} This change only affects serialization of models and model collections to arrays and JSON. This change has no effect on how dates are stored in your database.

<a name="factory-types"></a>
#### Factory Types

**Likelihood Of Impact: Medium**

Laravel 7 removes the "factory types" feature. This feature has been undocumented since October 2016. If you are still using this feature, you should upgrade to [factory states](/docs/{{version}}/database-testing#factory-states), which provide more flexibility.

#### The `getOriginal` Method

**Likelihood Of Impact: Low**

The `$model->getOriginal()` method will now respect any casts and mutators defined on the model. Previously, this method returned the uncast, raw attributes. If you would like to continue retrieving the raw, uncast values, you may use the `getRawOriginal` method instead.

#### Route Binding

**Likelihood Of Impact: Low**

The `resolveRouteBinding` method of the `Illuminate\Contracts\Routing\UrlRoutable` interface now accepts a `$field` argument. If you were implementing this interface by hand, you should update your implementation.

In addition, the `resolveRouteBinding` method of the `Illuminate\Database\Eloquent\Model` class also now accepts a `$field` parameter. If you were overriding this method, you should update your method to accept this argument.

Finally, the `resolveRouteBinding` method of the `Illuminate\Http\Resources\DelegatesToResources` trait also now accepts a `$field` parameter. If you were overriding this method, you should update your method to accept this argument.

### HTTP

#### PSR-7 Compatibility

**Likelihood Of Impact: Low**

The Zend Diactoros library for generating PSR-7 responses has been deprecated. If you are using this package for PSR-7 compatibility, please install the `nyholm/psr7` Composer package instead. In addition, please install the `^2.0` release of the `symfony/psr-http-message-bridge` Composer package.

### Mail

#### Configuration File Changes

**Likelihood Of Impact: Optional**

In order to support multiple mailers, the default `mail` configuration file has changed in Laravel 7.x to include an array of `mailers`. However, in order to preserve backwards compatibility, the Laravel 6.x format of this configuration file is still supported. So, no changes are **required** when upgrading to Laravel 7.x; however, you may wish to [examine the new `mail` configuration file](https://github.com/laravel/laravel/blob/develop/config/mail.php) structure and update your file to reflect the changes.

<a name="markdown-mail-template-updates"></a>
#### Markdown Mail Template Updates

**Likelihood Of Impact: Medium**

The default Markdown mail templates have been refreshed with a more professional and appealing design. In addition, the undocumented `promotion` Markdown mail component has been removed.

Because indentation has special meaning within Markdown, Markdown mail templates expect unindented HTML. If you've previously published Laravel's default mail templates, you'll need to re-publish your mail templates or manually unindent them:

    php artisan vendor:publish --tag=laravel-mail --force

#### Swift Mailer Bindings

**Likelihood Of Impact: Low**

Laravel 7.x doesn't provide `swift.mailer` and `swift.transport` container bindings. You may now access these objects through the `mailer` binding:

    $swiftMailer = app('mailer')->getSwiftMailer();

    $swiftTransport = $swiftMailer->getTransport();

### Resources

#### The `Illuminate\Http\Resources\Json\Resource` Class

**Likelihood Of Impact: Low**

The deprecated `Illuminate\Http\Resources\Json\Resource` class has been removed. Your resources should extend the `Illuminate\Http\Resources\Json\JsonResource` class instead.

### Routing

#### The Router `getRoutes` Method

**Likelihood Of Impact: Low**

The router's `getRoutes` method now returns an instance of `Illuminate\Routing\RouteCollectionInterface` instead of `Illuminate\Routing\RouteCollection`.

<a name="unique-route-names"></a>
#### Unique Route Names

**Likelihood Of Impact: Medium**

Even though never officially documented, previous Laravel releases allow you to define two different routes with the same name. In Laravel 7 this is no longer possible and you should always provide unique names for your routes. Routes with duplicate names can cause unexpected behavior in multiple areas of the framework.

<a name="cors-support"></a>
#### CORS Support

**Likelihood Of Impact: Medium**

Cross-Origin Resource Sharing (CORS) support is now integrated by default. If you are using any third-party CORS libraries you are now advised to use the [new `cors` configuration file](https://github.com/laravel/laravel/blob/master/config/cors.php).

Next, install the underlying CORS library as a dependency of your application:

    composer require fruitcake/laravel-cors

Finally, add the `\Fruitcake\Cors\HandleCors::class` middleware to your `App\Http\Kernel` global middleware list.

### Session

#### The `array` Session Driver

**Likelihood Of Impact: Low**

The `array` session driver data is now persistent for the current request. Previously, data stored in the `array` session could not be retrieved even during the current request.

### Testing

<a name="assert-see"></a>
#### The `assertSee` Assertion

**Likelihood Of Impact: Medium**

The `assertSee`, `assertDontSee`, `assertSeeText`, `assertDontSeeText`, `assertSeeInOrder` and `assertSeeTextInOrder` assertions on the `TestResponse` class will now automatically escape values. If you are manually escaping any values passed to these assertions you should no longer do so. If you need to assert unescaped values, you may pass `false` as the second argument to the method.

<a name="test-response"></a>
#### The `TestResponse` Class

**Likelihood Of Impact: Low**

The `Illuminate\Foundation\Testing\TestResponse` class has been renamed to `Illuminate\Testing\TestResponse`. If you're extending this class, make sure to update the namespace.

<a name="assert-class"></a>
#### The `Assert` Class

**Likelihood Of Impact: Low**

The `Illuminate\Foundation\Testing\Assert` class has been renamed to `Illuminate\Testing\Assert`. If you're using this class, make sure to update the namespace.

### Validation

<a name="the-different-rule"></a>
#### The `different` Rule

**Likelihood Of Impact: Medium**

The `different` rule will now fail if one of the specified parameters is missing from the request.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/6.x...master) and choose which updates are important to you.

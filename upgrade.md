# Upgrade Guide

- [Upgrading To 5.8.0 From 5.7](#upgrade-5.8.0)

<a name="upgrade-5.8.0"></a>
## Upgrading To 5.8.0 From 5.7

#### Estimated Upgrade Time: 10 Minutes

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.8.*` in your `composer.json` file.

Of course, don't forget to examine any 3rd party packages consumed by your application and verify you are using the proper version for Laravel 5.8 support.

### The `Application` Contract

#### The `environment` Method

**Likelihood Of Impact: Very Low**

The `environment` method signature of the `Illuminate/Contracts/Foundation/Application` contract [has changed](https://github.com/laravel/framework/pull/26296). If you are implementing this contract in your application, you should update the method signature:

    /**
     * Get or check the current application environment.
     *
     * @param  string|array  $environments
     * @return string|bool
     */
    public function environment(...$environments);

#### Added Methods

**Likelihood Of Impact: Low**

The `bootstrapPath`, `configPath`, `databasePath`, `environmentPath`, `resourcePath`, `storagePath`, `resolveProvider`, `bootstrapWith`, `configurationIsCached`, `detectEnvironment`, `environmentFile`, `environmentFilePath`, `getCachedConfigPath`, `getCachedRoutesPath`, `getLocale`, `getNamespace`, `getProviders`, `hasBeenBootstrapped`, `loadDeferredProviders`, `loadEnvironmentFrom`, `routesAreCached`, `setLocale`, `shouldSkipMiddleware` and `terminate`  methods [were added to the `Illuminate/Contracts/Foundation/Application` contract](https://github.com/laravel/framework/pull/26477).

If you are implementing this interface, you should add these methods to your implementation.

### Collections

#### The `firstWhere` Method

**Likelihood Of Impact: Very Low**

The `firstWhere` method signature [has changed](https://github.com/laravel/framework/pull/26261) to match the `where` method's signature. If you are overriding this method, you should update the method signature to match its parent:

    /**
     * Get the first item by the given key value pair.
     *
     * @param  string  $key
     * @param  mixed  $operator
     * @param  mixed  $value
     * @return mixed
     */
    public function firstWhere($key, $operator = null, $value = null);

### Console

#### The `Kernel` Contract

**Likelihood Of Impact: Very Low**

The `terminate` method [has been added to the `Illuminate/Contracts/Console/Kernel` contract](https://github.com/laravel/framework/pull/26393). If you are implementing this interface, you should add this method to your implementation.

### Container

**Likelihood Of Impact: Medium**

#### The `makeWith` Method

The `makeWith` method [has been deprecated](https://github.com/laravel/framework/pull/26644) and will be removed in Laravel `5.9`. You should use the `make` method instead.

#### `ArrayAccess` Contract Added To The `Container` Contract

**Likelihood Of Impact: Very Low**

[The `Illuminate\Contracts\Container\Container` contract](https://github.com/laravel/framework/pull/26378) now extends the `ArrayAccess` contract. If you are implementing the `Container` interface, your implementation should now also satisfy the `ArrayAccess` contract.

#### The `addContextualBinding` Method

**Likelihood Of Impact: Very Low**

The `addContextualBinding` method [was added to the `Illuminate\Contracts\Container\Container` contract](https://github.com/laravel/framework/pull/26551):

    /**
     * Add a contextual binding to the container.
     *
     * @param  string  $concrete
     * @param  string  $abstract
     * @param  \Closure|string  $implementation
     * @return void
     */
    public function addContextualBinding($concrete, $abstract, $implementation);

If you are implementing this interface, you should add this method to your implementation.

#### The `flush` Method

**Likelihood Of Impact: Very Low**

The `flush` method [was added to the `Illuminate\Contracts\Container\Container` contract](https://github.com/laravel/framework/pull/26477):

    /**
     * Flush the container of all bindings and resolved instances.
     *
     * @return void
     */
    public function flush();

If you are implementing this interface, you should add this method to your implementation.

### Database

#### Unquoted MySQL JSON Values

**Likelihood Of Impact: Low**

The query builder will now return unquoted JSON values when using MySQL and MariaDB. This behavior is consistent with the other supported databases:

    $value = DB::table('users')->value('options->language');

    dump($value);

    // Laravel 5.7...
    '"en"'

    // Laravel 5.8...
    'en'

As a result, the `->>` operator is no longer supported or necessary.

#### SQLite

**Likelihood Of Impact: Medium**

As of Laravel 5.8 the [oldest supported SQLite version](https://github.com/laravel/framework/pull/25995) is SQLite 3.7.11. If you are using an older SQLite version, you should update it (SQLite 3.8.8+ is recommended).

### Eloquent

#### The `originalIsEquivalent` Method

**Likelihood Of Impact: Very Low**

The `originalIsEquivalent` method of the `Illuminate\Database\Eloquent\Concerns\HasAttributes` trait [has been changed](https://github.com/laravel/framework/pull/26391) from `protected` to `public`.

### Events

#### The `fire` Method

The `fire` method (which was deprecated in Laravel 5.4) of the `Illuminate/Events/Dispatcher` class [has been removed](https://github.com/laravel/framework/pull/26392).
You should use the `dispatch` method instead.

### Exception Handling

#### The `ExceptionHandler` Contract

**Likelihood Of Impact: Low**

The `shouldReport` method [has been added to the `Illuminate\Contracts\Debug\ExceptionHandler` contract](https://github.com/laravel/framework/pull/26193). If you are implementing this interface, you should add this method to your implementation.

#### The `renderHttpException` Method

**Likelihood Of Impact: Low**

The `renderHttpException` method signature of the `Illuminate\Foundation\Exceptions\Handler` class [has changed](https://github.com/laravel/framework/pull/25975). If you are overriding this method in your exception handler, you should update the method signature to match its parent:

    /**
     * Render the given HttpException.
     *
     * @param  \Symfony\Component\HttpKernel\Exception\HttpExceptionInterface  $e
     * @return \Symfony\Component\HttpFoundation\Response
     */
    protected function renderHttpException(HttpExceptionInterface $e);

### Facades

#### Facade Service Resolving

**Likelihood Of Impact: Low**

The `getFacadeAccessor` method may now [only return the string value representing the container identifier of the service](https://github.com/laravel/framework/pull/25525). Previously, this method may have returned an object instance.

### Requests

#### The `TransformsRequest` Middleware

**Likelihood Of Impact: Low**

The `transform` method of the `Illuminate\Foundation\Http\Middleware\TransformsRequest` middleware now receives the "fully-qualified" request input key when the input is an array:

    'employee' => [
        'name' => 'Taylor Otwell',
    ],

    /**
     * Transform the given value.
     *
     * @param  string  $key
     * @param  mixed  $value
     * @return mixed
     */
    protected function transform($key, $value)
    {
        dump($key); // 'employee.name' (Laravel 5.8)
        dump($key); // 'name' (Laravel 5.7)
    }

### Routing

#### The `UrlGenerator` Contract

**Likelihood Of Impact: Very Low**

The `previous` method [has been added to the `Illuminate\Contracts\Routing\UrlGenerator` contract](https://github.com/laravel/framework/pull/25616). If you are implementing this interface, you should add this method to your implementation.

### Sessions

#### The `StartSession` Middleware

**Likelihood Of Impact: Very Low**

The session persistence logic has been [moved from the `terminate()` method to the `handle()` method](https://github.com/laravel/framework/pull/26410). If you are overriding one or both of these methods, you should update them to reflect these changes.

### Validation

#### The `Validator` Contract

**Likelihood Of Impact: Very Low**

The `validated` method [was added to the `Illuminate\Contracts\Validation\Validator` contract](https://github.com/laravel/framework/pull/26419):

    /**
     * Get the attributes and values that were validated.
     *
     * @return array
     */
    public function validated();

If you are implementing this interface, you should add this method to your implementation.

#### Email validation

**Likelihood Of Impact: Very Low**

The email validation rule now checks if the email is [RFC5630](https://tools.ietf.org/html/rfc6530) compliant (so that the validation is consistent with the one Swift Mailer performs). The email validation rule in Laravel `5.7` was only checking if the email is [RFC822](https://tools.ietf.org/html/rfc822) compliant which means that in `5.8` emails that were previously incorrectly considered invalid will now be considered valid e.g `hej@bär.se`.  Generally, this should be considered a bug fix; however, it is listed as a breaking change out of caution. [Please let us know if you encounter any issues surrounding this change](https://github.com/laravel/framework/pull/26503).

### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/5.7...master) and choose which updates are important to you.

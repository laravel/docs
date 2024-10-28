# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Flysystem 3.x](#flysystem-3)
- [Symfony Mailer](#symfony-mailer)

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods](#belongs-to-many-first-or-new)
- [Custom Casts & `null`](#custom-casts-and-null)
- [Default HTTP Client Timeout](#http-client-default-timeout)
- [PHP Return Types](#php-return-types)
- [Postgres "Schema" Configuration](#postgres-schema-configuration)
- [The `assertDeleted` Method](#the-assert-deleted-method)
- [The `lang` Directory](#the-lang-directory)
- [The `password` Rule](#the-password-rule)
- [The `when` / `unless` Methods](#when-and-unless-methods)
- [Unvalidated Array Keys](#unvalidated-array-keys)

</div>

<a name="upgrade-9.0"></a>
## Upgrading To 9.0 From 8.x

<a name="estimated-upgrade-time-30-minutes"></a>
#### Estimated Upgrade Time: 30 Minutes

> **Note**  
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. Want to save time? You can use [Laravel Shift](https://laravelshift.com/) to help automate your application upgrades.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

#### PHP 8.0.2 Required

Laravel now requires PHP 8.0.2 or greater.

#### Composer Dependencies

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- `laravel/framework` to `^9.0`
- `nunomaduro/collision` to `^6.1`

</div>

In addition, please replace `facade/ignition` with `"spatie/laravel-ignition": "^1.0"` and `pusher/pusher-php-server` (if applicable) with `"pusher/pusher-php-server": "^5.0"` in your application's `composer.json` file.

Furthermore, the following first-party packages have received new major releases to support Laravel 9.x. If applicable, you should read their individual upgrade guides before upgrading:

<div class="content-list" markdown="1">

- [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Replaces Nexmo)

</div>

Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 9 support.

<a name="php-return-types"></a>
#### PHP Return Types

PHP is beginning to transition to requiring return type definitions on PHP methods such as `offsetGet`, `offsetSet`, etc. In light of this, Laravel 9 has implemented these return types in its code base. Typically, this should not affect user written code; however, if you are overriding one of these methods by extending Laravel's core classes, you will need to add these return types to your own application or package code:

<div class="content-list" markdown="1">

- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`

</div>

In addition, return types were added to methods implementing PHP's `SessionHandlerInterface`. Again, it is unlikely that this change affects your own application or package code:

<div class="content-list" markdown="1">

- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`

</div>

<a name="application"></a>
### Application

<a name="the-application-contract"></a>
#### The `Application` Contract

**Likelihood Of Impact: Low**

The `storagePath` method of the `Illuminate\Contracts\Foundation\Application` interface has been updated to accept a `$path` argument. If you are implementing this interface you should update your implementation accordingly:

    public function storagePath($path = '');
    
Similarly, the `langPath` method of the `Illuminate\Foundation\Application` class has been updated to accept a `$path` argument: 

    public function langPath($path = '');

#### Exception Handler `ignore` Method

**Likelihood Of Impact: Low**

The exception handler's `ignore` method is now `public` instead of `protected`. This method is not included in the default application skeleton; however, if you have manually defined this method you should update its visibility to `public`:

```php
public function ignore(string $class);
```

#### Exception Handler Contract Binding

**Likelihood Of Impact: Very Low**

Previously, in order to override the default Laravel exception handler, custom implementations were bound into the service container using the `\App\Exceptions\Handler::class` type. However, you should now bind custom implementations using the `\Illuminate\Contracts\Debug\ExceptionHandler::class` type.

### Blade

#### Lazy Collections & The `$loop` Variable

**Likelihood Of Impact: Low**

When iterating over a `LazyCollection` instance within a Blade template, the `$loop` variable is no longer available, as accessing this variable causes the entire `LazyCollection` to be loaded into memory, thus rendering the usage of lazy collections pointless in this scenario.

#### Checked / Disabled / Selected Blade Directives

**Likelihood Of Impact: Low**

The new `@checked`, `@disabled`, and `@selected` Blade directives may conflict with Vue events of the same name. You may use `@@` to escape the directives and avoid this conflict: `@@selected`.

### Collections

#### The `Enumerable` Contract

**Likelihood Of Impact: Low**

The `Illuminate\Support\Enumerable` contract now defines a `sole` method. If you are manually implementing this interface, you should update your implementation to reflect this new method:

```php
public function sole($key = null, $operator = null, $value = null);
```

#### The `reduceWithKeys` Method

The `reduceWithKeys` method has been removed as the `reduce` method provides the same functionality. You may simply update your code to call `reduce` instead of `reduceWithKeys`.

#### The `reduceMany` Method

The `reduceMany` method has been renamed to `reduceSpread` for naming consistency with other similar methods.

### Container

#### The `Container` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Container\Container` contract has received two method definitions: `scoped` and `scopedIf`. If you are manually implementing this contract, you should update your implementation to reflect these new methods.

#### The `ContextualBindingBuilder` Contract

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Container\ContextualBindingBuilder` contract now defines a `giveConfig` method. If you are manually implementing this interface, you should update your implementation to reflect this new method:

```php
public function giveConfig($key, $default = null);
```

### Database

<a name="postgres-schema-configuration"></a>
#### Postgres "Schema" Configuration

**Likelihood Of Impact: Medium**

The `schema` configuration option used to configure Postgres connection search paths in your application's `config/database.php` configuration file should be renamed to `search_path`.

<a name="schema-builder-doctrine-method"></a>
#### Schema Builder `registerCustomDoctrineType` Method

**Likelihood Of Impact: Low**

The `registerCustomDoctrineType` method has been removed from the `Illuminate\Database\Schema\Builder` class. You may use the `registerDoctrineType` method on the `DB` facade instead, or register custom Doctrine types in the `config/database.php` configuration file.

### Eloquent

<a name="custom-casts-and-null"></a>
#### Custom Casts & `null`

**Likelihood Of Impact: Medium**

In previous releases of Laravel, the `set` method of custom cast classes was not invoked if the cast attribute was being set to `null`. However, this behavior was inconsistent with the Laravel documentation. In Laravel 9.x, the `set` method of the cast class will be invoked with `null` as the provided `$value` argument. Therefore, you should ensure your custom casts are able to sufficiently handle this scenario:

```php
/**
 * Prepare the given value for storage.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  AddressModel  $value
 * @param  array  $attributes
 * @return array
 */
public function set($model, $key, $value, $attributes)
{
    if (! $value instanceof AddressModel) {
        throw new InvalidArgumentException('The given value is not an Address instance.');
    }

    return [
        'address_line_one' => $value->lineOne,
        'address_line_two' => $value->lineTwo,
    ];
}
```

<a name="belongs-to-many-first-or-new"></a>
#### Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` Methods

**Likelihood Of Impact: Medium**

The `belongsToMany` relationship's `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods all accept an array of attributes as their first argument. In previous releases of Laravel, this array of attributes was compared against the "pivot" / intermediate table for existing records.

However, this behavior was unexpected and typically unwanted. Instead, these methods now compare the array of attributes against the table of the related model:

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

In addition, the `firstOrCreate` method now accepts a `$values` array as its second argument. This array will be merged with the first argument to the method (`$attributes`) when creating the related model if one does not already exist. This change makes this method consistent with the `firstOrCreate` methods offered by other relationship types:

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

#### The `touch` Method

**Likelihood Of Impact: Low**

The `touch` method now accepts an attribute to touch. If you were previously overwriting this method, you should update your method signature to reflect this new argument:

```php
public function touch($attribute = null);
```

### Encryption

#### The Encrypter Contract

**Likelihood Of Impact: Low**

The `Illuminate\Contracts\Encryption\Encrypter` contract now defines a `getKey` method. If you are manually implementing this interface, you should update your implementation accordingly:

```php
public function getKey();
```

### Facades

#### The `getFacadeAccessor` Method

**Likelihood Of Impact: Low**

The `getFacadeAccessor` method must always return a container binding key. In previous releases of Laravel, this method could return an object instance; however, this behavior is no longer supported. If you have written your own facades, you should ensure that this method returns a container binding string:

```php
/**
 * Get the registered name of the component.
 *
 * @return string
 */
protected static function getFacadeAccessor()
{
    return Example::class;
}
```

### Filesystem

#### The `FILESYSTEM_DRIVER` Environment Variable

**Likelihood Of Impact: Low**

The `FILESYSTEM_DRIVER` environment variable has been renamed to `FILESYSTEM_DISK` to more accurately reflect its usage. This change only affects the application skeleton; however, you are welcome to update your own application's environment variables to reflect this change if you wish.

#### The "Cloud" Disk

**Likelihood Of Impact: Low**

The `cloud` disk configuration option was removed from the default application skeleton in November of 2020. This change only affects the application skeleton. If you are using the `cloud` disk within your application, you should leave this configuration value in your own application's skeleton.

<a name="flysystem-3"></a>
### Flysystem 3.x

**Likelihood Of Impact: High**

Laravel 9.x has migrated from [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x to 3.x. Under the hood, Flysystem powers all of the file manipulation methods provided by the `Storage` facade. In light of this, some changes may be required within your application; however, we have tried to make this transition as seamless as possible.

#### Driver Prerequisites

Before using the S3, FTP, or SFTP drivers, you will need to install the appropriate package via the Composer package manager:

- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`

#### Overwriting Existing Files

Write operations such as `put`, `write`, and `writeStream` now overwrite existing files by default. If you do not want to overwrite existing files, you should manually check for the file's existence before performing the write operation.

#### Write Exceptions

Write operations such as `put`, `write`, and `writeStream` no longer throw an exception when a write operation fails. Instead, `false` is returned. If you would like to preserve the previous behavior which threw exceptions, you may define the `throw` option within a filesystem disk's configuration array:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

#### Reading Missing Files

Attempting to read from a file that does not exist now returns `null`. In previous releases of Laravel, an `Illuminate\Contracts\Filesystem\FileNotFoundException` would have been thrown.

#### Deleting Missing Files

Attempting to `delete` a file that does not exist now returns `true`.

#### Cached Adapters

Flysystem no longer supports "cached adapters". Thus, they have been removed from Laravel and any relevant configuration (such as the `cache` key within disk configurations) can be removed.

#### Custom Filesystems

Slight changes have been made to the steps required to register custom filesystem drivers. Therefore, if you were defining your own custom filesystem drivers, or using packages that define custom drivers, you should update your code and dependencies.

For example, in Laravel 8.x, a custom filesystem driver might be registered like so:

```php
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $client = new DropboxClient(
        $config['authorization_token']
    );

    return new Filesystem(new DropboxAdapter($client));
});
```

However, in Laravel 9.x, the callback given to the `Storage::extend` method should return an instance of `Illuminate\Filesystem\FilesystemAdapter` directly:

```php
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $adapter = new DropboxAdapter(
        new DropboxClient($config['authorization_token'])
    );

    return new FilesystemAdapter(
        new Filesystem($adapter, $config),
        $adapter,
        $config
    );
});
```

#### SFTP Private-Public Key Passphrase

If your application is using Flysystem's SFTP adapter and private-public key authentication, the `password` configuration item that is used to decrypt the private key should be renamed to `passphrase`.

#### AWS S3 V3 - Checking file/directory exists

Since [Flysystem v3 3.12.1](https://github.com/thephpleague/flysystem/tree/3.12.1), the way checking file / directory existence was changed. More information can be found [here](https://github.com/laravel/framework/issues/45639) but you may need to catch `League\Flysystem\UnableToCheckFileExistence` exceptions when using `Storage::exists()`, based on your AWS permission settings.

### Helpers

<a name="data-get-function"></a>
#### The `data_get` Helper & Iterable Objects

**Likelihood Of Impact: Very Low**

Previously, the `data_get` helper could be used to retrieve nested data on arrays and `Collection` instances; however, this helper can now retrieve nested data on all iterable objects.

<a name="str-function"></a>
#### The `str` Helper

**Likelihood Of Impact: Very Low**

Laravel 9.x now includes a global `str` [helper function](/docs/{{version}}/helpers#method-str). If you are defining a global `str` helper in your application, you should rename or remove it so that it does not conflict with Laravel's own `str` helper.

<a name="when-and-unless-methods"></a>
#### The `when` / `unless` Methods

**Likelihood Of Impact: Medium**

As you may know, `when` and `unless` methods are offered by various classes throughout the framework. These methods can be used to conditionally perform an action if the boolean value of the first argument to the method evaluates to `true` or `false`:

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

Therefore, in previous releases of Laravel, passing a closure to the `when` or `unless` methods meant that the conditional operation would always execute, since a loose comparison against a closure object (or any other object) always evaluates to `true`. This often led to unexpected outcomes because developers expect the **result** of the closure to be used as the boolean value that determines if the conditional action executes.

So, in Laravel 9.x, any closures passed to the `when` or `unless` methods will be executed and the value returned by the closure will be considered the boolean value used by the `when` and `unless` methods:

```php
$collection->when(function ($collection) {
    // This closure is executed...
    return false;
}, function ($collection) {
    // Not executed since first closure returned "false"...
    $collection->merge([1, 2, 3]);
});
```

### HTTP Client

<a name="http-client-default-timeout"></a>
#### Default Timeout

**Likelihood Of Impact: Medium**

The [HTTP client](/docs/{{version}}/http-client) now has a default timeout of 30 seconds. In other words, if the server does not respond within 30 seconds, an exception will be thrown. Previously, no default timeout length was configured on the HTTP client, causing requests to sometimes "hang" indefinitely.

If you wish to specify a longer timeout for a given request, you may do so using the `timeout` method:

    $response = Http::timeout(120)->get(/* ... */);

#### HTTP Fake & Middleware

**Likelihood Of Impact: Low**

Previously, Laravel would not execute any provided Guzzle HTTP middleware when the [HTTP client](/docs/{{version}}/http-client) was "faked". However, in Laravel 9.x, Guzzle HTTP middleware will be executed even when the HTTP client is faked.

#### HTTP Fake & Dependency Injection

**Likelihood Of Impact: Low**

In previous releases of Laravel, invoking the `Http::fake()` method would not affect instances of the `Illuminate\Http\Client\Factory` that were injected into class constructors. However, in Laravel 9.x, `Http::fake()` will ensure fake responses are returned by HTTP clients injected into other services via dependency injection. This behavior is more consistent with the behavior of other facades and fakes.

<a name="symfony-mailer"></a>
### Symfony Mailer

**Likelihood Of Impact: High**

One of the largest changes in Laravel 9.x is the transition from SwiftMailer, which is no longer maintained as of December 2021, to Symfony Mailer. However, we have tried to make this transition as seamless as possible for your applications. That being said, please thoroughly review the list of changes below to ensure your application is fully compatible.

#### Driver Prerequisites

To continue using the Mailgun transport, your application should require the `symfony/mailgun-mailer` and `symfony/http-client` Composer packages:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

The `wildbit/swiftmailer-postmark` Composer package should be removed from your application. Instead, your application should require the `symfony/postmark-mailer` and `symfony/http-client` Composer packages:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

#### Updated Return Types

The `send`, `html`, `raw`, and `plain` methods on `Illuminate\Mail\Mailer` no longer return `void`. Instead, an instance of `Illuminate\Mail\SentMessage` is returned. This object contains an instance of `Symfony\Component\Mailer\SentMessage` that is accessible via the `getSymfonySentMessage` method or by dynamically invoking methods on the object.

#### Renamed "Swift" Methods

Various SwiftMailer related methods, some of which were undocumented, have been renamed to their Symfony Mailer counterparts. For example, the `withSwiftMessage` method has been renamed to `withSymfonyMessage`:

    // Laravel 8.x...
    $this->withSwiftMessage(function ($message) {
        $message->getHeaders()->addTextHeader(
            'Custom-Header', 'Header Value'
        );
    });

    // Laravel 9.x...
    use Symfony\Component\Mime\Email;

    $this->withSymfonyMessage(function (Email $message) {
        $message->getHeaders()->addTextHeader(
            'Custom-Header', 'Header Value'
        );
    });

> **Warning**  
> Please thoroughly review the [Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages) for all possible interactions with the `Symfony\Component\Mime\Email` object.

The list below contains a more thorough overview of renamed methods. Many of these methods are low-level methods used to interact with SwiftMailer / Symfony Mailer directly, so may not be commonly used within most Laravel applications:

    Message::getSwiftMessage();
    Message::getSymfonyMessage();

    Mailable::withSwiftMessage($callback);
    Mailable::withSymfonyMessage($callback);

    MailMessage::withSwiftMessage($callback);
    MailMessage::withSymfonyMessage($callback);

    Mailer::getSwiftMailer();
    Mailer::getSymfonyTransport();

    Mailer::setSwiftMailer($swift);
    Mailer::setSymfonyTransport(TransportInterface $transport);

    MailManager::createTransport($config);
    MailManager::createSymfonyTransport($config);

#### Proxied `Illuminate\Mail\Message` Methods

The `Illuminate\Mail\Message` typically proxied missing methods to the underlying `Swift_Message` instance. However, missing methods are now proxied to an instance of `Symfony\Component\Mime\Email` instead. So, any code that was previously relying on missing methods to be proxied to SwiftMailer should be updated to their corresponding Symfony Mailer counterparts.

Again, many applications may not be interacting with these methods, as they are not documented within the Laravel documentation:

    // Laravel 8.x...
    $message
        ->setFrom('taylor@laravel.com')
        ->setTo('example@example.org')
        ->setSubject('Order Shipped')
        ->setBody('<h1>HTML</h1>', 'text/html')
        ->addPart('Plain Text', 'text/plain');

    // Laravel 9.x...
    $message
        ->from('taylor@laravel.com')
        ->to('example@example.org')
        ->subject('Order Shipped')
        ->html('<h1>HTML</h1>')
        ->text('Plain Text');

#### Generated Messages IDs

SwiftMailer offered the ability to define a custom domain to include in generated Message IDs via the `mime.idgenerator.idright` configuration option. This is not supported by Symfony Mailer. Instead, Symfony Mailer will automatically generate a Message ID based on the sender.

#### `MessageSent` Event Changes

The `message` property of the `Illuminate\Mail\Events\MessageSent` event now contains an instance of `Symfony\Component\Mime\Email` instead of an instance of `Swift_Message`. This message represents the email **before** it is sent.

Additionally, a new `sent` property has been added to the `MessageSent` event. This property contains an instance of `Illuminate\Mail\SentMessage` and contains information about the sent email, such as the message ID.

#### Forced Reconnections

It is no longer possible to force a transport reconnection (for example when the mailer is running via a daemon process). Instead, Symfony Mailer will attempt to reconnect to the transport automatically and throw an exception if the reconnection fails.

#### SMTP Stream Options

Defining stream options for the SMTP transport is no longer supported. Instead, you must define the relevant options directly within the configuration if they are supported. For example, to disable TLS peer verification:

    'smtp' => [
        // Laravel 8.x...
        'stream' => [
            'ssl' => [
                'verify_peer' => false,
            ],
        ],

        // Laravel 9.x...
        'verify_peer' => false,
    ],

To learn more about the available configuration options, please review the [Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#transport-setup).

> **Warning**  
> In spite of the example above, you are not generally advised to disable SSL verification since it introduces the possibility of "man-in-the-middle" attacks.

#### SMTP `auth_mode`

Defining the SMTP `auth_mode` in the `mail` configuration file is no longer required. The authentication mode will be automatically negotiated between Symfony Mailer and the SMTP server.

#### Failed Recipients

It is no longer possible to retrieve a list of failed recipients after sending a message. Instead, a `Symfony\Component\Mailer\Exception\TransportExceptionInterface` exception will be thrown if a message fails to send. Instead of relying on retrieving invalid email addresses after sending a message, we recommend that you validate email addresses before sending the message instead.

### Packages

<a name="the-lang-directory"></a>
#### The `lang` Directory

**Likelihood Of Impact: Medium**

In new Laravel applications, the `resources/lang` directory is now located in the root project directory (`lang`). If your package is publishing language files to this directory, you should ensure that your package is publishing to `app()->langPath()` instead of a hard-coded path.

<a name="queue"></a>
### Queue

<a name="the-opis-closure-library"></a>
#### The `opis/closure` Library

**Likelihood Of Impact: Low**

Laravel's dependency on `opis/closure` has been replaced by `laravel/serializable-closure`. This should not cause any breaking change in your application unless you are interacting with the `opis/closure` library directly. In addition, the previously deprecated `Illuminate\Queue\SerializableClosureFactory` and `Illuminate\Queue\SerializableClosure` classes have been removed. If you are interacting with `opis/closure` library directly or using any of the removed classes, you may use [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) instead.

#### The Failed Job Provider `flush` Method

**Likelihood Of Impact: Low**

The `flush` method defined by the `Illuminate\Queue\Failed\FailedJobProviderInterface` interface now accepts an `$hours` argument which determines how old a failed job must be (in hours) before it is flushed by the `queue:flush` command. If you are manually implementing the `FailedJobProviderInterface` you should ensure that your implementation is updated to reflect this new argument:

```php
public function flush($hours = null);
```

### Session

#### The `getSession` Method

**Likelihood Of Impact: Low**

The `Symfony\Component\HttpFoundaton\Request` class that is extended by Laravel's own `Illuminate\Http\Request` class offers a `getSession` method to get the current session storage handler. This method is not documented by Laravel as most Laravel applications interact with the session through Laravel's own `session` method.

The `getSession` method previously returned an instance of `Illuminate\Session\Store` or `null`; however, due to the Symfony 6.x release enforcing a return type of `Symfony\Component\HttpFoundation\Session\SessionInterface`, the `getSession` now correctly returns a `SessionInterface` implementation or throws an `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` exception when no session is available.

### Testing

<a name="the-assert-deleted-method"></a>
#### The `assertDeleted` Method

**Likelihood Of Impact: Medium**

All calls to the `assertDeleted` method should be updated to `assertModelMissing`.

### Trusted Proxies

**Likelihood Of Impact: Low**

If you are upgrading your Laravel 8 project to Laravel 9 by importing your existing application code into a totally new Laravel 9 application skeleton, you may need to update your application's "trusted proxy" middleware.

Within your `app/Http/Middleware/TrustProxies.php` file, update `use Fideloper\Proxy\TrustProxies as Middleware` to `use Illuminate\Http\Middleware\TrustProxies as Middleware`.

Next, within `app/Http/Middleware/TrustProxies.php`, you should update the `$headers` property definition:

```php
// Before...
protected $headers = Request::HEADER_X_FORWARDED_ALL;

// After...
protected $headers =
    Request::HEADER_X_FORWARDED_FOR |
    Request::HEADER_X_FORWARDED_HOST |
    Request::HEADER_X_FORWARDED_PORT |
    Request::HEADER_X_FORWARDED_PROTO |
    Request::HEADER_X_FORWARDED_AWS_ELB;
```

Finally, you can remove the `fideloper/proxy` Composer dependency from your application:

```shell
composer remove fideloper/proxy
```

### Validation

#### Form Request `validated` Method

**Likelihood Of Impact: Low**

The `validated` method offered by form requests now accepts `$key` and `$default` arguments. If you are manually overwriting the definition of this method, you should update your method's signature to reflect these new arguments:

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
#### The `password` Rule

**Likelihood Of Impact: Medium**

The `password` rule, which validates that the given input value matches the authenticated user's current password, has been renamed to `current_password`.

<a name="unvalidated-array-keys"></a>
#### Unvalidated Array Keys

**Likelihood Of Impact: Medium**

In previous releases of Laravel, you were required to manually instruct Laravel's validator to exclude unvalidated array keys from the "validated" data it returns, especially in combination with an `array` rule that does not specify a list of allowed keys.

However, in Laravel 9.x, unvalidated array keys are always excluded from the "validated" data even when no allowed keys have been specified via the `array` rule. Typically, this behavior is the most expected behavior and the previous `excludeUnvalidatedArrayKeys` method was only added to Laravel 8.x as a temporary measure in order to preserve backwards compatibility.

Although it is not recommended, you may opt-in to the previous Laravel 8.x behavior by invoking a new `includeUnvalidatedArrayKeys` method within the `boot` method of one of your application's service providers:

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::includeUnvalidatedArrayKeys();
}
```

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) and choose which updates are important to you.

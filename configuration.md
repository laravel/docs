# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining The Current Environment](#determining-the-current-environment)
    - [Encrypting Environment Files](#encrypting-environment-files)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
## Introduction

All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application timezone and encryption key.

<a name="application-overview"></a>
#### Application Overview

In a hurry? You can get a quick overview of your application's configuration, drivers, and environment via the `about` Artisan command:

```shell
php artisan about
```

If you're only interested in a particular section of the application overview output, you may filter for that section using the `--only` option:

```shell
php artisan about --only=environment
```

<a name="environment-configuration"></a>
## Environment Configuration

It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server.

To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`.

Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then retrieved from various Laravel configuration files within the `config` directory using Laravel's `env` function.

If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application.

> **Note**  
> Any variable in your `.env` file can be overridden by external environment variables such as server-level or system-level environment variables.

<a name="environment-file-security"></a>
#### Environment File Security

Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed.

<a name="additional-environment-files"></a>
#### Additional Environment Files

Before loading your application's environment variables, Laravel determines if an `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded.

<a name="environment-variable-types"></a>
### Environment Variable Types

All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function:

| `.env` Value | `env()` Value |
|--------------|---------------|
| true         | (bool) true   |
| (true)       | (bool) true   |
| false        | (bool) false  |
| (false)      | (bool) false  |
| empty        | (string) ''   |
| (empty)      | (string) ''   |
| null         | (null) null   |
| (null)       | (null) null   |

If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes:

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### Retrieving Environment Configuration

All of the variables listed in the `.env` file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` function to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this function:

    'debug' => env('APP_DEBUG', false),

The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key.

<a name="determining-the-current-environment"></a>
### Determining The Current Environment

The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/{{version}}/facades):

    use Illuminate\Support\Facades\App;

    $environment = App::environment();

You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values:

    if (App::environment('local')) {
        // The environment is local
    }

    if (App::environment(['local', 'staging'])) {
        // The environment is either local OR staging...
    }

> **Note**  
> The current application environment detection can be overridden by defining a server-level `APP_ENV` environment variable.

<a name="encrypting-environment-files"></a>
### Encrypting Environment Files

Sometimes, it can be useful to store environment variables in your application's source control repository. For example, you may wish to maintain an up to date version of your production environment variables for use during deployment. Laravel provides a set of Artisan commands which allow you to encrypt your environment files mitigating the security risk of committing them in plaintext.

<a name="encryption"></a>
#### Encryption

In order to encrypt an envrionment file, you may use the `env:encrypt` command:

```shell
php artisan env:encrypt
```

Running the command above will take the contents of your `.env` file, encrypt and write the output to a file called `.env.encrypted`. The decryption key is presented in the output of the command. Should you wish to use your own encryption key, you may pass the `--key` option:

```shell
php artisan env:encrypt --key=qUWuNRdfuImXcKxZ
```

> **Note**  
> The length of the key provided should match that required by the encryption cipher used. Laravel will default to `AES-256-CBC` which requires a 32 character key. You are free to use any cipher supported by Laravel's [encrypter](/docs/{{version}}/encryption) by passing the `--cipher` option.

Should you wish to encrypt a different envrionment, you may use the `--env` option.

```shell
php artisan env:encrypt --env=production
```

The above command will look for a file called `env.production` and will generate an encrypted file called `.env.production.encrypted`.

As a safety measure, if an encrypted environment file already exists, it will not be overwritten. Should you wish to overwrite it, you may pass the `--force` option.

```shell
php artisan env:encrypt --force
```

> **Warning**  
> Without your decryption key, you will not be able to decrypt an encrypted environment file so you should take a note of the key presented to you in the output of the command. Furthermore, this key should be stored securely and kept out of your application's source control to prevent the risk of sensitive credentials being exposed.

<a name="decryption"></a>
#### Decryption

In order to decrypt an encrypted environment file, you may use the `env:decrypt` command. This command requires a decryption key, which can be passed directly to the command:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ
```

> **Note**  
> In some situations, you may not want to expose the decryption key in plaintext when invoking the command. In this scenario, you may add your key to the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable instead.

When the command is invoked, it will look for a file called `.env.encrypted` and use the key to decrypt it to a file called `.env`.

If your environment file was encrypted with a cipher other than the default, you should pass the `--cipher` option to ensure it is decrypted with the same algorithm:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-256-GCM
```

Should you wish to decrypt a different environment, you may pass the `--env` option:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --env=production
```

The command above will attempt to decrypt a file called `.env.production.encrypted` and write it to a file called `.env.prodution`

Sometimes, you may need to write a decrypted environment into a custom file. By default decrypting your production environment during a deployment would result in an environment file called `.env.production`. However, a service such as Laravel Forge reads the environment from a file called `.env`. To mitigate this, you may use the `--filename` option:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --env=production --filename=.env
```

In order to overwrite an existing environment, you may pass the `--force` option.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --force
```

<a name="accessing-configuration-values"></a>
## Accessing Configuration Values

You may easily access your configuration values using the global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist:

    $value = config('app.timezone');

    // Retrieve a default value if the configuration value does not exist...
    $value = config('app.timezone', 'Asia/Seoul');

To set configuration values at runtime, pass an array to the `config` function:

    config(['app.timezone' => 'America/Chicago']);

<a name="configuration-caching"></a>
## Configuration Caching

To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework.

You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development.

> **Warning**  
> If you execute the `config:cache` command during your deployment process, you should be sure that you are only calling the `env` function from within your configuration files. Once the configuration has been cached, the `.env` file will not be loaded; therefore, the `env` function will only return external, system level environment variables.

<a name="debug-mode"></a>
## Debug Mode

The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file.

For local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.**

<a name="maintenance-mode"></a>
## Maintenance Mode

When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503.

To enable maintenance mode, execute the `down` Artisan command:

```shell
php artisan down
```

If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds:

```shell
php artisan down --refresh=15
```

You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header:

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### Bypassing Maintenance Mode

To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode.

> **Note**  
> Your maintenance mode secret should typically consist of alpha-numeric characters and, optionally, dashes. You should avoid using characters that have special meaning in URLs such as `?`.

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### Pre-Rendering The Maintenance Mode View

If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine.

For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option:

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### Redirecting Maintenance Mode Requests

While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI:

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### Disabling Maintenance Mode

To disable maintenance mode, use the `up` command:

```shell
php artisan up
```

> **Note**  
> You may customize the default maintenance mode template by defining your own template at `resources/views/errors/503.blade.php`.

<a name="maintenance-mode-queues"></a>
#### Maintenance Mode & Queues

While your application is in maintenance mode, no [queued jobs](/docs/{{version}}/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode.

<a name="alternatives-to-maintenance-mode"></a>
#### Alternatives To Maintenance Mode

Since maintenance mode requires your application to have several seconds of downtime, consider alternatives like [Laravel Vapor](https://vapor.laravel.com) and [Envoyer](https://envoyer.io) to accomplish zero-downtime deployment with Laravel.

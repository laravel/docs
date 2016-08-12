# Errors & Logging

- [Introduction](#introduction)
- [Configuration](#configuration)
- [The Exception Handler](#the-exception-handler)
    - [Report Method](#report-method)
    - [Render Method](#render-method)
- [HTTP Exceptions](#http-exceptions)
    - [Custom HTTP Error Pages](#custom-http-error-pages)
- [Logging](#logging)

<a name="introduction"></a>
## Introduction

When you start a new Laravel project, error and exception handling is already configured for you. In addition, Laravel is integrated with the [Monolog](https://github.com/Seldaek/monolog) logging library, which provides support for a variety of powerful log handlers.

<a name="configuration"></a>
## Configuration

#### Error Detail

The amount of error detail your application displays through the browser is controlled by the `debug` configuration option in your `config/app.php` configuration file. By default, this configuration option is set to respect the `APP_DEBUG` environment variable, which is stored in your `.env` file.

For local development, you should set the `APP_DEBUG` environment variable to `true`. In your production environment, this value should always be `false`.

#### Log Modes

Out of the box, Laravel supports `single`, `daily`, `syslog` and `errorlog` logging modes. For example, if you wish to use daily log files instead of a single file, you should simply set the `log` value in your `config/app.php` configuration file:

    'log' => 'daily'

When using the `daily` log mode, Laravel will only retain five days of log files by default. If you want to adjust the number of retained files, you may add an optional `log_max_files` configuration value to your `app.php` configuration file:

    'log_max_files' => 30

#### Custom Monolog Configuration

If you would like to have complete control over how Monolog is configured for your application, you may use the application's `configureMonologUsing` method. You should place a call to this method in your `bootstrap/app.php` file right before the `$app` variable is returned by the file:

    $app->configureMonologUsing(function($monolog) {
        $monolog->pushHandler(...);
    });

    return $app;

By default, Laravel writes all log levels. In your production environment, you may wish to configure the default log level by adding the `log_level` option to your `app.php` configuration file. Laravel will then log all levels greater than or equal to the specified severity level. For example, a default `log_level` of `error` will log **error**, **critical**, **alert**, and **emergency** messages:

    'log_level' => env('APP_LOG_LEVEL', 'debug'),

<a name="the-exception-handler"></a>
## The Exception Handler

All exceptions are handled by the `App\Exceptions\Handler` class. This class contains two methods: `report` and `render`. We'll examine each of these methods in detail.

<a name="report-method"></a>
### The Report Method

The `report` method is used to log exceptions or send them to an external service like [BugSnag](https://bugsnag.com) or [Sentry](https://github.com/getsentry/sentry-laravel). By default, the `report` method simply passes the exception to the base class where the exception is logged. However, you are free to log exceptions however you wish.

For example, if you need to report different types of exceptions in different ways, you may use the PHP `instanceof` comparison operator:

    /**
     * Report or log an exception.
     *
     * This is a great spot to send exceptions to Sentry, Bugsnag, etc.
     *
     * @param  \Exception  $e
     * @return void
     */
    public function report(Exception $e)
    {
        if ($e instanceof CustomException) {
            //
        }

        return parent::report($e);
    }

#### Ignoring Exceptions By Type

The `$dontReport` property of the exception handler contains an array of exception types that will not be logged. By default, exceptions resulting from 404 errors are not written to your log files. You may add other exception types to this array as needed.

<a name="render-method"></a>
### The Render Method

The `render` method is responsible for converting a given exception into an HTTP response that should be sent back to the browser. By default, the exception is passed to the base class which generates a response for you. However, you are free to check the exception type or return your own custom response:

    /**
     * Render an exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Exception  $e
     * @return \Illuminate\Http\Response
     */
    public function render($request, Exception $e)
    {
        if ($e instanceof CustomException) {
            return response()->view('errors.custom', [], 500);
        }

        return parent::render($request, $e);
    }

<a name="http-exceptions"></a>
## HTTP Exceptions

Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401) or even a developer generated 500 error. In order to generate such a response from anywhere in your application, use the following:

    abort(404);

The `abort` method will immediately raise an exception which will be rendered by the exception handler. Optionally, you may provide the response text:

    abort(403, 'Unauthorized action.');

This method may be used at any time during the request's lifecycle.

<a name="custom-http-error-pages"></a>
### Custom HTTP Error Pages

Laravel makes it easy to return custom error pages for various HTTP status codes. For example, if you wish to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php`. This file will be served on all 404 errors generated by your application.

The exception raised by the abort method will be passed to the view as $exception, which allows you to present the user with the error message if needed. e.g.

    $exception->getMessage()

The views within this directory should be named to match the HTTP status code they correspond to.

<a name="logging"></a>
## Logging

The Laravel logging facilities provide a simple layer on top of the powerful [Monolog](http://github.com/seldaek/monolog) library. By default, Laravel is configured to create a log file for your application in the `storage/logs` directory. You may write information to the logs using the `Log` [facade](/docs/{{version}}/facades):

    <?php

    namespace App\Http\Controllers;

    use Log;
    use App\User;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            Log::info('Showing user profile for user: '.$id);

            return view('user.profile', ['user' => User::findOrFail($id)]);
        }
    }

The logger provides the eight logging levels defined in [RFC 5424](http://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**.

    Log::emergency($error);
    Log::alert($error);
    Log::critical($error);
    Log::error($error);
    Log::warning($error);
    Log::notice($error);
    Log::info($error);
    Log::debug($error);

#### Contextual Information

An array of contextual data may also be passed to the log methods. This contextual data will be formatted and displayed with the log message:

    Log::info('User failed to login.', ['id' => $user->id]);

#### Accessing The Underlying Monolog Instance

Monolog has a variety of additional handlers you may use for logging. If needed, you may access the underlying Monolog instance being used by Laravel:

    $monolog = Log::getMonolog();

# Logging

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Building Log Stacks](#building-log-stacks)
    - [Customizing Monolog](#customizing-monolog)
- [Writing Log Messages](#writing-log-messages)

<a name="introduction"></a>
## Introduction

To help you learn more of what's happening within your application, Laravel provides robust logging services that allow you to log messages and errors to files, the system error log, or even to Slack to notify your entire team.

Under the hood, Laravel utilizes the [Monolog](https://github.com/Seldaek/monolog) library, which provides support for a variety of powerful log handlers. Laravel makes it a cinch to configure these handlers, allowing you to mix and match them to customize your application's log handling.

<a name="configuration"></a>
## Configuration

All of the configuration for your application's logging system is housed in the `config/logging.php` configuration file. This file allows you to configure your application's log channels, so be sure to review each of the available channels and their options. Of course, we'll review a few common options below.

By default, Laravel will use the `stack` channel when logging messages. The `stack` channel type is used to aggregate multiple log handlers into a single channel. For more information on building stacks, check out the [documentation below](#building-log-stacks).

#### Customizing The Channel Name

By default, Monolog is instantiated with a "channel name" that matches the current environment, such as `production` or `local`. To change this value, add a `name` option to your channel's configuration:

    'stack' => [
        'driver' => 'stack',
        'name' => 'channel-name',
        'channels' => ['single', 'slack'],
    ],

<a name="building-log-stacks"></a>
### Building Log Stacks

Here Test

<a name="log-severity-levels"></a>
#### Log Severity Levels

Log messages may have different levels of severity. By default, Laravel typically writes all log levels to storage. However, in your production environment, you may wish to configure the minimum severity that should be logged.

Once this option has been configured, Laravel will log all levels greater than or equal to the specified severity. For example, a default `log_level` of `error` will log **error**, **critical**, **alert**, and **emergency** messages:

    'log_level' => env('APP_LOG_LEVEL', 'error'),

> {tip} Monolog recognizes the following severity levels - from least severe to most severe: `debug`, `info`, `notice`, `warning`, `error`, `critical`, `alert`, `emergency`.

<a name="customizing-monolog"></a>
### Customizing Monolog

If you would like to have complete control over how Monolog is configured for your application, you may use the application's `configureMonologUsing` method. You should place a call to this method in your `bootstrap/app.php` file right before the `$app` variable is returned by the file:

    $app->configureMonologUsing(function ($monolog) {
        $monolog->pushHandler(...);
    });

    return $app;

<a name="writing-log-messages"></a>
## Writing Log Messages

Laravel provides a simple abstraction layer on top of the powerful [Monolog](https://github.com/seldaek/monolog) library. By default, Laravel is configured to create a log file for your application in the `storage/logs` directory. You may write information to the logs using the `Log` [facade](/docs/{{version}}/facades):

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use Illuminate\Support\Facades\Log;
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

The logger provides the eight logging levels defined in [RFC 5424](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**.

    Log::emergency($message);
    Log::alert($message);
    Log::critical($message);
    Log::error($message);
    Log::warning($message);
    Log::notice($message);
    Log::info($message);
    Log::debug($message);

#### Contextual Information

An array of contextual data may also be passed to the log methods. This contextual data will be formatted and displayed with the log message:

    Log::info('User failed to login.', ['id' => $user->id]);

#### Accessing The Underlying Monolog Instance

Monolog has a variety of additional handlers you may use for logging. If needed, you may access the underlying Monolog instance being used by Laravel:

    $monolog = Log::getMonolog();

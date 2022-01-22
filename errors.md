# Error Handling

- [Introduction](#introduction)
- [Configuration](#configuration)
- [The Exception Handler](#the-exception-handler)
    - [Reporting Exceptions](#reporting-exceptions)
    - [Ignoring Exceptions By Type](#ignoring-exceptions-by-type)
    - [Rendering Exceptions](#rendering-exceptions)
    - [Reportable & Renderable Exceptions](#renderable-exceptions)
- [HTTP Exceptions](#http-exceptions)
    - [Custom HTTP Error Pages](#custom-http-error-pages)

<a name="introduction"></a>
## Introduction

When you start a new Laravel project, error and exception handling is already configured for you. The `App\Exceptions\Handler` class is where all exceptions thrown by your application are logged and then rendered to the user. We'll dive deeper into this class throughout this documentation.

<a name="configuration"></a>
## Configuration

The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file.

During local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the value is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.**

<a name="the-exception-handler"></a>
## The Exception Handler

<a name="reporting-exceptions"></a>
### Reporting Exceptions

All exceptions are handled by the `App\Exceptions\Handler` class. This class contains a `register` method where you may register custom exception reporting and rendering callbacks. We'll examine each of these concepts in detail. Exception reporting is used to log exceptions or send them to an external service like [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com) or [Sentry](https://github.com/getsentry/sentry-laravel). By default, exceptions will be logged based on your [logging](/docs/{{version}}/logging) configuration. However, you are free to log exceptions however you wish.

For example, if you need to report different types of exceptions in different ways, you may use the `reportable` method to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will deduce what type of exception the closure reports by examining the type-hint of the closure:

    use App\Exceptions\InvalidOrderException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->reportable(function (InvalidOrderException $e) {
            //
        });
    }

When you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application. If you wish to stop the propagation of the exception to the default logging stack, you may use the `stop` method when defining your reporting callback or return `false` from the callback:

    $this->reportable(function (InvalidOrderException $e) {
        //
    })->stop();

    $this->reportable(function (InvalidOrderException $e) {
        return false;
    });

> {tip} To customize the exception reporting for a given exception, you may also utilize [reportable exceptions](/docs/{{version}}/errors#renderable-exceptions).

<a name="global-log-context"></a>
#### Global Log Context

If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data by overriding the `context` method of your application's `App\Exceptions\Handler` class. This information will be included in every exception's log message written by your application:

    /**
     * Get the default context variables for logging.
     *
     * @return array
     */
    protected function context()
    {
        return array_merge(parent::context(), [
            'foo' => 'bar',
        ]);
    }

<a name="exception-log-context"></a>
#### Exception Log Context

While adding context to every log message can be useful, sometimes a particular exception may have unique context that you would like to include in your logs. By defining a `context` method on one of your application's custom exceptions, you may specify any data relevant to that exception that should be added to the exception's log entry:

    <?php

    namespace App\Exceptions;

    use Exception;

    class InvalidOrderException extends Exception
    {
        // ...

        /**
         * Get the exception's context information.
         *
         * @return array
         */
        public function context()
        {
            return ['order_id' => $this->orderId];
        }
    }

<a name="the-report-helper"></a>
#### The `report` Helper

Sometimes you may need to report an exception but continue handling the current request. The `report` helper function allows you to quickly report an exception via the exception handler without rendering an error page to the user:

    public function isValid($value)
    {
        try {
            // Validate the value...
        } catch (Throwable $e) {
            report($e);

            return false;
        }
    }

<a name="ignoring-exceptions-by-type"></a>
### Ignoring Exceptions By Type

When building your application, there will be some types of exceptions you simply want to ignore and never report. Your application's exception handler contains a `$dontReport` property which is initialized to an empty array. Any classes that you add to this property will never be reported; however, they may still have custom rendering logic:

    use App\Exceptions\InvalidOrderException;

    /**
     * A list of the exception types that should not be reported.
     *
     * @var array
     */
    protected $dontReport = [
        InvalidOrderException::class,
    ];

> {tip} Behind the scenes, Laravel already ignores some types of errors for you, such as exceptions resulting from 404 HTTP "not found" errors or 419 HTTP responses generated by invalid CSRF tokens.

<a name="rendering-exceptions"></a>
### Rendering Exceptions

By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this via the `renderable` method of your exception handler.

The closure passed to the `renderable` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will deduce what type of exception the closure renders by examining the type-hint of the closure:

    use App\Exceptions\InvalidOrderException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (InvalidOrderException $e, $request) {
            return response()->view('errors.invalid-order', [], 500);
        });
    }

You may also use the `renderable` method to override the rendering behavior for built-in Laravel or Symfony exceptions such as `NotFoundHttpException`. If the closure given to the `renderable` method does not return a value, Laravel's default exception rendering will be utilized:

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (NotFoundHttpException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'Record not found.'
                ], 404);
            }
        });
    }

<a name="renderable-exceptions"></a>
### Reportable & Renderable Exceptions

Instead of type-checking exceptions in the exception handler's `register` method, you may define `report` and `render` methods directly on your custom exceptions. When these methods exist, they will be automatically called by the framework:

    <?php

    namespace App\Exceptions;

    use Exception;

    class InvalidOrderException extends Exception
    {
        /**
         * Report the exception.
         *
         * @return bool|null
         */
        public function report()
        {
            //
        }

        /**
         * Render the exception into an HTTP response.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function render($request)
        {
            return response(...);
        }
    }

If your exception extends an exception that is already renderable, such as a built-in Laravel or Symfony exception, you may return `false` from the exception's `render` method to render the exception's default HTTP response:

    /**
     * Render the exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function render($request)
    {
        // Determine if the exception needs custom rendering...

        return false;
    }

If your exception contains custom reporting logic that is only necessary when certain conditions are met, you may need to instruct Laravel to sometimes report the exception using the default exception handling configuration. To accomplish this, you may return `false` from the exception's `report` method:

    /**
     * Report the exception.
     *
     * @return bool|null
     */
    public function report()
    {
        // Determine if the exception needs custom reporting...

        return false;
    }

> {tip} You may type-hint any required dependencies of the `report` method and they will automatically be injected into the method by Laravel's [service container](/docs/{{version}}/container).

<a name="http-exceptions"></a>
## HTTP Exceptions

Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401) or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper:

    abort(404);

<a name="custom-http-error-pages"></a>
### Custom HTTP Error Pages

Laravel makes it easy to display custom error pages for various HTTP status codes. For example, if you wish to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered on all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable:

    <h2>{{ $exception->getMessage() }}</h2>

You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking:

    php artisan vendor:publish --tag=laravel-errors

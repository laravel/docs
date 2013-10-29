# Errors & Logging

- [Error Detail](#error-detail)
- [Handling Errors](#handling-errors)
- [HTTP Exceptions](#http-exceptions)
- [Handling 404 Errors](#handling-404-errors)
- [Logging](#logging)

<a name="error-detail"></a>
## Error Detail

By default, error detail is enabled for your application. This means that when an error occurs you will be shown an error page with a detailed stack trace and error message. You may turn off error details by setting the `debug` option in your `app/config/app.php` file to `false`. **It is strongly recommended that you turn off error detail in a production environment.**

<a name="handling-errors"></a>
## Handling Errors

By default, the `app/start/global.php` file contains an error handler for all exceptions:

	App::error(function(Exception $exception)
	{
		Log::error($exception);
	});

This is the most basic error handler. However, you may specify more handlers if needed. Handlers are called based on the type-hint of the Exception they handle. For example, you may create a handler that only handles `RuntimeException` instances:

	App::error(function(RuntimeException $exception)
	{
		// Handle the exception...
	});

If an exception handler returns a response, that response will be sent to the browser and no other error handlers will be called:

	App::error(function(InvalidUserException $exception)
	{
		Log::error($exception);

		return 'Sorry! Something is wrong with this account!';
	});

To listen for PHP fatal errors, you may use the `App::fatal` method:

	App::fatal(function($exception)
	{
		//
	});

If you have several exception handlers, they should be defined from most generic to most specific. So, for example, a handler that handles all exceptions of type `Exception` should be defined before a custom exception type such as `Illuminate\Encryption\DecryptException`.

<a name="http-exceptions"></a>
## HTTP Exceptions

Exceptions in respect to HTTP, refer to errors that may occur during a client request. This may be a page not found error (404), an unauthorized error (401) or even a generated 500 error. In order to return such a response, use the following:

	App::abort(404, 'Page not found');

The first argument, is the HTTP status code, with the following being a custom message you'd like to show with the error.

In order to raise a 401 Unauthorized exception, just do the following:

	App::abort(401, 'You are not authorized.');

These exceptions can be executed at any time during the request's lifecycle.

<a name="handling-404-errors"></a>
## Handling 404 Errors

You may register an error handler that handles all "404 Not Found" errors in your application, allowing you to return custom 404 error pages:

	App::missing(function($exception)
	{
		return Response::view('errors.missing', array(), 404);
	});

<a name="logging"></a>
## Logging

The Laravel logging facilities provide a simple layer on top of the powerful [Monolog](http://github.com/seldaek/monolog). By default, Laravel is configured to create daily log files for your application, and these files are stored in `app/storage/logs`. You may write information to these logs like so:

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

The logger provides the seven logging levels defined in [RFC 5424](http://tools.ietf.org/html/rfc5424): **debug**, **info**, **notice**, **warning**, **error**, **critical**, and **alert**.

An array of contextual data may also be passed to the log methods:

	Log::info('Log message', array('context' => 'Other helpful information'));

Monolog has a variety of additional handlers you may use for logging. If needed, you may access the underlying Monolog instance being used by Laravel:

	$monolog = Log::getMonolog();

You may also register an event to catch all messages passed to the log:

**Registering A Log Listener**

	Log::listen(function($level, $message, $context)
	{
		//
	});

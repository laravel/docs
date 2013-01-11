# Errors & Logging

- [Error Detail](#error-detail)
- [Handling Errors](#handling-errors)
- [Handling 404 Errors](#handling-404-errors)
- [Logging](#logging)

## Error Detail

By default, error detail is enabled for your application. This means that when an error occurs you will be showed an error page with a detailed stack trace and error message. You may turn off error details by setting the `debug` option in your `app/config/app.php` file to `false`. **It is strongly recommend you turn off error detail in a production environment.**

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

<a name="handling-404-errors"></a>
## Handling 404 Errors

You may register an error handler that handles all "404 Not Found" errors in your application, allowing you to return custom 404 error pages:

	App::missing(function($exception)
	{
		return View::make('errors.missing');
	});

<a name="logging"></a>
## Logging

The Laravel logging facilities provide a simple layer on top of the powerful [Monolog](http://github.com/seldaek/monolog). By default, Laravel is configured to create daily log files for your application, and these files are stored in `app/storage/logs`. You may write information to these logs like so:

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

The logger provides the seven logging levels defined in [RFC 5424](http://tools.ietf.org/html/rfc5424): **debug**, **info**, **notice**, **warning**, **error**, **critical**, and **alert**.

Monolog has a variety of additional handlers you may use for logging. If needed, you may access the underlying Monolog instance being used by Laravel:

	$monolog = Log::getMonolog();

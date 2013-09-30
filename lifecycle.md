# Request Lifecycle

- [Overview](#overview)
- [Start Files](#start-files)
- [Application Events](#application-events)

<a name="overview"></a>
## Overview

The Laravel request lifecycle is fairly simple. A request enters your application and is dispatched to the appropriate route or controller. The response from that route is then sent back to the browser and displayed on the screen. Sometimes you may wish to do some processing before or after your routes are actually called. There are several opportunities to do this, two of which are "start" files and application events.

<a name="start-files"></a>
## Start Files

Your application's start files are stored at `app/start`. By default, three are included with your application: `global.php`, `local.php`, and `artisan.php`. For more information about `artisan.php`, refer to the documentation on the [Artisan command line](/docs/commands#registering-commands).

The `global.php` start file contains a few basic items by default, such as the registration of the [Logger](/docs/errors) and the inclusion of your `app/filters.php` file. However, you are free to add anything to this file that you wish. It will be automatically included on _every_ request to your application, regardless of environment. The `local.php` file, on the other hand, is only called when the application is executing in the `local` environment. For more information on environments, check out the [configuration](/docs/configuration) documentation.

Of course, if you have other environments in addition to `local`, you may create start files for those environments as well. They will be automatically included when your application is running in that environment.

<a name="application-events"></a>
## Application Events

You may also do pre and post request processing by registering `before`, `after`, `close`, `finish`, and `shutdown` application events:

**Registering Application Events**

	App::before(function($request)
	{
		//
	});

	App::after(function($request, $response)
	{
		//
	});

Listeners to these events will be run `before` and `after` each request to your application.

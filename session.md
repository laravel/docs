# Session

- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Flash Data](#flash-data)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)

<a name="configuration"></a>
## Configuration

Since HTTP driven applications are stateless, sessions provide a way to store information about the user across requests. Laravel ships with a variety of session back-ends available for use through a clean, unified API. Support for popular back-ends such as [Memcached](http://memcached.org), [Redis](http://redis.io), and databases is included out of the box.

The session configuration file is stored at `config/session.php`. Be sure to review the well documented options available to you in this file. By default, Laravel is configured to use the `file` session driver, which will work well for many applications. In production applications, you may consider using the `memcached` driver for even faster session performance.

The session `driver` defines where session data will be stored for each request. Laravel ships with several great drivers out of the box:

- `file` - sessions will be stored in `storage/framework/sessions`.
- `cookie` - sessions will be stored in secure, encrypted cookies.
- `database` - sessions will be stored in a database used by your application.
- `memcached` / `redis` - sessions will be stored in one of these fast, cached based stores.
- `array` - sessions will be stored in a simple PHP array and will not be persisted across requests.

> **Note:** The array driver is typically used for running [unit tests](/docs/{{version}}/testing) to prevent session data from persisting.

### Driver Prerequisites

#### Database

When using the `database` session driver, you will need to setup a table to contain the session items. Below is an example `Schema` declaration for the table:

	Schema::create('sessions', function ($table) {
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

You may use the `session:table` Artisan command to generate this migration for you!

	php artisan session:table

	composer dump-autoload

	php artisan migrate

#### Redis

Before using Redis sessions with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

### Other Session Considerations

The Laravel framework uses the `flash` session key internally, so you should not add an item to the session by that name.

If you need all stored session data to be encrypted, set the `encrypt` configuration option to `true`.

For security reasons Laravel reads session data at the beginning and writes it back at the end of each request. Avoid using session while there is possibility of multiple simultaneous requests from one user (such can occur during long-polling).

<a name="basic-usage"></a>
## Basic Usage

#### Accessing The Session

First, let's access the session. We can access the session instance via the HTTP request, which can be type-hinted on a controller method. Remember, controller method dependencies are injected via the Laravel [service container](/docs/{{version}}/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show the profile for the given user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile(Request $request, $id)
		{
			$value = $request->session()->get('key');

			//
		}
	}

Once you have access to the session instance, you may call a variety of functions to interact with the underlying data:

#### Storing An Item In The Session

	$request->session()->put('key', 'value');

	// Alternatively, you may use the global "session" helper function...
	session(['key' => 'value']);

#### Push A Value Onto An Array Session Value

	$request->session()->push('user.teams', 'developers');

#### Retrieving An Item From The Session

	$value = $request->session()->get('key');

	// Alternatively, you may use the global "session" helper function...
	$value = session('key');

#### Retrieving An Item Or Returning A Default Value

	$value = $request->session()->get('key', 'default');

	$value = $request->session()->get('key', function() {
		return 'default';
	});

#### Retrieving An Item And Forgetting It

	$value = $request->session()->pull('key', 'default');

#### Retrieving All Data From The Session

	$data = $request->session()->all();

#### Determining If An Item Exists In The Session

	if ($request->session()->has('users')) {
		//
	}

#### Removing An Item From The Session

	$request->session()->forget('key');

#### Removing All Items From The Session

	$request->session()->flush();

#### Regenerating The Session ID

	$request->session()->regenerate();

<a name="flash-data"></a>
## Flash Data

Sometimes you may wish to store items in the session only for the next request. You may do so using the `flash` method. Method stored in the session using this method will only be available during the subsequent HTTP request, and then will be deleted. Flash data is primarily useful for short-lived status messages:

	$request->session()->flash('status', 'Task was successful!');

#### Reflashing The Current Flash Data For Another Request

	$request->session()->reflash();

#### Reflashing Only A Subset Of Flash Data

	$request->session()->keep(['username', 'email']);

<a name="adding-custom-session-drivers"></a>
## Adding Custom Session Drivers

To add additional drivers to Laravel's session back-end, we will use the `extend` method on the `Session` [facade](/docs/{{version}}/session). We will call the `extend` method from the `boot` method of a [service provider](/docs/{{version}}/providers):

    <?php namespace App\Providers;

    use Session;
    use App\Extensions\MongoSessionStore;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
			Session::extend('mongo', function($app) {
				// Return implementation of SessionHandlerInterface...
				return new MongoSessionStore;
			});
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

### Writing The Session Extension

Note that your custom session driver should implement the `SessionHandlerInterface`. This interface contains just a few simple methods we need to implement. A stubbed MongoDB implementation would look something like this:

	class MongoHandler implements SessionHandlerInterface
	{
		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}
	}

Since these methods are not as readily understandable as the cache `StoreInterface`, let's quickly cover what each of the methods do:

- The `open` method would typically be used in file based session store systems. Since Laravel ships with a `file` session driver, you will almost never need to put anything in this method. You can leave it as an empty stub. It is simply a fact of poor interface design (which we'll discuss later) that PHP requires us to implement this method.
- The `close` method, like the `open` method, can also usually be disregarded. For most drivers, it is not needed.
- The `read` method should return the string version of the session data associated with the given `$sessionId`. There is no need to do any serialization or other encoding when retrieving or storing session data in your driver, as Laravel will perform the serialization for you.
- The `write` method should write the given `$data` string associated with the `$sessionId` to some persistent storage system, such as MongoDB, Dynamo, etc.
- The `destroy` method should remove the data associated with the `$sessionId` from persistent storage.
- The `gc` method should destroy all session data that is older than the given `$lifetime`, which is a UNIX timestamp. For self-expiring systems like Memcached and Redis, this method may be left empty.

Once the session driver has been registered, you may use the `mongo` driver in your `config/session.php` configuration file.

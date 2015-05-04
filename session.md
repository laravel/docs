# Session

- [Configuration](#configuration)
- [Session Usage](#session-usage)
- [Flash Data](#flash-data)
- [Database Sessions](#database-sessions)
- [Session Drivers](#session-drivers)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)

<a name="configuration"></a>
## Configuration

Since HTTP driven applications are stateless, sessions provide a way to store information about the user across requests. Laravel ships with a variety of session back-ends available for use through a clean, unified API. Support for popular back-ends such as [Memcached](http://memcached.org), [Redis](http://redis.io), and databases is included out of the box.

The session configuration is stored in `config/session.php`. Be sure to review the well documented options available to you in this file. By default, Laravel is configured to use the `file` session driver, which will work well for the majority of applications.

Before using Redis sessions with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

> **Note:** If you need all stored session data to be encrypted, set the `encrypt` configuration option to `true`.

> **Note:** When using the `cookie` session driver, you should **never** remove the `EncryptCookie` middleware from your HTTP kernel. If you remove this middleware, your application will be vulnerable to remote code injection.

#### Reserved Keys

The Laravel framework uses the `flash` session key internally, so you should not add an item to the session by that name.

<a name="session-usage"></a>
## Session Usage

The session may be accessed in several ways, via the HTTP request's `session` method, the `Session` facade, or the `session` helper function. When the `session` helper is called without arguments, it will return the entire session object. For example:

	session()->regenerate();

#### Storing An Item In The Session

	Session::put('key', 'value');

	session(['key' => 'value']);

#### Push A Value Onto An Array Session Value

	Session::push('user.teams', 'developers');

#### Retrieving An Item From The Session

	$value = Session::get('key');

	$value = session('key');

#### Retrieving An Item Or Returning A Default Value

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

#### Retrieving An Item And Forgetting It

	$value = Session::pull('key', 'default');

#### Retrieving All Data From The Session

	$data = Session::all();

#### Determining If An Item Exists In The Session

	if (Session::has('users'))
	{
		//
	}

#### Removing An Item From The Session

	Session::forget('key');

#### Removing All Items From The Session

	Session::flush();

#### Regenerating The Session ID

	Session::regenerate();

<a name="flash-data"></a>
## Flash Data

Sometimes you may wish to store items in the session only for the next request. You may do so using the `Session::flash` method:

	Session::flash('key', 'value');

#### Reflashing The Current Flash Data For Another Request

	Session::reflash();

#### Reflashing Only A Subset Of Flash Data

	Session::keep(['username', 'email']);

<a name="database-sessions"></a>
## Database Sessions

When using the `database` session driver, you will need to setup a table to contain the session items. Below is an example `Schema` declaration for the table:

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

Of course, you may use the `session:table` Artisan command to generate this migration for you!

	php artisan session:table

	composer dump-autoload

	php artisan migrate

<a name="session-drivers"></a>
## Session Drivers

The session "driver" defines where session data will be stored for each request. Laravel ships with several great drivers out of the box:

- `file` - sessions will be stored in `storage/framework/sessions`.
- `cookie` - sessions will be stored in secure, encrypted cookies.
- `database` - sessions will be stored in a database used by your application.
- `memcached` / `redis` - sessions will be stored in one of these fast, cached based stores.
- `array` - sessions will be stored in a simple PHP array and will not be persisted across requests.

> **Note:** The array driver is typically used for running [unit tests](/docs/{{version}}/testing), so no session data will be persisted.

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

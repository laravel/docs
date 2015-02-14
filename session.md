# Session

- [Configuration](#configuration)
- [Session Usage](#session-usage)
- [Flash Data](#flash-data)
- [Database Sessions](#database-sessions)
- [Session Drivers](#session-drivers)

<a name="configuration"></a>
## Configuration

Since HTTP driven applications are stateless, sessions provide a way to store information about the user across requests. Laravel ships with a variety of session back-ends available for use through a clean, unified API. Support for popular back-ends such as [Memcached](http://memcached.org), [Redis](http://redis.io), and databases is included out of the box.

The session configuration is stored in `config/session.php`. Be sure to review the well documented options available to you in this file. By default, Laravel is configured to use the `file` session driver, which will work well for the majority of applications.

Before using Redis sessions with Laravel, you will need to install the `predis/predis` package (~1.0) via Composer.

> **Note:** If you need all stored session data to be encrypted, set the `encrypt` configuration option to `true`.

#### Reserved Keys

The Laravel framework uses the `flash` session key internally, so you should not add an item to the session by that name.

<a name="session-usage"></a>
## Session Usage

#### Storing An Item In The Session

	// Using the Session Facade
	Session::put('key', 'value');

	// Using the session helper
	session(['key' => 'value']);

#### Push A Value Onto An Array Session Value

	// Using the Session Facade
	Session::push('user.teams', 'developers');

	// Using the session helper
	session()->push('user.teams', 'developers');

#### Retrieving An Item From The Session

	// Using the Session Facade
	$value = Session::get('key');

	// Using the session helper
	$value = session('key');

#### Retrieving An Item Or Returning A Default Value

	// Using the Session Facade
	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

	// Using the session helper
	$value = session('key', 'default');

	$value = session('key', function() { return 'default'; });

#### Retrieving An Item And Forgetting It

	// Using the Session Facade
	$value = Session::pull('key', 'default');

	// Using the session helper
	$value = session()->pull('key', 'default');

#### Retrieving All Data From The Session

	// Using the Session Facade
	$data = Session::all();

	// Using the session helper
	$data = session()->all();

#### Determining If An Item Exists In The Session

	// Using the Session Facade
	if (Session::has('users'))
	{
		//
	}

	// Using the session helper
	if (session()->has('users'))
	{
		//
	}

#### Removing An Item From The Session

	// Using the Session Facade
	Session::forget('key');

	// Using the session helper
	session()->forget('key');

#### Removing All Items From The Session

	// Using the Session Facade
	Session::flush();

	// Using the session helper
	session()->flush();

#### Regenerating The Session ID

	// Using the Session Facade
	Session::regenerate();

	// Using the session helper
	session()->regenerate();

<a name="flash-data"></a>
## Flash Data

Sometimes you may wish to store items in the session only for the next request. You may do so using the `Session::flash` method:

	// Using the Session Facade
	Session::flash('key', 'value');

	// Using the session helper
	session()->flash('key', 'value');

#### Reflashing The Current Flash Data For Another Request

	// Using the Session Facade
	Session::reflash();

	// Using the session helper
	session()->reflash();

#### Reflashing Only A Subset Of Flash Data

	// Using the Session Facade
	Session::keep(['username', 'email']);

	// Using the session helper
	session()->keep(['username', 'email']);

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

- `file` - sessions will be stored in `app/storage/sessions`.
- `cookie` - sessions will be stored in secure, encrypted cookies.
- `database` - sessions will be stored in a database used by your application.
- `memcached` / `redis` - sessions will be stored in one of these fast, cached based stores.
- `array` - sessions will be stored in a simple PHP array and will not be persisted across requests.

> **Note:** The array driver is typically used for running [unit tests](/docs/5.0/testing), so no session data will be persisted.

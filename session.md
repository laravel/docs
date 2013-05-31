# Session

- [Configuration](#configuration)
- [Session Usage](#session-usage)
- [Flash Data](#flash-data)
- [Database Sessions](#database-sessions)

<a name="configuration"></a>
## Configuration

Since HTTP driven applications are stateless, sessions provide a way to store information about the user across requests. Laravel ships with a variety of session back-ends available for use through a clean, unified API. Support for popular back-ends such as [Memcached](http://memcached.org), [Redis](http://redis.io), and databases is included out of the box.

The session configuration is stored in `app/config/session.php`. Be sure to review the well documented options available to you in this file. By default, Laravel is configured to use the `native` session driver, which will work well for the majority of applications.

<a name="session-usage"></a>
## Session Usage

<a name="storing-an-item-in-the-session"></a>
**Storing An Item In The Session**

	Session::put('key', 'value');

<a name="retrieving-an-item-from-the-session"></a>
**Retrieving An Item From The Session**

	$value = Session::get('key');

<a name="retrieving-an-item-or-returning-a-default-value"></a>
**Retrieving An Item Or Returning A Default Value**

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

<a name="determining-if-an-item-exists-in-the-session"></a>
**Determining If An Item Exists In The Session**

	if (Session::has('users'))
	{
		//
	}

<a name="removing-an-item-from-the-session"></a>
**Removing An Item From The Session**

	Session::forget('key');

<a name="removing-all-items-from-the-session"></a>
**Removing All Items From The Session**

	Session::flush();

<a name="regenerating-the-session-id"></a>
**Regenerating The Session ID**

	Session::regenerate();

<a name="flash-data"></a>
## Flash Data

Sometimes you may wish to store items in the session only for the next request. You may do so using the `Session::flash` method:

	Session::flash('key', 'value');

<a name="reflashing-the-current-flash-data-for-another-request"></a>
**Reflashing The Current Flash Data For Another Request**

	Session::reflash();

<a name="reflashing-only-a-subset-of-flash-data"></a>
**Reflashing Only A Subset Of Flash Data**

	Session::keep(array('username', 'email'));

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
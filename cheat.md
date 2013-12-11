# Cheat Sheet

- [Introduction](#introduction)
- [Artisan](#artisan)
- [Composer](#composer)

<a name="introduction"></a>
## Introduction

Laravel community member Jesse O'Brien created a terrific cheat sheet for the framework. In fact, it is so good we decided to integrate with the main documentation. Below you will find a quick reference guide for almost every method in Laravel.

<a name="artisan"></a>
## Artisan

	php artisan --help OR -h
	php artisan --quiet OR -q
	php artisan --version OR -V
	php artisan --no-interaction OR -n
	php artisan --ansi
	php artisan --no-ansi
	php artisan --env

	// -v|vv|vvv Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug
	php artisan --verbose

	php artisan changes
	php artisan clear-compiled
	php artisan down
	php artisan dump-autoload
	php artisan env
	php artisan help
	php artisan list
	php artisan migrate
	php artisan optimize
	php artisan routes
	php artisan serve
	php artisan tinker
	php artisan up
	php artisan workbench

	php artisan asset:publish [--bench[="vendor/package"]] [--path[="..."]] [package]
	php artisan auth:reminders
	php artisan cache:clear
	php artisan command:make name [--command[="..."]] [--path[="..."]] [--namespace[="..."]]
	php artisan config:publish
	php artisan controller:make [--bench="vendor/package"]
	php artisan db:seed [--class[="..."]] [--database[="..."]]
	php artisan key:generate
	php artisan migrate [--bench="vendor/package"] [--database[="..."]] [--path[="..."]] [--package[="..."]] [--pretend] [--seed]
	php artisan migrate:install [--database[="..."]]
	php artisan migrate:make name [--bench="vendor/package"] [--create] [--package[="..."]] [--path[="..."]] [--table[="..."]]
	php artisan migrate:refresh [--database[="..."]] [--seed]
	php artisan migrate:reset [--database[="..."]] [--pretend]
	php artisan migrate:rollback [--database[="..."]] [--pretend]
	php artisan queue:listen [--queue[="..."]] [--delay[="..."]] [--memory[="..."]] [--timeout[="..."]] [connection]
	php artisan queue:subscribe [--type[="..."]] queue url
	php artisan queue:work [--queue[="..."]] [--delay[="..."]] [--memory[="..."]] [--sleep] [connection]
	php artisan session:table
	php artisan view:publish [--path[="..."]] package

<a name="composer"></a>
## Composer

	composer create-project laravel/laravel folder_name
	composer install
	composer update
	composer dump-autoload [--optimize]
	composer self-update

<a name="routing"></a>
## Routing

	Route::get('foo', function() {});
	Route::get('foo', 'ControllerName@function');
	Route::controller('foo', 'FooController');

### Triggering Errors

	App::abort(404);
	App::missing(function($exception){});

### Route Parameters

	Route::get('foo/{bar}', function($bar) {});
	Route::get('foo/{bar?}', function($bar = 'bar') {});

### HTTP Verbs

	Route::any('foo', function() {});
	Route::post('foo', function() {});
	Route::put('foo', function() {});
	Route::patch('foo', function() {});
	Route::delete('foo', function() {});

	// RESTful actions...
	Route::resource('foo', 'FooController');

### Secure Routes

	Route::get('foo', array('https', function() {}));

### Route Constraints

	Route::get('foo/{bar}', function($bar) {})
		->where('bar', '[0-9]+');

	Route::get('foo/{bar}/{baz}', function($bar, $baz) {})
		->where(array('bar' => '[0-9]+', 'baz' => '[A-Za-z]'));

### Filters

	// Declare an auth filter...
	Route::filter('auth', function(){});

	// Register a class filter...
	Route::filter('foo', 'FooFilter');
 	Route::get('foo', array('before' => 'auth', function(){}));

	// Routes in this group are guarded by the 'auth' filter...
	Route::get('foo', array('before' => 'auth', function(){}));
	Route::group(array('before' => 'auth'), function(){});

	// Pattern filter...
	Route::when('foo/*', 'foo');

	// HTTP verb pattern...
	Route::when('foo/*', 'foo', array('post'));

### Named Routes

	Route::currentRouteName();
	Route::get('foo/bar', array('as' => 'foobar', function() {}));

### Route Prefixing

	// This route group will carry the prefix 'foo'...
	Route::group(array('prefix' => 'foo'), function() {})

### Sub-Domain Routing

	// The {sub} parameter will be passed to the closure...
	 Route::group(array('domain' => '{sub}.example.com'), function() {});

<a name="urls"></a>
## URLs

	URL::full();
	URL::current();
	URL::previous();
	URL::to('foo/bar', $parameters, $secure);
	URL::action('FooController@method', $parameters, $absolute);
	URL::route('foo', $parameters, $absolute);
	URL::secure('foo/bar', $parameters);
	URL::asset('css/foo.css', $secure);
	URL::secureAsset('css/foo.css');
	URL::isValidUrl('http://example.com');
	URL::getRequest();
	URL::setRequest($request);

<a name="events"></a>
## Events

	Event::fire('foo.bar', array($bar));
	Event::listen('foo.bar', function($bar) {});
	Event::listen('foo.*', function($bar) {});
	Event::listen('foo.bar', 'FooHandler', 10);
	Event::listen('foo.bar', 'BarHandler', 5);
	Event::listen('foor.bar', function($event) { return false; });
	Event::queue('foo', array($bar));
	Event::flusher('foo', function($bar) {});
	Event::flush('foo');
	Event::subscribe(new FooEventHandler);

<a name="database"></a>
## Database

	DB::connection('connection_name');
	DB::statement('drop table users');
	DB::listen(function($sql, $bindings, $time){ code_here; });
	DB::transaction(function(){ transaction_code_here; });

	// Cache a query for $time minutes...
	DB::table('users')->remember($time)->get();

	// Escape raw input...
	DB::raw('sql expression here');

### Selects

	DB::table('name')->get();
	DB::table('name')->distinct()->get();
	DB::table('name')->select('column as column_alias')->get();
	DB::table('name')->where('name', '=', 'John')->get();
	DB::table('name')->whereBetween('column', array(1, 100))->get();
	DB::table('name')->whereIn('column', array(1, 2, 3))->get();
	DB::table('name')->whereNotIn('column', array(1, 2, 3))->get();
	DB::table('name')->whereNull('column')->get();
	DB::table('name')->whereNotNull('column')->get();
	DB::table('name')->groupBy('column')->get();
	DB::table('name')->orderBy('column')->get();
	DB::table('name')->having('count', '>', 100)->get();
	DB::table('name')->skip(10)->take(5)->get();
	DB::table('name')->first();
	DB::table('name')->pluck('column');
	DB::table('name')->lists('column');

	// Joins...
	DB::table('name')->join('table', 'name.id', '=', 'table.id')
	    ->select('name.id', 'table.email');

### Inserts, Updates, Deletes

	DB::table('name')->insert(array('name' => 'John', 'email' => 'john@example.com'));
	DB::table('name')->insertGetId(array('name' => 'John', 'email' => 'john@example.com'));

	// Batch insert...
	DB::table('name')->insert(
		array('name' => 'John', 'email' => 'john@example.com')
		array('name' => 'James', 'email' => 'james@example.com')
	);

	// Update a record...
	DB::table('name')->where('name', '=', 'John')
		->update(array('email', 'john@example2.com'));

	// Delete everything from a table...
	DB::table('name')->delete();

	// Delete specific records...
	DB::table('name')->where('id', '>', '10')->delete();
	DB::table('name')->truncate();

### Aggregates

	DB::table('name')->count();
	DB::table('name')->max('column');
	DB::table('name')->min('column');
	DB::table('name')->avg('column');
	DB::table('name')->sum('column');
	DB::table('name')->increment('column');
	DB::table('name')->increment('column', $amount);
	DB::table('name')->decrement('column');
	DB::table('name')->decrement('column', $amount);

### Raw Expressions

	DB::select('select * from users where id = ?', array('value'));
	DB::table('name')->select(DB::raw('count(*) as count, column2'))->get();

<a name="eloquent"></a>
## Eloquent

	// Fill a model with an array of attributes. Beware of mass assignment!
	Model::fill($attributes);

	Model::create(array('key' => 'value'));
	Model::destroy(1);
	Model::all();
	Model::find(1);
	Model::where('foo', '=', 'bar')->count();
	Model::where('foo', '=', 'bar')->delete();
	Model::whereRaw('foo = bar and cars = 2', array(20))->get();
	Model::remember(5)->get();
	Model::remember(5, 'cache-key-name')->get();
	Model::on('connection-name')->find(1);
	Model::with('relation')->get();
	Model::all()->take(10);
	Model::all()->skip(10);

	// Find using dual primary key...
	Model::find(array('first', 'last'));

	// Throw an exception if not found...
	Model::findOrFail(1);

	// Find using dual primary key and throw exception if not found...
	Model::findOrFail(array('first', 'last'));
	Model::where('foo', '=', 'bar')->get();
	Model::where('foo', '=', 'bar')->first();

	// Throw an exception if not found...
	Model::where('foo', '=', 'bar')->firstOrFail();

### Soft Deletes

	Model::withTrashed()->where('cars', 2)->get();
	Model::withTrashed()->where('cars', 2)->restore();
	Model::where('cars', 2)->forceDelete();
	Model::onlyTrashed()->where('cars', 2)->get();

### Events

	Model::creating(function($model) {});
	Model::created(function($model) {});
	Model::updating(function($model) {});
	Model::updated(function($model) {});
	Model::saving(function($model) {});
	Model::saved(function($model) {});
	Model::deleting(function($model) {});
	Model::deleted(function($model) {});
	Model::restoring(function($model) {});
	Model::restored(function($model) {});
	Model::observe(new FooObserver);

### Configuration

	// Disables mass assignment exceptions from being thrown...
	Eloquent::unguard();

	// Renables any ability to throw mass assignment exceptions...
	Eloquent::reguard();

<a name="schema"></a>
## Schema

	Schema::create('table', function($table)
	{
	    $table->increments('id');
	});

	// Specify a Connection...
	Schema::connection('foo')->create('table', function($table){});

	// Update an existing table...
	Schema::table('table', function($table){});

	Schema::rename($from, $to);
	Schema::drop('table');
	Schema::dropIfExists('table');
	Schema::hasTable('table');
	Schema::hasColumn('table', 'column');

	$table->renameColumn('from', 'to');
	$table->dropColumn(string|array);
	$table->engine = 'InnoDB';

	// Only works on MySQL...
	$table->string('name')->after('email');

### Indexes

	$table->string('column')->unique();
	$table->primary('column');

	// Creates a dual primary key...
	$table->primary(array('first', 'last'));

	$table->unique('column');
	$table->unique('column', 'key_name');

	// Creates a dual unique index...
	$table->unique(array('first', 'last'));
	$table->unique(array('first', 'last'), 'key_name');

	$table->index('column');
	$table->index('column', 'key_name');

	// Creates a dual index...
	$table->index(array('first', 'last'));
	$table->index(array('first', 'last'), 'key_name');

	$table->dropPrimary('table_column_primary');
	$table->dropUnique('table_column_unique');
	$table->dropIndex('table_column_index');

### Foreign Keys

	$table->foreign('user_id')->references('id')->on('users');
	$table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
	$table->dropForeign('posts_user_id_foreign');

### Column Types

	$table->increments('id');
	$table->bigIncrements('id');
	$table->string('email');
	$table->string('name', 100);
	$table->integer('votes');
	$table->bigInteger('votes');
	$table->smallInteger('votes');
	$table->float('amount');
	$table->double('column', 15, 8);
	$table->decimal('amount', 5, 2);
	$table->boolean('confirmed');
	$table->date('created_at');
	$table->dateTime('created_at');
	$table->time('sunrise');
	$table->timestamp('added_on');
	$table->timestamps();
	$table->softDeletes();
	$table->text('description');
	$table->binary('data');
	$table->enum('choices', array('foo', 'bar'));
	->nullable()
	->default($value)
	->unsigned()

<a name="input"></a>
## Input

	Input::get('key');
	Input::get('key', 'default');
	Input::has('key');
	Input::all();
	Input::only('foo', 'bar');
	Input::except('foo');

### Session Input (Flash)

	// Flash input to the session...
	Input::flash();

	Input::flashOnly('foo', 'bar');
	Input::flashExcept('foo', 'baz');
	Input::old('key', 'default_value');

### Files

	Input::file('filename');
	Input::hasFile('filename');
	Input::file('name')->getRealPath();
	Input::file('name')->getClientOriginalName();
	Input::file('name')->getClientOriginalExtension();
	Input::file('name')->getSize();
	Input::file('name')->getMimeType();
	Input::file('name')->move($destinationPath);
	Input::file('name')->move($destinationPath, $fileName);

<a name="cache"></a>
## Cache

	Cache::put('key', 'value', $minutes);
	Cache::add('key', 'value', $minutes);
	Cache::forever('key', 'value');
	Cache::remember('key', $minutes, function(){ return 'value' });
	Cache::rememberForever('key', function(){ return 'value' });
	Cache::forget('key');
	Cache::has('key');
	Cache::get('key');
	Cache::get('key', 'default');
	Cache::get('key', function(){ return 'default'; });
	Cache::increment('key');
	Cache::increment('key', $amount);
	Cache::decrement('key');
	Cache::decrement('key', $amount);
	Cache::tags('group')->put('key', $value);
	Cache::tags('group', 'sub-group')->put('key', $value);
	Cache::tags('group')->get('key');
	Cache::tags('group', 'sub-group')->get('key');
	Cache::tags('group')->flush();

<a name="cookies"></a>
## Cookies

	Cookie::get('key');
	Cookie::forever('key', 'value');

	// Set a cookie before a response has been created...
	Cookie::queue('key', 'value', 'minutes');

	// Send a cookie with a response
	$response = Response::make('Hello World');
	$response->withCookie(Cookie::make('name', 'value', $minutes));

<a name="sessions"></a>
## Sessions

	Session::get('key');
	Session::get('key', 'default');
	Session::get('key', function() { return 'default'; });
	Session::put('key', 'value');
	Session::all();
	Session::has('key');
	Session::forget('key');
	Session::flush();
	Session::regenerate();
	Session::flash('key', 'value');
	Session::reflash();
	Session::keep(array('key1', 'key2'));

<a name="requests"></a>
## Requests

	Request::path();
	Request::is('foo/*');
	Request::url();
	Request::segment(1);
	Request::header('Content-Type');
	Request::server('PATH_INFO');
	Request::ajax();
	Request::secure();

<a name="responses"></a>
## Responses

	return Response::make($contents);
	return Response::make($contents, 200);
	return Response::json(array('key' => 'value'));
	return Response::download($filepath);
	return Response::download($filepath, $filename, $headers);

	// Create a JSONP response...
	return Response::json(array('key' => 'value'))
		->setCallback(Input::get('callback'));

	// Create a response and modify a header value...
	$response = Response::make($contents, 200);
	$response->header('Content-Type', 'application/json');
	return $response;

	// Attach a cookie to a response...
	return Response::make($content)
		->withCookie(Cookie::make('key', 'value'));

<a name="redirects"></a>
## Redirects

	return Redirect::to('foo/bar');
	return Redirect::to('foo/bar')->with('key', 'value');
	return Redirect::to('foo/bar')->withInput(Input::get());
	return Redirect::to('foo/bar')->withInput(Input::except('password'));
	return Redirect::to('foo/bar')->withErrors($validator);
	return Redirect::back();
	return Redirect::route('foobar');
	return Redirect::route('foobar', array('value'));
	return Redirect::route('foobar', array('key' => 'value'));
	return Redirect::action('FooController@index');
	return Redirect::action('FooController@baz', array('value'));
	return Redirect::action('FooController@baz', array('key' => 'value'));

	// If intended redirect is not defined, defaults to foo/bar...
	return Redirect::intended('foo/bar');

<a name="ioc"></a>
## IoC

	App::bind('foo', function($app) { return new Foo; });
	App::make('foo');
	App::make('FooBar');
	App::singleton('foo', function(){ return new Foo; });
	App::instance('foo', new Foo);
	App::bind('FooRepositoryInterface', 'BarRepository');
	App::register('FooServiceProvider');
	App::resolving(function($type, $object) {});
	App::resolvingAny(function($object) {});

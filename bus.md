# Command Bus

- [Introduction](#introduction)
- [Creating Commands](#creating-commands)
- [Dispatching Commands](#dispatching-commands)
- [Queued Commands](#queued-commands)
- [Command Pipeline](#command-pipeline)

<a name="introduction"></a>
## Introduction

The Laravel command bus provides a convenient method of encapsulating tasks your application needs to perform into simple, easy to understand "commands". To help us understand the purpose of commands, let's pretend we are building an application that allows users to purchase podcasts.

When a user purchases a podcast, there are a variety of things that need to happen. For example, we may need to charge the user's credit card, add a record to our database that represents the purchase, and send a confirmation e-mail of the purchase. Perhaps we also need to perform some kind of validation as to whether the user is allowed to purchase podcasts.

We could put all of this logic inside a controller method; however, this has several disadvantages. The first disadvantage is that our controller probably handles several other incoming HTTP actions, and including complicated logic in each controller method will soon bloat our controller and make it harder to read. Secondly, it is difficult to re-use the purchase podcast logic outside of the controller context. Thirdly, it is more difficult to unit-test the command as we must also generate a stub HTTP request and make a full request to the application to test the purchase podcast logic.

Instead of putting this logic in the controller, we may choose to encapsulate it within a "command" object, such as a `PurchasePodcast` command.

<a name="creating-commands"></a>
## Creating Commands

The Artisan CLI can generate new command classes using the `make:command` command:

	php artisan make:command PurchasePodcast

The newly generated class will be placed in the `app/Commands` directory. By default, the command contains two methods: the constructor and the `handle` method. Of course, the constructor allows you to pass any relevant objects to the command, while the `handle` method executes the command. For example:

	class PurchasePodcast extends Command implements SelfHandling {

		protected $user, $podcast;

		/**
		 * Create a new command instance.
		 *
		 * @return void
		 */
		public function __construct(User $user, Podcast $podcast)
		{
			$this->user = $user;
			$this->podcast = $podcast;
		}

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle()
		{
			// Handle the logic to purchase the podcast...

			event(new PodcastWasPurchased($this->user, $this->podcast));
		}

	}

The `handle` method may also type-hint dependencies, and they will be automatically injected by the [service container](/docs/{{version}}/container). For example:

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle(BillingGateway $billing)
		{
			// Handle the logic to purchase the podcast...
		}

<a name="dispatching-commands"></a>
## Dispatching Commands

So, once we have created a command, how do we dispatch it? Of course, we could call the `handle` method directly; however, dispatching the command through the Laravel "command bus" has several advantages which we will discuss later.

If you glance at your application's base controller, you will see the `DispatchesCommands` trait. This trait allows us to call the `dispatch` method from any of our controllers. For example:

	public function purchasePodcast($podcastId)
	{
		$this->dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);
	}

The command bus will take care of executing the command and calling the IoC container to inject any needed dependencies into the `handle` method.

You may add the `Illuminate\Foundation\Bus\DispatchesCommands` trait to any class you wish. If you would like to receive a command bus instance through the constructor of any of your classes, you may type-hint the `Illuminate\Contracts\Bus\Dispatcher` interface. Finally, you may also use the `Bus` facade to quickly dispatch commands:

		Bus::dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);

### Mapping Command Properties From Requests

It is very common to map HTTP request variables into commands. So, instead of forcing you to do this manually for each request, Laravel provides some helper methods to make it a cinch. Let's take a look at the `dispatchFrom` method available on the `DispatchesCommands` trait:

	$this->dispatchFrom('Command\Class\Name', $request);

This method will examine the constructor of the command class it is given, and then extract variables from the HTTP request (or any other `ArrayAccess` object) to fill the needed constructor parameters of the command. So, if our command class accepts a `firstName` variable in its constructor, the command bus will attempt to pull the `firstName` parameter from the HTTP request.

You may also pass an array as the third argument to the `dispatchFrom` method. This array will be used to fill any constructor parameters that are not available on the request:

	$this->dispatchFrom('Command\Class\Name', $request, [
		'firstName' => 'Taylor',
	]);

<a name="queued-commands"></a>
## Queued Commands

The command bus is not just for synchronous jobs that run during the current request cycle, but also serves as the primary way to build queued jobs in Laravel. So, how do we instruct command bus to queue our job for background processing instead of running it synchronously? It's easy. Firstly, when generating a new command, just add the `--queued` flag to the command:

	php artisan make:command PurchasePodcast --queued

As you will see, this adds a few more features to the command, namely the `Illuminate\Contracts\Queue\ShouldBeQueued` interface and the `SerializesModels` trait. These instruct the command bus to queue the command, as well as gracefully serialize and deserialize any Eloquent models your command stores as properties.

If you would like to convert an existing command into a queued command, simply implement the `Illuminate\Contracts\Queue\ShouldBeQueued` interface on the class manually. It contains no methods, and merely serves as a "marker interface" for the dispatcher.

Then, just write your command normally. When you dispatch it to the bus that bus will automatically queue the command for background processing. It doesn't get any easier than that.

For more information on interacting with queued commands, view the full [queue documentation](/docs/{{version}}/queues).

<a name="command-pipeline"></a>
## Command Pipeline

Before a command is dispatched to a handler, you may pass it through other classes in a "pipeline". Command pipes work just like HTTP middleware, except for your commands! For example, a command pipe could wrap the entire command operation within a database transaction, or simply log its execution.

To add a pipe to your bus, call the `pipeThrough` method of the dispatcher from your `App\Providers\BusServiceProvider::boot` method:

	$dispatcher->pipeThrough(['UseDatabaseTransactions', 'LogCommand']);

A command pipe is defined with a `handle` method, just like a middleware:

	class UseDatabaseTransactions {

		public function handle($command, $next)
		{
			return DB::transaction(function() use ($command, $next)
			{
				return $next($command);
			});
		}

	}

Command pipe classes are resolved through the [IoC container](/docs/{{version}}/container), so feel free to type-hint any dependencies you need within their constructors.

You may even define a `Closure` as a command pipe:

	$dispatcher->pipeThrough([function($command, $next)
	{
		return DB::transaction(function() use ($command, $next)
		{
			return $next($command);
		});
	}]);

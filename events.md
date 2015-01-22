# Events

- [Basic Usage](#basic-usage)
- [Wildcard Listeners](#wildcard-listeners)
- [Event Subscribers](#event-subscribers)

<a name="basic-usage"></a>
## Basic Usage

The Laravel `Event` class provides a simple observer implementation, allowing you to subscribe and listen for events in your application. Individual event classes for your application are typically stored in the `app/Events` directory, while their handlers are stored in `app/Handlers/Events`.

You can generate a new event class using the Artisan CLI tool:

	php artisan make:event PodcastWasPurchased

#### Subscribing To An Event

The `EventServiceProvider` included with your Laravel installation provides a convenient place to register all event handlers. The `listen` property contains an array of all events (keys) and their handlers (values). Of course, you may add as many events to this array as your application requires. For example, let's add our `PodcastWasPurchased` event:

	/**
	 * The event handler mappings for the application.
	 *
	 * @var array
	 */
	protected $listen = [
		'App\Events\PodcastWasPurchased' => [
			'App\Handlers\Events\EmailPurchaseConfirmation@handle',
		],
	];

To generate a handler for an event, use the `handler:event` Artisan CLI command:

	php artisan handler:event EmailPurchaseConfirmation --event=PodcastWasPurchased

#### Firing An Event

Now we are ready to fire our event:

	$response = Event::fire(new PodcastWasPurchased($podcast));

The `fire` method returns an array of responses that you can use to control what happens next in your application.

You may also use the `event` helper to fire an event:

	event(new PodcastWasPurchased($podcast));

#### Closure Listeners

You can even listen to events without creating a separate handler class at all. For example, in the `boot` method of your `EventServiceProvider`, you could do the following:

	Event::listen('App\Events\PodcastWasPurchased', function($event)
	{
		// Handle the event...
	});

#### Stopping The Propagation Of An Event

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so using by returning `false` from your handler:

	Event::listen('App\Events\PodcastWasPurchased', function($event)
	{
		// Handle the event...

		return false;
	});

<a name="event-subscribers"></a>
## Event Subscribers

#### Defining An Event Subscriber

Event subscribers are classes that may subscribe to multiple events from within the class itself. Subscribers should define a `subscribe` method, which will be passed an event dispatcher instance:

	class UserEventHandler {

		/**
		 * Handle user login events.
		 */
		public function onUserLogin($event)
		{
			//
		}

		/**
		 * Handle user logout events.
		 */
		public function onUserLogout($event)
		{
			//
		}

		/**
		 * Register the listeners for the subscriber.
		 *
		 * @param  Illuminate\Events\Dispatcher  $events
		 * @return array
		 */
		public function subscribe($events)
		{
			$events->listen('App\Events\UserLoggedIn', 'UserEventHandler@onUserLogin');

			$events->listen('App\Events\UserLoggedOut', 'UserEventHandler@onUserLogout');
		}

	}

#### Registering An Event Subscriber

Once the subscriber has been defined, it may be registered with the `Event` class.

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

You may also use the [Laravel IoC container](/docs/ioc) to resolve your subscriber. To do so, simply pass the name of your subscriber to the `subscribe` method:

	Event::subscribe('UserEventHandler');


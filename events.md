# Events

- [Basic Usage](#basic-usage)
- [Wildcard Listeners](#wildcard-listeners)
- [Using Classes As Listeners](#using-classes-as-listeners)
- [Queued Events](#queued-events)
- [Event Subscribers](#event-subscribers)

<a name="basic-usage"></a>
## Basic Usage

The Laravel `Event` class provides a simple observer implementation, allowing you to subscribe and listen for events in your application.

#### Subscribing To An Event

	Event::listen('auth.login', function($user)
	{
		$user->last_login = new DateTime;

		$user->save();
	});

#### Firing An Event

	$response = Event::fire('auth.login', array($user));

The `fire` method returns an array of responses that you can use to control what happens next in your application.

#### Subscribing To Events With Priority

You may also specify a priority when subscribing to events. Listeners with higher priority will be run first, while listeners that have the same priority will be run in order of subscription.

	Event::listen('auth.login', 'LoginHandler', 10);

	Event::listen('auth.login', 'OtherHandler', 5);

#### Stopping The Propagation Of An Event

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so using by returning `false` from your listener:

	Event::listen('auth.login', function($event)
	{
		// Handle the event...

		return false;
	});

### Where To Register Events

So, you know how to register events, but you may be wondering _where_ to register them. Don't worry, this is a common question. Unfortunately, it's a hard question to answer because you can register an event almost anywhere! But, here are some tips. Again, like most other bootstrapping code, you may register events in one of your `start` files such as `app/start/global.php`.

If your `start` files are getting too crowded, you could create a separate `app/events.php` file that is included from a `start` file. This is a simple solution that keeps your event registration cleanly separated from the rest of your bootstrapping.

If you prefer a class based approach, you may register your events in a [service provider](/docs/4.2/ioc#service-providers). Since none of these approaches is inherently "correct", choose an approach you feel comfortable with based on the size of your application.

<a name="wildcard-listeners"></a>
## Wildcard Listeners

#### Registering Wildcard Event Listeners

When registering an event listener, you may use asterisks to specify wildcard listeners:

	Event::listen('foo.*', function($param)
	{
		// Handle the event...
	});

This listener will handle all events that begin with `foo.`.

You may use the `Event::firing` method to determine exactly which event was fired:

	Event::listen('foo.*', function($param)
	{
		if (Event::firing() == 'foo.bar')
		{
			//
		}
	});

<a name="using-classes-as-listeners"></a>
## Using Classes As Listeners

In some cases, you may wish to use a class to handle an event rather than a Closure. Class event listeners will be resolved out of the [Laravel IoC container](/docs/4.2/ioc), providing you the full power of dependency injection on your listeners.

#### Registering A Class Listener

	Event::listen('auth.login', 'LoginHandler');

#### Defining An Event Listener Class

By default, the `handle` method on the `LoginHandler` class will be called:

	class LoginHandler {

		public function handle($data)
		{
			//
		}

	}

#### Specifying Which Method To Subscribe

If you do not wish to use the default `handle` method, you may specify the method that should be subscribed:

	Event::listen('auth.login', 'LoginHandler@onLogin');

<a name="queued-events"></a>
## Queued Events

#### Registering A Queued Event

Using the `queue` and `flush` methods, you may "queue" an event for firing, but not fire it immediately:

	Event::queue('foo', array($user));

You may run the "flusher" and flush all queued events using the `flush` method:

	Event::flush('foo');

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
			$events->listen('auth.login', 'UserEventHandler@onUserLogin');

			$events->listen('auth.logout', 'UserEventHandler@onUserLogout');
		}

	}

#### Registering An Event Subscriber

Once the subscriber has been defined, it may be registered with the `Event` class.

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

You may also use the [Laravel IoC container](/docs/4.2/ioc) to resolve your subscriber. To do so, simply pass the name of your subscriber to the `subscribe` method:

	Event::subscribe('UserEventHandler');


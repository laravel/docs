# Events

- [Basic Usage](#basic-usage)
- [Where To Register Events](#where-to-register)
- [Wildcard Listeners](#wildcard-listeners)
- [Using Classes As Listeners](#using-classes-as-listeners)
- [Queued Events](#queued-events)
- [Event Subscribers](#event-subscribers)

<a name="basic-usage"></a>
## Basic Usage

The Laravel `Event` class provides a simple observer implementation, allowing you to subscribe and listen for events in your application.

**Subscribing To An Event**

	Event::listen('user.login', function($user)
	{
		$user->last_login = new DateTime;

		$user->save();
	});

**Firing An Event**

	$event = Event::fire('user.login', array($user));

You may also specify a priority when subscribing to events. Listeners with higher priority will be run first, while listeners that have the same priority will be run in order of subscription.

**Subscribing To Events With Priority**

	Event::listen('user.login', 'LoginHandler', 10);

	Event::listen('user.login', 'OtherHandler', 5);

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so using by returning `false` from your listener:

**Stopping The Propagation Of An Event**

	Event::listen('user.login', function($event)
	{
		// Handle the event...

		return false;
	});

<a name="where-to-register"></a>
## Where To Register Events

So, you know how to register events, but you may be wondering _where_ to register them. Don't worry, this is a common question. Unfortunately, it's a hard question to answer because you can register an event almost anywhere! But, here are some tips. Again, like most other bootstrapping code, you may register events in one of your `start` files such as `app/start/global.php`.

If your `start` files are getting too crowded, you could create a separate `app/events.php` file that is included from a `start` file. This is a simple solution that keeps your event registration cleanly separated from the rest of your bootstrapping. If you prefer a class based approach, you may register your events in a [service provider](/docs/ioc#service-providers). Since none of these approaches is inherently "correct", choose an approach you feel comfortable with based on the size of your application.

<a name="wildcard-listeners"></a>
## Wildcard Listeners

When registering an event listener, you may use asterisks to specify wildcard listeners:

**Registering Wildcard Event Listeners**

	Event::listen('foo.*', function($param)
	{
		// Handle the event...
	});

This listener will handle all events that begin with `foo.`.

You may use the `Event::fired` method to determine exactly which event was fired:

	Event::listen('foo.*', function($param)
	{
		if (Event::firing() == 'foo.bar')
		{
			//
		}
	});

<a name="using-classes-as-listeners"></a>
## Using Classes As Listeners

In some cases, you may wish to use a class to handle an event rather than a Closure. Class event listeners will be resolved out of the [Laravel IoC container](/docs/ioc), providing you the full power of dependency injection on your listeners.

**Registering A Class Listener**

	Event::listen('user.login', 'LoginHandler');

By default, the `handle` method on the `LoginHandler` class will be called:

**Defining An Event Listener Class**

	class LoginHandler {

		public function handle($data)
		{
			//
		}

	}

If you do not wish to use the default `handle` method, you may specify the method that should be subscribed:

**Specifying Which Method To Subscribe**

	Event::listen('user.login', 'LoginHandler@onLogin');

<a name="queued-events"></a>
## Queued Events

Using the `queue` and `flush` methods, you may "queue" an event for firing, but not fire it immediately:

**Registering A Queued Event**

	Event::queue('foo', array($user));

**Registering An Event Flusher**

	Event::flusher('foo', function($user)
	{
		//
	});

Finally, you may run the "flusher" and flush all queued events using the `flush` method:

	Event::flush('foo');

<a name="event-subscribers"></a>
## Event Subscribers

Event subscribers are classes that may subscribe to multiple events from within the class itself. Subscribers should define a `subscribe` method, which will be passed an event dispatcher instance:

**Defining An Event Subscriber**

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
			$events->listen('user.login', 'UserEventHandler@onUserLogin');

			$events->listen('user.logout', 'UserEventHandler@onUserLogout');
		}

	}

Once the subscriber has been defined, it may be registered with the `Event` class.

**Registering An Event Subscriber**

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

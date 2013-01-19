# Events

- [Basic Usage](#basic-usage)
- [Using Classes As Listeners](#using-classes-as-listeners)
- [Event Subscribers](#event-subscribers)

<a name="basic-usage"></a>
## Basic Usage

The Laravel `Event` class provides a simple observer implementation, allowing you to subscribe and listen for events in your application. The Laravel event facilities extend the `Symfony\Component\EventDispatcher\EventDispatcher` class.

**Subscribing To An Event**

	Event::listen('user.login', function($event)
	{
		$event->user->last_login = new DateTime;

		$event->user->save();
	});

**Firing An Event**

	$event = Event::fire('user.login', array('user' => $user));

Note that the `Event::fire` method returns an `Event` object, allowing you to inspect the event payload after the listeners have been called.

You may also specify a priority when subscribing to events. Listeners with higher priority will be run first, while listeners that have the same priority will be run in order of subscription.

**Subscribing To Events With Priority**

	Event::listen('user.login', 'LoginHandler', 10);

	Event::listen('user.login', 'OtherHandler', 5);

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so using the `$event->stop()` method.

**Stopping The Propagation Of An Event**

	Event::listen('user.login', function($event)
	{
		// Handle the event...

		$event->stop();
	});

<a name="using-classes-as-listeners"></a>
## Using Classes As Listeners

In some case, you may wish to use a class to handle an event rather than a Closure. Class event listeners will be resolved out of the [Laravel IoC container](/docs/ioc), providing you the full power of dependency injection on your listeners.

**Registering A Class Listener**

	Event::listen('user.login', 'LoginHandler');

By default, the `handle` method on the `LoginHandler` class will be called:

**Defining An Event Listener Class**

	class LoginHandler {

		public function handle($event)
		{
			//
		}

	}

If you do not wish to use the default `handle` method, you may specify the method that should be subscribed:

**Specifying Which Method To Subscribe**

	Event::listen('user.login', 'LoginHandler@onLogin');

<a name="event-subscribers"></a>
## Event Subscribers

Event subscribers are classes that may subscribe to multiple events from within the class itself. Subscribers should extend the `EventSubscriber` class and define a `subscribes` method.

**Defining An Event Subscriber**

	class UserEventHandler extends EventSubscriber {

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
		 * @return array
		 */
		public static function subscribes()
		{
			return array(
				'user.login' => array(
					array('onUserLogin', 10),
				),
				'user.logout' => array(
					array('onUserLogout', 10),
				),
			);
		}

	}

Once the subscriber has been defined, it may be registered with the `Event` class.

**Registering An Event Subscriber**

	$subscriber = new UserEventHandler();
	Event::subscribe($subscriber);

**Removing An Event Subscriber**

	Event::unsubscribe($subscriber);
	
The instance that was passed to the `subscribe()` method may also be passed to the `unsubscribe()` method to remove it.

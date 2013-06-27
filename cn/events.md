# 事件

- [基本用法](#basic-usage)
- [利用通配符匹配多个事件](#wildcard-listeners)
- [使用类作为监听器](#using-classes-as-listeners)
- [事件队列](#queued-events)
- [事件订阅者](#event-subscribers)

<a name="basic-usage"></a>
## 基本用法

Laravel中的`Event`类实现了简单的观察者模式，允许你在应用程序中订阅和监听事件。

**订阅事件**

	Event::listen('user.login', function($user)
	{
		$user->last_login = new DateTime;

		$user->save();
	});

**触发事件**

	$event = Event::fire('user.login', array($user));

你也可以在订阅事件时指定优先级。优先级高的监听器将会被优先执行，相同优先级的将被按照订阅顺序执行。

**带有优先级的事件订阅**

	Event::listen('user.login', 'LoginHandler', 10);

	Event::listen('user.login', 'OtherHandler', 5);

如果希望阻止事件传播到其他监听器，只需让监听器返回`false`即可实现：

**阻止事件传播**

	Event::listen('user.login', function($event)
	{
		// Handle the event...

		return false;
	});

<a name="wildcard-listeners"></a>
## 利用通配符匹配多个事件

注册事件监听器时，可以使用星号匹配多个事件进行监听：

**注册多个事件的监听器**

	Event::listen('foo.*', function($param, $event)
	{
		// Handle the event...
	});

该监听器将会处理所有以`foo.`开始的事件。注意：完整的事件名将以事件处理器的最后一个参数传入。

<a name="using-classes-as-listeners"></a>
## 使用类作为监听器

在某些情况下，你可能希望使用类来代替闭包处理事件。类事件监听器（Class event listener）通过 [Laravel IoC 容器](/docs/ioc)实现，为监听器提供了强大的依赖注入的能力。

**注册一个类监事件听器**

	Event::listen('user.login', 'LoginHandler');

默认情况下，`LoginHandler`类的`handle`方法将被调用：

**定义一个事件监听器类**

	class LoginHandler {

		public function handle($data)
		{
			//
		}

	}

如果你不想使用默认的`handle`方法，你可以在订阅时指定方法：

**指定实现订阅的方法**

	Event::listen('user.login', 'LoginHandler@onLogin');

<a name="queued-events"></a>
## 事件队列

使用`queue`和`flush`方法，可以将事件放入"队列"中，而不是立刻执行：


**向事件队列中添加一个事件**

	Event::queue('foo', array($user));

**注册一个事件清除器**

	Event::flusher('foo', function($user)
	{
		//
	});

最后，你可以使用`flush`方法清除掉队列中的所有事件：

	Event::flush('foo');

<a name="event-subscribers"></a>
## 事件订阅者

事件订阅者类可以在其自身内部订阅多个事件。并且事件订阅者应该定义`subscribe`方法，并接收一个事件调度器实例作为参数：

**定义一个事件订阅者**

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

一旦定义了事件订阅者，就可以使用`Event`类进行注册。

**注册一个事件订阅者**

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

译者：王赛  [（Bootstrap中文网）](http://www.bootcss.com)
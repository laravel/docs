# Events

- [Introduction](#introduction)
- [Registering Events & Listeners](#registering-events-and-listeners)
    - [Generating Events & Listeners](#generating-events-and-listeners)
    - [Manually Registering Events](#manually-registering-events)
    - [Event Discovery](#event-discovery)
- [Defining Events](#defining-events)
- [Defining Listeners](#defining-listeners)
- [Queued Event Listeners](#queued-event-listeners)
    - [Manually Interacting With The Queue](#manually-interacting-with-the-queue)
    - [Queued Event Listeners & Database Transactions](#queued-event-listeners-and-database-transactions)
    - [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
- [Event Subscribers](#event-subscribers)
    - [Writing Event Subscribers](#writing-event-subscribers)
    - [Registering Event Subscribers](#registering-event-subscribers)

<a name="introduction"></a>
## Introduction

Laravel's events provide a simple observer pattern implementation, allowing you to subscribe and listen for various events that occur within your application. Event classes are typically stored in the `app/Events` directory, while their listeners are stored in `app/Listeners`. Don't worry if you don't see these directories in your application as they will be created for you as you generate events and listeners using Artisan console commands.

Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other. For example, you may wish to send a Slack notification to your user each time an order has shipped. Instead of coupling your order processing code to your Slack notification code, you can raise an `App\Events\OrderShipped` event which a listener can receive and use to dispatch a Slack notification.

<a name="registering-events-and-listeners"></a>
## Registering Events & Listeners

The `App\Providers\EventServiceProvider` included with your Laravel application provides a convenient place to register all of your application's event listeners. The `listen` property contains an array of all events (keys) and their listeners (values). You may add as many events to this array as your application requires. For example, let's add an `OrderShipped` event:

    use App\Events\OrderShipped;
    use App\Listeners\SendShipmentNotification;

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        OrderShipped::class => [
            SendShipmentNotification::class,
        ],
    ];

> **Note**  
> The `event:list` command may be used to display a list of all events and listeners registered by your application.

<a name="generating-events-and-listeners"></a>
### Generating Events & Listeners

Of course, manually creating the files for each event and listener is cumbersome. Instead, add listeners and events to your `EventServiceProvider` and use the `event:generate` Artisan command. This command will generate any events or listeners that are listed in your `EventServiceProvider` that do not already exist:

```shell
php artisan event:generate
```

Alternatively, you may use the `make:event` and `make:listener` Artisan commands to generate individual events and listeners:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### Manually Registering Events

Typically, events should be registered via the `EventServiceProvider` `$listen` array; however, you may also register class or closure based event listeners manually in the `boot` method of your `EventServiceProvider`:

    use App\Events\PodcastProcessed;
    use App\Listeners\SendPodcastNotification;
    use Illuminate\Support\Facades\Event;

    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(
            PodcastProcessed::class,
            [SendPodcastNotification::class, 'handle']
        );

        Event::listen(function (PodcastProcessed $event) {
            // ...
        });
    }

<a name="queuable-anonymous-event-listeners"></a>
#### Queueable Anonymous Event Listeners

When registering closure based event listeners manually, you may wrap the listener closure within the `Illuminate\Events\queueable` function to instruct Laravel to execute the listener using the [queue](/docs/{{version}}/queues):

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;

    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(queueable(function (PodcastProcessed $event) {
            // ...
        }));
    }

Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener:

    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    })->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));

If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener. This closure will receive the event instance and the `Throwable` instance that caused the listener's failure:

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;
    use Throwable;

    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    })->catch(function (PodcastProcessed $event, Throwable $e) {
        // The queued listener failed...
    }));

<a name="wildcard-event-listeners"></a>
#### Wildcard Event Listeners

You may even register listeners using the `*` as a wildcard parameter, allowing you to catch multiple events on the same listener. Wildcard listeners receive the event name as their first argument and the entire event data array as their second argument:

    Event::listen('event.*', function (string $eventName, array $data) {
        // ...
    });

<a name="event-discovery"></a>
### Event Discovery

Instead of registering events and listeners manually in the `$listen` array of the `EventServiceProvider`, you can enable automatic event discovery. When event discovery is enabled, Laravel will automatically find and register your events and listeners by scanning your application's `Listeners` directory. In addition, any explicitly defined events listed in the `EventServiceProvider` will still be registered.

Laravel finds event listeners by scanning the listener classes using PHP's reflection services. When Laravel finds any listener class method that begins with `handle` or `__invoke`, Laravel will register those methods as event listeners for the event that is type-hinted in the method's signature:

    use App\Events\PodcastProcessed;

    class SendPodcastNotification
    {
        /**
         * Handle the given event.
         */
        public function handle(PodcastProcessed $event): void
        {
            // ...
        }
    }

Event discovery is disabled by default, but you can enable it by overriding the `shouldDiscoverEvents` method of your application's `EventServiceProvider`:

    /**
     * Determine if events and listeners should be automatically discovered.
     */
    public function shouldDiscoverEvents(): bool
    {
        return true;
    }

By default, all listeners within your application's `app/Listeners` directory will be scanned. If you would like to define additional directories to scan, you may override the `discoverEventsWithin` method in your `EventServiceProvider`:

    /**
     * Get the listener directories that should be used to discover events.
     *
     * @return array<int, string>
     */
    protected function discoverEventsWithin(): array
    {
        return [
            $this->app->path('Listeners'),
        ];
    }

<a name="event-discovery-in-production"></a>
#### Event Discovery In Production

In production, it is not efficient for the framework to scan all of your listeners on every request. Therefore, during your deployment process, you should run the `event:cache` Artisan command to cache a manifest of all of your application's events and listeners. This manifest will be used by the framework to speed up the event registration process. The `event:clear` command may be used to destroy the cache.

<a name="defining-events"></a>
## Defining Events

An event class is essentially a data container which holds the information related to the event. For example, let's assume an `App\Events\OrderShipped` event receives an [Eloquent ORM](/docs/{{version}}/eloquent) object:

    <?php

    namespace App\Events;

    use App\Models\Order;
    use Illuminate\Broadcasting\InteractsWithSockets;
    use Illuminate\Foundation\Events\Dispatchable;
    use Illuminate\Queue\SerializesModels;

    class OrderShipped
    {
        use Dispatchable, InteractsWithSockets, SerializesModels;

        /**
         * The order instance.
         *
         * @var \App\Models\Order
         */
        public $order;

        /**
         * Create a new event instance.
         */
        public function __construct(Order $order)
        {
            $this->order = $order;
        }
    }

As you can see, this event class contains no logic. It is a container for the `App\Models\Order` instance that was purchased. The `SerializesModels` trait used by the event will gracefully serialize any Eloquent models if the event object is serialized using PHP's `serialize` function, such as when utilizing [queued listeners](#queued-event-listeners).

<a name="defining-listeners"></a>
## Defining Listeners

Next, let's take a look at the listener for our example event. Event listeners receive event instances in their `handle` method. The `event:generate` and `make:listener` Artisan commands will automatically import the proper event class and type-hint the event on the `handle` method. Within the `handle` method, you may perform any actions necessary to respond to the event:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;

    class SendShipmentNotification
    {
        /**
         * Create the event listener.
         */
        public function __construct()
        {
            // ...
        }

        /**
         * Handle the event.
         */
        public function handle(OrderShipped $event): void
        {
            // Access the order using $event->order...
        }
    }

> **Note**  
> Your event listeners may also type-hint any dependencies they need on their constructors. All event listeners are resolved via the Laravel [service container](/docs/{{version}}/container), so dependencies will be injected automatically.

<a name="stopping-the-propagation-of-an-event"></a>
#### Stopping The Propagation Of An Event

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method.

<a name="queued-event-listeners"></a>
## Queued Event Listeners

Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/{{version}}/queues) and start a queue worker on your server or local development environment.

To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `event:generate` and `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        // ...
    }

That's it! Now, when an event handled by this listener is dispatched, the listener will automatically be queued by the event dispatcher using Laravel's [queue system](/docs/{{version}}/queues). If no exceptions are thrown when the listener is executed by the queue, the queued job will automatically be deleted after it has finished processing.

<a name="customizing-the-queue-connection-queue-name"></a>
#### Customizing The Queue Connection & Queue Name

If you would like to customize the queue connection, queue name, or queue delay time of an event listener, you may define the `$connection`, `$queue`, or `$delay` properties on your listener class:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        /**
         * The name of the connection the job should be sent to.
         *
         * @var string|null
         */
        public $connection = 'sqs';

        /**
         * The name of the queue the job should be sent to.
         *
         * @var string|null
         */
        public $queue = 'listeners';

        /**
         * The time (seconds) before the job should be processed.
         *
         * @var int
         */
        public $delay = 60;
    }

If you would like to define the listener's queue connection or queue name at runtime, you may define `viaConnection` or `viaQueue` methods on the listener:

    /**
     * Get the name of the listener's queue connection.
     */
    public function viaConnection(): string
    {
        return 'sqs';
    }

    /**
     * Get the name of the listener's queue.
     */
    public function viaQueue(): string
    {
        return 'listeners';
    }

<a name="conditionally-queueing-listeners"></a>
#### Conditionally Queueing Listeners

Sometimes, you may need to determine whether a listener should be queued based on some data that are only available at runtime. To accomplish this, a `shouldQueue` method may be added to a listener to determine whether the listener should be queued. If the `shouldQueue` method returns `false`, the listener will not be executed:

    <?php

    namespace App\Listeners;

    use App\Events\OrderCreated;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class RewardGiftCard implements ShouldQueue
    {
        /**
         * Reward a gift card to the customer.
         */
        public function handle(OrderCreated $event): void
        {
            // ...
        }

        /**
         * Determine whether the listener should be queued.
         */
        public function shouldQueue(OrderCreated $event): bool
        {
            return $event->order->subtotal >= 5000;
        }
    }

<a name="manually-interacting-with-the-queue"></a>
### Manually Interacting With The Queue

If you need to manually access the listener's underlying queue job's `delete` and `release` methods, you may do so using the `Illuminate\Queue\InteractsWithQueue` trait. This trait is imported by default on generated listeners and provides access to these methods:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        /**
         * Handle the event.
         */
        public function handle(OrderShipped $event): void
        {
            if (true) {
                $this->release(30);
            }
        }
    }

<a name="queued-event-listeners-and-database-transactions"></a>
### Queued Event Listeners & Database Transactions

When queued listeners are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your listener depends on these models, unexpected errors can occur when the job that dispatches the queued listener is processed.

If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued listener should be dispatched after all open database transactions have been committed by defining an `$afterCommit` property on the listener class:

    <?php

    namespace App\Listeners;

    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        public $afterCommit = true;
    }

> **Note**  
> To learn more about working around these issues, please review the documentation regarding [queued jobs and database transactions](/docs/{{version}}/queues#jobs-and-database-transactions).

<a name="handling-failed-jobs"></a>
### Handling Failed Jobs

Sometimes your queued event listeners may fail. If the queued listener exceeds the maximum number of attempts as defined by your queue worker, the `failed` method will be called on your listener. The `failed` method receives the event instance and the `Throwable` that caused the failure:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;
    use Throwable;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        /**
         * Handle the event.
         */
        public function handle(OrderShipped $event): void
        {
            // ...
        }

        /**
         * Handle a job failure.
         */
        public function failed(OrderShipped $event, Throwable $exception): void
        {
            // ...
        }
    }

<a name="specifying-queued-listener-maximum-attempts"></a>
#### Specifying Queued Listener Maximum Attempts

If one of your queued listeners is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a listener may be attempted.

You may define a `$tries` property on your listener class to specify how many times the listener may be attempted before it is considered to have failed:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        /**
         * The number of times the queued listener may be attempted.
         *
         * @var int
         */
        public $tries = 5;
    }

As an alternative to defining how many times a listener may be attempted before it fails, you may define a time at which the listener should no longer be attempted. This allows a listener to be attempted any number of times within a given time frame. To define the time at which a listener should no longer be attempted, add a `retryUntil` method to your listener class. This method should return a `DateTime` instance:

    use DateTime;

    /**
     * Determine the time at which the listener should timeout.
     */
    public function retryUntil(): DateTime
    {
        return now()->addMinutes(5);
    }

<a name="dispatching-events"></a>
## Dispatching Events

To dispatch an event, you may call the static `dispatch` method on the event. This method is made available on the event by the `Illuminate\Foundation\Events\Dispatchable` trait. Any arguments passed to the `dispatch` method will be passed to the event's constructor:

    <?php

    namespace App\Http\Controllers;

    use App\Events\OrderShipped;
    use App\Http\Controllers\Controller;
    use App\Models\Order;
    use Illuminate\Http\Request;
    use Illuminate\Http\Response;

    class OrderShipmentController extends Controller
    {
        /**
         * Ship the given order.
         */
        public function store(Request $request): Response
        {
            $order = Order::findOrFail($request->order_id);

            // Order shipment logic...

            OrderShipped::dispatch($order);

            return response()->noContent();
        }
    }
    
 If you would like to conditionally dispatch an event, you may use the `dispatchIf` and `dispatchUnless` methods:

    OrderShipped::dispatchIf($condition, $order);

    OrderShipped::dispatchUnless($condition, $order);

> **Note**  
> When testing, it can be helpful to assert that certain events were dispatched without actually triggering their listeners. Laravel's [built-in testing helpers](/docs/{{version}}/mocking#event-fake) makes it a cinch.

<a name="event-subscribers"></a>
## Event Subscribers

<a name="writing-event-subscribers"></a>
### Writing Event Subscribers

Event subscribers are classes that may subscribe to multiple events from within the subscriber class itself, allowing you to define several event handlers within a single class. Subscribers should define a `subscribe` method, which will be passed an event dispatcher instance. You may call the `listen` method on the given dispatcher to register event listeners:

    <?php

    namespace App\Listeners;

    use Illuminate\Auth\Events\Login;
    use Illuminate\Auth\Events\Logout;
    use Illuminate\Events\Dispatcher;

    class UserEventSubscriber
    {
        /**
         * Handle user login events.
         */
        public function handleUserLogin(string $event): void {}

        /**
         * Handle user logout events.
         */
        public function handleUserLogout(string $event): void {}

        /**
         * Register the listeners for the subscriber.
         */
        public function subscribe(Dispatcher $events): void
        {
            $events->listen(
                Login::class,
                [UserEventSubscriber::class, 'handleUserLogin']
            );

            $events->listen(
                Logout::class,
                [UserEventSubscriber::class, 'handleUserLogout']
            );
        }
    }

If your event listener methods are defined within the subscriber itself, you may find it more convenient to return an array of events and method names from the subscriber's `subscribe` method. Laravel will automatically determine the subscriber's class name when registering the event listeners:

    <?php

    namespace App\Listeners;

    use Illuminate\Auth\Events\Login;
    use Illuminate\Auth\Events\Logout;
    use Illuminate\Events\Dispatcher;

    class UserEventSubscriber
    {
        /**
         * Handle user login events.
         */
        public function handleUserLogin(string $event): void {}

        /**
         * Handle user logout events.
         */
        public function handleUserLogout(string $event): void {}

        /**
         * Register the listeners for the subscriber.
         *
         * @return array<string, string>
         */
        public function subscribe(Dispatcher $events): array
        {
            return [
                Login::class => 'handleUserLogin',
                Logout::class => 'handleUserLogout',
            ];
        }
    }

<a name="registering-event-subscribers"></a>
### Registering Event Subscribers

After writing the subscriber, you are ready to register it with the event dispatcher. You may register subscribers using the `$subscribe` property on the `EventServiceProvider`. For example, let's add the `UserEventSubscriber` to the list:

    <?php

    namespace App\Providers;

    use App\Listeners\UserEventSubscriber;
    use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

    class EventServiceProvider extends ServiceProvider
    {
        /**
         * The event listener mappings for the application.
         *
         * @var array
         */
        protected $listen = [
            // ...
        ];

        /**
         * The subscriber classes to register.
         *
         * @var array
         */
        protected $subscribe = [
            UserEventSubscriber::class,
        ];
    }

# Mocking

- [Introduction](#introduction)
- [Events](#mocking-events)
    - [Using Mocks](#using-event-mocks)
    - [Using Fakes](#using-event-fakes)
- [Jobs](#mocking-jobs)
    - [Using Mocks](#using-job-mocks)
    - [Using Fakes](#using-job-fakes)
- [Mail Fakes](#mail-fakes)
- [Notification Fakes](#notification-fakes)
- [Facades](#mocking-facades)

<a name="introduction"></a>
## Introduction

When testing Laravel applications, you may wish to "mock" certain aspects of your application so they are not actually executed during a given test. For example, when testing a controller that fires an event, you may wish to mock the event listeners so they are not actually executed during the test. This allows you to only test the controller's HTTP response without worrying about the execution of the event listeners, since the event listeners can be tested in their own test case.

Laravel provides helpers for mocking events, jobs, and facades out of the box. These helpers primarily provide a convenience layer over Mockery so you do not have to manually make complicated Mockery method calls. Of course, you are free to use [Mockery](http://docs.mockery.io/en/latest/) or PHPUnit to create your own mocks or spies.

<a name="mocking-events"></a>
## Events

<a name="using-event-mocks"></a>
### Using Mocks

If you are making heavy use of Laravel's event system, you may wish to silence or mock certain events while testing. For example, if you are testing user registration, you probably do not want all of a `UserRegistered` event's handlers firing, since the listeners may send "welcome" e-mails, etc.

Laravel provides a convenient `expectsEvents` method which verifies the expected events are fired, but prevents any listeners for those events from executing:

    <?php

    use App\Events\UserRegistered;

    class ExampleTest extends TestCase
    {
        /**
         * Test new user registration.
         */
        public function testUserRegistration()
        {
            $this->expectsEvents(UserRegistered::class);

            // Test user registration...
        }
    }

You may use the `doesntExpectEvents` method to verify that the given events are not fired:

    <?php

    use App\Events\OrderShipped;
    use App\Events\OrderFailedToShip;

    class ExampleTest extends TestCase
    {
        /**
         * Test order shipping.
         */
        public function testOrderShipping()
        {
            $this->expectsEvents(OrderShipped::class);
            $this->doesntExpectEvents(OrderFailedToShip::class);

            // Test order shipping...
        }
    }

If you would like to prevent all event listeners from running, you may use the `withoutEvents` method. When this method is called, all listeners for all events will be mocked:

    <?php

    class ExampleTest extends TestCase
    {
        public function testUserRegistration()
        {
            $this->withoutEvents();

            // Test user registration code...
        }
    }

<a name="using-event-fakes"></a>
### Using Fakes

As an alternative to mocking, you may use the `Event` facade's `fake` method to prevent all event listeners from executing. You may then assert that events were fired and even inspect the data they received. When using fakes, assertions are made after the code under test is executed:

    <?php

    use App\Events\OrderShipped;
    use App\Events\OrderFailedToShip;
    use Illuminate\Support\Facades\Event;

    class ExampleTest extends TestCase
    {
        /**
         * Test order shipping.
         */
        public function testOrderShipping()
        {
            Event::fake();

            // Perform order shipping...

            Event::assertFired(OrderShipped::class, function ($e) use ($order) {
                return $e->order->id === $order->id;
            });

            Event::assertNotFired(OrderFailedToShip::class);
        }
    }

<a name="mocking-jobs"></a>
## Jobs

<a name="using-job-mocks"></a>
### Using Mocks

Sometimes, you may wish to test that given jobs are dispatched when making requests to your application. This will allow you to test your routes and controllers in isolation without worrying about your job's logic. Of course, you should then test the job in a separate test case.

Laravel provides the convenient `expectsJobs` method which will verify that the expected jobs are dispatched. However, the job itself will not be executed:

    <?php

    use App\Jobs\ShipOrder;

    class ExampleTest extends TestCase
    {
        public function testOrderShipping()
        {
            $this->expectsJobs(ShipOrder::class);

            // Test order shipping...
        }
    }

> {note} This method only detects jobs that are dispatched via the `DispatchesJobs` trait's dispatch methods or the `dispatch` helper function. It does not detect queued jobs that are sent directly to `Queue::push`.

Like the event mocking helpers, you may also test that a job is not dispatched using the `doesntExpectJobs` method:

    <?php

    use App\Jobs\ShipOrder;

    class ExampleTest extends TestCase
    {
        /**
         * Test order cancellation.
         */
        public function testOrderCancellation()
        {
            $this->doesntExpectJobs(ShipOrder::class);

            // Test order cancellation...
        }
    }

Alternatively, you may ignore all dispatched jobs using the `withoutJobs` method. When this method is called within a test method, all jobs that are dispatched during that test will be discarded:

    <?php

    use App\Jobs\ShipOrder;

    class ExampleTest extends TestCase
    {
        /**
         * Test order cancellation.
         */
        public function testOrderCancellation()
        {
            $this->withoutJobs();

            // Test order cancellation...
        }
    }

<a name="using-job-fakes"></a>
### Using Fakes

As an alternative to mocking, you may use the `Queue` facade's `fake` method to prevent jobs from being queued. You may then assert that jobs were pushed to the queue and even inspect the data they received. When using fakes, assertions are made after the code under test is executed:

    <?php

    use App\Jobs\ShipOrder;
    use Illuminate\Support\Facades\Queue;

    class ExampleTest extends TestCase
    {
        public function testOrderShipping()
        {
            Queue::fake();

            // Perform order shipping...

            Queue::assertPushed(ShipOrder::class, function ($job) use ($order) {
                return $job->order->id === $order->id;
            });

            // Assert a job was pushed to a given queue...
            Queue::assertPushedOn('queue-name', ShipOrder::class);

            // Assert a job was not pushed...
            Queue::assertNotPushed(AnotherJob::class);
        }
    }

<a name="mail-fakes"></a>
## Mail Fakes

You may use the `Mail` facade's `fake` method to prevent mail from being sent. You may then assert that [mailables](/docs/{{version}}/mail) were sent to users and even inspect the data they received. When using fakes, assertions are made after the code under test is executed:

    <?php

    use App\Mail\OrderShipped;
    use Illuminate\Support\Facades\Mail;

    class ExampleTest extends TestCase
    {
        public function testOrderShipping()
        {
            Mail::fake();

            // Perform order shipping...

            Mail::assertSent(OrderShipped::class, function ($mail) use ($order) {
                return $mail->order->id === $order->id;
            });

            // Assert a message was sent to the given users...
            Mail::assertSentTo([$user], OrderShipped::class);

            // Assert a mailable was not sent...
            Mail::assertNotSent(AnotherMailable::class);
        }
    }

<a name="notification-fakes"></a>
## Notification Fakes

You may use the `Notification` facade's `fake` method to prevent notifications from being sent. You may then assert that [notifications](/docs/{{version}}/notifications) were sent to users and even inspect the data they received. When using fakes, assertions are made after the code under test is executed:

    <?php

    use App\Notifications\OrderShipped;
    use Illuminate\Support\Facades\Notification;

    class ExampleTest extends TestCase
    {
        public function testOrderShipping()
        {
            Notification::fake();

            // Perform order shipping...

            Notification::assertSentTo(
                $user,
                OrderShipped::class,
                function ($notification, $channels) use ($order) {
                    return $notification->order->id === $order->id;
                }
            );

            // Assert a notification was sent to the given users...
            Notification::assertSentTo(
                [$user], OrderShipped::class
            );

            // Assert a notification was not sent...
            Notification::assertNotSentTo(
                [$user], AnotherNotification::class
            );
        }
    }

<a name="mocking-facades"></a>
## Facades

Unlike traditional static method calls, [facades](/docs/{{version}}/facades) may be mocked. This provides a great advantage over traditional static methods and grants you the same testability you would have if you were using dependency injection. When testing, you may often want to mock a call to a Laravel facade in one of your controllers. For example, consider the following controller action:

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * Show a list of all users of the application.
         *
         * @return Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

We can mock the call to the `Cache` facade by using the `shouldReceive` method, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock. Since facades are actually resolved and managed by the Laravel [service container](/docs/{{version}}/container), they have much more testability than a typical static class. For example, let's mock our call to the `Cache` facade's `get` method:

    <?php

    class FooTest extends TestCase
    {
        public function testGetIndex()
        {
            Cache::shouldReceive('get')
                        ->once()
                        ->with('key')
                        ->andReturn('value');

            $this->visit('/users')->see('value');
        }
    }

> {note} You should not mock the `Request` facade. Instead, pass the input you desire into the HTTP helper methods such as `call` and `post` when running your test. Likewise, instead of mocking the `Config` facade, simply call the `Config::set` method in your tests.

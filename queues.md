# Queues

- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Queueing Closures](#queueing-closures)
- [Running The Queue Listener](#running-the-queue-listener)
- [Push Queues](#push-queues)

<a name="configuration"></a>
## Configuration

The Laravel Queue component provides a unified API across a variety of different queue services. Queues allow you to defer the processing of a time consuming task, such as sending an e-mail, until a later time, thus drastically speeding up the web requests to your application.

The queue configuration file is stored in `app/config/queue.php`. In this file you will find connection configurations for each of the queue drivers that are included with the framework, which includes a [Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs), and synchronous (for local use) driver.

The following dependencies are needed for the listed queue drivers:

- Beanstalkd: `pda/pheanstalk`
- Amazon SQS: `aws/aws-sdk-php`
- IronMQ: `iron-io/iron_mq`

<a name="basic-usage"></a>
## Basic Usage

To push a new job onto the queue, use the `Queue::push` method:

**Pushing A Job Onto The Queue**

	Queue::push('SendEmail', array('message' => $message));

The first argument given to the `push` method is the name of the class that should be used to process the job. The second argument is an array of data that should be passed to the handler. A job handler should be defined like so:

**Defining A Job Handler**

	class SendEmail {

		public function fire($job, $data)
		{
			//
		}

	}

Notice the only method that is required is `fire`, which receives a `Job` instance as well as the array of `data` that was pushed onto the queue.

If you want the job to use a method other than `fire`, you may specify the method when you push the job:

**Specifying A Custom Handler Method**

	Queue::push('SendEmail@send', array('message' => $message));

Once you have processed a job, it must be deleted from the queue, which can be done via the `delete` method on the `Job` instance:

**Deleting A Processed Job**

	public function fire($job, $data)
	{
		// Process the job...

		$job->delete();
	}

If you wish to release a job back onto the queue, you may do so via the `release` method:

**Releasing A Job Back Onto The Queue**

	public function fire($job, $data)
	{
		// Process the job...

		$job->release();
	}

You may also specify the number of seconds to wait before the job is released:

	$job->release(5);

If an exception occurs while the job is being processed, it will automatically be released back onto the queue. You may check the number of attempts that have been made to run the job using the `attempts` method:

**Checking The Number Of Run Attempts**

	if ($job->attempts() > 3)
	{
		//
	}

You may also access the job identifier:

**Accessing The Job ID**

	$job->getJobId();

<a name="queueing-closures"></a>
## Queueing Closures

You may also push a Closure onto the queue. This is very convenient for quick, simple tasks that need to be queued:

**Pushing A Closure Onto The Queue**

	Queue::push(function($job) use ($id)
	{
		Account::delete($id);

		$job->delete();
	});

> **Note:** When pushing Closures onto the queue, the `__DIR__` and `__FILE__` constants should not be used.

When using Iron.io [push queues](#push-queues), you should take extra precaution queueing Closures. The end-point that receives your queue messages should check for a token to verify that the request is actually from Iron.io. For example, your push queue end-point should be something like: `https://yourapp.com/queue/receive?token=SecretToken`. You may then check the value of the secret token in your application before marshalling the queue request.

<a name="running-the-queue-listener"></a>
## Running The Queue Listener

Laravel includes an Artisan task that will run new jobs as they are pushed onto the queue. You may run this task using the `queue:listen` command:

**Starting The Queue Listener**

	php artisan queue:listen

You may also specify which queue connection the listener should utilize:

	php artisan queue:listen connection

Note that once this task has started, it will continue to run until it is manually stopped. You may use a process monitor such as [Supervisor](http://supervisord.org/) to ensure that the queue listener does not stop running.

You may also set the length of time (in seconds) each job should be allowed to run:

**Specifying The Job Timeout Parameter**

	php artisan queue:listen --timeout=60

In addition, you may specify the number of seconds to wait before polling for new jobs:

	php artisan queue:listen --sleep=5

To process only the first job on the queue, you may use the `queue:work` command:

**Processing The First Job On The Queue**

	php artisan queue:work

<a name="push-queues"></a>
## Push Queues

Push queues allow you to utilize the powerful Laravel 4 queue facilities without running any daemons or background listeners. Currently, push queues are only supported by the [Iron.io](http://iron.io) driver. Before getting started, create an Iron.io account, and add your Iron credentials to the `app/config/queue.php` configuration file.

Next, you may use the `queue:subscribe` Artisan command to register a URL end-point that will receive newly pushed queue jobs:

**Registering A Push Queue Subscriber**

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

Now, when you login to your Iron dashboard, you will see your new push queue, as well as the subscribed URL. You may subscribe as many URLs as you wish to a given queue. Next, create a route for your `queue/receive` end-point and return the response from the `Queue::marshal` method:

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

The `marshal` method will take care of firing the correct job handler class. To fire jobs onto the push queue, just use the same `Queue::push` method used for conventional queues.

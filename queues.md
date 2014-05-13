# Queues

- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Queueing Closures](#queueing-closures)
- [Running The Queue Listener](#running-the-queue-listener)
- [Daemon Queue Worker](#daemon-queue-worker)
- [Push Queues](#push-queues)
- [Failed Jobs](#failed-jobs)

<a name="configuration"></a>
## Configuration

The Laravel Queue component provides a unified API across a variety of different queue services. Queues allow you to defer the processing of a time consuming task, such as sending an e-mail, until a later time, thus drastically speeding up the web requests to your application.

The queue configuration file is stored in `app/config/queue.php`. In this file you will find connection configurations for each of the queue drivers that are included with the framework, which includes a [Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs), [Redis](http://redis.io), and synchronous (for local use) driver.

The following dependencies are needed for the listed queue drivers:

- Beanstalkd: `pda/pheanstalk`
- Amazon SQS: `aws/aws-sdk-php`
- IronMQ: `iron-io/iron_mq`

<a name="basic-usage"></a>
## Basic Usage

#### Pushing A Job Onto The Queue

To push a new job onto the queue, use the `Queue::push` method:

	Queue::push('SendEmail', array('message' => $message));

#### Defining A Job Handler

The first argument given to the `push` method is the name of the class that should be used to process the job. The second argument is an array of data that should be passed to the handler. A job handler should be defined like so:

	class SendEmail {

		public function fire($job, $data)
		{
			//
		}

	}

Notice the only method that is required is `fire`, which receives a `Job` instance as well as the array of `data` that was pushed onto the queue.

#### Specifying A Custom Handler Method

If you want the job to use a method other than `fire`, you may specify the method when you push the job:

	Queue::push('SendEmail@send', array('message' => $message));

#### Specifying The Queue / Tube For A Job

You may also specify the queue / tube a job should be sent to:

	Queue::push('SendEmail@send', array('message' => $message), 'emails');

#### Passing The Same Payload To Multiple Jobs

If you need to pass the same data to several queue jobs, you may use the `Queue::bulk` method:

	Queue::bulk(array('SendEmail', 'NotifyUser'), $payload);

#### Delaying The Execution Of A Job

Sometimes you may wish to delay the execution of a queued job. For instance, you may wish to queue a job that sends a customer an e-mail 15 minutes after sign-up. You can accomplish this using the `Queue::later` method:

	$date = Carbon::now()->addMinutes(15);

	Queue::later($date, 'SendEmail@send', array('message' => $message));

In this example, we're using the [Carbon](https://github.com/briannesbitt/Carbon) date library to specify the delay we wish to assign to the job. Alternatively, you may pass the number of seconds you wish to delay as an integer.

#### Deleting A Processed Job

Once you have processed a job, it must be deleted from the queue, which can be done via the `delete` method on the `Job` instance:

	public function fire($job, $data)
	{
		// Process the job...

		$job->delete();
	}

#### Releasing A Job Back Onto The Queue

If you wish to release a job back onto the queue, you may do so via the `release` method:

	public function fire($job, $data)
	{
		// Process the job...

		$job->release();
	}

You may also specify the number of seconds to wait before the job is released:

	$job->release(5);

#### Checking The Number Of Run Attempts

If an exception occurs while the job is being processed, it will automatically be released back onto the queue. You may check the number of attempts that have been made to run the job using the `attempts` method:

	if ($job->attempts() > 3)
	{
		//
	}

#### Accessing The Job ID

You may also access the job identifier:

	$job->getJobId();

<a name="queueing-closures"></a>
## Queueing Closures

You may also push a Closure onto the queue. This is very convenient for quick, simple tasks that need to be queued:

#### Pushing A Closure Onto The Queue

	Queue::push(function($job) use ($id)
	{
		Account::delete($id);

		$job->delete();
	});

When using Iron.io [push queues](#push-queues), you should take extra precaution queueing Closures. The end-point that receives your queue messages should check for a token to verify that the request is actually from Iron.io. For example, your push queue end-point should be something like: `https://yourapp.com/queue/receive?token=SecretToken`. You may then check the value of the secret token in your application before marshaling the queue request.

<a name="running-the-queue-listener"></a>
## Running The Queue Listener

Laravel includes an Artisan task that will run new jobs as they are pushed onto the queue. You may run this task using the `queue:listen` command:

#### Starting The Queue Listener

	php artisan queue:listen

You may also specify which queue connection the listener should utilize:

	php artisan queue:listen connection

Note that once this task has started, it will continue to run until it is manually stopped. You may use a process monitor such as [Supervisor](http://supervisord.org/) to ensure that the queue listener does not stop running.

You may pass a comma-delimited list of queue connections to the `listen` command to set queue priorities:

	php artisan queue:listen --queue=high,low

In this example, jobs on the `high-connection` will always be processed before moving onto jobs from the `low-connection`.

#### Specifying The Job Timeout Parameter

You may also set the length of time (in seconds) each job should be allowed to run:

	php artisan queue:listen --timeout=60

#### Specifying Queue Sleep Duration

In addition, you may specify the number of seconds to wait before polling for new jobs:

	php artisan queue:listen --sleep=5

Note that the queue only "sleeps" if no jobs are on the queue. If more jobs are available, the queue will continue to work them without sleeping.

#### Processing The First Job On The Queue

To process only the first job on the queue, you may use the `queue:work` command:

	php artisan queue:work

<a name="daemon-queue-workers"></a>
## Daemon Queue Workers

The `queue:work` also includes a `--daemon` option for forcing the queue worker to continue processing jobs without ever re-booting the framework. This results in a significant reduction of CPU usage when compared to the `queue:listen` command, but at the added complexity of needing to drain the queues of currently executing jobs during your deployments.

To start a queue worker in daemon mode, use the `--daemon` flag:

	php artisan queue:work connection --daemon

	php artisan queue:work connection --daemon --sleep=3

	php artisan queue:work connection --daemon --sleep=3 --tries=3

As you can see, the `queue:work` command supports most of the same options available to `queue:listen`. You may use the `php artisan help queue:work` command to view all of the available options.

### Deploying With Daemon Queue Workers

The simplest way to deploy an application using daemon queue workers is to put the application in maintenance mode at the beginning of your deploymnet. This can be done using the `php artisan down` command. Once the application is in maintenance mode, Laravel will now accept any new jobs off of the queue, but will continue to process existing jobs. Once enough time has passed for all of your existing jobs to execute (usually no longer than 30-60 seconds), you may stop the worker and continue your deployment process.

If you are using Supervisor or Laravel Forge, which utilizes Supervisor, you may typically stop a worker with a command like the following:

	supervisorctl stop worker-1

Once the queues have been drained and your fresh code has been deployed to your server, you should restart the daemon queue work. If you are using Supervisor, this can typically be done with a command like this:

	supervisorctl start worker-1

<a name="push-queues"></a>
## Push Queues

Push queues allow you to utilize the powerful Laravel 4 queue facilities without running any daemons or background listeners. Currently, push queues are only supported by the [Iron.io](http://iron.io) driver. Before getting started, create an Iron.io account, and add your Iron credentials to the `app/config/queue.php` configuration file.

#### Registering A Push Queue Subscriber

Next, you may use the `queue:subscribe` Artisan command to register a URL end-point that will receive newly pushed queue jobs:

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

Now, when you login to your Iron dashboard, you will see your new push queue, as well as the subscribed URL. You may subscribe as many URLs as you wish to a given queue. Next, create a route for your `queue/receive` end-point and return the response from the `Queue::marshal` method:

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

The `marshal` method will take care of firing the correct job handler class. To fire jobs onto the push queue, just use the same `Queue::push` method used for conventional queues.

<a name="failed-jobs"></a>
## Failed Jobs

Since things don't always go as planned, sometimes your queued jobs will fail. Don't worry, it happens to the best of us! Laravel includes a convenient way to specify the maximum number of times a job should be attempted. After a job has exceeded this amount of attempts, it will be inserted into a `failed_jobs` table. The failed jobs table name can be configured via the `app/config/queue.php` configuration file.

To create a migration for the `failed_jobs` table, you may use the `queue:failed-table` command:

	php artisan queue:failed-table

You can specify the maximum number of times a job should be attempted using the `--tries` switch on the `queue:listen` command:

	php artisan queue:listen connection-name --tries=3

If you would like to register an event that will be called when a queue job fails, you may use the `Queue::failing` method. This event is a great opportunity to notify your team via e-mail or [HipChat](https://www.hipchat.com).

	Queue::failing(function($connection, $job, $data)
	{
		//
	});

To view all of your failed jobs, you may use the `queue:failed` Artisan command:

	php artisan queue:failed

The `queue:failed` command will list the job ID, connection, queue, and failure time. The job ID may be used to retry the failed job. For instance, to retry a failed job that has an ID of 5, the following command should be issued:

	php artisan queue:retry 5

If you would like to delete a failed job, you may use the `queue:forget` command:

	php artisan queue:forget 5

To delete all of your failed jobs, you may use the `queue:flush` command:

	php artisan queue:flush

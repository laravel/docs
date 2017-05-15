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

The queue configuration file is stored in `config/queue.php`. In this file you will find connection configurations for each of the queue drivers that are included with the framework, which includes a database, [Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs), [Redis](http://redis.io), null, and synchronous (for local use) driver. The `null` queue driver simply discards queued jobs so they are never run.

### Queue Database Table

In order to use the `database` queue driver, you will need a database table to hold the jobs. To generate a migration to create this table, run the `queue:table` Artisan command:

	php artisan queue:table

### Other Queue Dependencies

The following dependencies are needed for the listed queue drivers:

- Amazon SQS: `aws/aws-sdk-php`
- Beanstalkd: `pda/pheanstalk ~3.0`
- IronMQ: `iron-io/iron_mq ~1.5`
- Redis: `predis/predis ~1.0`

<a name="basic-usage"></a>
## Basic Usage

#### Pushing A Job Onto The Queue

All of the queueable jobs for your application are stored in the `App\Commands` directory. You may generate a new queued command using the Artisan CLI:

	php artisan make:command SendEmail --queued

To push a new job onto the queue, use the `Queue::push` method:

	Queue::push(new SendEmail($message));

> **Note:** In this example, we are using the `Queue` facade directly; however, typically you would dispatch queued command via the [Command Bus](/docs/{{version}}/bus). We will continue to use the `Queue` facade throughout this page; however, familiarize with the command bus as well, since it is used to dispatch both queued and synchronous commands for your application.

By default, the `make:command` Artisan command generates a "self-handling" command, meaning a `handle` method is added to the command itself. This method will be called when the job is executed by the queue. You may type-hint any dependencies you need on the `handle` method and the [service container](/docs/{{version}}/container) will automatically inject them:

	public function handle(UserRepository $users)
	{
		//
	}

If you would like your command to have a separate handler class, you should add the `--handler` flag to the `make:command` command:

	php artisan make:command SendEmail --queued --handler

The generated handler will be placed in `App\Handlers\Commands` and will be resolved out of the IoC container.

#### Specifying The Queue / Tube For A Job

You may also specify the queue / tube a job should be sent to:

	Queue::pushOn('emails', new SendEmail($message));

#### Passing The Same Payload To Multiple Jobs

If you need to pass the same data to several queue jobs, you may use the `Queue::bulk` method:

	Queue::bulk([new SendEmail($message), new AnotherCommand]);

#### Delaying The Execution Of A Job

Sometimes you may wish to delay the execution of a queued job. For instance, you may wish to queue a job that sends a customer an e-mail 15 minutes after sign-up. You can accomplish this using the `Queue::later` method:

	$date = Carbon::now()->addMinutes(15);

	Queue::later($date, new SendEmail($message));

In this example, we're using the [Carbon](https://github.com/briannesbitt/Carbon) date library to specify the delay we wish to assign to the job. Alternatively, you may pass the number of seconds you wish to delay as an integer.

> **Note:** The Amazon SQS service has a delay limit of 900 seconds (15 minutes).

#### Queues And Eloquent Models

If your queued job accepts an Eloquent model in its constructor, only the identifier for the model will be serialized onto the queue. When the job is actually handled, the queue system will automatically re-retrieve the full model instance from the database. It's all totally transparent to your application and prevents issues that can arise from serializing full Eloquent model instances.

#### Deleting A Processed Job

Once you have processed a job, it must be deleted from the queue. If no exception is thrown during the execution of your job, this will be done automatically.

If you would like to `delete` or `release` the job manually, the `Illuminate\Queue\InteractsWithQueue` trait provides access to the queue job `release` and `delete` methods. The `release` method accepts a single value: the number of seconds you wish to wait until the job is made available again.

	public function handle(SendEmail $command)
	{
		if (true)
		{
			$this->release(30);
		}
	}

#### Releasing A Job Back Onto The Queue

IF an exception is thrown while the job is being processed, it will automatically be released back onto the queue so it may be attempted again. The job will continue to be released until it has been attempted the maximum number of times allowed by your application. The number of maximum attempts is defined by the `--tries` switch used on the `queue:listen` or `queue:work` Artisan commands.

#### Checking The Number Of Run Attempts

If an exception occurs while the job is being processed, it will automatically be released back onto the queue. You may check the number of attempts that have been made to run the job using the `attempts` method:

	if ($this->attempts() > 3)
	{
		//
	}

> **Note:** Your command / handler must use the `Illuminate\Queue\InteractsWithQueue` trait in order to call this method.

<a name="queueing-closures"></a>
## Queueing Closures

You may also push a Closure onto the queue. This is very convenient for quick, simple tasks that need to be queued:

#### Pushing A Closure Onto The Queue

	Queue::push(function($job) use ($id)
	{
		Account::delete($id);

		$job->delete();
	});

> **Note:** Instead of making objects available to queued Closures via the `use` directive, consider passing primary keys and re-pulling the associated models from within your queue job. This often avoids unexpected serialization behavior.

When using Iron.io [push queues](#push-queues), you should take extra precaution queueing Closures. The end-point that receives your queue messages should check for a token to verify that the request is actually from Iron.io. For example, your push queue end-point should be something like: `https://yourapp.com/queue/receive?token=SecretToken`. You may then check the value of the secret token in your application before marshalling the queue request.

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

In this example, jobs on the `high` connection will always be processed before moving onto jobs from the `low` connection.

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

<a name="daemon-queue-worker"></a>
## Daemon Queue Worker

The `queue:work` also includes a `--daemon` option for forcing the queue worker to continue processing jobs without ever re-booting the framework. This results in a significant reduction of CPU usage when compared to the `queue:listen` command, but at the added complexity of needing to drain the queues of currently executing jobs during your deployments.

To start a queue worker in daemon mode, use the `--daemon` flag:

	php artisan queue:work connection --daemon

	php artisan queue:work connection --daemon --sleep=3

	php artisan queue:work connection --daemon --sleep=3 --tries=3

As you can see, the `queue:work` command supports most of the same options available to `queue:listen`. You may use the `php artisan help queue:work` command to view all of the available options.

### Deploying With Daemon Queue Workers

The simplest way to deploy an application using daemon queue workers is to put the application in maintenance mode at the beginning of your deployment. This can be done using the `php artisan down` command. Once the application is in maintenance mode, Laravel will not accept any new jobs off of the queue, but will continue to process existing jobs.

The easiest way to restart your workers is to include the following command in your deployment script:

	php artisan queue:restart

This command will instruct all queue workers to restart after they finish processing their current job.

> **Note:** This command relies on the cache system to schedule the restart. By default, APCu does not work for CLI commands. If you are using APCu, add `apc.enable_cli=1` to your APCu configuration.

### Coding For Daemon Queue Workers

Daemon queue workers do not restart the framework before processing each job. Therefore, you should be careful to free any heavy resources before your job finishes. For example, if you are doing image manipulation with the GD library, you should free the memory with `imagedestroy` when you are done.

Similarly, your database connection may disconnect when being used by long-running daemon. You may use the `DB::reconnect` method to ensure you have a fresh connection.

<a name="push-queues"></a>
## Push Queues

Push queues allow you to utilize the powerful Laravel 5 queue facilities without running any daemons or background listeners. Currently, push queues are only supported by the [Iron.io](http://iron.io) driver. Before getting started, create an Iron.io account, and add your Iron credentials to the `config/queue.php` configuration file.

#### Registering A Push Queue Subscriber

Next, you may use the `queue:subscribe` Artisan command to register a URL end-point that will receive newly pushed queue jobs:

	php artisan queue:subscribe queue_name queue/receive

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

Now, when you login to your Iron dashboard, you will see your new push queue, as well as the subscribed URL. You may subscribe as many URLs as you wish to a given queue. Next, create a route for your `queue/receive` end-point and return the response from the `Queue::marshal` method:

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

The `marshal` method will take care of firing the correct job handler class. To fire jobs onto the push queue, just use the same `Queue::push` method used for conventional queues.

<a name="failed-jobs"></a>
## Failed Jobs

Since things don't always go as planned, sometimes your queued jobs will fail. Don't worry, it happens to the best of us! Laravel includes a convenient way to specify the maximum number of times a job should be attempted. After a job has exceeded this amount of attempts, it will be inserted into a `failed_jobs` table. The failed jobs table name can be configured via the `config/queue.php` configuration file.

To create a migration for the `failed_jobs` table, you may use the `queue:failed-table` command:

	php artisan queue:failed-table

You can specify the maximum number of times a job should be attempted using the `--tries` switch on the `queue:listen` command:

	php artisan queue:listen connection-name --tries=3

If you would like to register an event that will be called when a queue job fails, you may use the `Queue::failing` method. This event is a great opportunity to notify your team via e-mail or [HipChat](https://www.hipchat.com).

	Queue::failing(function($connection, $job, $data)
	{
		//
	});

You may also define a `failed` method directly on a queue job class, allowing you to perform job specific actions when a failure occurs:

	public function failed()
	{
		// Called when the job is failing...
	}
	
If your job is not self-handling and has a seperate handler class the `failed` method needs to be defined there instead.

### Retrying Failed Jobs

To view all of your failed jobs, you may use the `queue:failed` Artisan command:

	php artisan queue:failed

The `queue:failed` command will list the job ID, connection, queue, and failure time. The job ID may be used to retry the failed job. For instance, to retry a failed job that has an ID of 5, the following command should be issued:

	php artisan queue:retry 5

If you would like to delete a failed job, you may use the `queue:forget` command:

	php artisan queue:forget 5

To delete all of your failed jobs, you may use the `queue:flush` command:

	php artisan queue:flush

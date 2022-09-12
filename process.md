# Console Processes

- [Introduction](#introduction)
- [Running Processes](#running-processes)
    - [Command](#command)
    - [Path](#path)
    - [Timeout](#timeout)
    - [Error Handling](#error-handling)
- [Concurrent Processes](#concurrent-processes)
- [Asynchronous Processes](#asynchronous-processes)
- [Macros](#macros)
- [Testing](#testing)
    - [Faking Process Results](#faking-results)
    - [Inspecting Process Requests](#inspecting-results)

<a name="introduction"></a>
## Introduction

When building web applications, it's common to have the need of running operating system tasks via command-line processes. Thankfully, Laravel provides an expressive, minimal API around Symfony's Process component, allowing you to quickly run processes in your Laravel application.

Laravel's wrapper around Symfony's Process component is focused on its most common use cases, testing, and a wonderful developer experience.

<a name="running-processes"></a>
## Running Processes

To run a process, you may use the `run` method provided by the `Process` facade. Let's examine how to run a basic `ls` command:

    use Illuminate\Support\Facades\Process;

    $result = Process::run('ls');

    $result->ok(); // true
    $result->output(); // my-file-1, my-file-2
    $result->toArray(); // ["my-file-1", "my-file-2"]

The `run` method returns an instance of `Illuminate\Console\Contracts\ProcessResult`, which provides a variety of methods that may be used to inspect the process result:

    $result = Process::run('ls');

    $result->output(): string;
    $result->toArray(): array;
    $result->errorOutput(): string;
    $result->exitCode(): int;
    $result->ok(): bool;
    $result->failed(): bool;

The `Illuminate\Console\Contracts\ProcessResult` object also implements the PHP `ArrayAccess` interface, allowing you to iterate over each line of the output. The output, is "exploded" via the `\n` character:

    $files = Process::run('ls');

    foreach ($files as $file) {
        // ...
    }

    return $files[0]; // my-file-1

<a name="accessing-the-output-at-real-time"></a>
#### Accessing the output at real-time

By default, when using the `output` method, Laravel waits for the process to be finished, so you can have access to the entire process's output:

    $result = Process::run('echo 1; sleep 1; echo 2');

    return $result->output(); // 1, 2

If you wish to access the process's output at real-time, you may use a closure as second argument of the `run` method:

    Process::run('echo 1; sleep 1; echo 2', function ($output) {
        dump($output); // Dumps "1", and after a second dumps "2"
    });

    return $result->output(); // 1, 2

In addition, if you with to know if the given output is from the type `stderr` or `stderr`, you may use the second argument of given closure:

    Process::run('echo 1; sleep 1; echo 2', function ($output, $type) {
        dump($type == "out"); // true
        dump($type == "err"); // false
    });

<a name="dumping-processes"></a>
#### Dumping Processes

If you would like to "dump" the outgoing process instance before it is sent and terminate the script's execution, you may add the `dump` or `dd` method to the beginning of your process definition:

    Process::dd()->run('ls');

    // ^ Illuminate\Console\Process^ {#662
    //  -commandline: "ls"
    //  -cwd: "/Users/nunomaduro/Work/Code/laravel"
    // ...

<a name="command"></a>
### Command

When running processes, you may pass an string or an array of strings as the first argument to the `run` method:

    Process::run('ls -la');
    Process::run(['ls', '-la', storage_path('images')]);

If you wish, you may set the command up-front using the `command` method:

    Process::command('ls -la')->run();
    Process::command(['ls', '-la', storage_path('images')])->run();

<a name="path"></a>
### Path

You may use the `path` method if you would like to specify the working directory / base path of the process:

    $path = storage_path('images');

    Process::path($path)->run('ls'); // image-1.jpg, image-2.jpg

<a name="timeout"></a>
### Timeout

The `timeout` method may be used to specify the maximum number of seconds to wait for a process:

    Process::timeout(3)->run('sleep 2');

If the given timeout is exceeded, an instance of `Illuminate\Console\Process\Exceptions\ProcessTimedOutException` will be thrown:

    try {
        Process::timeout(3)->run('sleep 4');
    } catch (ProcessTimedOutException $e) {
        dump($e->result()->exitCode()); // 143
    }

If you don't care about the time a process takes to run, and you would just like a process to run forever, you may use the `forever` method:

    Process::forever()->run(/* ... */);

<a name="error-handling"></a>
### Error Handling

By default, if a process fails, Laravel does not throw exceptions. You may determine if the process ran successfully using the `ok` or `failed` methods:

    // Determine if the status code is 0...
    $result->ok();

    // Determine if the status code is different from 0...
    $result->failed();

<a name="throwing-exceptions"></a>
#### Throwing Exceptions

If you have a process result and would like to throw an instance of `Illuminate\Console\Exceptions\ProcessFailedException` if the exit code indicates an error, you may use the `throw`, `throwIf`, or `throwUnless` methods:

    $result = Process::run(/* ... */);

    // Throw an exception if an error occurred...
    $result->throw();

    // Throw an exception if an error occurred and the given condition is true...
    $result->throwIf($condition);

    // Throw an exception if an error occurred and the given condition is false...
    $result->throwUnless($condition);

    return $result->output();

The `throw` method returns a regular result instance if no error occurred, allowing you to chain other operations onto the `throw` method:

    $result = Process::run(/* ... */);

    return $result->throw()->output();

If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw`, `throwIf`, or `throwUnless`  methods. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure:

    use Illuminate\Console\Exceptions\ProcessFailedException;

    return Process::run(/* ... */)->throw(function ($e) {
        // Perform some clean-up ...
    })->ok();

<a name="concurrent-processes"></a>
## Concurrent Processes

Sometimes, you may wish to run multiple processes concurrently. In other words, you want several processes to be "run" at the same time, instead of running them sequentially.

Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Console\Process\Pool` instance, allowing you to easily add processes to the pool so they can run concurrently:

    use Illuminate\Console\Process\Pool;
    use Illuminate\Support\Facades\Process;

    $results = Process::pool(fn (Pool $pool) => [
        $pool->run('sleep 1'),
        $pool->run('sleep 1'),
        $pool->run('sleep 1'),
    ]); // Takes 1 second...

    return $results[0]->ok() &&
           $results[1]->ok() &&
           $results[2]->ok();

<a name="asynchronous-processes"></a>
## Asynchronous Processes

By default, processes are synchronous, meaning that the method `run` will automatically wait for the process to be finished before returning the process's result. Yet, if you need to run processes asynchronously while performing other tasks in your code, you may use the `async` method:process pool so they can run concurrently:

    $result = Process::async()->run(/* ... */);

    // Do other tasks, while the process runs in background...

    // Wait for the result when necessary..
    return $result->wait()->output();

> **Warning**
> When running asynchronous processes, you must explicitly call the `wait` method on the returned result instance. Non-waited asynchronous processes may get stopped by Laravel using the `SIGTERM` or `SIGKILL` signals.

<a name="macros"></a>
## Macros

The Process's factory is also "macroable", meaning that you may define a macro within the `boot` method of your application's service providers:

    use Illuminate\Support\Facades\Process;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Process::macro('ls', fn () => Process::command('ls'));
    }

Once your macro has been configured, you may invoke it from anywhere in your application to create a pending process with the specified configuration:

    $result = Process::ls()->run();

    return $result->toArray(); // ["my-file-1", "my-file-2"]

<a name="testing"></a>
## Testing

The `Process` facade's `fake` method allows you to instruct Laravel to return stubbed / dummy results when processes are run.

<a name="faking-results"></a>
### Faking Process Results

For example, to instruct the `Process` to return successful empty result, you may call the `fake` method with no arguments:

    use Illuminate\Support\Facades\Process;

    Process::fake();

    $result = Process::run(/* ... */);

    return $result->ok(); // true

<a name="faking-specific-commands"></a>
#### Faking specific commands

Alternatively, you may pass an array to the `fake` method. The array's keys should represent command patterns that you wish to fake and their associated results. The `*` character may be used as a wildcard character. Any processes made to process commands that have not been faked will actually be executed. You may use the Process facade's `result` method to construct stub / fake results for these processes:

    Process::fake([
        // Stub a process result for the "ls" command...
        'ls' => Process::result(['file-1.php', 'file-2.php'),

        // Stub a process result for all "curl" commands...
        'curl*' => Process::result(json_encode(['item'])),
    ]);

If you would like to specify a fallback command pattern that will stub all unmatched commands, you may use a single `*` character:

    Process::fake([
        // Stub a process result for all "curl" commands...
        'curl*' => Process::result(json_encode(['item'])),

        // Stub a process result for all other commands...
        '*' => Process::result(),
    ]);

<a name="fake-callback"></a>
#### Fake Callback

If you require more complicated logic to determine what results to return for certain processes, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Console\Process` and should return a result instance. Within your closure, you may perform whatever logic is necessary to determine what type of result to return:

    use Illuminate\Support\Facades\Process;

    Process::fake(function ($process, $response) {
        if ($process->command() == /** ... */) {
            return Process::result('An error message', 1));
        }

        // ...
    });

<a name="inspecting-processes"></a>
### Inspecting Processes

When faking processes, you may occasionally wish to inspect the processes in order to make sure your application is running the correct commands. You may accomplish this by calling the `Process::assertRan` method after calling `Process::fake`.

Besides a simple `string`, the `assertRan` method also accepts a closure which receives an `Illuminate\Console\Process` instance and should return a boolean value indicating if the process matches your expectations. In order for the test to pass, at least one process must have ran matching the given expectations:

    Process::fake();

    Process::timeout(50)->run('sleep 30');

    Process::assertRan('sleep 30');

    // or using a closure...
    Process::assertRan(function ($process) {
        return $process->command() == 'sleep 30' && $process->timeout() == 50.0;
    });

If needed, you may assert that a specific process was not ran using the `assertNotRan` method:

    Process::fake();

    Process::run('ls');

    Process::assertNotRan('ls -la');

    // or using a closure...
    Process::assertNotRan(function ($process) {
        return $process->command() == 'ls -la');
    });

You may use the `assertRanCount` method to assert how many processes were "ran" during the test:

    Process::fake();

    Process::run('ls');
    Process::run('ls');

    Process::assertRanCount(2);

Or, you may use the `assertNothingRan` method to assert that no processes were ran during the test:

    Process::fake();

    Process::assertNothingRan();

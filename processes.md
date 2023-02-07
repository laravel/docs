# Processes

- [Introduction](#introduction)
- [Invoking Processes](#invoking-processes)
    - [Process Options](#process-options)
    - [Process Output](#process-output)
- [Asynchronous Processes](#asynchronous-processes)
    - [Process IDs & Signals](#process-ids-and-signals)
    - [Asynchronous Process Output](#asynchronous-process-output)
- [Concurrent Processes](#concurrent-processes)
- [Testing](#testing)
    - [Faking Processes](#faking-responses)
    - [Inspecting Results](#inspecting-requests)
    - [Preventing Stray Processes](#preventing-stray-processes)

<a name="introduction"></a>
## Introduction

Laravel provides an expressive, minimal API around the [Symfony Process component](https://symfony.com/doc/current/components/process.html), allowing you to conveniently invoke external processes from your Laravel application. Laravel's process features are focused on the most common use cases and a wonderful developer experience.

<a name="invoking-processes"></a>
## Invoking Processes

To invoke a process, you may use the `run` and `start` methods offered by the `Process` facade. The `run` method will invoke a process and wait for the process to finish executing, while the `start` method is used for asynchronous process execution. We'll examine both approaches within this documentation. First, let's examine how to invoke a basic process and inspect its result:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

Of course, the `Illuminate\Console\Process\ProcessResult` instance returned by the `run` method offers a variety of helpful methods that may be used to inspect the process result:

```php
$result = Process::run('ls -la');

$result->successful():
$result->failed();
$result->exitCode();
$result->output();
$result->errorOutput();
```

<a name="throwing-exceptions"></a>
#### Throwing Exceptions

If you have a process result and would like to throw an instance of `Illuminate\Console\Process\Exceptions\ProcessFailedException` if the exit code indicates that the process failed, you may use the `throw` and `throwIf` methods:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### Process Options

Of course, you may need to customize the behavior of a process before invoking it. Thankfully, Laravel allows you to tweak a variety of process features, such as the working directory, timeout, and environment variables.

<a name="working-directory-path"></a>
#### Working Directory Path

For instance, you may use the `path` method to specify the working directory of the process. If this method is not invoked, the process will inherit the working directory of the currently executing PHP script:

```php
$result = Process::path(base_path())->run('ls -la');
```

<a name="timeouts"></a>
#### Timeouts

By default, processes will throw an instance of `Illuminate\Console\Process\Exceptions\ProcessTimedOutException` after executing for more than 60 seconds. However, you can customize this behavior via the `timeout` method:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

Or, if you would like to disable the process timeout entirely, you may invoke the `forever` method:

```php
$result = Process::forever()->run('bash import.sh');
```

The `idleTimeout` method may be used to specify the maximum number of seconds the process may run without returning any output:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### Environment Variables

Environment variables may be provided to the process via the `env` method. The invoked process will also inherit all of the environment variables defined by your system:

```php
$result = Process::forever()
            ->env(['IMPORT_PATH' => base_path()])
            ->run('bash import.sh');
```

If you wish to remove an inherited environment variable from the invoked process, you may pass that environment variable with a value of `false`:

```php
$result = Process::forever()
            ->env(['LOAD_PATH' => false])
            ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY Mode

The `tty` method may be used to enable TTY mode for your process. TTY mode connects the input and output of the process to the input and output of your program, allowing your process to open an editor like Vim or Nano as a process:

```php
Process::forever()->tty()->run('vim');
```

<a name="process-output"></a>
### Process Output

As previously discussed, process output may be accessed using the `output` (stdout) and `errorOutput` (stderr) methods on a process result:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

However, output may also be gathered in real-time by passing a closure as the second argument to the `run` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel also offers the `seeInOutput` and `seeInErrorOutput` methods, which provide a convenient way to determine if a given string was contained in the process' output:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### Disabling Process Output

If your process is writing a significant amount of output that you are not interested in, you can conserve memory by disabling output retrieval entirely. To accomplish this, invoke the `withoutOutput` method while building the process:

```php
use Illuminate\Support\Facades\Process;

$result = Process::withoutOutput()->run('bash import.sh');
```

<a name="asynchronous-processes"></a>
## Asynchronous Processes

While the `run` method invokes processes synchronously, the `start` method may be used to invoke a process asynchronously. This allows your application to continue performing other tasks while the process runs in the background. Once the process has been invoked, you may utilize the `running` method to determine if the process is still running:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}
```

Instead of continually checking the `running` method to determine if a process is still running, you may invoke the `wait` method to wait until the process is finished executing and retrieve the process result instance:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### Process IDs & Signals

The `pid` method may be used to retrieve the operating system assigned process ID of the running process:

```php
$process = Process::start('bash import.sh');

return $process->pid();
```

You may use the `signal` method to send a "signal" to the running process. A list of predefined signal constants can be found within the [PHP documentation](https://www.php.net/manual/en/pcntl.constants.php):

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### Asynchronous Process Output

While an asynchronous process is running, you may of course access its entire current output using the `output` and `errorOutput` methods; however, you may utilize the `latestOutput` and `latestErrorOutput` to access the output from the process that has occurred since the output was last retrieved:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

Like the `run` method, output may also be gathered in real-time from asynchronous processes by passing a closure as the second argument to the `start` method. The closure will receive two arguments: the "type" of output (`stdout` or `stderr`) and the output string itself:

```php
Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});
```

<a name="concurrent-processes"></a>
## Concurrent Processes

Laravel also makes it a breeze to manage a pool of concurrent processes, allowing you to easily execute many processes simultaneously. To get started, invoke the `pool` method, which accepts a closure that will receive an instance of `Illuminate\Console\Process\Pool`.

Within this closure, you may define the processes that belong to the pool. Once a process pool is started via the `start` method, you may access a [collection](/docs/{{version}}/collections) of the running processes via the `running` method. Then, you may wait for all of the pool processes to finish executing and resolve their results via the `wait` method. The `wait` method returns an array accessible object that allows you to access the process result instance of each process in the pool by its key:

```php
$pool = Process::pool(function (Pool $pool) {
    $pool->path(base_path())->command('bash import-1.sh');
    $pool->path(base_path())->command('bash import-2.sh');
    $pool->path(base_path())->command('bash import-3.sh');
})->start(function ($type, $output, $key) {
    // ...
});

while ($pool->running()->isNotEmpty()) {
    // ...
}

$results = $pool->wait();

echo $results[0]->output();
```

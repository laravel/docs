# Processes

- [Introduction](#introduction)
- [Invoking Processes](#invoking-processes)
    - [Process Options](#process-options)
    - [Process Output](#process-output)
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


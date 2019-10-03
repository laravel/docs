# Artisan 指令列

- [介紹](#introduction)
    - [Tinker (REPL)](#tinker)
- [撰寫指令](#writing-commands)
    - [產生指令](#generating-commands)
    - [指令結構](#command-structure)
    - [閉包指令](#closure-commands)
- [定義預期的輸入](#defining-input-expectations)
    - [參數](#arguments)
    - [選項](#options)
    - [輸入陣列](#input-arrays)
    - [輸入說明](#input-descriptions)
- [指令 I/O](#command-io)
    - [取得輸入](#retrieving-input)
    - [互動式輸入](#prompting-for-input)
    - [自訂輸出](#writing-output)
- [註冊指令](#registering-commands)
- [使用程式碼呼叫指令](#programmatically-executing-commands)
    - [在指令中呼叫其他指令](#calling-commands-from-other-commands)

<a name="introduction"></a>
## 介紹

Artisan 是 Laravel 內建的指令集合，它能提供許多好用的指令來協助你開發程式。你可以使用 `list` 查詢更多指令：

    php artisan list

每個指令都有輔助說明，會告訴你有哪些參數及選項可以用。在需要查詢的指令前加上 `help` 即可顯示輔助說明內容:

    php artisan help migrate

<a name="tinker"></a>
### Tinker (REPL)

所有 Laravel 的應用程式都可以使用 Tinker，是基於 [PsySH](https://github.com/bobthecow/psysh) 這個套件所提供的 REPL。Tinker 可以直接操控你的整個 Laravel 應用程式，包括 Eloquent ORM、任務、事件等。 執行 `tinker` 這個指令，即可進入 Tinker 環境：

    php artisan tinker

You can publish Tinker's configuration file using the `vendor:publish` command:

    php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"

#### Command Whitelist

Tinker utilizes a white-list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, and `up` commands. If you would like to white-list more commands you may add them to the `commands` array in your `tinker.php` configuration file:

    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

#### Alias Blacklist

Typically, Tinker automatically aliases classes as you require them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file:

    'dont_alias' => [
        App\User::class,
    ],

<a name="writing-commands"></a>
## 撰寫指令

除了 Laravel 提供的原生指令外，你也可以自訂指令。預設檔案路徑是在 `app/Console/Commands`。然而，只要指令可以被 Composer 載入，那你就可以任意的選擇檔案路徑。

<a name="generating-commands"></a>
### 產生指令

要產生一個新指令，請使用 `make:command`。該指令會在 `app/Console/Commands` 這個目錄中建立檔案。如果你的 Laravel 應用程式中沒有這個目錄，別擔心！當你第一次使用 `make:command` 時，會即時建立該目錄。產生的指令會包括所有指令中預設的屬性與方法：

    php artisan make:command SendEmails

<a name="command-structure"></a>
### 指令結構

產生新的指令後，應該先宣告 `signature` 和 `description` 的屬性內容，這會在使用 `list` 這個指令的時候顯示出來。 當指令被執行時，`handle` 方法會被呼叫，因此你可以將任何的指令邏輯放到該方法中。

> {tip} 為了讓程式碼更有效的複用，最好讓終端指令的程式碼保持輕量化，並讓它們緩載到應用程式服務的任務完成。在下列範例中，請注意！我們注入了一個服務類別來完成發送信件的「重任」。

讓我們看一個例子。請注意，我們可以在建構子中注入任何需要的依賴，Laravel 的[服務容器](/docs/{{version}}/container)將會自動注入任何型別提示的依賴到建構子中：

    <?php

    namespace App\Console\Commands;

    use App\DripEmailer;
    use App\User;
    use Illuminate\Console\Command;

    class SendEmails extends Command
    {
        /**
         * 指令列的名稱及用法
         *
         * @var string
         */
        protected $signature = 'email:send {user}';

        /**
         * 指令列的描述
         *
         * @var string
         */
        protected $description = 'Send drip e-mails to a user';

        /**
         * 建立新的指令實例
         *
         * @return void
         */
        public function __construct()
        {
            parent::__construct();
        }

        /**
         * 執行指令
         *
         * @param  \App\DripEmailer  $drip
         * @return mixed
         */
        public function handle(DripEmailer $drip)
        {
            $drip->send(User::find($this->argument('user')));
        }
    }

<a name="closure-commands"></a>
### 閉包指令

基於閉包的指令提供了有別於使用類別定義終端指令的方法。簡單的說，路由閉包是另一種撰寫指令的方式。在 `app/Console/Kernel.php` 檔案的 `commands` 這個方法中，Laravel 會載入 `routes/console.php` 這個檔案：

    /**
     * 為應用程式註冊基於閉包的指令
     *
     * @return void
     */
    protected function commands()
    {
        require base_path('routes/console.php');
    }
    
即使這個檔案沒有定義 HTTP 路由，它仍可以透過路由終端定義到應用程式中。在這個檔案中，你可以使用 `Artisan::command` 這個方法定義所有基於閉包的路由。`command` 方法可以接受兩個參數：其一是[指令命名](#defining-input-expectations)，另一個取得指令參數與選項的閉包：

    Artisan::command('build {project}', function ($project) {
        $this->info("Building {$project}!");
    });

因為閉包綁定最底層的指令實例，所以你完全可以使用指令類別的所有輔助方法

#### 型別提示

除了接收指令參數與選項外，指令閉包還可以使用型別提示從[服務容器](/docs/{{version}}/container)中注入所需的任何依賴：

    use App\DripEmailer;
    use App\User;

    Artisan::command('email:send {user}', function (DripEmailer $drip, $user) {
        $drip->send(User::find($user));
    });

#### 撰寫閉包指令的描述

When defining a Closure based command, you may use the `describe` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands:

    Artisan::command('build {project}', function ($project) {
        $this->info("Building {$project}!");
    })->describe('Build the project');

<a name="defining-input-expectations"></a>
## Defining Input Expectations

When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax.

<a name="arguments"></a>
### Arguments

All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one **required** argument: `user`:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user}';

You may also make arguments optional and define default values for arguments:

    // Optional argument...
    email:send {user?}

    // Optional argument with default value...
    email:send {user=foo}

<a name="options"></a>
### Options

Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are specified on the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue}';

In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`:

    php artisan email:send 1 --queue

<a name="options-with-values"></a>
#### Options With Values

Next, let's take a look at an option that expects a value. If the user must specify a value for an option, suffix the option name with a `=` sign:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue=}';

In this example, the user may pass a value for the option like so:

    php artisan email:send 1 --queue=default

You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used:

    email:send {user} {--queue=default}

<a name="option-shortcuts"></a>
#### Option Shortcuts

To assign a shortcut when defining an option, you may specify it before the option name and use a | delimiter to separate the shortcut from the full option name:

    email:send {user} {--Q|queue}

<a name="input-arrays"></a>
### Input Arrays

If you would like to define arguments or options to expect array inputs, you may use the `*` character. First, let's take a look at an example that specifies an array argument:

    email:send {user*}

When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to `['foo', 'bar']`:

    php artisan email:send foo bar

When defining an option that expects an array input, each option value passed to the command should be prefixed with the option name:

    email:send {user} {--id=*}

    php artisan email:send --id=1 --id=2

<a name="input-descriptions"></a>
### Input Descriptions

You may assign descriptions to input arguments and options by separating the parameter from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send
                            {user : The ID of the user}
                            {--queue= : Whether the job should be queued}';

<a name="command-io"></a>
## Command I/O

<a name="retrieving-input"></a>
### Retrieving Input

While your command is executing, you will obviously need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

If you need to retrieve all of the arguments as an `array`, call the `arguments` method:

    $arguments = $this->arguments();

Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method:

    // Retrieve a specific option...
    $queueName = $this->option('queue');

    // Retrieve all options...
    $options = $this->options();

If the argument or option does not exist, `null` will be returned.

<a name="prompting-for-input"></a>
### Prompting For Input

In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('What is your name?');
    }

The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as a password:

    $password = $this->secret('What is the password?');

#### Asking For Confirmation

If you need to ask the user for a simple confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`.

    if ($this->confirm('Do you wish to continue?')) {
        //
    }

#### Auto-Completion

The `anticipate` method can be used to provide auto-completion for possible choices. The user can still choose any answer, regardless of the auto-completion hints:

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

#### Multiple Choice Questions

If you need to give the user a predefined set of choices, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen:

    $name = $this->choice('What is your name?', ['Taylor', 'Dayle'], $defaultIndex);

<a name="writing-output"></a>
### Writing Output

To send output to the console, use the `line`, `info`, `comment`, `question` and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green text:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->info('Display this on the screen');
    }

To display an error message, use the `error` method. Error message text is typically displayed in red:

    $this->error('Something went wrong!');

If you would like to display plain, uncolored console output, use the `line` method:

    $this->line('Display this on the screen');

#### Table Layouts

The `table` method makes it easy to correctly format multiple rows / columns of data. Just pass in the headers and rows to the method. The width and height will be dynamically calculated based on the given data:

    $headers = ['Name', 'Email'];

    $users = App\User::all(['name', 'email'])->toArray();

    $this->table($headers, $users);

#### Progress Bars

For long running tasks, it could be helpful to show a progress indicator. Using the output object, we can start, advance and stop the Progress Bar. First, define the total number of steps the process will iterate through. Then, advance the Progress Bar after processing each item:

    $users = App\User::all();

    $bar = $this->output->createProgressBar(count($users));

    $bar->start();

    foreach ($users as $user) {
        $this->performTask($user);

        $bar->advance();
    }

    $bar->finish();

For more advanced options, check out the [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html).

<a name="registering-commands"></a>
## Registering Commands

Because of the `load` method call in your console kernel's `commands` method, all commands within the `app/Console/Commands` directory will automatically be registered with Artisan. In fact, you are free to make additional calls to the `load` method to scan other directories for Artisan commands:

    /**
     * Register the commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__.'/Commands');
        $this->load(__DIR__.'/MoreCommands');

        // ...
    }

You may also manually register commands by adding its class name to the `$commands` property of your `app/Console/Kernel.php` file. When Artisan boots, all the commands listed in this property will be resolved by the [service container](/docs/{{version}}/container) and registered with Artisan:

    protected $commands = [
        Commands\SendEmails::class
    ];

<a name="programmatically-executing-commands"></a>
## Programmatically Executing Commands

Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to fire an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's name or class as the first argument, and an array of command parameters as the second argument. The exit code will be returned:

    Route::get('/foo', function () {
        $exitCode = Artisan::call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

Alternatively, you may pass the entire Artisan command to the `call` method as a string:

    Artisan::call('email:send 1 --queue=default');

Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/{{version}}/queues). Before using this method, make sure you have configured your queue and are running a queue listener:

    Route::get('/foo', function () {
        Artisan::queue('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

You may also specify the connection or queue the Artisan command should be dispatched to:

    Artisan::queue('email:send', [
        'user' => 1, '--queue' => 'default'
    ])->onConnection('redis')->onQueue('commands');

#### Passing Array Values

If your command defines an option that accepts an array, you may pass an array of values to that option:

    Route::get('/foo', function () {
        $exitCode = Artisan::call('email:send', [
            'user' => 1, '--id' => [5, 13]
        ]);
    });

#### Passing Boolean Values

If you need to specify the value of an option that does not accept string values, such as the `--force` flag on the `migrate:refresh` command, you should pass `true` or `false`:

    $exitCode = Artisan::call('migrate:refresh', [
        '--force' => true,
    ]);

<a name="calling-commands-from-other-commands"></a>
### Calling Commands From Other Commands

Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command parameters:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    }

If you would like to call another console command and suppress all of its output, you may use the `callSilent` method. The `callSilent` method has the same signature as the `call` method:

    $this->callSilent('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);

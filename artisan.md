# Artisan Console-Artisan 命令

- [Introduction-介绍](#introduction)
- [Writing Commands-写命令](#writing-commands)
    - [Command Structure-命令结构](#command-structure)
- [Command I/O-命令 I/O](#command-io)
    - [Defining Input Expectations-定义输入期望](#defining-input-expectations)
    - [Retrieving Input-输入检索](#retrieving-input)
    - [Prompting For Input-提示输入](#prompting-for-input)
    - [Writing Output-写输出](#writing-output)
- [Registering Commands-注册命令](#registering-commands)
- [Calling Commands Via Code-调用命令通过代码](#calling-commands-via-code)

<a name="introduction"></a>
## Introduction-介绍

Artisan is the name of the command-line interface included with Laravel. It provides a number of helpful commands for your use while developing your application. It is driven by the powerful Symfony Console component. To view a list of all available Artisan commands, you may use the `list` command:

Artisan 是包含Laravel命令行接口的名称。它提供了一些有用的命令，为您的使用，同时开发应用程序。它是由强大的Symfony控制台组件驱动。要查看所有可用的Artisan 命令的列表，你可以使用`list`命令：

    php artisan list

Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, simply precede the name of the command with `help`:

每个命令还包括一个“help”屏幕，显示和描述了命令的可用参数和选项。要查看帮助屏幕，只是前面加上'help`命令的名称：
    php artisan help migrate

<a name="writing-commands"></a>
## Writing Commands-写命令

In addition to the commands provided with Artisan, you may also build your own custom commands for working with your application. You may store your custom commands in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be autoloaded based on your `composer.json` settings.

除了提供与Artisan的命令，你也可以建立自己的自定义命令与您的应用程序中工作。您可以存储您的自定义命令，在命令行`app/Console/ Commands`目录;不过，你可以自由选择自己的存储位置，只要你的命令，可以根据你的`composer.json`设置来自动加载。

To create a new command, you may use the `make:console` Artisan command, which will generate a command stub to help you get started:

要创建一个新的命令，你可以使用`make：console`工匠命令，它会生成一个命令存根，以帮助您开始：

    php artisan make:console SendEmails

The command above would generate a class at `app/Console/Commands/SendEmails.php`. When creating the command, the `--command` option may be used to assign the terminal command name:

上面的命令会产生一类的应用程序`app/Console/Commands/SendEmails.php`。当创建的命令，可以使用`--command`选项来分配终端命令名：

    php artisan make:console SendEmails --command=emails:send

<a name="command-structure"></a>
### Command Structure-命令结构

Once your command is generated, you should fill out the `signature` and `description` properties of the class, which will be used when displaying your command on the `list` screen.

一旦生成你的命令，你应填写`signature`和类中，`list`屏幕上显示你的命令时将使用`description`性能。


The `handle` method will be called when your command is executed. You may place any command logic in this method. Let's take a look at an example command.

当执行你的命令`handle`方法将被调用。你可以将任何命令逻辑在此方法中。让我们看一个例子命令。

Note that we are able to inject any dependencies we need into the command's constructor. The Laravel [service container](/docs/{{version}}/container) will automatically inject all dependencies type-hinted in the constructor. For greater code reusability, it is good practice to keep your console commands light and let them defer to application services to accomplish their tasks.

需要注意的是，我们能够注入，我们需要在命令的构造任何依赖。该Laravel[服务容器](/docs/{{version}}/container) 将自动注入所有依赖型暗示在构造函数中。对于更大的代码重用，这是很好的做法，让您的控制台命令点亮，让他们推迟到应用服务来完成他们的任务。

    <?php namespace App\Console\Commands;

    use App\User;
    use App\DripEmailer;
    use Illuminate\Console\Command;
    use Illuminate\Foundation\Inspiring;

    class Inspire extends Command
    {
        /**
         * The name and signature of the console command.这个名字和控制台命令的签名。
         *
         * @var string
         */
        protected $signature = 'email:send {user}';

        /**
         * The console command description.控制台命令的说明。
         *
         * @var string
         */
        protected $description = 'Send drip e-mails to a user';

        /**
         * The drip e-mail service.滴水电子邮件服务。
         *
         * @var DripEmailer
         */
        protected $drip;

        /**
         * Create a new command instance.创建一个新的命令实例。
         *
         * @param  DripEmailer  $drip
         * @return void
         */
        public function __construct(DripEmailer $drip)
        {
            parent::__construct();

            $this->drip = $drip;
        }

        /**
         * Execute the console command.执行控制台命令。
         *
         * @return mixed
         */
        public function handle()
        {
            $this->drip->send(User::find($this->argument('user')));
        }
    }

<a name="command-io"></a>
## Command I/O-命令 I/O

<a name="defining-input-expectations"></a>
### Defining Input Expectations-定义输入期望

When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax.

当写控制台命令，它是常见的，收集从通过参数或选项的用户输入。 Laravel可以很方便地定义你用你的命令`signature`属性用户期望的输入。该`signature`属性，可以在一个单一的，表现力，路由的语法定义的名称，参数和选项的命令。

All user supplied arguments and options are wrapped in curly braces, for example:
所有的用户提供的参数和选项都包裹在花括号，例如：

    /**
     * The name and signature of the console command.这个名字和控制台命令的签名。
     *
     * @var string
     */
    protected $signature = 'email:send {user}';

In this example, the command defines one **required** argument: `user`. You may also make arguments optional and define default values for optional arguments:

在这个例子中，该命令定义了一个**必需**的参数：`user`。您也可以进行申辩和可选的可选参数定义默认值：

    // Optional argument... 可选参数
    email:send {user?}

    // Optional argument with default value...使用默认值可选参数...
    email:send {user=foo}

Options, like arguments, also are a form of user input. However, they are prefixed by two hyphens (`--`) when they are specified on the command line. We can define options in the signature like so:

选项，如参数，也有用户输入的形式。然而，他们是由两个连字符（`--`）时，在命令行上指定它们的前缀。我们可以定义在像这样的签名选项：

    /**
     * The name and signature of the console command.
     * 这个名字和控制台命令的签名。
     * @var string
     */
    protected $signature = 'email:send {user} {--queue}';

In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`:

在这个例子中，`--queue`开关可以调用工匠命令时指定。如果`--queue`开关传递，期权的价值将是'真'。否则，该值将是`FALSE`：

    php artisan email:send 1 --queue

You may also specify that the option should be assigned a value by the user by suffixing the option name with a `=` sign, indicating that a value should be provided:

你也可以指定该选项应该由用户分配一个值由一个'='符号后面添加选项名称，表明值应提供：

    /**
     * The name and signature of the console command.这个名字和控制台命令的签名。
     * 
     * @var string
     */
    protected $signature = 'email:send {user} {--queue=}';

In this example, the user may pass a value for the option like so:
在本实施例中，用户可以通过一个数值为像这样的选项：

    php artisan email:send 1 --queue=default

You may also assign default values to options:
您也可以指定默认值的选项：

    email:send {user} {--queue=default}

#### Input Descriptions-输入描述

You may assign descriptions to input arguments and options by separating the parameter from the description using a colon:

您可以通过使用一个冒号参数的描述分离分配描述输入参数和选项：

    /**
     * The name and signature of the console command.这个名字和控制台命令的签名。
     *
     * @var string
     */
    protected $signature = 'email:send
                            {user : The ID of the user}
                            {--queue= : Whether the job should be queued}';

<a name="retrieving-input"></a>
### Retrieving Input-输入检索

While your command is executing, you will obviously need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods:

当你的命令执行时，你会明显需要访问值由您的命令接受的参数和选项。要做到这一点，你可以使用`argument`和`option`方法：

To retrieve the value of an argument, use the `argument` method:
要检索的参数的值，使用`argument`方法：

    /**
     * Execute the console command.执行控制台命令。
     *
     * @return mixed
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

If you need to retrieve all of the arguments as an `array`, call the `argument` with no parameters:

如果您需要检索所有的参数作为`array`，调用`argument`不带参数：

    $arguments = $this->argument();

Options may be retrieved just as easily as arguments using the `option` method. Like the `argument` method, you may call `option` without any arguments in order to retrieve all of the options as an `array`:

选项可以检索一样容易使用`option`方法的参数。类似`argument`方法，你可以调用`option`不带任何参数，以获取所有的选项作为`array`：

    // Retrieve a specific option...检索特定选项...
    $queueName = $this->option('queue');

    // Retrieve all options... 检索所有选项...
    $options = $this->option();

If the argument or option does not exist, `null` will be returned.
如果参数或选项不存在，`null`将被退回。

<a name="prompting-for-input"></a>
### Prompting For Input 提示输入

In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command:

除了显示输出，您也可以要求用户到你的命令的执行过程中提供意见。该`ask`方法提示给定问题的用户，接受他们的输入，然后返回用户的输入回到你的命令：

    /**
     * Execute the console command.执行控制台命令。
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('What is your name?');
    }

The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful for asking for sensitive information such as a password:

该`secret`方法类似于`ask`，但是当他们在控制台输入用户的输入将是不可见他们。此方法要求提供敏感信息，如密码是有用：

    $password = $this->secret('What is the password?');

#### Asking For Confirmation 要求确认

If you need to ask the user for a simple confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` in response to the prompt, the method will return `true`.

如果你需要询问用户一个简单的确认，你可以使用`confirm`方法。默认情况下，此方法将返回`FALSE`。然而，如果用户输入`y`响应于该提示，该方法将返回`true`。

    if ($this->confirm('Do you wish to continue? [y|N]')) {
        //
    }

#### Giving The User A Choice 给用户一个选择

The `anticipate` method can be used to provided autocompletion for possible choices. The user can still choose any answer, regardless of the choices.

在`anticipate`方法可以用于提供自动完成可能的选择。用户仍然可以选择任何答案，无论选择。

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

If you need to give the user a predefined set of choices, you may use the `choice` method. The user chooses the index of the answer, but the value of the answer will be returned to you. You may set the default value to be returned if nothing is chosen:

如果你需要给用户一个预定义的选择，你可以使用`choice`方法。用户选择答案的指标，但答案的value将被退还给您。您可以设置默认值，如果没有选择退货：

    $name = $this->choice('What is your name?', ['Taylor', 'Dayle'], false);

<a name="writing-output"></a>
### Writing Output 写输出

To send output to the console, use the `info`, `comment`, `question` and `error` methods. Each of these methods will use the appropriate ANSI colors for their purpose.

将输出发送到控制台，使用`info`，`comment`，`question`和`error`方法。这些方法都将使用相应的ANSI颜色，他们的目的。

To display an information message to the user, use the `info` method. Typically, this will display in the console as green text:

要显示一个信息消息给用户，使用`info`方法。通常情况下，这将在控制台绿色文字显示：

    /**
     * Execute the console command.执行控制台命令。
     *
     * @return mixed
     */
    public function handle()
    {
        $this->info('Display this on the screen');
    }

To display an error message, use the `error` method. Error message text is typically displayed in red:

显示错误消息，使用'error`方法。错误消息文本中通常显示为红色：

    $this->error('Something went wrong!');

#### Table Layouts表格布局

The `table` method makes it easy to correctly format multiple rows / columns of data. Just pass in the headers and rows to the method. The width and height will be dynamically calculated based on the given data:

该`table`方法，可以很容易地正确地格式化数据的多个行/列。只是通过在标题和行的方法。的宽度和高度将被动态计算基于给定的数据：

    $headers = ['Name', 'Email'];

    $users = App\User::all(['name', 'email'])->toArray();

    $this->table($headers, $users);

#### Progress Bars 进度条

For long running tasks, it could be helpful to show a progress indicator. Using the output object, we can start, advance and stop the Progress Bar. You have to define the number of steps when you start the progress, then advance the Progress Bar after each step:

对于长时间运行的任务，它可能是有帮助的，以显示进度指示器。使用输出对象，我们就可以开始，前进和停止进度条。你必须定义的步数，当您启动进度，然后每个步骤后推进进度栏：

    $users = App\User::all();

    $this->output->progressStart(count($users));

    foreach ($users as $user) {
        $this->performTask($user);

        $this->output->progressAdvance();
    }

    $this->output->progressFinish();

For more advanced options, check out the [Symfony Progress Bar component documentation](http://symfony.com/doc/2.7/components/console/helpers/progressbar.html).

对于更高级的选项，检查出[Symfony的进度条组件文档](http://symfony.com/doc/2.7/components/console/helpers/progressbar.html).

<a name="registering-commands"></a>
## Registering Commands 注册命令

Once your command is finished, you need to register it with Artisan so it will be available for use. This is done within the `app/Console/Kernel.php` file.

一旦你的指令完成后，你需要用Artisan注册它所以这将是可供使用。这是'app/Console/Kernel.php`文件内完成。

Within this file, you will find a list of commands in the `commands` property. To register your command, simply add the class name to the list. When Artisan boots, all the commands listed in this property will be resolved by the [service container](/docs/{{version}}/container) and registered with Artisan:

在这个文件中，你会发现命令中的`commands` property list（财产清单）。要注册您的命令，只需添加类名到列表中。当Artisan的boots ，都在这个属性中列出的命令将由[服务容器](/docs/{{version}}/container)，并与Artisan注册：

    protected $commands = [
        'App\Console\Commands\SendEmails'
    ];

<a name="calling-commands-via-code"></a>
## Calling Commands Via Code 呼叫指令通过代码

Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to fire an Artisan command from an route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts the name of the command as the first argument, and an array of command parameters as the second argument. The exit code will be returned:

有时你不妨到CLI之外执行的Artisan命令。例如，您可能希望从路由或控制器触发一个Artisan命令。您可以使用在`Artisan`facade `call`方法来做到这一点。该`call`方法接受命令作为第一个参数的名称，命令参数数组作为第二个参数。退出代码将返回：

    Route::get('/foo', function () {
        $exitCode = Artisan::call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/{{version}}/queues):

在`Artisan`facade 使用`queue`方法，你甚至可以排队命令Artisan，使他们在后台通过你的[队列工作](/docs/{{version}}/queues)：

    Route::get('/foo', function () {
        Artisan::queue('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

### Calling Commands From Other Commands 调用命令，从其他命令

Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command parameters:

有时你不妨调用其他命令从现有的工匠命令。你可以这样做使用`call`方法。这`call`方法接受命令名称和命令参数数组：


    /**
     * Execute the console command.执行控制台命令。
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

如果你想调用另一个控制台命令禁止所有的输出，你可以使用`callSilent`方法。该`callSilent`方法具有相同的签名`call`方法：

    $this->callSilent('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);

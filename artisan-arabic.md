# Artisan Console æÍÏÉ ÊÍßã ÇáÍÑİí ÇáãÇåÑ 

- [Introduction](#introduction) ÇáãŞÏãÉ
    - [Tinker (REPL)](#tinker) ãÊÚÏÏ ÇáãåÇã 
- [Writing Commands](#writing-commands) ßÊÇÈÉ ÇáÃæÇãÑ 
    - [Generating Commands](#generating-commands) ÊæáíÏ ÇáÃæÇãÑ 
    - [Command Structure](#command-structure) ÈäíÉ ÇáÃæÇãÑ  
    - [Closure Commands](#closure-commands) ÃæÇãÑ äØÇŞ ÇáÅÛáÇŞ 
- [Defining Input Expectations](#defining-input-expectations) ÊÍÏíÏ ÇáÏÎá ÇáãÊæŞÚ 
    - [Arguments](#arguments) ÇáãÊÛíÑÇÊ
    - [Options](#options) ÇáÎíÇÑÇÊ 
    - [Input Arrays](#input-arrays) ãÕİæİÉ ÇáÇÏÎÇá 
    - [Input Descriptions](#input-descriptions) æÕİ ÇáÅÏÎÇá
- [Command I/O](#command-io) ÃæÇãÑ ÇáÏÎá æÇáÎÑÌ
    - [Retrieving Input](#retrieving-input) ÇÓÊÑÌÇÚ ÇáÏÎá
    - [Prompting For Input](#prompting-for-input) ÊáŞíä ÇáÏÎá 
    - [Writing Output](#writing-output) ßÊÇÈÉ ÇáÎÑÌ
- [Registering Commands](#registering-commands) ÊÓÌíá ÇáÃæÇãÑ 
- [Programmatically Executing Commands](#programmatically-executing-commands) ÊäİíĞ ÇáÃæÇãÑ ÈÑãÌíÇ 
    - [Calling Commands From Other Commands](#calling-commands-from-other-commands) äÏÇÁ ÇáÃæÇãÑ ãä ÃæÇãÑ ÃÎÑì 
- [Signal Handling](#signal-handling) ãÚÇáÌÉ ÇáÅÔÇÑÉ 
- [Stub Customization](#stub-customization) ÊÎÕíÕ ÌÒÁ
- [Events](#events) ÇáÃÍÏÇË 

<a name="introduction"></a> ÇáãŞÏãÉ 
## Introduction ÇáãŞÏãÉ 

Artisan is the command line interface included with Laravel. Artisan exists at the root of your application as the `artisan` script and provides a number of helpful commands that can assist you while you build your application. To view a list of all available Artisan commands, you may use the `list` command:

(Artisan) æÇÌåÉ ÇáÃæÇãÑ ÇáÎÇÕÉ ÈáÇÑÇİá¡ ãæÌæÏ Öãä ÇáÊØÈíŞ ßÓßÑíÈÊ `artisan` 
íÄãä ÇáÚÏíÏ ãä ÇáÃæÇãÑ ÇáãÓÇÚÏÉ ÃËäÇÁ ÈäÇÁ ÇáÊØÈíŞ¡ áÑæÄíÉ ŞÇÆãÉ ÇáÃæÇãÑ äßÊÈ ÇáÃãÑ ÇáÊÇáí 
 

```shell
php artisan list
```


Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`:

ßá ÃãÑ ÃíÖÇ íÊÖãä ÔÇÔÉ ÇáãÓÇÚÏÉ ("help" screen) áÚÑÖ ææÕİ ãÊÛíÑÇÊ æÎíÇÑÇÊ ÇáÃæÇãÑ 
áÚÑÖ ÔÇÔÉ ÇáãÓÇÚÏÉ áÃãÑ äßÊÈ help æÈÚÏåÇ ÇáÃãÑ 
 

```shell
php artisan help migrate
```

<a name="laravel-sail"></a> ÔÑÇÚ áÇÑÇİá 
#### Laravel Sail ÔÑÇÚ áÇÑÇİá 

If you are using [Laravel Sail](/docs/{{version}}/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers:

ÅĞÇ ßäÊ ÊÓÊÎÏã Laravel Sail İí ÈíÆÉ ÇáÊØæíÑ ÇáãÍáíÉ ÇÓÊÎÏã ÇáÃãÑ `sail` áäÏÇÁ ÃæÇãÑ Artisan 
Sail Óæİ íäİĞ ÃæÇãÑ Artisan Öãä ÍÇæíÇÊ Docker
 

```shell
./sail artisan list
```

<a name="tinker"></a> ãÊÚÏÏ ÇáãåÇã 
### Tinker (REPL) ãÊÚÏÏ ÇáãåÇã 

Laravel Tinker is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package.

åæ æÇÌåÉ ÇáÃæÇãÑ ÇáÓæÏÇÁ ÇáÎÇÕÉ ÈáÇÑÇİá powerful REPL 
REPL (read-eval-print-loop) äæÚ ãä ÇáæÇÌåÇÊ ÇáÓæÏÇÁ ÇáÊİÇÚáíÉ ÇáÊí ÊÃÎĞ ãÏÎáÇÊ ãÓÊÎÏã æÍíÏ æ íŞíã ÇáãÏÎáÇÊ æ íÚíÏ ÇáäÊíÌÉ ááãÓÊÎÏã
ãÔÛáÉ ÈæÇÓØÉ ÍÒãÉ (https://github.com/bobthecow/psysh)  PsySH
 

<a name="installation"></a> ÇáÊäÕíÈ
#### Installation ÇáÊäÕíÈ

All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application:

ÇáÊäßÑ ãÖãä ÇİÊÑÇÖíÇ ÈÊØÈíŞÇÊ ÇááÇÑÇİá áßä íãßäß ÇÓÊÎÏÇã Composer áÊäÕíÈå İí ÍÇá ÍĞİå ãä ÇáÊØÈíŞ 


```shell
composer require laravel/tinker
```

> {tip} Looking for a graphical UI for interacting with your Laravel application? Check out [Tinkerwell](https://tinkerwell.app)!

ááÈÍË Úä æÇÌåÉ ÑÓæãíÉ ááÊİÇÚá ãÚ ÊØÈíŞ áÇÑÇİá 
ÑÇÌÚ ÇáÑÇÈØ https://tinkerwell.app


<a name="usage"></a> ÇáÇÓÊÎÏÇã
#### Usage ÇáÇÓÊÎÏÇã

Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command:

ÇáÊäßÑ íÓãÍ áß ÇáÊİÇÚá ãÚ ÊØÈíŞ ÇááÇÑÇİá İí æÇÌåÉ ÇáÃæÇãÑ æ ÇáãæÏáÇÊ æ ÇáÇÚãÇá æ ÇáÇÍÏÇË
áÏÎæá ÈíÆÉ ÇáÊäßÑ äİĞ ÇáÃãÑ 


```shell
php artisan tinker
```

You can publish Tinker's configuration file using the `vendor:publish` command:	

áäÔÑ ãáİ ÇÚÏÇÏÇÊ ÇáÊäßÑ äİĞ ÇáÃãÑ


```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> {note} The `dispatch` helper function and `dispatch` method on the `Dispatchable` class depends on garbage collection to place the job on the queue. Therefore, when using tinker, you should use `Bus::dispatch` or `Queue::push` to dispatch jobs.

*ãáÇÍÙÉ: ÇáÏÇáÉ ÇáãÓÇÚÏÉ `dispatch`  æ ÇáØÑíŞÉ `dispatch` ÇáãæÌæÏÉ Öãä ßáÇÓ `Dispatchable` 
ÊÚÊãÏ Úáì æÖÚ ÇáÚãá Öãä ÑÊá æ ÈÇáÊÇáí ÚäÏ ÇÓÊÎÏÇã ÇáÊäßÑ íÌÈ ÇÓÊÎÏÇã `Bus::dispatch`
Ãæ `Queue::push`  áÅÑÓÇá ÇáÃÚãÇá 


<a name="command-allow-list"></a> ŞÇÆãÉ ÇáÓãÇÍíÉ
#### Command Allow List ŞÇÆãÉ ÇáÓãÇÍíÉ

Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, and `up` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file:

íÓÊÎÏã ÇáÊäßÑ ŞÇÆãÉ ÇáÓãÇÍíÉ áÊÍÏíÏ ÃæÇãÑ Artisan ÇáÊí ÊäİĞ Öãä Çá shell ÇáÎÇÕ Èå
íãßä ÊäİíĞ ÇáÃæÇãÑ ÇáÊÇáíÉ `clear-compiled`, `down`, `env`,`inspire`, `migrate`, `optimize`, and `up`
ÅĞÇ ÃÑÏÊ ÇáÓãÇÍ ÈÃæÇãÑ ÃßËÑ íãßääß ÇÖÇİÊåã áãÕİæİÉ ÇáÃæÇãÑ İí ãáİ ÇÚÏÇÏÇÊ ÇáÊäßÑ `tinker.php`


    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a> Õİæİ áÇ íÌÈ Ãä ÊÓÊÎÏã ÇÓã ãÓÊÚÇÑ Ãæ ÇÎÊÕÇÑ 
#### Classes That Should Not Be Aliased Õİæİ áÇ íÌÈ Ãä ÊÓÊÎÏã ÇÓã ãÓÊÚÇÑ Ãæ ÇÎÊÕÇÑ 

Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file:

ÚÇÏÉ ÇáÊäßÑ íÖÚ ÃÓãÇÁ ãÓÊÚÇÑÉ ááÕİæİ ÇĞÇ ÃÑÏÊ ÚÏã ÇáÇÎÊÕÇÑ ÖÚåã İí ãÕİæİÉ Öãä ãáİ ÇÚÏÇÏÇÊ ÇáÊäßÑ 


    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>  ßÊÇÈÉ ÇáÃæÇãÑ
## Writing Commands ßÊÇÈÉ ÇáÃæÇãÑ
In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be loaded by Composer.

íãßäß ÕäÚ ÃæÇãÑ ÎÇÕÉ Èß æ ÊÎÒä ÚÇÏÉ İí ãÌáÏ `app/Console/Commands`  æ íãßäß ÊÎÒíäåÇ ÈÃí ãÌáÏ ÊÑíÏå ØÇáãÇ íŞæã Composer ÈÊÍãíáåÇ 

<a name="generating-commands"></a>  ÊæáíÏ ÇáÃæÇãÑ
### Generating Commands ÊæáíÏ ÇáÃæÇãÑ

To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command:

áÇäÔÇÁ ÇãÑ ÌÏíÏ äÓÊÎÏã ÇáÇãÑ `make:command`	
íäÔÃ Õİ ÃãÑ ÌÏíÏ Öãä `app/Console/Commands`  ÇĞÇ áã íßä ãæÌæÏ ÇáãÌáÏ íäÔÃ ÊáŞÇÆíÇ ÚäÏ ÊäİíĞ ÇáÃãÑ


```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a> ÈäíÉ ÇáÃãÑ
### Command Structure ÈäíÉ ÇáÃãÑ

After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method.

ÈÚÏ ÊæáíÏ ÇáÃãÑ íÌÈ ÊÚÑíİ Şíã ãäÇÓÈÉ ááÎÇÕíÊíä `signature` æ `description`
åĞå ÇáÎÕÇÆÕ ÊÓÊÎÏã ÚäÏ ÚÑÖ ÃãÑß İí ÔÇÔÉ ÇáŞÇÆãÉ
signature  ÊÓÊÎÏã áÊÍÏíÏ ÇáÏÎá ÇáãÊæŞÚ ááÃãÑ
ÇáØÑíŞÉ handle íÊã äÏÇÆåÇ ÚäÏ ÊäİíĞ ÇáÃãÑ


Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/{{version}}/container) will automatically inject all dependencies that are type-hinted in this method's signature:

    <?php

    namespace App\Console\Commands;

    use App\Models\User;
    use App\Support\DripEmailer;
    use Illuminate\Console\Command;

    class SendEmails extends Command
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'mail:send {user}';

        /**
         * The console command description.
         *
         * @var string
         */
        protected $description = 'Send a marketing email to a user';

        /**
         * Create a new command instance.
         *
         * @return void
         */
        public function __construct()
        {
            parent::__construct();
        }

        /**
         * Execute the console command.
         *
         * @param  \App\Support\DripEmailer  $drip
         * @return mixed
         */
        public function handle(DripEmailer $drip)
        {
            $drip->send(User::find($this->argument('user')));
        }
    }

> {tip} For greater code reuse, it is good practice to keep your console commands light and let them defer to application services to accomplish their tasks. In the example above, note that we inject a service class to do the "heavy lifting" of sending the e-mails.

<a name="closure-commands"></a> ÃæÇãÑ ÇáäØÇŞ ÇáãÛáŞ
### Closure Commands ÃæÇãÑ ÇáäØÇŞ ÇáãÛáŞ
Closure based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. Within the `commands` method of your `app/Console/Kernel.php` file, Laravel loads the `routes/console.php` file:

íÚÊãÏ Closure Úáì ÃæÇãÑ ÊÄãä ÈÏíá áÊÍÏíÏ ÃæÇãÑ console ßÕİæİ 
ÈäİÓ ÇáØÑíŞÉ ãÓÇÑ closures ÈÏíá ÇáãÊÍßãÇÊ controllers
ÃãÑ closures ÈÏíá áÃãÑ classes
Öãä ÇáØÑíŞÉ `commands`  ÇáãæÌæÏÉ İí Çáãáİ `app/Console/Kernel.php`  ÊŞæã áÇÑÇİá ÈÊÍãíá ãáİ  `routes/console.php`

    /**
     * Register the closure based commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        require base_path('routes/console.php');
    }

Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. Within this file, you may define all of your closure based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options:

åĞÇ Çáãáİ áÇ íÍÏÏ ãÓÇÑÇÊ HTTP íÍÏÏ ÇáãÓÇÑÇÊ ÇáÏÇÎáíÉ İí ÇáÊØÈíŞ
İí åĞÇ Çáãáİ íãßä ÊÍÏíÏ ÇáäØÇŞ ÇáãÛáŞ ÇáãÊÚãÏ Úáì ÃæÇãÑ console ÈÇÓÊÎÏÇã ÇáØÑíŞÉ `Artisan::command`
ÇáØÑíŞÉ `command` ÊÃÎĞ ãÊÛíÑíä ÇáÃæá [command signature] æ ÇáËÇäí ÇáäØÇŞ ÇáãÛáŞ ÇáĞí ÓíÑÓá ãÊÛíÑÇÊ æ ÎíÇÑÇÊ ÇáÃãÑ


    Artisan::command('mail:send {user}', function ($user) {
        $this->info("Sending email to: {$user}!");
    });

The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class.

ÇáäØÇŞ ÇáãÛáŞ íÚØí ÊÍßã ßÇãá ÈÇáØÑŞ ÇáãÓÇÚÏÉ ÈÇáÊÇáí ÊÍßã ÈßÇãá Õİ ÇáÃãÑ

<a name="type-hinting-dependencies"></a>
#### Type-Hinting Dependencies

In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/{{version}}/container):

ÈÇáÅÖÇİÉ áÇÓÊŞÈÇá ÇáãÊÛíÑÇÊ ÃãÑ ÇáäØÇŞ ÇáãÛáŞ íŞæã ÈßÊÇÈÉ ÊáãíÍ ÅÖÇİí ãÚÊãÏ

    use App\Models\User;
    use App\Support\DripEmailer;

    Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
        $drip->send(User::find($user));
    });

<a name="closure-command-descriptions"></a>  æÕİ ÃãÑ ÇáäØÇŞ ÇáãÛáŞ 
#### Closure Command Descriptions æÕİ ÃãÑ ÇáäØÇŞ ÇáãÛáŞ 

When defining a closure based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands:

ÇÓÊÎÏÇã ÇáØÑíŞÉ `purpose` áßÊÇÈÉ æÕİ ááÃãÑ 
åĞÇ ÇáæÕİ íÙåÑ ÚäÏ ÊÔÛíá ÇáÃãÑ `php artisan help`  Ãæ ÇáÃãÑ `php artisan list`
 

    Artisan::command('mail:send {user}', function ($user) {
        // ...
    })->purpose('Send a marketing email to a user');

<a name="defining-input-expectations"></a> ÊÍÏíÏ ÇáÏÎá ÇáãÊæŞÚ 
## Defining Input Expectations ÊÍÏíÏ ÇáÏÎá ÇáãÊæŞÚ 

When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax.

áÊÍÏíÏ ÇáÏÎá ÇáãÊæŞÚ ãä ÇáãÓÊÎÏã äÓÊÎÏã ÇáÎÇÕíÉ `signature` ÊÓãÍ ÈÊÍÏíÏ ÇáÇÓã æÇáãÊÛíÑÇÊ æÇáÎíÇÑÇÊ 

<a name="arguments"></a> ÇáãÊÛíÑÇÊ 
### Arguments ÇáãÊÛíÑÇÊ 

All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`:

   ÊæÖÚ ÇáãÊÛíÑÇÊ Öãä ŞæÓíä ãä ÇáÔßá {argument name}
    İí åĞÇ ÇáãËÇá ÊÍÏíÏ ãÊÛíÑ æÇÍÏ ÇÌÈÇÑí 
 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

You may also make arguments optional or define default values for arguments:

   íãßä ÅÖÇİÉ ãÊÛíÑÇÊ ÇÎÊíÇÑíÉ Ãæ æÖÚ Şíã ÇİÊÑÇÖíÉ áãÊÛíÑÇÊ 

    // Optional argument...
    'mail:send {user?}'

    // Optional argument with default value...
    'mail:send {user=foo}'

<a name="options"></a> ÇáÎíÇÑÇÊ 
### Options ÇáÎíÇÑÇÊ 

Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are provided via the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option:

ÇáÎíÇÑÇÊ ãËá ÇáãÊÛíÑÇÊ ÃíÖÇ ÏÎá ãä ÇáãÓÊÎÏã äÖÚ ŞÈáåÇ áÇÍŞÉ (`--`)
íæÌÏ äæÚíä ãä ÇáÎíÇÑÇÊ ÇáÃæá áÇ íÓÊŞÈá ŞíãÉ æÇáäæÚ ÇáËÇäí íÃÎĞ ŞíãÉ
ÇáäæÚ ÇáÃæá Êßæä ŞíãÊå true Ãæ false 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue}';

In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`:

ÅĞÇ ãÑÑäÇ –queue Êßæä Şíãå true ÛíÑ Ğáß ŞíãÊå false

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a> ÎíÇÑÇÊ ãÚ Şíã
#### Options With Values  ÎíÇÑÇÊ ãÚ Şíã 

Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign:


ÇáäæÚ ÇáËÇäí ÊÍÏíÏ ŞíãÉ ááÎíÇÑ ÈÇÓÊÎÏÇã ÅÔÇÑÉ `=`

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue=}';

In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`:

ÇĞÇ áã äÍÏÏ ÇáÏÎá Êßæä ŞíãÊå null 
 

```shell
php artisan mail:send 1 --queue=default
```

You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used:

íãßä æÖÚ ŞíãÉ ÇİÊÑÇÖíÉ ÅĞÇ áã íãÑÑ ÇáãÓÊÎÏã ŞíãÉ íÃÎĞ ÇáÎíÇÑ ÇáŞíãÉ ÇáÇİÊÑÇÖíÉ 

    'mail:send {user} {--queue=default}'

<a name="option-shortcuts"></a> ÇÎÊÕÇÑÇÊ ÇáÎíÇÑ
#### Option Shortcuts ÇÎÊÕÇÑÇÊ ÇáÎíÇÑ

To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name:

áÊÍÏíÏ ÇÎÊÕÇÑ äÖÚå ŞÈá ÇÓã ÇáÎíÇÑ æ äÖÚ  `|` ááİÕá Èíä ÇáÇÎÊÕÇÑ æ ÇÓã ÇáÎíÇÑ 

    'mail:send {user} {--Q|queue}'

When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen:

äÓÊÎÏã ÇáÇÎÊÕÇÑ Öãä ÔÇÔÉ ÇáÃæÇãÑ 

```shell
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a> ÅÏÎÇá ÇáãÕİæİÇÊ 
### Input Arrays ÅÏÎÇá ÇáãÕİæİÇÊ 

If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument:

áÅÏÎÇá ÃßËÑ ãä ŞíãÉ ÏÎá äÓÊÎÏã `*` 

    'mail:send {user*}'

When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `foo` and `bar` as its values:

íãßä ááãÓÊÎÏã æÖÚ ÃßËÑ ãä ŞíãÉ 

```shell
php artisan mail:send foo bar
```

This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument:

íãßä ÇÓÊÎÏÇã `*`  ãÚ ÇáãÊÛíÑÇÊ ÇáÇÎÊíÇÑíÉ 

    'mail:send {user?*}'

<a name="option-arrays"></a> ãÕİæİÇÊ ÇáÎíÇÑ
#### Option Arrays ãÕİæİÇÊ ÇáÎíÇÑ 

When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name:

áÊÍÏíÏ ÎíÇÑ ãÊÚÏÏ ÇáŞíã

    'mail:send {user} {--id=*}'

Such a command may be invoked by passing multiple `--id` arguments:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>  æÕİ ÇáÏÎá 
### Input Descriptions æÕİ ÇáÏÎá 

You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines:

áæÖÚ æÕİ ááÏÎá äÖÚ : ÈÚÏ ÇáÇÓã Ëã ÇáæÕİ 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send
                            {user : The ID of the user}
                            {--queue : Whether the job should be queued}';

<a name="command-io"></a> ÃãÑ ÇáÏÎá æÇáÎÑÌ 
## Command I/O ÃãÑ ÇáÏÎá æÇáÎÑÌ 

<a name="retrieving-input"></a> ÇÓÊÑÌÇÚ ÇáÏÎá 
### Retrieving Input ÇÓÊÑÌÇÚ ÇáÏÎá 

While your command is executing, you will likely need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods. If an argument or option does not exist, `null` will be returned:

ÚäÏ ÊäİíĞ ÇáÃãÑ äÍÊÇÌ ÇáæÕæá ááãÊÛíÑÇÊ Çæ ÇáÎíÇÑÇÊ äÓÊÎÏã ÇáØÑíŞÉ `argument`   æÇáØÑíŞÉ `option`
ÅĞÇ ßÇä ÇáãÊÛíÑ Çæ ÇáÎíÇÑ ÛíÑ ãæÌæÏ íÚíÏ ŞíãÉ `null`

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

If you need to retrieve all of the arguments as an `array`, call the `arguments` method:

áÇÓÊÑÌÇÚ ßá ÇáãÊÛíÑÇÊ ßãÕİæİÉ äÓÊÎÏã ÇáØÑíŞÉ `arguments`
 

    $arguments = $this->arguments();

Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method:

áÇÓÊÑÌÇÚ ÇáÎíÇÑÇÊ äÓÊÎÏã ÇáØÑíŞÉ `option`
áÇÓÊÑÌÇÚ ÃßËÑ ãä ŞíãÉ ßãÕİæİÉ `options`
 

    // Retrieve a specific option...
    $queueName = $this->option('queue');

    // Retrieve all options as an array...
    $options = $this->options();

<a name="prompting-for-input"></a> ÊáŞíä ÇáÏÎá 
### Prompting For Input ÊáŞíä ÇáÏÎá 

In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command:


áÓÄÇá ÇáãÓÊÎÏã áíŞæã ÈÇáÅÏÎÇá äÓÊÎÏã ÇáØÑíŞÉ `ask` 

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('What is your name?');
    }

The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords:

ÇáØÑíŞÉ `secret` ÊÔÈå ÇáØÑíŞÉ `ask` áßä ÇáÏÎá ÛíÑ ãÑÆí ÊÓÊÎÏã ÚäÏ ÅÏÎÇá ÈíÇäÇÊ ÍÓÇÓÉ ãËá ßáãÇÊ ÇáãÑæÑ 

    $password = $this->secret('What is the password?');

<a name="asking-for-confirmation"></a> ÇáÓÄÇá ááÊÃßíÏ 
#### Asking For Confirmation ÇáÓÄÇá ááÊÃßíÏ 

If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`.

ÇáÓÄÇá ááÊÃßíÏ äÓÊÎÏã ÇáØÑíŞÉ `confirm` áíÏÎá ÇáãÓÊÎÏã yes Ãæ no 
ÇİÊÑÇÖíÇ ÊÚíÏ ŞíãÉ false 
ÅĞÇ ÃÏÎá ÇáãÓÊÎÏã yes Çæ y ÊÚíÏ true 
 

    if ($this->confirm('Do you wish to continue?')) {
        //
    }

If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method:

áÊÚíÏ ŞíãÉ ÇİÊÑÇÖíÉ true äÖÚåÇ ßãÊÛíÑ ËÇäí 

    if ($this->confirm('Do you wish to continue?', true)) {
        //
    }

<a name="auto-completion"></a> ÇáÅßãÇá ÇáÊáŞÇÆí 
#### Auto-Completion ÇáÅßãÇá ÇáÊáŞÇÆí 

The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints:

ÇáØÑíŞÉ `anticipate`  ÊæİÑ ÅßãÇá ÊáŞÇÆí ááÎíÇÑÇÊ ÇáããßäÉ 

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion:

íãßä ÊãÑíÑ closure ßãÊÛíÑ ËÇäí ááØÑíŞÉ `anticipate`  
closure íÓÊÏÚì İí ßá ãÑÉ íßÊÈ İíåÇ ÇáãÓÊÎÏã ãÍÑİ 
closure  íŞÈá ãÊÛíÑ äæÚ äÕí íÊÖãä ÃíÖÇ ÏÎá ÇáãÓÊÎÏã æ íÚíÏ ãÕİæİÉ ÎíÇÑÇÊ ááÅßãÇá ÇáÊáŞÇÆí

    $name = $this->anticipate('What is your address?', function ($input) {
        // Return auto-completion options...
    });

<a name="multiple-choice-questions"></a> ÃÓÆáÉ ÎíÇÑ ãÊÚÏÏ 
#### Multiple Choice Questions ÃÓÆáÉ ÎíÇÑ ãÊÚÏÏ 

If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method:

áÅÚØÇÁ ÇáãÓÊÎÏã ÎíÇÑÇÊ ÚäÏ ÇáÓÄÇá äÓÊÎÏã ÇáØÑíŞÉ `choice`
íãßä æÖÚ ãÕİæİÉ İíåÇ Şíã ÇİÊÑÇÖíÉ ÅĞÇ áã íÊã ÇÎÊíÇÑ Ãí ÎíÇÑ æÊæÖÚ ßãÊÛíÑ ËÇáË

    $name = $this->choice(
        'What is your name?',
        ['Taylor', 'Dayle'],
        $defaultIndex
    );

In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted:

æ ááØÑíŞÉ ãÊÛíÑ ÑÇÈÚ æ ÎÇãÓ ÇÎÊíÇÑíÉ áÊÍÏíÏ ÚÏÏ ÇáãÍÇæáÇÊ 

    $name = $this->choice(
        'What is your name?',
        ['Taylor', 'Dayle'],
        $defaultIndex,
        $maxAttempts = null,
        $allowMultipleSelections = false
    );

<a name="writing-output"></a> ßÊÇÈÉ ÎÑÌ 
### Writing Output ßÊÇÈÉ ÎÑÌ 

To send output to the console, you may use the `line`, `info`, `comment`, `question`, `warn`, and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green colored text:

ÇÓÊÎÏÇã ÇáØÑŞ ÇáÊÇáíÉ `line`, `info`, `comment`, `question`, `warn`, and `error` ßá ØÑíŞÉ ÊÚØí ÎÑÌ Èáæä ãäÇÓÈ
áÚÑÖ ÈÚÖ ÇáãÚáæãÇÊ ááãÓÊÎÏã äÓÊÎÏã ÇáØÑíŞÉ `info` ÓÊÙåÑ Öãä ÇáæÇÌåÉ console ßäÕ Èáæä ÃÎÖÑ
 

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        // ...

        $this->info('The command was successful!');
    }

To display an error message, use the `error` method. Error message text is typically displayed in red:

áÅÙåÇÑ ÑÓÇáÉ ÎØÃ äÓÊÎÏã `error`  æ ÓÊÙåÑ Èáæä ÃÍãÑ 

    $this->error('Something went wrong!');

You may use the `line` method to display plain, uncolored text:

äÓÊÎÏã ÇáØÑíŞÉ `line` áÅÙåÇÑ äÕ ÛíÑ ãáæä 

    $this->line('Display this on the screen');

You may use the `newLine` method to display a blank line:

äÓÊÎÏã ÇáØÑíŞÉ ` newLine ` áÅÙåÇÑ ÓØÑ İÇÑÛ 

    // Write a single blank line...
    $this->newLine();

    // Write three blank lines...
    $this->newLine(3);

<a name="tables"></a> ÇáÌÏÇæá 
#### Tables ÇáÌÏÇæá 

The `table` method makes it easy to correctly format multiple rows / columns of data. All you need to do is provide the column names and the data for the table and Laravel will
automatically calculate the appropriate width and height of the table for you:

äÓÊÎÏã ÇáØÑíŞÉ `table`
äÍÊÇÌ İŞØ ÇÏÎÇá ÇÓã ÇáÚãæÏ æäæÚ ÇáÈíÇäÇÊ
 áÇÑÇİá ÊÍÓÈ ÈÔßá ÏíäÇãíßí ÇáØæá æÇáÚÑÖ ÇáãäÇÓÈíä ááÌÏæá

    use App\Models\User;

    $this->table(
        ['Name', 'Email'],
        User::all(['name', 'email'])->toArray()
    );

<a name="progress-bars"></a> ÔÑíØ ÇáÊŞÏã
#### Progress Bars ÔÑíØ ÇáÊŞÏã

For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `withProgressBar` method, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value:


ÊÚÑÖ ááãÓÊÎÏã ÇáãŞÏÇÑ ÇáãäÌÒ ãä ÇáãåãÉ äÓÊÎÏã ÇáØÑíŞÉ `withProgressBar`

    use App\Models\User;

    $users = $this->withProgressBar(User::all(), function ($user) {
        $this->performTask($user);
    });

Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item:

ÃÍíÇäÇ äÍÊÇÌ áÊÍßã íÏæí ÈÔÑíØ ÇáÊŞÏã äÍÏÏ ÇáÚÏÏ Çáßáí áÎØæÇÊ ÇáÊŞÏã æÈÚÏåÇ ÊÍÓíä ÔÑíØ ÇáÊŞÏã ÈÚÏ ãÚÇáÌÉ ßá ÚäÕÑ 

    $users = App\Models\User::all();

    $bar = $this->output->createProgressBar(count($users));

    $bar->start();

    foreach ($users as $user) {
        $this->performTask($user);

        $bar->advance();
    }

    $bar->finish();

> {tip} For more advanced options, check out the [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html).

áãÒíÏ ãä ÇáÎíÇÑÇÊ ÇáãÊŞÏãÉ ÊİŞÏ ÊæËíŞ ãßæäÇÊ ÔÑíØ ÇáÊŞÏã ááÓíãİæäí
(https://symfony.com/doc/current/components/console/helpers/progressbar.html).
 

<a name="registering-commands"></a> ÊÓÌíá ÇáÃæÇãÑ 
## Registering Commands ÊÓÌíá ÇáÃæÇãÑ 

All of your console commands are registered within your application's `App\Console\Kernel` class, which is your application's "console kernel". Within the `commands` method of this class, you will see a call to the kernel's `load` method. The `load` method will scan the `app/Console/Commands` directory and automatically register each command it contains with Artisan. You are even free to make additional calls to the `load` method to scan other directories for Artisan commands:

ßá ÃæÇãÑ ÔÇÔÉ ÇáÎÑÌ console ÓÌáÊ İí ÇáÕİ `App\Console\Kernel`
Öãä ÇáØÑíŞÉ `commands`  İí åĞÇ ÇáÕİ äÏÇÁ ÇáØÑíŞÉ `load`
ÇáØÑíŞÉ `load` ÊŞæã ÈãÓÍ ãÌáÏ `app/Console/Commands`  ÈÔßá ÏíäÇãíßí áÊÓÌíá ßá ÃãÑ ãæÌæÏ ãÚ Artisan
íãßä äÏÇÁ ØÑíŞÉ `load` ÃÎÑì áãÓÍ ÈŞíÉ ÇáãÌáÏÇÊ áÃæÇãÑ Artisan

    /**
     * Register the commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__.'/Commands');
        $this->load(__DIR__.'/../Domain/Orders/Commands');

        // ...
    }

If necessary, you may manually register commands by adding the command's class name to a `$commands` property within your `App\Console\Kernel` class. If this property is not already defined on your kernel, you should define it manually. When Artisan boots, all the commands listed in this property will be resolved by the [service container](/docs/{{version}}/container) and registered with Artisan:

íãßä íÏæíÇ ÅÖÇİÉ ÇÓã Õİ ÇáÃãÑ Çáì ÇáÎÇÕíÉ `$commands` Öãä ÇáÕİ `App\Console\Kernel`
ÅĞÇ áã Êßä åĞå ÇáÎÇÕíÉ ãÚÑøİÉ Öãä ÇáäæÇÉ íÌÈ ÊÚÑíİåÇ íÏæíÇ ÚäÏ ÇŞáÇÚ Artisan
ßá ŞÇÆãÉ ÇáÃæÇãÑ İí åĞå ÇáÎÇÕíÉ ãÕããÉ ÈæÇÓØÉ [service container](/docs/{{version}}/container)
æãÓÌóáÉ ãÚ Artisan

    protected $commands = [
        Commands\SendEmails::class
    ];

<a name="programmatically-executing-commands"></a> ÊäİíĞ ÇáÃæÇãÑ ÈÑãÌíÇ
## Programmatically Executing Commands  ÊäİíĞ ÇáÃæÇãÑ ÈÑãÌíÇ  

Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned:

ÊäİíĞ ÃæÇãÑ Artisan Öãä ÇáãÓÇÑ route Ãæ ÇáãÊÍßã controller
ÇÓÊÎÏÇã ÇáØÑíŞÉ `call`  İí æÇÌåÉ `Artisan`
åĞå ÇáØÑíŞÉ ÊÃÎĞ İí ÇáãÊÛíÑ ÇáÃæá ÇÓã ÇáÕİ æİí ÇáãÊÛíÑ ÇáËÇäí ãÕİæİÉ ãÊÛíÑÇÊ ÇáÃãÑ
    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function ($user) {
        $exitCode = Artisan::call('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        //
    });

Alternatively, you may pass the entire Artisan command to the `call` method as a string:

ÈÏáÇ" ãä Ğáß íãßä ÅÏÎÇáå ÈÔßá äÕí 

    Artisan::call('mail:send 1 --queue=default');

<a name="passing-array-values"></a> ÊãÑíÑ ãÕİæİÉ Şíã 
#### Passing Array Values ÊãÑíÑ ãÕİæİÉ Şíã 

If your command defines an option that accepts an array, you may pass an array of values to that option:

ÅĞÇ ßÇä ÇáÃãÑ íÍæí ÎíÇÑ íŞÈá ãÕİæİÉ íãÑÑ ãÕİæİÉ Şíã 

    use Illuminate\Support\Facades\Artisan;

    Route::post('/mail', function () {
        $exitCode = Artisan::call('mail:send', [
            '--id' => [5, 13]
        ]);
    });

<a name="passing-boolean-values"></a> ÊãÑíÑ Şíã ãäØŞíÉ 
#### Passing Boolean Values ÊãÑíÑ Şíã ãäØŞíÉ 

If you need to specify the value of an option that does not accept string values, such as the `--force` flag on the `migrate:refresh` command, you should pass `true` or `false` as the value of the option:

ÚäÏ ÊÍÏíÏ ŞíãÉ áÎíÇÑ áíÓÊ äÕíÉ ãËáÇ ŞíãÉ `--force`  İí ÇáÃãÑ `migrate:refresh`
íÌÈ ÊãÑíÑ `true` Ãæ `false  ßŞíãÉ ááÎíÇÑ 

    $exitCode = Artisan::call('migrate:refresh', [
        '--force' => true,
    ]);

<a name="queueing-artisan-commands"></a> Artisan  ÑÊá ÃæÇãÑ 
#### Queueing Artisan Commands Artisan  ÑÊá ÃæÇãÑ 

Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/{{version}}/queues). Before using this method, make sure you have configured your queue and are running a queue listener:

ÇÓÊÎÏÇã ÇáØÑíŞÉ `queue`
ŞÈá ÇÓÊÎÏÇãåÇ ÊÃßÏ ãä ÇÚÏÇÏÇÊ ÇáÑÊá æÊÔÛíá ãÓÊãÚ ÇáÑÊá

    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function ($user) {
        Artisan::queue('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        //
    });

Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to:

ÇÓÊÎÏÇã ÇáØÑŞ`onConnection`  æ `onQueue`  áÊÍÏíÏ áÇÊÕÇá Çæ ÇáÇãÑ ÇáĞí íÌÈ Ãä íÑÓá 

    Artisan::queue('mail:send', [
        'user' => 1, '--queue' => 'default'
    ])->onConnection('redis')->onQueue('commands');

<a name="calling-commands-from-other-commands"></a> äÏÇÁ ÃæÇãÑ ãä ÃæÇãÑ ÃÎÑì 
### Calling Commands From Other Commands äÏÇÁ ÃæÇãÑ ãä ÃæÇãÑ ÃÎÑì 

Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options:

äÓÊÎÏã ÇáØÑíŞÉ`call`  ÊŞÈá ÇÓã ÇáÃãÑ æãÕİæİÉ ÈÇáÎíÇÑÇÊ æÇáãÊÛíÑÇÊ 

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->call('mail:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    }

If you would like to call another console command and suppress all of its output, you may use the `callSilently` method. The `callSilently` method has the same signature as the `call` method:

ÇáØÑíŞÉ `callSilently` áäÏÇÁ ÃãÑ console  ÃÎÑ æ ßÊã ÎÑÌå 

    $this->callSilently('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

<a name="signal-handling"></a> ãÚÇáÌÉ ÇáÅÔÇÑÉ
## Signal Handling ãÚÇáÌÉ ÇáÅÔÇÑÉ

The Symfony Console component, which powers the Artisan console, allows you to indicate which process signals (if any) your command handles. For example, you may indicate that your command handles the `SIGINT` and `SIGTERM` signals.

To get started, you should implement the `Symfony\Component\Console\Command\SignalableCommandInterface` interface on your Artisan command class. This interface requires you to define two methods: `getSubscribedSignals` and `handleSignal`:

íÌÈ ÊÍŞíŞ ÇáæÇÌåÉ `Symfony\Component\Console\Command\SignalableCommandInterface` 
İí Õİ ÃãÑ Artisan
ÊÊØáÈ ÊÚÑíİ ØÑíŞÊíä`getSubscribedSignals`  æ`handleSignal`
 

```php
<?php

use Symfony\Component\Console\Command\SignalableCommandInterface;

class StartServer extends Command implements SignalableCommandInterface
{
    // ...

    /**
     * Get the list of signals handled by the command.
     *
     * @return array
     */
    public function getSubscribedSignals(): array
    {
        return [SIGINT, SIGTERM];
    }

    /**
     * Handle an incoming signal.
     *
     * @param  int  $signal
     * @return void
     */
    public function handleSignal(int $signal): void
    {
        if ($signal === SIGINT) {
            $this->stopServer();

            return;
        }
    }
}
```

As you might expect, the `getSubscribedSignals` method should return an array of the signals that your command can handle, while the `handleSignal` method receives the signal and can respond accordingly.

ÇáØÑíŞÉ `getSubscribedSignals`  ÊÚíÏ ãÕİæİÉ ÅÔÇÑÇÊ íÚÇáÌåÇ ÇáÃãÑ 
ÇáØÑíŞÉ `handleSignal`  ÊÓÊŞÈá ÇáÅÔÇÑÇÊ

<a name="stub-customization"></a> ÊÎÕíÕ ÌÒÁ 
## Stub Customization ÊÎÕíÕ ÌÒÁ 
The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them:

ÃæÇãÑ Artisan console's `make` áÅäÔÇÁ Õİæİ ãËá controllers æ jobs æ migrations æ tests
åĞå ÇáÕİæİ ÊÓÊÎÏã ãáİÇÊ stub
ÊÊÖãä Şíã ÊÚÊãÏ Úáì ÏÎáß
äÓÊÎÏã`stub:publish`  áäÔÑ stubs İí ÇáÊØÈíŞ ÈÇáÊÇáí íãßä ÊÎÕíÕåã



```shell
php artisan stub:publish
```

The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands.

ÊÊæÖÚ stubs Öãä ãÌáÏ stubs İí ÌĞÑ ÇáÊØÈíŞ 

<a name="events"></a> ÇáÃÍÏÇË 
## Events ÇáÃÍÏÇË 

Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing.


ÊÑÓá Artisan ËáÇË ÃÍÏÇË ÚäÏ ÊÔÛíá ÇáÃæÇãÑ
`Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.
ÇáÍÏË `ArtisanStarting`  íõÑÓá ãÈÇÔÑÉ ÚäÏ ÊÔÛíá artisan
ÇáÍÏË`CommandStarting`  íõÑÓá ãÈÇÔÑÉ ŞÈá ÊÔÛíá ÇáÃãÑ
ÇáÍÏË`CommandFinished`  íõÑÓá ãÈÇÔÑÉ ÚäÏ ÇäÊåÇÁ ÊäİíĞ ÇáÃãÑ


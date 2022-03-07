# Artisan Console وحدة تحكم الحرفي الماهر 

- [Introduction](#introduction) المقدمة
    - [Tinker (REPL)](#tinker) متعدد المهام 
- [Writing Commands](#writing-commands) كتابة الأوامر 
    - [Generating Commands](#generating-commands) توليد الأوامر 
    - [Command Structure](#command-structure) بنية الأوامر  
    - [Closure Commands](#closure-commands) أوامر نطاق الإغلاق 
- [Defining Input Expectations](#defining-input-expectations) تحديد الدخل المتوقع 
    - [Arguments](#arguments) المتغيرات
    - [Options](#options) الخيارات 
    - [Input Arrays](#input-arrays) مصفوفة الادخال 
    - [Input Descriptions](#input-descriptions) وصف الإدخال
- [Command I/O](#command-io) أوامر الدخل والخرج
    - [Retrieving Input](#retrieving-input) استرجاع الدخل
    - [Prompting For Input](#prompting-for-input) تلقين الدخل 
    - [Writing Output](#writing-output) كتابة الخرج
- [Registering Commands](#registering-commands) تسجيل الأوامر 
- [Programmatically Executing Commands](#programmatically-executing-commands) تنفيذ الأوامر برمجيا 
    - [Calling Commands From Other Commands](#calling-commands-from-other-commands) نداء الأوامر من أوامر أخرى 
- [Signal Handling](#signal-handling) معالجة الإشارة 
- [Stub Customization](#stub-customization) تخصيص جزء
- [Events](#events) الأحداث 

<a name="introduction"></a> المقدمة 
## Introduction المقدمة 

Artisan is the command line interface included with Laravel. Artisan exists at the root of your application as the `artisan` script and provides a number of helpful commands that can assist you while you build your application. To view a list of all available Artisan commands, you may use the `list` command:

(Artisan) واجهة الأوامر الخاصة بلارافل، موجود ضمن التطبيق كسكريبت `artisan` 
                                                                       يؤمن العديد من الأوامر المساعدة أثناء بناء التطبيق، لروؤية قائمة الأوامر نكتب الأمر التالي 
 

```shell
php artisan list
```


Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`:

كل أمر أيضا يتضمن شاشة المساعدة ("help" screen) لعرض ووصف متغيرات وخيارات الأوامر 
لعرض شاشة المساعدة لأمر نكتب help وبعدها الأمر 
 

```shell
php artisan help migrate
```

<a name="laravel-sail"></a> شراع لارافل 
#### Laravel Sail شراع لارافل 

If you are using [Laravel Sail](/docs/{{version}}/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers:

إذا كنت تستخدم Laravel Sail في بيئة التطوير المحلية استخدم الأمر `sail` لنداء أوامر Artisan 
Sail سوف ينفذ أوامر Artisan ضمن حاويات Docker
 

```shell
./sail artisan list
```

<a name="tinker"></a> متعدد المهام 
### Tinker (REPL) متعدد المهام 

Laravel Tinker is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package.

هو واجهة الأوامر السوداء الخاصة بلارافل powerful REPL 
REPL (read-eval-print-loop) نوع من الواجهات السوداء التفاعلية التي تأخذ مدخلات مستخدم وحيد و يقيم المدخلات و يعيد النتيجة للمستخدم
مشغلة بواسطة حزمة (https://github.com/bobthecow/psysh)  PsySH
 

<a name="installation"></a> التنصيب
#### Installation التنصيب

All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application:

التنكر مضمن افتراضيا بتطبيقات اللارافل لكن يمكنك استخدام Composer لتنصيبه في حال حذفه من التطبيق 


```shell
composer require laravel/tinker
```

> {tip} Looking for a graphical UI for interacting with your Laravel application? Check out [Tinkerwell](https://tinkerwell.app)!

للبحث عن واجهة رسومية للتفاعل مع تطبيق لارافل 
راجع الرابط https://tinkerwell.app


<a name="usage"></a> الاستخدام
#### Usage الاستخدام

Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command:

التنكر يسمح لك التفاعل مع تطبيق اللارافل في واجهة الأوامر و المودلات و الاعمال و الاحداث
لدخول بيئة التنكر نفذ الأمر 


```shell
php artisan tinker
```

You can publish Tinker's configuration file using the `vendor:publish` command:	

لنشر ملف اعدادات التنكر نفذ الأمر


```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> {note} The `dispatch` helper function and `dispatch` method on the `Dispatchable` class depends on garbage collection to place the job on the queue. Therefore, when using tinker, you should use `Bus::dispatch` or `Queue::push` to dispatch jobs.

*ملاحظة: الدالة المساعدة `dispatch`  و الطريقة `dispatch` الموجودة ضمن كلاس `Dispatchable` 
تعتمد على وضع العمل ضمن رتل و بالتالي عند استخدام التنكر يجب استخدام `Bus::dispatch`
أو `Queue::push`  لإرسال الأعمال 


<a name="command-allow-list"></a> قائمة السماحية
#### Command Allow List قائمة السماحية

Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, and `up` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file:

يستخدم التنكر قائمة السماحية لتحديد أوامر Artisan التي تنفذ ضمن ال shell الخاص به
يمكن تنفيذ الأوامر التالية `clear-compiled`, `down`, `env`,`inspire`, `migrate`, `optimize`, and `up`
إذا أردت السماح بأوامر أكثر يمكننك اضافتهم لمصفوفة الأوامر في ملف اعدادات التنكر `tinker.php`


    'commands' => [
        // App\Console\Commands\ExampleCommand::class,
    ],

<a name="classes-that-should-not-be-aliased"></a> صفوف لا يجب أن تستخدم اسم مستعار أو اختصار 
#### Classes That Should Not Be Aliased صفوف لا يجب أن تستخدم اسم مستعار أو اختصار 

Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file:

عادة التنكر يضع أسماء مستعارة للصفوف اذا أردت عدم الاختصار ضعهم في مصفوفة ضمن ملف اعدادات التنكر 


    'dont_alias' => [
        App\Models\User::class,
    ],

<a name="writing-commands"></a>  كتابة الأوامر
## Writing Commands كتابة الأوامر
In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be loaded by Composer.

يمكنك صنع أوامر خاصة بك و تخزن عادة في مجلد `app/Console/Commands`  و يمكنك تخزينها بأي مجلد تريده طالما يقوم Composer بتحميلها 

<a name="generating-commands"></a>  توليد الأوامر
### Generating Commands توليد الأوامر

To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command:

لانشاء امر جديد نستخدم الامر `make:command`	
ينشأ صف أمر جديد ضمن `app/Console/Commands`  اذا لم يكن موجود المجلد ينشأ تلقائيا عند تنفيذ الأمر


```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a> بنية الأمر
### Command Structure بنية الأمر

After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method.

بعد توليد الأمر يجب تعريف قيم مناسبة للخاصيتين `signature` و `description`
هذه الخصائص تستخدم عند عرض أمرك في شاشة القائمة
signature  تستخدم لتحديد الدخل المتوقع للأمر
الطريقة handle يتم ندائها عند تنفيذ الأمر


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

<a name="closure-commands"></a> أوامر النطاق المغلق
### Closure Commands أوامر النطاق المغلق
Closure based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. Within the `commands` method of your `app/Console/Kernel.php` file, Laravel loads the `routes/console.php` file:

يعتمد Closure على أوامر تؤمن بديل لتحديد أوامر console كصفوف 
بنفس الطريقة مسار closures بديل المتحكمات controllers
أمر closures بديل لأمر classes
ضمن الطريقة `commands`  الموجودة في الملف `app/Console/Kernel.php`  تقوم لارافل بتحميل ملف  `routes/console.php`

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

هذا الملف لا يحدد مسارات HTTP يحدد المسارات الداخلية في التطبيق
في هذا الملف يمكن تحديد النطاق المغلق المتعمد على أوامر console باستخدام الطريقة `Artisan::command`
الطريقة `command` تأخذ متغيرين الأول [command signature] و الثاني النطاق المغلق الذي سيرسل متغيرات و خيارات الأمر


    Artisan::command('mail:send {user}', function ($user) {
        $this->info("Sending email to: {$user}!");
    });

The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class.

النطاق المغلق يعطي تحكم كامل بالطرق المساعدة بالتالي تحكم بكامل صف الأمر

<a name="type-hinting-dependencies"></a>
#### Type-Hinting Dependencies

In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/{{version}}/container):

بالإضافة لاستقبال المتغيرات أمر النطاق المغلق يقوم بكتابة تلميح إضافي معتمد

    use App\Models\User;
    use App\Support\DripEmailer;

    Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
        $drip->send(User::find($user));
    });

<a name="closure-command-descriptions"></a>  وصف أمر النطاق المغلق 
#### Closure Command Descriptions وصف أمر النطاق المغلق 

When defining a closure based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands:

استخدام الطريقة `purpose` لكتابة وصف للأمر 
هذا الوصف يظهر عند تشغيل الأمر `php artisan help`  أو الأمر `php artisan list`
 

    Artisan::command('mail:send {user}', function ($user) {
        // ...
    })->purpose('Send a marketing email to a user');

<a name="defining-input-expectations"></a> تحديد الدخل المتوقع 
## Defining Input Expectations تحديد الدخل المتوقع 

When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax.

لتحديد الدخل المتوقع من المستخدم نستخدم الخاصية `signature` تسمح بتحديد الاسم والمتغيرات والخيارات 

<a name="arguments"></a> المتغيرات 
### Arguments المتغيرات 

All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`:

   توضع المتغيرات ضمن قوسين من الشكل {argument name}
    في هذا المثال تحديد متغير واحد اجباري 
 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

You may also make arguments optional or define default values for arguments:

   يمكن إضافة متغيرات اختيارية أو وضع قيم افتراضية لمتغيرات 

    // Optional argument...
    'mail:send {user?}'

    // Optional argument with default value...
    'mail:send {user=foo}'

<a name="options"></a> الخيارات 
### Options الخيارات 

Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are provided via the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option:

الخيارات مثل المتغيرات أيضا دخل من المستخدم نضع قبلها لاحقة (`--`)
يوجد نوعين من الخيارات الأول لا يستقبل قيمة والنوع الثاني يأخذ قيمة
النوع الأول تكون قيمته true أو false 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue}';

In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`:

إذا مررنا –queue تكون قيمه true غير ذلك قيمته false

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a> خيارات مع قيم
#### Options With Values  خيارات مع قيم 

Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign:


النوع الثاني تحديد قيمة للخيار باستخدام إشارة `=`

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user} {--queue=}';

In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`:

اذا لم نحدد الدخل تكون قيمته null 
 

```shell
php artisan mail:send 1 --queue=default
```

You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used:

يمكن وضع قيمة افتراضية إذا لم يمرر المستخدم قيمة يأخذ الخيار القيمة الافتراضية 

    'mail:send {user} {--queue=default}'

<a name="option-shortcuts"></a> اختصارات الخيار
#### Option Shortcuts اختصارات الخيار

To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name:

لتحديد اختصار نضعه قبل اسم الخيار و نضع  `|` للفصل بين الاختصار و اسم الخيار 

    'mail:send {user} {--Q|queue}'

When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen:

نستخدم الاختصار ضمن شاشة الأوامر 

```shell
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a> إدخال المصفوفات 
### Input Arrays إدخال المصفوفات 

If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument:

لإدخال أكثر من قيمة دخل نستخدم `*` 

    'mail:send {user*}'

When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `foo` and `bar` as its values:

يمكن للمستخدم وضع أكثر من قيمة 

```shell
php artisan mail:send foo bar
```

This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument:

يمكن استخدام `*`  مع المتغيرات الاختيارية 

    'mail:send {user?*}'

<a name="option-arrays"></a> مصفوفات الخيار
#### Option Arrays مصفوفات الخيار 

When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name:

لتحديد خيار متعدد القيم

    'mail:send {user} {--id=*}'

Such a command may be invoked by passing multiple `--id` arguments:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>  وصف الدخل 
### Input Descriptions وصف الدخل 

You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines:

لوضع وصف للدخل نضع : بعد الاسم ثم الوصف 

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send
                            {user : The ID of the user}
                            {--queue : Whether the job should be queued}';

<a name="command-io"></a> أمر الدخل والخرج 
## Command I/O أمر الدخل والخرج 

<a name="retrieving-input"></a> استرجاع الدخل 
### Retrieving Input استرجاع الدخل 

While your command is executing, you will likely need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods. If an argument or option does not exist, `null` will be returned:

عند تنفيذ الأمر نحتاج الوصول للمتغيرات او الخيارات نستخدم الطريقة `argument`   والطريقة `option`
إذا كان المتغير او الخيار غير موجود يعيد قيمة `null`

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

لاسترجاع كل المتغيرات كمصفوفة نستخدم الطريقة `arguments`
 

    $arguments = $this->arguments();

Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method:

لاسترجاع الخيارات نستخدم الطريقة `option`
لاسترجاع أكثر من قيمة كمصفوفة `options`
 

    // Retrieve a specific option...
    $queueName = $this->option('queue');

    // Retrieve all options as an array...
    $options = $this->options();

<a name="prompting-for-input"></a> تلقين الدخل 
### Prompting For Input تلقين الدخل 

In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command:


لسؤال المستخدم ليقوم بالإدخال نستخدم الطريقة `ask` 

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

الطريقة `secret` تشبه الطريقة `ask` لكن الدخل غير مرئي تستخدم عند إدخال بيانات حساسة مثل كلمات المرور 

    $password = $this->secret('What is the password?');

<a name="asking-for-confirmation"></a> السؤال للتأكيد 
#### Asking For Confirmation السؤال للتأكيد 

If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`.

السؤال للتأكيد نستخدم الطريقة `confirm` ليدخل المستخدم yes أو no 
افتراضيا تعيد قيمة false 
إذا أدخل المستخدم yes او y تعيد true 
 

    if ($this->confirm('Do you wish to continue?')) {
        //
    }

If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method:

لتعيد قيمة افتراضية true نضعها كمتغير ثاني 

    if ($this->confirm('Do you wish to continue?', true)) {
        //
    }

<a name="auto-completion"></a> الإكمال التلقائي 
#### Auto-Completion الإكمال التلقائي 

The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints:

الطريقة `anticipate`  توفر إكمال تلقائي للخيارات الممكنة 

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion:

يمكن تمرير closure كمتغير ثاني للطريقة `anticipate`  
closure يستدعى في كل مرة يكتب فيها المستخدم محرف 
closure  يقبل متغير نوع نصي يتضمن أيضا دخل المستخدم و يعيد مصفوفة خيارات للإكمال التلقائي

    $name = $this->anticipate('What is your address?', function ($input) {
        // Return auto-completion options...
    });

<a name="multiple-choice-questions"></a> أسئلة خيار متعدد 
#### Multiple Choice Questions أسئلة خيار متعدد 

If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method:

لإعطاء المستخدم خيارات عند السؤال نستخدم الطريقة `choice`
يمكن وضع مصفوفة فيها قيم افتراضية إذا لم يتم اختيار أي خيار وتوضع كمتغير ثالث

    $name = $this->choice(
        'What is your name?',
        ['Taylor', 'Dayle'],
        $defaultIndex
    );

In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted:

و للطريقة متغير رابع و خامس اختيارية لتحديد عدد المحاولات 

    $name = $this->choice(
        'What is your name?',
        ['Taylor', 'Dayle'],
        $defaultIndex,
        $maxAttempts = null,
        $allowMultipleSelections = false
    );

<a name="writing-output"></a> كتابة خرج 
### Writing Output كتابة خرج 

To send output to the console, you may use the `line`, `info`, `comment`, `question`, `warn`, and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green colored text:

استخدام الطرق التالية `line`, `info`, `comment`, `question`, `warn`, and `error` كل طريقة تعطي خرج بلون مناسب
لعرض بعض المعلومات للمستخدم نستخدم الطريقة `info` ستظهر ضمن الواجهة console كنص بلون أخضر
 

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

لإظهار رسالة خطأ نستخدم `error`  و ستظهر بلون أحمر 

    $this->error('Something went wrong!');

You may use the `line` method to display plain, uncolored text:

نستخدم الطريقة `line` لإظهار نص غير ملون 

    $this->line('Display this on the screen');

You may use the `newLine` method to display a blank line:

نستخدم الطريقة ` newLine ` لإظهار سطر فارغ 

    // Write a single blank line...
    $this->newLine();

    // Write three blank lines...
    $this->newLine(3);

<a name="tables"></a> الجداول 
#### Tables الجداول 

The `table` method makes it easy to correctly format multiple rows / columns of data. All you need to do is provide the column names and the data for the table and Laravel will
automatically calculate the appropriate width and height of the table for you:

نستخدم الطريقة `table`
نحتاج فقط ادخال اسم العمود ونوع البيانات
 لارافل تحسب بشكل ديناميكي الطول والعرض المناسبين للجدول

    use App\Models\User;

    $this->table(
        ['Name', 'Email'],
        User::all(['name', 'email'])->toArray()
    );

<a name="progress-bars"></a> شريط التقدم
#### Progress Bars شريط التقدم

For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `withProgressBar` method, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value:


تعرض للمستخدم المقدار المنجز من المهمة نستخدم الطريقة `withProgressBar`

    use App\Models\User;

    $users = $this->withProgressBar(User::all(), function ($user) {
        $this->performTask($user);
    });

Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item:

أحيانا نحتاج لتحكم يدوي بشريط التقدم نحدد العدد الكلي لخطوات التقدم وبعدها تحسين شريط التقدم بعد معالجة كل عنصر 

    $users = App\Models\User::all();

    $bar = $this->output->createProgressBar(count($users));

    $bar->start();

    foreach ($users as $user) {
        $this->performTask($user);

        $bar->advance();
    }

    $bar->finish();

> {tip} For more advanced options, check out the [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html).

لمزيد من الخيارات المتقدمة تفقد توثيق مكونات شريط التقدم للسيمفوني
(https://symfony.com/doc/current/components/console/helpers/progressbar.html).
 

<a name="registering-commands"></a> تسجيل الأوامر 
## Registering Commands تسجيل الأوامر 

All of your console commands are registered within your application's `App\Console\Kernel` class, which is your application's "console kernel". Within the `commands` method of this class, you will see a call to the kernel's `load` method. The `load` method will scan the `app/Console/Commands` directory and automatically register each command it contains with Artisan. You are even free to make additional calls to the `load` method to scan other directories for Artisan commands:

كل أوامر شاشة الخرج console سجلت في الصف `App\Console\Kernel`
ضمن الطريقة `commands`  في هذا الصف نداء الطريقة `load`
الطريقة `load` تقوم بمسح مجلد `app/Console/Commands`  بشكل ديناميكي لتسجيل كل أمر موجود مع Artisan
يمكن نداء طريقة `load` أخرى لمسح بقية المجلدات لأوامر Artisan

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

يمكن يدويا إضافة اسم صف الأمر الى الخاصية `$commands` ضمن الصف `App\Console\Kernel`
إذا لم تكن هذه الخاصية معرّفة ضمن النواة يجب تعريفها يدويا عند اقلاع Artisan
كل قائمة الأوامر في هذه الخاصية مصممة بواسطة [service container](/docs/{{version}}/container)
ومسجَلة مع Artisan

    protected $commands = [
        Commands\SendEmails::class
    ];

<a name="programmatically-executing-commands"></a> تنفيذ الأوامر برمجيا
## Programmatically Executing Commands  تنفيذ الأوامر برمجيا  

Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned:

تنفيذ أوامر Artisan ضمن المسار route أو المتحكم controller
استخدام الطريقة `call`  في واجهة `Artisan`
هذه الطريقة تأخذ في المتغير الأول اسم الصف وفي المتغير الثاني مصفوفة متغيرات الأمر
    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function ($user) {
        $exitCode = Artisan::call('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        //
    });

Alternatively, you may pass the entire Artisan command to the `call` method as a string:

بدلا" من ذلك يمكن إدخاله بشكل نصي 

    Artisan::call('mail:send 1 --queue=default');

<a name="passing-array-values"></a> تمرير مصفوفة قيم 
#### Passing Array Values تمرير مصفوفة قيم 

If your command defines an option that accepts an array, you may pass an array of values to that option:

إذا كان الأمر يحوي خيار يقبل مصفوفة يمرر مصفوفة قيم 

    use Illuminate\Support\Facades\Artisan;

    Route::post('/mail', function () {
        $exitCode = Artisan::call('mail:send', [
            '--id' => [5, 13]
        ]);
    });

<a name="passing-boolean-values"></a> تمرير قيم منطقية 
#### Passing Boolean Values تمرير قيم منطقية 

If you need to specify the value of an option that does not accept string values, such as the `--force` flag on the `migrate:refresh` command, you should pass `true` or `false` as the value of the option:

عند تحديد قيمة لخيار ليست نصية مثلا قيمة `--force`  في الأمر `migrate:refresh`
يجب تمرير `true` أو `false  كقيمة للخيار 

    $exitCode = Artisan::call('migrate:refresh', [
        '--force' => true,
    ]);

<a name="queueing-artisan-commands"></a> Artisan  رتل أوامر 
#### Queueing Artisan Commands Artisan  رتل أوامر 

Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/{{version}}/queues). Before using this method, make sure you have configured your queue and are running a queue listener:

استخدام الطريقة `queue`
قبل استخدامها تأكد من اعدادات الرتل وتشغيل مستمع الرتل

    use Illuminate\Support\Facades\Artisan;

    Route::post('/user/{user}/mail', function ($user) {
        Artisan::queue('mail:send', [
            'user' => $user, '--queue' => 'default'
        ]);

        //
    });

Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to:

استخدام الطرق`onConnection`  و `onQueue`  لتحديد لاتصال او الامر الذي يجب أن يرسل 

    Artisan::queue('mail:send', [
        'user' => 1, '--queue' => 'default'
    ])->onConnection('redis')->onQueue('commands');

<a name="calling-commands-from-other-commands"></a> نداء أوامر من أوامر أخرى 
### Calling Commands From Other Commands نداء أوامر من أوامر أخرى 

Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options:

نستخدم الطريقة`call`  تقبل اسم الأمر ومصفوفة بالخيارات والمتغيرات 

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

الطريقة `callSilently` لنداء أمر console  أخر و كتم خرجه 

    $this->callSilently('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

<a name="signal-handling"></a> معالجة الإشارة
## Signal Handling معالجة الإشارة

The Symfony Console component, which powers the Artisan console, allows you to indicate which process signals (if any) your command handles. For example, you may indicate that your command handles the `SIGINT` and `SIGTERM` signals.

To get started, you should implement the `Symfony\Component\Console\Command\SignalableCommandInterface` interface on your Artisan command class. This interface requires you to define two methods: `getSubscribedSignals` and `handleSignal`:

يجب تحقيق الواجهة `Symfony\Component\Console\Command\SignalableCommandInterface` 
في صف أمر Artisan
تتطلب تعريف طريقتين`getSubscribedSignals`  و`handleSignal`
 

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

الطريقة `getSubscribedSignals`  تعيد مصفوفة إشارات يعالجها الأمر 
الطريقة `handleSignal`  تستقبل الإشارات

<a name="stub-customization"></a> تخصيص جزء 
## Stub Customization تخصيص جزء 
The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them:

أوامر Artisan console's `make` لإنشاء صفوف مثل controllers و jobs و migrations و tests
هذه الصفوف تستخدم ملفات stub
تتضمن قيم تعتمد على دخلك
نستخدم`stub:publish`  لنشر stubs في التطبيق بالتالي يمكن تخصيصهم



```shell
php artisan stub:publish
```

The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands.

تتوضع stubs ضمن مجلد stubs في جذر التطبيق 

<a name="events"></a> الأحداث 
## Events الأحداث 

Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing.


ترسل Artisan ثلاث أحداث عند تشغيل الأوامر
`Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.
الحدث `ArtisanStarting`  يُرسل مباشرة عند تشغيل artisan
الحدث`CommandStarting`  يُرسل مباشرة قبل تشغيل الأمر
الحدث`CommandFinished`  يُرسل مباشرة عند انتهاء تنفيذ الأمر


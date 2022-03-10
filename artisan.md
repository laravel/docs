Artisan Console وحدة تحكم الحرفي الماهر
Introduction المقدمة
Tinker (REPL) متعدد المهام
Writing Commands كتابة الأوامر
Generating Commands توليد الأوامر
Command Structure بنية الأوامر
Closure Commands أوامر نطاق الإغلاق
Defining Input Expectations تحديد الدخل المتوقع
Arguments المتغيرات
Options الخيارات
Input Arrays مصفوفة الادخال
Input Descriptions وصف الإدخال
Command I/O أوامر الدخل والخرج
Retrieving Input استرجاع الدخل
Prompting For Input تلقين الدخل
Writing Output كتابة الخرج
Registering Commands تسجيل الأوامر
Programmatically Executing Commands تنفيذ الأوامر برمجيا
Calling Commands From Other Commands نداء الأوامر من أوامر أخرى
Signal Handling معالجة الإشارة
Stub Customization تخصيص جزء
Events الأحداث
المقدمة

Introduction المقدمة
واجهة الأوامر الخاصة بلارافل، موجود ضمن التطبيق كسكريبت artisan

يؤمن العديد من الأوامر المساعدة أثناء بناء التطبيق، لروؤية قائمة الأوامر نكتب الأمر التالي

php artisan list
``

كل أمر أيضا يتضمن شاشة المساعدة ("help" screen) لعرض ووصف متغيرات وخيارات الأوامر 
لعرض شاشة المساعدة لأمر نكتب help وبعدها الأمر 
 

```shell
php artisan help migrate
شراع لارافل

Laravel Sail شراع لارافل
إذا كنت تستخدم Laravel Sail في بيئة التطوير المحلية استخدم الأمر sail لنداء أوامر Artisan Sail سوف ينفذ أوامر Artisan ضمن حاويات Docker

./sail artisan list
متعدد المهام

Tinker (REPL) متعدد المهام
هو واجهة الأوامر السوداء الخاصة بلارافل powerful REPL REPL (read-eval-print-loop) نوع من الواجهات السوداء التفاعلية التي تأخذ مدخلات مستخدم وحيد و يقيم المدخلات و يعيد النتيجة للمستخدم مشغلة بواسطة حزمة (https://github.com/bobthecow/psysh) PsySH

التنصيب

Installation التنصيب
التنكر مضمن افتراضيا بتطبيقات اللارافل لكن يمكنك استخدام Composer لتنصيبه في حال حذفه من التطبيق

composer require laravel/tinker
للبحث عن واجهة رسومية للتفاعل مع تطبيق لارافل راجع الرابط https://tinkerwell.app

الاستخدام

Usage الاستخدام
التنكر يسمح لك التفاعل مع تطبيق اللارافل في واجهة الأوامر و المودلات و الاعمال و الاحداث لدخول بيئة التنكر نفذ الأمر

php artisan tinker
لنشر ملف اعدادات التنكر نفذ الأمر

php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
*ملاحظة: الدالة المساعدة dispatch و الطريقة dispatch الموجودة ضمن كلاس Dispatchable تعتمد على وضع العمل ضمن رتل و بالتالي عند استخدام التنكر يجب استخدام Bus::dispatch أو Queue::push لإرسال الأعمال

قائمة السماحية

Command Allow List قائمة السماحية
يستخدم التنكر قائمة السماحية لتحديد أوامر Artisan التي تنفذ ضمن ال shell الخاص به يمكن تنفيذ الأوامر التالية clear-compiled, down, env,inspire, migrate, optimize, and up إذا أردت السماح بأوامر أكثر يمكننك اضافتهم لمصفوفة الأوامر في ملف اعدادات التنكر tinker.php

'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
صفوف لا يجب أن تستخدم اسم مستعار أو اختصار

Classes That Should Not Be Aliased صفوف لا يجب أن تستخدم اسم مستعار أو اختصار
عادة التنكر يضع أسماء مستعارة للصفوف اذا أردت عدم الاختصار ضعهم في مصفوفة ضمن ملف اعدادات التنكر

'dont_alias' => [
    App\Models\User::class,
],
كتابة الأوامر

Writing Commands كتابة الأوامر
يمكنك صنع أوامر خاصة بك و تخزن عادة في مجلد app/Console/Commands و يمكنك تخزينها بأي مجلد تريده طالما يقوم Composer بتحميلها

توليد الأوامر

Generating Commands توليد الأوامر
لانشاء امر جديد نستخدم الامر make:command ينشأ صف أمر جديد ضمن app/Console/Commands اذا لم يكن موجود المجلد ينشأ تلقائيا عند تنفيذ الأمر

php artisan make:command SendEmails
بنية الأمر

Command Structure بنية الأمر
بعد توليد الأمر يجب تعريف قيم مناسبة للخاصيتين signature و description هذه الخصائص تستخدم عند عرض أمرك في شاشة القائمة signature تستخدم لتحديد الدخل المتوقع للأمر الطريقة handle يتم ندائها عند تنفيذ الأمر

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
أوامر النطاق المغلق

Closure Commands أوامر النطاق المغلق
يعتمد Closure على أوامر تؤمن بديل لتحديد أوامر console كصفوف بنفس الطريقة مسار closures بديل المتحكمات controllers أمر closures بديل لأمر classes ضمن الطريقة commands الموجودة في الملف app/Console/Kernel.php تقوم لارافل بتحميل ملف routes/console.php

/**
 * Register the closure based commands for the application.
 *
 * @return void
 */
protected function commands()
{
    require base_path('routes/console.php');
}
هذا الملف لا يحدد مسارات HTTP يحدد المسارات الداخلية في التطبيق في هذا الملف يمكن تحديد النطاق المغلق المتعمد على أوامر console باستخدام الطريقة Artisan::command الطريقة command تأخذ متغيرين الأول [command signature] و الثاني النطاق المغلق الذي سيرسل متغيرات و خيارات الأمر

Artisan::command('mail:send {user}', function ($user) {
    $this->info("Sending email to: {$user}!");
});
النطاق المغلق يعطي تحكم كامل بالطرق المساعدة بالتالي تحكم بكامل صف الأمر


Type-Hinting Dependencies
بالإضافة لاستقبال المتغيرات أمر النطاق المغلق يقوم بكتابة تلميح إضافي معتمد

use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
    $drip->send(User::find($user));
});
وصف أمر النطاق المغلق

Closure Command Descriptions وصف أمر النطاق المغلق
استخدام الطريقة purpose لكتابة وصف للأمر هذا الوصف يظهر عند تشغيل الأمر php artisan help أو الأمر php artisan list

Artisan::command('mail:send {user}', function ($user) {
    // ...
})->purpose('Send a marketing email to a user');
تحديد الدخل المتوقع

Defining Input Expectations تحديد الدخل المتوقع
لتحديد الدخل المتوقع من المستخدم نستخدم الخاصية signature تسمح بتحديد الاسم والمتغيرات والخيارات

المتغيرات

Arguments المتغيرات
توضع المتغيرات ضمن قوسين من الشكل {argument name} في هذا المثال تحديد متغير واحد اجباري

/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
يمكن إضافة متغيرات اختيارية أو وضع قيم افتراضية لمتغيرات

// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
الخيارات

Options الخيارات
الخيارات مثل المتغيرات أيضا دخل من المستخدم نضع قبلها لاحقة (--) يوجد نوعين من الخيارات الأول لا يستقبل قيمة والنوع الثاني يأخذ قيمة النوع الأول تكون قيمته true أو false

/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
إذا مررنا –queue تكون قيمه true غير ذلك قيمته false

php artisan mail:send 1 --queue
خيارات مع قيم

Options With Values خيارات مع قيم
النوع الثاني تحديد قيمة للخيار باستخدام إشارة =

/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
اذا لم نحدد الدخل تكون قيمته null

php artisan mail:send 1 --queue=default
يمكن وضع قيمة افتراضية إذا لم يمرر المستخدم قيمة يأخذ الخيار القيمة الافتراضية

'mail:send {user} {--queue=default}'
اختصارات الخيار

Option Shortcuts اختصارات الخيار
لتحديد اختصار نضعه قبل اسم الخيار و نضع | للفصل بين الاختصار و اسم الخيار

'mail:send {user} {--Q|queue}'
نستخدم الاختصار ضمن شاشة الأوامر

php artisan mail:send 1 -Q
إدخال المصفوفات

Input Arrays إدخال المصفوفات
لإدخال أكثر من قيمة دخل نستخدم *

'mail:send {user*}'
يمكن للمستخدم وضع أكثر من قيمة

php artisan mail:send foo bar
This * character can be combined with an optional argument definition to allow zero or more instances of an argument:

يمكن استخدام * مع المتغيرات الاختيارية

'mail:send {user?*}'
مصفوفات الخيار

Option Arrays مصفوفات الخيار
لتحديد خيار متعدد القيم

'mail:send {user} {--id=*}'
Such a command may be invoked by passing multiple --id arguments:

php artisan mail:send --id=1 --id=2
وصف الدخل

Input Descriptions وصف الدخل
لوضع وصف للدخل نضع : بعد الاسم ثم الوصف

/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
أمر الدخل والخرج

Command I/O أمر الدخل والخرج
استرجاع الدخل

Retrieving Input استرجاع الدخل
عند تنفيذ الأمر نحتاج الوصول للمتغيرات او الخيارات نستخدم الطريقة argument والطريقة option إذا كان المتغير او الخيار غير موجود يعيد قيمة null

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
لاسترجاع كل المتغيرات كمصفوفة نستخدم الطريقة arguments

$arguments = $this->arguments();
لاسترجاع الخيارات نستخدم الطريقة option لاسترجاع أكثر من قيمة كمصفوفة options

// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
تلقين الدخل

Prompting For Input تلقين الدخل
لسؤال المستخدم ليقوم بالإدخال نستخدم الطريقة ask

/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $name = $this->ask('What is your name?');
}
الطريقة secret تشبه الطريقة ask لكن الدخل غير مرئي تستخدم عند إدخال بيانات حساسة مثل كلمات المرور

$password = $this->secret('What is the password?');
السؤال للتأكيد

Asking For Confirmation السؤال للتأكيد
السؤال للتأكيد نستخدم الطريقة confirm ليدخل المستخدم yes أو no افتراضيا تعيد قيمة false إذا أدخل المستخدم yes او y تعيد true

if ($this->confirm('Do you wish to continue?')) {
    //
}
لتعيد قيمة افتراضية true نضعها كمتغير ثاني

if ($this->confirm('Do you wish to continue?', true)) {
    //
}
الإكمال التلقائي

Auto-Completion الإكمال التلقائي
الطريقة anticipate توفر إكمال تلقائي للخيارات الممكنة

$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
يمكن تمرير closure كمتغير ثاني للطريقة anticipate
closure يستدعى في كل مرة يكتب فيها المستخدم محرف closure يقبل متغير نوع نصي يتضمن أيضا دخل المستخدم و يعيد مصفوفة خيارات للإكمال التلقائي

$name = $this->anticipate('What is your address?', function ($input) {
    // Return auto-completion options...
});
أسئلة خيار متعدد

Multiple Choice Questions أسئلة خيار متعدد
لإعطاء المستخدم خيارات عند السؤال نستخدم الطريقة choice يمكن وضع مصفوفة فيها قيم افتراضية إذا لم يتم اختيار أي خيار وتوضع كمتغير ثالث

$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
و للطريقة متغير رابع و خامس اختيارية لتحديد عدد المحاولات

$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
كتابة خرج

Writing Output كتابة خرج
استخدام الطرق التالية line, info, comment, question, warn, and error كل طريقة تعطي خرج بلون مناسب لعرض بعض المعلومات للمستخدم نستخدم الطريقة info ستظهر ضمن الواجهة console كنص بلون أخضر

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
لإظهار رسالة خطأ نستخدم error و ستظهر بلون أحمر

$this->error('Something went wrong!');
نستخدم الطريقة line لإظهار نص غير ملون

$this->line('Display this on the screen');
نستخدم الطريقة newLine لإظهار سطر فارغ

// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
الجداول

Tables الجداول
نستخدم الطريقة table نحتاج فقط ادخال اسم العمود ونوع البيانات لارافل تحسب بشكل ديناميكي الطول والعرض المناسبين للجدول

use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
شريط التقدم

Progress Bars شريط التقدم
تعرض للمستخدم المقدار المنجز من المهمة نستخدم الطريقة withProgressBar

use App\Models\User;

$users = $this->withProgressBar(User::all(), function ($user) {
    $this->performTask($user);
});
أحيانا نحتاج لتحكم يدوي بشريط التقدم نحدد العدد الكلي لخطوات التقدم وبعدها تحسين شريط التقدم بعد معالجة كل عنصر

$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
لمزيد من الخيارات المتقدمة تفقد توثيق مكونات شريط التقدم للسيمفوني (https://symfony.com/doc/current/components/console/helpers/progressbar.html).

تسجيل الأوامر

Registering Commands تسجيل الأوامر
كل أوامر شاشة الخرج console سجلت في الصف App\Console\Kernel ضمن الطريقة commands في هذا الصف نداء الطريقة load الطريقة load تقوم بمسح مجلد app/Console/Commands بشكل ديناميكي لتسجيل كل أمر موجود مع Artisan يمكن نداء طريقة load أخرى لمسح بقية المجلدات لأوامر Artisan

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
يمكن يدويا إضافة اسم صف الأمر الى الخاصية $commands ضمن الصف App\Console\Kernel إذا لم تكن هذه الخاصية معرّفة ضمن النواة يجب تعريفها يدويا عند اقلاع Artisan كل قائمة الأوامر في هذه الخاصية مصممة بواسطة service container ومسجَلة مع Artisan

protected $commands = [
    Commands\SendEmails::class
];
تنفيذ الأوامر برمجيا

Programmatically Executing Commands تنفيذ الأوامر برمجيا
تنفيذ أوامر Artisan ضمن المسار route أو المتحكم controller استخدام الطريقة call في واجهة Artisan هذه الطريقة تأخذ في المتغير الأول اسم الصف وفي المتغير الثاني مصفوفة متغيرات الأمر use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
بدلا" من ذلك يمكن إدخاله بشكل نصي

Artisan::call('mail:send 1 --queue=default');
تمرير مصفوفة قيم

Passing Array Values تمرير مصفوفة قيم
إذا كان الأمر يحوي خيار يقبل مصفوفة يمرر مصفوفة قيم

use Illuminate\Support\Facades\Artisan;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
تمرير قيم منطقية

Passing Boolean Values تمرير قيم منطقية
عند تحديد قيمة لخيار ليست نصية مثلا قيمة --force في الأمر migrate:refresh يجب تمرير true أو `false كقيمة للخيار

$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
Artisan رتل أوامر

Queueing Artisan Commands Artisan رتل أوامر
استخدام الطريقة queue قبل استخدامها تأكد من اعدادات الرتل وتشغيل مستمع الرتل

use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
استخدام الطرقonConnection و onQueue لتحديد لاتصال او الامر الذي يجب أن يرسل

Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
نداء أوامر من أوامر أخرى

Calling Commands From Other Commands نداء أوامر من أوامر أخرى
نستخدم الطريقةcall تقبل اسم الأمر ومصفوفة بالخيارات والمتغيرات

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
الطريقة callSilently لنداء أمر console أخر و كتم خرجه

$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
معالجة الإشارة

Signal Handling معالجة الإشارة
يجب تحقيق الواجهة Symfony\Component\Console\Command\SignalableCommandInterface في صف أمر Artisan تتطلب تعريف طريقتينgetSubscribedSignals وhandleSignal

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
الطريقة getSubscribedSignals تعيد مصفوفة إشارات يعالجها الأمر الطريقة handleSignal تستقبل الإشارات

تخصيص جزء

Stub Customization تخصيص جزء
أوامر Artisan console's make لإنشاء صفوف مثل controllers و jobs و migrations و tests هذه الصفوف تستخدم ملفات stub تتضمن قيم تعتمد على دخلك نستخدمstub:publish لنشر stubs في التطبيق بالتالي يمكن تخصيصهم

php artisan stub:publish
تتوضع stubs ضمن مجلد stubs في جذر التطبيق

الأحداث

Events الأحداث
ترسل Artisan ثلاث أحداث عند تشغيل الأوامر Illuminate\Console\Events\ArtisanStarting, Illuminate\Console\Events\CommandStarting, Illuminate\Console\Events\CommandFinished. الحدث ArtisanStarting يُرسل مباشرة عند تشغيل artisan الحدثCommandStarting يُرسل مباشرة قبل تشغيل الأمر الحدثCommandFinished يُرسل مباشرة عند انتهاء تنفيذ الأمر

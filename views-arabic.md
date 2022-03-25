# الواجهات (Views)

- [مقدمة](#introduction)
- [إنشاء وتقديم الواجهات](#creating-and-rendering-views)
    - [مجلدات الواجهة المتداخلة](#nested-view-directories)
    - [إنشاء أوّل واجهة متاحة](#creating-the-first-available-view)
    - [تحديد إن كانت الواجهة موجودة](#determining-if-a-view-exists)
- [Passing Data To Views](#passing-data-to-views)
    - [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
    - [View Creators](#view-creators)
- [Optimizing Views](#optimizing-views)

<a name="introduction"></a>
## مقدمة

بالطبع ، ليس من العملي إرجاع سلاسل مستندات HTML بالكامل مباشرةً من المسارات (paths) والمتحكمات الخاصة بك (controllers). لحسن الحظ ، توفر الواجهات طريقة مناسبة لوضع كل HTML في ملفات منفصلة. تفصل الواجهات منطق وحدة التحكم / منطق التطبيق عن منطق عرضك التقديمي  (presentation logic) ويتم تخزين الواجهات في المجلد `resources/view`. قد تشبه الواجهة البسيطة المثال التالي:

```blade
<!-- الواجهات المُخزّنة في resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```
نظراً لأن هذه الواجهة مخزنة في `resources/views/greeting.blade.php` ، يمكننا ارجاعها باستخدام المساعد العام `view` مثل:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });


> ملاحظة: هل تبحث عن مزيد من المعلومات حول كيفية كتابة قوالب Blade؟ ألق نظرة على [توثيق Blade](/docs/{{version}}/blade) الكامل للبدء.

<a name="creating-and-rendering-views"></a>

## إنشاء وتقديم الواجهات
يمكنك إنشاء واجهة عن طريق وضع ملف بامتداد `.blade.php` في مجلد `resources/views` في تطبيقك. يخبر الامتداد `.blade.php` إطار العمل (framework) بأن الملف يحتوي على [قالب Blade](/docs/{{version}}/blade). تحتوي قوالب الBlade على HTML بالإضافة إلى مجلدات  Blade التي تتيح لك محاكاة القيم بسهولة وإنشاء عبارات "if" والتكرار على البيانات والمزيد.

بمجرد إنشاء واجهة ، يمكنك إرجاعها من أحد مسارات أو متحكمات في تطبيقك باستخدام  المساعد العام `view`:

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

يمكن أيضاً إرجاع الواجهة عبر الواجهة الساكنة `View`:

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);

كما ترى، يُوافق المّتغيّر الوسيط الأوّل المُمرّر إلى المُساعد view اسم ملف الواجهة في المجلّد resources/views. المتغيّر الوسيط الثاني هو مصفوفة البيانات التي يجب أن تُتاح للواجهة. نقوم في هذه الحالة بتمرير المتغيّر name الذي يُعرض في الواجهة باستخدام [صيغة Blade](/docs/{{version}}/blade). 

<a name="nested-view-directories"></a>

### مجلدات الواجهة المتداخلة(Nested)
يمكن أيضاً تضمين (nesting) الواجهات ضمن مُجلّدات فرعية من المُجلّد `resources/views`. يمكن استخدام الترميز "نقطة" للإشارة للعروض المتداخلة (nested). مثلا، إن خُزّن عرضك في `resources/views/admin/profile.blade.php`، يمكن ارجاعه من أحد مسارات/ متحكمات تطبيقك على النحو التالي:

    return view('admin.profile', $data);

> ملاحظة: يجب ألا تحتوي مجلدات الواجهة على نقطة `.`

<a name="creating-the-first-available-view"></a>

### إنشاء أوّل واجهة متاحة 

يمكنك إنشاء `الواجهة` الأولى في مصفوفة معيّنة من الواجهات باستخدام التابع `first`. يُفيدك هذا إن سمح تطبيقك أو حزمتك بتخصيص الواجهات أو إعادة تعريفها (overwritten):

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>

### تحديد إن كانت الواجهة موجودة

إن كنت بحاجة لتحديد إن كانت الواجهة موجودة، يمكنك استخدام الواجهة الساكنة View (أي `View` facade). سيرد التابع `exists` بالقيمة true إن وُجدت الواجهة:

    use Illuminate\Support\Facades\View;

    if (View::exists('emails.customer')) {
        //
    }






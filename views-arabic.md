# الواجهات (Views)

- [الواجهات (Views)](#الواجهات-views)
  - [مقدمة](#مقدمة)
  - [إنشاء وتقديم الواجهات](#إنشاء-وتقديم-الواجهات)
    - [إنشاء أوّل واجهة متاحة](#إنشاء-أوّل-واجهة-متاحة)
    - [تحديد إن كانت الواجهة موجودة](#تحديد-إن-كانت-الواجهة-موجودة)
  - [تمرير البيانات للواجهات](#تمرير-البيانات-للواجهات)
    - [مشاركة البيانات مع جميع الواجهات](#مشاركة-البيانات-مع-جميع-الواجهات)
  - [مؤلّفو الواجهات (View Composers)](#مؤلّفو-الواجهات-view-composers)

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
```php
    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });
```

> ملاحظة: هل تبحث عن مزيد من المعلومات حول كيفية كتابة قوالب Blade؟ ألق نظرة على [توثيق Blade](/docs/{{version}}/blade) الكامل للبدء.

<a name="creating-and-rendering-views"></a>

## إنشاء وتقديم الواجهات
يمكنك إنشاء واجهة عن طريق وضع ملف بامتداد `.blade.php` في مجلد `resources/views` في تطبيقك. يخبر الامتداد `.blade.php` إطار العمل (framework) بأن الملف يحتوي على [قالب Blade](/docs/{{version}}/blade). تحتوي قوالب الBlade على HTML بالإضافة إلى مجلدات  Blade التي تتيح لك محاكاة القيم بسهولة وإنشاء عبارات "if" والتكرار على البيانات والمزيد.

بمجرد إنشاء واجهة ، يمكنك إرجاعها من أحد مسارات أو متحكمات في تطبيقك باستخدام  المساعد العام `view`:
```php
    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

يمكن أيضاً إرجاع الواجهة عبر الواجهة الساكنة `View`:

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);
````
كما ترى، يُوافق المّتغيّر الوسيط الأوّل المُمرّر إلى المُساعد view اسم ملف الواجهة في المجلّد resources/views. المتغيّر الوسيط الثاني هو مصفوفة البيانات التي يجب أن تُتاح للواجهة. نقوم في هذه الحالة بتمرير المتغيّر name الذي يُعرض في الواجهة باستخدام [صيغة Blade](/docs/{{version}}/blade). 

<a name="nested-view-directories"></a>

### مجلدات الواجهة المتداخلة(Nested)
يمكن أيضاً تضمين (nesting) الواجهات ضمن مُجلّدات فرعية من المُجلّد `resources/views`. يمكن استخدام الترميز "نقطة" للإشارة للعروض المتداخلة (nested). مثلا، إن خُزّن عرضك في `resources/views/admin/profile.blade.php`، يمكن ارجاعه من أحد مسارات/ متحكمات تطبيقك على النحو التالي:
```php
    return view('admin.profile', $data);
```
> ملاحظة: يجب ألا تحتوي مجلدات الواجهة على نقطة `.`

<a name="creating-the-first-available-view"></a>

### إنشاء أوّل واجهة متاحة 

يمكنك إنشاء `الواجهة` الأولى في مصفوفة معيّنة من الواجهات باستخدام التابع `first`. يُفيدك هذا إن سمح تطبيقك أو حزمتك بتخصيص الواجهات أو إعادة تعريفها (overwritten):

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>

### تحديد إن كانت الواجهة موجودة

إن كنت بحاجة لتحديد إن كانت الواجهة موجودة، يمكنك استخدام الواجهة الساكنة View (أي `View` facade). سيرد التابع `exists` بالقيمة true إن وُجدت الواجهة:
```php
    use Illuminate\Support\Facades\View;

    if (View::exists('emails.customer')) {
        //
    }
```
<a name="passing-data-to-views"></a>

## تمرير البيانات للواجهات

كما رأيت في الأمثلة السابقة، يمكنك تمرير مصفوفة من البيانات للواجهات لجعل تلك البيانات متوفرة للواجهة:
```php
    return view('greetings', ['name' => 'Victoria']);
```
عند تمرير المعلومات بهذه الطريقة ، يجب أن تكون البيانات مصفوفة من الأزواج مفتاح / قيمة (key/value). بعد تمرير البيانات للواجهة
 يمكنك الوصول لكل قيمة باستخدام مفتاحها المُوافق داخل واجهتك، مثل `<?;php echo $key ?>`. كبديل لتمرير مصفوفة كاملة من البيانات إلى دالّة المُساعد `view،` يمكنك استخدام التابع `with` لإضافة أجزاء منفردة من البيانات للواجهة. يرجع التابع `with` نسخة من كائن الواجهة (view object) بحيث يمكنك متابعة تسلسل التوابع قبل إرجاع الواجهة:
```php
    return view('greeting')
                ->with('name', 'Victoria')
                ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>

### مشاركة البيانات مع جميع الواجهات
في بعض الأحيان ، قد تحتاج إلى مشاركة البيانات مع جميع واجهات تطبيقك.
يمكنك استخدام التابع `share` من واجهة العرض الساكنة (view facade) للقيام بذلك. عادة، عليك وضع نداءات التابع `share` داخل تابع مقدّم الخدمات `boot`. لك حريّة إضافتها إلى `App\Providers\AppServiceProvider class` أو إنشاء مُقدّم خدمة منفصل لإيوائها:

```php
    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\View;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * تسجيل أي خدمة تطبيق
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            View::share('key', 'value');
        }
    }
```
<a name="view-composers"></a>

## مؤلّفو الواجهات (View Composers)
مُؤلّفو الواجهات هم عمليات نداء (callbacks)  أو دوال أصناف (class methods) تُستدعى عند عرض الواجهة. إذا كانت لديك بيانات تريد ربطها بواجهة في كل مرة يتم فيها عرض هذا الواجهة ، فيمكن أن يساعدك مؤلف الواجهة في تنظيم هذا المنطق في مكان واحد. قد يكون مؤلفو الواجهة ذو فائدة بشكل خاص إذا تم إرجاع نفس الواجهة من خلال مسارات أو متحكمات متعددة داخل تطبيقك وتحتاج دائماً إلى جزء معين من البيانات.
عادةً ، سيتم تسجيل مؤلفي الواجهات في أحد [مزودي الخدمة](/docs/{{version}}/providers)  لتطبيقك. في هذا المثال ، سنفترض أننا أنشأنا `App\Providers\ViewServiceProvider` جديدًا لإيواء هذا المنطق.
سنستخدم التابع `composer` للواجهة الساكنة View لتسجيل مؤلف الواجهة تذكر أن Laravel لا يحتوي على مجلّد افتراضي لمؤلّفي الواجهات المعتمدة على الأصناف (class based).  لديك حريّة تنظيمها كما شئت. على سبيل المثال ، يمكنك إنشاء دليل `app/View/Composers` لإيواء جميع مؤلفي واجهات تطبيقك:
```php
    <?php

    namespace App\Providers;

    use App\View\Composers\ProfileComposer;
    use Illuminate\Support\Facades\View;
    use Illuminate\Support\ServiceProvider;

    class ViewServiceProvider extends ServiceProvider
    {
        /**
         * تسجيل أي خدمات تطبيق.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            // استخدام المؤلّفين على أساس الصنف ...

            View::composer('profile', ProfileComposer::class);

            // Closure استخدام المؤلّفين على أساس 
            View::composer('dashboard', function ($view) {
                //
            });
        }
    }

```
> ملاحظة: تذكر أنه إن أنشأت مقدّم خدمات جديد لاحتواء تسجيلات مؤلف واجهاتك ستحتاج لإضافة مُقدّم الخدمات إلى مصفوفة `providers` في ملف الإعدادات `config/app.php.`.

 بعد تسجيلنا للمؤلّف سيُنفّذ الآن سينفذ التابع `compose` من الصنف `App\View\Composers\ProfileComposer` في كل مرة يتم عرض واجهة `profile`.  لذا فلنتعرف على صنف المؤلف:
```php
   <?php

    namespace App\View\Composers;

    use App\Repositories\UserRepository;
    use Illuminate\View\View;

    class ProfileComposer
    {
        /**
         * The user repository implementation.
         *
         * @var \App\Repositories\UserRepository
         */
        protected $users;

        /**
         * profile أنشئ مؤلّف جديد من
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            // Dependencies are automatically resolved by the service container...
            $this->users = $users;
        }

        /**
         * إربط البيانات بالواجهة
         *
         * @param  \Illuminate\View\View  $view
         * @return void
         */
        public function compose(View $view)
        {
            $view->with('count', $this->users->count());
        }
    }

```
كما ترى، يُستبين كل مؤلّفو الواجهة عبر  [حاوي الخدمات](/docs/{{version}}/container)، لذا تستطيع التلميح على نوع أي إعتماديّة تحتاجها داخل تابع بناء المؤلّف (composer's constructor).




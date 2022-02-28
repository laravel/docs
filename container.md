# حاوي الخدمات

- [مقدمة](#introduction)
    - [ميزة عدم الإعداد (Zero Configuration Resolution)](#zero-configuration-resolution)
    - [متى يتم استخدام حاوي الخدمات](#when-to-use-the-container)
- [الربط](#binding)
    - [أساسيات الربط](#binding-basics)
    - [ربط الواجهات بالاستخدام (Binding Interfaces To Implementations)](#binding-interfaces-to-implementations)
    - [الربط السياقي](#contextual-binding)
    - [ربط القيم الأساسية (Binding Primitives)](#binding-primitives)
    - [ربط الأنواع المتغيرة](#binding-typed-variadics)
    - [الوَسم (Tagging)](#tagging)
    - [توسيع الروابط](#extending-bindings)
- [الاستبيان](#resolving)
    - [الدالة make](#the-make-method)
    - [ الحقن التلقائي](#automatic-injection)
- [استدعاء وحقن الدوال](#method-invocation-and-injection)
- [أحداث حاوي الخدمات](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## مقدمة

حاوي الخدمات (service container) في لارافيل هو أداة فعالة لإدارة إعتماديات الصفوف (class dependencies) والقيام بحقن الإعتماديات. حيث أن حقن الاعتمادية (Dependency injection) هو مصطلح تقني يشير بأن إعتماديات الصفوف سيتم "حقنها" في الصف إما عن طريق الباني (constructor) أو عن طريق الدوال المُسنِدة للقيم (setter methods) في بعض الحالات. 

لنلقِ نظرة على هذا المثال البسيط:

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Repositories\UserRepository;
    use App\Models\User;

    class UserController extends Controller
    {
        /**
         * The user repository implementation.
         *
         * @var UserRepository
         */
        protected $users;

        /**
         * Create a new controller instance.
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return Response
         */
        public function show($id)
        {
            $user = $this->users->find($id);

            return view('user.profile', ['user' => $user]);
        }
    }

في هذا المثال، يحتاج المتحكم (Controller) التالي `UserController` لجلب المستخدمين من مصدر للبيانات. لهذا السبب سوف نقوم **بحقن** خدمة تستطيع جلب المستخدمين.  وعلى الأرجح سيقوم `UserRepository` باستخدام [Eloquent](/docs/{{version}}/eloquent) لجلب معلومات المستخدمين من قاعدة البيانات. بكل الأحوال، وبما أن المستودع (repository) قد تم حقنه، يمكننا وبسهولة تبديله باستخدام (implementation) آخر. ويمكننا أيضاً "تقليد"، أو إنشاء استخدام مزيف (dummy implementation) من `UserRepository` عند اختبار التطبيق. 

إن الفهم العميق لحاوي خدمات لارافيل ضروري لبناء تطبيق ضخم وقوي، كما أنه ضروي للمساهة في جوهر لارافيل نفسها.

<a name="zero-configuration-resolution"></a>
### ميزة عدم الإعداد (Zero Configuration Resolution)

اذا لم يحتوي الصف على أي اعتماديات أو اعتمد فقط على صفوف محددة (concrete classes) ليست واجهات (not Interfaces)، فلن يحتاج حاوي الخدمات في لارافيل لتوجيهات عن كيفية استبيان الصف. فعلى سبيل المثال يمكنك وضع الكود التالي في الملف `routes/web.php`: 

    <?php

    class Service
    {
        //
    }

    Route::get('/', function (Service $service) {
        die(get_class($service));
    });

في هذا المثال، زيارة المسار (route) التالي `/` في تطبيقك سيؤدي اوتوماتيكياً لاستبيان الصف `Service` والقيام بحقنه في معالج المسار (route's handler). يعد ذلك نقطة تحول. أي أنك تستطيع تطوير تطبيقك والاستفادة من حقن الاعتماديات دون الخشية من تضخم ملفات الإعداد. 

لحسن الحظ، العديد من الصفوف التي ستقوم بكتابتها عند بناء تطبيق لارافيل ستحصل بشكل أوتوماتيكي على اعتمادياتها بواسطة حاوي الخدمة، بما فيها [المتحكمات (controllers)](/docs/{{version}}/controllers)، [المتنصتات على الأحداث (event listeners)](/docs/{{version}}/events)، [البرمجيات الوسيطة (middleware)](/docs/{{version}}/middleware)، والمزيد. بالإضافة لذلك يمكنك التلميح لنوع (type-hint) الاعتماديات في الدالة `handle` الخاصة [بالأعمال في صفوف الانتظار (queued jobs)](/docs/{{version}}/queues). وبمجرد أن تشعر بقوة الحقن التلقائي للاعتماديات بدون الإعداد ستشعر بأنه يستحيل التطوير بدونه. 

<a name="when-to-use-the-container"></a>
### متى يتم استخدام حاوي الخدمات

بفضل ميزة عدم الإعداد، في غالب الأحيان ستقوم بالتلميح لنوع (type-hint) الإعتماديات على المسارات (routes)، والمتحكمات (controllers)، والمتنصتات على الأحداث (event listeners)، وفي أماكن أخرى بدون التعامل اليدوي حتى مع حاوي الخدمات. على سبيل المثال، يمكنك التلميح لنوع الغرض `Illuminate\Http\Request` على تعريف المسار (route) التالي مما يجعلك ببساطة قادراً على الوصول للطلب (request) الحالي. حتى إن لم تقم بالتفاعل مع حاوي الخدمات لكتابة هذا الكود، سيقوم حاوي الخدمات بإدارة الحقن لهذه الإعتماديات خلف الكواليس: 

    use Illuminate\Http\Request;

    Route::get('/', function (Request $request) {
        // ...
    });

في العديد من الحالات، وبفضل الحقن الأوتماتيكي للإعتماديات و [Facades](/docs/{{version}}/facades)، يمكنك بناء تطبيقات لارافيل بدون الربط أو الاستبيان اليدوي عن أي شيئ **أبداً** في حاوي الخدمات. **اذاً متى يجب التعامل مع حاوي الخدمات؟** دعنا نقوم باختبار حالتين.

الحالة الأولى، اذا قمت بكتابة صف يقوم باستخدام واجهة (interface) وتوّد القيام بتلميح لنوع (type-hint) تلك الواجهة على مسار (route) أو ضمن باني صف (class constructor). عندئذٍ يجب عليك أن تقوم [بإخبار حاوي الخدمات عن كيفية التعامل مع تلك الواجهة](#binding-interfaces-to-implementations). الحالة الثانية، إذا كنت تقوم [بكتابة حزمة لارافيل](/docs/{{version}}/packages)  تخطط لمشاركتها مع مطوري لارافيل آخرين، ربما تحتاج لربط خدمات حزمتك بحاوي الخدمات. 

<a name="binding"></a>
## الربط

<a name="binding-basics"></a>
### أساسيات الربط

<a name="simple-bindings"></a>
#### الربط البسيط

كل الارتباطات الخاصة بحاوي خدماتك سيتم تسجيلها في [مزودي الخدمات (service providers)](/docs/{{version}}/providers)، لذا ستقوم معظم هذه الأمثلة بإرشادك حول كيفية استخدام حاوي الخدمات في هذا السياق. 

ضمن مزودي الخدمات (service provider)، يجب عليك دائماً الوصول لحاوي الخدمات باستخدام الخاصية `$this->app`. حيث يمكننا تسجيل الارتباط بواسطة الدالة `bind`، عبر تمرير اسم الصف أو الواجهة التي نرغب بتسجيلها مع التعبير (closure) الذي سيعيد نسخة (instance) من الصف: 

    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $this->app->bind(Transistor::class, function ($app) {
        return new Transistor($app->make(PodcastParser::class));
    });

لاحظ بأننا نحصل على حاوي الخدمات بنفسه كوسيط للمُستبين (resolver). مما يعني أنه بإمكاننا استخدام حاوي الخدمات للتعامل مع الاعتماديات الثانوية (sub-dependencies) للغرض (object) الذي نقوم ببنائه. 

كما ذُكر، عادة ما ستقوم بالتعامل مع حاوي الخدمات ضمن مزودي الخدمات (service providers). وبكل الأحوال، اذا كنت ترغب بالتعامل مع حاوي الخدمات خارج مزودي الخدمات (service provider)، يمكنك ذلك عبر الـ[facade](/docs/{{version}}/facades)  التالي `App`: 

    use App\Services\Transistor;
    use Illuminate\Support\Facades\App;

    App::bind(Transistor::class, function ($app) {
        // ...
    });

> {tip} ليس هناك داعٍ لربط الصفوف التي لا تعتمد على أي واجهات بحاوي الخدمات. لأن حاوي الخدمات لا يحتاج لإرشاد حول كيفية بناء هذه الأغراض لأن بإمكانه القيام بالاستبيان عن هذه الأغراض أوتوماتيكاً باستخدام الانعكاس (reflection). 

<a name="binding-a-singleton"></a>
#### ربط Singleton
تقوم الدالة `singleton` بربط صف أو واجهة (interface) يجب استبيانها لمرة واحدة بحاوي الخدمات. فعندما يتم استيان ارتباط  singleton، سيتم إعادة نفس النسخة (same instance) في الاستدعاءات اللاحقة لحاوي الخدمات. 


    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $this->app->singleton(Transistor::class, function ($app) {
        return new Transistor($app->make(PodcastParser::class));
    });

<a name="binding-scoped"></a>
#### ربط صفوف Singleton محددة النطاق (Binding Scoped Singletons) 

تقوم الدالة `scoped` بربط صف أو واجهة (interface) يجب استبيانها لمرة واحدة خلال دورة حياة طلب أو مهمة محددة في لارافيل بحاوي الخدمات. حيث أن هذه الدالة مشابهة للدالة `singleton`، ولكن النسخ  (instances) التي تم تسجيلها بالطريقة `scoped` سيتم التخلص منها عندما يقوم تطبيق لارافيل ببدء "دورة حياة" جديدة، كما هو الحال عندما يقوم الـ worker الخاص بـ [Laravel Octane](/docs/{{version}}/octane) بمعالجة طلب جديد أو عندما يقوم الـ[queue worker](/docs/{{version}}/queues) بلارافيل بمعاجة عمل جديد:


    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $this->app->scoped(Transistor::class, function ($app) {
        return new Transistor($app->make(PodcastParser::class));
    });

<a name="binding-instances"></a>
#### ربط النُسخ (Binding Instances)

تستطيع أيضاً ربط نسخة غرض موجودة (existing object instance) بحاوي الخدمات باستخدام الدالة `instance`. حيث سيتم دائماً إعادة النسخة التي تم تمريرها في الاستدعاءات اللاحقة لحاوي الخدمات:


    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $service = new Transistor(new PodcastParser);

    $this->app->instance(Transistor::class, $service);

<a name="binding-interfaces-to-implementations"></a>
### ربط الواجهات بالاستخدام (Binding Interfaces To Implementations)

إحدى الميزات القوية لحاوية الخدمات هي القدرة على ربط واجهة (interface) باستخدام (implementation) لها. على سبيل المثال، لنفترض بأنه لدينا الواجهة (interface) التالية `EventPusher` ولدينا الاستخدام (implementation) التالي `RedisEventPusher` لها. عندما ننتهي من كتابة الاستخدام `RedisEventPusher` لهذه الواجهة (interface) نستطيع تسجيله بحاوي الخدمات بالطريقة التالية: 

    use App\Contracts\EventPusher;
    use App\Services\RedisEventPusher;

    $this->app->bind(EventPusher::class, RedisEventPusher::class);

تقوم العبارة السابقة بإخبار حاوي الخدمات بأن عليه حقن `RedisEventPusher` عند حاجة أي صف لاستخدام (implementation) للواجهة `EventPusher`. وأصبح بإمكاننا الآن التلميح لنوع (type-hint) الواجهة `EventPusher` في باني أي صف يتعامل مع حاوي الخدمات. وتذكر بأن المتحكمات (controllers)، والمتنصتات على الأحداث (event listeners)، والبرمجيات الوسيطة (middleware)، والعديد من أنواع الصفوف الأخرى في تطبيقات لارافيل دوماً ما يتم استبيانها باستخدام حاوي الخدمات: 

    use App\Contracts\EventPusher;

    /**
     * Create a new class instance.
     *
     * @param  \App\Contracts\EventPusher  $pusher
     * @return void
     */
    public function __construct(EventPusher $pusher)
    {
        $this->pusher = $pusher;
    }

<a name="contextual-binding"></a>
### الربط السياقي

في بعض الأحيان يمكن لصفين الاستفادة من نفس الواجهة، ولكنك قد ترغب بحقن استخدامات (implementations) مختلفة في كل صف منهما. على سبيل المثال، يمكن لاثنين من المتحكمات (controllers) الاعتماد على استخدامات (implementations) مختلفة للـ [contract](/docs/{{version}}/contracts) التالي `Illuminate\Contracts\Filesystem\Filesystem`. إن لارافيل توفر واجهة (interface) سهلة و سلسة لتعريف هذا السلوك: 

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\UploadController;
    use App\Http\Controllers\VideoController;
    use Illuminate\Contracts\Filesystem\Filesystem;
    use Illuminate\Support\Facades\Storage;

    $this->app->when(PhotoController::class)
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('local');
              });

    $this->app->when([VideoController::class, UploadController::class])
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('s3');
              });

<a name="binding-primitives"></a>
### ربط القيم الأساسية (Binding Primitives)

في بعض الأحيان قد يكون لديك صف يستقبل بعض الصفوف المحقونة،  وبنفس الوقت قد تحتاج لحقن قيمة أساسية (primitive value) مثل عدد صحيح (integer). يمكنك ببساطة استخدام الربط السياقي لحقن أي قيمة قد تحتاجها في صفك: 

    $this->app->when('App\Http\Controllers\UserController')
              ->needs('$variableName')
              ->give($value);

في بعض الأحيان قد يعتمد صفك على مصفوفة نُسخ (instances) [موسومة (tagged)](#tagging). يمكنك وبسهولة بواسطة الدالة `giveTagged`  حقن كل روابط حاوي الخدمات التي تحمل الوسم (tag) نفسه. 

    $this->app->when(ReportAggregator::class)
        ->needs('$reports')
        ->giveTagged('reports');

اذا كنت تحتاج لحقن قيمة من أحد ملفات الإعداد في تطبيقك، يمكنك استخدام الدالة  `giveConfig`: 

    $this->app->when(ReportAggregator::class)
        ->needs('$timezone')
        ->giveConfig('app.timezone');

<a name="binding-typed-variadics"></a>
### ربط الأنواع المتغيرة 

في بعض الأحيان، قد تمتلك صفاً يستقبل مصفوفة أغراض مصرح عن نوعها باستخدام وسيط متغير في الباني (constructor):

    <?php

    use App\Models\Filter;
    use App\Services\Logger;

    class Firewall
    {
        /**
         * The logger instance.
         *
         * @var \App\Services\Logger
         */
        protected $logger;

        /**
         * The filter instances.
         *
         * @var array
         */
        protected $filters;

        /**
         * Create a new class instance.
         *
         * @param  \App\Services\Logger  $logger
         * @param  array  $filters
         * @return void
         */
        public function __construct(Logger $logger, Filter ...$filters)
        {
            $this->logger = $logger;
            $this->filters = $filters;
        }
    }

باستخدام الربط السياقي ، يمكنك التعامل مع الإعتمادية السابقة عبر تزويد الدالة `give` بتعبير (closure) يعيد مصفوفة نُسخ (instances) من نوع `Filter` تم استبيانها: 

    $this->app->when(Firewall::class)
              ->needs(Filter::class)
              ->give(function ($app) {
                    return [
                        $app->make(NullFilter::class),
                        $app->make(ProfanityFilter::class),
                        $app->make(TooLongFilter::class),
                    ];
              });

للسهولة، يمكنك تزويد المصفوفة بأسماء الصفوف ليقوم حاوي الخدمات باستبيانها عندما يحتاج الصف `Firewall` نُسخاً (instances) من `Filter`: 

    $this->app->when(Firewall::class)
              ->needs(Filter::class)
              ->give([
                  NullFilter::class,
                  ProfanityFilter::class,
                  TooLongFilter::class,
              ]);

<a name="variadic-tag-dependencies"></a>
#### الإعتماديات المتغيرة الوسوم

في بعض الأحيان  قد يحوي أحد الصفوف اعتمادية متغيرة يتم التلميح لنوعها (type-hinted) كصف مُعطى (`Report ...$reports`). يمكنك وبسهولة باستخدام الدوال التالية `needs` و `giveTagged` حقن كل روابط حاوي الخدمات التي تحمل [الوسم (tag)](#tagging) للاعتمادية المُعطاة: 

    $this->app->when(ReportAggregator::class)
        ->needs(Report::class)
        ->giveTagged('reports');

<a name="tagging"></a>
### الوَسم (Tagging)

في بعض الأحيان قد تحتاج لاستبيان جميع روابط "صنف" ("category") معين. على سبيل المثال، ربما تقوم ببناء محلل تقارير يستقبل مصفوفة تحتوي العديد من استخدمات (implementations)  الواجهة `Report`. بعد تسجيل أغلب استخدامات الواجهة `Report`، يمكنك تعيين وسم (tag) باستخدام الدالة التالية `tag`: 

    $this->app->bind(CpuReport::class, function () {
        //
    });

    $this->app->bind(MemoryReport::class, function () {
        //
    });

    $this->app->tag([CpuReport::class, MemoryReport::class], 'reports');

عندما يتم وسم الخدمات، يمكنك ببساطة استبيانها جميعها بواسطة الدالة `tagged` الخاصة بحاوي الخدمات:

    $this->app->bind(ReportAnalyzer::class, function ($app) {
        return new ReportAnalyzer($app->tagged('reports'));
    });

<a name="extending-bindings"></a>
### توسيع الروابط

 تسمح الدالة `extend` بتعديل الخدمات التي تم استبيانها. على سبيل المثال، يمكنك اجراء تعليمات إضافية عند استبيان خدمة بهدف تحسينها أو ضبطها. حيث أن الدالة `extend` تقبل وسيطاً وحيداً وهو تعبير (closure) يعيد الخدمة بعد التعديل. ويستقبل التعبير (closure) الخدمة التي يتم استبيانها ونُسخة (instance) حاوي الخدمات:

    $this->app->extend(Service::class, function ($service, $app) {
        return new DecoratedService($service);
    });

<a name="resolving"></a>
## الاستبيان

<a name="the-make-method"></a>
### الدالة `make`

يمكنك استخدام الدالة `make` لاستبيان صف من حاوي الخدمات. حيث أن  الدالة `make` تقبل اسم الصف أو اسم الواجهة التي تريد استبيانها كوسيط:

    use App\Services\Transistor;

    $transistor = $this->app->make(Transistor::class);

اذا كان بعض اعتماديات صفوفك غير قابلة للاستبيان بواسطة حاوي الخدمات، يمكنك حقنها عبر تمريرها كمصفوفة ترابطية للدالة `makeWith`. فعلى سبيل المثال يمكننا تمرير وسيط الباني `$id` المطلوب من قبل الخدمة `Transistor` يدوياً: 

    use App\Services\Transistor;

    $transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);

إن كنت خارج مزود الخدمة  في منطقة ما في كودك لا يمكنها الوصول للمتحول `$app` يمكنك استخدام الـ [facade](/docs/{{version}}/facades) التالي `App` لاستبيان صف من حاوي الخدمات: 

    use App\Services\Transistor;
    use Illuminate\Support\Facades\App;

    $transistor = App::make(Transistor::class);

إن كنت ترغب بحقن نسخة حاوي خدمات لارافيل في صف يتم استبيانه بواسطة حاوي الخدمات، يمكنك التلميح للنوع (type-hint) التالي `Illuminate\Container\Container` في باني الصف الخاص بك:

    use Illuminate\Container\Container;

    /**
     * Create a new class instance.
     *
     * @param  \Illuminate\Container\Container  $container
     * @return void
     */
    public function __construct(Container $container)
    {
        $this->container = $container;
    }

<a name="automatic-injection"></a>
### الحقن التلقائي

الجدير بالذكر أنه بإمكانك التلميح لنوع (type-hint) الاعتمادية في باني الصف الذي يتم استبيانه من قبل حاوي الخدمات، بما فيها [المتحكمات (controllers)](/docs/{{version}}/controllers)، [المتنصتات على الأحداث (event listeners)](/docs/{{version}}/events)، [البرمجيات الوسيطة (middleware)](/docs/{{version}}/middleware)، والمزيد. بالإضافة لذلك يمكنك التلميح لنوع الاعتمادية في الدالة `handle` الخاصة [بالأعمال في الطوابير (queued jobs)](/docs/{{version}}/queues). وعملياً يجب عليك اتباع هذا الأسلوب في معظم الأغراض التي التي يجب استبيانها بواسطة حاوي الخدمات. 

على سبيل المثال، يمكنك التلميح لنوع المستودع (repository) الذي تم تعريفه بواسطة تطبيقك في باني المتحكم (controller). حيث سيتم استبيان وحقن المستودع تلقائياً في الصف:

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * The user repository instance.
         *
         * @var \App\Repositories\UserRepository
         */
        protected $users;

        /**
         * Create a new controller instance.
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * Show the user with the given ID.
         *
         * @param  int  $id
         * @return \Illuminate\Http\Response
         */
        public function show($id)
        {
            //
        }
    }

<a name="method-invocation-and-injection"></a>
## استدعاء وحقن الدوال

في بعض الأحيان قد ترغب باستدعاء دالة على نسخة غرض (object instance) أثناء قيام حاوي الخدمات بحقن اعتماديات الدالة تلقائياً. على سبيل المثال، لدينا الصف التالي:

    <?php

    namespace App;

    use App\Repositories\UserRepository;

    class UserReport
    {
        /**
         * Generate a new user report.
         *
         * @param  \App\Repositories\UserRepository  $repository
         * @return array
         */
        public function generate(UserRepository $repository)
        {
            // ...
        }
    }

يمكننا استدعاء الدالة `generate` باستخدام حاوي الخدمات كما يلي: 

    use App\UserReport;
    use Illuminate\Support\Facades\App;

    $report = App::call([new UserReport, 'generate']);

تقبل الدالة `call` أي متحول PHP من النمط callable. حيث يمكن استخدام الدالة `call` الخاصة بحاوي الخدمات لاستدعاء تعبير (closure) أثناء الحقن التلقائي لاعتمادياته: 

    use App\Repositories\UserRepository;
    use Illuminate\Support\Facades\App;

    $result = App::call(function (UserRepository $repository) {
        // ...
    });

<a name="container-events"></a>
## أحداث حاوي الخدمات

يُطلق حاوي الخدمات حدثاً في كل مرة يقوم فيها باستبيان غرض (object). حيث يمكنك التنصت على هذه الأحداث باستخدام الدالة `resolving`:

    use App\Services\Transistor;

    $this->app->resolving(Transistor::class, function ($transistor, $app) {
        // Called when container resolves objects of type "Transistor"...
    });

    $this->app->resolving(function ($object, $app) {
        // Called when container resolves object of any type...
    });

كما تلاحظ، سيتم تمرير الغرض الذي يتم استبيانه للاستدعاء (callback)، مما يسمح بضبط أي خواص اضافية للغرض قبل تمريره للمستخدم. 

<a name="psr-11"></a>
## PSR-11

يقوم حاوي خدمات لارافيل باستخدم (implement) الواجهة [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md). لذلك تستطيع التلميح لنوع واجهة الحاوي PSR-11 للحصول على نسخة (instance) من حاوي خدمات لارافيل: 

    use App\Services\Transistor;
    use Psr\Container\ContainerInterface;

    Route::get('/', function (ContainerInterface $container) {
        $service = $container->get(Transistor::class);

        //
    });

سيتم رمي استثناء (exception) في حال كون المُعرِف (identifier) غير قابل للاستبيان. حيث أن الاستثناء (exception) سيكون عبارة عن نسخة (instance) من `Psr\Container\NotFoundExceptionInterface` في حال لم يتم ربط المُعرِف (identifier). أما في حال ربط المُعرِف (identifier) وعدم القدرة على استبيانه سيتم رمي استثناء (exception) عبارة عن نسخة (instance) من `Psr\Container\ContainerExceptionInterface`. 

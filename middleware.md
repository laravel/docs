# الكائن الوسيط

- [المقدمة](#introduction)
- [تعريف الكائن الوسيط](#defining-middleware)
- [تسجيل الكائن الوسيط](#registering-middleware)
    - [الكائن الوسيط العام](#global-middleware)
    - [تعيين الكائن الوسيط للمسارات](#assigning-middleware-to-routes)
    - [مجموعات الكائن الوسيط](#middleware-groups)
    - [ترتيب الكائن الوسيط](#sorting-middleware)
- [متغيرات الكائن الوسيط](#middleware-parameters)
- [الكائن الوسيط القابل للإنهاء](#terminable-middleware)

<a name="introduction"></a>
## المقدمة 
يؤمن الكائن الوسيط اّلية مناسبة لفحص وفلترة طلبات بروتوكول HTTP 
مثال: يتحقق الكائن الوسيط ضمن لارافل من المستخدم إذا كان مسجل ضمن الموقع أو غير مسجل
إذا كان غير مسجل يحوله إلى صفحة تسجيل الدخول إذا كان مسجل يسمح له بالدخول إلى الموقع

يتوضع الكائن الوسيط ضمن مجلد `app/Http/Middleware` 
يوجد كائنات لتنفيذ المهام المتنوعة إلى جانب كائن التحقق من تسجيل الدخول والحماية من ثغرة CSRF (Cross-Site Request Forgery)

<a name="defining-middleware"></a>
## تعريف الكائن الوسيط 

لإنشاء كائن وسيط نستخدم الأمر`make:middleware`  

```shell
php artisan make:middleware EnsureTokenIsValid
```


أنشأ الأمر السابق صف`EnsureTokenIsValid`  ضمن المجلد`app/Http/Middleware`   
هذا الكائن الوسيط يسمح بالوصول إلى المسار في حال تساوي`token`  المدخلة مع القيمة الموجودة غير ذلك يقوم بتحويل المستخدم إلى الصفحة الرئيسية`home`  

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureTokenIsValid
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            if ($request->input('token') !== 'my-secret-token') {
                return redirect('home');
            }

            return $next($request);
        }
    }

كما ترى إذا كان العّلام المُعطى لا يماثل العّلام السري سيقوم الكائن الوسيط بتحويل المستخدم للصفحة الرئيسية غير ذلك يسمح للمستخدم بالدخول إلى صفحات التطبيق نقوم بنداء `$next` و ضمنها `$request`

من الأفضل تصور الكائن الوسيط كسلسلة طبقات تمر عبرها طلبات HTTP كل طبقة تفحص طلب HTTP و حتى رفضه داخليا 


<a name="before-after-middleware"></a>
<a name="middleware-and-responses"></a>
#### الكائن الوسيط والاستجابة
ينفذ الكائن الوسيط المهام قبل وبعد تمرير الطلب أعمق بالتطبيق
في المثال التالي سيقوم الكائن الوسيط بتنفيذ المهمة قبل معالجة الطلب من قبل التطبيق

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class BeforeMiddleware
    {
        public function handle($request, Closure $next)
        {
            // Perform action

            return $next($request);
        }
    }

هذا الكائن الوسيط يقوم بالتحسين بعد معالجة الطلب

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class AfterMiddleware
    {
        public function handle($request, Closure $next)
        {
            $response = $next($request);

            // Perform action

            return $response;
        }
    }

<a name="registering-middleware"></a>
## تسجيل الكائن الوسيط
<a name="global-middleware"></a>
### الكائن الوسيط العام

إذا أردت تشغيل الكائن الوسيط في كل طلب HTTP ضع صف الكائن الوسيط في الخاصية`$middleware` في الصف  `app/Http/Kernel.php`

<a name="assigning-middleware-to-routes"></a>
### تعيين الكائن الوسيط للمسارات
إذا أردت تعيين الكائن الوسيط لمسارات مخصصة يجب تعيين مفتاح للكائن الوسيط ضمن الملف `app/Http/Kernel.php` 
افتراضيا تحوي الخاصية`$routeMiddleware`  في هذا الصف الكائن الوسيط المضمن في لارافل 
يمكنك إضافة الوسيط الخاص بك وتعيين مفتاح خاص به

    // Within App\Http\Kernel class...

    protected $routeMiddleware = [
        'auth' => \App\Http\Middleware\Authenticate::class,
        'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
        'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
        'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
        'can' => \Illuminate\Auth\Middleware\Authorize::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
        'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
        'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    ];

الكائن الوسيط الأول تم تعريفه لنستخدم الطريقة`middleware`  في تعيين كائن وسيط للمسار 

    Route::get('/profile', function () {
        //
    })->middleware('auth');


يمكن تعيين عدة كائنات وسيطة للمسار بتمرير مصفوفة بأسماء الكائنات الوسيطة للطريقة `middleware`

    Route::get('/', function () {
        //
    })->middleware(['first', 'second']);

عند تعيين الكائن الوسيط يمكنك تمرير الاسم الكامل للصف

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::get('/profile', function () {
        //
    })->middleware(EnsureTokenIsValid::class);

<a name="excluding-middleware"></a>
#### استثناء أو استبعاد الكائن الوسيط

عند تعيين كائن وسيط لمجموعة مسارات عادة نحتاج استثناء كائن وسيط من أحد المسارات ضمن المجموعة يمكن انجاز ذلك باستخدام الطريقة  `withoutMiddleware’

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::middleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/', function () {
            //
        });

        Route::get('/profile', function () {
            //
        })->withoutMiddleware([EnsureTokenIsValid::class]);
    });


يمكن استبعاد مجموعة كائنات وسيطة معطاة من مجموعة مدخلة للمسار الوجهة

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/profile', function () {
            //
        });
    });


الطريقة `withoutMiddleware`  تحذف مسار الكائن الوسيط ولا تقبل [global middleware](#global-middleware)


<a name="middleware-groups"></a>
### مجموعات الكائن الوسيط

إذا أردت عمل مجموعة كائن وسيط تحت مفتاح واحد لسهولة تعيينهم للمسارات يمكن انجاز ذلك باستخدام الخاصية `$middlewareGroups` ضمن الصف  HTTP kernel 

يأتي مع لارافل مجموعات كائن وسيط`web`  و`api`  تحوي كائن وسيط يُطبق على مسارات `api`  و`api`  
هذه المجموعات تُطبق بشكل اّلي بواسطة مقدم الخدمة `App\Providers\RouteServiceProvider للمسارات `api`  و  `api`  



    /**
     * The application's route middleware groups.
     *
     * @var array
     */
    protected $middlewareGroups = [
        'web' => [
            \App\Http\Middleware\EncryptCookies::class,
            \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
            \Illuminate\Session\Middleware\StartSession::class,
            // \Illuminate\Session\Middleware\AuthenticateSession::class,
            \Illuminate\View\Middleware\ShareErrorsFromSession::class,
            \App\Http\Middleware\VerifyCsrfToken::class,
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],

        'api' => [
            'throttle:api',
            \Illuminate\Routing\Middleware\SubstituteBindings::class,
        ],
    ];

مجموعات الكائن الوسيط تستخدم نفس بناء الكود للكائن الوسيط الوحيد


    Route::get('/', function () {
        //
    })->middleware('web');

    Route::middleware(['web'])->group(function () {
        //
    });


<a name="sorting-middleware"></a>
### ترتيب الكائن الوسيط

نادراً ما نحتاج لتنفيذ الوسيط بترتيب معين لا نملك سيطرة على هذا الترتيب عند تعيين المسار
في هذه الحالة نحدد أولوية للكائن باستخدام الخاصية`$middlewarePriority`   في الملف  `app/Http/Kernel.php` 
إذا لم تكن موجودة ضمن الملف يمكن وضع الكود الافتراضي في الملف

    /**
     * The priority-sorted list of middleware.
     *
     * This forces non-global middleware to always be in the given order.
     *
     * @var string[]
     */
    protected $middlewarePriority = [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Session\Middleware\AuthenticateSession::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ];

<a name="middleware-parameters"></a>
## متغيرات الكائن الوسيط

يمكن أن يستقبل الوسيط متغيرات إضافية مثلاً عندما نحتاج لنتحقق من مستخدم مسجل إذا كان لديه وظيفة أو دور "role" 
ننشئ وسيط EnsureUserHasRole يستقبل اسم الوظيفة كمتغير إضافي
سيتم تمرير المتغيرات بعد المتغير`$next` 

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureUserHasRole
    {
        /**
         * Handle the incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @param  string  $role
         * @return mixed
         */
        public function handle($request, Closure $next, $role)
        {
            if (! $request->user()->hasRole($role)) {
                // Redirect...
            }

            return $next($request);
        }

    }


تحديد متغيرات الوسيط عند تعريف المسار بفصل اسم الوسيط و المتغير باستخدام `:`  في حال وجود عدة متغيرات نستخدم الفواصل

    Route::put('/post/{id}', function ($id) {
        //
    })->middleware('role:editor');

<a name="terminable-middleware"></a>
## الوسيط القابل للإنهاء 
أحيانا يحتاج الوسيط للقيام بعمل ما قبل أن تُرسل استجابة HTTP إلى المتصفح 
إذا عرفت الطريقة `terminate` في الوسيط ومخدم الويب الذي يستخدم FastCGI سيتم نداء الطريقة بشكل اّلي يعد إرسال الاستجابة للمتصفح 

    <?php

    namespace Illuminate\Session\Middleware;

    use Closure;

    class TerminatingMiddleware
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return $next($request);
        }

        /**
         * Handle tasks after the response has been sent to the browser.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Illuminate\Http\Response  $response
         * @return void
         */
        public function terminate($request, $response)
        {
            // ...
        }
    }


الطريقة `terminate` تستقبل الطلب والاستجابة. يجب تعريف الوسيط القابل للإنهاء وإضافته إلى قائمة المسارات أو الوسيط العام في ملف `app/Http/Kernel.php`

عند نداء الطريقة `terminate` في الوسيط تقوم لارافل بإنشاء نسخة من الوسيط من [service container](/docs/{{version}}/container)
إذا أردنا استخدام نفس النسخة من الوسيط عند نداء الطريقتين `handle`  و `terminate`  سجّل الوسيط مع container باستخدام الطريقة `singleton` 
يتم ذلك في الطريقة `register`  من `AppServiceProvider`

    use App\Http\Middleware\TerminatingMiddleware;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(TerminatingMiddleware::class);
    }

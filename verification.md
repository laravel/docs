# التحقق من الإيميل

- [المقدمة](#introduction)
    - [تحضير النموذج](#model-preparation)
    - [تحضير قاعدة البيانات](#database-preparation)
- [التوجيه](#verification-routing)
    - [إنذار التحقق من الإيميل](#the-email-verification-notice)
    - [معالج التحقق من الإيميل](#the-email-verification-handler)
    - [إعادة إرسال إيميل التحقق](#resending-the-verification-email)
    - [حماية المسارات](#protecting-routes)
- [التخصيص](#customization)
- [الأحداث](#events)

<a name="introduction"></a>
## المقدمة 

العديد من تطبيقات الويب تطلب من المستخدمين التحقق من عنوان بريدهم الالكتروني قبل استخدام التطبيق

تجبرك لإعادة تحقيق هذه الميزة لكل تطبيق تنشئه

تؤمن لارافل خدمة مضمنة معها لإرسال إيميل التحقق

<a name="model-preparation"></a>
### تحضير النموذج 

قبل البدء تحقق أن النموذج`App\Models\User`  يحقق العقد `Illuminate\Contracts\Auth\MustVerifyEmail` 
    <?php

    namespace App\Models;

    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }


تُضاف هذه الواجهة إلى النموذج، يُرسل إيميل بشكل ألي إلى المستخدمين المسجلين حديثاً يحتوي رابط التحقق من الإيميل
كما ترى عن طريق فحص `App\Providers\EventServiceProvider` تحوي لارافل `SendEmailVerificationNotification` [listener](/docs/{{version}}/events) الملحق بالحدث 
`Illuminate\Auth\Events\Registered`
يُرسل هذا الحدث المستمع رابط التحقق من الإيميل للمستخدم 

إذا كنت تتحقق من التسجيل يدوياً بدلاً من استخدام [a starter kit](/docs/{{version}}/starter-kits) يجب أن تتأكد من إرسال الحدث `Illuminate\Auth\Events\Registered` بعد إتمام عملية تسجيل المستخدم بنجاح

    use Illuminate\Auth\Events\Registered;

    event(new Registered($user));

<a name="database-preparation"></a>
### تحضير قاعدة البيانات

يجب أن يحوي جدول المستخدمين `users` حقل `email_verified_at` لتخزين تاريخ ووقت التحقق من إيميل المستخدم

افتراضياً يحتوي تهجير جدول المستخدمين المضمن في لارافل هذا الحقل بالفعل لذلك نحتاج فقط لتشغيل تهجير قاعدة البيانات

```shell
php artisan migrate
```

<a name="verification-routing"></a>
## التوجيه

يجب تعريف ثلاث مسارات لتحقق من الإيميل 

المسار الأول لعرض ملاحظة للمستخدم للضغط على رابط التحقق من الإيميل الذي أرسلته لارافل للمستخدم بعد التسجيل

الثاني لمعالجة الطلبات بعد ضغط المستخدم على الرابط

الثالث لإعادة إرسال رابط تحقق في حال فقدان المستخدم الرابط الأول


<a name="the-email-verification-notice"></a>
### ملاحظة أو انذار التحقق من الإيميل

كما ذكرنا سابقاً المسار الأول يعيد واجهة ترشد المستخدم للضغط على إيميل التحقق المرسلة من قبل لارافل بعد عملية التسجيل

تظهر هذه الواجهة للمستخدم في حال حاول الدخول للتطبيق بدون التحقق من الإيميل
 
يُرسل هذا الرابط بشكل ألي للمستخدم طالما حقق النموذج `App\Models\User` الواجهة `MustVerifyEmail`

    Route::get('/email/verify', function () {
        return view('auth.verify-email');
    })->middleware('auth')->name('verification.notice');

يجب تسمية المسار الذي أرسل إنذار التحقق من الإيميل `verification.notice` 

من المهم إعطاء هذا الاسم بالضبط ليقوم الكائن الوسيط `verified` بتحويل المستخدم إلى اسم هذا المسار إذا لم يتحقق المستخدم من الإيميل

<a name="the-email-verification-handler"></a>
### معالج التحقق من الإيميل

يجب تعريف المسار الذي سيعالج الطلبات بعد ضغط المستخدم على رابط التحقق من الإيميل الذي أُرسل له

اسم هذا المسار `verification.verify`
 
وتعيين كائنين وسيطين `auth` و `signed` 


    use Illuminate\Foundation\Auth\EmailVerificationRequest;

    Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
        $request->fulfill();

        return redirect('/home');
    })->middleware(['auth', 'signed'])->name('verification.verify');

استخدمنا في هذا المثال `EmailVerificationRequest`
 
يأخذ هذا الطلب متغيرين`id`  و `hash`  

نقوم بنداء الطريقة `fulfill` هذه الطريقة تقوم بنداء الطريقة `markEmailAsVerified` على المستخدم المسجل وترسل الحدث `Illuminate\Auth\Events\Verified` 

الطريقة `markEmailAsVerified` متاحة مع النموذج الافتراضي `App\Models\User` عن طريق الصف الأساسي `Illuminate\Foundation\Auth\User`

اذا تم التحقق من الايميل يمكنك توجيه المستخدم للصفحة التي تريدها  

<a name="resending-the-verification-email"></a>
### إعادة إرسال التحقق من الايميل

أحيانا يفقد المستخدم ايميل التحقق يجب تحيد مسار يسمح بإعادة إرسال الايميل لذلك نستخدم زر إعادة الإرسال ضمن واجهة إنذار التحقق

 [verification notice view](#the-email-verification-notice) 
    use Illuminate\Http\Request;

    Route::post('/email/verification-notification', function (Request $request) {
        $request->user()->sendEmailVerificationNotification();

        return back()->with('message', 'Verification link sent!');
    })->middleware(['auth', 'throttle:6,1'])->name('verification.send');

<a name="protecting-routes"></a>
### حماية المسارات

 يسمح الكائن الوسيط [Route middleware](/docs/{{version}}/middleware)  للمستخدمين المسجلين بالوصول للمسار المعطى

اذا تم تسجيل الكائن الوسيط ضمن التطبيق في نواة HTTP 

كل ما عليك فعله ربط الوسيط بالمسار المعرف

    Route::get('/profile', function () {
        // Only verified users may access this route...
    })->middleware('verified');

إذا حاول المستخدم غير متحقق من الايميل الوصول إلى مسار يقوم الوسيط بتحويله إلى `verification.notice` [named route](/docs/{{version}}/routing#named-routes)

<a name="customization"></a>
## التخصيص

<a name="verification-email-customization"></a>
#### تخصيص التحقق من الايميل

تسمح لارافل بتخصيص بنية رسالة ايميل التحقق

مرر closure للطريقة `toMailUsing` الموجودة في `Illuminate\Auth\Notifications\VerifyEmail` 

closure يستقبل نسخة من نموذج الاشعار الذي يرسل اشعار بالرابط الذي يتوجب على المستخدم زيارته ليتم التحقق من الايميل

closure يعيد نسخة من `Illuminate\Notifications\Messages\MailMessage` 

يجب نداء الطريقة `toMailUsing` من الطريقة `boot` بالصف `App\Providers\AuthServiceProvider` 


    use Illuminate\Auth\Notifications\VerifyEmail;
    use Illuminate\Notifications\Messages\MailMessage;

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        // ...

        VerifyEmail::toMailUsing(function ($notifiable, $url) {
            return (new MailMessage)
                ->subject('Verify Email Address')
                ->line('Click the button below to verify your email address.')
                ->action('Verify Email Address', $url);
        });
    }


<a name="events"></a>
## الأحداث

عند استخدام [Laravel application starter kits](/docs/{{version}}/starter-kits) تقوم لارافل بإرسال Laravel dispatches [events](/docs/{{version}}/events) خلال عملية التحقق من الايميل

إذا تمت معالجة التحقق من الايميل بشكل يدوي يجب ارسال هذه الأحداث يدويا بعد انتهاء عملية التحقق

ربط المستمعات لهذه الأحداث في `EventServiceProvider`

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Auth\Events\Verified' => [
            'App\Listeners\LogVerifiedUser',
        ],
    ];

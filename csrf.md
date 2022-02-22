# الحماية من الطلبات المزورة عبر المواقع

- [مقدمة](#csrf-introduction)
- [منع الطلبات المزورة عبر المواقع](#preventing-csrf-requests)
    - [استثناء الروابط (URIs)](#csrf-excluding-uris)
- [رمز (X-CSRF-TOKEN)](#csrf-x-csrf-token)
- [رمز (X-XSRF-TOKEN)](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## مقدمة

تزوير الطلبات عبر المواقع هو نوع من الثغرات الضارة حيث يتم تنفيذ أوامر غير مصرح بها نيابة عن المستخدم الموثق (authenticated user). لكن ولحسن الحظ، يقوم إطار عمل  لارافيل بتسهيل حماية تطبيقك من [الطلبات المزورة عبر المواقع](https://en.wikipedia.org/wiki/Cross-site_request_forgery) أو مايعرف بهجمات الطلبات المزورة عبر المواقع (CSRF attacks).

<a name="csrf-explanation"></a>
#### شرح للثغرة
في حال أنك لم تسمع من قبل بالطلبات المزورة عبر الموقع، لنناقش مثالاً عن كيفية استغلال هذه الثغرة. لنتخيل بأن تطبيقك يحتوي المسار (route) التالي `/user/email` ويقبل طلب من الطريقة `POST` وهدفه تغيير عنوان البريد الالكتروني للمستخدم الموثق (authenticated user). غالباً هذا المسار (route) يقبل عنوان بريد الكتروني `email` كحقل إدخال يحوي على عنوان البريد الالكتروني للمستخدم الذي يود المستخدم البدء باستخدامه. 

بدون الحماية من الطلبات المزورة عبر المواقع (CSRF protection)، يمكن لأي موقع ضار إنشاء استمارة (HTML form) تشير للمسار (route) التالي `/user/email` في تطبيقك، فيقوم عندها المخترق بإرسل عنوان بريد الكتروني خاص به ليستبدل عنوان المستخدم الضحية في تطبيقك:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

إذا كان الموقع الضار يقوم اتوماتيكياً بإرسال الاستمارة (form) السابقة فور تحميل الصفحة، فإن المخترق يحتاج فقط لجذب المستخدم غير الحذر لزيارة موقعه وبمجرد زيارته الموقع الضار سيتم فوراً تغيير بريده الاكتروني في تطبيقك. 

لمنع هذه الثغرة، نحتاج لفحص الطلبات من نوع `POST`، `PUT`، `PATCH`، أو `DELETE` القادمة للتطبيق إن كانت تحتوي على قيمة سرية خاصة بالجلسة (session)، حيث لا يمكن للتطبيقات الضارة الوصول لها. 

<a name="preventing-csrf-requests"></a>
## منع الطلبات المزورة عبر المواقع
يقوم إطار عمل لارافيل اوتوماتيكياً بإنشاء "رمز" لمنع الطلبات المزورة عبر المواقع (CSRF token) لكل [جلسة مستخدم](/docs/{{version}}/session) نشطة تتم إدارتها من قبل التطبيق. هذا الرمز (token) يستخدم للتحقق من أن المستخدم الموثق (authenticated user) هو الذي يقوم بإرسال الطلبات للتطبيق. وباعتبار أن هذا الرمز (token) مخزن في جلسة المستخدم ويتغير في كل مرة يتم فيها إعادة إنشاء الجلسة، فإن التطبيق الضار لا يستطيع الوصول لها. 

رمز منع الطلبات المزورة عبر المواقع (CSRF token) الحالي يمكن الوصول له بواسطة الطلب الخاص بالجلسة (request's session) أو بواسطة التابع المساعد (helper function) `csrf_token`: 

    use Illuminate\Http\Request;

    Route::get('/token', function (Request $request) {
        $token = $request->session()->token();

        $token = csrf_token();

        // ...
    });

في كل مرة تقوم فيها بإنشاء استمارة (HTML form) تحتوي على طلبات من نوع  `POST`، `PUT`، `PATCH`، أو `DELETE` في تطبيقك، يجب عليك تضمين حقل مخفي لرمز ( CSRF `_token`) في الاستمارة (form) بحيث يمكن للبرمجية الوسيطة للحماية من الطلبات المزورة عبر المواقع (CSRF protection middleware) التحقق من الطلب. ولتسهيل تلك العملية، يمكنك استخدام الموجه (Blade directive) التالي `@csrf` الذي سيقوم بإنشاء حقل إدخال مخفي لرمز ( CSRF `_token`):

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```
 [البرمجية الوسيطة (middleware)](/docs/{{version}}/middleware)  `App\Http\Middleware\VerifyCsrfToken` والمضمنة بشكل افتراضي في مجموعة البرمجيات الوسيطة `web` 
 أي (`web` middleware group) مما يعني أنه سيتم بشكل تلقائي التحقق من تطابق الرمز (CSRF token) الموجود ضمن الطلب والرمز المخزن ضمن الجلسة. وفي حال تطابق الرمزين يكون المستخدم هو من أرسل الطلب. 

<a name="csrf-tokens-and-spas"></a>
### رموز الحماية من الطلبات المزورة عبر المواقع وتطبيقات الصفحة الواحدة (SPA)
في حال كان تطبيقك تطبيق بصفحة واحدة (SPA) يستخدم لارفيل كواجهة خلفية للتطبيق (backend API)، فعليك مراجعة  [توثيق نظام المصادقة لارافيل سانكتوم (Laravel Sanctum)](/docs/{{version}}/sanctum) لمزيد من المعلومات حول المصادقة بالواجهة التطبيقية لبرنامجك (API) وحمايتها من ثغرات الطلبات المزورة عبر المواقع. 

<a name="csrf-excluding-uris"></a>
### استثناء الروابط (URI) من الحماية من الطلبات المزورة عبر المواقع
في بعض الأحيان تحتاج لاستثناء مجموعة روابط (URIs) من الحماية من الطلبات المزورة عبر المواقع (CSRF protection). على سبيل المثال، اذا كنت تستخدم [سترايب (Stripe)](https://stripe.com) لمعالجة عمليات الدفع وتستفيد من نظام روابط الويب هوك (webhook system) الخاص به، فسوف تحتاج لاستثناء مسار معالج روابط الويب هوك الخاصة بسترايب (Stripe webhook handler route) من هذه الحماية لأن سترايب لا يعلم ما هو رمز (CSRF token) الذي يجب ارساله لمساراتك (routes). 

عادة، يجب عليك وضع هذا النوع من المسارات (routes) خارج مجموعة البرمجيات الوسيطة (`web` middleware group) التي يطبقها `App\Providers\RouteServiceProvider` على جميع المسارات (routes) الموجودة في الملف `routes/web.php` حتى يتم استثنائها. ولكن وبكل الأحوال يمكنك أيضاً استثناء المسارات (routes) بطريقة أخرى عبر وضع روابطها (URIs) في الخاصية `$except` في البرمجية الوسيطة (middleware) `VerifyCsrfToken`: 

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

    class VerifyCsrfToken extends Middleware
    {
        /**
         * The URIs that should be excluded from CSRF verification.
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
            'http://example.com/foo/bar',
            'http://example.com/foo/*',
        ];
    }

> {tip} للسهولة، تكون البرمجية الوسيطة معطلة تلقائياً لكل المسارات (routes) عند [إجراء الاختبارات](/docs/{{version}}/testing).

<a name="csrf-x-csrf-token"></a>
## رمز (X-CSRF-TOKEN)
بالإضافة للتحقق من رمز (CSRF token) كوسيط في طريقة الإرسال POST ستقوم البرمجية الوسيطة `App\Http\Middleware\VerifyCsrfToken` أيضاً من بالتحقق من الترويسة (header)  `X-CSRF-TOKEN` في الطلب، على سبيل المثال يمكنك تخزين الرمز في عنصر `meta` الخاص بلغة HTML: 


```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```
من ثم يمكنك استعمال مكتبة مثل جي كويري (jQuery) لإضافة الرمز (token) تلقائياً لجميع ترويسات الطلبات. مما يوفر حماية سهلة وبسيطة من الطلبات المزورة عبر المواقع لتطبيقك الذي يعتمد على اجاكس (AJAX) باستعمال تقنية قديمة لجافاسكريبت (JavaScript) : 

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## رمز (X-XSRF-TOKEN)

يقوم إطار عمل لارافيل بتخزين رمز (CSRF token) ضمن كوكي (cookie) كرمز مشفر `XSRF-TOKEN` ويقوم بتضمينها في كل رد يقوم بانشائه. حيث يمكنك استعمال قيمة الكوكي (cookie) تلك كقيمة لترويسة `X-XSRF-TOKEN` ضمن الطلب. 

يتم إرسال هذه الكوكي (cookie) بشكل أساسي لتسهيل عمل المطور حيث أن بعض اطر عمل ومكتبات جافاسكريبت (JavaScript)  مثل أنغيولر (Angular) وأكسيوس (Axios)، تقوم بشكل تلقائي بوضع قيمة الترويسة `X-XSRF-TOKEN` على الطلبات من نفس المصدر. 

> {tip} بشكل افترضي، يحتوي الملف `resources/js/bootstrap.js` على مكتبة HTTP الخاصة باكسيوس (Axios) التي ستقوم وبشكل تلقائي بإرسال ترويسة `X-XSRF-TOKEN` لك. 

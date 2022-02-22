# الحماية من الطلبات المزورة عبر المواقع

- [مقدمة](#csrf-introduction)
- [منع الطلبات المزورة عبر المواقع](#preventing-csrf-requests)
    - [Excluding URIs](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## مقدمة

تزوير الطلبات عبر المواقع هو نوع من الثغرات الضارة حيث يتم تنفيذ أوامر غير مصرح بها نيابة المستخدم الموثق (authenticated user). لكن ولحسن الحظ، يقوم إطار عمل  لارافيل بتسهيل حماية تطبيقك من [الطلبات المزورة عبر المواقع](https://en.wikipedia.org/wiki/Cross-site_request_forgery) أو مايعرف بهجمات الطلبات المزورة عبر المواقع (CSRF attacks).

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
يقوم إطار عمل لارافيل اوتوماتيكياً بإنشاء "رمز" لمنع الطلبات المزورة عبر المواقع (CSRF token) لكل [جلسة مستخدم](/docs/{{version}}/session) نشطة تتم إدارتها من قبل التطبيق. هذا الرمز (token) يستخدم للتحقق من أن المستخدم الموثق (authenticated user) هو الذي يقوم بإؤاسل الطلبات للتطبيق. وباعتبار أن هذا الرمز (token) مخزن في جلسة المستخدم ويتغير في كل مرة يتم فيها إعادة إنشاء الجلسة، فإن التطبيق الضار لا يستطيع الوصول لها. 

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
 [البرمجية الوسيطة (middleware)](/docs/{{version}}/middleware) الموجودة في `App\Http\Middleware\VerifyCsrfToken` والمضمنة بشكل افتراضي في مجموعة البرمجيات الوسيطة `web` 
 أي (`web` middleware group) مما يعني أنه بشكل تلقائي سيتم التحقق من تطابق الرمز (CSRF token) الموجود ضمن الطلب والرمز المخزن ضمن الجلسة. في حال تطابق الرمزين يكون المستخدم هو من أرسل الطلب. 

<a name="csrf-tokens-and-spas"></a>
### CSRF Tokens & SPAs

If you are building an SPA that is utilizing Laravel as an API backend, you should consult the [Laravel Sanctum documentation](/docs/{{version}}/sanctum) for information on authenticating with your API and protecting against CSRF vulnerabilities.

<a name="csrf-excluding-uris"></a>
### Excluding URIs From CSRF Protection

Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes.

Typically, you should place these kinds of routes outside of the `web` middleware group that the `App\Providers\RouteServiceProvider` applies to all routes in the `routes/web.php` file. However, you may also exclude the routes by adding their URIs to the `$except` property of the `VerifyCsrfToken` middleware:

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

> {tip} For convenience, the CSRF middleware is automatically disabled for all routes when [running tests](/docs/{{version}}/testing).

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

In addition to checking for the CSRF token as a POST parameter, the `App\Http\Middleware\VerifyCsrfToken` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

Then, you can instruct a library like jQuery to automatically add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications using legacy JavaScript technology:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel stores the current CSRF token in an encrypted `XSRF-TOKEN` cookie that is included with each response generated by the framework. You can use the cookie value to set the `X-XSRF-TOKEN` request header.

This cookie is primarily sent as a developer convenience since some JavaScript frameworks and libraries, like Angular and Axios, automatically place its value in the `X-XSRF-TOKEN` header on same-origin requests.

> {tip} By default, the `resources/js/bootstrap.js` file includes the Axios HTTP library which will automatically send the `X-XSRF-TOKEN` header for you.

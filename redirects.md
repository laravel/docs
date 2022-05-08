# HTTP Redirects

- [إنشاء عمليات إعادة التوجيه (Redirects)](#creating-redirects)
- [ إعادة التوجيه لمسارات (routes) ذات أسماء](#redirecting-named-routes)
- [ إعادة التوجيه لعمليات المتحكم (controller actions)](#redirecting-controller-actions)
- [إعادة التوجيه مع بيانات مخزنة مؤقتاً في الجلسة (Flashed Session Data)](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## إنشاء عمليات إعادة التوجيه (Redirects)

إن ردود إعادة التوجيه (redirect responses) هي نُسخ (instances) من الكائن `Illuminate\Http\RedirectResponse` تحتوي على الترويسات (headers) المطلوبة لإعادة توجيه المستخدم لرابط URL أخر. يوجد عدة طرق لإنشاء نسخة من الكائن `RedirectResponse` وأبسطها هو استعمال التابع المساعد `redirect`: 

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

أحياناً قد ترغب بإعادة توجيه المستخدمين لموقعهم السابق، كما في حالة إرسالهم لبيانات استمارة (form) خاطئة. يمكنك ذلك باستخدام التابع المساعد `back`. وبما أن هذه الميزة تعتمد على [الجلسة (session)](/docs/{{version}}/session) تأكد بأن استدعاء التابع `back` يستعمل مجموعة البرمجيات الوسيطة (middleware group) التالية `web` أو أنه يخضع لتطبيق جميع البرمجيات الوسيطة (middleware) الخاصة بالجلسة: 

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
##  إعادة التوجيه لمسارات (routes) ذات أسماء

عندما تستخدم التابع المساعد `redirect` بدون تمرير وسطاء سيتم إعادة نسخة (instance) من نوع `Illuminate\Routing\Redirector`، مما يسمح لك باستدعاء أي طريقة على النسخة `Redirector`. على سبيل المثال لإنشاء رد `RedirectResponse` على مسار ذو اسم (named route) يمكنك استخدام الطريقة `route`: 

```php
return redirect()->route('login');
```

وفي حال كون المسار (route) يحتوي على وسطاء يمكنك تمريرهم كوسيط ثانٍ للطريقة `route`: 

```php
// For a route with the following URI: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### تمرير النماذج (Eloquent Models) كوسطاء

اذا كنت تعيد التوجيه لمسار (route) يحوي على وسيط  "ID" خاص بنموذج (Eloquent Model)، يمكنك تمرير النموذج (model) نفسه. حيث أنه سيتم استخراج الخاصية "ID" تلقائياً:


```php
// For a route with the following URI: profile/{id}

return redirect()->route('profile', [$user]);
```

اذا كنت تريد تغيير القيمة التي يتم استخراجها عند تمرير النموذج كوسيط للمسار (route) يجب عليك عمل override للطريقة `getRouteKey` في النموذج (Eloquent Model) الخاص بك.: 


```php
/**
 * Get the value of the model's route key.
 *
 * @return mixed
 */
public function getRouteKey()
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
## إعادة التوجيه لعمليات المتحكم (Controller actions)

يمكنك أيضاً إنشاء إعادة توجيه (redirect) [لعمليات متحكم (controller actions)](/docs/{{version}}/controllers) عن طريق تمرير المتحكم واسم العملية للطريقة `action`: 


```php
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

في حال كان مسار المتحكم يحتاج لوسطاء يمكنك تمريرهم كوسيط ثانٍ للطريقة `action`:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## إعادة التوجيه مع بيانات مخزنة مؤقتاً في الجلسة (Flashed Session Data) 

إن عملية إعادة التوجيه لرابط (URL) جديد مع [تخزين بيانات بشكل مؤقت في الجلسة (flashing data to the session)](/docs/{{version}}/session#flash-data) يتم عادة بنفس الوقت. ويتم ذلك بعد تنفيذ إجراء ما بنجاح فتقوم بتخزين رسالة نجاح في الجلسة (session). للسهولة يمكنك انشاء نسخة (instance) من الكائن `RedirectResponse` وتخزينها مؤقتاً في الجلسة في طريقة فردية سلسة ومتسلسلة: 

```php
Route::post('/user/profile', function () {
    // Update the user's profile...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

يمكنك استخدام الطريقة `withInput` التي تقدمها النسخة (instance) من الكائن `RedirectResponse` لتخزين بيانات الدخل الخاصة بالطلب (request) الحالي في الجلسة قبل إعادة توجيه المستخدم لمكان جديد. وعندما يتم تخزين البيانات في الجلسة يمكنك [استعادتها](/docs/{{version}}/requests#retrieving-old-input) بسهولة خلال الطلب (request) التالي: 

```php
return back()->withInput();
```

بعد إعادة توجيه المستخدم يمكنك عرض الرسالة التي تم تخزينها مؤقتاً في [الجلسة](/docs/{{version}}/session). على سبيل المثال باستخدام [تركيب Blade](/docs/{{version}}/blade) التالي: 

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```
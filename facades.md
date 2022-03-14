# Facades

- [مقدمة](#introduction)
- [متى تُستخدم واجهات Facades](#when-to-use-facades)
    - [مقارنة واجهات Facades مع حقن الاعتماديات](#facades-vs-dependency-injection)
    - [مقارنة واجهات Facades بالتوابع المساعدة (Helper Functions)](#facades-vs-helper-functions)
- [كيفية عمل واجهات Facades](#how-facades-work)
- [واجهات Facades أثناء التنفيذ](#real-time-facades)
- [مرجع لكائنات Facades](#facade-class-reference)

<a name="introduction"></a>
## مقدمة

خلال قراءتك لتوثيق لارافيل ستشاهد أمثلة لأكواد تقوم بالتفاعل مع ميزات لارافيل بواسطة "facades". توفر واجهات لارافيل Facades واجهة ستاتيكية (static interface) للكائنات (classes) المتوافرة في [حاوي خدمات](/docs/{{version}}/container) التطبيق. تحتوي لارافيل العديد من واجهات Facades التي توفر الوصول لمعظم ميزات لارافيل. 

تعمل واجهات لارافيل Facades بصفتها وكيل ستاتيكي ("static proxies") للكائنات الأساسية في حاوي الخدمة، حيث توفر ميزة الصياغة المعبرة والموجزة مع الحفاظ على قابلية الاختبار ومرونة أكبر من الطرق الستاتيكية (static methods) التقليدية. من الطبيعي جداً عدم فهمك بشكل كامل لكيفية عمل Facades ضمنياً، عليك فقط بالمسايرة واكمال تعلمك عن لارافيل. 

كل واجهات لارافيل Facades معرفة ضمن نطاق الأسماء `Illuminate\Support\Facades`. أي أنه يمكننا وبسهولة الوصول لـ Facades بالأسلوب التالي: 

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```
خلال توثيق لارافيل يوجد العديد من الأمثلة التي تستعمل واجهات Facades لتوضيح ميزات متنوعة لإطار عمل لارافيل. 

<a name="helper-functions"></a>
#### التوابع المساعدة (Helper Functions)

واستكمالاً لواجهات Facades تقدم لارافيل عدة توابع مساعدة متنوعة لتجعل التعامل مع الميزات العامة في لارافيل أكثر سهولة. قد تتعامل مع بعض التوابع المساعدة الشائعة مثل `view`، `response`، `url`، `config` وغيرها المزيد. كل تابع مساعد مقدم من لارافيل يتم توثيقه مع الميزة التي يقدمها، وبكل الأحوال تتوفر لائحة كاملة في [التوثيق المخصص للتوابع المساعدة](/docs/{{version}}/helpers) .

على سبيل المثال، بدلاً من استخدام الـ  Facade التالي `Illuminate\Support\Facades\Response` لانشاء رد (response) من النوع JSON يمكنك ببساطة استخدام التابع المساعد `response`. ولأن التوابع المساعدة متوفرة على نطاق التطبيق (globally available)، لست بحاجة لاستيراد (import) أي صفوف لاستخدمها: 

```php
use Illuminate\Support\Facades\Response;

Route::get('/users', function () {
    return Response::json([
        // ...
    ]);
});

Route::get('/users', function () {
    return response()->json([
        // ...
    ]);
});
```

<a name="when-to-use-facades"></a>
## متى تُستخدم واجهات Facades

إن واجهات Facades عديدة الفوائد. فهي توفر صياغة موجزة وقابلة للتذكر مما يتيح استخدام ميزات لارافيل بدون تذكر أسماء الكائنات الطويلة التي يجب حقنها أو اعدادها يدوياً. وبسبب استخدامها الفريد لطرائق PHP الديناميكية يجعلها ذلك سهلة الاختبار أيضاً. 

بكل الأحوال، يجب الاحتياط قليلاً عند استعمال واجهات Facades. لأن خطرها الرئيسي يكمن بتمدد نطاق الكائن ("scope creep"). بما أن واجهات Facades سهلة الاستعمال ولا تحتاج لحقن، فمن السهولة أن تتضخم كائناتك (classes) عند استخدام أكثر من واجهة Facade في كائن واحد. إن استخدام حقن الاعتماديات من المحتمل أن يحد من المشكلة بسبب التحذيرات المرئية التي يصدرها الباني (constructor) الضخم بأن الكائن يتضخم بشكل كبير. فعند استخدامك لواجهات Facades يجب إعارة انتباه خاص لحجم الكائن لكي يبقى نطاق مسؤليته (scope of responsibility) ضيقاً. وفي حال تضخم الكائن كثيراً، قد تحتاج لتقسيمه لعدة كائنات أصغر. 

<a name="facades-vs-dependency-injection"></a>
### مقارنة واجهات Facades مع حقن الاعتماديات

واحد من الفوائد الأساسية لحقن الاعتمادية هو امكانية تبديل استخدامات (implementations) الكائن الذي تم حقنه. مما يفيد أثناء الاختبار حيث يمكنك حقن غرض مُقلِّد (mock) أو نموذج القابل للاستبدال (stub) وتتحقق من استدعاء مختلف الطرق فيها.

عملياً، ليس من الممكن استخدام الأغراض المُقلِّدة (mock) أو النماذج القابلة للاستبدال (stubs) على طريقة ستاتيكية للكائن. ولكن ولأن واجهات Facades تستخدم الطرق الديناميكة لتوكيل طرق لاستدعاء الكائنات تم الحصول عليها بواسطة حاوي الخدمة، يمكننا في الواقع اختبار Facades كما يمكننا اختبار نسخة (instance) لكائن تم حقنه. على سبيل المثال ليكن لدينا المسار (route) التالي: 

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

باستخدام طرق الاختبار الخاصة بلارافيل Facade، يمكننا كتابة النص التالي للتحقق من أنه تم استدعاء الطريقة `Cache::get` بالوسيط الذي نتوقعه:

```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 *
 * @return void
 */
public function testBasicExample()
{
    Cache::shouldReceive('get')
         ->with('key')
         ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="facades-vs-helper-functions"></a>
### مقارنة واجهات Facades بالتوابع المساعدة (Helper Functions)

بالإضافة لواجهات Facades تحتوي لارافيل العديد من التوابع المساعدة التي تقوم بالمهام الشائعة كإنشاء واجهات (views)، إطلاق الأحداث (events)، توزيع الأعمال، أو ارسال ردود (responses) من نوع HTTP. والعديد من هذه التوابع المساعدة يقوم بتنفيذ الوظيفة نفسها لواجهة Facade المقابلة لها، فعلى سبيل المثال استدعاء واجهة Facade التالي مطابق  لاستدعاء التابع المساعد: 

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

عملياً لا يوجد أي فرق بين واجهات Facades والتوابع المساعدة. عند استخدام التوابع المساعدة، يمكنك اختبارها بنفس الأسلوب الذي قد تختبر فيه واجهة Facade  الموافقة. على سبيل المثال ليكن لدينا المسار (route) التالي:

```php
Route::get('/cache', function () {
    return cache('key');
});
```
ضمنياً يقوم لتابع المساعد `cache` باستدعاء الطريقة `get` على الكائن المضمن في واجهة Facade التالية `Cache`. مما يعني أنه حتى لو قمنا باستخدام التابع المساعد، يمكننا كتابة الاختبار التالي للتأكد من أنه تم استدعاء الطريقة بالوسيط الذي نتوقعه: 


```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 *
 * @return void
 */
public function testBasicExample()
{
    Cache::shouldReceive('get')
            ->with('key')
            ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="how-facades-work"></a>
## كيفية عمل واجهات Facades

في تطبيق لارافيل، واجهة Facade هي كائن يوفر الوصول لكائن من حاوي الخدمات. حيث أن الآلية التي تسمح بذلك موجودة في الكائن `Facade`. إن واجهات لارافيل Facades وأي واجهات Facades تقوم بإنشائها، سوف ترث من الكائن الأساسي (base class) `Illuminate\Support\Facades\Facade`. 

الكائن الأساسي `Facade` يستخدم الطريقة الجاهزة (magic-method) `()callStatic__` لتحويل الاستدعاءات من واجهة Facade لكائن يتم الحصول عليه من حاوي الخدمات. في المثال التالي، سيتم استدعاء نظام الذاكرة المؤقت (cache system) الخاص بلارافيل. عند القاء نظرة على هذا الكود قد تظن بأن الطريقة الستاتيكية `get` يتم استدعائها على الصف `Cache`: 


```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     *
     * @param  int  $id
     * @return Response
     */
    public function showProfile($id)
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

لاحظ في أعلى الملف بأننا نقوم باستيراد (importing) واجهة Facade التالية `Cache`. حيث تقوم واجهة Facade بالعمل كوكيل للوصول للاستخدام (implementation) الخاص بالواجهة `Illuminate\Contracts\Cache\Factory`. حيث أن أي استدعاءات نقوم بها باستخدام واجهة Facade سيتم تمريرها للنسخة (instance) الضمنية في خدمة الذاكرة المؤقتة في لارافيل. 

اذا قمنا بإلقاء نظرة على الكائن `Illuminate\Support\Facades\Cache` ستجد بأنه لا وجود للطريقة الستاتيكية `get`: 

```php
class Cache extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor() { return 'cache'; }
}
```
بدلاً من ذلك ترث واجهة Facade التالية `Cache` من الصف الأساسي `Facade` وتُعرِّف الطريقة `()getFacadeAccessor`. إن مهمة هذه الطريقة هو إعادة اسم ارتباط خاص بحاوي الخدمات. عندما يشير المستخدم لأي طريقة ستاتيكية في واجهة Facade التالية `Cache` ستقوم لارافيل بالحصول على الارتباط بين `cache` و [حاوي الخدمات](/docs/{{version}}/container) وتنفيذ الطريقة المطلوبة (في هذه الحالة الطريقة `get`) على الكائن. 

<a name="real-time-facades"></a>
## واجهات Facades أثناء التنفيذ

يمكنك معاملة أي كائن من كائناتك بالتطبيق كما لو كان واجهة Facades باستخدام واجهات Facades أثناء التنفيذ. لتوضيح كيفية استخدام ذلك، دعنا بدايةً نتصفح بعض الأكواد التي لا تستخدم واجهات Facades أثناء التنفيذ. على سبيل المثال لنفترض بأن النموذج (model) التالي `Podcast` يحتوي على طريقة `publish`. حسناً لكي نقوم بنشر بودكاست نحتاج لحقن نسخة (instance) من الناشر `Publisher`: 


```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     *
     * @param  Publisher  $publisher
     * @return void
     */
    public function publish(Publisher $publisher)
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```
 يسمح لنا حقن استخدام (implementation) للناشر publisher في الطريقة باختبار الطريقة على انفراد طالما أننا قادرون على تقليد (mock) الناشر الذي تم حقنه. بكل الأحوال مطلوب بشكل دائم تمرير نسخة (instance) من الناشر publisher في كل مرة نقوم  فيها باستدعاء الطريقة `publish`. لذلك وباستخدام واجهات Facades  أثناء التنفيذ يمكننا المحافظة على قابلية الاختبار بدون أن نكون مطالبين بشكل صريح بتمرير نسخة من `Publisher`. لإنشاء واجهة Facade أثناء التنفيذ أضف كلمة `Facades` كبادئة لنطاق الأسماء (namespace) للكائن المستورد (imported class): 

```php
<?php

namespace App\Models;

use Facades\App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
        * Publish the podcast.
        *
        * @return void
        */
    public function publish()
    {
        $this->update(['publishing' => now()]);

        Publisher::publish($this);
    }
}
```

عند استخدام واجهات Facades  أثناء التنفيذ سيتم الحصول على استخدام (implementation) للواجهة publisher من حاوي الخدمات باستخدام جزء من الواجهة أو اسم الكائن الذي يظهر بعد البادئة `Facades`. عند الاختبار يمكننا استخدام التوابع المساعدة للاختبار المُدمجة بلارافيل لتقليد (mock) استدعاء هذه الطريقة: 

```php
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A test example.
     *
     * @return void
     */
    public function test_podcast_can_be_published()
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a name="facade-class-reference"></a>
## مرجع لكائنات Facades

ستجد في الأسفل كل واجهات Facades وكائناتها الضمنية(underlying classes). يوفر هذا أداة سهلة للبحث عن أصل واجهة Facade في توثيق API الخاص بلارافيل. كما يتوفر [مفتاح الارتباط الخاص بحاوي الخدمات](/docs/{{version}}/container) في الأماكن المناسبة:

Facade  |  Class  |  Service Container Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html)  |  `app`
Artisan  |  [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (Instance)  |  [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Guard.html)  |  `auth.driver`
Blade  |  [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Broadcast  |  [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html)  |  &nbsp;
Broadcast (Instance)  |  [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html)  |  &nbsp;
Bus  |  [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html)  |  &nbsp;
Cache  |  [Illuminate\Cache\CacheManager](https://laravel.com/api/{{version}}/Illuminate/Cache/CacheManager.html)  |  `cache`
Cache (Instance)  |  [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html)  |  `cache.store`
Config  |  [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
Date  |  [Illuminate\Support\DateFactory](https://laravel.com/api/{{version}}/Illuminate/Support/DateFactory.html)  |  `date`
DB  |  [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html)  |  `db.connection`
Event  |  [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html)  |  `files`
Gate  |  [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html)  |  &nbsp;
Hash  |  [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash`
Http  |  [Illuminate\Http\Client\Factory](https://laravel.com/api/{{version}}/Illuminate/Http/Client/Factory.html)  |  &nbsp;
Lang  |  [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\LogManager](https://laravel.com/api/{{version}}/Illuminate/Log/LogManager.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html)  |  `mailer`
Notification  |  [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html)  |  &nbsp;
Password  |  [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html)  |  `auth.password`
Password (Instance)  |  [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.password.broker`
Queue  |  [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance)  |  [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html)  |  `queue.connection`
Queue (Base Class)  |  [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html)  |  &nbsp;
Redirect  |  [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\RedisManager](https://laravel.com/api/{{version}}/Illuminate/Redis/RedisManager.html)  |  `redis`
Redis (Instance)  |  [Illuminate\Redis\Connections\Connection](https://laravel.com/api/{{version}}/Illuminate/Redis/Connections/Connection.html)  |  `redis.connection`
Request  |  [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html)  |  &nbsp;
Response (Instance)  |  [Illuminate\Http\Response](https://laravel.com/api/{{version}}/Illuminate/Http/Response.html)  |  &nbsp;
Route  |  [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Builder](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Builder.html)  |  &nbsp;
Session  |  [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html)  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html)  |  `session.store`
Storage  |  [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/{{version}}/Illuminate/Filesystem/FilesystemManager.html)  |  `filesystem`
Storage (Instance)  |  [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html)  |  `filesystem.disk`
URL  |  [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html)  |  &nbsp;
View  |  [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html)  |  &nbsp;

---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Валідація

- [Вступ](#introduction)
- [Швидкий старт](#validation-quickstart)
    - [Визначення маршрутів](#quick-defining-the-routes)
    - [Створення контролера](#quick-creating-the-controller)
    - [Написання логіки валідації](#quick-writing-the-validation-logic)
    - [Виведення помилок валідації](#quick-displaying-the-validation-errors)
    - [Повторне заповнення форм](#repopulating-forms)
    - [Зауваження про необов'язкові поля](#a-note-on-optional-fields)
    - [Формат відповіді з помилками валідації](#validation-error-response-format)
- [Валідація через запити форм](#form-request-validation)
    - [Створення запитів форм](#creating-form-requests)
    - [Авторизація запитів форм](#authorizing-form-requests)
    - [Налаштування повідомлень про помилки](#customizing-the-error-messages)
    - [Підготовка даних до валідації](#preparing-input-for-validation)
- [Ручне створення валідаторів](#manually-creating-validators)
    - [Автоматичне перенаправлення](#automatic-redirection)
    - [Іменовані набори помилок](#named-error-bags)
    - [Налаштування повідомлень про помилки](#manual-customizing-the-error-messages)
    - [Додаткова валідація](#performing-additional-validation)
- [Робота з валідованими даними](#working-with-validated-input)
- [Робота з повідомленнями про помилки](#working-with-error-messages)
    - [Власні повідомлення у мовних файлах](#specifying-custom-messages-in-language-files)
    - [Атрибути у мовних файлах](#specifying-attribute-in-language-files)
    - [Значення у мовних файлах](#specifying-values-in-language-files)
- [Доступні правила валідації](#available-validation-rules)
- [Умовне додавання правил](#conditionally-adding-rules)
- [Валідація масивів](#validating-arrays)
    - [Валідація вкладених масивів](#validating-nested-array-input)
    - [Індекси та позиції в повідомленнях про помилки](#error-message-indexes-and-positions)
- [Валідація файлів](#validating-files)
- [Валідація паролів](#validating-passwords)
- [Власні правила валідації](#custom-validation-rules)
    - [Використання об'єктів правил](#using-rule-objects)
    - [Використання замикань](#using-closures)
    - [Неявні правила](#implicit-rules)

<a name="introduction"></a>
## Вступ

Laravel пропонує кілька різних підходів до валідації вхідних даних вашого застосунку. Найпоширеніший - скористатися методом `validate`, доступним для всіх вхідних HTTP-запитів. Утім, ми розглянемо й інші підходи до валідації.

Laravel містить широкий набір зручних правил валідації, які ви можете застосовувати до даних, - зокрема можливість перевірити унікальність значення в певній таблиці бази даних. Ми детально розглянемо кожне з цих правил, щоб ви ознайомилися з усіма можливостями валідації в Laravel.

<a name="validation-quickstart"></a>
## Швидкий старт

Щоб дізнатися про потужні можливості валідації в Laravel, розгляньмо повний приклад валідації форми та показу повідомлень про помилки користувачеві. Прочитавши цей загальний огляд, ви добре зрозумієте, як валідувати вхідні дані запиту засобами Laravel:

<a name="quick-defining-the-routes"></a>
### Визначення маршрутів

Спершу припустімо, що ми маємо такі маршрути у файлі `routes/web.php`:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

Маршрут `GET` показуватиме форму створення нового допису блогу, а маршрут `POST` зберігатиме допис у базі даних.

<a name="quick-creating-the-controller"></a>
### Створення контролера

Далі погляньмо на простий контролер, що обробляє вхідні запити до цих маршрутів. Метод `store` поки залишимо порожнім:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate and store the blog post...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### Написання логіки валідації

Тепер ми готові заповнити метод `store` логікою валідації нового допису. Для цього скористаємося методом `validate`, який надає об'єкт `Illuminate\Http\Request`. Якщо правила валідації пройдено, ваш код виконуватиметься далі як звичайно; однак якщо валідація не пройшла, буде викинуто виняток `Illuminate\Validation\ValidationException`, і користувачеві автоматично буде надіслано відповідну відповідь із помилкою.

Якщо валідація не пройшла під час традиційного HTTP-запиту, буде згенеровано відповідь-перенаправлення на попередню адресу. Якщо вхідний запит є XHR-запитом, буде повернуто [JSON-відповідь із повідомленнями про помилки валідації](#validation-error-response-format).

Щоб краще зрозуміти метод `validate`, повернімося до методу `store`:

```php
/**
 * Store a new blog post.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

    // The blog post is valid...

    return redirect('/posts');
}
```

Як бачите, правила валідації передаються методу `validate`. Не хвилюйтеся - усі доступні правила [задокументовано](#available-validation-rules). Знову ж таки, якщо валідація не пройде, відповідну відповідь буде згенеровано автоматично. Якщо валідація пройшла, наш контролер продовжить виконуватися як звичайно.

Крім того, ви можете скористатися методом `validateWithBag`, щоб валідувати запит і зберегти повідомлення про помилки в [іменованому наборі помилок](#named-error-bags):

```php
$validated = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### Зупинка на першій невдалій перевірці

Іноді ви можете захотіти припинити виконання правил валідації для атрибута після першої невдачі. Для цього призначте атрибуту правило `bail`:

```php
$request->validate([
    'title' => ['bail', 'required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

У цьому прикладі, якщо правило `unique` для атрибута `title` не пройде, правило `max` не перевірятиметься. Правила перевіряються в порядку їх призначення.

<a name="a-note-on-nested-attributes"></a>
#### Зауваження про вкладені атрибути

Якщо вхідний HTTP-запит містить «вкладені» дані полів, ви можете вказати ці поля у правилах валідації через «крапковий» синтаксис:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'author.name' => ['required'],
    'author.description' => ['required'],
]);
```

З іншого боку, якщо ім'я вашого поля містить справжню крапку, ви можете явно запобігти її трактуванню як «крапкового» синтаксису, екранувавши її зворотним слешем:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'v1\.0' => ['required'],
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### Виведення помилок валідації

Отже, що станеться, якщо поля вхідного запиту не пройдуть указаних правил валідації? Як згадувалося раніше, Laravel автоматично перенаправить користувача на попередню сторінку. Крім того, усі помилки валідації та [вхідні дані запиту](/docs/{{version}}/requests#retrieving-old-input) буде автоматично [записано до сесії](/docs/{{version}}/session#flash-data).

Змінна `$errors` доступна всім представленням вашого застосунку завдяки `middleware` `Illuminate\View\Middleware\ShareErrorsFromSession`, який входить до групи `web`. Коли цей `middleware` застосовано, змінна `$errors` завжди доступна у ваших представленнях, тож ви можете спокійно вважати, що вона завжди визначена. Змінна `$errors` є екземпляром `Illuminate\Support\MessageBag`. Докладніше про роботу з цим об'єктом читайте в [його документації](#working-with-error-messages).

Тож у нашому прикладі, коли валідація не пройде, користувача буде перенаправлено до методу `create` нашого контролера, що дозволить показати повідомлення про помилки в представленні:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>Create Post</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```

<a name="quick-customizing-the-error-messages"></a>
#### Налаштування повідомлень про помилки

Кожне вбудоване правило валідації Laravel має повідомлення про помилку, розташоване у файлі `lang/en/validation.php` вашого застосунку. Якщо ваш застосунок не має каталогу `lang`, ви можете створити його командою Artisan `lang:publish`.

У файлі `lang/en/validation.php` ви знайдете запис перекладу для кожного правила валідації. Ви вільні змінювати ці повідомлення відповідно до потреб свого застосунку.

Крім того, ви можете скопіювати цей файл до каталогу іншої мови, щоб перекласти повідомлення мовою вашого застосунку. Докладніше про локалізацію в Laravel читайте в повній [документації з локалізації](/docs/{{version}}/localization).

> [!WARNING]
> За замовчуванням каркас застосунку Laravel не містить каталогу `lang`. Якщо ви хочете налаштувати мовні файли Laravel, опублікуйте їх командою Artisan `lang:publish`.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR-запити та валідація

У цьому прикладі ми використали традиційну форму для надсилання даних застосунку. Однак багато застосунків отримують XHR-запити від фронтенду на JavaScript. Використовуючи метод `validate` під час XHR-запиту, Laravel не генеруватиме відповідь-перенаправлення. Натомість Laravel згенерує [JSON-відповідь з усіма помилками валідації](#validation-error-response-format). Цю JSON-відповідь буде надіслано зі статус-кодом 422.

<a name="the-at-error-directive"></a>
#### Директива `@error`

Ви можете скористатися директивою [Blade](/docs/{{version}}/blade) `@error`, щоб швидко визначити, чи існують повідомлення про помилки валідації для певного атрибута. Усередині директиви `@error` ви можете вивести змінну `$message`, щоб показати повідомлення про помилку:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

Якщо ви користуєтеся [іменованими наборами помилок](#named-error-bags), передайте ім'я набору другим аргументом директиви `@error`:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### Повторне заповнення форм

Коли Laravel генерує відповідь-перенаправлення через помилку валідації, фреймворк автоматично [записує всі вхідні дані запиту до сесії](/docs/{{version}}/session#flash-data). Це робиться для того, щоб ви могли зручно звернутися до цих даних під час наступного запиту й заново заповнити форму, яку намагався надіслати користувач.

Щоб отримати збережені дані попереднього запиту, викличте метод `old` на екземплярі `Illuminate\Http\Request`. Метод `old` візьме раніше збережені дані із [сесії](/docs/{{version}}/session):

```php
$title = $request->old('title');
```

Laravel також надає глобальний хелпер `old`. Якщо ви показуєте попередні дані в [шаблоні Blade](/docs/{{version}}/blade), зручніше скористатися хелпером `old`, щоб заново заповнити форму. Якщо попередніх даних для вказаного поля немає, буде повернуто `null`:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### Зауваження про необов'язкові поля

За замовчуванням Laravel додає `middleware` `TrimStrings` та `ConvertEmptyStringsToNull` до глобального стека вашого застосунку. Через це вам часто доведеться позначати «необов'язкові» поля запиту як `nullable`, якщо ви не хочете, щоб валідатор вважав значення `null` недійсними. Наприклад:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
    'publish_at' => ['nullable', 'date'],
]);
```

У цьому прикладі ми вказуємо, що поле `publish_at` може бути або `null`, або дійсним поданням дати. Якщо модифікатор `nullable` не додати до визначення правила, валідатор вважатиме `null` недійсною датою.

<a name="validation-error-response-format"></a>
### Формат відповіді з помилками валідації

Коли ваш застосунок викидає виняток `Illuminate\Validation\ValidationException`, а вхідний HTTP-запит очікує JSON-відповідь, Laravel автоматично відформатує повідомлення про помилки й поверне HTTP-відповідь `422 Unprocessable Entity`.

Нижче наведено приклад формату JSON-відповіді для помилок валідації. Зверніть увагу: вкладені ключі помилок зводяться до «крапкової» нотації:

```json
{
    "message": "The team name must be a string. (and 4 more errors)",
    "errors": {
        "team_name": [
            "The team name must be a string.",
            "The team name must be at least 1 characters."
        ],
        "authorization.role": [
            "The selected authorization.role is invalid."
        ],
        "users.0.email": [
            "The users.0.email field is required."
        ],
        "users.2.email": [
            "The users.2.email must be a valid email address."
        ]
    }
}
```

<a name="form-request-validation"></a>
## Валідація через запити форм

<a name="creating-form-requests"></a>
### Створення запитів форм

Для складніших сценаріїв валідації ви можете створити «запит форми» (form request). Запити форм - це власні класи запитів, що інкапсулюють власну логіку валідації та авторизації. Щоб створити клас запиту форми, скористайтеся командою Artisan `make:request`:

```shell
php artisan make:request StorePostRequest
```

Згенерований клас запиту форми буде розміщено в каталозі `app/Http/Requests`. Якщо цього каталогу немає, його буде створено під час виконання команди `make:request`. Кожен згенерований Laravel запит форми має два методи: `authorize` і `rules`.

Як ви могли здогадатися, метод `authorize` відповідає за визначення того, чи може поточний автентифікований користувач виконати дію, яку представляє запит, а метод `rules` повертає правила валідації, що мають застосовуватися до даних запиту:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
 */
public function rules(): array
{
    return [
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ];
}
```

> [!NOTE]
> Ви можете вказати типи будь-яких потрібних залежностей у сигнатурі методу `rules`. Їх буде автоматично розв'язано через [сервіс-контейнер](/docs/{{version}}/container) Laravel.

Отже, як обчислюються правила валідації? Вам потрібно лише вказати тип запиту в методі контролера. Вхідний запит форми валідується до виклику методу контролера, тобто вам не потрібно захаращувати контролер логікою валідації:

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // Store the blog post...

    return redirect('/posts');
}
```

Якщо валідація не пройде, буде згенеровано відповідь-перенаправлення, щоб повернути користувача на попередню сторінку. Помилки також буде записано до сесії, щоб їх можна було показати. Якщо запит був XHR-запитом, користувачеві буде повернуто HTTP-відповідь зі статус-кодом 422, що містить [JSON-подання помилок валідації](#validation-error-response-format).

> [!NOTE]
> Потрібно додати валідацію запитів форм у реальному часі до вашого фронтенду на Inertia? Перегляньте [Laravel Precognition](/docs/{{version}}/precognition).

<a name="performing-additional-validation-on-form-requests"></a>
#### Додаткова валідація

Іноді вам потрібно виконати додаткову валідацію після завершення початкової. Це робиться методом `after` запиту форми.

Метод `after` має повертати масив викликаних об'єктів чи замикань, які буде виконано після завершення валідації. Передані об'єкти отримають екземпляр `Illuminate\Validation\Validator`, що дозволить за потреби додати нові повідомлення про помилки:

```php
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    'Something is wrong with this field!'
                );
            }
        }
    ];
}
```

Як зазначено, масив, повернений методом `after`, може також містити викликані класи. Метод `__invoke` цих класів отримає екземпляр `Illuminate\Validation\Validator`:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        new ValidateUserStatus,
        new ValidateShippingTime,
        function (Validator $validator) {
            //
        }
    ];
}
```

<a name="request-stopping-on-first-validation-rule-failure"></a>
#### Зупинка на першій невдалій перевірці

Додавши до класу запиту атрибут `StopOnFirstFailure`, ви можете повідомити валідатор, що йому слід припинити валідацію всіх атрибутів після першої ж невдачі:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a name="request-failing-on-unknown-fields"></a>
#### Відхилення невідомих полів

Додавши до класу запиту атрибут `FailOnUnknownFields`, ви можете вказати Laravel відхиляти будь-які вхідні поля, не визначені правилами валідації вашого запиту:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\FailOnUnknownFields;
use Illuminate\Foundation\Http\FormRequest;

#[FailOnUnknownFields]
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string'],
            'body' => ['required', 'string'],
        ];
    }
}
```

Ви також можете увімкнути цю поведінку глобально для всіх запитів форм зі свого `AppServiceProvider`:

```php
use Illuminate\Foundation\Http\FormRequest;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    FormRequest::failOnUnknownFields();
}
```

За потреби ви можете вимкнути цю поведінку для конкретного запиту, передавши атрибуту `false`:

```php
#[FailOnUnknownFields(false)]
class PublicWebhookRequest extends FormRequest
{
    // ...
}
```

Відхилення невідомих полів дає додатковий захист від проблем на кшталт mass-assignment, не даючи неочікуваним ключам потрапляти глибше у ваш застосунок. Утім, вам усе одно слід налаштувати властивості `$fillable` / `$guarded` своєї моделі та зберігати лише довірені валідовані дані.

<a name="customizing-the-redirect-location"></a>
#### Налаштування адреси перенаправлення

Коли валідація запиту форми не проходить, генерується відповідь-перенаправлення, що повертає користувача на попередню сторінку. Утім, ви вільні налаштувати цю поведінку. Для цього скористайтеся атрибутом `RedirectTo` у своєму запиті форми:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectTo;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectTo('/dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

Або, якщо ви хочете перенаправляти користувачів до іменованого маршруту, скористайтеся натомість атрибутом `RedirectToRoute`:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectToRoute;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectToRoute('dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a name="customizing-the-error-bag"></a>
#### Налаштування набору помилок

Коли валідація запиту форми не проходить, помилки записуються до набору `default`. Якщо вам потрібно зберігати їх в іншому [іменованому наборі помилок](#named-error-bags), скористайтеся атрибутом `ErrorBag` у своєму запиті форми:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\ErrorBag;
use Illuminate\Foundation\Http\FormRequest;

#[ErrorBag('login')]
class LoginRequest extends FormRequest
{
    // ...
}
```

<a name="authorizing-form-requests"></a>
### Авторизація запитів форм

Клас запиту форми також містить метод `authorize`. У ньому ви можете визначити, чи справді автентифікований користувач має право оновити певний ресурс. Наприклад, ви можете визначити, чи справді користувач володіє коментарем у блозі, який намагається оновити. Найімовірніше, у цьому методі ви взаємодіятимете зі своїми [гейтами та політиками авторизації](/docs/{{version}}/authorization):

```php
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

Оскільки всі запити форм успадковують базовий клас запиту Laravel, ми можемо скористатися методом `user`, щоб отримати поточного автентифікованого користувача. Також зверніть увагу на виклик методу `route` у прикладі вище. Він дає доступ до параметрів URI, визначених у маршруті, який викликається, - як-от параметр `{comment}` у прикладі нижче:

```php
Route::post('/comment/{comment}');
```

Тому, якщо ваш застосунок використовує [прив'язку моделей до маршрутів](/docs/{{version}}/routing#route-model-binding), ваш код можна зробити ще стислішим, звернувшись до розв'язаної моделі як до властивості запиту:

```php
return $this->user()->can('update', $this->comment);
```

Якщо метод `authorize` поверне `false`, автоматично буде повернуто HTTP-відповідь зі статус-кодом 403, а метод вашого контролера не виконається.

Якщо ви плануєте обробляти логіку авторизації запиту в іншій частині застосунку, ви можете цілком прибрати метод `authorize` або просто повертати `true`:

```php
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> Ви можете вказати типи будь-яких потрібних залежностей у сигнатурі методу `authorize`. Їх буде автоматично розв'язано через [сервіс-контейнер](/docs/{{version}}/container) Laravel.

<a name="customizing-the-error-messages"></a>
### Налаштування повідомлень про помилки

Ви можете налаштувати повідомлення про помилки, які використовує запит форми, перевизначивши метод `messages`. Цей метод має повертати масив пар «атрибут / правило» та відповідних повідомлень про помилки:

```php
/**
 * Get the error messages for the defined validation rules.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### Налаштування атрибутів валідації

Багато вбудованих повідомлень про помилки валідації в Laravel містять заповнювач `:attribute`. Якщо ви хочете, щоб заповнювач `:attribute` у вашому повідомленні замінювався власним іменем атрибута, вкажіть власні імена, перевизначивши метод `attributes`. Цей метод має повертати масив пар «атрибут / ім'я»:

```php
/**
 * Get custom attributes for validator errors.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => 'email address',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### Підготовка даних до валідації

Якщо вам потрібно підготувати чи очистити дані запиту перед застосуванням правил валідації, скористайтеся методом `prepareForValidation`:

```php
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

Так само, якщо вам потрібно нормалізувати дані запиту після завершення валідації, скористайтеся методом `passedValidation`:

```php
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## Ручне створення валідаторів

Якщо ви не хочете використовувати метод `validate` на запиті, ви можете створити екземпляр валідатора вручну через [фасад](/docs/{{version}}/facades) `Validator`. Метод `make` фасаду створює новий екземпляр валідатора:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => ['required', 'unique:posts', 'max:255'],
            'body' => ['required'],
        ]);

        if ($validator->fails()) {
            return redirect('/post/create')
                ->withErrors($validator)
                ->withInput();
        }

        // Retrieve the validated input...
        $validated = $validator->validated();

        // Retrieve a portion of the validated input...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // Store the blog post...

        return redirect('/posts');
    }
}
```

Перший аргумент, переданий методу `make`, - дані, що підлягають валідації. Другий - масив правил валідації, які слід застосувати до цих даних.

Визначивши, що валідація запиту не пройшла, ви можете скористатися методом `withErrors`, щоб записати повідомлення про помилки до сесії. Використовуючи цей метод, змінна `$errors` автоматично стане доступною вашим представленням після перенаправлення, що дозволить легко показати помилки користувачеві. Метод `withErrors` приймає валідатор, `MessageBag` або PHP-масив.

#### Зупинка на першій невдалій перевірці

Метод `stopOnFirstFailure` повідомить валідатор, що йому слід припинити валідацію всіх атрибутів після першої ж невдачі:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### Автоматичне перенаправлення

Якщо ви хочете створити екземпляр валідатора вручну, але водночас скористатися автоматичним перенаправленням, яке дає метод `validate` HTTP-запиту, викличте метод `validate` на наявному екземплярі валідатора. Якщо валідація не пройде, користувача буде автоматично перенаправлено або, у випадку XHR-запиту, [повернено JSON-відповідь](#validation-error-response-format):

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validate();
```

Ви можете скористатися методом `validateWithBag`, щоб зберегти повідомлення про помилки в [іменованому наборі помилок](#named-error-bags), якщо валідація не пройде:

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### Іменовані набори помилок

Якщо на одній сторінці у вас кілька форм, ви можете захотіти дати ім'я `MessageBag`, що містить помилки валідації, аби отримувати повідомлення для конкретної форми. Для цього передайте ім'я другим аргументом `withErrors`:

```php
return redirect('/register')->withErrors($validator, 'login');
```

Далі ви можете звернутися до іменованого екземпляра `MessageBag` через змінну `$errors`:

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### Налаштування повідомлень про помилки

За потреби ви можете надати власні повідомлення про помилки, які валідатор використовуватиме замість типових повідомлень Laravel. Указати власні повідомлення можна кількома способами. По-перше, ви можете передати їх третім аргументом методу `Validator::make`:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

У цьому прикладі заповнювач `:attribute` буде замінено фактичним іменем поля, що валідується. Ви можете використовувати й інші заповнювачі в повідомленнях валідації. Наприклад:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### Власне повідомлення для конкретного атрибута

Іноді ви можете захотіти вказати власне повідомлення лише для конкретного атрибута. Це робиться через «крапкову» нотацію: спершу ім'я атрибута, потім правило:

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### Власні значення атрибутів

Багато вбудованих повідомлень про помилки Laravel містять заповнювач `:attribute`, який замінюється іменем поля чи атрибута, що валідується. Щоб налаштувати значення для заміни цих заповнювачів у конкретних полях, передайте масив власних атрибутів четвертим аргументом методу `Validator::make`:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### Додаткова валідація

Іноді вам потрібно виконати додаткову валідацію після завершення початкової. Це робиться методом `after` валідатора. Метод `after` приймає замикання або масив викликаних об'єктів, які буде виконано після завершення валідації. Вони отримають екземпляр `Illuminate\Validation\Validator`, що дозволить за потреби додати нові повідомлення про помилки:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

Як зазначено, метод `after` також приймає масив викликаних об'єктів - це особливо зручно, якщо ваша логіка «після валідації» інкапсульована у викликаних класах, які отримають екземпляр `Illuminate\Validation\Validator` через метод `__invoke`:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;

$validator->after([
    new ValidateUserStatus,
    new ValidateShippingTime,
    function ($validator) {
        // ...
    },
]);
```

<a name="working-with-validated-input"></a>
## Робота з валідованими даними

Провалідувавши вхідні дані запиту через запит форми чи створений вручну валідатор, ви можете захотіти отримати саме ті дані, які пройшли валідацію. Це можна зробити кількома способами. По-перше, ви можете викликати метод `validated` на запиті форми чи екземплярі валідатора. Цей метод повертає масив валідованих даних:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

Як альтернативу ви можете викликати метод `safe` на запиті форми чи екземплярі валідатора. Він повертає екземпляр `Illuminate\Support\ValidatedInput`. Цей об'єкт має методи `only`, `except` і `all`, щоб отримати підмножину валідованих даних або весь їх масив:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

Крім того, екземпляр `Illuminate\Support\ValidatedInput` можна ітерувати й звертатися до нього як до масиву:

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

Якщо ви хочете додати до валідованих даних додаткові поля, викличте метод `merge`:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

Якщо ви хочете отримати валідовані дані як [колекцію](/docs/{{version}}/collections), викличте метод `collect`:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## Робота з повідомленнями про помилки

Викликавши метод `errors` на екземплярі `Validator`, ви отримаєте екземпляр `Illuminate\Support\MessageBag`, що має низку зручних методів для роботи з повідомленнями про помилки. Змінна `$errors`, автоматично доступна всім представленням, теж є екземпляром класу `MessageBag`.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### Отримання першого повідомлення для поля

Щоб отримати перше повідомлення про помилку для певного поля, скористайтеся методом `first`:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### Отримання всіх повідомлень для поля

Якщо вам потрібен масив усіх повідомлень для певного поля, скористайтеся методом `get`:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

Якщо ви валідуєте поле форми, що є масивом, ви можете отримати всі повідомлення для кожного елемента масиву за допомогою символу `*`:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### Отримання всіх повідомлень для всіх полів

Щоб отримати масив усіх повідомлень для всіх полів, скористайтеся методом `all`:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### Визначення наявності повідомлень для поля

Метод `has` дозволяє визначити, чи існують повідомлення про помилки для певного поля:

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### Власні повідомлення у мовних файлах

Кожне вбудоване правило валідації Laravel має повідомлення про помилку, розташоване у файлі `lang/en/validation.php` вашого застосунку. Якщо ваш застосунок не має каталогу `lang`, ви можете створити його командою Artisan `lang:publish`.

У файлі `lang/en/validation.php` ви знайдете запис перекладу для кожного правила валідації. Ви вільні змінювати ці повідомлення відповідно до потреб свого застосунку.

Крім того, ви можете скопіювати цей файл до каталогу іншої мови, щоб перекласти повідомлення мовою вашого застосунку. Докладніше про локалізацію в Laravel читайте в повній [документації з локалізації](/docs/{{version}}/localization).

> [!WARNING]
> За замовчуванням каркас застосунку Laravel не містить каталогу `lang`. Якщо ви хочете налаштувати мовні файли Laravel, опублікуйте їх командою Artisan `lang:publish`.

<a name="custom-messages-for-specific-attributes"></a>
#### Власні повідомлення для конкретних атрибутів

Ви можете налаштувати повідомлення про помилки для вказаних комбінацій атрибута й правила у мовних файлах валідації вашого застосунку. Для цього додайте свої налаштування до масиву `custom` у файлі `lang/xx/validation.php`:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### Атрибути у мовних файлах

Багато вбудованих повідомлень про помилки Laravel містять заповнювач `:attribute`, який замінюється іменем поля чи атрибута, що валідується. Якщо ви хочете, щоб частину `:attribute` вашого повідомлення було замінено власним значенням, вкажіть власне ім'я атрибута в масиві `attributes` вашого файлу `lang/xx/validation.php`:

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> За замовчуванням каркас застосунку Laravel не містить каталогу `lang`. Якщо ви хочете налаштувати мовні файли Laravel, опублікуйте їх командою Artisan `lang:publish`.

<a name="specifying-values-in-language-files"></a>
### Значення у мовних файлах

Деякі вбудовані повідомлення про помилки валідації в Laravel містять заповнювач `:value`, який замінюється поточним значенням атрибута запиту. Однак подекуди вам може знадобитися, щоб частину `:value` вашого повідомлення було замінено зрозумілішим поданням значення. Наприклад, розгляньмо правило, яке вказує, що номер кредитної картки обов'язковий, якщо `payment_type` має значення `cc`:

```php
Validator::make($request->all(), [
    'credit_card_number' => ['required_if:payment_type,cc']
]);
```

Якщо це правило валідації не пройде, воно створить таке повідомлення про помилку:

```text
The credit card number field is required when payment type is cc.
```

Замість показувати `cc` як значення типу платежу, ви можете вказати зрозуміліше подання у своєму файлі `lang/xx/validation.php`, визначивши масив `values`:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> За замовчуванням каркас застосунку Laravel не містить каталогу `lang`. Якщо ви хочете налаштувати мовні файли Laravel, опублікуйте їх командою Artisan `lang:publish`.

Після визначення цього значення правило валідації створить таке повідомлення про помилку:

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## Доступні правила валідації

Нижче наведено список усіх доступних правил валідації та їхнє призначення:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

#### Booleans

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### Strings

<div class="collection-method-list" markdown="1">

[Active URL](#rule-active-url)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Different](#rule-different)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Hex Color](#rule-hex-color)
[In](#rule-in)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Min](#rule-min)
[Not In](#rule-not-in)
[Regular Expression](#rule-regex)
[Not Regular Expression](#rule-not-regex)
[Same](#rule-same)
[Size](#rule-size)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

#### Numbers

<div class="collection-method-list" markdown="1">

[Between](#rule-between)
[Decimal](#rule-decimal)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Integer](#rule-integer)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Multiple Of](#rule-multiple-of)
[Numeric](#rule-numeric)
[Same](#rule-same)
[Size](#rule-size)

</div>

#### Arrays

<div class="collection-method-list" markdown="1">

[Array](#rule-array)
[Between](#rule-between)
[Contains](#rule-contains)
[Doesnt Contain](#rule-doesnt-contain)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)

</div>

#### Dates

<div class="collection-method-list" markdown="1">

[After](#rule-after)
[After Or Equal](#rule-after-or-equal)
[Before](#rule-before)
[Before Or Equal](#rule-before-or-equal)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Timezone](#rule-timezone)

</div>

#### Files

<div class="collection-method-list" markdown="1">

[Between](#rule-between)
[Dimensions](#rule-dimensions)
[Encoding](#rule-encoding)
[Extensions](#rule-extensions)
[File](#rule-file)
[Image](#rule-image)
[Max](#rule-max)
[Min](#rule-min)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Size](#rule-size)

</div>

#### Database

<div class="collection-method-list" markdown="1">

[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

#### Utilities

<div class="collection-method-list" markdown="1">

[Any Of](#rule-anyof)
[Bail](#rule-bail)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Filled](#rule-filled)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Nullable](#rule-nullable)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited If Accepted](#rule-prohibited-if-accepted)
[Prohibited If Declined](#rule-prohibited-if-declined)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required If Declined](#rule-required-if-declined)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Sometimes](#validating-when-present)

</div>

<a name="rule-accepted"></a>
#### accepted

Поле, що валідується, має бути `"yes"`, `"on"`, `1`, `"1"`, `true` чи `"true"`. Це корисно для перевірки прийняття «Умов використання» та подібних полів.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

Поле, що валідується, має бути `"yes"`, `"on"`, `1`, `"1"`, `true` чи `"true"`, якщо інше поле дорівнює вказаному значенню. Це корисно для перевірки прийняття «Умов використання» та подібних полів.

<a name="rule-active-url"></a>
#### active_url

Поле, що валідується, має мати дійсний запис A чи AAAA згідно з PHP-функцією `dns_get_record`. Ім'я хоста з наданого URL витягується PHP-функцією `parse_url` перед передаванням до `dns_get_record`.

<a name="rule-after"></a>
#### after:_date_

Поле, що валідується, має бути значенням після вказаної дати. Дати передаються до PHP-функції `strtotime`, щоб перетворити їх на дійсний екземпляр `DateTime`:

```php
'start_date' => ['required', 'date', 'after:tomorrow']
```

Замість передавати рядок дати для обчислення через `strtotime`, ви можете вказати інше поле для порівняння:

```php
'finish_date' => ['required', 'date', 'after:start_date']
```

Для зручності правила на основі дат можна будувати плинним конструктором `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

Методи `afterToday` і `todayOrAfter` дозволяють плинно виразити, що дата має бути після сьогодні або сьогодні чи пізніше відповідно:

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

Поле, що валідується, має бути значенням після вказаної дати або дорівнювати їй. Докладніше дивіться правило [after](#rule-after).

Для зручності правила на основі дат можна будувати плинним конструктором `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

Правило валідації `Rule::anyOf` дозволяє вказати, що поле має задовольняти будь-який із наведених наборів правил. Наприклад, наступне правило перевірить, що поле `username` є або адресою електронної пошти, або буквено-цифровим рядком (із дефісами) щонайменше з 6 символів:

```php
use Illuminate\Validation\Rule;

'username' => [
    'required',
    Rule::anyOf([
        ['string', 'email'],
        ['string', 'alpha_dash', 'min:6'],
    ]),
],
```

<a name="rule-alpha"></a>
#### alpha

Поле, що валідується, має складатися виключно з літер Unicode, що входять до [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) та [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=).

Щоб обмежити це правило символами діапазону ASCII (`a-z` та `A-Z`), передайте правилу опцію `ascii`:

```php
'username' => ['alpha:ascii'],
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

Поле, що валідується, має складатися виключно з буквено-цифрових символів Unicode, що входять до [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), а також ASCII-дефісів (`-`) та ASCII-підкреслень (`_`).

Щоб обмежити це правило символами діапазону ASCII (`a-z`, `A-Z` та `0-9`), передайте правилу опцію `ascii`:

```php
'username' => ['alpha_dash:ascii'],
```

<a name="rule-alpha-num"></a>
#### alpha_num

Поле, що валідується, має складатися виключно з буквено-цифрових символів Unicode, що входять до [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) та [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=).

Щоб обмежити це правило символами діапазону ASCII (`a-z`, `A-Z` та `0-9`), передайте правилу опцію `ascii`:

```php
'username' => ['alpha_num:ascii'],
```

<a name="rule-array"></a>
#### array

Поле, що валідується, має бути PHP-масивом (`array`).

Коли правилу `array` передано додаткові значення, кожен ключ вхідного масиву має бути присутнім у переданому списку значень. У прикладі нижче ключ `admin` у вхідному масиві недійсний, бо його немає в списку значень, переданих правилу `array`:

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```

Загалом вам слід завжди вказувати ключі масиву, які дозволено в ньому мати.

<a name="rule-ascii"></a>
#### ascii

Поле, що валідується, має складатися виключно із 7-бітних символів ASCII.

<a name="rule-bail"></a>
#### bail

Припинити виконання правил валідації для поля після першої невдалої перевірки.

Тоді як правило `bail` припиняє валідацію лише конкретного поля, метод `stopOnFirstFailure` повідомить валідатор, що йому слід припинити валідацію всіх атрибутів після першої ж невдачі:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

Поле, що валідується, має бути значенням перед указаною датою. Дати передаються до PHP-функції `strtotime`, щоб перетворити їх на дійсний екземпляр `DateTime`. Крім того, як і в правилі [after](#rule-after), як значення `date` можна передати ім'я іншого поля.

Для зручності правила на основі дат можна також будувати плинним конструктором `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

Методи `beforeToday` і `todayOrBefore` дозволяють плинно виразити, що дата має бути до сьогодні або сьогодні чи раніше відповідно:

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

Поле, що валідується, має бути значенням перед указаною датою або дорівнювати їй. Дати передаються до PHP-функції `strtotime`, щоб перетворити їх на дійсний екземпляр `DateTime`. Крім того, як і в правилі [after](#rule-after), як значення `date` можна передати ім'я іншого поля.

Для зручності правила на основі дат можна також будувати плинним конструктором `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

Поле, що валідується, має мати розмір між указаними _min_ і _max_ (включно). Рядки, числа, масиви та файли оцінюються так само, як у правилі [size](#rule-size).

<a name="rule-boolean"></a>
#### boolean

Поле, що валідується, має піддаватися приведенню до булевого типу. Прийнятні значення: `true`, `false`, `1`, `0`, `"1"` та `"0"`.

Ви можете скористатися параметром `strict`, щоб вважати поле дійсним лише тоді, коли його значення є `true` чи `false`:

```php
'foo' => ['boolean:strict']
```

<a name="rule-confirmed"></a>
#### confirmed

Поле, що валідується, має мати відповідне поле `{field}_confirmation`. Наприклад, якщо валідується поле `password`, у вхідних даних має бути присутнє поле `password_confirmation`.

Ви також можете передати власне ім'я поля підтвердження. Наприклад, `confirmed:repeat_username` очікуватиме, що поле `repeat_username` збігатиметься з полем, що валідується.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

Поле, що валідується, має бути масивом, який містить усі передані значення. Оскільки це правило часто потребує `implode` масиву, для плинної побудови правила можна скористатися методом `Rule::contains`:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::contains(['admin', 'editor']),
    ],
]);
```

<a name="rule-doesnt-contain"></a>
#### doesnt_contain:_foo_,_bar_,...

Поле, що валідується, має бути масивом, який не містить жодного з переданих значень. Оскільки це правило часто потребує `implode` масиву, для плинної побудови правила можна скористатися методом `Rule::doesntContain`:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::doesntContain(['admin', 'editor']),
    ],
]);
```

<a name="rule-current-password"></a>
#### current_password

Поле, що валідується, має збігатися з паролем автентифікованого користувача. Ви можете вказати [гард автентифікації](/docs/{{version}}/authentication) першим параметром правила:

```php
'password' => ['current_password:api']
```

<a name="rule-date"></a>
#### date

Поле, що валідується, має бути дійсною невідносною датою згідно з PHP-функцією `strtotime`.

<a name="rule-date-equals"></a>
#### date_equals:_date_

Поле, що валідується, має дорівнювати вказаній даті. Дати передаються до PHP-функції `strtotime`, щоб перетворити їх на дійсний екземпляр `DateTime`.

<a name="rule-date-format"></a>
#### date_format:_format_,...

Поле, що валідується, має відповідати одному з указаних _форматів_. Валідуючи поле, слід використовувати **або** `date`, **або** `date_format`, але не обидва. Це правило підтримує всі формати, які підтримує PHP-клас [DateTime](https://www.php.net/manual/en/class.datetime.php).

Для зручності правила на основі дат можна будувати плинним конструктором `date`:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

Поле, що валідується, має бути числовим і містити вказану кількість десяткових знаків:

```php
// Must have exactly two decimal places (9.99)...
'price' => ['decimal:2']

// Must have between 2 and 4 decimal places...
'price' => ['decimal:2,4']
```

<a name="rule-declined"></a>
#### declined

Поле, що валідується, має бути `"no"`, `"off"`, `0`, `"0"`, `false` чи `"false"`.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

Поле, що валідується, має бути `"no"`, `"off"`, `0`, `"0"`, `false` чи `"false"`, якщо інше поле дорівнює вказаному значенню.

<a name="rule-different"></a>
#### different:_field_

Поле, що валідується, має мати значення, відмінне від _field_.

<a name="rule-digits"></a>
#### digits:_value_

Ціле число, що валідується, має мати точну довжину _value_.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

Ціле число, що валідується, має мати довжину між указаними _min_ і _max_.

<a name="rule-dimensions"></a>
#### dimensions

Файл, що валідується, має бути зображенням, яке відповідає обмеженням розмірів, указаним у параметрах правила:

```php
'avatar' => ['dimensions:min_width=100,min_height=200']
```

Доступні обмеження: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_, _min\_ratio_, _max\_ratio_.

Обмеження _ratio_ слід подавати як ширину, поділену на висоту. Це можна вказати або дробом на кшталт `3/2`, або числом із рухомою комою на кшталт `1.5`:

```php
'avatar' => ['dimensions:ratio=3/2']
```

Обмеження _min\_ratio_ та _max\_ratio_ дозволяють задати діапазон прийнятних співвідношень сторін:

```php
'avatar' => ['dimensions:min_ratio=1/2,max_ratio=3/2']
```

Оскільки це правило потребує кількох аргументів, часто зручніше скористатися методом `Rule::dimensions` для плинної побудови правила:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()
            ->maxWidth(1000)
            ->maxHeight(500)
            ->ratio(3 / 2),
    ],
]);
```

Ви також можете скористатися методами `minRatio`, `maxRatio` та `ratioBetween`, щоб плинно задати обмеження співвідношення:

```php
Rule::dimensions()->ratioBetween(min: 1 / 2, max: 3 / 2)
```

<a name="rule-distinct"></a>
#### distinct

Валідуючи масиви, поле, що валідується, не має містити повторюваних значень:

```php
'foo.*.id' => ['distinct']
```

За замовчуванням `distinct` використовує нестроге порівняння змінних. Щоб застосувати строге порівняння, додайте до визначення правила параметр `strict`:

```php
'foo.*.id' => ['distinct:strict']
```

Ви можете додати до аргументів правила `ignore_case`, щоб воно ігнорувало відмінності в регістрі:

```php
'foo.*.id' => ['distinct:ignore_case']
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

Поле, що валідується, не має починатися з жодного з переданих значень.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

Поле, що валідується, не має закінчуватися жодним із переданих значень.

<a name="rule-email"></a>
#### email

Поле, що валідується, має бути відформатоване як адреса електронної пошти. Це правило використовує пакет [egulias/email-validator](https://github.com/egulias/EmailValidator). За замовчуванням застосовується валідатор `RFCValidation`, але ви можете застосувати й інші стилі валідації:

```php
'email' => ['email:rfc,dns']
```

Наведений вище приклад застосує валідації `RFCValidation` та `DNSCheckValidation`. Ось повний список стилів валідації, які можна застосувати:

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - валідувати адресу згідно з [підтримуваними RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs).
- `strict`: `NoRFCWarningsValidation` - валідувати адресу згідно з [підтримуваними RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs), відхиляючи її за наявності попереджень (наприклад, крапка наприкінці чи кілька крапок поспіль).
- `dns`: `DNSCheckValidation` - переконатися, що домен адреси має дійсний MX-запис.
- `spoof`: `SpoofCheckValidation` - переконатися, що адреса не містить гомогліфів чи оманливих символів Unicode.
- `filter`: `FilterEmailValidation` - переконатися, що адреса дійсна згідно з PHP-функцією `filter_var`.
- `filter_unicode`: `FilterEmailValidation::unicode()` - переконатися, що адреса дійсна згідно з PHP-функцією `filter_var`, дозволяючи деякі символи Unicode.

</div>

Для зручності правила валідації електронної пошти можна будувати плинним конструктором:

```php
use Illuminate\Validation\Rule;

$request->validate([
    'email' => [
        'required',
        Rule::email()
            ->rfcCompliant(strict: false)
            ->validateMxRecord()
            ->preventSpoofing()
    ],
]);
```

> [!WARNING]
> Валідатори `dns` і `spoof` потребують PHP-розширення `intl`.

<a name="rule-encoding"></a>
#### encoding:*encoding_type*

Поле, що валідується, має відповідати вказаному кодуванню символів. Це правило використовує PHP-функцію `mb_check_encoding`, щоб перевірити кодування переданого файлу чи рядка. Для зручності правило `encoding` можна будувати плинним конструктором файлових правил Laravel:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['csv'])
            ->encoding('utf-8'),
    ],
]);
```

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

Поле, що валідується, має закінчуватися одним із переданих значень.

<a name="rule-enum"></a>
#### enum

Правило `Enum` - це правило на основі класу, що перевіряє, чи містить поле дійсне значення enum. Правило `Enum` приймає ім'я enum як єдиний аргумент конструктора. Валідуючи примітивні значення, правилу `Enum` слід передавати enum на основі значень (backed enum):

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

Методи `only` та `except` правила `Enum` дозволяють обмежити, які випадки enum вважати дійсними:

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

Метод `when` дозволяє умовно змінювати правило `Enum`:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

Rule::enum(ServerStatus::class)
    ->when(
        Auth::user()->isAdmin(),
        fn ($rule) => $rule->only(...),
        fn ($rule) => $rule->only(...),
    );
```

<a name="rule-exclude"></a>
#### exclude

Поле, що валідується, буде виключено з даних запиту, які повертають методи `validate` та `validated`.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

Поле, що валідується, буде виключено з даних запиту, які повертають методи `validate` та `validated`, якщо поле _anotherfield_ дорівнює _value_.

Якщо потрібна складна умовна логіка виключення, скористайтеся методом `Rule::excludeIf`. Він приймає булеве значення або замикання. Замикання має повертати `true` чи `false`, вказуючи, чи слід виключити поле:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_

Поле, що валідується, буде виключено з даних запиту, які повертають методи `validate` та `validated`, якщо тільки поле _anotherfield_ не дорівнює _value_. Якщо _value_ є `null` (`exclude_unless:name,null`), поле буде виключено, якщо тільки поле для порівняння не є `null` або відсутнє в даних запиту.

Якщо потрібна складна умовна логіка виключення, скористайтеся методом `Rule::excludeUnless`. Він приймає булеве значення або замикання. Замикання має повертати `true` чи `false`, вказуючи, чи не слід виключати поле:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

Поле, що валідується, буде виключено з даних запиту, які повертають методи `validate` та `validated`, якщо поле _anotherfield_ присутнє.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

Поле, що валідується, буде виключено з даних запиту, які повертають методи `validate` та `validated`, якщо поле _anotherfield_ відсутнє.

<a name="rule-exists"></a>
#### exists:_table_,_column_

Поле, що валідується, має існувати у вказаній таблиці бази даних.

<a name="basic-usage-of-exists-rule"></a>
#### Базове використання правила Exists

```php
'state' => ['exists:states']
```

Якщо опцію `column` не вказано, буде використано ім'я поля. Тож у цьому випадку правило перевірить, що таблиця `states` містить запис зі значенням колонки `state`, що збігається зі значенням атрибута `state` у запиті.

<a name="specifying-a-custom-column-name"></a>
#### Указання власного імені колонки

Ви можете явно вказати ім'я колонки бази даних, яку має використовувати правило валідації, розмістивши його після імені таблиці:

```php
'state' => ['exists:states,abbreviation']
```

Подекуди вам може знадобитися вказати конкретне підключення до бази даних для запиту `exists`. Це робиться додаванням імені підключення перед іменем таблиці:

```php
'email' => ['exists:connection.staff,email']
```

Замість указувати ім'я таблиці напряму, ви можете вказати модель Eloquent, за якою буде визначено ім'я таблиці:

```php
'user_id' => ['exists:App\Models\User,id']
```

Якщо ви хочете налаштувати запит, який виконує правило валідації, скористайтеся класом `Rule` для плинного визначення правила.

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            $query->where('account_id', 1);
        }),
    ],
]);
```

Ви можете явно вказати ім'я колонки для правила `exists`, згенерованого методом `Rule::exists`, передавши його другим аргументом методу `exists`:

```php
'state' => [Rule::exists('states', 'abbreviation')],
```

Іноді ви можете захотіти перевірити, чи існує в базі даних масив значень. Це робиться додаванням до поля обох правил - `exists` та [array](#rule-array):

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

Коли полю призначено обидва ці правила, Laravel автоматично побудує єдиний запит, щоб визначити, чи всі передані значення існують у вказаній таблиці.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

Файл, що валідується, має мати призначене користувачем розширення, що відповідає одному з перелічених:

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> Ніколи не покладайтеся на перевірку файлу лише за призначеним користувачем розширенням. Це правило зазвичай слід використовувати в поєднанні з правилами [mimes](#rule-mimes) чи [mimetypes](#rule-mimetypes).

<a name="rule-file"></a>
#### file

Поле, що валідується, має бути успішно завантаженим файлом.

<a name="rule-filled"></a>
#### filled

Поле, що валідується, не має бути порожнім, коли воно присутнє.

<a name="rule-gt"></a>
#### gt:_field_

Поле, що валідується, має бути більшим за вказане _field_ чи _value_. Обидва поля мають бути одного типу. Рядки, числа, масиви та файли оцінюються за тими самими домовленостями, що й у правилі [size](#rule-size).

<a name="rule-gte"></a>
#### gte:_field_

Поле, що валідується, має бути більшим за вказане _field_ чи _value_ або дорівнювати йому. Обидва поля мають бути одного типу. Рядки, числа, масиви та файли оцінюються за тими самими домовленостями, що й у правилі [size](#rule-size).

<a name="rule-hex-color"></a>
#### hex_color

Поле, що валідується, має містити дійсне значення кольору у [шістнадцятковому](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) форматі.

<a name="rule-image"></a>
#### image

Файл, що валідується, має бути зображенням (jpg, jpeg, png, bmp, gif чи webp).

> [!WARNING]
> За замовчуванням правило `image` не дозволяє файли SVG через можливість XSS-вразливостей. Якщо вам потрібно дозволити SVG, передайте правилу `image` директиву `allow_svg` (`image:allow_svg`).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

Поле, що валідується, має входити до переданого списку значень. Оскільки це правило часто потребує `implode` масиву, для плинної побудови правила можна скористатися методом `Rule::in`:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

Коли правило `in` поєднано з правилом `array`, кожне значення вхідного масиву має бути присутнім у списку значень, переданих правилу `in`. У прикладі нижче код аеропорту `LAS` у вхідному масиві недійсний, бо його немає в переданому списку:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

Поле, що валідується, має існувати серед значень _anotherfield_.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

Поле, що валідується, має бути масивом, який містить принаймні одне з переданих _значень_ як ключ:

```php
'config' => ['array', 'in_array_keys:timezone']
```

<a name="rule-integer"></a>
#### integer

Поле, що валідується, має бути цілим числом.

Ви можете скористатися параметром `strict`, щоб вважати поле дійсним лише тоді, коли його тип - `integer`. Рядки з цілими значеннями вважатимуться недійсними:

```php
'age' => ['integer:strict']
```

> [!WARNING]
> Це правило не перевіряє, що вхідні дані мають тип змінної «integer», а лише те, що вони мають тип, прийнятний для PHP-правила `FILTER_VALIDATE_INT`. Якщо вам потрібно перевірити, що вхідні дані є числом, використовуйте це правило в поєднанні з [правилом `numeric`](#rule-numeric).

<a name="rule-ip"></a>
#### ip

Поле, що валідується, має бути IP-адресою.

<a name="ipv4"></a>
#### ipv4

Поле, що валідується, має бути адресою IPv4.

<a name="ipv6"></a>
#### ipv6

Поле, що валідується, має бути адресою IPv6.

<a name="rule-json"></a>
#### json

Поле, що валідується, має бути дійсним рядком JSON.

<a name="rule-lt"></a>
#### lt:_field_

Поле, що валідується, має бути меншим за вказане _field_. Обидва поля мають бути одного типу. Рядки, числа, масиви та файли оцінюються за тими самими домовленостями, що й у правилі [size](#rule-size).

<a name="rule-lte"></a>
#### lte:_field_

Поле, що валідується, має бути меншим за вказане _field_ або дорівнювати йому. Обидва поля мають бути одного типу. Рядки, числа, масиви та файли оцінюються за тими самими домовленостями, що й у правилі [size](#rule-size).

<a name="rule-lowercase"></a>
#### lowercase

Поле, що валідується, має бути в нижньому регістрі.

<a name="rule-list"></a>
#### list

Поле, що валідується, має бути масивом-списком. Масив вважається списком, якщо його ключі є послідовними числами від 0 до `count($array) - 1`.

<a name="rule-mac"></a>
#### mac_address

Поле, що валідується, має бути MAC-адресою.

<a name="rule-max"></a>
#### max:_value_

Поле, що валідується, має бути меншим за максимальне _value_ або дорівнювати йому. Рядки, числа, масиви та файли оцінюються так само, як у правилі [size](#rule-size).

<a name="rule-max-digits"></a>
#### max_digits:_value_

Ціле число, що валідується, має мати максимальну довжину _value_.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

Файл, що валідується, має відповідати одному з указаних MIME-типів:

```php
'video' => ['mimetypes:video/avi,video/mpeg,video/quicktime'],

'media' => ['mimetypes:image/*,video/*'],
```

Щоб визначити MIME-тип завантаженого файлу, буде прочитано його вміст, і фреймворк спробує вгадати тип, який може відрізнятися від наданого клієнтом.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

Файл, що валідується, має мати MIME-тип, що відповідає одному з перелічених розширень:

```php
'photo' => ['mimes:jpg,bmp,png']
```

Хоча вам потрібно вказати лише розширення, це правило насправді перевіряє MIME-тип файлу, читаючи його вміст і вгадуючи тип. Повний перелік MIME-типів та відповідних їм розширень можна знайти тут:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME-типи та розширення

Це правило не перевіряє відповідність між MIME-типом і розширенням, яке користувач призначив файлу. Наприклад, правило `mimes:png` вважатиме файл із дійсним вмістом PNG дійсним зображенням PNG, навіть якщо файл названо `photo.txt`. Якщо ви хочете перевірити призначене користувачем розширення, скористайтеся правилом [extensions](#rule-extensions).

<a name="rule-min"></a>
#### min:_value_

Поле, що валідується, має мати мінімальне значення _value_. Рядки, числа, масиви та файли оцінюються так само, як у правилі [size](#rule-size).

<a name="rule-min-digits"></a>
#### min_digits:_value_

Ціле число, що валідується, має мати мінімальну довжину _value_.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

Поле, що валідується, має бути кратним _value_.

<a name="rule-missing"></a>
#### missing

Поле, що валідується, не має бути присутнім у вхідних даних.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

Поле, що валідується, не має бути присутнім, якщо поле _anotherfield_ дорівнює будь-якому _value_.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

Поле, що валідується, не має бути присутнім, якщо тільки поле _anotherfield_ не дорівнює будь-якому _value_.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

Поле, що валідується, не має бути присутнім, _лише якщо_ присутнє будь-яке з інших указаних полів.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

Поле, що валідується, не має бути присутнім, _лише якщо_ присутні всі інші вказані поля.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

Поле, що валідується, не має входити до переданого списку значень. Для плинної побудови правила можна скористатися методом `Rule::notIn`:

```php
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a name="rule-not-regex"></a>
#### not_regex:_pattern_

Поле, що валідується, не має збігатися з указаним регулярним виразом.

Внутрішньо це правило використовує PHP-функцію `preg_match`. Указаний шаблон має відповідати тому самому форматуванню, якого потребує `preg_match`, тобто містити й дійсні роздільники. Наприклад: `'email' => ['not_regex:/^.+$/i']`.

<a name="rule-nullable"></a>
#### nullable

Поле, що валідується, може бути `null`.

<a name="rule-numeric"></a>
#### numeric

Поле, що валідується, має бути [числовим](https://www.php.net/manual/en/function.is-numeric.php).

Ви можете скористатися параметром `strict`, щоб вважати поле дійсним лише тоді, коли його значення має тип integer чи float. Числові рядки вважатимуться недійсними:

```php
'amount' => ['numeric:strict']
```

<a name="rule-present"></a>
#### present

Поле, що валідується, має існувати у вхідних даних.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

Поле, що валідується, має бути присутнім, якщо поле _anotherfield_ дорівнює будь-якому _value_.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

Поле, що валідується, має бути присутнім, якщо тільки поле _anotherfield_ не дорівнює будь-якому _value_.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

Поле, що валідується, має бути присутнім, _лише якщо_ присутнє будь-яке з інших указаних полів.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

Поле, що валідується, має бути присутнім, _лише якщо_ присутні всі інші вказані поля.

<a name="rule-prohibited"></a>
#### prohibited

Поле, що валідується, має бути відсутнім або порожнім. Поле є «порожнім», якщо воно відповідає одному з таких критеріїв:

<div class="content-list" markdown="1">

- Значення дорівнює `null`.
- Значення є порожнім рядком.
- Значення є порожнім масивом або порожнім об'єктом `Countable`.
- Значення є завантаженим файлом із порожнім шляхом.

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

Поле, що валідується, має бути відсутнім або порожнім, якщо поле _anotherfield_ дорівнює будь-якому _value_. Поле є «порожнім», якщо воно відповідає одному з таких критеріїв:

<div class="content-list" markdown="1">

- Значення дорівнює `null`.
- Значення є порожнім рядком.
- Значення є порожнім масивом або порожнім об'єктом `Countable`.
- Значення є завантаженим файлом із порожнім шляхом.

</div>

Якщо потрібна складна умовна логіка заборони, скористайтеся методом `Rule::prohibitedIf`. Він приймає булеве значення або замикання. Замикання має повертати `true` чи `false`, вказуючи, чи слід заборонити поле:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf(fn () => $request->user()->is_admin)],
]);
```
<a name="rule-prohibited-if-accepted"></a>
#### prohibited_if_accepted:_anotherfield_,...

Поле, що валідується, має бути відсутнім або порожнім, якщо поле _anotherfield_ дорівнює `"yes"`, `"on"`, `1`, `"1"`, `true` чи `"true"`.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

Поле, що валідується, має бути відсутнім або порожнім, якщо поле _anotherfield_ дорівнює `"no"`, `"off"`, `0`, `"0"`, `false` чи `"false"`.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

Поле, що валідується, має бути відсутнім або порожнім, якщо тільки поле _anotherfield_ не дорівнює будь-якому _value_. Поле є «порожнім», якщо воно відповідає одному з таких критеріїв:

<div class="content-list" markdown="1">

- Значення дорівнює `null`.
- Значення є порожнім рядком.
- Значення є порожнім масивом або порожнім об'єктом `Countable`.
- Значення є завантаженим файлом із порожнім шляхом.

</div>

Якщо потрібна складна умовна логіка заборони, скористайтеся методом `Rule::prohibitedUnless`. Він приймає булеве значення або замикання. Замикання має повертати `true` чи `false`, вказуючи, чи не слід забороняти поле:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

Якщо поле, що валідується, не є відсутнім чи порожнім, усі поля в _anotherfield_ мають бути відсутніми або порожніми. Поле є «порожнім», якщо воно відповідає одному з таких критеріїв:

<div class="content-list" markdown="1">

- Значення дорівнює `null`.
- Значення є порожнім рядком.
- Значення є порожнім масивом або порожнім об'єктом `Countable`.
- Значення є завантаженим файлом із порожнім шляхом.

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

Поле, що валідується, має збігатися з указаним регулярним виразом.

Внутрішньо це правило використовує PHP-функцію `preg_match`. Указаний шаблон має відповідати тому самому форматуванню, якого потребує `preg_match`, тобто містити й дійсні роздільники. Наприклад: `'email' => ['regex:/^.+@.+$/i']`.

<a name="rule-required"></a>
#### required

Поле, що валідується, має бути присутнім у вхідних даних і не бути порожнім. Поле є «порожнім», якщо воно відповідає одному з таких критеріїв:

<div class="content-list" markdown="1">

- Значення дорівнює `null`.
- Значення є порожнім рядком.
- Значення є порожнім масивом або порожнім об'єктом `Countable`.
- Значення є завантаженим файлом без шляху.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

Поле, що валідується, має бути присутнім і не порожнім, якщо поле _anotherfield_ дорівнює будь-якому _value_.

Якщо ви хочете побудувати складнішу умову для правила `required_if`, скористайтеся методом `Rule::requiredIf`. Він приймає булеве значення або замикання. Замикання має повертати `true` чи `false`, вказуючи, чи є поле обов'язковим:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-required-if-accepted"></a>
#### required_if_accepted:_anotherfield_,...

Поле, що валідується, має бути присутнім і не порожнім, якщо поле _anotherfield_ дорівнює `"yes"`, `"on"`, `1`, `"1"`, `true` чи `"true"`.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

Поле, що валідується, має бути присутнім і не порожнім, якщо поле _anotherfield_ дорівнює `"no"`, `"off"`, `0`, `"0"`, `false` чи `"false"`.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

Поле, що валідується, має бути присутнім і не порожнім, якщо тільки поле _anotherfield_ не дорівнює будь-якому _value_. Це також означає, що _anotherfield_ має бути присутнім у даних запиту, якщо тільки _value_ не є `null`. Якщо _value_ є `null` (`required_unless:name,null`), поле буде обов'язковим, якщо тільки поле для порівняння не є `null` або відсутнє в даних запиту.

Якщо ви хочете побудувати складнішу умову для правила `required_unless`, скористайтеся методом `Rule::requiredUnless`. Він приймає булеве значення або замикання. Замикання має повертати `true` чи `false`, вказуючи, чи не є поле обов'язковим:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

Поле, що валідується, має бути присутнім і не порожнім, _лише якщо_ будь-яке з інших указаних полів присутнє й не порожнє.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

Поле, що валідується, має бути присутнім і не порожнім, _лише якщо_ всі інші вказані поля присутні й не порожні.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

Поле, що валідується, має бути присутнім і не порожнім, _лише коли_ будь-яке з інших указаних полів порожнє чи відсутнє.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

Поле, що валідується, має бути присутнім і не порожнім, _лише коли_ всі інші вказані поля порожні чи відсутні.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

Поле, що валідується, має бути масивом і містити принаймні вказані ключі.

<a name="rule-same"></a>
#### same:_field_

Указане _field_ має збігатися з полем, що валідується.

<a name="rule-size"></a>
#### size:_value_

Поле, що валідується, має мати розмір, що відповідає вказаному _value_. Для рядкових даних _value_ відповідає кількості символів. Для числових - вказаному цілому значенню (атрибут також має мати правило `numeric` чи `integer`). Для масиву _size_ відповідає результату `count`. Для файлів _size_ відповідає розміру файлу в кілобайтах. Погляньмо на приклади:

```php
// Validate that a string is exactly 12 characters long...
'title' => ['size:12'];

// Validate that a provided integer equals 10...
'seats' => ['integer', 'size:10'];

// Validate that an array has exactly 5 elements...
'tags' => ['array', 'size:5'];

// Validate that an uploaded file is exactly 512 kilobytes...
'image' => ['file', 'size:512'];
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

Поле, що валідується, має починатися з одного з переданих значень.

<a name="rule-string"></a>
#### string

Поле, що валідується, має бути рядком. Якщо ви хочете дозволити полю бути також `null`, призначте йому правило `nullable`.

Для зручності правила валідації рядків можна також будувати плинним конструктором `Rule::string()`:

```php
use Illuminate\Validation\Rule;

'title' => [
    'required',
    Rule::string()
        ->min(3)
        ->max(255)
        ->alphaDash(ascii: true),
],
```

Конструктор рядкових правил надає методи для поширених обмежень, зокрема `alpha`, `alphaDash`, `alphaNumeric`, `ascii`, `between`, `doesntEndWith`, `doesntStartWith`, `endsWith`, `exactly`, `lowercase`, `max`, `min`, `startsWith` та `uppercase`. Оскільки конструктор підтримує умови, ви можете також скористатися методами `when` та `unless`, щоб застосовувати обмеження умовно.

<a name="rule-timezone"></a>
#### timezone

Поле, що валідується, має бути дійсним ідентифікатором часового поясу згідно з методом `DateTimeZone::listIdentifiers`.

Аргументи, [які приймає метод `DateTimeZone::listIdentifiers`](https://www.php.net/manual/en/datetimezone.listidentifiers.php), можна також передати цьому правилу валідації:

```php
'timezone' => ['required', 'timezone:all'];

'timezone' => ['required', 'timezone:Africa'];

'timezone' => ['required', 'timezone:per_country,US'];
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

Поле, що валідується, не має існувати у вказаній таблиці бази даних.

**Указання власного імені таблиці чи колонки:**

Замість указувати ім'я таблиці напряму, ви можете вказати модель Eloquent, за якою буде визначено ім'я таблиці:

```php
'email' => ['unique:App\Models\User,email_address']
```

Опція `column` дозволяє вказати відповідну колонку бази даних для поля. Якщо її не вказано, буде використано ім'я поля, що валідується.

```php
'email' => ['unique:users,email_address']
```

**Указання власного підключення до бази даних**

Подекуди вам може знадобитися задати власне підключення для запитів, які робить валідатор. Це робиться додаванням імені підключення перед іменем таблиці:

```php
'email' => ['unique:connection.users,email_address']
```

**Змушення правила Unique ігнорувати певний ID:**

Іноді ви можете захотіти ігнорувати певний ідентифікатор під час перевірки унікальності. Наприклад, розгляньмо екран «оновлення профілю», що містить ім'я користувача, адресу електронної пошти та місцезнаходження. Ви, імовірно, захочете перевірити унікальність адреси. Однак якщо користувач змінює лише поле імені, а не адреси, ви не хочете, щоб виникала помилка валідації, адже користувач уже є власником цієї адреси.

Щоб вказати валідатору ігнорувати ідентифікатор користувача, скористаємося класом `Rule` для плинного визначення правила.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```

> [!WARNING]
> Ніколи не передавайте методу `ignore` вхідні дані запиту, які контролює користувач. Натомість передавайте лише згенерований системою унікальний ідентифікатор - як-от автоінкрементний ID чи UUID з екземпляра моделі Eloquent. Інакше ваш застосунок стане вразливим до SQL-ін'єкцій.

Замість передавати методу `ignore` значення ключа моделі, ви можете передати весь екземпляр моделі. Laravel автоматично витягне з неї ключ:

```php
Rule::unique('users')->ignore($user)
```

Якщо ваша таблиця використовує ім'я колонки первинного ключа, відмінне від `id`, ви можете вказати його під час виклику методу `ignore`:

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

За замовчуванням правило `unique` перевіряє унікальність колонки, ім'я якої збігається з іменем атрибута, що валідується. Утім, ви можете передати інше ім'я колонки другим аргументом методу `unique`:

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**Додавання додаткових умов Where:**

Ви можете вказати додаткові умови запиту, налаштувавши його методом `where`. Наприклад, додаймо умову, що обмежує запит записами зі значенням колонки `account_id`, рівним `1`:

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Ігнорування м'яко видалених записів під час перевірки унікальності:**

За замовчуванням правило `unique` враховує м'яко видалені записи, визначаючи унікальність. Щоб виключити їх із перевірки, викличте метод `withoutTrashed`:

```php
Rule::unique('users')->withoutTrashed();
```

Якщо ваша модель використовує для м'яко видалених записів колонку з іменем, відмінним від `deleted_at`, вкажіть її під час виклику `withoutTrashed`:

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

Поле, що валідується, має бути у верхньому регістрі.

<a name="rule-url"></a>
#### url

Поле, що валідується, має бути дійсним URL.

Якщо ви хочете вказати протоколи URL, які слід вважати дійсними, передайте їх як параметри правила валідації:

```php
'url' => ['url:http,https'],

'game' => ['url:minecraft,steam'],
```

<a name="rule-ulid"></a>
#### ulid

Поле, що валідується, має бути дійсним [універсально унікальним лексикографічно сортованим ідентифікатором](https://github.com/ulid/spec) (ULID).

<a name="rule-uuid"></a>
#### uuid

Поле, що валідується, має бути дійсним універсально унікальним ідентифікатором (UUID) за RFC 9562 (версії 1, 3, 4, 5, 6, 7 чи 8).

Ви також можете перевірити, що переданий UUID відповідає специфікації UUID за версією:

```php
'uuid' => ['uuid:4']
```

<a name="conditionally-adding-rules"></a>
## Умовне додавання правил

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### Пропуск валідації, коли поля мають певні значення

Подекуди ви можете захотіти не валідувати певне поле, якщо інше поле має певне значення. Це робиться правилом `exclude_if`. У цьому прикладі поля `appointment_date` та `doctor_name` не валідуватимуться, якщо поле `has_appointment` має значення `false`:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_if:has_appointment,false', 'required', 'date'],
    'doctor_name' => ['exclude_if:has_appointment,false', 'required', 'string'],
]);
```

Як альтернативу ви можете скористатися правилом `exclude_unless`, щоб не валідувати поле, якщо тільки інше поле не має певного значення:

```php
$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_unless:has_appointment,true', 'required', 'date'],
    'doctor_name' => ['exclude_unless:has_appointment,true', 'required', 'string'],
]);
```

<a name="validating-when-present"></a>
#### Валідація за наявності

У деяких ситуаціях ви можете захотіти виконувати перевірки для поля **лише** тоді, коли воно присутнє у даних, що валідуються. Щоб швидко цього досягти, додайте до списку правило `sometimes`:

```php
$validator = Validator::make($data, [
    'email' => ['sometimes', 'required', 'email'],
]);
```

У прикладі вище поле `email` валідуватиметься лише тоді, коли воно присутнє в масиві `$data`.

> [!NOTE]
> Якщо ви намагаєтеся валідувати поле, яке має бути присутнім завжди, але може бути порожнім, перегляньте [зауваження про необов'язкові поля](#a-note-on-optional-fields).

<a name="complex-conditional-validation"></a>
#### Складна умовна валідація

Іноді ви можете захотіти додавати правила валідації на основі складнішої умовної логіки. Наприклад, ви можете зробити поле обов'язковим лише тоді, коли інше поле має значення більше за 100. Або вам можуть знадобитися два поля з певним значенням лише тоді, коли присутнє інше поле. Додавати такі правила не обов'язково болісно. Спершу створіть екземпляр `Validator` зі _статичними правилами_, які ніколи не змінюються:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => ['required', 'email'],
    'games' => ['required', 'integer', 'min:0'],
]);
```

Припустімо, наш веб-застосунок призначений для колекціонерів ігор. Якщо колекціонер реєструється в нашому застосунку і має понад 100 ігор, ми хочемо, щоб він пояснив, чому їх так багато. Наприклад, можливо, він тримає магазин перепродажу ігор, а може, просто любить їх колекціонувати. Щоб додати цю вимогу умовно, ми можемо скористатися методом `sometimes` екземпляра `Validator`.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', ['required', 'max:500'], function (Fluent $input) {
    return $input->games >= 100;
});
```

Перший аргумент, переданий методу `sometimes`, - ім'я поля, яке ми валідуємо умовно. Другий - список правил, які хочемо додати. Якщо замикання, передане третім аргументом, повертає `true`, правила буде додано. Цей метод дозволяє легко будувати складні умовні перевірки. Ви можете навіть додавати умовні перевірки одразу для кількох полів:

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> Параметр `$input`, переданий вашому замиканню, буде екземпляром `Illuminate\Support\Fluent` і дозволить звертатися до ваших вхідних даних і файлів, що валідуються.

<a name="complex-conditional-array-validation"></a>
#### Складна умовна валідація масивів

Іноді ви можете захотіти валідувати поле на основі іншого поля в тому самому вкладеному масиві, індексу якого не знаєте. У таких ситуаціях ви можете дозволити своєму замиканню приймати другий аргумент - поточний елемент масиву, що валідується:

```php
$input = [
    'channels' => [
        [
            'type' => 'email',
            'address' => 'abigail@example.com',
        ],
        [
            'type' => 'url',
            'address' => 'https://example.com',
        ],
    ],
];

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

Як і параметр `$input`, параметр `$item` є екземпляром `Illuminate\Support\Fluent`, коли дані атрибута є масивом; інакше це рядок.

<a name="validating-arrays"></a>
## Валідація масивів

Як зазначено в [документації правила array](#rule-array), правило `array` приймає список дозволених ключів масиву. Якщо в масиві присутні будь-які додаткові ключі, валідація не пройде:

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```

Загалом вам слід завжди вказувати ключі масиву, які дозволено в ньому мати. Інакше методи `validate` та `validated` валідатора повернуть усі валідовані дані, зокрема масив і всі його ключі, навіть якщо ці ключі не валідувалися іншими правилами.

<a name="validating-nested-array-input"></a>
### Валідація вкладених масивів

Валідація вкладених полів форми на основі масивів не обов'язково болісна. Ви можете скористатися «крапковою нотацією», щоб валідувати атрибути всередині масиву. Наприклад, якщо вхідний HTTP-запит містить поле `photos[profile]`, ви можете валідувати його так:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => ['required', 'image'],
]);
```

Ви також можете валідувати кожен елемент масиву. Наприклад, щоб перевірити унікальність кожної адреси електронної пошти в масиві, зробіть так:

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => ['email', 'unique:users'],
    'users.*.first_name' => ['required_with:users.*.last_name'],
]);
```

Так само ви можете використовувати символ `*`, указуючи [власні повідомлення валідації у мовних файлах](#custom-messages-for-specific-attributes), що дозволяє легко застосувати одне повідомлення до полів-масивів:

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### Доступ до даних вкладеного масиву

Іноді вам може знадобитися звернутися до значення певного елемента вкладеного масиву, призначаючи атрибуту правила валідації. Це робиться методом `Rule::forEach`. Метод `forEach` приймає замикання, яке буде викликано для кожної ітерації атрибута-масиву й отримає значення атрибута та його явне повне ім'я. Замикання має повертати масив правил для цього елемента:

```php
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="error-message-indexes-and-positions"></a>
### Індекси та позиції в повідомленнях про помилки

Валідуючи масиви, ви можете захотіти послатися в повідомленні про помилку на індекс чи позицію конкретного елемента, який не пройшов валідацію. Для цього включіть у своє [власне повідомлення](#manual-customizing-the-error-messages) заповнювачі `:index` (починається з `0`), `:position` (починається з `1`) чи `:ordinal-position` (починається з `1st`):

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'photos' => [
        [
            'name' => 'BeachVacation.jpg',
            'description' => 'A photo of my beach vacation!',
        ],
        [
            'name' => 'GrandCanyon.jpg',
            'description' => '',
        ],
    ],
];

Validator::validate($input, [
    'photos.*.description' => ['required'],
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

З наведеним вище прикладом валідація не пройде, і користувач побачить помилку _«Please describe photo #2.»_

За потреби ви можете посилатися на глибше вкладені індекси та позиції через `second-index`, `second-position`, `third-index`, `third-position` тощо.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## Валідація файлів

Laravel надає різноманітні правила валідації для завантажених файлів - як-от `mimes`, `image`, `min` і `max`. Хоча ви вільні вказувати ці правила окремо, Laravel також пропонує плинний конструктор правил валідації файлів, який може здатися вам зручним:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)
            ->max(12 * 1024),
    ],
]);
```

<a name="validating-files-file-types"></a>
#### Валідація типів файлів

Хоча під час виклику методу `types` вам потрібно вказати лише розширення, цей метод насправді перевіряє MIME-тип файлу, читаючи його вміст і вгадуючи тип. Повний перелік MIME-типів та відповідних їм розширень можна знайти тут:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### Валідація розмірів файлів

Для зручності мінімальний і максимальний розміри файлу можна вказати рядком із суфіксом одиниць. Підтримуються суфікси `kb`, `mb`, `gb` і `tb`:

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### Валідація файлів зображень

Якщо ваш застосунок приймає зображення, завантажені користувачами, ви можете скористатися конструктором `image` правила `File`, щоб переконатися, що файл є зображенням (jpg, jpeg, png, bmp, gif чи webp).

Крім того, правило `dimensions` дозволяє обмежити розміри зображення:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image()
            ->min(1024)
            ->max(12 * 1024)
            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),
    ],
]);
```

> [!NOTE]
> Докладніше про валідацію розмірів зображень читайте в [документації правила dimensions](#rule-dimensions).

> [!WARNING]
> За замовчуванням правило `image` не дозволяє файли SVG через можливість XSS-вразливостей. Якщо вам потрібно дозволити SVG, передайте правилу `image` параметр `allowSvg: true`: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
#### Валідація розмірів зображень

Ви також можете валідувати розміри зображення. Наприклад, щоб перевірити, що завантажене зображення має ширину щонайменше 1000 пікселів і висоту 500 пікселів, скористайтеся правилом `dimensions`:

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

File::image()->dimensions(
    Rule::dimensions()
        ->maxWidth(1000)
        ->maxHeight(500)
)
```

> [!NOTE]
> Докладніше про валідацію розмірів зображень читайте в [документації правила dimensions](#rule-dimensions).

<a name="validating-passwords"></a>
## Валідація паролів

Щоб переконатися, що паролі мають достатній рівень складності, скористайтеся об'єктом правила `Password` від Laravel:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

Об'єкт правила `Password` дозволяє легко налаштувати вимоги до складності паролів у вашому застосунку - наприклад, вказати, що пароль має містити щонайменше одну літеру, цифру, символ чи літери різного регістру:

```php
// Require at least 8 characters...
Password::min(8)

// Require at least one letter...
Password::min(8)->letters()

// Require at least one uppercase and one lowercase letter...
Password::min(8)->mixedCase()

// Require at least one number...
Password::min(8)->numbers()

// Require at least one symbol...
Password::min(8)->symbols()
```

Крім того, ви можете переконатися, що пароль не було скомпрометовано в публічному витоку даних, за допомогою методу `uncompromised`:

```php
Password::min(8)->uncompromised()
```

Внутрішньо об'єкт правила `Password` використовує модель [k-анонімності](https://en.wikipedia.org/wiki/K-anonymity), щоб визначити, чи пароль витік, через сервіс [haveibeenpwned.com](https://haveibeenpwned.com), не жертвуючи приватністю чи безпекою користувача.

За замовчуванням, якщо пароль з'являється у витоку даних хоча б раз, він вважається скомпрометованим. Ви можете налаштувати цей поріг першим аргументом методу `uncompromised`:

```php
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

Звісно, ви можете об'єднати всі методи з наведених вище прикладів у ланцюжок:

```php
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

Ви можете перетворити об'єкт правила `Password` на рядок, придатний для HTML-атрибута `passwordrules`, методом `toPasswordRulesString`:

```blade
<input
    type="password"
    name="password"
    autocomplete="new-password"
    passwordrules="{{ Password::defaults()->toPasswordRulesString() }}"
/>
```

<a name="defining-default-password-rules"></a>
#### Визначення типових правил для паролів

Вам може бути зручно вказати типові правила валідації паролів в одному місці застосунку. Це легко зробити методом `Password::defaults`, який приймає замикання. Замикання, передане методу `defaults`, має повертати типову конфігурацію правила Password. Зазвичай `defaults` слід викликати в методі `boot` одного із сервіс-провайдерів вашого застосунку:

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
            ? $rule->mixedCase()->uncompromised()
            : $rule;
    });
}
```

Далі, коли ви захочете застосувати типові правила до конкретного пароля, викличте метод `defaults` без аргументів:

```php
'password' => ['required', Password::defaults()],
```

Подекуди ви можете захотіти приєднати до типових правил валідації паролів додаткові правила. Це робиться методом `rules`:

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## Власні правила валідації

<a name="using-rule-objects"></a>
### Використання об'єктів правил

Laravel надає різноманітні корисні правила валідації; утім, ви можете захотіти визначити власні. Один зі способів зареєструвати власні правила - використати об'єкти правил. Щоб згенерувати новий об'єкт правила, скористайтеся командою Artisan `make:rule`. Скористаймося цією командою, щоб згенерувати правило, яке перевіряє, що рядок записано у верхньому регістрі. Laravel помістить нове правило в каталог `app/Rules`. Якщо цього каталогу немає, Laravel створить його під час виконання команди:

```shell
php artisan make:rule Uppercase
```

Щойно правило створено, ми готові визначити його поведінку. Об'єкт правила містить єдиний метод `validate`. Він отримує ім'я атрибута, його значення та колбек, який слід викликати в разі невдачі з повідомленням про помилку:

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

Щойно правило визначено, ви можете приєднати його до валідатора, передавши екземпляр об'єкта правила разом з іншими правилами:

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### Переклад повідомлень валідації

Замість передавати замиканню `$fail` буквальне повідомлення про помилку, ви можете передати [ключ рядка перекладу](/docs/{{version}}/localization) і вказати Laravel перекласти повідомлення:

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

За потреби ви можете передати заміни заповнювачів і бажану мову першим і другим аргументами методу `translate`:

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### Доступ до додаткових даних

Якщо вашому класу власного правила потрібен доступ до всіх інших даних, що валідуються, він може реалізувати інтерфейс `Illuminate\Contracts\Validation\DataAwareRule`. Цей інтерфейс вимагає, щоб ваш клас визначив метод `setData`. Laravel автоматично викличе його (перед початком валідації) з усіма даними, що валідуються:

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * All of the data under validation.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array<string, mixed>  $data
     */
    public function setData(array $data): static
    {
        $this->data = $data;

        return $this;
    }
}
```

Або, якщо вашому правилу потрібен доступ до екземпляра валідатора, що виконує валідацію, реалізуйте інтерфейс `ValidatorAwareRule`:

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * The validator instance.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Set the current validator.
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a name="using-closures"></a>
### Використання замикань

Якщо функціональність власного правила потрібна вам у застосунку лише раз, ви можете скористатися замиканням замість об'єкта правила. Замикання отримує ім'я атрибута, його значення та колбек `$fail`, який слід викликати, якщо валідація не пройшла:

```php
use Illuminate\Support\Facades\Validator;
use Closure;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function (string $attribute, mixed $value, Closure $fail) {
            if ($value === 'foo') {
                $fail("The {$attribute} is invalid.");
            }
        },
    ],
]);
```

<a name="implicit-rules"></a>
### Неявні правила

За замовчуванням, коли атрибут, що валідується, відсутній або містить порожній рядок, звичайні правила валідації - зокрема власні - не виконуються. Наприклад, правило [unique](#rule-unique) не виконуватиметься для порожнього рядка:

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => ['unique:users,name']];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

Щоб власне правило виконувалося навіть тоді, коли атрибут порожній, правило має неявно вказувати, що атрибут обов'язковий. Щоб швидко згенерувати новий об'єкт неявного правила, скористайтеся командою Artisan `make:rule` з опцією `--implicit`:

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> «Неявне» правило лише _натякає_, що атрибут обов'язковий. Чи справді воно відхилятиме відсутній чи порожній атрибут - вирішувати вам.

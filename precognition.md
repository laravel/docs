---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Precognition

- [Вступ](#introduction)
- [Жива валідація](#live-validation)
    - [Через Vue](#using-vue)
    - [Через React](#using-react)
    - [Через Alpine і Blade](#using-alpine)
    - [Налаштування Axios](#configuring-axios)
- [Валідація масивів](#validating-arrays)
- [Налаштування правил валідації](#customizing-validation-rules)
- [Обробка завантаження файлів](#handling-file-uploads)
- [Керування побічними ефектами](#managing-side-effects)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

Laravel Precognition дозволяє передбачити результат майбутнього HTTP-запиту. Одне з головних застосувань Precognition - «жива» валідація у вашому фронтенді на JavaScript без дублювання правил валідації з бекенду застосунку.

Коли Laravel отримує «прекогнітивний запит», він виконає все `middleware` маршруту й розв'яже залежності його контролера, зокрема провалідує [запити форм](/docs/{{version}}/validation#form-request-validation), - але не виконуватиме сам метод контролера.

> [!NOTE]
> Починаючи з Inertia 2.3, підтримка Precognition вбудована. Докладніше читайте в [документації Inertia про форми](https://inertiajs.com/forms). Раніші версії Inertia потребують Precognition 0.x.

<a name="live-validation"></a>
## Жива валідація

<a name="using-vue"></a>
### Через Vue

За допомогою Laravel Precognition ви можете дати користувачам живу валідацію, не дублюючи правила валідації у своєму фронтенді на Vue. Щоб показати, як це працює, побудуймо форму створення нових користувачів у нашому застосунку.

Спершу, щоб увімкнути Precognition для маршруту, додайте до його визначення `middleware` `HandlePrecognitiveRequests`. Вам також слід створити [запит форми](/docs/{{version}}/validation#form-request-validation), який міститиме правила валідації маршруту:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

Далі встановіть фронтенд-хелпери Laravel Precognition для Vue через NPM:

```shell
npm install laravel-precognition-vue
```

Коли пакет Laravel Precognition встановлено, ви можете створити об'єкт форми функцією `useForm` із Precognition, передавши HTTP-метод (`post`), цільовий URL (`/users`) і початкові дані форми.

Далі, щоб увімкнути живу валідацію, викликайте метод форми `validate` на події `change` кожного поля, передаючи ім'я поля:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

Тепер, поки користувач заповнює форму, Precognition даватиме результати живої валідації на основі правил із запиту форми маршруту. Коли поля форми змінюються, до вашого застосунку Laravel надсилатиметься відкладений (debounced) «прекогнітивний» запит валідації. Ви можете налаштувати час відкладання, викликавши функцію форми `setValidationTimeout`:

```js
form.setValidationTimeout(3000);
```

Доки запит валідації в дорозі, властивість форми `validating` дорівнюватиме `true`:

```html
<div v-if="form.validating">
    Validating...
</div>
```

Будь-які помилки валідації, повернені під час запиту валідації чи надсилання форми, автоматично заповнять об'єкт форми `errors`:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

Визначити, чи має форма помилки, можна через властивість форми `hasErrors`:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

Ви також можете визначити, чи пройшло поле валідацію, передавши його ім'я до функцій форми `valid` та `invalid` відповідно:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> Поле форми буде позначено як дійсне чи недійсне лише після того, як воно зміниться й надійде відповідь валідації.

Якщо ви валідуєте через Precognition лише частину полів форми, вам може знадобитися вручну очистити помилки. Зробити це можна функцією форми `forgetError`:

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

Як ми бачили, ви можете підключитися до події `change` поля й валідувати окремі поля в міру взаємодії користувача з ними; проте вам може знадобитися провалідувати поля, з якими користувач ще не взаємодіяв. Так буває при побудові «майстра», де ви хочете провалідувати всі видимі поля - незалежно від того, чи торкався їх користувач, - перш ніж переходити до наступного кроку.

Щоб зробити це через Precognition, викличте метод `validate`, передавши імена потрібних полів у ключ конфігурації `only`. Обробити результат валідації можна колбеками `onSuccess` чи `onValidationError`:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

Звісно, ви можете виконувати код і у відповідь на результат надсилання форми. Функція форми `submit` повертає проміс запиту Axios. Це зручний спосіб дістатися даних відповіді, скинути поля форми після успішного надсилання чи обробити невдалий запит:

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

Визначити, чи запит на надсилання форми в дорозі, можна за властивістю форми `processing`:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-react"></a>
### Через React

За допомогою Laravel Precognition ви можете дати користувачам живу валідацію, не дублюючи правила валідації у своєму фронтенді на React. Щоб показати, як це працює, побудуймо форму створення нових користувачів у нашому застосунку.

Спершу, щоб увімкнути Precognition для маршруту, додайте до його визначення `middleware` `HandlePrecognitiveRequests`. Вам також слід створити [запит форми](/docs/{{version}}/validation#form-request-validation), який міститиме правила валідації маршруту:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

Далі встановіть фронтенд-хелпери Laravel Precognition для React через NPM:

```shell
npm install laravel-precognition-react
```

Коли пакет Laravel Precognition встановлено, ви можете створити об'єкт форми функцією `useForm` із Precognition, передавши HTTP-метод (`post`), цільовий URL (`/users`) і початкові дані форми.

Щоб увімкнути живу валідацію, слухайте події `change` і `blur` кожного поля. В обробнику `change` задавайте дані форми функцією `setData`, передаючи ім'я поля та нове значення. Далі, в обробнику `blur`, викликайте метод форми `validate`, передаючи ім'я поля:

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

Тепер, поки користувач заповнює форму, Precognition даватиме результати живої валідації на основі правил із запиту форми маршруту. Коли поля форми змінюються, до вашого застосунку Laravel надсилатиметься відкладений (debounced) «прекогнітивний» запит валідації. Ви можете налаштувати час відкладання, викликавши функцію форми `setValidationTimeout`:

```js
form.setValidationTimeout(3000);
```

Доки запит валідації в дорозі, властивість форми `validating` дорівнюватиме `true`:

```jsx
{form.validating && <div>Validating...</div>}
```

Будь-які помилки валідації, повернені під час запиту валідації чи надсилання форми, автоматично заповнять об'єкт форми `errors`:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

Визначити, чи має форма помилки, можна через властивість форми `hasErrors`:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

Ви також можете визначити, чи пройшло поле валідацію, передавши його ім'я до функцій форми `valid` та `invalid` відповідно:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> Поле форми буде позначено як дійсне чи недійсне лише після того, як воно зміниться й надійде відповідь валідації.

Якщо ви валідуєте через Precognition лише частину полів форми, вам може знадобитися вручну очистити помилки. Зробити це можна функцією форми `forgetError`:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.files[0]);

        form.forgetError('avatar');
    }}
>
```

Як ми бачили, ви можете підключитися до події `blur` поля й валідувати окремі поля в міру взаємодії користувача з ними; проте вам може знадобитися провалідувати поля, з якими користувач ще не взаємодіяв. Так буває при побудові «майстра», де ви хочете провалідувати всі видимі поля - незалежно від того, чи торкався їх користувач, - перш ніж переходити до наступного кроку.

Щоб зробити це через Precognition, викличте метод `validate`, передавши імена потрібних полів у ключ конфігурації `only`. Обробити результат валідації можна колбеками `onSuccess` чи `onValidationError`:

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

Звісно, ви можете виконувати код і у відповідь на результат надсилання форми. Функція форми `submit` повертає проміс запиту Axios. Це зручний спосіб дістатися даних відповіді, скинути поля форми після успішного надсилання чи обробити невдалий запит:

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

Визначити, чи запит на надсилання форми в дорозі, можна за властивістю форми `processing`:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-alpine"></a>
### Через Alpine і Blade

За допомогою Laravel Precognition ви можете дати користувачам живу валідацію, не дублюючи правила валідації у своєму фронтенді на Alpine. Щоб показати, як це працює, побудуймо форму створення нових користувачів у нашому застосунку.

Спершу, щоб увімкнути Precognition для маршруту, додайте до його визначення `middleware` `HandlePrecognitiveRequests`. Вам також слід створити [запит форми](/docs/{{version}}/validation#form-request-validation), який міститиме правила валідації маршруту:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

Далі встановіть фронтенд-хелпери Laravel Precognition для Alpine через NPM:

```shell
npm install laravel-precognition-alpine
```

Далі зареєструйте плагін Precognition в Alpine у своєму файлі `resources/js/app.js`:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Коли пакет Laravel Precognition встановлено й зареєстровано, ви можете створити об'єкт форми через «магію» `$form` із Precognition, передавши HTTP-метод (`post`), цільовий URL (`/users`) і початкові дані форми.

Щоб увімкнути живу валідацію, прив'яжіть дані форми до відповідного поля, а потім слухайте подію `change` кожного поля. В обробнику `change` викликайте метод форми `validate`, передаючи ім'я поля:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

Тепер, поки користувач заповнює форму, Precognition даватиме результати живої валідації на основі правил із запиту форми маршруту. Коли поля форми змінюються, до вашого застосунку Laravel надсилатиметься відкладений (debounced) «прекогнітивний» запит валідації. Ви можете налаштувати час відкладання, викликавши функцію форми `setValidationTimeout`:

```js
form.setValidationTimeout(3000);
```

Доки запит валідації в дорозі, властивість форми `validating` дорівнюватиме `true`:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

Будь-які помилки валідації, повернені під час запиту валідації чи надсилання форми, автоматично заповнять об'єкт форми `errors`:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

Визначити, чи має форма помилки, можна через властивість форми `hasErrors`:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

Ви також можете визначити, чи пройшло поле валідацію, передавши його ім'я до функцій форми `valid` та `invalid` відповідно:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> Поле форми буде позначено як дійсне чи недійсне лише після того, як воно зміниться й надійде відповідь валідації.

Як ми бачили, ви можете підключитися до події `change` поля й валідувати окремі поля в міру взаємодії користувача з ними; проте вам може знадобитися провалідувати поля, з якими користувач ще не взаємодіяв. Так буває при побудові «майстра», де ви хочете провалідувати всі видимі поля - незалежно від того, чи торкався їх користувач, - перш ніж переходити до наступного кроку.

Щоб зробити це через Precognition, викличте метод `validate`, передавши імена потрібних полів у ключ конфігурації `only`. Обробити результат валідації можна колбеками `onSuccess` чи `onValidationError`:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

Визначити, чи запит на надсилання форми в дорозі, можна за властивістю форми `processing`:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### Повторне заповнення старих даних форми

У наведеному вище прикладі створення користувача ми використовуємо Precognition для живої валідації; проте саму форму надсилаємо традиційно, на бік сервера. Тож форму слід заповнити «старими» даними й помилками валідації, поверненими після серверного надсилання:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

Або ж, якщо ви хочете надсилати форму через XHR, скористайтеся функцією форми `submit`, яка повертає проміс запиту Axios:

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    this.form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Налаштування Axios

Бібліотеки валідації Precognition використовують HTTP-клієнт [Axios](https://github.com/axios/axios), щоб надсилати запити до бекенду вашого застосунку. Для зручності екземпляр Axios можна налаштувати, якщо цього вимагає ваш застосунок. Наприклад, користуючись бібліотекою `laravel-precognition-vue`, ви можете додати додаткові заголовки до кожного вихідного запиту у файлі `resources/js/app.js` вашого застосунку:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

Або ж, якщо у вас уже є налаштований екземпляр Axios, ви можете вказати Precognition використовувати саме його:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

<a name="validating-arrays"></a>
## Валідація масивів

Ви можете скористатися символами підстановки, щоб валідувати поля всередині масивів чи вкладених об'єктів. Кожен `*` відповідає одному сегменту шляху:

```js
// Validate email for all users in an array...
form.validate('users.*.email');

// Validate all fields in a profile object...
form.validate('profile.*');

// Validate all fields for all users...
form.validate('users.*.*');
```

<a name="customizing-validation-rules"></a>
## Налаштування правил валідації

Правила валідації, які виконуються під час прекогнітивного запиту, можна налаштувати методом запиту `isPrecognitive`.

Наприклад, у формі створення користувача ми можемо захотіти перевіряти пароль на «невикритість» лише при остаточному надсиланні форми. Для прекогнітивних запитів валідації ми просто перевірятимемо, що пароль обов'язковий і має щонайменше 8 символів. Методом `isPrecognitive` ми можемо налаштувати правила, визначені в нашому запиті форми:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-file-uploads"></a>
## Обробка завантаження файлів

За замовчуванням Laravel Precognition не завантажує й не валідує файли під час прекогнітивного запиту валідації. Це гарантує, що великі файли не завантажуватимуться зайвий раз кілька разів.

Через таку поведінку вам слід переконатися, що ваш застосунок [налаштовує відповідні правила валідації запиту форми](#customizing-validation-rules) так, щоб поле було обов'язковим лише при повному надсиланні форми:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

Якщо ви хочете включати файли до кожного запиту валідації, викличте функцію `validateFiles` на екземплярі форми на боці клієнта:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## Керування побічними ефектами

Додаючи до маршруту `middleware` `HandlePrecognitiveRequests`, подумайте, чи немає в _іншому_ `middleware` побічних ефектів, які слід пропустити під час прекогнітивного запиту.

Наприклад, у вас може бути `middleware`, яке рахує загальну кількість «взаємодій» кожного користувача з вашим застосунком, - але ви можете не хотіти, щоб прекогнітивні запити рахувалися як взаємодія. Щоб цього досягти, перевіряйте метод запиту `isPrecognitive` перед збільшенням лічильника:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

<a name="testing"></a>
## Тестування

Якщо ви хочете робити прекогнітивні запити у своїх тестах, `TestCase` у Laravel містить хелпер `withPrecognition`, який додасть заголовок запиту `Precognition`.

Крім того, якщо ви хочете перевірити, що прекогнітивний запит був успішним - тобто не повернув помилок валідації, - скористайтеся методом `assertSuccessfulPrecognition` на відповіді:

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```

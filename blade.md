---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Шаблони Blade

- [Вступ](#introduction)
    - [Підсилення Blade за допомогою Livewire](#supercharging-blade-with-livewire)
- [Виведення даних](#displaying-data)
    - [Кодування HTML-сутностей](#html-entity-encoding)
    - [Blade та JavaScript-фреймворки](#blade-and-javascript-frameworks)
- [Директиви Blade](#blade-directives)
    - [Умовні конструкції](#if-statements)
    - [Конструкції switch](#switch-statements)
    - [Цикли](#loops)
    - [Змінна циклу](#the-loop-variable)
    - [Умовні класи](#conditional-classes)
    - [Додаткові атрибути](#additional-attributes)
    - [Включення підпредставлень](#including-subviews)
    - [Директива `@once`](#the-once-directive)
    - [Чистий PHP](#raw-php)
    - [Шрифти](#fonts)
    - [Коментарі](#comments)
- [Компоненти](#components)
    - [Рендеринг компонентів](#rendering-components)
    - [Індексні компоненти](#index-components)
    - [Передавання даних до компонентів](#passing-data-to-components)
    - [Атрибути компонентів](#component-attributes)
    - [Зарезервовані ключові слова](#reserved-keywords)
    - [Слоти](#slots)
    - [Вбудовані представлення компонентів](#inline-component-views)
    - [Динамічні компоненти](#dynamic-components)
    - [Ручна реєстрація компонентів](#manually-registering-components)
- [Анонімні компоненти](#anonymous-components)
    - [Анонімні індексні компоненти](#anonymous-index-components)
    - [Властивості даних та атрибути](#data-properties-attributes)
    - [Доступ до даних батьківського компонента](#accessing-parent-data)
    - [Шляхи анонімних компонентів](#anonymous-component-paths)
- [Створення макетів](#building-layouts)
    - [Макети на компонентах](#layouts-using-components)
    - [Макети на успадкуванні шаблонів](#layouts-using-template-inheritance)
- [Форми](#forms)
    - [Поле CSRF](#csrf-field)
    - [Поле методу](#method-field)
    - [Помилки валідації](#validation-errors)
- [Стеки](#stacks)
- [Впровадження сервісів](#service-injection)
- [Рендеринг вбудованих шаблонів Blade](#rendering-inline-blade-templates)
- [Рендеринг фрагментів Blade](#rendering-blade-fragments)
- [Розширення Blade](#extending-blade)
    - [Власні обробники виведення](#custom-echo-handlers)
    - [Власні умовні конструкції](#custom-if-statements)

<a name="introduction"></a>
## Вступ

Blade - це простий, але потужний шаблонізатор, що входить до складу Laravel. На відміну від деяких PHP-шаблонізаторів, Blade не забороняє використовувати звичайний PHP-код у ваших шаблонах. Насправді всі шаблони Blade компілюються у звичайний PHP-код і кешуються, доки їх не змінено, тобто Blade практично не додає накладних витрат вашому застосунку. Файли шаблонів Blade мають розширення `.blade.php` і зазвичай зберігаються в каталозі `resources/views`.

Представлення Blade можна повертати з маршрутів чи контролерів за допомогою глобального хелпера `view`. Звісно, як зазначено в документації з [представлень](/docs/{{version}}/views), дані можна передати представленню Blade другим аргументом хелпера `view`:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Підсилення Blade за допомогою Livewire

Хочете вивести свої шаблони Blade на новий рівень і легко створювати динамічні інтерфейси? Перегляньте [Laravel Livewire](https://livewire.laravel.com). Livewire дозволяє писати компоненти Blade, доповнені динамічною функціональністю, яка зазвичай можлива лише через фронтенд-фреймворки на кшталт React, Svelte чи Vue, - це чудовий підхід до створення сучасних реактивних інтерфейсів без складнощів, клієнтського рендерингу чи етапів збірки, властивих багатьом JavaScript-фреймворкам.

<a name="displaying-data"></a>
## Виведення даних

Ви можете виводити дані, передані вашим представленням Blade, узявши змінну у фігурні дужки. Наприклад, маючи такий маршрут:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

Ви можете вивести вміст змінної `name` так:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Інструкції виведення `{{ }}` у Blade автоматично проходять через PHP-функцію `htmlspecialchars`, щоб запобігти XSS-атакам.

Ви не обмежені виведенням лише переданих представленню змінних. Ви також можете вивести результат будь-якої PHP-функції. Насправді ви можете розмістити всередині інструкції виведення Blade будь-який PHP-код:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### Кодування HTML-сутностей

За замовчуванням Blade (і функція Laravel `e`) виконує подвійне кодування HTML-сутностей. Якщо ви хочете вимкнути подвійне кодування, викличте метод `Blade::withoutDoubleEncoding` у методі `boot` вашого `AppServiceProvider`:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### Виведення неекранованих даних

За замовчуванням інструкції `{{ }}` у Blade автоматично проходять через PHP-функцію `htmlspecialchars`, щоб запобігти XSS-атакам. Якщо ви не хочете, щоб ваші дані екранувалися, скористайтеся таким синтаксисом:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> Будьте дуже обережні, виводячи вміст, наданий користувачами вашого застосунку. Зазвичай, показуючи надані користувачами дані, слід використовувати екранований синтаксис із подвійними фігурними дужками, щоб запобігти XSS-атакам.

<a name="blade-and-javascript-frameworks"></a>
### Blade та JavaScript-фреймворки

Оскільки багато JavaScript-фреймворків теж використовують фігурні дужки, щоб позначити вираз для виведення в браузері, ви можете скористатися символом `@`, щоб повідомити рушій Blade, що вираз слід залишити недоторканим. Наприклад:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

У цьому прикладі Blade прибере символ `@`; однак вираз `{{ name }}` лишиться недоторканим рушієм Blade, що дозволить вашому JavaScript-фреймворку відрендерити його.

Символ `@` можна також використовувати, щоб екранувати директиви Blade:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### Рендеринг JSON

Іноді ви можете передавати представленню масив, щоб відрендерити його як JSON і ініціалізувати JavaScript-змінну. Наприклад:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

Однак замість викликати `json_encode` вручну, ви можете скористатися методом `Illuminate\Support\Js::from`. Метод `from` приймає ті самі аргументи, що й PHP-функція `json_encode`; однак він гарантує, що отриманий JSON правильно екрановано для вставки в HTML-лапки. Метод `from` поверне рядок з інструкцією JavaScript `JSON.parse`, яка перетворить переданий об'єкт чи масив на дійсний об'єкт JavaScript:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Найновіші версії каркаса застосунку Laravel містять фасад `Js`, що дає зручний доступ до цієї функціональності у ваших шаблонах Blade:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> Метод `Js::from` слід використовувати лише для рендерингу наявних змінних як JSON. Шаблонізатор Blade побудований на регулярних виразах, і спроби передати директиві складний вираз можуть спричинити несподівані збої.

<a name="the-at-verbatim-directive"></a>
#### Директива `@verbatim`

Якщо ви виводите JavaScript-змінні у великій частині свого шаблону, ви можете обгорнути HTML директивою `@verbatim`, щоб не додавати символ `@` до кожної інструкції виведення Blade:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Директиви Blade

Окрім успадкування шаблонів і виведення даних, Blade також надає зручні скорочення для поширених керуючих конструкцій PHP - як-от умовних конструкцій і циклів. Ці скорочення дають дуже чистий і стислий спосіб працювати з керуючими конструкціями PHP, залишаючись водночас звичними для їхніх PHP-відповідників.

<a name="if-statements"></a>
### Умовні конструкції

Ви можете створювати конструкції `if` за допомогою директив `@if`, `@elseif`, `@else` та `@endif`. Вони працюють ідентично до своїх PHP-відповідників:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

Для зручності Blade також надає директиву `@unless`:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

Окрім уже розглянутих умовних директив, директиви `@isset` та `@empty` можна використовувати як зручні скорочення для відповідних PHP-функцій:

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```

<a name="authentication-directives"></a>
#### Директиви автентифікації

Директиви `@auth` та `@guest` дозволяють швидко визначити, чи є поточний користувач [автентифікованим](/docs/{{version}}/authentication), чи гостем:

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

За потреби ви можете вказати гард автентифікації, який слід перевіряти, використовуючи директиви `@auth` та `@guest`:

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```

<a name="environment-directives"></a>
#### Директиви середовища

Перевірити, чи працює застосунок у продакшен-середовищі, можна директивою `@production`:

```blade
@production
    // Production specific content...
@endproduction
```

Або ж ви можете визначити, чи працює застосунок у конкретному середовищі, директивою `@env`:

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```

<a name="section-directives"></a>
#### Директиви секцій

Ви можете визначити, чи має секція успадкування шаблонів вміст, директивою `@hasSection`:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

Директива `sectionMissing` дозволяє визначити, що секція не має вмісту:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### Директиви сесії

Директива `@session` дозволяє визначити, чи існує значення [сесії](/docs/{{version}}/session). Якщо воно існує, вміст шаблону між директивами `@session` та `@endsession` буде обчислено. Усередині директиви `@session` ви можете вивести змінну `$value`, щоб показати значення сесії:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### Директиви контексту

Директива `@context` дозволяє визначити, чи існує значення [контексту](/docs/{{version}}/context). Якщо воно існує, вміст шаблону між директивами `@context` та `@endcontext` буде обчислено. Усередині директиви `@context` ви можете вивести змінну `$value`, щоб показати значення контексту:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Конструкції switch

Конструкції switch можна створювати за допомогою директив `@switch`, `@case`, `@break`, `@default` та `@endswitch`:

```blade
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```

<a name="loops"></a>
### Цикли

Окрім умовних конструкцій, Blade надає прості директиви для роботи з циклами PHP. Знову ж таки, кожна з них працює ідентично до свого PHP-відповідника:

```blade
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

> [!NOTE]
> Ітеруючи в циклі `foreach`, ви можете скористатися [змінною циклу](#the-loop-variable), щоб отримати корисну інформацію про цикл - наприклад, чи це перша або остання ітерація.

Використовуючи цикли, ви також можете пропустити поточну ітерацію чи завершити цикл директивами `@continue` та `@break`:

```blade
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```

Ви також можете вказати умову продовження чи переривання просто в оголошенні директиви:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Змінна циклу

Ітеруючи в циклі `foreach`, усередині циклу вам буде доступна змінна `$loop`. Вона дає доступ до корисної інформації - як-от поточний індекс циклу та чи є ця ітерація першою або останньою:

```blade
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```

Якщо ви у вкладеному циклі, ви можете звернутися до змінної `$loop` батьківського циклу через властивість `parent`:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

Змінна `$loop` також містить низку інших корисних властивостей:

<div class="overflow-auto">

| Властивість        | Опис                                                   |
| ------------------ | ------------------------------------------------------ |
| `$loop->index`     | Індекс поточної ітерації циклу (починається з 0).      |
| `$loop->iteration` | Поточна ітерація циклу (починається з 1).              |
| `$loop->remaining` | Скільки ітерацій лишилося в циклі.                     |
| `$loop->count`     | Загальна кількість елементів у масиві, який ітерується.|
| `$loop->first`     | Чи є ця ітерація першою в циклі.                       |
| `$loop->last`      | Чи є ця ітерація останньою в циклі.                    |
| `$loop->even`      | Чи є ця ітерація парною.                               |
| `$loop->odd`       | Чи є ця ітерація непарною.                             |
| `$loop->depth`     | Рівень вкладеності поточного циклу.                    |
| `$loop->parent`    | У вкладеному циклі - змінна циклу батька.              |

</div>

<a name="conditional-classes"></a>
### Умовні класи та стилі

Директива `@class` умовно компілює рядок CSS-класів. Вона приймає масив класів, де ключ містить клас або класи, які ви хочете додати, а значення є булевим виразом. Якщо елемент масиву має числовий ключ, його буде включено завжди:

```blade
@php
    $isActive = false;
    $hasError = true;
@endphp

<span @class([
    'p-4',
    'font-bold' => $isActive,
    'text-gray-500' => ! $isActive,
    'bg-red' => $hasError,
])></span>

<span class="p-4 text-gray-500 bg-red"></span>
```

Так само директива `@style` дозволяє умовно додавати вбудовані CSS-стилі до HTML-елемента:

```blade
@php
    $isActive = true;
@endphp

<span @style([
    'background-color: red',
    'font-weight: bold' => $isActive,
])></span>

<span style="background-color: red; font-weight: bold;"></span>
```

<a name="additional-attributes"></a>
### Додаткові атрибути

Для зручності ви можете скористатися директивою `@checked`, щоб легко вказати, чи є певний HTML-чекбокс «позначеним». Ця директива виведе `checked`, якщо передана умова дає `true`:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

Так само директива `@selected` дозволяє вказати, чи має бути обраний певний варіант у списку:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

Крім того, директива `@disabled` дозволяє вказати, чи має елемент бути вимкненим:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

Ба більше, директива `@readonly` дозволяє вказати, чи має елемент бути лише для читання:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

Крім того, директива `@required` дозволяє вказати, чи є елемент обов'язковим:

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
### Включення підпредставлень

> [!NOTE]
> Хоча ви вільні використовувати директиву `@include`, [компоненти](#components) Blade дають схожу функціональність і кілька переваг над `@include` - як-от прив'язку даних і атрибутів.

Директива `@include` у Blade дозволяє включити одне представлення Blade всередину іншого. Усі змінні, доступні батьківському представленню, будуть доступні й включеному:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

Хоча включене представлення успадкує всі дані батьківського, ви також можете передати масив додаткових даних:

```blade
@include('view.name', ['status' => 'complete'])
```

Якщо ви спробуєте включити (`@include`) представлення, якого не існує, Laravel викине помилку. Якщо ви хочете включити представлення, яке може існувати, а може й ні, скористайтеся директивою `@includeIf`:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

Якщо ви хочете включити представлення, коли булевий вираз дає `true` чи `false`, скористайтеся директивами `@includeWhen` та `@includeUnless`:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

Щоб включити перше наявне представлення з переданого масиву, скористайтеся директивою `includeFirst`:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

Якщо ви хочете включити представлення, не успадковуючи змінних батьківського, скористайтеся директивою `@includeIsolated`. Включене представлення матиме доступ лише до змінних, які ви передасте явно:

```blade
@includeIsolated('view.name', ['user' => $user])
```

> [!WARNING]
> Уникайте використання констант `__DIR__` і `__FILE__` у своїх представленнях Blade, адже вони вказуватимуть на розташування закешованого скомпільованого представлення.

<a name="rendering-views-for-collections"></a>
#### Рендеринг представлень для колекцій

Ви можете поєднати цикли та включення в один рядок директивою `@each`:

```blade
@each('view.name', $jobs, 'job')
```

Перший аргумент директиви `@each` - представлення для рендерингу кожного елемента масиву чи колекції. Другий - масив чи колекція, яку ви хочете ітерувати, а третій - ім'я змінної, яку буде призначено поточній ітерації всередині представлення. Тож, наприклад, якщо ви ітеруєте масив `jobs`, зазвичай ви захочете звертатися до кожного завдання як до змінної `job`. Ключ масиву для поточної ітерації буде доступний у представленні як змінна `key`.

Директиві `@each` можна також передати четвертий аргумент. Він визначає представлення, яке буде відрендерено, якщо переданий масив порожній.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> Представлення, відрендерені через `@each`, не успадковують змінних батьківського представлення. Якщо дочірньому представленню потрібні ці змінні, скористайтеся натомість директивами `@foreach` та `@include`.

<a name="the-once-directive"></a>
### Директива `@once`

Директива `@once` дозволяє визначити частину шаблону, яка буде обчислена лише один раз за цикл рендерингу. Це може бути корисно, щоб додати певний JavaScript у шапку сторінки через [стеки](#stacks). Наприклад, якщо ви рендерите [компонент](#components) у циклі, ви можете захотіти додати JavaScript у шапку лише під час першого рендерингу компонента:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

Оскільки директиву `@once` часто використовують разом із `@push` чи `@prepend`, для зручності доступні директиви `@pushOnce` та `@prependOnce`:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

Якщо ви додаєте однаковий вміст із двох різних шаблонів Blade, передайте унікальний ідентифікатор другим аргументом директиви `@pushOnce`, щоб вміст відрендерився лише раз:

```blade
<!-- pie-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce

<!-- line-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce
```

<a name="raw-php"></a>
### Чистий PHP

У деяких ситуаціях корисно вставити PHP-код у свої представлення. Ви можете скористатися директивою Blade `@php`, щоб виконати блок звичайного PHP у своєму шаблоні:

```blade
@php
    $counter = 1;
@endphp
```

Або, якщо PHP потрібен вам лише для імпорту класу, скористайтеся директивою `@use`:

```blade
@use('App\Models\Flight')
```

Директиві `@use` можна передати другий аргумент, щоб задати псевдонім імпортованому класу:

```blade
@use('App\Models\Flight', 'FlightModel')
```

Якщо у вас кілька класів в одному просторі імен, ви можете згрупувати їхні імпорти:

```blade
@use('App\Models\{Flight, Airport}')
```

Директива `@use` також підтримує імпорт PHP-функцій і констант - для цього додайте до шляху імпорту модифікатор `function` чи `const`:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

Як і для класів, для функцій і констант підтримуються псевдоніми:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

Згруповані імпорти теж підтримуються з модифікаторами `function` і `const`, що дозволяє імпортувати кілька символів з одного простору імен однією директивою:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="fonts"></a>
### Шрифти

Використовуючи [оптимізацію шрифтів через Vite](/docs/{{version}}/vite#working-with-fonts) у Laravel, ви можете скористатися директивою `@fonts`, щоб відрендерити налаштовані посилання попереднього завантаження шрифтів і вбудований CSS шрифтів у макеті вашого застосунку:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @fonts
    @vite('resources/js/app.js')
</head>
```

Директива `@fonts` рендерить усі родини шрифтів, налаштовані у вашому файлі `vite.config.js`. Зазвичай її слід розміщувати в `<head>` кореневого макета вашого застосунку перед будь-яким вмістом, що використовує ці шрифти.

Якщо сторінці потрібні лише деякі з налаштованих шрифтів, ви можете передати директиві один чи кілька псевдонімів:

```blade
{{-- Load a single font alias... --}}
@fonts('sans')

{{-- Load multiple font aliases... --}}
@fonts(['sans', 'mono'])
```

Псевдоніми шрифтів налаштовуються опцією `alias` під час визначення шрифтів у вашій конфігурації Vite. Директива `@fonts` викликає метод `fonts` фасаду `Vite`, який можна викликати й напряму:

```blade
{{ Vite::fonts(['sans', 'mono']) }}
```

<a name="comments"></a>
### Коментарі

Blade також дозволяє визначати коментарі у ваших представленнях. Однак, на відміну від HTML-коментарів, коментарі Blade не потрапляють до HTML, який повертає ваш застосунок:

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
## Компоненти

Компоненти та слоти дають переваги, схожі на секції, макети та включення; утім, декому ментальна модель компонентів і слотів може здатися зрозумілішою. Є два підходи до написання компонентів: компоненти на основі класів та анонімні компоненти.

Щоб створити компонент на основі класу, скористайтеся командою Artisan `make:component`. Щоб проілюструвати використання компонентів, ми створимо простий компонент `Alert`. Команда `make:component` помістить компонент у каталог `app/View/Components`:

```shell
php artisan make:component Alert
```

Команда `make:component` також створить шаблон представлення для компонента. Представлення буде розміщено в каталозі `resources/views/components`. Пишучи компоненти для власного застосунку, ви не потребуєте додаткової реєстрації: компоненти автоматично виявляються в каталогах `app/View/Components` і `resources/views/components`.

Ви також можете створювати компоненти в підкаталогах:

```shell
php artisan make:component Forms/Input
```

Наведена вище команда створить компонент `Input` у каталозі `app/View/Components/Forms`, а представлення буде розміщено в `resources/views/components/forms`.

<a name="manually-registering-package-components"></a>
#### Ручна реєстрація компонентів пакета

Пишучи компоненти для власного застосунку, ви не потребуєте додаткової реєстрації: вони автоматично виявляються в каталогах `app/View/Components` і `resources/views/components`.

Однак якщо ви створюєте пакет, що використовує компоненти Blade, вам доведеться вручну зареєструвати клас компонента та його псевдонім HTML-тега. Зазвичай компоненти слід реєструвати в методі `boot` сервіс-провайдера вашого пакета:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

Щойно компонент зареєстровано, його можна відрендерити за псевдонімом тега:

```blade
<x-package-alert/>
```

Як альтернативу ви можете скористатися методом `componentNamespace`, щоб автозавантажувати класи компонентів за домовленостями. Наприклад, пакет `Nightshade` може мати компоненти `Calendar` і `ColorPicker`, розташовані у просторі імен `Package\Views\Components`:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

Це дозволить використовувати компоненти пакета через простір імен постачальника за синтаксисом `package-name::`:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade автоматично визначить клас, пов'язаний із цим компонентом, перетворивши ім'я компонента на PascalCase. Підкаталоги теж підтримуються через «крапкову» нотацію.

<a name="rendering-components"></a>
### Рендеринг компонентів

Щоб показати компонент, скористайтеся тегом компонента Blade в одному зі своїх шаблонів. Теги компонентів Blade починаються з рядка `x-`, за яким іде ім'я класу компонента в kebab-case:

```blade
<x-alert/>

<x-user-profile/>
```

Якщо клас компонента вкладено глибше в каталозі `app/View/Components`, ви можете скористатися символом `.`, щоб позначити вкладеність каталогів. Наприклад, якщо компонент розташовано в `app/View/Components/Inputs/Button.php`, ми можемо відрендерити його так:

```blade
<x-inputs.button/>
```

Якщо ви хочете рендерити компонент умовно, визначте в його класі метод `shouldRender`. Якщо `shouldRender` поверне `false`, компонент не буде відрендерено:

```php
use Illuminate\Support\Str;

/**
 * Whether the component should be rendered
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### Індексні компоненти

Іноді компоненти є частиною групи, і ви можете захотіти згрупувати пов'язані компоненти в одному каталозі. Наприклад, уявіть компонент «card» із такою структурою класів:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

Оскільки кореневий компонент `Card` вкладено в каталог `Card`, можна було б очікувати, що рендерити його доведеться через `<x-card.card>`. Однак коли ім'я файлу компонента збігається з іменем його каталогу, Laravel автоматично вважає цей компонент «кореневим» і дозволяє рендерити його без повторення імені каталогу:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### Передавання даних до компонентів

Ви можете передавати дані компонентам Blade через HTML-атрибути. Жорстко задані примітивні значення передаються звичайними рядковими атрибутами HTML. PHP-вирази та змінні слід передавати через атрибути з префіксом `:`:

```blade
<x-alert type="error" :message="$message"/>
```

Усі атрибути даних компонента слід визначити в конструкторі його класу. Усі публічні властивості компонента автоматично стануть доступними його представленню. Передавати дані представленню з методу `render` компонента не потрібно:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

Коли ваш компонент рендериться, ви можете вивести вміст його публічних змінних, звернувшись до них за іменем:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### Регістр

Аргументи конструктора компонента слід записувати в `camelCase`, тоді як у HTML-атрибутах на них посилаються в `kebab-case`. Наприклад, маючи такий конструктор компонента:

```php
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```

Аргумент `$alertType` можна передати компоненту так:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### Короткий синтаксис атрибутів

Передаючи атрибути компонентам, ви можете скористатися «коротким синтаксисом атрибутів». Це часто зручно, адже імена атрибутів нерідко збігаються з іменами відповідних змінних:

```blade
{{-- Short attribute syntax... --}}
<x-profile :$userId :$name />

{{-- Is equivalent to... --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### Екранування рендерингу атрибутів

Оскільки деякі JavaScript-фреймворки на кшталт Alpine.js теж використовують атрибути з двокрапкою, ви можете скористатися префіксом із подвійною двокрапкою (`::`), щоб повідомити Blade, що атрибут не є PHP-виразом. Наприклад, маючи такий компонент:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade відрендерить такий HTML:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### Методи компонента

Окрім публічних змінних, доступних шаблону компонента, можна викликати будь-які його публічні методи. Наприклад, уявіть компонент із методом `isSelected`:

```php
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

Ви можете виконати цей метод із шаблону компонента, звернувшись до змінної з іменем цього методу:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### Доступ до атрибутів і слотів усередині класів компонентів

Компоненти Blade також дозволяють звертатися до імені компонента, його атрибутів і слота всередині методу `render` класу. Однак щоб отримати доступ до цих даних, метод `render` має повертати замикання:

```php
use Closure;

/**
 * Get the view / contents that represent the component.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

Замикання, повернене методом `render`, може також отримувати масив `$data` як єдиний аргумент. Цей масив міститиме кілька елементів з інформацією про компонент:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> Елементи масиву `$data` ніколи не слід вставляти безпосередньо в рядок Blade, який повертає ваш метод `render`, адже це може дозволити віддалене виконання коду через зловмисний вміст атрибутів.

`componentName` дорівнює імені, використаному в HTML-тегу після префікса `x-`. Тож для `<x-alert />` `componentName` буде `alert`. Елемент `attributes` міститиме всі атрибути, присутні в HTML-тегу. Елемент `slot` є екземпляром `Illuminate\Support\HtmlString` із вмістом слота компонента.

Замикання має повертати рядок. Якщо повернений рядок відповідає наявному представленню, буде відрендерено це представлення; інакше рядок буде обчислено як вбудоване представлення Blade.

<a name="additional-dependencies"></a>
#### Додаткові залежності

Якщо вашому компоненту потрібні залежності із [сервіс-контейнера](/docs/{{version}}/container) Laravel, перелічіть їх перед будь-якими атрибутами даних компонента, і контейнер автоматично впровадить їх:

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### Приховування атрибутів і методів

Якщо ви хочете, щоб деякі публічні методи чи властивості не потрапляли до шаблону компонента як змінні, додайте їх до масиву `$except` у своєму компоненті:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The properties / methods that should not be exposed to the component template.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### Атрибути компонентів

Ми вже розглянули, як передавати компоненту атрибути даних; однак іноді вам може знадобитися вказати додаткові HTML-атрибути - як-от `class`, - які не є частиною даних, потрібних компоненту для роботи. Зазвичай ви захочете передати ці додаткові атрибути кореневому елементу шаблону компонента. Наприклад, уявіть, що ми хочемо відрендерити компонент `alert` так:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

Усі атрибути, які не є частиною конструктора компонента, автоматично потраплять до «набору атрибутів» компонента. Цей набір автоматично доступний компоненту через змінну `$attributes`. Усі атрибути можна відрендерити в компоненті, вивівши цю змінну:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> Використання директив на кшталт `@env` усередині тегів компонентів наразі не підтримується. Наприклад, `<x-alert :live="@env('production')"/>` не буде скомпільовано.

<a name="default-merged-attributes"></a>
#### Типові та об'єднані атрибути

Іноді вам може знадобитися задати типові значення атрибутів або додати значення до наявних атрибутів компонента. Для цього скористайтеся методом `merge` набору атрибутів. Цей метод особливо корисний, щоб визначити набір типових CSS-класів, які завжди мають застосовуватися до компонента:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

Якщо припустити, що цей компонент використовується так:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

Кінцевий відрендерений HTML компонента виглядатиме так:

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### Умовне об'єднання класів

Іноді ви можете захотіти об'єднати класи, якщо певна умова дає `true`. Це робиться методом `class`, який приймає масив класів, де ключ містить клас або класи, які ви хочете додати, а значення є булевим виразом. Якщо елемент масиву має числовий ключ, його буде включено завжди:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

Якщо вам потрібно об'єднати інші атрибути компонента, ви можете приєднати метод `merge` до методу `class`:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> Якщо вам потрібно умовно компілювати класи для інших HTML-елементів, які не мають отримувати об'єднані атрибути, скористайтеся [директивою @class](#conditional-classes).

<a name="non-class-attribute-merging"></a>
#### Об'єднання атрибутів, відмінних від class

Об'єднуючи атрибути, відмінні від `class`, значення, передані методу `merge`, вважатимуться «типовими» значеннями атрибута. Однак, на відміну від `class`, ці атрибути не об'єднуватимуться з переданими значеннями, а будуть перезаписані. Наприклад, реалізація компонента `button` може виглядати так:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

Щоб відрендерити компонент кнопки з власним `type`, його можна вказати під час використання компонента. Якщо тип не вказано, буде використано `button`:

```blade
<x-button type="submit">
    Submit
</x-button>
```

Відрендерений HTML компонента `button` у цьому прикладі буде таким:

```blade
<button type="submit">
    Submit
</button>
```

Якщо ви хочете, щоб типове та передане значення атрибута, відмінного від `class`, об'єднувалися, скористайтеся методом `prepends`. У цьому прикладі атрибут `data-controller` завжди починатиметься з `profile-controller`, а будь-які додаткові передані значення `data-controller` розміщуватимуться після цього типового значення:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### Отримання та фільтрування атрибутів

Ви можете фільтрувати атрибути методом `filter`. Він приймає замикання, яке має повертати `true`, якщо ви хочете залишити атрибут у наборі:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

Для зручності ви можете скористатися методом `whereStartsWith`, щоб отримати всі атрибути, чиї ключі починаються з певного рядка:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

І навпаки, метод `whereDoesntStartWith` дозволяє виключити всі атрибути, чиї ключі починаються з певного рядка:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

Методом `first` ви можете відрендерити перший атрибут у наборі:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

Якщо ви хочете перевірити наявність атрибута в компоненті, скористайтеся методом `has`. Він приймає ім'я атрибута як єдиний аргумент і повертає булеве значення, що вказує на його наявність:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

Якщо методу `has` передано масив, він визначить, чи присутні в компоненті всі вказані атрибути:

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

Метод `hasAny` дозволяє визначити, чи присутній у компоненті хоч один із указаних атрибутів:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

Отримати значення конкретного атрибута можна методом `get`:

```blade
{{ $attributes->get('class') }}
```

Метод `only` дозволяє отримати лише атрибути з указаними ключами:

```blade
{{ $attributes->only(['class']) }}
```

Метод `except` дозволяє отримати всі атрибути, крім тих, що мають указані ключі:

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### Зарезервовані ключові слова

За замовчуванням деякі ключові слова зарезервовано для внутрішнього використання Blade під час рендерингу компонентів. Наведені нижче слова не можна визначати як публічні властивості чи імена методів у ваших компонентах:

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a name="slots"></a>
### Слоти

Часто вам потрібно передати компоненту додатковий вміст через «слоти». Слоти компонента рендеряться виведенням змінної `$slot`. Щоб дослідити цю концепцію, уявімо, що компонент `alert` має таку розмітку:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

Ми можемо передати вміст у `slot`, вставивши його в компонент:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

Іноді компоненту може знадобитися відрендерити кілька різних слотів у різних місцях. Змінімо наш компонент alert, щоб дозволити вставку слота «title»:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

Вміст іменованого слота визначається тегом `x-slot`. Будь-який вміст поза явним тегом `x-slot` буде передано компоненту у змінній `$slot`:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

Ви можете викликати метод `isEmpty` слота, щоб визначити, чи містить він вміст:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>
```

Крім того, метод `hasActualContent` дозволяє визначити, чи містить слот «справжній» вміст, що не є HTML-коментарем:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
#### Слоти з областю видимості

Якщо ви користувалися JavaScript-фреймворком на кшталт Vue, вам можуть бути знайомі «scoped slots», які дозволяють звертатися до даних чи методів компонента всередині слота. Схожої поведінки в Laravel можна досягти, визначивши публічні методи чи властивості компонента й звертаючись до компонента всередині слота через змінну `$component`. У цьому прикладі ми припустимо, що компонент `x-alert` має публічний метод `formatAlert`, визначений у його класі:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
#### Атрибути слотів

Як і компонентам Blade, слотам можна призначати додаткові [атрибути](#component-attributes) - як-от імена CSS-класів:

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot:footer class="text-sm">
        Footer
    </x-slot>
</x-card>
```

Щоб працювати з атрибутами слота, звертайтеся до властивості `attributes` змінної слота. Докладніше про роботу з атрибутами дивіться в документації з [атрибутів компонентів](#component-attributes):

```blade
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```

<a name="inline-component-views"></a>
### Вбудовані представлення компонентів

Для дуже маленьких компонентів керувати і класом компонента, і його шаблоном може здаватися марудним. Тому ви можете повертати розмітку компонента просто з методу `render`:

```php
/**
 * Get the view / contents that represent the component.
 */
public function render(): string
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```

<a name="generating-inline-view-components"></a>
#### Генерація компонентів із вбудованим представленням

Щоб створити компонент, який рендерить вбудоване представлення, скористайтеся опцією `inline` під час виконання команди `make:component`:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### Динамічні компоненти

Іноді вам може знадобитися відрендерити компонент, не знаючи до моменту виконання, який саме компонент слід рендерити. У такій ситуації скористайтеся вбудованим компонентом `dynamic-component`, щоб відрендерити компонент на основі значення чи змінної під час виконання:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### Ручна реєстрація компонентів

> [!WARNING]
> Наведена нижче документація про ручну реєстрацію компонентів стосується насамперед тих, хто пише пакети Laravel із компонентами представлень. Якщо ви не пишете пакет, ця частина документації може бути для вас неактуальною.

Пишучи компоненти для власного застосунку, ви не потребуєте додаткової реєстрації: вони автоматично виявляються в каталогах `app/View/Components` і `resources/views/components`.

Однак якщо ви створюєте пакет, що використовує компоненти Blade, або розміщуєте компоненти в нетипових каталогах, вам доведеться вручну зареєструвати клас компонента та його псевдонім HTML-тега, щоб Laravel знав, де шукати компонент. Зазвичай компоненти слід реєструвати в методі `boot` сервіс-провайдера вашого пакета:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

Щойно компонент зареєстровано, його можна відрендерити за псевдонімом тега:

```blade
<x-package-alert/>
```

#### Автозавантаження компонентів пакета

Як альтернативу ви можете скористатися методом `componentNamespace`, щоб автозавантажувати класи компонентів за домовленостями. Наприклад, пакет `Nightshade` може мати компоненти `Calendar` і `ColorPicker`, розташовані у просторі імен `Package\Views\Components`:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

Це дозволить використовувати компоненти пакета через простір імен постачальника за синтаксисом `package-name::`:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade автоматично визначить клас, пов'язаний із цим компонентом, перетворивши ім'я компонента на PascalCase. Підкаталоги теж підтримуються через «крапкову» нотацію.

<a name="anonymous-components"></a>
## Анонімні компоненти

Подібно до вбудованих компонентів, анонімні компоненти дають механізм керування компонентом через один файл. Однак анонімні компоненти використовують лише файл представлення й не мають пов'язаного класу. Щоб визначити анонімний компонент, достатньо розмістити шаблон Blade у каталозі `resources/views/components`. Наприклад, якщо ви визначили компонент у `resources/views/components/alert.blade.php`, ви можете відрендерити його так:

```blade
<x-alert/>
```

Ви можете скористатися символом `.`, щоб позначити вкладеність компонента глибше в каталозі `components`. Наприклад, якщо компонент визначено в `resources/views/components/inputs/button.blade.php`, відрендерити його можна так:

```blade
<x-inputs.button/>
```

Щоб створити анонімний компонент через Artisan, скористайтеся прапорцем `--view` під час виклику команди `make:component`:

```shell
php artisan make:component forms.input --view
```

Наведена вище команда створить файл Blade у `resources/views/components/forms/input.blade.php`, який можна відрендерити як компонент через `<x-forms.input />`.

<a name="anonymous-index-components"></a>
### Анонімні індексні компоненти

Іноді, коли компонент складається з багатьох шаблонів Blade, ви можете захотіти згрупувати їх в одному каталозі. Наприклад, уявіть компонент «accordion» із такою структурою каталогів:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

Ця структура дозволяє рендерити компонент accordion та його елемент так:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

Однак щоб відрендерити компонент accordion через `x-accordion`, нам довелося розмістити «індексний» шаблон accordion у каталозі `resources/views/components`, а не вкладати його в каталог `accordion` разом з іншими пов'язаними шаблонами.

На щастя, Blade дозволяє розмістити файл, ім'я якого збігається з іменем каталогу компонента, усередині самого цього каталогу. Коли такий шаблон існує, його можна рендерити як «кореневий» елемент компонента, навіть якщо він вкладений у каталог. Тож ми можемо й далі використовувати той самий синтаксис Blade, наведений у прикладі вище, але змінимо структуру каталогів так:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### Властивості даних та атрибути

Оскільки анонімні компоненти не мають пов'язаного класу, ви можете замислитися, як розрізнити, які дані слід передавати компоненту як змінні, а які атрибути мають потрапити до [набору атрибутів](#component-attributes) компонента.

Ви можете вказати, які атрибути слід вважати змінними даних, директивою `@props` на початку шаблону вашого компонента. Усі інші атрибути компонента будуть доступні через набір атрибутів. Якщо ви хочете задати змінній даних типове значення, вкажіть ім'я змінної як ключ масиву, а типове значення - як значення:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

З наведеним вище визначенням компонента ми можемо відрендерити його так:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### Доступ до даних батьківського компонента

Іноді вам може знадобитися звернутися до даних батьківського компонента всередині дочірнього. У таких випадках скористайтеся директивою `@aware`. Наприклад, уявімо, що ми створюємо складний компонент меню, який складається з батьківського `<x-menu>` і дочірнього `<x-menu.item>`:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

Компонент `<x-menu>` може мати таку реалізацію:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

Оскільки проп `color` було передано лише батьківському компоненту (`<x-menu>`), він не буде доступний усередині `<x-menu.item>`. Однак якщо ми скористаємося директивою `@aware`, ми можемо зробити його доступним і там:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> Директива `@aware` не може звертатися до даних батька, які не передано батьківському компоненту явно через HTML-атрибути. Типові значення `@props`, не передані батьківському компоненту явно, недоступні директиві `@aware`.

<a name="anonymous-component-paths"></a>
### Шляхи анонімних компонентів

Як зазначалося раніше, анонімні компоненти зазвичай визначаються розміщенням шаблону Blade у каталозі `resources/views/components`. Утім, подекуди ви можете захотіти зареєструвати в Laravel інші шляхи анонімних компонентів на додачу до типового.

Метод `anonymousComponentPath` приймає «шлях» до розташування анонімних компонентів першим аргументом і необов'язковий «простір імен», під яким слід розміщувати компоненти, - другим. Зазвичай цей метод слід викликати з методу `boot` одного із [сервіс-провайдерів](/docs/{{version}}/providers) вашого застосунку:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

Коли шляхи компонентів зареєстровано без указаного префікса, як у прикладі вище, їх можна рендерити у ваших компонентах Blade теж без префікса. Наприклад, якщо за зареєстрованим вище шляхом існує компонент `panel.blade.php`, його можна відрендерити так:

```blade
<x-panel />
```

Префікси-«простори імен» можна передати другим аргументом методу `anonymousComponentPath`:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

Коли префікс указано, компоненти в цьому «просторі імен» рендеряться додаванням простору імен до імені компонента:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## Створення макетів

<a name="layouts-using-components"></a>
### Макети на компонентах

Більшість веб-застосунків мають однаковий загальний макет на різних сторінках. Було б неймовірно марудно й важко підтримувати застосунок, якби нам доводилося повторювати весь HTML макета в кожному створеному представленні. На щастя, зручно визначити цей макет як єдиний [компонент Blade](#components) і використовувати його в усьому застосунку.

<a name="defining-the-layout-component"></a>
#### Визначення компонента макета

Наприклад, уявімо, що ми створюємо застосунок зі списком справ. Ми можемо визначити компонент `layout`, який виглядає так:

```blade
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```

<a name="applying-the-layout-component"></a>
#### Застосування компонента макета

Щойно компонент `layout` визначено, ми можемо створити представлення Blade, що його використовує. У цьому прикладі ми визначимо просте представлення, яке показує наш список завдань:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

Пам'ятайте: вміст, вставлений у компонент, потрапить до типової змінної `$slot` усередині нашого компонента `layout`. Як ви могли помітити, наш `layout` також враховує слот `$title`, якщо його передано; інакше показується типовий заголовок. Ми можемо передати власний заголовок із представлення списку завдань, використовуючи стандартний синтаксис слотів, розглянутий у [документації з компонентів](#components):

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

Тепер, коли ми визначили макет і представлення списку завдань, залишається лише повернути представлення `task` із маршруту:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### Макети на успадкуванні шаблонів

<a name="defining-a-layout"></a>
#### Визначення макета

Макети можна також створювати через «успадкування шаблонів». Це був основний спосіб створення застосунків до появи [компонентів](#components).

Щоб почати, погляньмо на простий приклад. Спершу розглянемо макет сторінки. Оскільки більшість веб-застосунків мають однаковий загальний макет на різних сторінках, зручно визначити цей макет як єдине представлення Blade:

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

Як бачите, цей файл містить типову HTML-розмітку. Однак зверніть увагу на директиви `@section` і `@yield`. Директива `@section`, як випливає з назви, визначає секцію вмісту, а директива `@yield` слугує для виведення вмісту певної секції.

Тепер, коли ми визначили макет для нашого застосунку, визначмо дочірню сторінку, що успадковує цей макет.

<a name="extending-a-layout"></a>
#### Розширення макета

Визначаючи дочірнє представлення, скористайтеся директивою Blade `@extends`, щоб указати, який макет має «успадкувати» це представлення. Представлення, що розширюють макет Blade, можуть вставляти вміст у секції макета через директиви `@section`. Пам'ятайте: як показано в прикладі вище, вміст цих секцій буде показано в макеті через `@yield`:

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

У цьому прикладі секція `sidebar` використовує директиву `@@parent`, щоб додати вміст до бічної панелі макета, а не перезаписати його. Директиву `@@parent` буде замінено вмістом макета під час рендерингу представлення.

> [!NOTE]
> На відміну від попереднього прикладу, ця секція `sidebar` закінчується `@endsection`, а не `@show`. Директива `@endsection` лише визначає секцію, тоді як `@show` визначає і **одразу виводить** її.

Директива `@yield` також приймає типове значення другим параметром. Воно буде відрендерено, якщо секція, яку виводять, не визначена:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## Форми

<a name="csrf-field"></a>
### Поле CSRF

Щоразу, визначаючи HTML-форму у своєму застосунку, додавайте до неї приховане поле з CSRF-токеном, щоб `middleware` [захисту від CSRF](/docs/{{version}}/csrf) міг перевірити запит. Згенерувати поле з токеном можна директивою Blade `@csrf`:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### Поле методу

Оскільки HTML-форми не можуть робити запити `PUT`, `PATCH` чи `DELETE`, вам потрібно додати приховане поле `_method`, щоб підмінити ці HTTP-методи. Створити це поле за вас може директива Blade `@method`:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### Помилки валідації

Директива `@error` дозволяє швидко перевірити, чи існують [повідомлення про помилки валідації](/docs/{{version}}/validation#quick-displaying-the-validation-errors) для певного атрибута. Усередині директиви `@error` ви можете вивести змінну `$message`, щоб показати повідомлення про помилку:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

Оскільки директива `@error` компілюється в конструкцію «if», ви можете скористатися директивою `@else`, щоб відрендерити вміст, коли помилки для атрибута немає:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

Ви можете передати [ім'я конкретного набору помилок](/docs/{{version}}/validation#named-error-bags) другим параметром директиви `@error`, щоб отримати повідомлення про помилки валідації на сторінках із кількома формами:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror"
/>

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
## Стеки

Blade дозволяє додавати вміст до іменованих стеків, які можна відрендерити деінде - в іншому представленні чи макеті. Це особливо корисно, щоб указати JavaScript-бібліотеки, потрібні вашим дочірнім представленням:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

Якщо ви хочете додати вміст до стека, коли булевий вираз дає `true`, скористайтеся директивою `@pushIf`:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

Ви можете додавати до стека скільки завгодно разів. Щоб відрендерити повний вміст стека, передайте його ім'я директиві `@stack`:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

Якщо ви хочете додати вміст на початок стека, скористайтеся директивою `@prepend`:

```blade
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```

Директива `@hasstack` дозволяє визначити, чи стек порожній:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a name="service-injection"></a>
## Впровадження сервісів

Директива `@inject` дозволяє отримати сервіс із [сервіс-контейнера](/docs/{{version}}/container) Laravel. Перший аргумент, переданий `@inject`, - ім'я змінної, у яку буде поміщено сервіс, а другий - ім'я класу чи інтерфейсу сервісу, який ви хочете розв'язати:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## Рендеринг вбудованих шаблонів Blade

Іноді вам може знадобитися перетворити сирий рядок шаблону Blade на дійсний HTML. Це робиться методом `render` фасаду `Blade`. Метод `render` приймає рядок шаблону Blade і необов'язковий масив даних для шаблону:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel рендерить вбудовані шаблони Blade, записуючи їх у каталог `storage/framework/views`. Якщо ви хочете, щоб Laravel видаляв ці тимчасові файли після рендерингу, передайте методу аргумент `deleteCachedView`:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## Рендеринг фрагментів Blade

Використовуючи фронтенд-фреймворки на кшталт [Turbo](https://turbo.hotwired.dev/) чи [htmx](https://htmx.org/), ви можете подекуди потребувати повернення лише частини шаблону Blade у HTTP-відповіді. «Фрагменти» Blade дозволяють саме це. Щоб почати, розмістіть частину свого шаблону Blade між директивами `@fragment` та `@endfragment`:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

Далі, рендерячи представлення, що використовує цей шаблон, викличте метод `fragment`, щоб указати, що до вихідної HTTP-відповіді слід включити лише вказаний фрагмент:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

Метод `fragmentIf` дозволяє умовно повернути фрагмент представлення залежно від певної умови. Інакше буде повернуто все представлення:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

Методи `fragments` і `fragmentsIf` дозволяють повернути у відповіді кілька фрагментів представлення. Фрагменти буде з'єднано разом:

```php
view('dashboard', ['users' => $users])
    ->fragments(['user-list', 'comment-list']);

view('dashboard', ['users' => $users])
    ->fragmentsIf(
        $request->hasHeader('HX-Request'),
        ['user-list', 'comment-list']
    );
```

<a name="extending-blade"></a>
## Розширення Blade

Blade дозволяє визначати власні директиви методом `directive`. Коли компілятор Blade натрапляє на власну директиву, він викликає наданий колбек із виразом, який містить директива.

Наведений нижче приклад створює директиву `@datetime($var)`, яка форматує переданий `$var`, що має бути екземпляром `DateTime`:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

Як бачите, ми приєднаємо метод `format` до будь-якого виразу, переданого директиві. Тож у цьому прикладі кінцевий PHP, згенерований директивою, буде таким:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Після оновлення логіки директиви Blade вам потрібно буде видалити всі закешовані представлення Blade. Зробити це можна командою Artisan `view:clear`.

<a name="custom-echo-handlers"></a>
### Власні обробники виведення

Якщо ви спробуєте вивести об'єкт через Blade, буде викликано магічний метод `__toString` цього об'єкта. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) - один із вбудованих «магічних методів» PHP. Однак іноді ви не маєте контролю над методом `__toString` певного класу - наприклад, коли клас належить сторонній бібліотеці.

У таких випадках Blade дозволяє зареєструвати власний обробник виведення для конкретного типу об'єктів. Для цього викличте метод `stringable` у Blade. Метод `stringable` приймає замикання, яке має вказувати тип об'єкта, за рендеринг якого воно відповідає. Зазвичай метод `stringable` слід викликати в методі `boot` класу `AppServiceProvider` вашого застосунку:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

Щойно ваш обробник виведення визначено, ви можете просто вивести об'єкт у своєму шаблоні Blade:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### Власні умовні конструкції

Програмування власної директиви іноді складніше, ніж потрібно, коли йдеться про прості власні умовні конструкції. Тому Blade надає метод `Blade::if`, який дозволяє швидко визначати власні умовні директиви через замикання. Наприклад, визначмо власну умову, що перевіряє налаштований типовий «диск» застосунку. Зробимо це в методі `boot` нашого `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

Щойно власну умову визначено, ви можете використовувати її у своїх шаблонах:

```blade
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```

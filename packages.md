---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Розробка пакетів

- [Вступ](#introduction)
    - [Створення пакета](#creating-a-package)
    - [Кілька слів про фасади](#a-note-on-facades)
- [Виявлення пакетів](#package-discovery)
- [Сервіс-провайдери](#service-providers)
- [Ресурси](#resources)
    - [Конфігурація](#configuration)
    - [Маршрути](#routes)
    - [Міграції](#migrations)
    - [Мовні файли](#language-files)
    - [Представлення](#views)
    - [Компоненти представлень](#view-components)
    - [Команда Artisan «about»](#about-artisan-command)
- [Команди](#commands)
    - [Команди оптимізації](#optimize-commands)
    - [Команди перезавантаження](#reload-commands)
- [Публічні ресурси](#public-assets)
- [Публікація груп файлів](#publishing-file-groups)

<a name="introduction"></a>
## Вступ

Пакети - основний спосіб додавати функціональність до Laravel. Пакетом може бути будь-що: від чудового способу працювати з датами на кшталт [Carbon](https://github.com/briannesbitt/Carbon) до пакета, який дозволяє прив'язувати файли до моделей Eloquent, - як-от [Laravel Media Library](https://github.com/spatie/laravel-medialibrary) від Spatie.

Пакети бувають різних типів. Деякі з них самостійні, тобто працюють із будь-яким PHP-фреймворком. Carbon і Pest - приклади самостійних пакетів. Будь-який із них можна використовувати з Laravel, підключивши його у файлі `composer.json`.

Натомість інші пакети призначені саме для Laravel. Такі пакети можуть мати маршрути, контролери, представлення й конфігурацію, створені спеціально для розширення застосунку Laravel. Цей посібник насамперед описує розробку саме таких пакетів, специфічних для Laravel.

<a name="creating-a-package"></a>
### Створення пакета

Найпростіший спосіб почати створювати новий пакет для Laravel - офіційний [каркас пакета Laravel](https://github.com/laravel/package-skeleton). Каркас надає все потрібне для створення пакета Laravel: сервіс-провайдер, тестування через Pest, статичний аналіз через Larastan, форматування коду через Pint і застосунок-верстак для наскрізної розробки пакета. Створити новий пакет можна командою `package` з [CLI-інсталятора Laravel](/docs/{{version}}/installation#creating-a-laravel-project):

```shell
laravel package my-package
```

Інтерактивний скрипт конфігурації персоналізує каркас під ваш пакет, налаштувавши простір імен, сервіс-провайдер і лише ті можливості, які вам потрібні: файли конфігурації, маршрути, представлення, переклади, міграції, ресурси, команди та фасад.

<a name="a-note-on-facades"></a>
### Кілька слів про фасади

Пишучи застосунок Laravel, зазвичай не має значення, чи користуєтеся ви контрактами, чи фасадами, - обидва дають по суті однаковий рівень тестованості. Проте, коли ви пишете пакети, ваш пакет зазвичай не має доступу до всіх тестових хелперів Laravel. Якщо ви хочете писати тести пакета так, ніби пакет встановлено у звичайному застосунку Laravel, скористайтеся пакетом [Orchestral Testbench](https://github.com/orchestral/testbench).

<a name="package-discovery"></a>
## Виявлення пакетів

Файл `bootstrap/providers.php` застосунку Laravel містить список сервіс-провайдерів, які має завантажити Laravel. Проте, замість змушувати користувачів вручну додавати ваш сервіс-провайдер до списку, ви можете описати провайдер у секції `extra` файлу `composer.json` вашого пакета, і Laravel завантажить його автоматично. Окрім сервіс-провайдерів, ви можете перелічити й [фасади](/docs/{{version}}/facades), які хочете зареєструвати:

```json
"extra": {
    "laravel": {
        "providers": [
            "Barryvdh\\Debugbar\\ServiceProvider"
        ],
        "aliases": {
            "Debugbar": "Barryvdh\\Debugbar\\Facade"
        }
    }
},
```

Щойно ваш пакет налаштовано на виявлення, Laravel автоматично зареєструє його сервіс-провайдери та фасади під час встановлення, створюючи зручний досвід встановлення для користувачів вашого пакета.

<a name="opting-out-of-package-discovery"></a>
#### Відмова від виявлення пакетів

Якщо ви споживач пакета й хочете вимкнути виявлення для нього, перелічіть назву пакета в секції `extra` файлу `composer.json` вашого застосунку:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

Ви можете вимкнути виявлення для всіх пакетів, скориставшись символом `*` у директиві `dont-discover` вашого застосунку:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a name="service-providers"></a>
## Сервіс-провайдери

[Сервіс-провайдери](/docs/{{version}}/providers) - це точка з'єднання між вашим пакетом і Laravel. Сервіс-провайдер відповідає за прив'язку речей до [сервіс-контейнера](/docs/{{version}}/container) Laravel і за те, щоб повідомити Laravel, звідки завантажувати ресурси пакета: представлення, конфігурацію та мовні файли.

Сервіс-провайдер розширює клас `Illuminate\Support\ServiceProvider` і містить два методи: `register` та `boot`. Базовий клас `ServiceProvider` лежить у Composer-пакеті `illuminate/support`, який слід додати до залежностей вашого пакета. Щоб дізнатися більше про структуру й призначення сервіс-провайдерів, перегляньте [їхню документацію](/docs/{{version}}/providers).

<a name="resources"></a>
## Ресурси

<a name="configuration"></a>
### Конфігурація

Зазвичай вам знадобиться публікувати файл конфігурації вашого пакета до каталогу `config` застосунку. Це дозволить користувачам вашого пакета легко перевизначати ваші опції за замовчуванням. Щоб дозволити публікацію файлів конфігурації, викличте метод `publishes` у методі `boot` вашого сервіс-провайдера:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

Тепер, коли користувачі вашого пакета виконають команду Laravel `vendor:publish`, ваш файл буде скопійовано до вказаного місця публікації. Щойно конфігурацію опубліковано, до її значень можна звертатися як до будь-якого іншого файлу конфігурації:

```php
$value = config('courier.option');
```

> [!WARNING]
> Не описуйте замикань у файлах конфігурації. Їх не вдасться коректно серіалізувати, коли користувачі виконають команду Artisan `config:cache`.

<a name="default-package-configuration"></a>
#### Конфігурація пакета за замовчуванням

Ви також можете злити власний файл конфігурації пакета з опублікованою копією застосунку. Це дозволить вашим користувачам описувати в опублікованій копії лише ті опції, які вони справді хочуть перевизначити. Щоб злити значення файлу конфігурації, скористайтеся методом `mergeConfigFrom` у методі `register` вашого сервіс-провайдера.

Метод `mergeConfigFrom` приймає першим аргументом шлях до файлу конфігурації вашого пакета, а другим - ім'я копії файлу конфігурації в застосунку:

```php
/**
 * Register any package services.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]
> Цей метод зливає лише перший рівень масиву конфігурації. Якщо ваші користувачі частково опишуть багатовимірний масив конфігурації, відсутні опції не буде злито.

<a name="routes"></a>
### Маршрути

Якщо ваш пакет містить маршрути, завантажити їх можна методом `loadRoutesFrom`. Цей метод автоматично визначить, чи закешовані маршрути застосунку, і не завантажуватиме ваш файл маршрутів, якщо їх уже закешовано:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### Міграції

Якщо ваш пакет містить [міграції бази даних](/docs/{{version}}/migrations), скористайтеся методом `publishesMigrations`, щоб повідомити Laravel, що заданий каталог чи файл містить міграції. Публікуючи міграції, Laravel автоматично оновить мітку часу в їхніх іменах відповідно до поточних дати й часу:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishesMigrations([
        __DIR__.'/../database/migrations' => database_path('migrations'),
    ]);
}
```

<a name="language-files"></a>
### Мовні файли

Якщо ваш пакет містить [мовні файли](/docs/{{version}}/localization), скористайтеся методом `loadTranslationsFrom`, щоб повідомити Laravel, як їх завантажувати. Наприклад, якщо ваш пакет називається `courier`, додайте до методу `boot` вашого сервіс-провайдера таке:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

До рядків перекладу пакета звертаються за домовленістю `package::file.line`. Тож завантажити рядок `welcome` пакета `courier` із файлу `messages` можна так:

```php
echo trans('courier::messages.welcome');
```

Зареєструвати JSON-файли перекладів для вашого пакета можна методом `loadJsonTranslationsFrom`. Цей метод приймає шлях до каталогу, який містить JSON-файли перекладів вашого пакета:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### Публікація мовних файлів

Якщо ви хочете публікувати мовні файли вашого пакета до каталогу `lang/vendor` застосунку, скористайтеся методом `publishes` сервіс-провайдера. Метод `publishes` приймає масив шляхів пакета та бажаних місць публікації. Наприклад, щоб опублікувати мовні файли пакета `courier`, зробіть так:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

Тепер, коли користувачі вашого пакета виконають команду Artisan `vendor:publish`, мовні файли вашого пакета буде опубліковано до вказаного місця.

<a name="views"></a>
### Представлення

Щоб зареєструвати [представлення](/docs/{{version}}/views) вашого пакета в Laravel, вам потрібно вказати Laravel, де вони лежать. Це робиться методом `loadViewsFrom` сервіс-провайдера. Метод `loadViewsFrom` приймає два аргументи: шлях до ваших шаблонів представлень і назву вашого пакета. Наприклад, якщо ваш пакет називається `courier`, додайте до методу `boot` вашого сервіс-провайдера таке:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

До представлень пакета звертаються за домовленістю `package::view`. Тож, щойно шлях до представлень зареєстровано в сервіс-провайдері, ви можете завантажити представлення `dashboard` з пакета `courier` так:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### Перевизначення представлень пакета

Коли ви користуєтеся методом `loadViewsFrom`, Laravel насправді реєструє для ваших представлень два розташування: каталог `resources/views/vendor` застосунку й вказаний вами каталог. Тож, на прикладі пакета `courier`, Laravel спершу перевірить, чи розробник поклав власну версію представлення в каталог `resources/views/vendor/courier`. Далі, якщо представлення не змінювали, Laravel шукатиме в каталозі представлень пакета, який ви вказали у виклику `loadViewsFrom`. Це спрощує користувачам пакета налаштування / перевизначення ваших представлень.

<a name="publishing-views"></a>
#### Публікація представлень

Якщо ви хочете зробити свої представлення доступними для публікації до каталогу `resources/views/vendor` застосунку, скористайтеся методом `publishes` сервіс-провайдера. Метод `publishes` приймає масив шляхів до представлень пакета та бажаних місць публікації:

```php
/**
 * Bootstrap the package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

Тепер, коли користувачі вашого пакета виконають команду Artisan `vendor:publish`, представлення вашого пакета буде скопійовано до вказаного місця публікації.

<a name="view-components"></a>
### Компоненти представлень

Якщо ви створюєте пакет, який використовує компоненти Blade, або кладете компоненти в нетипові каталоги, вам доведеться вручну зареєструвати клас компонента та його HTML-аліас, щоб Laravel знав, де його шукати. Зазвичай компоненти реєструють у методі `boot` сервіс-провайдера вашого пакета:

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

Щойно ваш компонент зареєстровано, його можна відрендерити за його тегом-аліасом:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### Автозавантаження компонентів пакета

Як варіант, ви можете скористатися методом `componentNamespace`, щоб автозавантажувати класи компонентів за домовленістю. Наприклад, пакет `Nightshade` може мати компоненти `Calendar` і `ColorPicker`, які лежать у просторі імен `Nightshade\Views\Components`:

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

Це дозволить користуватися компонентами пакета за простором імен вендора через синтаксис `package-name::`:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade автоматично визначить клас, пов'язаний із цим компонентом, перетворивши назву компонента в PascalCase. Підкаталоги також підтримуються через «крапкову» нотацію.

<a name="anonymous-components"></a>
#### Анонімні компоненти

Якщо ваш пакет містить анонімні компоненти, їх слід класти в каталог `components` каталогу представлень вашого пакета (вказаного в [методі loadViewsFrom](#views)). Далі ви можете рендерити їх, додавши до назви компонента префікс простору імен представлень пакета:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### Команда Artisan «about»

Вбудована команда Artisan `about` дає стислий огляд середовища й конфігурації застосунку. Пакети можуть додавати до виводу цієї команди власну інформацію через клас `AboutCommand`. Зазвичай цю інформацію додають у методі `boot` сервіс-провайдера вашого пакета:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## Команди

Щоб зареєструвати команди Artisan вашого пакета в Laravel, скористайтеся методом `commands`. Цей метод очікує масив назв класів команд. Щойно команди зареєстровано, ви можете виконувати їх через [CLI Artisan](/docs/{{version}}/artisan):

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}
```

<a name="optimize-commands"></a>
### Команди оптимізації

[Команда optimize](/docs/{{version}}/deployment#optimization) Laravel кешує конфігурацію, події, маршрути та представлення застосунку. Методом `optimizes` ви можете зареєструвати власні команди Artisan вашого пакета, які слід викликати під час виконання команд `optimize` та `optimize:clear`:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->optimizes(
            optimize: 'package:optimize',
            clear: 'package:clear-optimizations',
        );
    }
}
```

<a name="reload-commands"></a>
### Команди перезавантаження

[Команда reload](/docs/{{version}}/deployment#reloading-services) Laravel зупиняє всі запущені сервіси, щоб системний монітор процесів автоматично їх перезапустив. Методом `reloads` ви можете зареєструвати власні команди Artisan вашого пакета, які слід викликати під час виконання команди `reload`:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->reloads('package:reload');
    }
}
```

<a name="public-assets"></a>
## Публічні ресурси

Ваш пакет може мати ресурси - JavaScript, CSS та зображення. Щоб опублікувати ці ресурси до каталогу `public` застосунку, скористайтеся методом `publishes` сервіс-провайдера. У цьому прикладі ми також додамо тег групи ресурсів `public`, який дозволяє легко публікувати групи пов'язаних ресурсів:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

Тепер, коли користувачі вашого пакета виконають команду `vendor:publish`, ваші ресурси буде скопійовано до вказаного місця публікації. Оскільки користувачам зазвичай доводиться перезаписувати ресурси щоразу під час оновлення пакета, вони можуть скористатися прапорцем `--force`:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## Публікація груп файлів

Вам може захотітися публікувати групи ресурсів пакета окремо. Наприклад, ви можете хотіти дозволити користувачам публікувати файли конфігурації вашого пакета, не змушуючи їх публікувати ресурси. Це робиться «тегуванням» під час виклику методу `publishes` із сервіс-провайдера пакета. Наприклад, скористаймося тегами, щоб описати дві групи публікації для пакета `courier` (`courier-config` та `courier-migrations`) у методі `boot` сервіс-провайдера пакета:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishesMigrations([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

Тепер ваші користувачі можуть публікувати ці групи окремо, вказавши їхній тег під час виконання команди `vendor:publish`:

```shell
php artisan vendor:publish --tag=courier-config
```

Ваші користувачі також можуть опублікувати всі публіковані файли, описані сервіс-провайдером вашого пакета, за допомогою прапорця `--provider`:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```

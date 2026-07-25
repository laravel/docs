---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Представлення

- [Вступ](#introduction)
    - [Написання представлень на React / Svelte / Vue](#writing-views-in-react-svelte-or-vue)
- [Створення та рендеринг представлень](#creating-and-rendering-views)
    - [Вкладені каталоги представлень](#nested-view-directories)
    - [Створення першого доступного представлення](#creating-the-first-available-view)
    - [Визначення наявності представлення](#determining-if-a-view-exists)
- [Передавання даних до представлень](#passing-data-to-views)
    - [Спільні дані для всіх представлень](#sharing-data-with-all-views)
- [Компоновники представлень](#view-composers)
    - [Творці представлень](#view-creators)
- [Оптимізація представлень](#optimizing-views)

<a name="introduction"></a>
## Вступ

Звісно, повертати цілі рядки HTML-документів безпосередньо з маршрутів і контролерів непрактично. На щастя, представлення дають зручний спосіб розмістити весь наш HTML в окремих файлах.

Представлення відокремлюють логіку контролера чи застосунку від логіки відображення і зберігаються в каталозі `resources/views`. У Laravel шаблони представлень зазвичай пишуть [мовою шаблонів Blade](/docs/{{version}}/blade). Просте представлення може виглядати так:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

Оскільки це представлення зберігається за шляхом `resources/views/greeting.blade.php`, ми можемо повернути його за допомогою глобального хелпера `view`:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Шукаєте докладнішу інформацію про написання шаблонів Blade? Перегляньте повну [документацію Blade](/docs/{{version}}/blade), щоб почати.

<a name="writing-views-in-react-svelte-or-vue"></a>
### Написання представлень на React / Svelte / Vue

Замість писати шаблони фронтенду на PHP через Blade, багато розробників почали віддавати перевагу React, Svelte чи Vue. Laravel робить це безболісним завдяки [Inertia](https://inertiajs.com/) - бібліотеці, яка легко пов'язує ваш фронтенд на React / Svelte / Vue із бекендом на Laravel без типових складнощів створення SPA.

Наші [стартові набори застосунків для React, Svelte і Vue](/docs/{{version}}/starter-kits) дають чудову відправну точку для вашого наступного застосунку Laravel на основі Inertia.

<a name="creating-and-rendering-views"></a>
## Створення та рендеринг представлень

Ви можете створити представлення, розмістивши файл із розширенням `.blade.php` у каталозі `resources/views` вашого застосунку або скориставшись командою Artisan `make:view`:

```shell
php artisan make:view greeting
```

Розширення `.blade.php` повідомляє фреймворку, що файл містить [шаблон Blade](/docs/{{version}}/blade). Шаблони Blade містять HTML, а також директиви Blade, які дозволяють легко виводити значення, створювати умови «if», ітерувати дані тощо.

Створивши представлення, ви можете повернути його з одного з маршрутів чи контролерів свого застосунку за допомогою глобального хелпера `view`:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

Представлення також можна повертати через фасад `View`:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

Як бачите, перший аргумент, переданий хелперу `view`, відповідає імені файлу представлення в каталозі `resources/views`. Другий аргумент - масив даних, які мають бути доступні представленню. У цьому випадку ми передаємо змінну `name`, яка виводиться в представленні за допомогою [синтаксису Blade](/docs/{{version}}/blade).

<a name="nested-view-directories"></a>
### Вкладені каталоги представлень

Представлення також можуть бути вкладені в підкаталоги каталогу `resources/views`. Для звернення до вкладених представлень можна використовувати «крапкову» нотацію. Наприклад, якщо ваше представлення зберігається за шляхом `resources/views/admin/profile.blade.php`, ви можете повернути його з маршруту чи контролера так:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> Імена каталогів представлень не повинні містити символ `.`.

<a name="creating-the-first-available-view"></a>
### Створення першого доступного представлення

За допомогою методу `first` фасаду `View` ви можете створити перше представлення, що існує в переданому масиві представлень. Це може бути корисно, якщо ваш застосунок чи пакет дозволяє налаштовувати або перевизначати представлення:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### Визначення наявності представлення

Якщо вам потрібно визначити, чи існує представлення, скористайтеся фасадом `View`. Метод `exists` поверне `true`, якщо представлення існує:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## Передавання даних до представлень

Як ви бачили в попередніх прикладах, ви можете передати представленню масив даних, щоб ці дані стали йому доступні:

```php
return view('greetings', ['name' => 'Victoria']);
```

Передаючи інформацію в такий спосіб, дані мають бути масивом пар «ключ - значення». Надавши дані представленню, ви можете звертатися до кожного значення в ньому за ключами - наприклад, `<?php echo $name; ?>`.

Як альтернативу передаванню повного масиву даних функції-хелперу `view`, ви можете скористатися методом `with`, щоб додавати до представлення окремі фрагменти даних. Метод `with` повертає екземпляр об'єкта представлення, тож ви можете продовжувати ланцюжок методів перед поверненням представлення:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### Спільні дані для всіх представлень

Подекуди вам може знадобитися надати дані всім представленням, які рендерить ваш застосунок. Це можна зробити методом `share` фасаду `View`. Зазвичай виклики `share` варто розміщувати в методі `boot` сервіс-провайдера. Ви вільні додати їх до класу `App\Providers\AppServiceProvider` або створити для цього окремий сервіс-провайдер:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

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
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
## Компоновники представлень

Компоновники представлень - це колбеки або методи класів, які викликаються під час рендерингу представлення. Якщо у вас є дані, які потрібно прив'язувати до представлення щоразу, коли воно рендериться, компоновник допоможе зібрати цю логіку в одному місці. Компоновники особливо корисні, коли те саме представлення повертають кілька маршрутів чи контролерів вашого застосунку і йому завжди потрібен певний фрагмент даних.

Зазвичай компоновники представлень реєструються в одному із [сервіс-провайдерів](/docs/{{version}}/providers) вашого застосунку. У цьому прикладі ми припустимо, що цю логіку міститиме `App\Providers\AppServiceProvider`.

Ми скористаємося методом `composer` фасаду `View`, щоб зареєструвати компоновник. Laravel не має типового каталогу для компоновників на основі класів, тож ви вільні організувати їх як завгодно. Наприклад, ви можете створити каталог `app/View/Composers` для всіх компоновників вашого застосунку:

```php
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

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
        // Using class-based composers...
        Facades\View::composer('profile', ProfileComposer::class);

        // Using closure-based composers...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

Тепер, коли ми зареєстрували компоновник, метод `compose` класу `App\View\Composers\ProfileComposer` виконуватиметься щоразу, коли рендериться представлення `profile`. Погляньмо на приклад класу компоновника:

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * Create a new profile composer.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * Bind data to the view.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

Як бачите, усі компоновники представлень розв'язуються через [сервіс-контейнер](/docs/{{version}}/container), тож ви можете вказати типи будь-яких потрібних залежностей у конструкторі компоновника.

<a name="attaching-a-composer-to-multiple-views"></a>
#### Прикріплення компоновника до кількох представлень

Ви можете прикріпити компоновник одразу до кількох представлень, передавши масив представлень першим аргументом методу `composer`:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

Метод `composer` також приймає символ `*` як шаблон, що дозволяє прикріпити компоновник до всіх представлень:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### Творці представлень

«Творці» представлень дуже схожі на компоновників, однак виконуються одразу після створення екземпляра представлення, а не чекають моменту рендерингу. Щоб зареєструвати творця представлення, скористайтеся методом `creator`:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## Оптимізація представлень

За замовчуванням представлення на шаблонах Blade компілюються на вимогу. Коли виконується запит, що рендерить представлення, Laravel визначає, чи існує скомпільована версія. Якщо файл існує, Laravel перевіряє, чи змінювалося нескомпільоване представлення пізніше за скомпільоване. Якщо скомпільованого представлення немає або нескомпільоване було змінено, Laravel перекомпілює його.

Компіляція представлень під час запиту може трохи негативно вплинути на швидкодію, тож Laravel надає команду Artisan `view:cache` для попередньої компіляції всіх представлень, які використовує ваш застосунок. Задля кращої швидкодії варто виконувати цю команду як частину процесу розгортання:

```shell
php artisan view:cache
```

Щоб очистити кеш представлень, скористайтеся командою `view:clear`:

```shell
php artisan view:clear
```

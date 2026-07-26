---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# База даних: пагінація

- [Вступ](#introduction)
- [Базове використання](#basic-usage)
    - [Пагінація результатів конструктора запитів](#paginating-query-builder-results)
    - [Пагінація результатів Eloquent](#paginating-eloquent-results)
    - [Курсорна пагінація](#cursor-pagination)
    - [Створення пагінатора вручну](#manually-creating-a-paginator)
    - [Налаштування URL пагінації](#customizing-pagination-urls)
- [Відображення результатів пагінації](#displaying-pagination-results)
    - [Налаштування вікна посилань пагінації](#adjusting-the-pagination-link-window)
    - [Перетворення результатів на JSON](#converting-results-to-json)
- [Налаштування представлення пагінації](#customizing-the-pagination-view)
    - [Використання Bootstrap](#using-bootstrap)
- [Методи екземплярів Paginator і LengthAwarePaginator](#paginator-instance-methods)
- [Методи екземпляра курсорного пагінатора](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## Вступ

В інших фреймворках пагінація буває справжньою мукою. Сподіваємося, підхід Laravel стане для вас ковтком свіжого повітря. Пагінатор Laravel інтегрований із [конструктором запитів](/docs/{{version}}/queries) та [Eloquent ORM](/docs/{{version}}/eloquent) і дає зручну, просту пагінацію записів бази даних без жодних налаштувань.

За замовчуванням HTML, який генерує пагінатор, сумісний із [фреймворком Tailwind CSS](https://tailwindcss.com/); втім, доступна й підтримка пагінації Bootstrap.

<a name="tailwind"></a>
#### Tailwind

Якщо ви користуєтеся стандартними представленнями пагінації Laravel для Tailwind разом із Tailwind 4.x, файл `resources/css/app.css` вашого застосунку вже буде правильно налаштований на `@source` для представлень пагінації Laravel:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## Базове використання

<a name="paginating-query-builder-results"></a>
### Пагінація результатів конструктора запитів

Розбити елементи на сторінки можна кількома способами. Найпростіший - метод `paginate` [конструктора запитів](/docs/{{version}}/queries) або [запиту Eloquent](/docs/{{version}}/eloquent). Метод `paginate` сам подбає про «limit» і «offset» запиту відповідно до сторінки, яку зараз переглядає користувач. За замовчуванням поточна сторінка визначається за значенням параметра `page` у рядку запиту HTTP-запиту. Laravel визначає це значення автоматично й так само автоматично підставляє його в посилання, які генерує пагінатор.

У цьому прикладі методу `paginate` передається єдиний аргумент - кількість елементів, які ви хочете показувати «на сторінці». Задаймо `15` елементів на сторінку:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show all application users.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a name="simple-pagination"></a>
#### Проста пагінація

Перш ніж дістати записи з бази даних, метод `paginate` рахує загальну кількість записів, що відповідають запиту. Це потрібно, щоб пагінатор знав, скільки всього сторінок. Але якщо ви не збираєтеся показувати загальну кількість сторінок в інтерфейсі застосунку, цей підрахунок зайвий.

Тож коли вам потрібні лише прості посилання «Далі» й «Назад», скористайтеся методом `simplePaginate` - він виконає один ефективний запит:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Пагінація результатів Eloquent

Ви також можете розбивати на сторінки запити [Eloquent](/docs/{{version}}/eloquent). У цьому прикладі ми розіб'ємо на сторінки модель `App\Models\User` по 15 записів на сторінку. Як бачите, синтаксис майже не відрізняється від пагінації результатів конструктора запитів:

```php
use App\Models\User;

$users = User::paginate(15);
```

Звісно, метод `paginate` можна викликати після того, як ви задали інші обмеження запиту - наприклад, умови `where`:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Для моделей Eloquent так само доступний метод `simplePaginate`:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

Аналогічно, для курсорної пагінації моделей Eloquent є метод `cursorPaginate`:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### Кілька екземплярів пагінатора на сторінці

Іноді вам потрібно вивести два окремі пагінатори на одному екрані. Але якщо обидва екземпляри зберігають поточну сторінку в параметрі `page` рядка запиту, вони конфліктуватимуть. Щоб вирішити цей конфлікт, передайте назву параметра рядка запиту, у якому зберігатиметься поточна сторінка пагінатора, третім аргументом методів `paginate`, `simplePaginate` і `cursorPaginate`:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### Курсорна пагінація

Якщо `paginate` і `simplePaginate` будують запити з SQL-виразом «offset», то курсорна пагінація створює умови «where», які порівнюють значення стовпців сортування із запиту. Це дає найкращу продуктивність бази даних з-поміж усіх методів пагінації Laravel. Такий спосіб особливо доречний для великих наборів даних і «нескінченного» прокручування в інтерфейсі.

На відміну від пагінації за зміщенням, яка додає номер сторінки до рядка запиту згенерованих URL, курсорна пагінація кладе в рядок запиту рядок-«курсор». Курсор - це закодований рядок, у якому міститься позиція, з якої наступний запит має продовжити пагінацію, і напрямок руху:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

Створити екземпляр курсорного пагінатора можна методом `cursorPaginate` конструктора запитів. Він повертає екземпляр `Illuminate\Pagination\CursorPaginator`:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

Отримавши екземпляр курсорного пагінатора, ви можете [відобразити результати пагінації](#displaying-pagination-results) так само, як робите це з `paginate` і `simplePaginate`. Докладніше про методи екземпляра курсорного пагінатора читайте в [документації з методів курсорного пагінатора](#cursor-paginator-instance-methods).

> [!WARNING]
> Щоб скористатися курсорною пагінацією, ваш запит обов'язково має містити вираз «order by». Крім того, стовпці, за якими сортується запит, мають належати таблиці, яку ви розбиваєте на сторінки.

<a name="cursor-vs-offset-pagination"></a>
#### Курсорна пагінація проти пагінації за зміщенням

Щоб проілюструвати різницю між пагінацією за зміщенням і курсорною, погляньмо на приклади SQL-запитів. Обидва наведені нижче запити покажуть «другу сторінку» результатів таблиці `users`, відсортованої за `id`:

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

Запит із курсорною пагінацією має такі переваги перед пагінацією за зміщенням:

- На великих наборах даних курсорна пагінація працює швидше, якщо стовпці з «order by» проіндексовані. Причина в тому, що вираз «offset» сканує всі раніше відібрані дані.
- На даних із частими записами пагінація за зміщенням може пропускати записи чи показувати дублікати, якщо на сторінку, яку зараз переглядає користувач, нещодавно щось додали або з неї щось видалили.

Втім, курсорна пагінація має такі обмеження:

- Як і `simplePaginate`, курсорна пагінація придатна лише для посилань «Далі» й «Назад» і не вміє генерувати посилання з номерами сторінок.
- Вона вимагає, щоб сортування спиралося щонайменше на один унікальний стовпець або на комбінацію унікальних стовпців. Стовпці зі значеннями `null` не підтримуються.
- Вирази запитів у «order by» підтримуються лише тоді, коли вони мають псевдонім і додані також до виразу «select».
- Вирази запитів із параметрами не підтримуються.

<a name="manually-creating-a-paginator"></a>
### Створення пагінатора вручну

Іноді вам може знадобитися створити пагінатор вручну, передавши йому масив елементів, які вже є в пам'яті. Залежно від потреби, створіть екземпляр `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator` або `Illuminate\Pagination\CursorPaginator`.

Класам `Paginator` і `CursorPaginator` не потрібно знати загальну кількість елементів у наборі результатів; саме тому вони й не мають методів для отримання індексу останньої сторінки. `LengthAwarePaginator` приймає майже ті самі аргументи, що й `Paginator`, але додатково вимагає загальну кількість елементів у наборі результатів.

Іншими словами, `Paginator` відповідає методу `simplePaginate` конструктора запитів, `CursorPaginator` - методу `cursorPaginate`, а `LengthAwarePaginator` - методу `paginate`.

> [!WARNING]
> Створюючи пагінатор вручну, ви маєте самі «нарізати» масив результатів, який передаєте пагінатору. Якщо не певні, як це зробити, погляньте на PHP-функцію [array_slice](https://secure.php.net/manual/en/function.array-slice.php).

<a name="customizing-pagination-urls"></a>
### Налаштування URL пагінації

За замовчуванням посилання, які генерує пагінатор, збігаються з URI поточного запиту. Втім, метод `withPath` дозволяє задати власний URI для генерації посилань. Наприклад, якщо ви хочете, щоб пагінатор генерував посилання на кшталт `http://example.com/admin/users?page=N`, передайте `/admin/users` до методу `withPath`:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### Додавання значень до рядка запиту

Ви можете додавати значення до рядка запиту посилань пагінації методом `appends`. Наприклад, щоб додати `sort=votes` до кожного посилання, викличте `appends` так:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

Якщо ви хочете додати до посилань пагінації всі значення рядка запиту з поточного HTTP-запиту, скористайтеся методом `withQueryString`:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### Додавання хеш-фрагментів

Якщо до згенерованих пагінатором URL потрібно додати «хеш-фрагмент», скористайтеся методом `fragment`. Наприклад, щоб додати `#users` у кінець кожного посилання пагінації, викличте метод `fragment` так:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## Відображення результатів пагінації

Метод `paginate` повертає екземпляр `Illuminate\Pagination\LengthAwarePaginator`, метод `simplePaginate` - екземпляр `Illuminate\Pagination\Paginator`, а метод `cursorPaginate` - екземпляр `Illuminate\Pagination\CursorPaginator`.

Ці об'єкти мають кілька методів, які описують набір результатів. Крім цих допоміжних методів, екземпляри пагінатора є ітераторами, тож їх можна обходити в циклі як масив. Отже, отримавши результати, ви можете вивести їх і відрендерити посилання на сторінки за допомогою [Blade](/docs/{{version}}/blade):

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

Метод `links` рендерить посилання на решту сторінок набору результатів. Кожне з цих посилань уже містить потрібну змінну `page` у рядку запиту. Пам'ятайте: HTML, який генерує метод `links`, сумісний із [фреймворком Tailwind CSS](https://tailwindcss.com).

<a name="adjusting-the-pagination-link-window"></a>
### Налаштування вікна посилань пагінації

Коли пагінатор виводить посилання, він показує номер поточної сторінки, а також посилання на три сторінки до та після неї. Методом `onEachSide` ви можете керувати тим, скільки додаткових посилань показувати з кожного боку від поточної сторінки в середньому рухомому вікні посилань:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### Перетворення результатів на JSON

Класи пагінаторів Laravel реалізують контракт `Illuminate\Contracts\Support\Jsonable` і мають метод `toJson`, тож перетворити результати пагінації на JSON дуже просто. Ви також можете отримати JSON, просто повернувши екземпляр пагінатора з маршруту чи дії контролера:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

JSON від пагінатора міститиме метаінформацію: `total`, `current_page`, `last_page` та інше. Самі записи результатів доступні за ключем `data`. Ось приклад JSON, який утворюється, коли з маршруту повертають екземпляр пагінатора:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "current_page_url": "http://laravel.app?page=1",
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## Налаштування представлення пагінації

За замовчуванням представлення, які рендерять посилання пагінації, сумісні з фреймворком [Tailwind CSS](https://tailwindcss.com). Втім, якщо ви не користуєтеся Tailwind, ви вільні описати власні представлення для цих посилань. Викликаючи метод `links` на екземплярі пагінатора, передайте назву представлення першим аргументом:

```blade
{{ $paginator->links('view.name') }}

<!-- Passing additional data to the view... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

Проте найпростіший спосіб налаштувати представлення пагінації - експортувати їх до каталогу `resources/views/vendor` командою `vendor:publish`:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

Ця команда покладе представлення до каталогу `resources/views/vendor/pagination` вашого застосунку. Файл `tailwind.blade.php` у цьому каталозі відповідає представленню пагінації за замовчуванням. Відредагуйте цей файл, щоб змінити HTML пагінації.

Якщо ви хочете призначити представленням пагінації за замовчуванням інший файл, викличте методи `defaultView` і `defaultSimpleView` пагінатора в методі `boot` класу `App\Providers\AppServiceProvider`:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### Використання Bootstrap

Laravel містить представлення пагінації, побудовані на [Bootstrap CSS](https://getbootstrap.com/). Щоб використати їх замість стандартних представлень Tailwind, викличте методи пагінатора `useBootstrapFour` або `useBootstrapFive` у методі `boot` класу `App\Providers\AppServiceProvider`:

```php
use Illuminate\Pagination\Paginator;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Методи екземплярів Paginator / LengthAwarePaginator

Кожен екземпляр пагінатора надає додаткову інформацію про пагінацію через такі методи:

<div class="overflow-auto">

| Метод                                   | Опис                                                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `$paginator->count()`                   | Отримати кількість елементів на поточній сторінці.                                                            |
| `$paginator->currentPage()`             | Отримати номер поточної сторінки.                                                                            |
| `$paginator->firstItem()`               | Отримати порядковий номер першого елемента в результатах.                                                    |
| `$paginator->getOptions()`              | Отримати опції пагінатора.                                                                                   |
| `$paginator->getUrlRange($start, $end)` | Створити діапазон URL пагінації.                                                                             |
| `$paginator->hasPages()`                | Визначити, чи достатньо елементів, щоб розбити їх на кілька сторінок.                                         |
| `$paginator->hasMorePages()`            | Визначити, чи є ще елементи у сховищі даних.                                                                 |
| `$paginator->items()`                   | Отримати елементи поточної сторінки.                                                                         |
| `$paginator->lastItem()`                | Отримати порядковий номер останнього елемента в результатах.                                                 |
| `$paginator->lastPage()`                | Отримати номер останньої доступної сторінки. (Недоступний із `simplePaginate`).                              |
| `$paginator->nextPageUrl()`             | Отримати URL наступної сторінки.                                                                             |
| `$paginator->onFirstPage()`             | Визначити, чи пагінатор перебуває на першій сторінці.                                                        |
| `$paginator->onLastPage()`              | Визначити, чи пагінатор перебуває на останній сторінці.                                                      |
| `$paginator->perPage()`                 | Кількість елементів, які показуються на сторінці.                                                            |
| `$paginator->previousPageUrl()`         | Отримати URL попередньої сторінки.                                                                           |
| `$paginator->total()`                   | Визначити загальну кількість відповідних елементів у сховищі даних. (Недоступний із `simplePaginate`).        |
| `$paginator->url($page)`                | Отримати URL для заданого номера сторінки.                                                                   |
| `$paginator->getPageName()`             | Отримати змінну рядка запиту, у якій зберігається сторінка.                                                  |
| `$paginator->setPageName($name)`        | Задати змінну рядка запиту, у якій зберігається сторінка.                                                    |
| `$paginator->through($callback)`        | Перетворити кожен елемент за допомогою колбека.                                                              |

</div>

<a name="cursor-paginator-instance-methods"></a>
## Методи екземпляра курсорного пагінатора

Кожен екземпляр курсорного пагінатора надає додаткову інформацію про пагінацію через такі методи:

<div class="overflow-auto">

| Метод                           | Опис                                                                 |
| ------------------------------- | ----------------------------------------------------------------- |
| `$paginator->count()`           | Отримати кількість елементів на поточній сторінці.                  |
| `$paginator->cursor()`          | Отримати поточний екземпляр курсора.                                |
| `$paginator->getOptions()`      | Отримати опції пагінатора.                                          |
| `$paginator->hasPages()`        | Визначити, чи достатньо елементів, щоб розбити їх на кілька сторінок. |
| `$paginator->hasMorePages()`    | Визначити, чи є ще елементи у сховищі даних.                        |
| `$paginator->getCursorName()`   | Отримати змінну рядка запиту, у якій зберігається курсор.           |
| `$paginator->items()`           | Отримати елементи поточної сторінки.                                |
| `$paginator->nextCursor()`      | Отримати екземпляр курсора для наступного набору елементів.         |
| `$paginator->nextPageUrl()`     | Отримати URL наступної сторінки.                                    |
| `$paginator->onFirstPage()`     | Визначити, чи пагінатор перебуває на першій сторінці.               |
| `$paginator->onLastPage()`      | Визначити, чи пагінатор перебуває на останній сторінці.             |
| `$paginator->perPage()`         | Кількість елементів, які показуються на сторінці.                   |
| `$paginator->previousCursor()`  | Отримати екземпляр курсора для попереднього набору елементів.       |
| `$paginator->previousPageUrl()` | Отримати URL попередньої сторінки.                                  |
| `$paginator->setCursorName()`   | Задати змінну рядка запиту, у якій зберігається курсор.             |
| `$paginator->url($cursor)`      | Отримати URL для заданого екземпляра курсора.                       |

</div>

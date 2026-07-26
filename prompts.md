---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Prompts

- [Вступ](#introduction)
- [Встановлення](#installation)
- [Доступні промпти](#available-prompts)
    - [Text](#text)
    - [Textarea](#textarea)
    - [Number](#number)
    - [Password](#password)
    - [Confirm](#confirm)
    - [Select](#select)
    - [Multi-select](#multiselect)
    - [Suggest](#suggest)
    - [Search](#search)
    - [Multi-search](#multisearch)
    - [Pause](#pause)
    - [Autocomplete](#autocomplete)
- [Перетворення вводу перед валідацією](#transforming-input-before-validation)
- [Форми](#forms)
- [Інформаційні повідомлення](#informational-messages)
- [Виноски](#callouts)
- [Таблиці](#tables)
- [Spin](#spin)
- [Індикатор прогресу](#progress)
- [Task](#task)
- [Stream](#stream)
- [Заголовок термінала](#terminal-title)
- [Очищення термінала](#clear)
- [Що врахувати щодо термінала](#terminal-considerations)
- [Непідтримувані середовища та запасні варіанти](#fallbacks)
- [Тестування](#testing)

<a name="introduction"></a>
## Вступ

[Laravel Prompts](https://github.com/laravel/prompts) - це PHP-пакет для додавання гарних і зручних форм до ваших консольних застосунків, з можливостями як у браузері - зокрема текстом-підказкою та валідацією.

<img src="https://laravel.com/img/docs/prompts-example.png">

Laravel Prompts чудово пасує для отримання вводу користувача у ваших [консольних командах Artisan](/docs/{{version}}/artisan#writing-commands), але його можна використовувати і в будь-якому консольному проєкті на PHP.

> [!NOTE]
> Laravel Prompts підтримує macOS, Linux і Windows із WSL. Докладніше читайте в нашій документації про [непідтримувані середовища та запасні варіанти](#fallbacks).

<a name="installation"></a>
## Встановлення

Laravel Prompts уже входить до останнього випуску Laravel.

Laravel Prompts можна також встановити в інші ваші проєкти на PHP через менеджер пакетів Composer:

```shell
composer require laravel/prompts
```

<a name="available-prompts"></a>
## Доступні промпти

<a name="text"></a>
### Text

Функція `text` поставить користувачеві задане запитання, прийме його ввід і поверне його:

```php
use function Laravel\Prompts\text;

$name = text('What is your name?');
```

Ви також можете додати текст-підказку, значення за замовчуванням та інформаційну підказку:

```php
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="text-required"></a>
#### Обов'язкові значення

Якщо ви вимагаєте, щоб значення було введено, передайте аргумент `required`:

```php
$name = text(
    label: 'What is your name?',
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$name = text(
    label: 'What is your name?',
    required: 'Your name is required.'
);
```

<a name="text-validation"></a>
#### Додаткова валідація

Нарешті, якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

Замикання отримає введене значення й може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

Або ж ви можете скористатися силою [валідатора](/docs/{{version}}/validation) Laravel. Для цього передайте в аргумент `validate` масив з іменем атрибута та потрібними правилами валідації:

```php
$name = text(
    label: 'What is your name?',
    validate: ['name' => 'required|max:255|unique:users']
);
```

<a name="textarea"></a>
### Textarea

Функція `textarea` поставить користувачеві задане запитання, прийме його ввід через багаторядкове поле й поверне його:

```php
use function Laravel\Prompts\textarea;

$story = textarea('Tell me a story.');
```

Ви також можете додати текст-підказку, значення за замовчуванням та інформаційну підказку:

```php
$story = textarea(
    label: 'Tell me a story.',
    placeholder: 'This is a story about...',
    hint: 'This will be displayed on your profile.'
);
```

<a name="textarea-required"></a>
#### Обов'язкові значення

Якщо ви вимагаєте, щоб значення було введено, передайте аргумент `required`:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$story = textarea(
    label: 'Tell me a story.',
    required: 'A story is required.'
);
```

<a name="textarea-validation"></a>
#### Додаткова валідація

Нарешті, якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: fn (string $value) => match (true) {
        strlen($value) < 250 => 'The story must be at least 250 characters.',
        strlen($value) > 10000 => 'The story must not exceed 10,000 characters.',
        default => null
    }
);
```

Замикання отримає введене значення й може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

Або ж ви можете скористатися силою [валідатора](/docs/{{version}}/validation) Laravel. Для цього передайте в аргумент `validate` масив з іменем атрибута та потрібними правилами валідації:

```php
$story = textarea(
    label: 'Tell me a story.',
    validate: ['story' => 'required|max:10000']
);
```

<a name="number"></a>
### Number

Функція `number` поставить користувачеві задане запитання, прийме його числовий ввід і поверне його. Функція `number` дозволяє користувачеві змінювати число клавішами зі стрілками вгору й вниз:

```php
use function Laravel\Prompts\number;

$number = number('How many copies would you like?');
```

Ви також можете додати текст-підказку, значення за замовчуванням та інформаційну підказку:

```php
$name = number(
    label: 'How many copies would you like?',
    placeholder: '5',
    default: 1,
    hint: 'This will be determine how many copies to create.'
);
```

<a name="number-required"></a>
#### Обов'язкові значення

Якщо ви вимагаєте, щоб значення було введено, передайте аргумент `required`:

```php
$copies = number(
    label: 'How many copies would you like?',
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$copies = number(
    label: 'How many copies would you like?',
    required: 'A number of copies is required.'
);
```

<a name="number-validation"></a>
#### Додаткова валідація

Нарешті, якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: fn (?int $value) => match (true) {
        $value < 1 => 'At least one copy is required.',
        $value > 100 => 'You may not create more than 100 copies.',
        default => null
    }
);
```

Замикання отримає введене значення й може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

Або ж ви можете скористатися силою [валідатора](/docs/{{version}}/validation) Laravel. Для цього передайте в аргумент `validate` масив з іменем атрибута та потрібними правилами валідації:

```php
$copies = number(
    label: 'How many copies would you like?',
    validate: ['copies' => 'required|integer|min:1|max:100']
);
```

<a name="password"></a>
### Password

Функція `password` схожа на функцію `text`, але ввід користувача маскується під час набору в консолі. Це стає в пригоді, коли ви запитуєте чутливу інформацію - як-от паролі:

```php
use function Laravel\Prompts\password;

$password = password('What is your password?');
```

Ви також можете додати текст-підказку та інформаційну підказку:

```php
$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.'
);
```

<a name="password-required"></a>
#### Обов'язкові значення

Якщо ви вимагаєте, щоб значення було введено, передайте аргумент `required`:

```php
$password = password(
    label: 'What is your password?',
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$password = password(
    label: 'What is your password?',
    required: 'The password is required.'
);
```

<a name="password-validation"></a>
#### Додаткова валідація

Нарешті, якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$password = password(
    label: 'What is your password?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

Замикання отримає введене значення й може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

Або ж ви можете скористатися силою [валідатора](/docs/{{version}}/validation) Laravel. Для цього передайте в аргумент `validate` масив з іменем атрибута та потрібними правилами валідації:

```php
$password = password(
    label: 'What is your password?',
    validate: ['password' => 'min:8']
);
```

<a name="confirm"></a>
### Confirm

Якщо вам треба запитати в користувача підтвердження «так чи ні», скористайтеся функцією `confirm`. Користувачі можуть скористатися клавішами зі стрілками або натиснути `y` чи `n`, щоб обрати відповідь. Ця функція поверне `true` або `false`.

```php
use function Laravel\Prompts\confirm;

$confirmed = confirm('Do you accept the terms?');
```

Ви також можете додати значення за замовчуванням, власні написи для «Yes» і «No» та інформаційну підказку:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    default: false,
    yes: 'I accept',
    no: 'I decline',
    hint: 'The terms must be accepted to continue.'
);
```

<a name="confirm-required"></a>
#### Вимога відповіді «Yes»

За потреби ви можете зобов'язати користувачів обрати «Yes», передавши аргумент `required`:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: 'You must accept the terms to continue.'
);
```

<a name="select"></a>
### Select

Якщо вам потрібно, щоб користувач обрав із наперед визначеного набору варіантів, скористайтеся функцією `select`:

```php
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);
```

Ви також можете вказати варіант за замовчуванням та інформаційну підказку:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    default: 'Owner',
    hint: 'The role may be changed at any time.'
);
```

Ви також можете передати в аргумент `options` асоціативний масив, щоб повертався ключ обраного варіанта, а не його значення:

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    default: 'owner'
);
```

До п'яти варіантів буде показано, перш ніж список почне прокручуватися. Ви можете змінити це, передавши аргумент `scroll`:

```php
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="select-info"></a>
#### Додаткова інформація

Аргумент `info` дозволяє показувати додаткову інформацію про поточний підсвічений варіант. Якщо передати замикання, воно отримає значення підсвіченого варіанта й має повернути рядок або `null`:

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    info: fn (string $value) => match ($value) {
        'member' => 'Can view and comment.',
        'contributor' => 'Can view, comment, and edit.',
        'owner' => 'Full access to all resources.',
        default => null,
    }
);
```

Ви також можете передати в аргумент `info` статичний рядок, якщо інформація не залежить від підсвіченого варіанта:

```php
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner'],
    info: 'The role may be changed at any time.'
);
```

<a name="select-validation"></a>
#### Додаткова валідація

На відміну від інших функцій-промптів, функція `select` не приймає аргумент `required`, адже не обрати нічого неможливо. Проте ви можете передати замикання в аргумент `validate`, якщо вам треба показати варіант, але завадити його вибору:

```php
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    validate: fn (string $value) =>
        $value === 'owner' && User::where('role', 'owner')->exists()
            ? 'An owner already exists.'
            : null
);
```

Якщо аргумент `options` - асоціативний масив, замикання отримає обраний ключ, інакше - обране значення. Замикання може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

<a name="multiselect"></a>
### Multi-select

Якщо вам потрібно, щоб користувач міг обрати кілька варіантів, скористайтеся функцією `multiselect`:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete']
);
```

Ви також можете вказати варіанти за замовчуванням та інформаційну підказку:

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);
```

Ви також можете передати в аргумент `options` асоціативний масив, щоб повертати ключі обраних варіантів, а не їхні значення:

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    default: ['read', 'create']
);
```

До п'яти варіантів буде показано, перш ніж список почне прокручуватися. Ви можете змінити це, передавши аргумент `scroll`:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

<a name="multiselect-info"></a>
#### Додаткова інформація

Аргумент `info` дозволяє показувати додаткову інформацію про поточний підсвічений варіант. Якщо передати замикання, воно отримає значення підсвіченого варіанта й має повернути рядок або `null`:

```php
$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    info: fn (string $value) => match ($value) {
        'read' => 'View resources and their properties.',
        'create' => 'Create new resources.',
        'update' => 'Modify existing resources.',
        'delete' => 'Permanently remove resources.',
        default => null,
    }
);
```

<a name="multiselect-required"></a>
#### Вимога значення

За замовчуванням користувач може обрати нуль чи більше варіантів. Ви можете передати аргумент `required`, щоб вимагати щонайменше один:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок в аргумент `required`:

```php
$categories = multiselect(
    label: 'What categories should be assigned?',
    options: Category::pluck('name', 'id'),
    required: 'You must select at least one category'
);
```

<a name="multiselect-validation"></a>
#### Додаткова валідація

Ви можете передати замикання в аргумент `validate`, якщо вам треба показати варіант, але завадити його вибору:

```php
$permissions = multiselect(
    label: 'What permissions should the user have?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    validate: fn (array $values) => ! in_array('read', $values)
        ? 'All users require the read permission.'
        : null
);
```

Якщо аргумент `options` - асоціативний масив, замикання отримає обрані ключі, інакше - обрані значення. Замикання може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

<a name="suggest"></a>
### Suggest

Функція `suggest` дозволяє додати автодоповнення для можливих варіантів. Користувач і далі може ввести будь-яку відповідь, незалежно від підказок автодоповнення:

```php
use function Laravel\Prompts\suggest;

$name = suggest('What is your name?', ['Taylor', 'Dayle']);
```

Або ж ви можете передати замикання другим аргументом до функції `suggest`. Замикання викликатиметься щоразу, коли користувач вводить символ. Воно має приймати рядковий параметр із уже введеним текстом і повертати масив варіантів для автодоповнення:

```php
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
)
```

Ви також можете додати текст-підказку, значення за замовчуванням та інформаційну підказку:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    placeholder: 'E.g. Taylor',
    default: $user?->name,
    hint: 'This will be displayed on your profile.'
);
```

<a name="suggest-info"></a>
#### Додаткова інформація

Аргумент `info` дозволяє показувати додаткову інформацію про поточний підсвічений варіант. Якщо передати замикання, воно отримає значення підсвіченого варіанта й має повернути рядок або `null`:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    info: fn (string $value) => match ($value) {
        'Taylor' => 'Administrator',
        'Dayle' => 'Contributor',
        default => null,
    }
);
```

<a name="suggest-required"></a>
#### Обов'язкові значення

Якщо ви вимагаєте, щоб значення було введено, передайте аргумент `required`:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    required: 'Your name is required.'
);
```

<a name="suggest-validation"></a>
#### Додаткова валідація

Нарешті, якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

Замикання отримає введене значення й може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

Або ж ви можете скористатися силою [валідатора](/docs/{{version}}/validation) Laravel. Для цього передайте в аргумент `validate` масив з іменем атрибута та потрібними правилами валідації:

```php
$name = suggest(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle'],
    validate: ['name' => 'required|min:3|max:255']
);
```

<a name="search"></a>
### Search

Якщо у вас багато варіантів на вибір, функція `search` дозволяє користувачеві ввести пошуковий запит, щоб відфільтрувати результати, а вже потім обрати варіант клавішами зі стрілками:

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

Замикання отримає текст, уже введений користувачем, і має повернути масив варіантів. Якщо ви повернете асоціативний масив, буде повернено ключ обраного варіанта, інакше - його значення.

Фільтруючи масив, коли ви маєте намір повертати значення, скористайтеся функцією `array_values` або методом колекції `values`, щоб масив не став асоціативним:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

Ви також можете додати текст-підказку та інформаційну підказку:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

До п'яти варіантів буде показано, перш ніж список почне прокручуватися. Ви можете змінити це, передавши аргумент `scroll`:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="search-info"></a>
#### Додаткова інформація

Аргумент `info` дозволяє показувати додаткову інформацію про поточний підсвічений варіант. Якщо передати замикання, воно отримає значення підсвіченого варіанта й має повернути рядок або `null`:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    info: fn (int $userId) => User::find($userId)?->email
);
```

<a name="search-validation"></a>
#### Додаткова валідація

Якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$id = search(
    label: 'Search for the user that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (int|string $value) {
        $user = User::findOrFail($value);

        if ($user->opted_out) {
            return 'This user has opted-out of receiving mail.';
        }
    }
);
```

Якщо замикання `options` повертає асоціативний масив, замикання валідації отримає обраний ключ, інакше - обране значення. Замикання може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

<a name="multisearch"></a>
### Multi-search

Якщо у вас багато варіантів для пошуку й користувачеві треба обрати кілька, функція `multisearch` дозволяє ввести пошуковий запит, щоб відфільтрувати результати, а вже потім обрати варіанти клавішами зі стрілками й пробілом:

```php
use function Laravel\Prompts\multisearch;

$ids = multisearch(
    'Search for users who should receive the mail',
    fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : []
);
```

Замикання отримає текст, уже введений користувачем, і має повернути масив варіантів. Якщо ви повернете асоціативний масив, буде повернено ключі обраних варіантів; інакше - їхні значення.

Фільтруючи масив, коли ви маєте намір повертати значення, скористайтеся функцією `array_values` або методом колекції `values`, щоб масив не став асоціативним:

```php
$names = collect(['Taylor', 'Abigail']);

$selected = multisearch(
    label: 'Search for users who should receive the mail',
    options: fn (string $value) => $names
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
        ->values()
        ->all(),
);
```

Ви також можете додати текст-підказку та інформаційну підказку:

```php
$ids = multisearch(
    label: 'Search for users who should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.'
);
```

До п'яти варіантів буде показано, перш ніж список почне прокручуватися. Ви можете змінити це, передавши аргумент `scroll`:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    scroll: 10
);
```

<a name="multisearch-info"></a>
#### Додаткова інформація

Аргумент `info` дозволяє показувати додаткову інформацію про поточний підсвічений варіант. Якщо передати замикання, воно отримає значення підсвіченого варіанта й має повернути рядок або `null`:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    info: fn (int $userId) => User::find($userId)?->email
);
```

<a name="multisearch-required"></a>
#### Вимога значення

За замовчуванням користувач може обрати нуль чи більше варіантів. Ви можете передати аргумент `required`, щоб вимагати щонайменше один:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок в аргумент `required`:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    required: 'You must select at least one user.'
);
```

<a name="multisearch-validation"></a>
#### Додаткова валідація

Якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$ids = multisearch(
    label: 'Search for the users that should receive the mail',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    validate: function (array $values) {
        $optedOut = User::whereLike('name', '%a%')->findMany($values);

        if ($optedOut->isNotEmpty()) {
            return $optedOut->pluck('name')->join(', ', ', and ').' have opted out.';
        }
    }
);
```

Якщо замикання `options` повертає асоціативний масив, замикання валідації отримає обрані ключі; інакше - обрані значення. Замикання може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

<a name="pause"></a>
### Pause

Функція `pause` дозволяє показати користувачеві інформаційний текст і зачекати, доки він підтвердить бажання рухатися далі, натиснувши клавішу Enter / Return:

```php
use function Laravel\Prompts\pause;

pause('Press ENTER to continue.');
```

<a name="autocomplete"></a>
### Autocomplete

Функція `autocomplete` дозволяє додати вбудоване автодоповнення для можливих варіантів. Поки користувач набирає текст, підказки, що відповідають його вводу, з'являтимуться як примарний текст, який можна прийняти натисканням `Tab` чи стрілки вправо:

```php
use function Laravel\Prompts\autocomplete;

$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim']
);
```

Ви також можете додати текст-підказку, значення за замовчуванням та інформаційну підказку:

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    placeholder: 'E.g. Taylor',
    default: $user?->name,
    hint: 'Use tab to accept, up/down to cycle.'
);
```

<a name="autocomplete-closure"></a>
#### Динамічні варіанти

Ви також можете передати замикання, щоб динамічно генерувати варіанти за вводом користувача. Замикання викликатиметься щоразу, коли користувач вводить символ, і має повертати масив варіантів для автодоповнення:

```php
$file = autocomplete(
    label: 'Which file?',
    options: fn (string $value) => collect($files)
        ->filter(fn ($file) => str_starts_with(strtolower($file), strtolower($value)))
        ->values()
        ->all(),
);
```

<a name="autocomplete-required"></a>
#### Обов'язкові значення

Якщо ви вимагаєте, щоб значення було введено, передайте аргумент `required`:

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    required: true
);
```

Якщо ви хочете змінити повідомлення про помилку валідації, передайте рядок:

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    required: 'Your name is required.'
);
```

<a name="autocomplete-validation"></a>
#### Додаткова валідація

Нарешті, якщо ви хочете виконати додаткову логіку валідації, передайте замикання в аргумент `validate`:

```php
$name = autocomplete(
    label: 'What is your name?',
    options: ['Taylor', 'Dayle', 'Jess', 'Nuno', 'Tim'],
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

Замикання отримає введене значення й може повернути повідомлення про помилку або `null`, якщо валідація пройшла.

<a name="transforming-input-before-validation"></a>
## Перетворення вводу перед валідацією

Іноді вам може знадобитися перетворити ввід промпту, перш ніж відбудеться валідація. Наприклад, ви можете захотіти прибрати пробіли з переданих рядків. Для цього багато функцій-промптів надають аргумент `transform`, який приймає замикання:

```php
$name = text(
    label: 'What is your name?',
    transform: fn (string $value) => trim($value),
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

<a name="forms"></a>
## Форми

Часто у вас буде кілька промптів, які показуються послідовно, щоб зібрати інформацію перед подальшими діями. Ви можете скористатися функцією `form`, щоб створити згрупований набір промптів для заповнення:

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true)
    ->password('What is your password?', validate: ['password' => 'min:8'])
    ->confirm('Do you accept the terms?')
    ->submit();
```

Метод `submit` поверне масив із числовими індексами, що містить усі відповіді з промптів форми. Проте ви можете дати кожному промпту ім'я через аргумент `name`. Коли ім'я задано, до відповіді цього промпту можна звертатися за цим іменем:

```php
use App\Models\User;
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->password(
        label: 'What is your password?',
        validate: ['password' => 'min:8'],
        name: 'password'
    )
    ->confirm('Do you accept the terms?')
    ->submit();

User::create([
    'name' => $responses['name'],
    'password' => $responses['password'],
]);
```

Головна перевага функції `form` - можливість повернутися до попередніх промптів форми через `CTRL + U`. Це дозволяє користувачеві виправити помилки чи змінити вибір, не скасовуючи й не починаючи форму заново.

Якщо вам потрібен тонший контроль над промптом у формі, викличте метод `add` замість того, щоб напряму викликати одну з функцій-промптів. Методу `add` передаються всі попередні відповіді користувача:

```php
use function Laravel\Prompts\form;
use function Laravel\Prompts\outro;
use function Laravel\Prompts\text;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->add(function ($responses) {
        return text("How old are you, {$responses['name']}?");
    }, name: 'age')
    ->submit();

outro("Your name is {$responses['name']} and you are {$responses['age']} years old.");
```

<a name="informational-messages"></a>
## Інформаційні повідомлення

Функції `note`, `info`, `warning`, `error` та `alert` дозволяють показувати інформаційні повідомлення:

```php
use function Laravel\Prompts\info;

info('Package installed successfully.');
```

<a name="callouts"></a>
## Виноски

Функція `callout` показує повідомлення в рамці із заголовком і вмістом. Виноски стають у пригоді, щоб показати важливу інформацію, яка має вирізнятися, - як-от підсумки розгортання, деталі помилок чи оновлення статусу:

```php
use function Laravel\Prompts\callout;

callout(
    label: 'Environment Configured',
    content: 'Your application is running in production mode with 4 workers.',
);
```

Ви можете передати `warning` чи `error` в аргумент `type`, щоб змінити візуальний стиль виноски:

```php
callout(
    label: 'Deprecation Notice',
    content: 'The `--prefer-stable` flag will be removed in v4.0. Use `--stability=stable` instead.',
    type: 'warning',
);

callout(
    label: 'Database Connection Failed',
    content: 'Could not connect to MySQL on 127.0.0.1:3306.',
    type: 'error',
);
```

Аргумент `info` додає до виноски рядок-підвал, що стає в пригоді для показу метаданих на кшталт ID чи часових міток:

```php
callout(
    label: 'Deployment Summary',
    content: 'Your application was deployed to production.',
    info: 'deploy-id: d4f8a2c',
);
```

<a name="callout-rich-content"></a>
#### Насичений вміст

Замість рядка ви можете передати масив рядків та елементів, щоб побудувати насичені структуровані виноски. Клас `Element` надає фабричні методи для створення заголовків, марковані та нумеровані списки, списки «ключ - значення» та посилання:

```php
use Laravel\Prompts\Elements\Element;

use function Laravel\Prompts\callout;

callout('Deployment Summary', [
    'Your application was deployed to production at 2024-03-15 14:32 UTC.',
    Element::heading('What Changed'),
    Element::bulletedList([
        'Migrated 3 pending database migrations',
        'Cleared and rebuilt route cache',
        'Restarted 4 queue workers',
    ]),
    Element::heading('Next Steps'),
    Element::numberedList([
        'Verify the health check endpoint at /up',
        'Monitor error rates for the next 15 minutes',
        'Confirm background jobs are processing',
    ]),
]);
```

Ви також можете скористатися `Element::keyValueList`, щоб показати дані з підписами:

```php
callout('Database Connection Failed', [
    'Could not connect to the database server.',
    Element::keyValueList([
        'Host' => '127.0.0.1',
        'Port' => '3306',
        'Database' => 'forge',
        'Status' => 'Connection refused',
    ]),
], type: 'error');
```

Метод `Element::link` створює клікабельне гіперпосилання в терміналах, які підтримують [OSC 8](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda). Ви можете передати сам URL або URL із власним підписом:

```php
callout('Server Health Check', [
    'Multiple services are reporting degraded performance.',
    Element::heading('Affected Services'),
    'Look here: '.Element::link('https://example.com/health', 'Health Dashboard'),
    Element::link('https://example.com/health'),
]);
```

Якщо підпис не задано, як текст посилання буде показано сам URL.

<a name="tables"></a>
## Таблиці

Функція `table` дозволяє легко показати кілька рядків і стовпців даних. Усе, що вам треба, - передати імена стовпців і дані таблиці:

```php
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email'],
    rows: User::all(['name', 'email'])->toArray()
);
```

<a name="spin"></a>
## Spin

Функція `spin` показує спінер разом із необов'язковим повідомленням, доки виконується заданий колбек. Вона слугує індикатором тривалих процесів і повертає результати колбека після завершення:

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

> [!WARNING]
> Функція `spin` вимагає розширення PHP [PCNTL](https://www.php.net/manual/en/book.pcntl.php), щоб анімувати спінер. Коли це розширення недоступне, натомість з'явиться статична версія спінера.

<a name="progress"></a>
## Індикатори прогресу

Для тривалих завдань буває корисно показати індикатор прогресу, який повідомляє користувачам, наскільки завдання виконане. За допомогою функції `progress` Laravel покаже індикатор прогресу й просуватиме його на кожній ітерації по заданому ітерабельному значенню:

```php
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);
```

Функція `progress` працює як функція map і поверне масив із результатами кожної ітерації вашого колбека.

Колбек може також приймати екземпляр `Laravel\Prompts\Progress`, що дозволяє змінювати підпис і підказку на кожній ітерації:

```php
$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: function ($user, $progress) {
        $progress
            ->label("Updating {$user->name}")
            ->hint("Created on {$user->created_at}");

        return $this->performTask($user);
    },
    hint: 'This may take some time.'
);
```

Іноді вам може знадобитися ручніший контроль над просуванням індикатора. Спершу задайте загальну кількість кроків, які пройде процес. Далі просувайте індикатор методом `advance` після обробки кожного елемента:

```php
$progress = progress(label: 'Updating users', steps: 10);

$users = User::all();

$progress->start();

foreach ($users as $user) {
    $this->performTask($user);

    $progress->advance();
}

$progress->finish();
```

<a name="task"></a>
## Task

Функція `task` показує підписане завдання зі спінером і прокручуваною областю живого виводу, доки виконується заданий колбек. Вона ідеальна, щоб обгорнути тривалі процеси - як-от встановлення залежностей чи скрипти розгортання, - даючи змогу бачити в реальному часі, що відбувається:

```php
use function Laravel\Prompts\task;

task(
    label: 'Installing dependencies',
    callback: function ($logger) {
        // Long-running process...
    }
);
```

Колбек отримує екземпляр `Logger`, яким ви можете показувати рядки логу, повідомлення про статус і потоковий текст в області виводу завдання.

> [!WARNING]
> Функція `task` вимагає розширення PHP [PCNTL](https://www.php.net/manual/en/book.pcntl.php), щоб анімувати спінер. Коли це розширення недоступне, натомість з'явиться статична версія завдання.

<a name="task-logging"></a>
#### Запис рядків логу

Метод `line` пише один рядок логу до прокручуваної області виводу завдання:

```php
task(
    label: 'Installing dependencies',
    callback: function ($logger) {
        $logger->line('Resolving packages...');
        // ...
        $logger->line('Downloading laravel/framework');
        // ...
    }
);
```

<a name="task-status-messages"></a>
#### Повідомлення про статус

Ви можете скористатися методами `success`, `warning` та `error`, щоб показувати повідомлення про статус. Вони з'являються як стабільні підсвічені повідомлення над прокручуваною областю логу:

```php
task(
    label: 'Deploying application',
    callback: function ($logger) {
        $logger->line('Pulling latest changes...');
        // ...
        $logger->success('Changes pulled!');

        $logger->line('Running migrations...');
        // ...
        $logger->warning('No new migrations to run.');

        $logger->line('Clearing cache...');
        // ...
        $logger->success('Cache cleared!');
    }
);
```

<a name="task-label"></a>
#### Оновлення підпису

Метод `label` дозволяє оновлювати підпис завдання, доки воно виконується:

```php
task(
    label: 'Starting deployment...',
    callback: function ($logger) {
        $logger->label('Pulling latest changes...');
        // ...
        $logger->label('Running migrations...');
        // ...
        $logger->label('Clearing cache...');
        // ...
    }
);
```

<a name="task-sub-label"></a>
#### Показ підпідпису

Метод `subLabel` показує притлумлений рядок під головним підписом завдання, що стає в пригоді, щоб повідомляти тимчасовий статус - як-от крок, який виконується зараз. Передайте порожній рядок, щоб очистити підпідпис:

```php
task(
    label: 'Deploying',
    callback: function ($logger) {
        $logger->subLabel('Building assets...');
        // ...
        $logger->subLabel('Running migrations...');
        // ...
        $logger->subLabel('');
    }
);
```

Ви також можете задати початковий підпідпис через аргумент `subLabel`:

```php
task(
    label: 'Deploying',
    callback: function ($logger) {
        // ...
    },
    subLabel: 'Preparing...'
);
```

<a name="task-streaming"></a>
#### Потоковий текст

Для процесів, які видають вивід поступово - як-от згенеровані AI відповіді, - метод `partial` дозволяє транслювати текст слово за словом чи порція за порцією. Коли потік завершено, викличте `commitPartial`, щоб фіналізувати вивід:

```php
task(
    label: 'Generating response...',
    callback: function ($logger) {
        foreach ($words as $word) {
            $logger->partial($word . ' ');
        }

        $logger->commitPartial();
    }
);
```

<a name="task-limit"></a>
#### Налаштування ліміту виводу

За замовчуванням завдання показує до 10 рядків прокручуваного виводу. Ви можете змінити це через аргумент `limit`:

```php
task(
    label: 'Installing dependencies',
    callback: function ($logger) {
        // ...
    },
    limit: 20
);
```

<a name="task-keep-summary"></a>
#### Збереження підсумку

За замовчуванням вивід завдання стирається, щойно колбек завершується. Якщо ви хочете лишити повідомлення про статус на екрані після завершення завдання, передайте аргумент `keepSummary`:

```php
task(
    label: 'Deploying',
    callback: function ($logger) {
        $logger->success('Assets built');
        // ...
        $logger->success('Migrations complete');
    },
    keepSummary: true,
);
```

<a name="stream"></a>
## Stream

Функція `stream` показує текст, який транслюється в термінал, - ідеально для показу згенерованого AI вмісту чи будь-якого тексту, що надходить поступово:

```php
use function Laravel\Prompts\stream;

$stream = stream();

foreach ($words as $word) {
    $stream->append($word . ' ');
    usleep(25_000); // Simulate delay between chunks...
}

$stream->close();
```

Метод `append` додає текст до потоку, рендерячи його з ефектом поступової появи. Коли весь вміст передано, викличте метод `close`, щоб фіналізувати вивід і повернути курсор.

<a name="terminal-title"></a>
## Заголовок термінала

Функція `title` оновлює заголовок вікна чи вкладки термінала користувача:

```php
use function Laravel\Prompts\title;

title('Installing Dependencies');
```

Щоб скинути заголовок термінала до стандартного, передайте порожній рядок:

```php
title('');
```

<a name="clear"></a>
## Очищення термінала

Функція `clear` дозволяє очистити термінал користувача:

```php
use function Laravel\Prompts\clear;

clear();
```

<a name="terminal-considerations"></a>
## Що врахувати щодо термінала

<a name="terminal-width"></a>
#### Ширина термінала

Якщо довжина будь-якого підпису, варіанта чи повідомлення про помилку валідації перевищує кількість «стовпців» у терміналі користувача, її буде автоматично обрізано. Подумайте про скорочення цих рядків, якщо ваші користувачі можуть працювати у вузьких терміналах. Зазвичай безпечна максимальна довжина - 74 символи, щоб підтримати 80-символьний термінал.

<a name="terminal-height"></a>
#### Висота термінала

Для будь-яких промптів, що приймають аргумент `scroll`, задане значення буде автоматично зменшено під висоту термінала користувача - з урахуванням місця для повідомлення про помилку валідації.

<a name="fallbacks"></a>
## Непідтримувані середовища та запасні варіанти

Laravel Prompts підтримує macOS, Linux і Windows із WSL. Через обмеження Windows-версії PHP наразі неможливо користуватися Laravel Prompts у Windows поза WSL.

Тому Laravel Prompts підтримує запасний варіант з альтернативною реалізацією - як-от [Symfony Console Question Helper](https://symfony.com/doc/current/components/console/helpers/questionhelper.html).

> [!NOTE]
> Коли ви користуєтеся Laravel Prompts разом із фреймворком Laravel, запасні варіанти для кожного промпту вже налаштовані за вас і автоматично вмикатимуться в непідтримуваних середовищах.

<a name="fallback-conditions"></a>
#### Умови запасного варіанта

Якщо ви не користуєтеся Laravel або хочете налаштувати, коли саме застосовується запасна поведінка, передайте булеве значення статичному методу `fallbackWhen` класу `Prompt`:

```php
use Laravel\Prompts\Prompt;

Prompt::fallbackWhen(
    ! $input->isInteractive() || windows_os() || app()->runningUnitTests()
);
```

<a name="fallback-behavior"></a>
#### Запасна поведінка

Якщо ви не користуєтеся Laravel або хочете налаштувати запасну поведінку, передайте замикання статичному методу `fallbackUsing` кожного класу промпту:

```php
use Laravel\Prompts\TextPrompt;
use Symfony\Component\Console\Question\Question;
use Symfony\Component\Console\Style\SymfonyStyle;

TextPrompt::fallbackUsing(function (TextPrompt $prompt) use ($input, $output) {
    $question = (new Question($prompt->label, $prompt->default ?: null))
        ->setValidator(function ($answer) use ($prompt) {
            if ($prompt->required && $answer === null) {
                throw new \RuntimeException(
                    is_string($prompt->required) ? $prompt->required : 'Required.'
                );
            }

            if ($prompt->validate) {
                $error = ($prompt->validate)($answer ?? '');

                if ($error) {
                    throw new \RuntimeException($error);
                }
            }

            return $answer;
        });

    return (new SymfonyStyle($input, $output))
        ->askQuestion($question);
});
```

Запасні варіанти треба налаштовувати окремо для кожного класу промпту. Замикання отримає екземпляр класу промпту й має повернути тип, відповідний для цього промпту.

<a name="testing"></a>
## Тестування

Laravel надає різні методи, щоб перевірити, що ваша команда показує очікувані повідомлення Prompts:

```php tab=Pest
test('report generation', function () {
    $this->artisan('report:generate')
        ->expectsPromptsInfo('Welcome to the application!')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsAlert('Important notice!')
        ->expectsPromptsIntro('Starting process...')
        ->expectsPromptsOutro('Process completed!')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', 'taylor@example.com'],
                ['Jason Beggs', 'jason@example.com'],
            ]
        )
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
public function test_report_generation(): void
{
    $this->artisan('report:generate')
        ->expectsPromptsInfo('Welcome to the application!')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsAlert('Important notice!')
        ->expectsPromptsIntro('Starting process...')
        ->expectsPromptsOutro('Process completed!')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', 'taylor@example.com'],
                ['Jason Beggs', 'jason@example.com'],
            ]
        )
        ->assertExitCode(0);
}
```

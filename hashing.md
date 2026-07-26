---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Хешування

- [Вступ](#introduction)
- [Конфігурація](#configuration)
- [Базове використання](#basic-usage)
    - [Хешування паролів](#hashing-passwords)
    - [Перевірка відповідності пароля хешу](#verifying-that-a-password-matches-a-hash)
    - [Визначення потреби в перехешуванні пароля](#determining-if-a-password-needs-to-be-rehashed)
- [Перевірка алгоритму хешування](#hash-algorithm-verification)

<a name="introduction"></a>
## Вступ

[Фасад](/docs/{{version}}/facades) `Hash` у Laravel надає безпечне хешування Bcrypt та Argon2 для зберігання паролів користувачів. Якщо ви користуєтеся одним зі [стартових наборів застосунку Laravel](/docs/{{version}}/starter-kits), для реєстрації та автентифікації за замовчуванням використовуватиметься Bcrypt.

Bcrypt - чудовий вибір для хешування паролів, бо його «фактор складності» (work factor) можна регулювати: час генерування хешу можна збільшувати в міру зростання потужності обладнання. Коли йдеться про хешування паролів, повільно - це добре. Що довше алгоритм хешує пароль, то більше часу потрібно зловмисникам, щоб згенерувати «райдужні таблиці» з усіма можливими хешами рядків, які використовують в атаках перебором на застосунки.

<a name="configuration"></a>
## Конфігурація

За замовчуванням Laravel хешує дані драйвером `bcrypt`. Проте підтримуються й інші драйвери хешування, зокрема [argon](https://en.wikipedia.org/wiki/Argon2) та [argon2id](https://en.wikipedia.org/wiki/Argon2).

Драйвер хешування вашого застосунку можна вказати через змінну оточення `HASH_DRIVER`. Але якщо ви хочете налаштувати всі опції драйверів хешування Laravel, опублікуйте повний конфігураційний файл `hashing` артизан-командою `config:publish`:

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## Базове використання

<a name="hashing-passwords"></a>
### Хешування паролів

Захешувати пароль можна викликом методу `make` на фасаді `Hash`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * Update the password for the user.
     */
    public function update(Request $request): RedirectResponse
    {
        // Validate the new password length...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Налаштування фактора складності Bcrypt

Якщо ви користуєтеся алгоритмом Bcrypt, метод `make` дозволяє керувати фактором складності алгоритму через опцію `rounds`; проте значення за замовчуванням, яке підтримує Laravel, прийнятне для більшості застосунків:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Налаштування фактора складності Argon2

Якщо ви користуєтеся алгоритмом Argon2, метод `make` дозволяє керувати фактором складності алгоритму через опції `memory`, `time` та `threads`; проте значення за замовчуванням, які підтримує Laravel, прийнятні для більшості застосунків:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> Докладніше про ці опції читайте в [офіційній документації PHP щодо хешування Argon](https://secure.php.net/manual/en/function.password-hash.php).

<a name="verifying-that-a-password-matches-a-hash"></a>
### Перевірка відповідності пароля хешу

Метод `check`, який надає фасад `Hash`, дозволяє перевірити, чи відповідає заданий рядок відкритим текстом заданому хешу:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### Визначення потреби в перехешуванні пароля

Метод `needsRehash`, який надає фасад `Hash`, дозволяє визначити, чи змінився фактор складності хешувальника відтоді, як пароль було захешовано. Деякі застосунки виконують цю перевірку під час автентифікації:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## Перевірка алгоритму хешування

Щоб запобігти маніпуляціям з алгоритмом хешування, метод `Hash::check` у Laravel спершу перевіряє, чи було заданий хеш згенеровано обраним у застосунку алгоритмом хешування. Якщо алгоритми різні, буде кинуто виняток `RuntimeException`.

Саме такої поведінки очікують у більшості застосунків, де алгоритм хешування не має змінюватися, а інший алгоритм може свідчити про атаку зловмисника. Проте якщо вашому застосунку потрібно підтримувати кілька алгоритмів хешування - наприклад, під час переходу з одного алгоритму на інший, - ви можете вимкнути перевірку алгоритму, встановивши змінну оточення `HASH_VERIFY` у значення `false`:

```ini
HASH_VERIFY=false
```

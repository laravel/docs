---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Шифрування

- [Вступ](#introduction)
- [Конфігурація](#configuration)
    - [Плавна ротація ключів шифрування](#gracefully-rotating-encryption-keys)
- [Використання шифрувальника](#using-the-encrypter)

<a name="introduction"></a>
## Вступ

Сервіси шифрування Laravel надають простий і зручний інтерфейс для шифрування та розшифрування тексту через OpenSSL із використанням AES-256 та AES-128. Усі зашифровані Laravel значення підписуються кодом автентифікації повідомлення (MAC), тож після шифрування їхнє початкове значення не можна змінити чи підробити.

<a name="configuration"></a>
## Конфігурація

Перш ніж користуватися шифрувальником Laravel, ви маєте задати опцію конфігурації `key` у файлі `config/app.php`. Це значення береться зі змінної оточення `APP_KEY`. Згенерувати значення цієї змінної варто командою `php artisan key:generate`, адже команда `key:generate` використовує безпечний генератор випадкових байтів PHP і створює криптографічно стійкий ключ для вашого застосунку. Зазвичай значення змінної оточення `APP_KEY` генерується автоматично під час [встановлення Laravel](/docs/{{version}}/installation).

<a name="gracefully-rotating-encryption-keys"></a>
### Плавна ротація ключів шифрування

Якщо ви зміните ключ шифрування застосунку, усі автентифіковані сесії користувачів завершаться. Так стається тому, що Laravel шифрує кожен cookie, зокрема й сесійні. Крім того, стане неможливо розшифрувати будь-які дані, зашифровані попереднім ключем.

Щоб пом'якшити цю проблему, Laravel дозволяє перелічити ваші попередні ключі шифрування у змінній оточення `APP_PREVIOUS_KEYS`. Ця змінна може містити список усіх ваших попередніх ключів шифрування через кому:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

Коли ви задаєте цю змінну оточення, Laravel завжди шифруватиме значення «поточним» ключем. Проте під час розшифрування Laravel спершу спробує поточний ключ, а якщо з ним розшифрувати не вдасться - перебере всі попередні ключі, доки один із них не розшифрує значення.

Такий підхід до плавного розшифрування дозволяє користувачам працювати з вашим застосунком без перебоїв, навіть якщо ключ шифрування було змінено.

<a name="using-the-encrypter"></a>
## Використання шифрувальника

<a name="encrypting-a-value"></a>
#### Шифрування значення

Зашифрувати значення можна методом `encryptString`, який надає фасад `Crypt`. Усі значення шифруються через OpenSSL шифром AES-256-CBC. Крім того, всі зашифровані значення підписуються кодом автентифікації повідомлення (MAC). Вбудований код автентифікації повідомлення не дасть розшифрувати значення, які зловмисники намагалися підробити:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}
```

<a name="decrypting-a-value"></a>
#### Розшифрування значення

Розшифрувати значення можна методом `decryptString`, який надає фасад `Crypt`. Якщо значення не вдається коректно розшифрувати - наприклад, коли код автентифікації повідомлення недійсний, - буде кинуто виняток `Illuminate\Contracts\Encryption\DecryptException`:

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```

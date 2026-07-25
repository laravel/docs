---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Обмеження частоти

- [Вступ](#introduction)
    - [Конфігурація кешу](#cache-configuration)
- [Базове використання](#basic-usage)
    - [Ручне збільшення лічильника спроб](#manually-incrementing-attempts)
    - [Скидання спроб](#clearing-attempts)

<a name="introduction"></a>
## Вступ

Laravel містить просту абстракцію обмеження частоти, яка разом із [кешем](cache) вашого застосунку дає легкий спосіб обмежити будь-яку дію в межах заданого проміжку часу.

> [!NOTE]
> Якщо вас цікавить обмеження частоти вхідних HTTP-запитів, зверніться до [документації middleware обмежувача частоти](/docs/{{version}}/routing#rate-limiting).

<a name="cache-configuration"></a>
### Конфігурація кешу

Зазвичай обмежувач частоти використовує кеш застосунку за замовчуванням, заданий ключем `default` у файлі конфігурації `cache`. Проте ви можете вказати, який драйвер кешу має використовувати обмежувач частоти, описавши ключ `limiter` у файлі конфігурації `cache` вашого застосунку:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]
```

<a name="basic-usage"></a>
## Базове використання

Для роботи з обмежувачем частоти призначено фасад `Illuminate\Support\Facades\RateLimiter`. Найпростіший метод, який пропонує обмежувач, - `attempt`: він обмежує частоту виконання заданого колбека протягом заданої кількості секунд.

Метод `attempt` повертає `false`, коли в колбека не лишилося доступних спроб; інакше `attempt` поверне результат колбека або `true`. Перший аргумент, який приймає метод `attempt`, - «ключ» обмежувача частоти: це може бути будь-який рядок на ваш вибір, що представляє дію, частоту якої обмежують:

```php
use Illuminate\Support\Facades\RateLimiter;

$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function() {
        // Send message...
    }
);

if (! $executed) {
    return 'Too many messages sent!';
}
```

За потреби ви можете передати методу `attempt` четвертий аргумент - «швидкість згасання», тобто кількість секунд до скидання доступних спроб. Наприклад, ми можемо змінити приклад вище так, щоб дозволити п'ять спроб кожні дві хвилини:

```php
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perTwoMinutes = 5,
    function() {
        // Send message...
    },
    $decayRate = 120,
);
```

<a name="manually-incrementing-attempts"></a>
### Ручне збільшення лічильника спроб

Якщо ви хочете працювати з обмежувачем частоти вручну, вам доступна низка інших методів. Наприклад, ви можете викликати метод `tooManyAttempts`, щоб визначити, чи перевищив заданий ключ обмежувача максимальну дозволену кількість спроб за хвилину:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

Обмежуючи частоту точки, яка може отримувати багато одночасних запитів, вам, можливо, варто перевіряти значення, яке повертає метод `increment`, замість використовувати `tooManyAttempts` та `increment` як окремі операції. Зі сховищами кешу `redis`, `memcached` чи `database` це значення збільшується атомарно, тож кожен паралельний запит отримує унікальний лічильник:

```php
use Illuminate\Support\Facades\RateLimiter;

$perMinute = 5;

if (RateLimiter::increment('send-message:'.$user->id) > $perMinute) {
    return 'Too many attempts!';
}

// Send message...
```

Як варіант, ви можете скористатися методом `remaining`, щоб дізнатися, скільки спроб лишилося для заданого ключа. Якщо для ключа є спроби, ви можете викликати метод `increment`, щоб збільшити загальну кількість спроб:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

Якщо ви хочете збільшити значення для заданого ключа обмежувача більше ніж на одиницю, передайте потрібну величину методу `increment`:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### Визначення доступності обмежувача

Коли в ключа не лишилося спроб, метод `availableIn` повертає кількість секунд до того, як спроби знову стануть доступними:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<a name="clearing-attempts"></a>
### Скидання спроб

Ви можете скинути кількість спроб для заданого ключа обмежувача методом `clear`. Наприклад, ви можете скидати кількість спроб, коли отримувач прочитав повідомлення:

```php
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Mark the message as read.
 */
public function read(Message $message): Message
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```

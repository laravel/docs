---
title: "Limitação de Taxa"
---

- [Introdução](#introduction)
    - [Configuração do Cache](#cache-configuration)
- [Uso Básico](#basic-usage)
    - [Incrementando Tentativas Manualmente](#manually-incrementing-attempts)
    - [Limpando Tentativas](#clearing-attempts)

<a id="introduction"></a>
## Introdução

O Laravel inclui uma abstração de limitação de taxa simples de usar que, em conjunto com o [cache](../cache/) da sua aplicação, fornece uma maneira fácil de limitar qualquer ação durante um intervalo de tempo especificado.

> **Nota:**
> Se você tem interesse em limitar a taxa de requisições HTTP recebidas, consulte a [documentação do middleware de limitação de taxa](../routing/#rate-limiting).

<a id="cache-configuration"></a>
### Configuração do Cache

Normalmente, o limitador de taxa utiliza o cache padrão da sua aplicação, definido pela chave `default` no arquivo de configuração `cache` da sua aplicação. No entanto, você pode especificar qual driver de cache o limitador de taxa deve usar definindo uma chave `limiter` no arquivo de configuração `cache` da sua aplicação:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]
```

<a id="basic-usage"></a>
## Uso Básico

A facade `Illuminate\Support\Facades\RateLimiter` pode ser usada para interagir com o limitador de taxa. O método mais simples oferecido pelo limitador de taxa é o método `attempt`, que limita a taxa de um callback fornecido por um número determinado de segundos.

O método `attempt` retorna `false` quando o callback não tem mais tentativas disponíveis; caso contrário, o método `attempt` retornará o resultado do callback ou `true`. O primeiro argumento aceito pelo método `attempt` é uma "chave" do limitador de taxa, que pode ser qualquer string de sua escolha que represente a ação limitada:

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

Se necessário, você pode fornecer um quarto argumento ao método `attempt`, que é a "taxa de decaimento", ou seja, o número de segundos até que as tentativas disponíveis sejam redefinidas. Por exemplo, podemos modificar o exemplo acima para permitir cinco tentativas a cada dois minutos:

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

<a id="manually-incrementing-attempts"></a>
### Incrementando Tentativas Manualmente

Se você quiser interagir manualmente com o limitador de taxa, há uma variedade de outros métodos disponíveis. Por exemplo, você pode invocar o método `tooManyAttempts` para determinar se uma determinada chave do limitador de taxa excedeu seu número máximo de tentativas permitidas por minuto:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

Ao limitar a taxa de um endpoint que pode receber muitas requisições simultâneas, você pode querer verificar o valor retornado pelo método `increment`, em vez de usar `tooManyAttempts` e `increment` como operações separadas. Ao usar os drivers de cache `redis`, `memcached` ou `database`, esse valor é incrementado de forma atômica, garantindo que cada requisição concorrente receba uma contagem única:

```php
use Illuminate\Support\Facades\RateLimiter;

$perMinute = 5;

if (RateLimiter::increment('send-message:'.$user->id) > $perMinute) {
    return 'Too many attempts!';
}

// Send message...
```

Alternativamente, você pode usar o método `remaining` para obter o número de tentativas restantes para uma determinada chave. Se uma chave tiver tentativas restantes, você pode invocar o método `increment` para incrementar o número total de tentativas:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

Se você quiser incrementar o valor de uma determinada chave do limitador de taxa em mais de um, pode fornecer a quantidade desejada ao método `increment`:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a id="determining-limiter-availability"></a>
#### Determinando a Disponibilidade do Limitador

Quando uma chave não tem mais tentativas, o método `availableIn` retorna o número de segundos restantes até que mais tentativas estejam disponíveis:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<a id="clearing-attempts"></a>
### Limpando Tentativas

Você pode redefinir o número de tentativas para uma determinada chave do limitador de taxa usando o método `clear`. Por exemplo, você pode redefinir o número de tentativas quando uma determinada mensagem for lida pelo destinatário:

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

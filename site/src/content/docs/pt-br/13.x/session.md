---
title: "Sessão HTTP"
---

- [Introdução](#introduction)
    - [Configuração](#configuration)
    - [Pré-requisitos do Driver](#driver-prerequisites)
- [Interagindo com a Sessão](#interacting-with-the-session)
    - [Recuperando Dados](#retrieving-data)
    - [Armazenando Dados](#storing-data)
    - [Dados Flash](#flash-data)
    - [Deletando Dados](#deleting-data)
    - [Regenerando o ID da Sessão](#regenerating-the-session-id)
- [Cache de Sessão](#session-cache)
- [Bloqueio de Sessão](#session-blocking)
- [Adicionando Drivers de Sessão Personalizados](#adding-custom-session-drivers)
    - [Implementando o Driver](#implementing-the-driver)
    - [Registrando o Driver](#registering-the-driver)

<a id="introduction"></a>
## Introdução

Como aplicações orientadas por HTTP são stateless, sessões fornecem uma maneira de armazenar informações sobre o usuário através de múltiplas requisições. Essas informações do usuário são tipicamente colocadas em um armazenamento / backend persistente que pode ser acessado a partir de requisições subsequentes.

O Laravel vem com uma variedade de backends de sessão que são acessados através de uma API expressiva e unificada. Suporte para backends populares como [Memcached](https://memcached.org), [Redis](https://redis.io) e bancos de dados está incluído.

<a id="configuration"></a>
### Configuração

O arquivo de configuração de sessão da sua aplicação está armazenado em `config/session.php`. Certifique-se de revisar as opções disponíveis para você neste arquivo. Por padrão, o Laravel está configurado para usar o driver de sessão `database`.

A opção de configuração `driver` da sessão define onde os dados da sessão serão armazenados para cada requisição. O Laravel inclui uma variedade de drivers:

<div class="content-list" markdown="1">

- `file` - sessões são armazenadas em `storage/framework/sessions`.
- `cookie` - sessões são armazenadas em cookies seguros e criptografados.
- `database` - sessões são armazenadas em um banco de dados relacional.
- `memcached` / `redis` - sessões são armazenadas em um desses armazenamentos rápidos baseados em cache.
- `dynamodb` - sessões são armazenadas no AWS DynamoDB.
- `array` - sessões são armazenadas em um array PHP e não serão persistidas.

</div>

> **Nota:**
> O driver array é usado primariamente durante [testes](../testing/) e impede que os dados armazenados na sessão sejam persistidos.

<a id="driver-prerequisites"></a>
### Pré-requisitos do Driver

<a id="database"></a>
#### Database

Ao usar o driver de sessão `database`, você precisará garantir que tem uma tabela de banco de dados para conter os dados da sessão. Tipicamente, isso está incluído na [migração de banco de dados](../migrations/) padrão `0001_01_01_000000_create_users_table.php` do Laravel; no entanto, se por qualquer motivo você não tiver uma tabela `sessions`, você pode usar o comando Artisan `make:session-table` para gerar esta migração:

```shell
php artisan make:session-table

php artisan migrate
```

<a id="redis"></a>
#### Redis

Antes de usar sessões Redis com o Laravel, você precisará instalar a extensão PHP PhpRedis via PECL ou instalar o pacote `predis/predis` via Composer. Para mais informações sobre configuração do Redis, consulte a [documentação do Redis](../redis/#configuration) do Laravel.

> **Nota:**
> A variável de ambiente `SESSION_CONNECTION`, ou a opção `connection` no arquivo de configuração `session.php`, pode ser usada para especificar qual conexão Redis é usada para armazenamento de sessão.

<a id="interacting-with-the-session"></a>
## Interagindo com a Sessão

<a id="retrieving-data"></a>
### Recuperando Dados

Existem duas maneiras principais de trabalhar com dados de sessão no Laravel: o helper global `session` e via uma instância de `Request`. Primeiro, vamos ver como acessar a sessão via uma instância de `Request`, que pode ser type-hinted em um closure de rota ou método de controller. Lembre-se, as dependências do método do controller são injetadas automaticamente via o [container de serviço](../container/) do Laravel:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(Request $request, string $id): View
    {
        $value = $request->session()->get('key');

        // ...

        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

Quando você recupera um item da sessão, você também pode passar um valor padrão como segundo argumento ao método `get`. Este valor padrão será retornado se a chave especificada não existir na sessão. Se você passar um closure como valor padrão ao método `get` e a chave solicitada não existir, o closure será executado e seu resultado retornado:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a id="the-global-session-helper"></a>
#### O Helper Global de Sessão

Você também pode usar a função global PHP `session` para recuperar e armazenar dados na sessão. Quando o helper `session` é chamado com um único argumento string, ele retornará o valor daquela chave de sessão. Quando o helper é chamado com um array de pares chave / valor, esses valores serão armazenados na sessão:

```php
Route::get('/home', function () {
    // Retrieve a piece of data from the session...
    $value = session('key');

    // Specifying a default value...
    $value = session('key', 'default');

    // Store a piece of data in the session...
    session(['key' => 'value']);
});
```

> **Nota:**
> Há pouca diferença prática entre usar a sessão via uma instância de requisição HTTP versus usar o helper global `session`. Ambos os métodos são [testáveis](../testing/) via o método `assertSessionHas` que está disponível em todos os seus casos de teste.

<a id="retrieving-all-session-data"></a>
#### Recuperando Todos os Dados da Sessão

Se você gostaria de recuperar todos os dados da sessão, você pode usar o método `all`:

```php
$data = $request->session()->all();
```

<a id="retrieving-a-portion-of-the-session-data"></a>
#### Recuperando uma Porção dos Dados da Sessão

Os métodos `only` e `except` podem ser usados para recuperar um subconjunto dos dados da sessão:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a id="determining-if-an-item-exists-in-the-session"></a>
#### Determinando se um Item Existe na Sessão

Para determinar se um item está presente na sessão, você pode usar o método `has`. O método `has` retorna `true` se o item está presente e não é `null`:

```php
if ($request->session()->has('users')) {
    // ...
}
```

Para determinar se um item está presente na sessão, mesmo que seu valor seja `null`, você pode usar o método `exists`:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

Para determinar se um item não está presente na sessão, você pode usar o método `missing`. O método `missing` retorna `true` se o item não estiver presente:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a id="storing-data"></a>
### Armazenando Dados

Para armazenar dados na sessão, você normalmente usará o método `put` da instância de requisição ou o helper global `session`:

```php
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);
```

<a id="pushing-to-array-session-values"></a>
#### Adicionando a Valores de Sessão em Array

O método `push` pode ser usado para adicionar um novo valor a um valor de sessão que é um array. Por exemplo, se a chave `user.teams` contém um array de nomes de equipes, você pode adicionar um novo valor ao array assim:

```php
$request->session()->push('user.teams', 'developers');
```

<a id="retrieving-deleting-an-item"></a>
#### Recuperando e Deletando um Item

O método `pull` irá recuperar e deletar um item da sessão em uma única instrução:

```php
$value = $request->session()->pull('key', 'default');
```

<a id="incrementing-and-decrementing-session-values"></a>
#### Incrementando e Decrementando Valores de Sessão

Se seus dados de sessão contêm um inteiro que você deseja incrementar ou decrementar, você pode usar os métodos `increment` e `decrement`:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a id="flash-data"></a>
### Dados Flash

Às vezes, você pode desejar armazenar itens na sessão para a próxima requisição. Você pode fazer isso usando o método `flash`. Dados armazenados na sessão usando este método estarão disponíveis imediatamente e durante a próxima requisição HTTP. Após a próxima requisição HTTP, os dados flash serão deletados. Dados flash são primariamente úteis para mensagens de status de curta duração:

```php
$request->session()->flash('status', 'Task was successful!');
```

Se você precisa persistir seus dados flash por várias requisições, você pode usar o método `reflash`, que manterá todos os dados flash para uma requisição adicional. Se você só precisa manter dados flash específicos, você pode usar o método `keep`:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

Para persistir seus dados flash apenas para a requisição atual, você pode usar o método `now`:

```php
$request->session()->now('status', 'Task was successful!');
```

<a id="deleting-data"></a>
### Deletando Dados

O método `forget` removerá um pedaço de dados da sessão. Se você gostaria de remover todos os dados da sessão, você pode usar o método `flush`:

```php
// Forget a single key...
$request->session()->forget('name');

// Forget multiple keys...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a id="regenerating-the-session-id"></a>
### Regenerando o ID da Sessão

Regenerar o ID da sessão é frequentemente feito para prevenir que usuários maliciosos explorem um ataque de [fixação de sessão](https://owasp.org/www-community/attacks/Session_fixation) na sua aplicação.

O Laravel regenera automaticamente o ID da sessão durante a autenticação se você estiver usando um dos [starter kits de aplicação](../starter-kits/) do Laravel ou [Laravel Fortify](../fortify/); no entanto, se você precisar regenerar manualmente o ID da sessão, você pode usar o método `regenerate`:

```php
$request->session()->regenerate();
```

Se você precisa regenerar o ID da sessão e remover todos os dados da sessão em uma única instrução, você pode usar o método `invalidate`:

```php
$request->session()->invalidate();
```

<a id="session-cache"></a>
## Cache de Sessão

O cache de sessão do Laravel fornece uma maneira conveniente de armazenar em cache dados que são escopados para uma sessão de usuário individual. Diferente do cache global da aplicação, os dados do cache de sessão são automaticamente isolados por sessão e são limpos quando a sessão expira ou é destruída. O cache de sessão suporta todos os [métodos de cache do Laravel](../cache/) familiares como `get`, `put`, `remember`, `forget`, e mais, mas escopados para a sessão atual.

O cache de sessão é perfeito para armazenar dados temporários específicos do usuário que você deseja persistir através de múltiplas requisições dentro da mesma sessão, mas não precisa armazenar permanentemente. Isso inclui coisas como dados de formulário, cálculos temporários, respostas de API ou quaisquer outros dados efêmeros que devem estar vinculados à sessão de um usuário específico.

Você pode acessar o cache de sessão através do método `cache` na sessão:

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->plus(minutes: 5)
);
```

Para mais informações sobre os métodos de cache do Laravel, consulte a [documentação de cache](../cache/).

<a id="session-blocking"></a>
## Bloqueio de Sessão

> **Aviso:**
> Para utilizar o bloqueio de sessão, sua aplicação deve estar usando um driver de cache que suporte [locks atômicos](../cache/#atomic-locks). Atualmente, esses drivers de cache incluem os drivers `memcached`, `dynamodb`, `redis`, `mongodb` (incluído no pacote oficial `mongodb/laravel-mongodb`), `database`, `file` e `array`. Além disso, você não pode usar o driver de sessão `cookie`.

Por padrão, o Laravel permite que requisições usando a mesma sessão sejam executadas concorrentemente. Então, por exemplo, se você usar uma biblioteca HTTP JavaScript para fazer duas requisições HTTP para sua aplicação, ambas serão executadas ao mesmo tempo. Para muitas aplicações, isso não é um problema; no entanto, perda de dados de sessão pode ocorrer em um pequeno subconjunto de aplicações que fazem requisições concorrentes para dois endpoints diferentes da aplicação que ambos escrevem dados na sessão.

Para mitigar isso, o Laravel fornece funcionalidade que permite limitar requisições concorrentes para uma determinada sessão. Para começar, você pode simplesmente encadear o método `block` na definição da sua rota. Neste exemplo, uma requisição recebida para o endpoint `/profile` adquiriria um lock de sessão. Enquanto este lock estiver sendo mantido, quaisquer requisições recebidas para os endpoints `/profile` ou `/order` que compartilham o mesmo ID de sessão esperarão que a primeira requisição termine de executar antes de continuar sua execução:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

O método `block` aceita dois argumentos opcionais. O primeiro argumento aceito pelo método `block` é o número máximo de segundos que o lock da sessão deve ser mantido antes de ser liberado. Claro, se a requisição terminar de executar antes deste tempo, o lock será liberado mais cedo.

O segundo argumento aceito pelo método `block` é o número de segundos que uma requisição deve esperar enquanto tenta obter um lock de sessão. Uma exceção `Illuminate\Contracts\Cache\LockTimeoutException` será lançada se a requisição não conseguir obter um lock de sessão dentro do número fornecido de segundos.

Se nenhum desses argumentos for passado, o lock será obtido por um máximo de 10 segundos e as requisições esperarão um máximo de 10 segundos enquanto tentam obter um lock:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a id="adding-custom-session-drivers"></a>
## Adicionando Drivers de Sessão Personalizados

<a id="implementing-the-driver"></a>
### Implementando o Driver

Se nenhum dos drivers de sessão existentes atender às necessidades da sua aplicação, o Laravel torna possível escrever seu próprio handler de sessão. Seu driver de sessão personalizado deve implementar a interface nativa do PHP `SessionHandlerInterface`. Esta interface contém apenas alguns métodos simples. Uma implementação stubbed do MongoDB se parece com o seguinte:

```php
<?php

namespace App\Extensions;

class MongoSessionHandler implements \SessionHandlerInterface
{
    public function open($savePath, $sessionName) {}
    public function close() {}
    public function read($sessionId) {}
    public function write($sessionId, $data) {}
    public function destroy($sessionId) {}
    public function gc($lifetime) {}
}
```

Como o Laravel não inclui um diretório padrão para abrigar suas extensões, você é livre para colocá-las onde quiser. Neste exemplo, criamos um diretório `Extensions` para abrigar o `MongoSessionHandler`.

Como o propósito desses métodos não é facilmente compreensível, aqui está uma visão geral do propósito de cada método:

<div class="content-list" markdown="1">

- O método `open` seria tipicamente usado em sistemas de armazenamento de sessão baseados em arquivo. Como o Laravel vem com um driver de sessão `file`, você raramente precisará colocar qualquer coisa neste método. Você pode simplesmente deixar este método vazio.
- O método `close`, como o método `open`, também pode geralmente ser ignorado. Para a maioria dos drivers, ele não é necessário.
- O método `read` deve retornar a versão string dos dados da sessão associados com o `$sessionId` fornecido. Não há necessidade de fazer qualquer serialização ou outra codificação ao recuperar ou armazenar dados da sessão no seu driver, pois o Laravel realizará a serialização para você.
- O método `write` deve escrever a string `$data` fornecida associada com o `$sessionId` em algum sistema de armazenamento persistente, como MongoDB ou outro sistema de armazenamento de sua escolha. Novamente, você não deve realizar qualquer serialização - o Laravel já terá tratado isso para você.
- O método `destroy` deve remover os dados associados com o `$sessionId` do armazenamento persistente.
- O método `gc` deve destruir todos os dados da sessão que são mais antigos que o `$lifetime` fornecido, que é um número de segundos. Para sistemas auto-expiráveis como Memcached e Redis, este método pode ser deixado vazio.

</div>

<a id="registering-the-driver"></a>
### Registrando o Driver

Uma vez que seu driver tenha sido implementado, você está pronto para registrá-lo com o Laravel. Para adicionar drivers adicionais ao backend de sessão do Laravel, você pode usar o método `extend` fornecido pela [facade](../facades/) `Session`. Você deve chamar o método `extend` do método `boot` de um [provedor de serviço](../providers/). Você pode fazer isso do existente `App\Providers\AppServiceProvider` ou criar um provedor totalmente novo:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
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
        Session::extend('mongo', function (Application $app) {
            // Return an implementation of SessionHandlerInterface...
            return new MongoSessionHandler;
        });
    }
}
```

Uma vez que o driver de sessão tenha sido registrado, você pode especificar o driver `mongo` como o driver de sessão da sua aplicação usando a variável de ambiente `SESSION_DRIVER` ou dentro do arquivo de configuração `config/session.php` da aplicação.
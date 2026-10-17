---
title: "Console Artisan"
---

- [Introdução](#introduction)
    - [Tinker (REPL)](#tinker)
- [Escrevendo Comandos](#writing-commands)
    - [Gerando Comandos](#generating-commands)
    - [Estrutura do Comando](#command-structure)
    - [Comandos com Closure](#closure-commands)
    - [Comandos Isoláveis](#isolatable-commands)
- [Definindo Expectativas de Entrada](#defining-input-expectations)
    - [Argumentos](#arguments)
    - [Opções](#options)
    - [Arrays de Entrada](#input-arrays)
    - [Descrições de Entrada](#input-descriptions)
    - [Solicitando Entrada Ausente](#prompting-for-missing-input)
- [I/O do Comando](#command-io)
    - [Recuperando Entrada](#retrieving-input)
    - [Solicitando Entrada](#prompting-for-input)
    - [Escrevendo Saída](#writing-output)
- [Registrando Comandos](#registering-commands)
- [Executando Comandos Programaticamente](#programmatically-executing-commands)
    - [Chamando Comandos a Partir de Outros Comandos](#calling-commands-from-other-commands)
- [Tratamento de Sinais](#signal-handling)
- [O Comando Dev](#the-dev-command)
    - [Personalizando Processos Dev](#customizing-dev-processes)
    - [Filtrando Processos Dev](#filtering-dev-processes)
- [Personalização de Stubs](#stub-customization)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

O Artisan é a interface de linha de comando incluída com o Laravel. O Artisan existe na raiz da sua aplicação como o script `artisan` e fornece uma série de comandos úteis que você pode usar enquanto constrói sua aplicação. Para ver uma lista de todos os comandos Artisan disponíveis, você pode usar o comando `list`:

```shell
php artisan list
```

Todo comando também inclui uma tela de "help" (ajuda) que exibe e descreve os argumentos e opções disponíveis do comando. Para ver uma tela de ajuda, preceda o nome do comando com `help`:

```shell
php artisan help migrate
```

<a id="laravel-sail"></a>
#### Laravel Sail

Se você estiver usando o [Laravel Sail](../sail/) como seu ambiente de desenvolvimento local, lembre-se de usar a linha de comando `sail` para invocar comandos Artisan. O Sail executará seus comandos Artisan dentro dos contêineres Docker da sua aplicação:

```shell
./vendor/bin/sail artisan list
```

<a id="tinker"></a>
### Tinker (REPL)

O [Laravel Tinker](https://github.com/laravel/tinker) é um REPL poderoso para o framework Laravel, impulsionado pelo pacote [PsySH](https://github.com/bobthecow/psysh).

<a id="installation"></a>
#### Instalação

Todas as aplicações Laravel incluem o Tinker por padrão. No entanto, você pode instalar o Tinker usando o Composer se você o tiver removido previamente da sua aplicação:

```shell
composer require laravel/tinker
```

> **Nota:**
> Procurando por hot reloading, edição de código multilinha e autocompletar ao interagir com sua aplicação Laravel? Confira o [Tinkerwell](https://tinkerwell.app)!

<a id="usage"></a>
#### Uso

O Tinker permite que você interaja com toda a sua aplicação Laravel na linha de comando, incluindo seus models Eloquent, jobs, eventos e muito mais. Para entrar no ambiente do Tinker, execute o comando Artisan `tinker`:

```shell
php artisan tinker
```

Você pode publicar o arquivo de configuração do Tinker usando o comando `vendor:publish`:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> **Aviso:**
> A função helper `dispatch` e o método `dispatch` na classe `Dispatchable` dependem da coleta de lixo (garbage collection) para colocar o job na fila. Portanto, ao usar o Tinker, você deve usar `Bus::dispatch` ou `Queue::push` para despachar jobs.

<a id="command-allow-list"></a>
#### Lista de Permissão de Comandos

O Tinker utiliza uma lista de "permissão" para determinar quais comandos Artisan têm permissão para serem executados dentro do seu shell. Por padrão, você pode executar os comandos `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up` e `optimize`. Se você gostaria de permitir mais comandos, você pode adicioná-los ao array `commands` no seu arquivo de configuração `tinker.php`:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a id="classes-that-should-not-be-aliased"></a>
#### Classes Que Não Devem Receber Alias

Normalmente, o Tinker cria aliases de classes automaticamente conforme você interage com elas no Tinker. No entanto, você pode querer nunca criar alias de algumas classes. Você pode fazer isso listando as classes no array `dont_alias` do seu arquivo de configuração `tinker.php`:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a id="writing-commands"></a>
## Escrevendo Comandos

Além dos comandos fornecidos com o Artisan, você pode construir seus próprios comandos personalizados. Os comandos são normalmente armazenados no diretório `app/Console/Commands`; no entanto, você está livre para escolher seu próprio local de armazenamento, desde que você instrua o Laravel a [escanear outros diretórios em busca de comandos Artisan](#registering-commands).

<a id="generating-commands"></a>
### Gerando Comandos

Para criar um novo comando, você pode usar o comando Artisan `make:command`. Este comando criará uma nova classe de comando no diretório `app/Console/Commands`. Não se preocupe se este diretório não existir na sua aplicação - ele será criado na primeira vez que você executar o comando Artisan `make:command`:

```shell
php artisan make:command SendEmails
```

<a id="command-structure"></a>
### Estrutura do Comando

Depois de gerar seu comando, você deve definir a assinatura e a descrição do comando usando os atributos `Signature` e `Description`. O atributo `Signature` também permite que você defina [as expectativas de entrada do seu comando](#defining-input-expectations). O método `handle` será chamado quando seu comando for executado. Você pode colocar a lógica do seu comando neste método.

Vamos dar uma olhada em um comando de exemplo. Observe que somos capazes de solicitar quaisquer dependências que precisarmos via o método `handle` do comando. O [container de serviço](../container/) do Laravel injetará automaticamente todas as dependências que têm type-hint na assinatura deste método:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('mail:send {user}')]
#[Description('Send a marketing email to a user')]
class SendEmails extends Command
{
    /**
     * Execute the console command.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> **Nota:**
> Para maior reutilização de código, é uma boa prática manter seus comandos de console leves e deixar que eles deleguem aos serviços da aplicação para realizar suas tarefas. No exemplo acima, observe que injetamos uma classe de serviço para fazer o "trabalho pesado" de enviar os e-mails.

<a id="exit-codes"></a>
#### Códigos de Saída

Se nada for retornado do método `handle` e o comando for executado com sucesso, o comando sairá com um código de saída `0`, indicando sucesso. No entanto, o método `handle` pode opcionalmente retornar um inteiro para especificar manualmente o código de saída do comando:

```php
$this->error('Something went wrong.');

return 1;
```

Se você gostaria de "falhar" o comando a partir de qualquer método dentro do comando, você pode utilizar o método `fail`. O método `fail` encerrará imediatamente a execução do comando e retornará um código de saída `1`:

```php
$this->fail('Something went wrong.');
```

<a id="closure-commands"></a>
### Comandos com Closure

Os comandos baseados em closure fornecem uma alternativa a definir comandos de console como classes. Da mesma forma que as closures de rota são uma alternativa aos controllers, pense nas closures de comando como uma alternativa às classes de comando.

Mesmo que o arquivo `routes/console.php` não defina rotas HTTP, ele define pontos de entrada (rotas) baseados em console para a sua aplicação. Dentro deste arquivo, você pode definir todos os seus comandos de console baseados em closure usando o método `Artisan::command`. O método `command` aceita dois argumentos: a [assinatura do comando](#defining-input-expectations) e uma closure que recebe os argumentos e opções do comando:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

A closure é vinculada à instância de comando subjacente, então você tem acesso completo a todos os métodos helper que você normalmente conseguiria acessar em uma classe de comando completa.

<a id="type-hinting-dependencies"></a>
#### Type-Hinting de Dependências

Além de receber os argumentos e opções do seu comando, as closures de comando também podem fazer type-hint de dependências adicionais que você gostaria que fossem resolvidas a partir do [container de serviço](../container/):

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a id="closure-command-descriptions"></a>
#### Descrições de Comandos com Closure

Ao definir um comando baseado em closure, você pode usar o método `purpose` para adicionar uma descrição ao comando. Essa descrição será exibida quando você executar os comandos `php artisan list` ou `php artisan help`:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a id="isolatable-commands"></a>
### Comandos Isoláveis

> **Aviso:**
> Para utilizar este recurso, sua aplicação deve estar usando o driver de cache `memcached`, `redis`, `dynamodb`, `database`, `file` ou `array` como o driver de cache padrão da sua aplicação. Além disso, todos os servidores devem estar se comunicando com o mesmo servidor de cache central.

Às vezes você pode querer garantir que apenas uma instância de um comando possa ser executada por vez. Para fazer isso, você pode implementar a interface `Illuminate\Contracts\Console\Isolatable` na sua classe de comando:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

Quando você marca um comando como `Isolatable`, o Laravel disponibiliza automaticamente a opção `--isolated` para o comando sem precisar defini-la explicitamente nas opções do comando. Quando o comando é invocado com essa opção, o Laravel garantirá que nenhuma outra instância desse comando já esteja em execução. O Laravel faz isso tentando adquirir um lock atômico usando o driver de cache padrão da sua aplicação. Se outras instâncias do comando estiverem em execução, o comando não será executado; no entanto, o comando ainda sairá com um código de status de saída bem-sucedido:

```shell
php artisan mail:send 1 --isolated
```

Se você gostaria de especificar o código de status de saída que o comando deve retornar caso não seja capaz de executar, você pode fornecer o código de status desejado via a opção `isolated`:

```shell
php artisan mail:send 1 --isolated=12
```

<a id="lock-id"></a>
#### ID do Lock

Por padrão, o Laravel usará o nome do comando para gerar a chave string que é usada para adquirir o lock atômico no cache da sua aplicação. No entanto, você pode personalizar essa chave definindo um método `isolatableId` na sua classe de comando Artisan, permitindo que você integre os argumentos ou opções do comando na chave:

```php
/**
 * Get the isolatable ID for the command.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a id="lock-expiration-time"></a>
#### Tempo de Expiração do Lock

Por padrão, os locks de isolamento expiram após o comando terminar. Ou, se o comando for interrompido e não conseguir terminar, o lock expirará após uma hora. No entanto, você pode ajustar o tempo de expiração do lock definindo um método `isolationLockExpiresAt` no seu comando:

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```

<a id="defining-input-expectations"></a>
## Definindo Expectativas de Entrada

Ao escrever comandos de console, é comum reunir a entrada do usuário através de argumentos ou opções. O Laravel torna muito conveniente definir a entrada que você espera do usuário usando a propriedade `signature` nos seus comandos. A propriedade `signature` permite que você defina o nome, os argumentos e as opções para o comando em uma sintaxe única, expressiva e semelhante a uma rota.

<a id="arguments"></a>
### Argumentos

Todos os argumentos e opções fornecidos pelo usuário são envolvidos em chaves. No exemplo a seguir, o comando define um argumento obrigatório: `user`:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

Você também pode tornar os argumentos opcionais ou definir valores padrão para os argumentos:

```php
// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
```

<a id="options"></a>
### Opções

As opções, assim como os argumentos, são outra forma de entrada do usuário. As opções são prefixadas por dois hífens (`--`) quando são fornecidas via linha de comando. Existem dois tipos de opções: aquelas que recebem um valor e aquelas que não recebem. As opções que não recebem um valor servem como um "interruptor" booleano. Vamos dar uma olhada em um exemplo desse tipo de opção:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

Neste exemplo, o interruptor `--queue` pode ser especificado ao chamar o comando Artisan. Se o interruptor `--queue` for passado, o valor da opção será `true`. Caso contrário, o valor será `false`:

```shell
php artisan mail:send 1 --queue
```

<a id="options-with-values"></a>
#### Opções Com Valores

Em seguida, vamos dar uma olhada em uma opção que espera um valor. Se o usuário precisar especificar um valor para uma opção, você deve adicionar o sufixo `=` ao nome da opção:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

Neste exemplo, o usuário pode passar um valor para a opção assim. Se a opção não for especificada ao invocar o comando, seu valor será `null`:

```shell
php artisan mail:send 1 --queue=default
```

Você pode atribuir valores padrão às opções especificando o valor padrão após o nome da opção. Se nenhum valor de opção for passado pelo usuário, o valor padrão será usado:

```php
'mail:send {user} {--queue=default}'
```

<a id="option-shortcuts"></a>
#### Atalhos de Opção

Para atribuir um atalho ao definir uma opção, você pode especificá-lo antes do nome da opção e usar o caractere `|` como delimitador para separar o atalho do nome completo da opção:

```php
'mail:send {user} {--Q|queue=}'
```

Ao invocar o comando no seu terminal, os atalhos de opção devem ser prefixados com um único hífen e nenhum caractere `=` deve ser incluído ao especificar um valor para a opção:

```shell
php artisan mail:send 1 -Qdefault
```

<a id="input-arrays"></a>
### Arrays de Entrada

Se você gostaria de definir argumentos ou opções para esperar múltiplos valores de entrada, você pode usar o caractere `*`. Primeiro, vamos dar uma olhada em um exemplo que especifica tal argumento:

```php
'mail:send {user*}'
```

Ao executar este comando, os argumentos `user` podem ser passados em ordem para a linha de comando. Por exemplo, o comando a seguir definirá o valor de `user` como um array com `1` e `2` como seus valores:

```shell
php artisan mail:send 1 2
```

Este caractere `*` pode ser combinado com uma definição de argumento opcional para permitir zero ou mais instâncias de um argumento:

```php
'mail:send {user?*}'
```

<a id="option-arrays"></a>
#### Arrays de Opção

Ao definir uma opção que espera múltiplos valores de entrada, cada valor de opção passado ao comando deve ser prefixado com o nome da opção:

```php
'mail:send {--id=*}'
```

Tal comando pode ser invocado passando múltiplos argumentos `--id`:

```shell
php artisan mail:send --id=1 --id=2
```

<a id="input-descriptions"></a>
### Descrições de Entrada

Você pode atribuir descrições aos argumentos e opções de entrada separando o nome do argumento da descrição usando dois pontos. Se você precisar de um pouco mais de espaço para definir seu comando, sinta-se à vontade para espalhar a definição por múltiplas linhas:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a id="prompting-for-missing-input"></a>
### Solicitando Entrada Ausente

Se o seu comando contém argumentos obrigatórios, o usuário receberá uma mensagem de erro quando eles não forem fornecidos. Alternativamente, você pode configurar seu comando para solicitar automaticamente ao usuário quando os argumentos obrigatórios estiverem ausentes, implementando a interface `PromptsForMissingInput`:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Se o Laravel precisar reunir um argumento obrigatório do usuário, ele automaticamente perguntará ao usuário pelo argumento, formulando a pergunta de forma inteligente usando o nome ou a descrição do argumento. Se você desejar personalizar a pergunta usada para reunir o argumento obrigatório, você pode implementar o método `promptForMissingArgumentsUsing`, retornando um array de perguntas indexadas pelos nomes dos argumentos:

```php
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

Você também pode fornecer texto de placeholder usando uma tupla contendo a pergunta e o placeholder:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

Se você gostaria de ter controle completo sobre o prompt, você pode fornecer uma closure que deve solicitar o usuário e retornar a resposta dele:

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> **Nota:**
A documentação abrangente do [Laravel Prompts](../prompts/) inclui informações adicionais sobre os prompts disponíveis e seu uso.

Se você desejar solicitar ao usuário que selecione ou insira [opções](#options), você pode incluir prompts no método `handle` do seu comando. No entanto, se você desejar solicitar ao usuário apenas quando ele também tiver sido solicitado automaticamente por argumentos ausentes, então você pode implementar o método `afterPromptingForMissingArguments`:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: 'Would you like to queue the mail?',
        default: $this->option('queue')
    ));
}
```

<a id="command-io"></a>
## I/O do Comando

<a id="retrieving-input"></a>
### Recuperando Entrada

Enquanto seu comando está sendo executado, você provavelmente precisará acessar os valores dos argumentos e opções aceitos pelo seu comando. Para fazer isso, você pode usar os métodos `argument` e `option`. Se um argumento ou opção não existir, `null` será retornado:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

Se você precisar recuperar todos os argumentos como um `array`, chame o método `arguments`:

```php
$arguments = $this->arguments();
```

As opções podem ser recuperadas tão facilmente quanto os argumentos usando o método `option`. Para recuperar todas as opções como um array, chame o método `options`:

```php
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

Você pode usar o método `input` para recuperar os argumentos e opções de um comando como uma instância de `Illuminate\Console\CommandInput`, que fornece os mesmos acessadores tipados que estão disponíveis em requisições HTTP e outros contêineres de dados:

```php
use App\Enums\ReportType;

/**
 * Execute the console command.
 */
public function handle(): void
{
    $input = $this->input()->date('from');

    // ...
}
```

O método `input` também pode ser usado para recuperar um único valor de entrada seja dos argumentos ou das opções:

```php
$queue = $this->input('queue', 'default');
```

<a id="prompting-for-input"></a>
### Solicitando Entrada

> **Nota:**
> O [Laravel Prompts](../prompts/) é um pacote PHP para adicionar formulários bonitos e amigáveis às suas aplicações de linha de comando, com recursos semelhantes aos de um navegador, incluindo texto de placeholder e validação.

Além de exibir saída, você também pode pedir ao usuário para fornecer entrada durante a execução do seu comando. O método `ask` solicitará ao usuário com a pergunta dada, aceitará a entrada dele e então retornará a entrada do usuário de volta ao seu comando:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

O método `ask` também aceita um segundo argumento opcional que especifica o valor padrão que deve ser retornado se nenhuma entrada do usuário for fornecida:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

O método `secret` é semelhante ao `ask`, mas a entrada do usuário não ficará visível para ele enquanto digita no console. Este método é útil ao pedir informações sensíveis, como senhas:

```php
$password = $this->secret('What is the password?');
```

<a id="asking-for-confirmation"></a>
#### Pedindo Confirmação

Se você precisar pedir ao usuário uma simples confirmação de "sim ou não", você pode usar o método `confirm`. Por padrão, este método retornará `false`. No entanto, se o usuário inserir `y` ou `yes` em resposta ao prompt, o método retornará `true`.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

Se necessário, você pode especificar que o prompt de confirmação deve retornar `true` por padrão passando `true` como o segundo argumento ao método `confirm`:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a id="auto-completion"></a>
#### Autocompletar

O método `anticipate` pode ser usado para fornecer autocompletar para possíveis escolhas. O usuário ainda pode fornecer qualquer resposta, independentemente das dicas de autocompletar:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

Alternativamente, você pode passar uma closure como o segundo argumento ao método `anticipate`. A closure será chamada toda vez que o usuário digitar um caractere de entrada. A closure deve aceitar um parâmetro string contendo a entrada do usuário até o momento e retornar um array de opções para autocompletar:

```php
use App\Models\Address;

$name = $this->anticipate('What is your address?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```

<a id="multiple-choice-questions"></a>
#### Perguntas de Múltipla Escolha

Se você precisar dar ao usuário um conjunto predefinido de escolhas ao fazer uma pergunta, você pode usar o método `choice`. Você pode definir o índice do array do valor padrão a ser retornado caso nenhuma opção seja escolhida, passando o índice como o terceiro argumento ao método:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

Além disso, o método `choice` aceita um quarto e um quinto argumentos opcionais para determinar o número máximo de tentativas de selecionar uma resposta válida e se múltiplas seleções são permitidas:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a id="writing-output"></a>
### Escrevendo Saída

Para enviar saída ao console, você pode usar os métodos `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert` e `error`. Cada um desses métodos usará cores ANSI apropriadas para o seu propósito. Por exemplo, vamos exibir algumas informações gerais ao usuário. Normalmente, o método `info` será exibido no console como texto colorido em verde:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

Para exibir uma mensagem de erro, use o método `error`. O texto da mensagem de erro é normalmente exibido em vermelho:

```php
$this->error('Something went wrong!');
```

Você pode usar o método `line` para exibir texto simples, sem cor:

```php
$this->line('Display this on the screen');
```

Você pode usar o método `newLine` para exibir uma linha em branco:

```php
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```

<a id="tables"></a>
#### Tabelas

O método `table` facilita formatar corretamente múltiplas linhas / colunas de dados. Tudo o que você precisa fazer é fornecer os nomes das colunas e os dados para a tabela, e o Laravel calculará automaticamente a largura e a altura apropriadas da tabela para você:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a id="progress-bars"></a>
#### Barras de Progresso

Para tarefas de longa duração, pode ser útil mostrar uma barra de progresso que informa aos usuários o quão completa está a tarefa. Usando o método `withProgressBar`, o Laravel exibirá uma barra de progresso e avançará seu progresso a cada iteração sobre um determinado valor iterável:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

Às vezes, você pode precisar de mais controle manual sobre como uma barra de progresso é avançada. Primeiro, defina o número total de etapas pelas quais o processo irá iterar. Então, avance a barra de progresso após processar cada item:

```php
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```

> **Nota:**
> Para opções mais avançadas, confira a [documentação do componente Symfony Progress Bar](https://symfony.com/doc/current/components/console/helpers/progressbar.html).

<a id="registering-commands"></a>
## Registrando Comandos

Por padrão, o Laravel registra automaticamente todos os comandos dentro do diretório `app/Console/Commands`. No entanto, você pode instruir o Laravel a escanear outros diretórios em busca de comandos Artisan usando o método `withCommands` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

Se necessário, você também pode registrar comandos manualmente fornecendo o nome da classe do comando ao método `withCommands`:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Quando o Artisan é inicializado, todos os comandos da sua aplicação serão resolvidos pelo [container de serviço](../container/) e registrados com o Artisan.

<a id="programmatically-executing-commands"></a>
## Executando Comandos Programaticamente

Às vezes você pode querer executar um comando Artisan fora da CLI. Por exemplo, você pode querer executar um comando Artisan a partir de uma rota ou controller. Você pode usar o método `call` na facade `Artisan` para fazer isso. O método `call` aceita o nome da assinatura do comando ou o nome da classe como seu primeiro argumento, e um array de parâmetros do comando como o segundo argumento. O código de saída será retornado:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

Alternativamente, você pode passar o comando Artisan inteiro ao método `call` como uma string:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a id="passing-array-values"></a>
#### Passando Valores de Array

Se o seu comando define uma opção que aceita um array, você pode passar um array de valores para essa opção:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a id="passing-boolean-values"></a>
#### Passando Valores Booleanos

Se você precisar especificar o valor de uma opção que não aceita valores string, como a flag `--force` no comando `migrate:refresh`, você deve passar `true` ou `false` como o valor da opção:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a id="queueing-artisan-commands"></a>
#### Enfileirando Comandos Artisan

Usando o método `queue` na facade `Artisan`, você pode até mesmo enfileirar comandos Artisan para que sejam processados em segundo plano pelos seus [queue workers](../queues/). Antes de usar este método, certifique-se de ter configurado sua fila e de estar executando um queue listener:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

Usando os métodos `onConnection` e `onQueue`, você pode especificar a conexão ou a fila para a qual o comando Artisan deve ser despachado:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a id="calling-commands-from-other-commands"></a>
### Chamando Comandos a Partir de Outros Comandos

Às vezes você pode querer chamar outros comandos a partir de um comando Artisan existente. Você pode fazer isso usando o método `call`. Este método `call` aceita o nome do comando e um array de argumentos / opções do comando:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

Se você gostaria de chamar outro comando de console e suprimir toda a sua saída, você pode usar o método `callSilently`. O método `callSilently` tem a mesma assinatura que o método `call`:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a id="signal-handling"></a>
## Tratamento de Sinais

Como você deve saber, os sistemas operacionais permitem que sinais sejam enviados a processos em execução. Por exemplo, o sinal `SIGTERM` é a forma como os sistemas operacionais pedem que um programa seja encerrado de forma controlada. Se você desejar ouvir sinais nos seus comandos de console Artisan e executar código quando eles ocorrerem, você pode usar o método `trap`:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

Para ouvir múltiplos sinais de uma vez, você pode fornecer um array de sinais ao método `trap`:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a id="the-dev-command"></a>
## O Comando Dev

O comando Artisan `dev` inicia todos os processos necessários para o desenvolvimento local em uma única janela de terminal. Por padrão, ele executa simultaneamente o servidor de desenvolvimento PHP, um queue worker, o acompanhamento de logs via [Pail](../logging/#tailing-log-messages-using-pail) e a compilação de assets do Vite:

```shell
php artisan dev
```

Nos bastidores, o comando `dev` usa o pacote npm `@laravel/multiplex` para gerenciar os processos, dando a cada processo sua própria aba com saída pesquisável e rolável. Cada processo é rotulado e codificado por cores para que você possa facilmente distinguir entre eles. Se um processo travar, ele será reiniciado automaticamente e, quando você sair, toda a saída é escrita de volta no seu terminal para que nada seja perdido.

> **Nota:**
> O comando `dev` requer Node 22.13 ou posterior. No Windows, ele recorre ao pacote npm `concurrently` e a interface com abas não está disponível.

Os processos padrão são:

| Nome | Comando |
| --- | --- |
| `server` | `php artisan serve` |
| `queue` | `php artisan queue:listen --tries=1 --timeout=0` |
| `logs` | `php artisan pail --timeout=0` |
| `vite` | `npm run dev` |

> **Nota:**
> O processo `vite` detecta automaticamente seu gerenciador de pacotes Node (npm, pnpm, Yarn ou Bun) e usa o comando de execução apropriado.

<a id="customizing-dev-processes"></a>
### Personalizando Processos Dev

Você pode personalizar os processos que o comando `dev` executa usando a classe `DevCommands`, normalmente dentro do método `boot` do `AppServiceProvider` da sua aplicação. O método `register` aceita uma string de comando e um nome opcional:

```php
use Illuminate\Foundation\DevCommands;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    DevCommands::register('some-command --flag', 'my-process');
}
```

Ao registrar um comando Artisan, você pode usar o método `artisan`, que automaticamente prefixa o comando com `php artisan`:

```php
DevCommands::artisan('horizon', 'horizon');
```

Da mesma forma, o método `node` prefixa o comando com o comando de execução do gerenciador de pacotes detectado (ex.: `npm run`), e o método `nodeExec` prefixa o comando com o comando exec do gerenciador de pacotes (ex.: `npx`):

```php
DevCommands::node('storybook', 'storybook');

DevCommands::nodeExec('tailwindcss -i resources/css/app.css -o public/css/app.css --watch', 'tailwind');
```

Se você registrar um processo com o mesmo nome de um processo padrão, seu processo substituirá o padrão. Por exemplo, você pode personalizar o processo do servidor para usar uma porta diferente:

```php
DevCommands::artisan('serve --host=localhost --port=9000', 'server');
```

Você também pode personalizar a cor do rótulo de um processo no seu terminal. Os métodos de cor disponíveis são `blue`, `purple`, `pink`, `orange`, `green` e `yellow`. Você também pode passar uma cor hexadecimal personalizada ao método `color`:

```php
DevCommands::register('my-command', 'my-process')->green();

DevCommands::register('my-command', 'my-process')->color('#ff6347');
```

Para ver todos os processos dev registrados sem iniciá-los, use o comando `dev:list`:

```shell
php artisan dev:list
```

<a id="restarting-failed-processes"></a>
#### Reiniciando Processos com Falha

Se um processo travar, o Laravel o reiniciará após um curto atraso, até cinco vezes, antes de marcá-lo como falho. Um processo que morre dentro de um segundo após iniciar não é reiniciado, pois provavelmente nunca iniciou com sucesso em primeiro lugar. Reiniciar um processo manualmente com `r` reinicia o contador.

Você pode desativar esse comportamento para uma única execução usando a opção `--no-restart`:

```shell
php artisan dev --no-restart
```

Ou, você pode desativá-lo para toda a sua aplicação usando o método `disableAutoRestart`:

```php
DevCommands::disableAutoRestart();
```

<a id="filtering-dev-processes"></a>
### Filtrando Processos Dev

Você pode instruir o comando `dev` a executar apenas processos específicos quando ele for invocado usando o método `only`. Da mesma forma, você pode excluir processos específicos usando o método `except`:

```php
// Only run the server and vite processes...
DevCommands::only('server', 'vite');

// Run all processes except the queue worker...
DevCommands::except('queue');
```

Você pode excluir comandos registrados por pacotes ou os comandos padrão do Laravel usando os métodos `withoutVendorCommands` e `withoutDefaultCommands`:

```php
DevCommands::withoutVendorCommands();

DevCommands::withoutDefaultCommands();
```

<a id="stub-customization"></a>
## Personalização de Stubs

Os comandos `make` do console Artisan são usados para criar uma variedade de classes, como controllers, jobs, migrations e tests. Essas classes são geradas usando arquivos "stub" que são preenchidos com valores com base na sua entrada. No entanto, você pode querer fazer pequenas alterações nos arquivos gerados pelo Artisan. Para fazer isso, você pode usar o comando `stub:publish` para publicar os stubs mais comuns na sua aplicação, de modo que você possa personalizá-los:

```shell
php artisan stub:publish
```

Os stubs publicados estarão localizados dentro de um diretório `stubs` na raiz da sua aplicação. Quaisquer alterações que você fizer nesses stubs serão refletidas quando você gerar suas classes correspondentes usando os comandos `make` do Artisan.

<a id="events"></a>
## Eventos

O Artisan despacha três eventos ao executar comandos: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting` e `Illuminate\Console\Events\CommandFinished`. O evento `ArtisanStarting` é despachado imediatamente quando o Artisan começa a ser executado. Em seguida, o evento `CommandStarting` é despachado imediatamente antes de um comando ser executado. Por fim, o evento `CommandFinished` é despachado assim que um comando termina de ser executado.

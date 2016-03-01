# Artisan Console

- [Introdução](#introduction)
- [Escrevendo comandos](#writing-commands)
    - [Estrutura de um comando](#command-structure)
- [Entrada e Saída (I/O) de um comando ](#command-io)
    - [Definindo possíveis entradas](#defining-input-expectations)
    - [Obtendo a entrada](#retrieving-input)
    - [Perguntando](#prompting-for-input)
    - [Escrevendo a saída](#writing-output)
- [Registrando comandos](#registering-commands)
- [Chamando comandos a partir do código](#calling-commands-via-code)

<a name="introduction"></a>
## Introdução

Artisan é o nome da interface para linha de comando incluida que faz parte do Laravel. Ele provê inúmeros comandos úteis que você pode usar enquanto desenvolve sua aplicacação. Ele é baseado no poderoso componente Symfony Console. Para visualizar a lista de comandos disponíveis, você pode usar o comando `list`:

    php artisan list

Cada comando inclui também uma tela de ajuda ("help") que exibe e descreve os possíveis argumentos e opções disponíveis. Para visualizar a tela de ajuda, basta informar antes do nome do comando, a palavra `help`:

    php artisan help migrate

<a name="writing-commands"></a>
## Escrevendo comandos

Além dos comandos fornecidos pelo Artisan, você talvez queira criar seus próprios comandos customizados para sua aplicação. Você pode armazenar seus comandos customizados no diretório `app/Console/Commands`; porém, você é livre para escolher outro local para armazená-los, desde que seus comandos estejam sendo carregados com base nas configurações do seu arquivo `composer.json`.

Para criar um novo comando, você pode utilizar o comando `make:console` do próprio Artisan, que irá gerar um comando básico para te ajudar a começar:

    php artisan make:console SendEmails

O comando acima iria gerar uma classe em `app/Console/Commands/SendEmails.php`. No momento da criação do comando, a opção `--command` pode também ser usada para definir o nome ao qual o comando irá atender quando invocado na linha de comando:

    php artisan make:console SendEmails --command=emails:send

<a name="command-structure"></a>
### Estrutura de um comando

Uma vez que seu comando foi gerado, você pode preencher as propriedades `signature` (assinatura) e `description` (descrição) da classe, que serão usadas pelo Artisan quando o mesmo estiver listando os comandos disponíveis através do comando `list`.

O método `handle` será chamado automaticamente quando seu comando for executado. Você pode colocar qualquer lógica ali dentro. Vamos dar uma olhada em um comando de exemplo.

Veja que nós podemos injetar qualquer dependência necessária no construtor do método. O [service container](/docs/{{version}}/container) do Laravel irá automaticamente injetar todas as dependências definidas com tipo (type-hint) no construtor. Para melhor reusabilidade, aconselho deixar seus comandos "leves" e deixar o [service container](/docs/{{version}}/container) tomar conta da resolução das dependências.

    <?php namespace App\Console\Commands;

    use App\User;
    use App\DripEmailer;
    use Illuminate\Console\Command;
    use Illuminate\Foundation\Inspiring;

    class Inspire extends Command
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'email:send {user}';

        /**
         * The console command description.
         *
         * @var string
         */
        protected $description = 'Send drip e-mails to a user';

        /**
         * The drip e-mail service.
         *
         * @var DripEmailer
         */
        protected $drip;

        /**
         * Create a new command instance.
         *
         * @param  DripEmailer  $drip
         * @return void
         */
        public function __construct(DripEmailer $drip)
        {
            parent::__construct();

            $this->drip = $drip;
        }

        /**
         * Execute the console command.
         *
         * @return mixed
         */
        public function handle()
        {
            $this->drip->send(User::find($this->argument('user')));
        }
    }

<a name="command-io"></a>
## Entrada e Saída (I/O) de uma comando

<a name="defining-input-expectations"></a>
### Definindo possíveis entradas

Ao desenvolver um comando, é comum que você necessite obter a alguma entrada do usuário no momento da execução, o que pode ser feito através de argumentos ou opções (arguments and options). O Laravel torna a tarefa de definir qual entrada esperar do usuário utilizando a propriedade de `signature` (assinatura) em seus comandos. A propriedade `signature` permite você definir o nome, os argumentos e opções para o comando em uma forma simples, expressiva, semelhante o que você já faz nas suas rotas.

Todos os argumentos e opções que podem ser utilizadas pelo usuário devem estar entre chaves {}:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user}';

Nesse exemplo, o comando define um argumento **obrigatório** : `user`. Mas é claro, você também pode definir um argumento como opcional a ainda definir um um valor padrão para os casos onde o usuário tenha omitido a informação:

    // Argumento Opcional...
    email:send {user?}

    // Argumento Opcional com valor padrão...
    email:send {user=foo}

Opções, assim como argumentos, também são uma forma de entrada. Todavia, opções são utilizadas com o prefixo `--` (dois traços). Podemos definir opções na assinatura do comando da seguinte forma:

    /**
     * O nome e assinatura do comando.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue}';

Nesse exemplo, a opção `--queue` pode ser especificada pelo comando Artisan. Se a opção `--queue` for utilizada, o valor dessa opção será `true`. Caso contrário, o valor será `false`:

    php artisan email:send 1 --queue

Você também pode especificar que a opção receberá um valor, isso pode ser feito especificano o sinal `=` (igualdade), o que indica ao Artisan que um valor deve ser passado:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue=}';

No exemplo, o usuário poderá passar um valor junto a opção, da seguinte forma:

    php artisan email:send 1 --queue=default

É claro, você também pode definir valores padrão para as opções:

    email:send {user} {--queue=default}

<a name="retrieving-input"></a>
### Obtendo entrada

Quando seu comando for executado, você obviamente irá precisar acessar os valores passados pelo usuário nas opções e argumentos. Para isso, você pode utilizar os métodos `argument` e `option` :

Para obter o valor passado a um argumento, use o método `argument`:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

Se você precisar obter todos os argumentos ao mesmo tempo, em formato de `array`, é só chamar o método `argument` sem passar parâmetro algum:

    $arguments = $this->argument();

Opções podem ser obtidas tão facilmente quanto os argumentos, porem através do método `option`. Assim como o método `argument`, você pode chamar o método `option` sem argumentos para obter todas as opções em fomato de `array`:

    // Obter a valor passado em uma opção...
    $queueName = $this->option('queue');

    // Obter os valores de todas as opções...
    $options = $this->option();

<a name="prompting-for-input"></a>
### Perguntando

Além de exibir alguma saída, você pode também pedir ao usuário que forneça algum valor durante a execução do comando. O método `ask` irá aguardar a entrada do usuário, aceitar a entrada, e então retorná-la para o comando:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('What is your name?');
    }

O método `secret` é similiar ao método `ask`, porém a entrada fornecida pelo usuário não será visivel enquanto ele a digita. Esse método é útil quando a pergunta em questão espera uma resposta que contenha informações sensíveis, como senhas:

    $password = $this->secret('What is the password?');

#### Pedindo confirmação

Se precisar de uma simples confirmação, você pode usar o método `confirm`. Por padrão, esse método irá retornar `false` para qualquer entrada, exceto quando a entrada for igual a `y`, nesse caso, o método retornará `true`.

    if ($this->confirm('Do you wish to continue? [y|N]')) {
        //
    }

#### Dando escolhas ao usuário

O método `anticipate` pode ser usado para completar automaticamente as escolhas possíveis. O usuário ainda continuará podendo escolher qualquer valor, independente das opções que você fornecer.

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

Se precisar fornecer ao usuário um conjunto predefinido de escolhas, você pode utilizar o método `choice`. O usuário irá escolher uma opção em uma lista de respostas e o valor escolhido será retornado a você. Você pode ainda, definir o valor padrão caso nenhuma escolha seja feita pelo usuário:

    $name = $this->choice('What is your name?', ['Taylor', 'Dayle'], false);

<a name="writing-output"></a>
### Escrevendo a saída

Para enviar informação ao console, você pode utilizar os métodos `info`, `comment`, `question` e `error`. Cada um desses métodos irá utilizar a cor **ANSI** apropriada.

Para exibir uma mensagem informativa ao usuário, utilize o método `info`. Tipicamente, a mensagem será exibida no console na cor verde:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->info('Display this on the screen');
    }

Para exibir uma mensagem de erro, use o método `error`. Mensagens de erro são tipicamente exibidas em vermelho:

    $this->error('Something went wrong!');

#### Layout de tabelas

O método `table` torna fácil a tarefa de exibir multiplas colunas e linhas de dados formatados. Apenas passe os cabeçalhos e linhas ao método. A largura e altura da tabela serão automaticamente calculados baseado nos dados passados:

    $headers = ['Name', 'Email'];

    $users = App\User::all(['name', 'email'])->toArray();

    $this->table($headers, $users);

#### Barras de progresso

Para tarefas demoradas, é útil exibir ao usuário um indicador de progresso. Usando objeto de saída, podemos iniciar, avançar e parar uma barra de progresso. Você precisa definir o número de passos ao iniciar, e então ir avançando a barra a cada passo:

    $users = App\User::all();

    $this->output->progressStart(count($users));

    foreach ($users as $user) {
        $this->performTask($user);

        $this->output->progressAdvance();
    }

    $this->output->progressFinish();

Para opções avançadas, confira [Symfony Progress Bar component documentation](http://symfony.com/doc/2.7/components/console/helpers/progressbar.html).

<a name="registering-commands"></a>
## Registrando comandos

Uma vêz que seu comando está concluído, será necessário registrá-lo junto ao Artisan para que o mesmo esteja disponível para uso. Isso pode ser feito no arquivo `app/Console/Kernel.php`.

Nesse arquivo, você irá encontrar uma lista de comandos na propriedade `commands`. Para registrar seu comando, adicione o nome da classe a essa lista. Quando o Artisan inicia, todos os comandos listados serão resolvidos pelo [service container](/docs/{{version}}/container) e registrados no Artisan:

    protected $commands = [
        'App\Console\Commands\SendEmails'
    ];

<a name="calling-commands-via-code"></a>
## Chamando comandos a partir do código

Algumas vezes, você talvez precise executar um comando fora do console. Por exemplo, você talvez queira disparar um comando do Artisan a partir de uma rota ou controller. Para fazer isso, você pode utilizar o método `call` da Facade `Artisan`. O método `call` aceita o nome do comando a ser executado como o primeiro parâmetro, e um array de argumentos e opções como segundo parâmetro. O retorno do método `call` é o código de saida do comando:

    Route::get('/foo', function () {
        $exitCode = Artisan::call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

Usando o método `queue` da Facade `Artisan`, você pode colocar um comando para ser executado em fila, afim de que os mesmo sejam executados em plano de fundo pelos seus [queue workers](/docs/{{version}}/queues):

    Route::get('/foo', function () {
        Artisan::queue('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

### Chamando comandos a partir de outros comandos

Pode ser que você precisa chamar um comando a partir de outro comando. O mesmo também pode feito através do método (local) `call`. Esse método `call` aceita o nome do comando e um array com a uma lista de opções e argumentos:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    }

Se você precisar chamar um comando e suprimir toda saída gerado pelo mesmo, você pode utilizar o método `callSilent`. Esse método tem a mesma assinatura que o método `call`:

    $this->callSilent('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);

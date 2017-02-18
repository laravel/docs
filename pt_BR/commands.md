# Desenvolvimento para Artisan

- [Introdução](#introduction)
- [Construindo um Comando](#building-a-command)
- [Registrando Comandos](#registering-commands)

<a name="introduction"></a>
## Introdução

Além dos comandos fornecidos com o Artisan, você também pode construir seus próprios comandos customizados para trabalhar com a sua aplicação. Você pode armazenar seus comandos customizados no diretório `app/Console/Commands`, mas você é livre para escolher seu próprio local de armazenamento desde que seus comandos possam ser carregados, baseado nas configurações do `composer.json`.

<a name="building-a-command"></a>
## Construindo um Comando

### Gerando uma Classe

Para criar um novo comando, você pode usar o comando do Artisan `make:console`, que ira criar um pedaço de código de um comando para ajudá-lo a começar:

#### Gerando uma nova Command Class

	php artisan make:console FooCommand

O comando acima irá gerar a classe em `app/Console/Commands/FooCommand.php`.

Quando o comando estiver criado, a opção `--command` pode ser usada para atribuir um nome de comando para uso no terminal:

	php artisan make:console AssignUsers --command=users:assign

### Escrevendo o Comando

Uma vez com seu comando gerado, você deve preencher as propriedades `name` e `description` da classe, as quais serão usadas quando seu comando for exibido na tela `list`.

O método `fire` será chamado quando seu comando for executado. Você pode inserir qualquer lógica de comando nesse método.

### Argumentos e Opções

Os métodos `getArguments` e `getOptions` são aqueles onde você pode definir qualquer argumento ou opções que seu comando recebe. Ambos os métodos retornam um array de comandos, que são descritos por uma lista de opções de array.

Ao definir `arguments`, o array de valores é representado a seguir:

	[$name, $mode, $description, $defaultValue]

O argumento `mode` pode ser um deles: `InputArgument::REQUIRED` ou `InputArgument::OPTIONAL`.

Ao definir `options`, o array de valores será o seguinte:

	[$name, $shortcut, $mode, $description, $defaultValue]

Para options, o argumento `mode` pode ser: `InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`.

O modo `VALUE_IS_ARRAY` indica que o seletor pode ser usado várias vezes ao chamar o comando:

	InputOption::VALUE_REQUIRED | InputOption::VALUE_IS_ARRAY

Permitiria, então, para este comando:

	php artisan foo --option=bar --option=baz

A opção `VALUE_NONE` indica que a opção é simplesmente usada como um "interruptor":

	php artisan foo --option

### Recuperando Input

Enquanto seu comando está sendo executado, você obviamente precisará acessar os valores para os argumentos e opções aceitos por sua aplicação. Para fazer isso, pode usar os métodos `argument` e `option`:

#### Recuperando o Valor do Argumento de um Comando

	$value = $this->argument('name');

#### Recuperando Todos os Argumentos

	$arguments = $this->argument();

#### Recuperando o Valor da Opção de um Comando

	$value = $this->option('name');

#### Recuperando todas as Opções

	$options = $this->option();

### Escrevendo uma Saída

Para enviar uma saída ao console, você deve usar os métodos `info`, `comment`, `question` e `error`. Cada um desses métodos vai usar as cores ANSI apropriadas para seus propósitos.

#### Enviando Informação para o Console

	$this->info('Display this on the screen');

#### Enviando uma Mensagem de Erro para o Console

	$this->error('Something went wrong!');

### Fazendo Perguntas

Você pode também usar os métodos `ask` e `confirm` para solicitar uma entrada do usuário:

#### Pedindo uma Entrada do Usuário

	$name = $this->ask('What is your name?');

#### Pedindo uma Entrada Secreta do Usuário

	$password = $this->secret('What is the password?');

#### Pedindo Confirmação do Usuário

	if ($this->confirm('Do you wish to continue? [yes|no]'))
	{
		//
	}

Você pode também especificar um valor padrão para o método `confirm`, que pode ser `true` ou `false`:

	$this->confirm($question, true);

### Chamando outros Comandos

Algumas vezes você pode precisar chamar outros comandos a partir do seu comando criado. Você pode fazer isso usando o método `call`:

	$this->call('command:name', ['argument' => 'foo', '--option' => 'bar']);

<a name="registering-commands"></a>
## Registrando Comandos

#### Registrando um Comando do Artisan

Com o seu comando concluído, você precisa registrá-lo com o Artisan para que ele fique disponível para uso. Isso é normalmente feito no arquivo `app/Console/Kernel.php`. Neste arquivo, você encontrará uma lista de comandos na propriedade `commands`. Para registrar seu comando basta adicioná-lo a essa lista. 

	protected $commands = [
		'App\Console\Commands\FooCommand'
	];

Quando o Artisan for inicializado, todos os comandos listados nesta propriedade serão resolvidos pelo [service container](/docs/{{version}}/container) e registrados pelo Artisan.

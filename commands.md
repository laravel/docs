# Artisan Development

- [Introdução](#introduction)
- [Building A Command](#building-a-command)
- [Registering Commands](#registering-commands)

<a name="introduction"></a>
## Introdução

In addition to the commands provided with Artisan, you may also build your own custom commands for working with your application. You may store your custom commands in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be autoloaded based on your `composer.json` settings.

<a name="building-a-command"></a>
## Construindo um Comando

### Gerando a Classe

Para criar um novo comando, você pode usar o comando Artisan `make:console`, que gerará um esboço do comando para ajudar você a começar:

#### Gerando uma Nova Classe de Comando

	php artisan make:console FooCommand

O comando acima irá gerar a clsse em `app/Console/FooCommand.php`.

Quando nos estamos criando um comando, a opção `--command` pode ser usada para atribuir o nome do comando no terminal:

	php artisan make:console AssignUsers --command=users:assign

### Escrevendo o Comando

Uma vez que o seu comando é gerado, você deve preencher o `nome` e `descrição` propriedades da classe, que irá ser utilizada quando seu comando for mostrado na tela de listagem `list`.

O método `fire` irá ser chamado quando seu comando é executado. Você pode colocar qualquer lógica de comando neste método. 

### Argumentos e Opções

Os métodos `getArguments` e `getOptions` é onde você define qualquer parâmetro ou opção que o seu comando pode receber.
Ambos dos méotoso retornam um array de comandos, que são descritos por uma lista de array de opções.

Quando se está definindo `arguments` (parâmetros), os valores de definição do array representam o seguinte.  

	array($name, $mode, $description, $defaultValue)

The argument `mode` may be any of the following: `InputArgument::REQUIRED` or `InputArgument::OPTIONAL`.

When defining `options`, the array definition values represent the following:

	array($name, $shortcut, $mode, $description, $defaultValue)

For options, the argument `mode` may be: `InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`.

The `VALUE_IS_ARRAY` mode indicates that the switch may be used multiple times when calling the command:

	php artisan foo --option=bar --option=baz

The `VALUE_NONE` option indicates that the option is simply used as a "switch":

	php artisan foo --option

### Retrieving Input

While your command is executing, you will obviously need to access the values for the arguments and options accepted by your application. To do so, you may use the `argument` and `option` methods:

#### Retrieving The Value Of A Command Argument

	$value = $this->argument('name');

#### Retrieving All Arguments

	$arguments = $this->argument();

#### Retrieving The Value Of A Command Option

	$value = $this->option('name');

#### Retrieving All Options

	$options = $this->option();

### Writing Output

To send output to the console, you may use the `info`, `comment`, `question` and `error` methods. Each of these methods will use the appropriate ANSI colors for their purpose.

#### Sending Information To The Console

	$this->info('Display this on the screen');

#### Sending An Error Message To The Console

	$this->error('Something went wrong!');

### Asking Questions

You may also use the `ask` and `confirm` methods to prompt the user for input:

#### Asking The User For Input

	$name = $this->ask('What is your name?');

#### Asking The User For Secret Input

	$password = $this->secret('What is the password?');

#### Asking The User For Confirmation

	if ($this->confirm('Do you wish to continue? [yes|no]'))
	{
		//
	}

You may also specify a default value to the `confirm` method, which should be `true` or `false`:

	$this->confirm($question, true);

### Calling Other Commands

Sometimes you may wish to call other commands from your command. You may do so using the `call` method:

	$this->call('command:name', ['argument' => 'foo', '--option' => 'bar']);

<a name="registering-commands"></a>
## Registering Commands

#### Registering An Artisan Command

Once your command is finished, you need to register it with Artisan so it will be available for use. This is typically done in the `app/Console/Kernel.php` file. Within this file, you will find a list of commands in the `commands` property. To register your command, simply add it to this list. When Artisan boots, all the commands listed in this property will be resolved by the [IoC container](/docs/5.0/container) and registered with Artisan.

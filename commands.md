# Artisan Development

- [Introdução](#introduction)
- [Construindo um Comando](#building-a-command)
- [Registrando Comandos](#registering-commands)

<a name="introduction"></a>
## Introdução

Além dos comandos fornecidos pelo Artisan, você pode também criar os seus comandos personalizados para trabalhar com sua aplicação. Você pode armazenar seus comandos personalizados no diretório `app/Console/Commands`; no entanto, você é livre para escolher a localização do seu diretório de armazenamento, desde que seus comandos possam ser carregados automaticamente baseados nas configurações do seu `composer.json`.

<a name="building-a-command"></a>
## Construindo um Comando

### Gerando a Classe

Para criar um novo comando, você pode usar o comando Artisan `make:console`, que gerará um esboço do comando para ajudar você a começar:

#### Gerando uma Nova Classe de Comando

	php artisan make:console FooCommand

O comando acima irá gerar a classe em `app/Console/FooCommand.php`.

Quando nos estamos criando um comando, a opção `--command` pode ser usada para atribuir o nome do comando no terminal:

	php artisan make:console AssignUsers --command=users:assign

### Escrevendo o Comando

Uma vez que o seu comando é gerado, você deve preencher o `nome` e `descrição` propriedades da classe, que irá ser utilizada quando seu comando for mostrado na tela de listagem `list`.

O método `fire` irá ser chamado quando seu comando é executado. Você pode colocar qualquer lógica de comando neste método. 

### Argumentos e Opções

Os métodos `getArguments` e `getOptions` é onde você define qualquer parâmetro ou opção que o seu comando pode receber.
Ambos os métodos retornam um array de comandos, que são descritos por uma lista de array de opções.

Quando se está definindo `arguments` (parâmetros), os valores de definição do array representam o seguinte.  

	[$name, $mode, $description, $defaultValue]

O parâmetro `mode` oide ser qualquer um dos seguintes:`InputArgument::REQUIRED` ou `InputArgument::OPTIONAL`.

Quando estamos definindo `options`, o valores de definição do array representam o seguinte: 

	[$name, $shortcut, $mode, $description, $defaultValue]

Para opções, o parâmetro `mode` pode ser: `InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`.

O modo `VALUE_IS_ARRAY` indica que a chave pode ser usado várias vezes ao chamar o comando:

	InputOption::VALUE_REQUIRED | InputOption::VALUE_IS_ARRAY
	
Would then allow for this command:

	php artisan foo --option=bar --option=baz

A opção `VALUE_NONE` indica que a opção é simplesmente usada como uma "chave": 

	php artisan foo --option

### Recuperando o Input

Enquanto o seu comando é executado, você obviamente precisa do acesso aos valores para os argumentos e opções aceitas pela sua aplicação. Para isto, você pode usar os métodos `argument` e `option`:

#### Recuperando O Valor De Um Argumento de Comando 

	$value = $this->argument('name');

#### Recuperando Todos os Argumentos

	$arguments = $this->argument();

#### Recuperando O Valor De Uma Opção de Comando 

	$value = $this->option('name');

#### Recuperando todas as Opções 

	$options = $this->option();

### Escrevendo Output (Saídas) 

Para mandar saídas para o seu console, você pode usar os métodos de `info`, `comment`, `question` and `error`. Cada um destes métodos usará a cor ANSI apropriada para sua finalidade.

#### Enviando Informação Para o Console

	$this->info('Display this on the screen');

#### Enviando Uma Mensagem De Erro Para O Console

	$this->error('Something went wrong!');

### Fazendo Perguntas

Você pode também usar os métodos `ask` e `confirm` para para solicitar entradas no console para o usuário:

#### Fazendo Perguntas Ao Usuário

	$name = $this->ask('What is your name?');

#### Pergutando Ao Usuário Por Uma Entrada Secreta

	$password = $this->secret('What is the password?');

#### Pergutando O Usuário Por Confirmação

	if ($this->confirm('Do you wish to continue? [yes|no]'))
	{
		//
	}

Você também pode especificar um valor default para o método `confirm`, que deve ser `true` ou `false`

	$this->confirm($question, true);

### Chamando Outros Comandos

Algumas vezes você pode desejar chamar outros comandos a partir do seu. Você pode fazer isto usando o método `call`:

	$this->call('command:name', ['argument' => 'foo', '--option' => 'bar']);

<a name="registering-commands"></a>
## Registrando Comandos

#### Registrando o Comando Artisan

Uma vez que seu comando estiver pronto, você precisa registrar o mesmo com Artisan então ele ficará disponível para uso. Isto é geralmente feito no arquivo `app/Console/Kernel.php`. Dentro deste arquivo, você irá encontrar uma lista de comandos na propriedade `commands`. Para registrar o seu comando, você simplesmente deve adiciona-lo à esta lista. Quando o Artisan inicializar, todos os comandos listados na propriedade `commands` que serão resolvidos pelo [service container](/docs/master/container)  e registrados no Artisan. 

# Requisições HTTP

- [Acessando a Requisição](#accessing-the-request)
	- [Informações Básicas Sobre a Requisição](#basic-request-information)
	- [Requisições PSR-7](#psr7-requests)
- [Obentendo o Input](#retrieving-input)
	- [Dados Anteriores](#old-input)
	- [Cookies](#cookies)
	- [Arquivos](#files)

<a name="accessing-the-request"></a>
## Acessando o Requisição

Para obter uma instância da atual requisição HTTP via injeção de dependência, você pode indicar o tipo da variável (type-hint) para a classe `Illuminate\Http\Request` no construtor do seu controller ou num método. Uma instância da requisição atual será automaticamente injetada pelo [service container](/docs/{{version}}/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}
	}

Se o método do seu controller também espera dados vindos dos parametros da rota, simplesmente liste os argumentos da rota depois das outras dependências. Por exemplo, se sua rota é definida como:

	Route::put('user/{id}', 'UserController@update');

Você ainda deve indicar o tipo `Illuminate\Http\Request` e passar o parametro `id` da sua rota definindo método do seu controller da seguinte maneira:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Update the specified user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}
	}

<a name="basic-request-information"></a>
### Informações Básicas da Requisição

Uma instância de `Illuminate\Http\Request` provê uma variedade de métodos para examinar a requisição HTTP da sua aplicação. Essa classe estende a `Symfony\Component\HttpFoundation\Request`. Aqui estão alguns métodos úteis que estão disponíveis nessa classe:

#### Obtendo a URI da Requisição

O método `path` retorna a URI da requisição. Então, se a requisição for para `http://domain.com/foo/bar`, o método `path` retornará `foo/bar`:

	$uri = $request->path();

O método `is` permite que você verifique se a URI da requisição combina com um determinado padrão. Você pode usar o caractere `*` como coringa quando utilizar essa método:

	if ($request->is('admin/*')) {
		//
	}

Para obter a URL completa, não somente o caminho, você pode usar o método `url` da instância da requisição:

	$url = $request->url();

#### Obtendo o Método da Requisição (verbo HTTP)

O método `method` retornará o verbo HTTP (get, post, delete ...) da requisição. Você também pode usar o método `isMethod` para verificar se o verbo HTTP combina com a string passada como argumento:

	$method = $request->method();

	if ($request->isMethod('post')) {
		//
	}

<a name="psr7-requests"></a>
### Requisições PSR-7

O padrão PSR-7 especifica a interface para mensagens HTTP, incluindo requisições e respostas. Se você gostaria de obter uma instância da requisição PSR-7, você precisa instalar algumas bibliotecas. O Laravel usa o componente Symfony HTTP Message Bridge par aconverter uma requisição típica do Laravel em requisições e respostas em compatibilidade com o padrão PSR-7.

	composer require symfony/psr-http-message-bridge

	composer require zendframework/zend-diactoros

Uma vez instaladas estas biblitecas, você pode obter uma requisição PSR-7 simplesmente indicando o tipo da requisição na sua rota ou controller:

	use Psr\Http\Message\ServerRequestInterface;

	Route::get('/', function (ServerRequestInterface $request) {
		//
	});

Se você retornar uma resposta PSR-7 a partir da rota ou do controller ela será automaticamente convertida de volta a uma instância de resposta Laravel e exibida pelo framework.

<a name="retrieving-input"></a>
## Obtendo os Dados da Requisição

#### Obtendo Valores dos Dados da Requisição

Usando alguns métodos simples, você pode acessar todos os valores enviados pelo usuário a partir da sua instância de `Illuminate\Http\Request`. Você não precisa se preocupar com o verbo HTTP usado na requisição, os dados são acessados da mesma forma para todos os verbos.

	$name = $request->input('name');

Você pode passar um valor padrão como segundo argumento do método `input`. Esse valor será retornado se não houver o campo nos dados da requisição:

	$name = $request->input('name', 'Sally');

Quando trabalha com formulários que contém array, você pode usar a notação "dot" (ponto) para acessar os índices:

	$input = $request->input('products.0.name');

#### Determinando se Existe um Campo na Requisição

Para determinar se um valor está está presente na requisição, você pode usar o método `has`. Ele retornará `true` se o valor estiver presente **E**  não é uma string vazia:

	if ($request->has('name')) {
		//
	}

#### Obtendo Todos os Dados

Você pode obter todos os dados da requisição como um `array` usando o método `all`:

	$input = $request->all();

#### Obtendo Uma Parte dos Dados

Se você só precisa de um sub-conjunto dos dados, você pode usar os métodos `only` ou `except`. Ambos aceitam um `array` como argumento:

    // Retornará somente (only) os campos 'username' e 'password'
	$input = $request->only('username', 'password');

    // Retornará todos os campos exceto (except) o campo 'credit_card'
	$input = $request->except('credit_card');

<a name="old-input"></a>
### Dados Anteriores da Sessão

O Laravel permite que você mantenha os dados de uma requisição durante a próxima requisição. Essa particulariedade é útil para repopular formulários depois de detectar algum erro. Entretanto, se você está usando o [serviço de validação](/docs/{{version}}/validation) do Laravel, é improvável que você vá precisar usar algum desses métodos manualmente, assim como algumas das facilidades que o Laravel trás internamente, o serviço de validação os usará automagicamente:

#### Enviando o Input Para a Sessão (Flash Input)

O método `flash` da instância de `Illuminate\Http\Request` enviará todos os dados da requisição atual para a [sessão](/docs/{{version}}/session) então assim eles estarão disponíveis durante a próxima requisição do usuário para a aplicação:

	$request->flash();

Você pode também usar os métodos `flashOnly` e `flashExcept` para enviar um subconjunto dos dados da requisição para a sessão:

	$request->flashOnly('username', 'email');

	$request->flashExcept('password');

#### Enviando Dados para Sessão e Então Redirecionar (Flash Input)

Muito provável que você queira enviar os dados para a sessão e então redirecionar para a página anterior, você pode fazer isso facilmente usando o método `withInput`:

	return redirect('form')->withInput();

	return redirect('form')->withInput($request->except('password'));

#### Obtendo Dados Enviados Para a Sessão (Old Input)

Para obter os dados enviados para a sessão da requisição anterior, use o método `old` da sua instância de `Illuminate\Http\Request`. O método `old` é um utilitário conveniente para obter esses dados da sessão:

	$username = $request->old('username');

O Laravel também provê a função utilitária global `old`. Se você for exibir os dados a partir de um [Template Blade](/docs/{{version}}/views), é mais conveniente usá-lo:

	{{ old('username') }}

<a name="cookies"></a>
### Cookies

#### Obtendo Cookies Da Requisição

Todos os cookies criados pelo Laravel são encriptados e assinados com um código de autenticação, isso significa que eles serão considerados inválidos se forem alterados pelo cliente. Para recuperar o valor de um cookie a partir da requisição, você pode usar o método `cookie` da sua instância de `Illuminate\Http\Request`:

	$value = $request->cookie('name');

#### Adicionando Novos Cookies À Resposta

O Laravel provê uma função utilitária global `cookie` que serve para gerar uma instância da classe `Symfony\Component\HttpFoundation\Cookie`. O cookie deve ser adicionado à sua instância de `Illuminate\Http\Response` usando o método `withCookie`:

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

	return $response;

Para criar um cookie de tempo de vida longo, que sobrevive por 5 anos, você pode usar a função utilitária `cookie` sem argumentos e então aninhar o método `forever`:

	$response->withCookie(cookie()->forever('name', 'value'));

<a name="files"></a>
### Arquivos

#### Recebendo Arquivos Enviados (Upload)

Você pode acessar arquivos enviados à requisição usando o método `file` da sua instância de `Illuminate\Http\Request`. O objeto retornado por esse método é uma instância da classe `Symfony\Component\HttpFoundation\File\UploadedFile`, que estende `SplFileInfo` e provê uma variedade de métodos para interagir com o arquivo.

	$file = $request->file('photo');

#### Verificando a Presença do Arquivo

Você também pode determinar se um arquivo está ou não na requisição usando o método `hasFile`:

	if ($request->hasFile('photo')) {
		//
	}

#### Validando Arquivos

Além de verificar a presença do arquivo, você também pode verificar se não houve problemas durante o envio com o método `isValid`:

	if ($request->file('photo')->isValid())
	{
		//
	}

#### Movendo Arquivos Enviados

Para mover um arquivo enviado para uma nova localização, você deve usar o método `move`. Esse método moverá o arquivo da sua localização temporária (determinada nas configurações do PHP) para um local permanente de sua escolha:

	$request->file('photo')->move($destinationPath);

	$request->file('photo')->move($destinationPath, $fileName);

#### Outros Métodos de Arquivos

Há uma variedade de métodos disponíveis na instância de `UploadedFile`. Para saber mais veja a [documentação da API dessa classe](http://api.symfony.com/2.7/Symfony/Component/HttpFoundation/File/UploadedFile.html).

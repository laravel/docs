# Errors & Logging

- [Introdução](#introduction)
- [Configuração](#configuration)
- [Manipulador de Exceções](#the-exception-handler)
	- [Método Report](#report-method)
	- [Método Render](#render-method)
- [HTTP Exceptions](#http-exceptions)
	- [Páginas de Erro HTTP Personalizadas](#custom-http-error-pages)
- [Logging](#logging)

<a name="introduction"></a>
## Introdução

Quando você inicia um novo projeto Laravel, erro e manipulação de exceção já estão configurados para você. Além disso, Laravel está integrado com a biblioteca de log [Monolog](https://github.com/Seldaek/monolog), que proporciona suporte para uma variedade de manipuladores de log poderosos.

<a name="configuration"></a>
## Configuração

#### Detalhes de Erros

A quantidade de detalhes de erros que sua aplicação exibe através do navegador é controlada pela opção de configuração `debug` no seu arquivo de configuração `config/app.php` . Por padrão, essa opção de configuração está definido para respeitar a variável de ambiente `APP_DEBUG`, que é armazenada no seu arquivo `.env`.

Para o desenvolvimento local, você deve definir a variável de ambiente `APP_DEBUG` como `true`. Em seu ambiente de produção, esse valor deve ser sempre `false`.

#### Modos de Log

O Laravel trás pronto para uso os modos de log `single`, `daily`, `syslog` e `errorlog`. Por exemplo, se você quiser usar arquivos de log diários em vez de um único arquivo, você deve simplesmente definir o valor `log` no seu arquivo de configuração `config/app.php`:

	'log' => 'daily'

#### Monolog Configuração Personalizada

Se você gostaria de ter controle completo sobre como Monolog está configurado em sua aplicação, você pode usar método `configureMonologUsing` da aplicação. Você deve fazer uma chamada para este método em seu arquivo `bootstrap/app.php` logo antes da variável `$app` ser retornada pelo arquivo:

	$app->configureMonologUsing(function($monolog) {
		$monolog->pushHandler(...);
	});

	return $app;

<a name="the-exception-handler"></a>
## Manipulador de Exceções

Todas as exceções são tratadas por `App\Exceptions\Handler`. Essa classe contém dois métodos: `report` e `render`. Vamos examinar cada um desses métodos em detalhes.

<a name="report-method"></a>
### Método Report

O método `report` é usado para exceções log ou enviá-los para um serviço externo como [BugSnag](https://bugsnag.com). Por padrão, o método `report` simplesmente passa a exceção para a classe base onde a exceção é registrada. No entanto, você é livre para fazer exceções de log como quiser.

Por exemplo, se você precisa relatar diferentes tipos de exceções de maneiras diferentes, você pode usar o operador de comparação PHP `instanceof`:

	/**
	 * Relatar ou registrar uma exceção.
	 *
	 * Este é um ótimo local para enviar exceções para Sentry, Bugsnag, etc.
	 *
	 * @param  \Exception  $e
	 * @return void
	 */
	public function report(Exception $e)
	{
		if ($e instanceof CustomException) {
			//
		}

		return parent::report($e);
	}

#### Ignorando Exceções Por Tipo

A propriedade `$dontReport` do manipulador de exceção contém um array de tipos de exceção que não serão registados. Por padrão, as exceções resultantes de erros 404 não são escritas em seus arquivos de log. Você pode adicionar outros tipos de exceção a esse array, conforme necessário.

<a name="render-method"></a>
### Método Render

O método `render` é responsável por converter uma determinada exceção em uma resposta HTTP que deve ser enviado de volta para o navegador. Por padrão, a exceção é passado para a classe base que gera uma resposta para você. No entanto, você é livre para verificar o tipo de exceção ou retornar a sua própria resposta personalizada:

    /**
     * Renderizar uma exceção em uma resposta HTTP.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Exception  $e
     * @return \Illuminate\Http\Response
     */
    public function render($request, Exception $e)
    {
    	if ($e instanceof CustomException) {
    		return response()->view('errors.custom', [], 500);
    	}

        return parent::render($request, $e);
    }

<a name="http-exceptions"></a>
## Exceções HTTP

Algumas exceções HTTP descrevem os códigos de erro a partir do servidor. Por exemplo, esta pode ser uma "page not found" (página não encontrada) erro (404), um "unauthorized" (não autorizado) erro (401) ou até mesmo um "internal server error" (erro interno do servidor) erro 500. A fim de gerar essas respostas de qualquer lugar em sua aplicação, use o seguinte:

	abort(404);

O método `abort` irá criar imediatamente uma excepção que será processado pelo manipulador de exceções. Opcionalmente, você pode fornecer um texto de resposta:

	abort(403, 'Ação não autorizada.');

Este método pode ser utilizado em qualquer momento durante o ciclo de vida da requisição.

<a name="custom-http-error-pages"></a>
### Páginas de Erro HTTP Customizadas

Laravel torna fácil o retorno de páginas de erro personalizadas para vários códigos de status HTTP. Por exemplo, se você deseja personalizar a página de erro para os códigos de status HTTP 404, crie um `resources/views/errors/404.blade.php`. Este arquivo será servido em todos os erros404 gerados pela sua aplicação.

As views dentro deste diretório devem ser nomeadas para coincidir com o código de status HTTP que a corresponde.

<a name="logging"></a>
## Logging

O recurso de logging do Laravel proporciona uma camada simples em cima da poderosa biblioteca [Monolog](http://github.com/seldaek/monolog). Por padrão, Laravel está configurado para criar arquivos de log diários para a sua aplicação, que são armazenados no diretório `storage/logs`. Você pode escrever informações para os logs usando o `Log` [facade](/docs/{{version}}/facades):

	<?php namespace App\Http\Controllers;

	use Log;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Exibir o perfil para um determinado usuário.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			Log::info('Mostrando perfil de usuário para o usuário: '.$id);

			return view('user.profile', ['user' => User::findOrFail($id)]);
		}
	}

O logger prevê os sete níveis de log definidos no [RFC 5424](http://tools.ietf.org/html/rfc5424): **debug**, **info**, **notice**, **warning**, **error**, **critical**, and **alert**.

	Log::debug($error);
	Log::info($error);
	Log::notice($error);
	Log::warning($error);
	Log::error($error);
	Log::critical($error);
	Log::alert($error);

#### Informação Contextual

Um array de dados contextuais também podem ser passadas para os métodos de log. Estes dados contextuais serão formatados e exibidos com a mensagem de log:

	Log::info('Usuário falhou ao logar.', ['id' => $user->id]);

#### Acessando a Instância Básica para Monolog

Monolog tem uma variedade de handlers (manipuladores) adicionais que você pode usar para fazer logging. Se necessário, você pode acessar a instância básica para Monolog básico utilizada pelo Laravel:

	$monolog = Log::getMonolog();

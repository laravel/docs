# Respostas HTTP

- [Respostas Básicas](#basic-responses)
    - [Colocando Cabeçalhos nas Respostas](#attaching-headers-to-responses)
    - [Colocando Cookies nas Respostas](#attaching-cookies-to-responses)
- [Outros Tipos de Respostas](#other-response-types)
    - [Resposta em View](#view-responses)
    - [Resposta JSON](#json-responses)
    - [Downloads de Arquivos](#file-downloads)
- [Redirecionamentos](#redirects)
    - [Redirecionando Para Rotas Nomeadas](#redirecting-named-routes)
    - [Redirecionando Para Ações de Controllers](#redirecting-controller-actions)
    - [Redirecionando com Informações em Sessao](#redirecting-with-flashed-session-data)
- [Resposta Customizada (Macro)](#response-macros)

<a name="basic-responses"></a>
## Respostas Básicas


Claro, todas as rotas e controllers devem retornar algum tipo de resposta para ser enviado de volta para o navegador do usuário. Laravel fornece várias maneiras diferentes para retornar respostas. A resposta mais básica é simplesmente devolver uma string a partir de uma rota ou controller:

    Route::get('/', function () {
        return 'Hello World';
    });

A string fornecida será automaticamente convertida em uma resposta HTTP pelo framework.

No entando, para a maioria das rotas e ações de controllers, você estará retornando uma instância de `Illuminate\Http\Response` ou uma [view](/docs/{{version}}/views). Retornar uma instância de `Response` permite a você customizar códigos de resposta HTTP e cabeçalhos. A instância de `Response` herda da classe `Symfony\Component\HttpFoundation\Response`, provendo uma variedade de métodos para construir respostas HTTP:


    use Illuminate\Http\Response;

    Route::get('home', function () {
        return (new Response($content, $status))
                      ->header('Content-Type', $value);
    });
Por conveniência, você poderá usar o helper `response`:

    Route::get('home', function () {
        return response($content, $status)
                      ->header('Content-Type', $value);
    });

> **Nota:** Para uma lista disponível com todos os métodos de `Response`, consulte a [Documentação da API](http://laravel.com/api/master/Illuminate/Http/Response.html) e a [Documentação da API Symfony](http://api.symfony.com/2.7/Symfony/Component/HttpFoundation/Response.html).

<a name="attaching-headers-to-responses"></a>
#### Colocando Cabeçalhos nas Respostas
Tenha em mente que a maioria dos métodos de resposta são encadeados, permitindo a construção de respostas fluente. Por exemplo, você pode usar o método `header` para adicionar uma série de cabeçalhos para a resposta antes de enviá-lo de volta para o usuário:

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Valor do Cabeçalho 1')
                ->header('X-Header-Two', 'Valor do Cabeçalho 2');


<a name="attaching-cookies-to-responses"></a>
#### Colocando Cookies nas Respostas

O método `withCookie` da instância da resposta permite você facilmente colocar cookies nas respostas. Por exemplo, you poderá usar o método `withCookie` para gerar um Cookie e colocá-lo na resposta:

    return response($content)->header('Content-Type', $type)
                     ->withCookie('nome', 'valor');

O método `withCookie` aceita argumentos opcionais adicionais que permitem customizar ainda mais as propriedades do seu Cookie:

    ->withCookie($nome, $valor, $minutos, $caminho, $cominio, $seguro, $apenasHttp)

Por padrão, todos os cookies gerados pelo Laravel são criptografados e assinados, de modo que não possam ser lidos e modificados pelo cliente. Você também poderá desativar a criptografia para um determinado conjunto de Cookies gerados pela aplicação, você poderá usar a propriedade `$except` do middleware `App\Http\Middleware\EncryptCookies`:

    /**
     * Os nomes dos cookies que não serão criptografados
     *
     * @var array
     */
    protected $except = [
        'nome_do_cookie',
    ];

<a name="other-response-types"></a>
## Outros Tipos de Respostas

O helper `response` pode ser usado para gerar outros tipos de casos de resposta. Quando o `response` é chamado sem argumentos, uma implementação do [Contrato](/docs/{{version}}/contracts) `Iluminar\Contratos\Routing\ResponseFactory` é retornado. Este contrato fornece vários métodos úteis para gerar respostas.

<a name="view-responses"></a>
#### Respostas Views

Se você precisa de controle sobre o status de resposta e cabeçalhos, mas também precisa retornar uma [view](/docs/{{version}}/views) como o conteúdo da resposta, você pode usar o método de `view`:

    return response()->view('hello', $data)->header('Content-Type', $type);

Claro, você não precisa passar um código de status HTTP customizado ou cabeçalhos customizados, você pode simplesmente usar a função `view` do helper.

<a name="json-responses"></a>
#### Respostas Json

O método `json` vai definir automaticamente o cabeçalho `Content-Type` para `application/json`, bem como converter o array dado em JSON usando a função `json_encode` do PHP:

    return response()->json(['nome' => 'Abigail', 'estado' => 'RS']);

Se você gostaria de criar uma resposta JSONP, você pode usar o método `json`, adicionando o método `setCallback`:

    return response()->json(['name' => 'Abigail', 'state' => 'CA'])
                     ->setCallback($request->input('callback'));

<a name="file-downloads"></a>
#### Downloads de Arquivos

O método `download` pode ser usado para gerar uma resposta que obriga o navegador do usuário a baixar o arquivo no caminho informado. este método aceita um nome de arquivo como o segundo argumento, que irá determinar o nome do arquivo que é visto para usuário baixar. Finalmente, você pode passar um array de cabeçalhos HTTP como o terceiro argumento para o método:

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> **Nota:** Symfony HttpFoundation, que gerencia o download de arquivos, exige que o nome do arquivo a ser baixado esteja no formato ASCII.

<a name="redirects"></a>
## Redirecionamentos

Resposta de redirecionamento são instâncias da classe  `Illuminate\Http\RedirectResponse`, e contém os cabeçalhos necessários para redirecionar o usuário para outra URL. Existem várias maneiras de gerar uma instância de `RedirectResponse`. A formar mais simples é utilizar o método `redirect` do helper:

    Route::get('dashboard', function () {
        return redirect('home/dashboard');
    });

Às vezes você pode precisar redirecionar o usuário para seu local anterior, por exemplo, depois de um envio de formulário que é inválido. Você pode fazer isso usando o método `back` do helper:

    Route::post('usuario/prefil', function () {
        // Validar a requisição

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
#### Redirecionando para Rotas Nomeadas

Quando você chamar método `redirect` sem parâmetros, uma instância de`Illuminate\Routing\Redirector` é devolvido, o que lhe permite chamar qualquer método da classe `Redirector`. Por exemplo, para gerar um `RedirectResponse` para uma rota nomeada, você pode usar o método `route`:

    return redirect()->route('login');

Se sua rota possuir parametros, você poderá passar como segundo argumento para o método `route`:

    // Para uma rota com a seguinte URI: perfil/{id}

    return redirect()->route('perfil', [1]);

Se você está redirecionando para uma rota com um parâmetro "ID" que é preenchido por um Model Eloquent, você pode simplesmente passar o próprio model. O ID será extraído automaticamente:

    return redirect()->route('perfil', [$usuario]);

<a name="redirecting-controller-actions"></a>
#### Redirecionando para Ações de Controllers

Você também pode gerar redirecionamentos para uma [Ação de Controller](/docs/{{version}}/controllers). Para fazer isso, simplesmente passe o controller e a ação para o método `action`. Lembre, você não precisa especificar o namespace completo do controller, o `RouteServiceProvider` irá definir o namespace padrão para o controller:

    return redirect()->action('HomeController@index');

Claro, se a rota para seu controller requer parâmetros, você poderá passar como segundo argumento para o método `action`:

    return redirect()->action('UserController@profile', [1]);

<a name="redirecting-with-flashed-session-data"></a>
#### Redirecionando com Dados Flash de Sessão
Redirecinando para uma nova URL e [setando dados flash na sessão](/docs/{{version}}/session#flash-data) são tipicamente feitos ao mesmo tempo. Então, por conveniência, você pode criar uma instância de `RedirectResponse` **e** setar dados flash na sessão com um simples método encadeado. Isto é particularmente conveviente para armezenar mensagens de status após uma ação;

    Route::post('usuario/perfil', function () {
        // Atualiza as informações do usuário

        return redirect('painel')->with('status', 'Perfil Atualizado!');
    });

Claro, após o usuário ser redirecionando para uma nova página, você poderá receber e exibir a mensagem flash da [session](/docs/{{version}}/session). Por exemplo, usando [Blade syntax](/docs/{{version}}/blade):

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="response-macros"></a>
## Respostas customizadas (Macros)

Se você gostaria de definir respostas customizadas que poderá ser reutilizada em uma variedade e rota e controllers, você poderá usar o método `macro` de uma implementação de `Illuminate\Contracts\Routing\ResponseFactory`.

Por Exemplo, no método `boot` do [service provider](/docs/{{version}}/providers):

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;
    use Illuminate\Contracts\Routing\ResponseFactory;

    class RespostaMacroServiceProvider extends ServiceProvider
    {
        /**
         * Executa a inicialização do serviço pré-registrado
         *
         * @param  ResponseFactory  $factory
         * @return void
         */
        public function boot(ResponseFactory $factory)
        {
            $factory->macro('maiusculas', function ($value) use ($factory) {
                return $factory->make(strtoupper($value));
            });
        }
    }

A função `macro` aceita um nome como primeiro argumento, e uma Closure com segundo. A Closure da macro será executada quando chamaar o nome da macro de uma implementação de `ResponseFactory` ou o helper `response`:

    return response()->maiusculas('foo');

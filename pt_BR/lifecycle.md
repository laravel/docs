# Request Lifecycle

- [Introducao](#introducao)
- [Ciclo de Vida Da Requisição](#ciclo-de-vida)
- [Foco no Service Providers](#foco-no-service-providers)

<a name="introducao"></a>
## Introdução

Ao usar qualquer ferramenta no "mundo real", você se senti mais confiante se entender como essa ferramenta funciona. Desenvolvimento de aplicações não é diferente. Quando você entender como a sua ferramenta de desenvolvimento funciona, você irá se sentir mais confortável e confiante ao usá-lo.

O objetivo desta documentação é lhe fornecer uma visão geral de alto nível de como o Framework Laravel "trabalha". Ao conhecer todo o framework, tudo será menos "mágico" e você estará mais confiante no desenvolvimento de suas aplicações.

Se você não entender todos os termos imediatamente, não desanime! Basta tentar obter uma compreensão básica do que está acontecendo, e seu conhecimento vai crescer quando você explorar outras seções da documentação.

<a name="ciclo-de-vida"></a>
## Ciclo de Vida Da Requisição

### First Things

O ponto de entrada de todas as requisições para um aplicativo em Laravel é o arquivo `public/index.php`. Todas as requisições são encaminhadas para este arquivo de configuração do seu servidor web (Apache/Nginx). O arquivo `index.php` não contém muito código. Pelo contrário, é um simplesmente  ponto de partida para carregar o resto do Framework.

O arquivo `index.php` carrega o arquivo de autoload gerado pelo Composer, e em seguida, recupera uma instância da aplicação Laravel em `bootstrap/app.php`. A primeira medida tomada por si só da aplicação em Laravel é criar uma instância do [service container](/docs/{{version}}/container).

### HTTP / Console Kernels

Em seguida, a requisição pode ser enviada para o kernel HTTP ou para o kernel console, dependendo do tipo de requisição que está entrando na aplicação. Estes dois kernels são responsáveis e são a central de todo o fluxo da requisição. Por enquanto, vamos apenas focar no kernel HTTP, que está localizado em `app/HTTP/Kernel.php`.

O kernel HTTP estende a classe `Illuminate\Foundation\Http\Kernel`, que define uma série de `bootstrappers` que será executado antes que a requisição seja executada. Estes inicializadores configuram manipulações de erro, configuram logs, [detecta o ambiente de aplicação](/docs/{{version}}/installation#environment-configuration), e executar outras tarefas que precisam ser feitas antes da requisição realmente ser tratada.

O kernel HTTP também define uma lista de [middlewares](/docs/{{version}}/middleware) HTTP, que todas as requisições devem passar antes de serem manuseados pelo aplicativo. Estes middlewares podem fazer leitura e escrita da [sessão HTTP](/docs/{{version}}/session), determinar se a aplicação está no modo de manutenção, [verificar o token CSRF](/docs/{{version}}/routing#csrf-protection), e muito mais.

O entendimento do método `handle` do kernel HTTP é bastante simples: receber um `Request` e retornar um `Response`. Pense no Kernel como sendo uma grande caixa preta que representa todo o seu aplicativo. Alimentá-lo com request HTTP irá retornar um response HTTP.

#### Service Providers

Uma das mais importantes ações de kernel bootstrapping é de carregar os [service providers](/docs/{{version}}/providers) para sua aplicação. Todos os service providers da aplicação são configurados em `config/app.php` no array `providers`. Primeiro, o método `register` será chamado, e em seguida todos os providers, uma vez que todos os providers foram registrado, o método `boot` será chamado.

Service providers são responsáveis pela inicialização de vários componentes do Framework, como os componentes de banco de dados, filas, de validação e de roteamento. Uma vez que inicializado, será configurado todos os recursos oferecidos pelo Framework, os service providers são o aspecto mais importante de todo o processo de inicialização do Laravel.

#### Dispatch Request

Uma vez que o aplicativo foi inicializado e todos os services providers tenham sido registradas, o `request` será transferido para o router que irá fazer a expedição. O router irá enviar a solicitação para uma rota ou controller, bem como executar qualquer middleware específico a rota.

<a name="foco-no-service-providers"></a>
## Foco no Service Providers

Os services providers são realmente a chave para a inicialização de um aplicativo em Laravel. A instância do aplicativo é criado, os services providers são registrados, e a requisição é entregue ao aplicativo bootstrap. É realmente muito simples!

É muito valioso ter fixado de como uma aplicação em Laravel é construída e inicializada via services providers. Claro, os services providers padrão do aplicativo são armazenadas no diretório `app/Providers`.

Por padrão, o `AppServiceProvider` é bastante vazio. Este provider é um ótimo lugar para adicionar os próprios inicializadores e service container do seu aplicativo. Claro que, para aplicações de grande porte, você pode querer criar vários services providers, cada um com um tipo mais granular de inicialização.
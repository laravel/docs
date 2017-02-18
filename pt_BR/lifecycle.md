# Request Lifecycle

- [Introdução](#introducao)
- [Ciclo de Vida da Requisição](#ciclo-de-vida)
- [Foco nos Service Providers](#foco-nos-service-providers)

<a name="introducao"></a>
## Introdução

Ao usar qualquer ferramenta no "mundo real", você se sente mais confiante se entender como essa ferramenta funciona. Desenvolvimento de aplicações não é diferente. Quando você compreende como a sua ferramenta de desenvolvimento funciona, você se sente mais confortável e confiante para usá-la.

O objetivo desta documentação é lhe fornecer uma visão geral de alto nível de como o Framework Laravel "trabalha". Ao conhecer todo o framework, tudo será menos "mágico" e você estará mais confiante no desenvolvimento de suas aplicações.

Se você não entender todos os termos imediatamente, não desanime! Basta tentar obter uma compreensão básica do que está acontecendo, e seu conhecimento vai crescer quando você explorar outras seções da documentação.

<a name="ciclo-de-vida"></a>
## Ciclo de Vida da Requisição

### First Things

O ponto de entrada de todas as requisições para um aplicativo em Laravel é o arquivo `public/index.php`. Todas as requisições são encaminhadas para este arquivo pela configuração do seu servidor web (Apache/Nginx). O arquivo `index.php` não contém muito código. Pelo contrário, ele é simplesmente um ponto de partida para carregar o resto do Framework.

O arquivo `index.php` carrega o arquivo de definiçao de autoload gerado pelo Composer, e em seguida, recupera uma instância da aplicação Laravel em `bootstrap/app.php`. A primeira ação tomada pelo Laravel é criar uma instância da aplicação  [service container](/docs/{{version}}/container).

### HTTP / Console Kernels

Em seguida, a requisição é enviada para o kernel HTTP ou para o kernel console, dependendo do tipo de requisição que está entrando na aplicação. Estes dois kernels funcionam como uma central de controle de fluxo de todas as requisições. Por enquanto, vamos apenas focar no kernel HTTP, que está localizado em `app/HTTP/Kernel.php`.

O kernel HTTP estende a classe `Illuminate\Foundation\Http\Kernel`, que define uma série de `bootstrappers` que serão executados antes que a requisição seja executada. Estes inicializadores configuram manipulações de erro, configuram logs, [detectam o ambiente de aplicação](/docs/{{version}}/installation#environment-configuration), e executam outras tarefas que precisam ser feitas antes da requisição ser realmente tratada.

O kernel HTTP também define uma lista de [middlewares](/docs/{{version}}/middleware) HTTP, pelos quais todas as requisições devem passar antes de serem manuseadas pela aplicação. Estes middlewares manipulam a leitura e escrita da [sessão HTTP](/docs/{{version}}/session), determinam se a aplicação está no modo de manutenção, [verificam o token CSRF](/docs/{{version}}/routing#csrf-protection), e muito mais.

A assinatura do método `handle` do kernel HTTP é bastante simples: receber um `Request` e retornar um `Response`. Pense no Kernel como sendo uma grande caixa preta que representa toda a sua aplicação. Alimente-o com um request HTTP e ele irá retornar um response HTTP.

#### Service Providers

Uma das mais importantes ações de inicialização do Kernel é a de carregar os [service providers](/docs/{{version}}/providers) para sua aplicação. Todos os service providers da aplicação são configurados em `config/app.php` no array `providers`. Primeiro, o método `register` será chamado em todos os providers, então, uma vez que todos os providers tirevem sido registrados, o método `boot` será chamado.

Service providers são responsáveis pela inicialização de vários componentes do Framework, tais como bancos de dados, filas, validação e roteamento. Uma vez que eles inicializam e configuram cada um dos recursos oferecidos pelo Framework, os service providers são o aspecto mais importante de todo o processo de inicialização do Laravel.

#### Dispatch Request

Uma vez que a aplicação tenha sido inicializada e todos os service providers tenham sido registrados, o `request` será transferido para o router que irá fazer a expedição. O router irá enviar a solicitação para uma rota ou controller, bem como executar qualquer middleware específico para a rota.

<a name="foco-nos-service-providers"></a>
## Foco nos Service Providers

Os services providers são realmente a chave para a inicialização de uma aplicação Laravel. A instância da aplicação é criada, os service providers são registrados, e a requisição é entregue ao aplicativo bootstrap. É realmente muito simples!

Ter uma sólida compreensão de como uma aplicação em Laravel é construída e inicializada via services providers é muito valioso. Claro, os service providers padrão da aplicação são armazenados no diretório `app/Providers`.

Por padrão, o `AppServiceProvider` é bastante vazio. Este provider é um ótimo lugar para adicionar os seus próprios inicializadores e ligações para os service container da aplicação. Claro que, para aplicações de grande porte, você pode querer criar vários services providers, cada um com um tipo mais granular de inicialização.

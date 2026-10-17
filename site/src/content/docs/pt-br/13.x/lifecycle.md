---
title: "Ciclo de Vida da Requisição"
---

- [Introdução](#introduction)
- [Visão Geral do Ciclo de Vida](#lifecycle-overview)
    - [Primeiros Passos](#first-steps)
    - [Kernels HTTP / Console](#http-console-kernels)
    - [Provedores de Serviço](#service-providers)
    - [Roteamento](#routing)
    - [Finalizando](#finishing-up)
- [Foco nos Provedores de Serviço](#focus-on-service-providers)

<a id="introduction"></a>
## Introdução

Ao usar qualquer ferramenta no "mundo real", você se sente mais confiante se entende como essa ferramenta funciona. O desenvolvimento de aplicações não é diferente. Quando você entende como suas ferramentas de desenvolvimento funcionam, você se sente mais confortável e confiante ao usá-las.

O objetivo deste documento é fornecer uma boa visão geral de alto nível de como o framework Laravel funciona. Ao conhecer melhor o framework como um tudo, tudo parece menos "mágico" e você terá mais confiança para construir suas aplicações. Se você não entender todos os termos imediatamente, não desanime! Apenas tente ter uma compreensão básica do que está acontecendo, e seu conhecimento crescerá à medida que você explora outras seções da documentação.

<a id="lifecycle-overview"></a>
## Visão Geral do Ciclo de Vida

<a id="first-steps"></a>
### Primeiros Passos

O ponto de entrada para todas as requisições em uma aplicação Laravel é o arquivo `public/index.php`. Todas as requisições são direcionadas para este arquivo pela configuração do seu servidor web (Apache / Nginx). O arquivo `index.php` não contém muito código. Em vez disso, ele é um ponto de partida para carregar o restante do framework.

O arquivo `index.php` carrega a definição de autoloading gerada pelo Composer e, em seguida, recupera uma instância da aplicação Laravel de `bootstrap/app.php`. A primeira ação tomada pelo próprio Laravel é criar uma instância da aplicação / [container de serviço](../container/).

<a id="http-console-kernels"></a>
### Kernels HTTP / Console

Em seguida, a requisição recebida é enviada para o kernel HTTP ou o kernel do console, usando os métodos `handleRequest` ou `handleCommand` da instância da aplicação, dependendo do tipo de requisição entrando na aplicação. Esses dois kernels servem como o local central por onde todas as requisições fluem. Por enquanto, vamos focar apenas no kernel HTTP, que é uma instância de `Illuminate\Foundation\Http\Kernel`.

O kernel HTTP define um array de `bootstrappers` que serão executados antes que a requisição seja processada. Esses bootstrappers configuram o tratamento de erros, configuram logging, [detectam o ambiente da aplicação](../configuration/#environment-configuration), e realizam outras tarefas que precisam ser feitas antes que a requisição seja realmente tratada. Tipicamente, essas classes tratam da configuração interna do Laravel que você não precisa se preocupar.

O kernel HTTP também é responsável por passar a requisição através da pilha de middleware da aplicação. Esses middlewares tratam da leitura e escrita da [sessão HTTP](../session/), determinam se a aplicação está em modo de manutenção, [verificam o token CSRF](../csrf/), e mais. Falaremos mais sobre isso em breve.

A assinatura do método `handle` do kernel HTTP é bem simples: ele recebe uma `Request` e retorna uma `Response`. Pense no kernel como uma grande caixa preta que representa toda a sua aplicação. Alimente-o com requisições HTTP e ele retornará respostas HTTP.

<a id="service-providers"></a>
### Provedores de Serviço

Uma das ações de bootstrapping mais importantes do kernel é carregar os [provedores de serviço](../providers/) para sua aplicação. Os provedores de serviço são responsáveis por fazer o bootstrap de todos os vários componentes do framework, como banco de dados, fila, validação e componentes de roteamento.

O Laravel iterará através desta lista de provedores e instanciará cada um deles. Depois de instanciar os provedores, o método `register` será chamado em todos os provedores. Então, uma vez que todos os provedores tenham sido registrados, o método `boot` será chamado em cada provedor. Isso é para que os provedores de serviço possam depender de cada binding do container estando registrado e disponível até que seu método `boot` seja executado.

Essencialmente, cada grande recurso oferecido pelo Laravel é inicializado e configurado por um provedor de serviço. Como eles inicializam e configuram tantos recursos oferecidos pelo framework, os provedores de serviço são o aspecto mais importante de todo o processo de bootstrap do Laravel.

Enquanto o framework internamente usa dezenas de provedores de serviço, você também tem a opção de criar seus próprios. Você pode encontrar uma lista dos provedores de serviço definidos pelo usuário ou de terceiros que sua aplicação está usando no arquivo `bootstrap/providers.php`.

<a id="routing"></a>
### Roteamento

Uma vez que a aplicação tenha sido inicializada e todos os provedores de serviço tenham sido registrados, a `Request` será entregue ao roteador para despacho. O roteador despachará a requisição para uma rota ou controller, bem como executará qualquer middleware específico da rota.

Middleware fornece um mecanismo conveniente para filtrar ou examinar requisições HTTP entrando em sua aplicação. Por exemplo, o Laravel inclui um middleware que verifica se o usuário da sua aplicação está autenticado. Se o usuário não estiver autenticado, o middleware redirecionará o usuário para a tela de login. No entanto, se o usuário estiver autenticado, o middleware permitirá que a requisição prossiga mais adiante na aplicação. Alguns middlewares são atribuídos a todas as rotas dentro da aplicação, como `PreventRequestsDuringMaintenance`, enquanto alguns são atribuídos apenas a rotas específicas ou grupos de rotas. Você pode aprender mais sobre middleware lendo a [documentação completa de middleware](../middleware/).

Se a requisição passar por todos os middlewares atribuídos à rota correspondente, o método da rota ou controller será executado e a resposta retornada pelo método da rota ou controller será enviada de volta através da cadeia de middlewares da rota.

<a id="finishing-up"></a>
### Finalizando

Uma vez que o método da rota ou controller retorne uma resposta, a resposta viajará de volta para fora através dos middlewares da rota, dando à aplicação a chance de modificar ou examinar a resposta de saída.

Finalmente, uma vez que a resposta viaje de volta através dos middlewares, o método `handle` do kernel HTTP retorna o objeto de resposta para o `handleRequest` da instância da aplicação, e este método chama o método `send` na resposta retornada. O método `send` envia o conteúdo da resposta para o navegador web do usuário. Agora completamos nossa jornada por todo o ciclo de vida de requisição do Laravel!

<a id="focus-on-service-providers"></a>
## Foco nos Provedores de Serviço

Os provedores de serviço são realmente a chave para inicializar uma aplicação Laravel. A instância da aplicação é criada, os provedores de serviço são registrados, e a requisição é entregue à aplicação inicializada. É realmente tão simples!

Ter uma compreensão sólida de como uma aplicação Laravel é construída e inicializada via provedores de serviço é muito valioso. Os provedores de serviço definidos pelo usuário da sua aplicação são armazenados no diretório `app/Providers`.

Por padrão, o `AppServiceProvider` é bastante vazio. Este provedor é um ótimo lugar para adicionar o bootstrapping e os bindings do container de serviço da sua própria aplicação. Para aplicações grandes, você pode desejar criar vários provedores de serviço, cada um com bootstrapping mais granular para serviços específicos usados pela sua aplicação.
# Request Lifecycle

- [Introducao](#introducao)
- [Ciclo de Vida Da Requisição](#ciclo-de-vida)
- [Foco no Service Providers](#foco-no-service-providers)

<a name="introducao"></a>
## Introdução

Ao usar qualquer ferramenta no "mundo real", você se senti mais confiante se você entender como essa ferramenta funciona. Desenvolvimento de aplicações não é diferente. Quando você entender como a sua ferramenta de desenvolvimento funciona, você irá se sentir mais confortável e confiante ao usá-lo.

O objetivo desta documentação é lhe fornecer uma visão geral de alto nível, de como o Framework Laravel "trabalha". Ao conhecer todo o framework, tudo será menos "mágico" e você estará mais confiante no desenvolvimento de suas aplicações.

Se você não entender todos os termos imediatamente, não desanime! Basta tentar obter uma compreensão básica do que está acontecendo, e seu conhecimento vai crescer quando você explorar outras seções da documentação.

<a name="ciclo-de-vida"></a>
## Ciclo de Vida Da Requisição

### Primeiros Passos

O ponto de entrada de todas as solicitações para um aplicativo em Laravel é o arquivo `public/index.php`. Todos os pedidos/requests são encaminhados para este arquivo de configuração do seu servidor web (Apache/Nginx). O arquivo `index.php` não contém muito código. Pelo contrário, é um simplesmente  ponto de partida para carregar o resto do Framework.

O arquivo `index.php` carrega o arquivo de autoload gerado pelo Composer, e em seguida, recupera uma instância da aplicação Laravel em `bootstrap/app.php`. A primeira medida tomada por si só da aplicação em Laravel é criar uma instância do [service container](/docs/{{version}}/container).

### HTTP / Console Kernels

Em seguida, o request pode ser enviado para o kernel HTTP ou para o kernel console, dependendo do tipo de request que está entrando na aplicação. Estes dois kernels são responsaveis e são a central de todo o fluxo do request. Por enquanto, vamos apenas focar no kernel HTTP, que está localizado em `app/HTTP/Kernel.php`.

O kernel HTTP estende a classe `Illuminate\Foundation\Http\Kernel`, que define uma série de `bootstrappers` que será executado antes que o request seja executado. Estes bootstrappers configuram manipulações de erro, configuram logs, [detecta o ambiente de aplicação](/docs/{{version}}/installation#environment-configuration), e executar outras tarefas que precisam ser feitas antes do request realmente ser tratado.

O kernel HTTP também define uma lista de [middlewares](/docs/{{version}}/middleware) HTTP, que todos os requests devem passar antes de serem manuseados pelo aplicativo. Estes middlewares podem fazer leitura e escrita de [sessão HTTP](/docs/{{version}}/session), determinar se a aplicação está no modo de manutenção, [verificar o token CSRF](/docs/{{version}}/routing#csrf-protection), e muito mais.

O entendimento do método `handle` do kernel HTTP é bastante simples: receber um `Request` e retornar um `Response`. Pense no Kernel como sendo uma grande caixa preta que representa todo o seu aplicativo. Alimentá-lo com request HTTP ele irá retornar um response HTTP.

#### Service Providers

#### Expedição da Requisição

<a name="foco-no-service-providers"></a>
## Foco no Service Providers
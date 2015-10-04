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

#### Service Providers

#### Expedição da Requisição

<a name="foco-no-service-providers"></a>
## Foco no Service Providers
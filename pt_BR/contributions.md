# Guia de Contribuição

- [Relatórios de Bug](#bug-reports)
- [Discussões de Desenvolvimento do Core](#core-development-discussion)
- [Qual Branch?](#which-branch)
- [Vunerabilidades de Segurança](#security-vulnerabilities)
- [Estilo de Código](#coding-style)

<a name="bug-reports"></a>
## Relatórios de Bug

Para encorajar a colaboração ativa, o Laravel incentiva fortemente os pull requests, e não apenas relatórios de bugs. Os "Relatórios de bugs" podem ser transmitidos sob a forma de um pull request contendo um teste com falha.

No entanto, se você enviar um relatório de bug, ele deve conter um título e uma descrição detalhada do problema. Você também deve incluir o máximo de informações relevantes possíveis e uma amostra de código que demonstre o problema. O objetivo de um relatório de bug é tornar mais fácil para si mesmo - e outros - uma forma de reproduzir o bug e desenvolver uma correção.

Lembre-se, os relatórios de bugs são criados na esperança de que outras pessoas com o mesmo problema sejam capazes de colaborar com você em resolvê-lo. Não espere que o relatório de bug seja automaticamente corrigido ou que os outros vão saltar para corrigi-lo. Criar um relatório de bug serve para ajudar a si e aos outros a iniciar o caminho na correção do problema.

O código fonte do Laravel é mantido e versionado pelo Github, e há repositórios para cada um dos projetos Laravel:

- [Framework Laravel](https://github.com/laravel/framework)
- [Aplicação Laravel](https://github.com/laravel/laravel)
- [Documentação Laravel](https://github.com/laravel/docs)
- [Cashier Laravel](https://github.com/laravel/cashier)
- [Envoy Laravel](https://github.com/laravel/envoy)
- [Homestead Laravel](https://github.com/laravel/homestead)
- [Homestead Scripts de Construção Laravel](https://github.com/laravel/settler)
- [Site Laravel](https://github.com/laravel/laravel.com)
- [Arte Laravel](https://github.com/laravel/art)

<a name="core-development-discussion"></a>
## Discussões de Desenvolvimento do Core

Discussões sobre bugs, novas funcionalidades e implementação de funcionalidades existentes ocorrem no canal `#internals` do [LaraChat](http://larachat.co) no Slack. Taylor Otwell, o mantenedor do Laravel, está normalmente presente no canal durante a semana, das 8hs às 17hs, no fuso horário CST (UTC-06:00 ou America/Chicago), e esporadicamente presente no canal em outros momentos.

<a name="which-branch"></a>
## Qual Branch?

**Todas** as correções de bugs devem ser enviadas para o último branch estável. As Correções de bugs **nunca** devem ser enviadas para o branch `master` a menos que a correção seja de funcionalidades que existam apenas na próxima versão.

As funcionalidades qualificadas como **Minor**, **que sejam totalmente compatíveis** com a versão atual do Laravel podem ser enviadas para o último branch estável.

As novas funcionalidades qualificadas como **Major** devem ser sempre enviadas para o branch `master`, que contém a próxima versão do Laravel.

Se você não tiver certeza se a sua funcionalidade se qualifica como uma major (maior) ou minor (menor), por favor, pergunte ao Taylor Otwell no canal IRC `#laravel-dev` (Freenode).

<a name="security-vulnerabilities"></a>
## Vunerabilidades de Segurança

Se você descobrir uma vunerabilidade na segurança do Laravel, por favor envie um e-mail para Taylor Otwell em <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. Todas as vunerabilidades de segurança serão prontamente corrigidas.

<a name="coding-style"></a>
## Estilo de Código

Laravel segue o padrão de codificação [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) e o padrão [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) de carregamento automático.

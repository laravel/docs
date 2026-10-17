---
title: "Guia de Contribuição"
---

- [Relatórios de Bugs](#bug-reports)
- [Dúvidas de Suporte](#support-questions)
- [Qual Branch?](#which-branch)
- [Assets Compilados](#compiled-assets)
- [Contribuições Geradas por IA](#ai-generated-contributions)
- [Vulnerabilidades de Segurança](#security-vulnerabilities)
- [Estilo de Código](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [Código de Conduta](#code-of-conduct)

<a id="bug-reports"></a>
## Relatórios de Bugs

Para incentivar a colaboração ativa, o Laravel recomenda fortemente pull requests que resolvam problemas, e não issues no GitHub. As issues do GitHub estão desabilitadas na maioria dos nossos pacotes first-party.

Se você descobrir um problema, crie um pull request que o resolva. Seu pull request deve conter um título e uma descrição clara do problema e de sua solução. Você também deve incluir o máximo de informações relevantes possível e um exemplo de código que demonstre o problema. O objetivo de um pull request é facilitar a compreensão do problema e a verificação da correção, tanto para você quanto para os outros.

Se você não souber como corrigir o problema, descreva-o para um agente de programação e use-o para tentar criar um pull request.

Os pull requests só serão revisados quando estiverem marcados como "pronto para revisão" (não no estado "draft") e todos os testes para novas funcionalidades estiverem passando. Pull requests parados, sem atividade, mantidos no estado "draft" serão fechados após alguns dias.

O código-fonte do Laravel é gerenciado no GitHub, e há repositórios para cada um dos projetos do Laravel:

<div class="content-list" markdown="1">

- [Laravel AI SDK](https://github.com/laravel/ai)
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Boost](https://github.com/laravel/boost)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Starter Kits (Maestro)](https://github.com/laravel/maestro)

</div>

<a id="support-questions"></a>
## Dúvidas de Suporte

As issue trackers do GitHub do Laravel não têm a intenção de fornecer ajuda ou suporte sobre o Laravel. Em vez disso, use um dos seguintes canais:

<div class="content-list" markdown="1">

- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a id="which-branch"></a>
## Qual Branch?

**Todas** as correções de bugs devem ser enviadas para a versão mais recente que ainda suporta correções de bugs (atualmente `13.x`). Correções de bugs **nunca** devem ser enviadas para a branch `master`, a menos que corrijam funcionalidades que existem apenas na próxima versão.

Funcionalidades **menores** que são **totalmente compatíveis** com a versão atual podem ser enviadas para a branch estável mais recente (atualmente `13.x`).

Novas funcionalidades **maiores** ou funcionalidades com mudanças que quebram compatibilidade devem sempre ser enviadas para a branch `master`, que contém a próxima versão.

<a id="compiled-assets"></a>
## Assets Compilados

Se você estiver enviando uma alteração que afetará um arquivo compilado, como a maioria dos arquivos em `resources/css` ou `resources/js` do repositório `laravel/laravel`, não faça commit dos arquivos compilados. Devido ao seu grande tamanho, eles não podem ser revisados de forma realista por um mantenedor. Isso poderia ser explorado como uma forma de injetar código malicioso no Laravel. Para se proteger preventivamente contra isso, todos os arquivos compilados serão gerados e commitados pelos mantenedores do Laravel.

<a id="ai-generated-contributions"></a>
## Contribuições Geradas por IA

Agradecemos todo pull request enviado ao Laravel. No entanto, contribuições substanciais que são primariamente geradas por IA, sem uma revisão e reflexão humana cuidadosa, não são aceitáveis.

Se você optar por usar ferramentas de IA para auxiliar em contribuições grandes ou complexas para o framework, o código resultante **deve** ser minuciosamente revisado, testado e compreendido por você antes de ser enviado.

As descrições de pull requests **devem** ser escritas inteiramente pelo contribuidor. Pull requests com descrições geradas por IA serão fechados.

**Abrir em massa issues ou pull requests inteiramente gerados por IA não será tolerado.** Tais pull requests serão fechados sem revisão, e o usuário contribuidor poderá ser bloqueado do repositório.

Encorajamos os contribuidores a se familiarizarem com a base de código existente, a interagir com a comunidade e a enviar pull requests que reflitam sua própria compreensão e a consideração cuidadosa do problema que estão resolvendo.

<a id="security-vulnerabilities"></a>
## Vulnerabilidades de Segurança

Se você descobrir uma vulnerabilidade de segurança no Laravel, envie um e-mail para nossa equipe de segurança em <a href="mailto:security@laravel.com">security@laravel.com</a>. Todas as vulnerabilidades de segurança serão tratadas prontamente.

<a id="coding-style"></a>
## Estilo de Código

O Laravel segue o padrão de codificação [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) e o padrão de autoloading [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md).

<a id="phpdoc"></a>
### PHPDoc

Abaixo está um exemplo de um bloco de documentação válido do Laravel. Observe que o atributo `@param` é seguido por dois espaços, o tipo do argumento, mais dois espaços e, por fim, o nome da variável:

```php
/**
 * Register a binding with the container.
 *
 * @param  string|array  $abstract
 * @param  \Closure|string|null  $concrete
 * @param  bool  $shared
 * @return void
 *
 * @throws \Exception
 */
public function bind($abstract, $concrete = null, $shared = false)
{
    // ...
}
```

Quando os atributos `@param` ou `@return` forem redundantes devido ao uso de tipos nativos, eles podem ser removidos:

```php
/**
 * Execute the job.
 * [tl! remove]
 * @return void [tl! remove]
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

No entanto, quando o tipo nativo for genérico, especifique o tipo genérico por meio dos atributos `@param` ou `@return`:

```php
/**
 * Get the attachments for the message.
 * [tl! add]
 * @return array<int, \Illuminate\Mail\Mailables\Attachment> [tl! add]
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

<a id="styleci"></a>
### StyleCI

Não se preocupe se a formatação do seu código não estiver perfeita! O [StyleCI](https://styleci.io/) irá mesclar automaticamente quaisquer correções de estilo no repositório do Laravel após os pull requests serem mesclados. Isso nos permite focar no conteúdo da contribuição e não no estilo do código.

<a id="code-of-conduct"></a>
## Código de Conduta

O código de conduta do Laravel é derivado do código de conduta do Ruby. Quaisquer violações do código de conduta podem ser reportadas a Taylor Otwell (taylor@laravel.com):

<div class="content-list" markdown="1">

- Os participantes serão tolerantes com pontos de vista opostos.
- Os participantes devem garantir que sua linguagem e ações estejam livres de ataques pessoais e comentários depreciativos.
- Ao interpretar as palavras e ações de outras pessoas, os participantes devem sempre presumir boas intenções.
- Comportamentos que possam ser razoavelmente considerados assédio não serão tolerados.

</div>

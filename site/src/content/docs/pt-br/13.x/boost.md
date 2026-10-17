---
title: "Laravel Boost"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Configure Seus Agentes](#set-up-your-agents)
    - [Mantendo os Recursos do Boost Atualizados](#keeping-boost-resources-updated)
- [Servidor MCP](#mcp-server)
    - [Ferramentas MCP Disponíveis](#available-mcp-tools)
    - [Registrando o Servidor MCP Manualmente](#manually-registering-the-mcp-server)
- [Diretrizes de IA](#ai-guidelines)
    - [Diretrizes de IA Disponíveis](#available-ai-guidelines)
    - [Adicionando Diretrizes de IA Personalizadas](#adding-custom-ai-guidelines)
    - [Sobrescrevendo as Diretrizes de IA do Boost](#overriding-boost-ai-guidelines)
    - [Diretrizes de IA de Pacotes de Terceiros](#third-party-package-ai-guidelines)
- [Skills de Agentes](#agent-skills)
    - [Skills Disponíveis](#available-skills)
    - [Skills Personalizadas](#custom-skills)
    - [Sobrescrevendo Skills](#overriding-skills)
    - [Skills de Pacotes de Terceiros](#third-party-package-skills)
- [Diretrizes vs. Skills](#guidelines-vs-skills)
- [Regras do Projeto](#project-rules)
    - [Registrando Regras](#recording-rules)
    - [Inferindo as Convenções da Sua Aplicação](#inferring-your-applications-conventions)
    - [Desativando Regras do Projeto](#disabling-project-rules)
- [API de Documentação](#documentation-api)
- [Estendendo o Boost](#extending-boost)
    - [Adicionando Suporte a Outras IDEs / Agentes de IA](#adding-support-for-other-ides-ai-agents)

<a id="introduction"></a>
## Introdução

O Laravel Boost acelera o desenvolvimento assistido por IA fornecendo as diretrizes essenciais e as skills de agentes que ajudam os agentes de IA a escrever aplicações Laravel de alta qualidade, aderentes às melhores práticas do Laravel.

O Boost também fornece uma poderosa API de documentação do ecossistema Laravel que combina uma ferramenta MCP integrada com uma extensa base de conhecimento contendo mais de 17.000 informações específicas do Laravel, tudo aprimorado por recursos de busca semântica usando embeddings para resultados precisos e sensíveis ao contexto. O Boost instrui agentes de IA como o Claude Code e o Cursor a usar essa API para conhecer os recursos e as melhores práticas mais recentes do Laravel.

<a id="installation"></a>
## Instalação

O Laravel Boost pode ser instalado via Composer:

```shell
composer require laravel/boost --dev
```

Em seguida, instale o servidor MCP e as diretrizes de codificação:

```shell
php artisan boost:install
```

O comando `boost:install` gerará os arquivos de diretrizes e skills dos agentes de codificação que você selecionou durante o processo de instalação. Se um arquivo de diretrizes como `CLAUDE.md` ou `AGENTS.md` já existir, o Boost substitui apenas o conteúdo dentro do bloco `<laravel-boost-guidelines>`, então qualquer coisa que você tenha escrito fora desse bloco é preservada.

Depois que o Laravel Boost estiver instalado, você está pronto para começar a programar com o Cursor, o Claude Code ou o agente de IA de sua preferência.

> **Nota:**
> Sinta-se à vontade para adicionar o arquivo de configuração MCP gerado (`.mcp.json`), os arquivos de diretrizes (`CLAUDE.md`, `AGENTS.md`, `junie/`, etc.) e o arquivo de configuração `boost.json` ao `.gitignore` da sua aplicação, pois esses arquivos são regenerados automaticamente ao executar `boost:install` e `boost:update`.

<a id="set-up-your-agents"></a>
### Configure Seus Agentes

```text tab=Cursor
1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "/open MCP Settings"
3. Turn the toggle on for `laravel-boost`
```

```text tab=Claude Code
Claude Code support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

```text tab=Codex
Codex support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

```text tab=GitHub Copilot (VS Code)
1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "MCP: List Servers"
3. Arrow to `laravel-boost` and press `enter`
4. Choose "Start server"
```

```text tab=Junie
1. Press `shift` twice to open the command palette
2. Search "MCP Settings" and press `enter`
3. Check the box next to `laravel-boost`
4. Click "Apply" at the bottom right
```

<a id="keeping-boost-resources-updated"></a>
### Mantendo os Recursos do Boost Atualizados

Você pode querer atualizar periodicamente seus recursos locais do Boost (diretrizes de IA e skills) para garantir que eles reflitam as versões mais recentes dos pacotes do ecossistema Laravel que você instalou. Para isso, você pode usar o comando Artisan `boost:update`.

```shell
php artisan boost:update
```

Você também pode automatizar esse processo adicionando-o aos scripts "post-update-cmd" do Composer:

```json
{
  "scripts": {
    "post-update-cmd": [
      "@php artisan boost:update --ansi"
    ]
  }
}
```

Por padrão, o comando `boost:update` também varrerá sua aplicação em busca de pacotes recém-instalados e oferecerá a publicação de suas respectivas diretrizes e skills. Essa pergunta é ignorada quando o comando é executado de forma não interativa, como a partir de um script do Composer. Se você quiser que o Boost atualize apenas os recursos do Boost já publicados na sua aplicação, pode usar a opção `--no-discover`:

```shell
php artisan boost:update --no-discover
```

<a id="mcp-server"></a>
## Servidor MCP

O Laravel Boost fornece um servidor MCP (Model Context Protocol) que expõe ferramentas para que agentes de IA interajam com a sua aplicação Laravel. Essas ferramentas dão aos agentes a capacidade de inspecionar a estrutura da sua aplicação, consultar o banco de dados, executar código e muito mais.

<a id="available-mcp-tools"></a>
### Ferramentas MCP Disponíveis

<div class="overflow-auto">

| Nome                 | Observações                                                                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Application Info     | Lê as versões do PHP e do Laravel, o mecanismo de banco de dados, a lista de pacotes do ecossistema com suas versões e os models Eloquent |
| Browser Logs         | Lê logs e erros do navegador                                                                                |
| Database Connections | Inspeciona as conexões de banco de dados disponíveis, incluindo a conexão padrão                            |
| Database Query       | Executa uma query no banco de dados                                                                         |
| Database Schema      | Lê o schema do banco de dados                                                                               |
| Get Absolute URL     | Converte URIs de caminhos relativos em absolutas para que os agentes gerem URLs válidas                     |
| Last Error           | Lê o último erro dos arquivos de log da aplicação                                                           |
| Read Log Entries     | Lê as últimas N entradas de log                                                                             |
| Record Rule          | Registra uma [regra do projeto](#project-rules) durável em `.ai/rules` para que agentes futuros a herdem    |
| Search Docs          | Consulta o serviço de API de documentação hospedado do Laravel para obter documentação com base nos pacotes instalados |

</div>

<a id="manually-registering-the-mcp-server"></a>
### Registrando o Servidor MCP Manualmente

Às vezes, pode ser necessário registrar manualmente o servidor MCP do Laravel Boost no editor de sua preferência. Você deve registrar o servidor MCP usando os seguintes dados:

<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

Exemplo em JSON:

```json
{
    "mcpServers": {
        "laravel-boost": {
            "command": "php",
            "args": ["artisan", "boost:mcp"]
        }
    }
}
```

<a id="ai-guidelines"></a>
## Diretrizes de IA

As diretrizes de IA são arquivos de instruções componíveis, carregados antecipadamente para fornecer aos agentes de IA o contexto essencial sobre os pacotes do ecossistema Laravel. Essas diretrizes contêm convenções centrais, melhores práticas e padrões específicos de frameworks que ajudam os agentes a gerar código consistente e de alta qualidade.

<a id="available-ai-guidelines"></a>
### Diretrizes de IA Disponíveis

O Laravel Boost inclui diretrizes de IA para os seguintes pacotes e frameworks. As diretrizes `core` fornecem conselhos genéricos e generalizados para a IA sobre o pacote indicado, aplicáveis a todas as versões.

<div class="overflow-auto">

| Pacote            | Versões Suportadas           |
| ----------------- | ---------------------------- |
| Core & Boost      | core                         |
| Laravel Framework | core, 10.x, 11.x, 12.x, 13.x |
| Livewire          | core, 2.x, 3.x, 4.x          |
| Flux UI           | core, free, pro              |
| Folio             | core                         |
| Herd              | core                         |
| Inertia Laravel   | core, 1.x, 2.x, 3.x          |
| Inertia React     | core, 1.x, 2.x, 3.x          |
| Inertia Vue       | core, 1.x, 2.x, 3.x          |
| Inertia Svelte    | core, 1.x, 2.x, 3.x          |
| MCP               | core                         |
| Pennant           | core                         |
| Pest              | core, 3.x, 4.x               |
| PHPUnit           | core                         |
| Pint              | core                         |
| Sail              | core                         |
| Tailwind CSS      | core, 3.x, 4.x               |
| Livewire Volt     | core                         |
| Wayfinder         | core                         |
| Enforce Tests     | conditional                  |

</div>

> **Nota:** Para manter suas diretrizes de IA atualizadas, consulte a seção [Mantendo os Recursos do Boost Atualizados](#keeping-boost-resources-updated).

<a id="adding-custom-ai-guidelines"></a>
### Adicionando Diretrizes de IA Personalizadas

Para complementar o Laravel Boost com suas próprias diretrizes de IA personalizadas, adicione arquivos `.blade.php` ou `.md` ao diretório `.ai/guidelines/*` da sua aplicação. Esses arquivos serão incluídos automaticamente junto com as diretrizes do Laravel Boost quando você executar `boost:install`.

<a id="overriding-boost-ai-guidelines"></a>
### Sobrescrevendo as Diretrizes de IA do Boost

Você pode sobrescrever as diretrizes de IA nativas do Boost criando suas próprias diretrizes personalizadas com caminhos de arquivo correspondentes. Quando você cria uma diretriz personalizada que corresponde ao caminho de uma diretriz existente do Boost, o Boost usará sua versão personalizada no lugar da nativa.

Por exemplo, para sobrescrever as diretrizes "Inertia React v2 Form Guidance" do Boost, crie um arquivo em `.ai/guidelines/inertia-react/2/forms.blade.php`. Quando você executar `boost:install`, o Boost incluirá a sua diretriz personalizada em vez da padrão.

<a id="third-party-package-ai-guidelines"></a>
### Diretrizes de IA de Pacotes de Terceiros

Se você mantém um pacote de terceiros e gostaria que o Boost incluísse diretrizes de IA para ele, pode fazer isso adicionando um arquivo `resources/boost/guidelines/core.blade.php` ao seu pacote. Quando os usuários do seu pacote executarem `php artisan boost:install`, o Boost carregará automaticamente as suas diretrizes.

As diretrizes de IA devem fornecer uma breve visão geral do que o seu pacote faz, descrever qualquer estrutura de arquivos ou convenção necessária e explicar como criar ou usar seus principais recursos (com exemplos de comandos ou trechos de código). Mantenha-as concisas, objetivas e focadas em boas práticas para que a IA possa gerar código correto para os seus usuários. Aqui está um exemplo:

```markdown
## Package Name

This package provides [brief description of functionality].

### Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

<a id="agent-skills"></a>
## Skills de Agentes

As [Skills de Agentes](https://agentskills.io/home) são módulos de conhecimento leves e direcionados que os agentes podem ativar sob demanda ao trabalhar em domínios específicos. Diferente das diretrizes, que são carregadas antecipadamente, as skills permitem que padrões detalhados e melhores práticas sejam carregados apenas quando relevantes, reduzindo o excesso de contexto e melhorando a relevância do código gerado pela IA.

Quando você executa `boost:install` e seleciona skills como um recurso, as skills são instaladas automaticamente com base nos pacotes detectados no seu `composer.json`. Por exemplo, se o seu projeto incluir `livewire/livewire`, a skill `livewire-development` será instalada automaticamente. As skills incluídas com o Boost, como `infer-conventions`, são instaladas independentemente dos pacotes que você possui.

<a id="available-skills"></a>
### Skills Disponíveis

<div class="overflow-auto">

| Skill                      | Pacote         |
| -------------------------- | -------------- |
| fluxui-development         | Flux UI        |
| folio-routing              | Folio          |
| infer-conventions          | Boost          |
| inertia-react-development  | Inertia React  |
| inertia-svelte-development | Inertia Svelte |
| inertia-vue-development    | Inertia Vue    |
| livewire-development       | Livewire       |
| mcp-development            | MCP            |
| pennant-development        | Pennant        |
| pest-testing               | Pest           |
| tailwindcss-development    | Tailwind CSS   |
| volt-development           | Volt           |
| wayfinder-development      | Wayfinder      |

</div>

> **Nota:** Para manter suas skills atualizadas, consulte a seção [Mantendo os Recursos do Boost Atualizados](#keeping-boost-resources-updated).

<a id="custom-skills"></a>
### Skills Personalizadas

Para criar suas próprias skills personalizadas, adicione um arquivo `SKILL.md` ao diretório `.ai/skills/{skill-name}/` da sua aplicação. Quando você executar `boost:update`, suas skills personalizadas serão instaladas junto com as skills nativas do Boost.

Por exemplo, para criar uma skill personalizada para a lógica de domínio da sua aplicação:

```
.ai/skills/creating-invoices/SKILL.md
```

<a id="overriding-skills"></a>
### Sobrescrevendo Skills

Você pode sobrescrever as skills nativas do Boost criando suas próprias skills personalizadas com nomes correspondentes. Quando você cria uma skill personalizada com o mesmo nome de uma skill existente do Boost, o Boost usará sua versão personalizada no lugar da nativa.

Por exemplo, para sobrescrever a skill `livewire-development` do Boost, crie um arquivo em `.ai/skills/livewire-development/SKILL.md`. Quando você executar `boost:update`, o Boost incluirá a sua skill personalizada em vez da padrão.

<a id="third-party-package-skills"></a>
### Skills de Pacotes de Terceiros

Se você mantém um pacote de terceiros e gostaria que o Boost incluísse skills para ele, pode fazer isso adicionando um arquivo `resources/boost/skills/{skill-name}/SKILL.md` ao seu pacote. Quando os usuários do seu pacote executarem `php artisan boost:install`, o Boost instalará automaticamente as suas skills de acordo com a preferência do usuário.

As skills do Boost seguem o [formato de Agent Skills](https://agentskills.io/what-are-skills) e devem ser estruturadas como uma pasta contendo um arquivo `SKILL.md` com frontmatter YAML e instruções em Markdown. O arquivo `SKILL.md` deve incluir o frontmatter obrigatório (`name` e `description`) e pode opcionalmente incluir scripts, templates e materiais de referência.

As skills devem descrever qualquer estrutura de arquivos ou convenção necessária e explicar como criar ou usar seus principais recursos (com exemplos de comandos ou trechos de código). Mantenha-as concisas, objetivas e focadas em boas práticas para que a IA possa gerar código correto para os seus usuários:

```markdown
---
name: package-name-development
description: Build and work with PackageName features, including components and workflows.
---

# Package Name Development

## When to use this skill
Use this skill when working with PackageName features...

## Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

$result = PackageName::featureTwo($param1, $param2);
```

<a id="guidelines-vs-skills"></a>
## Diretrizes vs. Skills

O Laravel Boost oferece duas formas distintas de fornecer aos agentes de IA contexto sobre a sua aplicação: **diretrizes** e **skills**.

**Diretrizes** são carregadas antecipadamente quando o agente de IA é iniciado, fornecendo o contexto essencial sobre as convenções e melhores práticas do Laravel que se aplicam de forma ampla a toda a sua base de código.

**Skills** são ativadas sob demanda ao trabalhar em tarefas específicas, contendo padrões detalhados para domínios particulares (como componentes Livewire ou testes Pest). Carregar skills apenas quando relevantes reduz o excesso de contexto e melhora a qualidade do código.

<div class="overflow-auto">

| Aspecto     | Diretrizes                         | Skills                            |
| ----------- | ---------------------------------- | --------------------------------- |
| **Carregamento** | Antecipado, sempre presente   | Sob demanda, quando relevante     |
| **Escopo**  | Amplo, fundamental                 | Focado, específico da tarefa      |
| **Propósito** | Convenções centrais e melhores práticas | Padrões detalhados de implementação |

</div>

Tanto as diretrizes quanto as skills descrevem o ecossistema Laravel. Para capturar as convenções da sua própria aplicação, você deve usar as [regras do projeto](#project-rules).

<a id="project-rules"></a>
## Regras do Projeto

Enquanto as diretrizes e as skills ensinam os agentes a escrever Laravel, as regras do projeto ensinam-nos a escrever a sua aplicação. Uma regra é qualquer coisa que você precisaria explicar novamente em cada nova sessão:

<div class="content-list" markdown="1">

- Decisões tomadas ao longo do caminho por você, pelos seus agentes ou pelos seus colegas de equipe.
- Diretrizes de estilo e preferências que são difíceis de fazer um agente seguir.
- Armadilhas e restrições que não podem ser inferidas a partir do código ao redor.

</div>

As regras são armazenadas como arquivos Markdown dentro do diretório `.ai/rules` da sua aplicação e devem ser versionadas no controle de código-fonte. Diferente da memória própria de um agente, que é pessoal e restrita à sessão, as suas regras são compartilhadas com a sua equipe e com todos os agentes que trabalham na sua aplicação.

Cada arquivo de regra declara, no seu frontmatter, os padrões glob de arquivos aos quais se aplica:

```markdown
---
paths:
  - app/Http/Controllers/**
---

# Http Controllers

## Extend BaseController for tenant scoping

All controllers must extend `App\Http\Controllers\BaseController`, which applies the
current tenant's query scope. Extending Laravel's base controller directly will leak
data across tenants.
```

Além disso, o Boost mantém um arquivo `.ai/rules/index.md` que mapeia os globs para seus arquivos de regra. Os agentes são instruídos a consultar este índice antes de planejar ou editar qualquer arquivo, para que uma regra só seja carregada quando for relevante:

```markdown
# Project Rules Index

Before planning or editing, find the row whose globs match the file's path and read that rule file.

| Applies to | Rule file |
| --- | --- |
| app/Http/Controllers/** | .ai/rules/controllers.md |
| app/Models/** | .ai/rules/models.md |
```

> **Nota:**
> Diferente do `.mcp.json` e dos arquivos de diretrizes gerados, o diretório `.ai/rules` deve ser versionado no controle de código-fonte para que as suas regras sejam compartilhadas com a sua equipe.

<a id="recording-rules"></a>
### Registrando Regras

Para registrar uma regra, basta pedir ao seu agente que a memorize:

```text
Remember that all money values are stored as integer cents, never as floats.
```

O agente invocará a ferramenta MCP `record-rule` do Boost com um `glob`, um `title` curto e uma `note`. Em seguida, o Boost registrará a regra na área correspondente, criando o arquivo de regra se necessário, e atualizará o índice.

Você deve sempre registrar regras usando a ferramenta `record-rule`, em vez de criar arquivos de regra manualmente. O Boost regenera o `.ai/rules/index.md` como parte do registro de uma regra, e os agentes dependem desse índice para descobrir quais regras se aplicam ao arquivo em que estão trabalhando. Um arquivo de regra adicionado manualmente não será descoberto até que o índice seja regenerado novamente.

<a id="inferring-your-applications-conventions"></a>
### Inferindo as Convenções da Sua Aplicação

Registrar regras uma a uma funciona bem daqui para frente; no entanto, uma aplicação existente já contém anos de convenções. A skill `infer-conventions` inicializará suas regras a partir do código que você já escreveu. Para começar, peça ao seu agente que use a skill:

```text
Use the infer-conventions skill
```

A skill varrerá a sua aplicação com base em uma lista de verificação de dimensões de convenções do Laravel, incluindo validação, controllers, autorização, models, arquitetura, testes, frontend, banco de dados e console, seguida por uma passagem aberta em busca de padrões como classes base, traits compartilhadas e layouts de módulos.

A skill documenta o que o seu código realmente faz, e não o que ele deveria fazer. Ela registra apenas convenções não padrão bem sustentadas por evidências, ignora os padrões do framework e qualquer coisa que o Pint ou o Rector já façam cumprir, e relata padrões genuinamente mistos em vez de registrá-los. Antes de escrever qualquer regra, a skill apresentará cada convenção descoberta, junto com as evidências que a sustentam, para a sua aprovação. Se você quiser que a skill registre todas as convenções descobertas sem confirmação, pode dizer a ela para "yolo".

<a id="disabling-project-rules"></a>
### Desativando Regras do Projeto

As regras do projeto são ativadas por padrão. Para desativá-las completamente, defina a seguinte variável de ambiente. Isso remove a ferramenta MCP `record-rule` e impede que o Boost gerencie o diretório `.ai/rules`:

```ini
BOOST_RULES_ENABLED=false
```

<a id="documentation-api"></a>
## API de Documentação

O Laravel Boost inclui uma API de Documentação que dá aos agentes de IA acesso a uma extensa base de conhecimento com mais de 17.000 informações específicas do Laravel. A API usa busca semântica com embeddings para entregar resultados precisos e sensíveis ao contexto.

A ferramenta MCP `Search Docs` permite que os agentes consultem o serviço de API de documentação hospedado do Laravel para obter documentação com base nos seus pacotes instalados. As diretrizes e skills de IA do Boost instruirão automaticamente o seu agente de codificação a usar esta API.

<div class="overflow-auto">

| Pacote            | Versões Suportadas     |
| ----------------- | ---------------------- |
| Laravel Framework | 10.x, 11.x, 12.x, 13.x |
| Filament          | 2.x, 3.x, 4.x, 5.x     |
| Flux UI           | 2.x Free, 2.x Pro      |
| Inertia           | 1.x, 2.x               |
| Livewire          | 1.x, 2.x, 3.x, 4.x     |
| Nova              | 4.x, 5.x               |
| Pest              | 3.x, 4.x               |
| Tailwind CSS      | 3.x, 4.x               |

</div>

<a id="extending-boost"></a>
## Estendendo o Boost

O Boost funciona com muitas IDEs e agentes de IA populares logo de início. Se a sua ferramenta de codificação ainda não for suportada, você pode criar o seu próprio agente e integrá-lo ao Boost.

<a id="adding-support-for-other-ides-ai-agents"></a>
### Adicionando Suporte a Outras IDEs / Agentes de IA

Para adicionar suporte a uma nova IDE ou agente de IA, crie uma classe que estenda `Laravel\Boost\Install\Agents\Agent` e implemente um ou mais dos seguintes contratos, dependendo do que você precisa:

- `Laravel\Boost\Contracts\SupportsGuidelines` - Adiciona suporte a diretrizes de IA.
- `Laravel\Boost\Contracts\SupportsMcp` - Adiciona suporte a MCP.
- `Laravel\Boost\Contracts\SupportsSkills` - Adiciona suporte a Skills de Agentes.

<a id="writing-the-agent"></a>
#### Escrevendo o Agente

```php
<?php

declare(strict_types=1);

namespace App;

use Laravel\Boost\Contracts\SupportsGuidelines;
use Laravel\Boost\Contracts\SupportsMcp;
use Laravel\Boost\Contracts\SupportsSkills;
use Laravel\Boost\Install\Agents\Agent;

class CustomAgent extends Agent implements SupportsGuidelines, SupportsMcp, SupportsSkills
{
    // Your implementation...
}
```

Para um exemplo de implementação, veja [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php).

<a id="registering-the-agent"></a>
#### Registrando o Agente

Registre o seu agente personalizado no método `boot` do `App\Providers\AppServiceProvider` da sua aplicação:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

Depois de registrado, o seu agente estará disponível para seleção ao executar `php artisan boost:install`.

---
title: "Desenvolvimento Assistido por IA"
---

- [Introdução](#introduction)
     - [Por que Laravel para Desenvolvimento com IA?](#why-laravel-for-ai-development)
  - [Laravel Boost](#laravel-boost)
     - [Instalação](#installation)
     - [Ferramentas Disponíveis](#available-tools)
     - [Diretrizes de IA](#ai-guidelines)
     - [Agent Skills](#agent-skills)
     - [Busca na Documentação](#documentation-search)
     - [Integração com Agentes](#agents-integration)

<a id="introduction"></a>
## Introdução

O Laravel está em uma posição única para ser o melhor framework para desenvolvimento assistido por IA e agêntico. A ascensão de agentes de programação com IA como [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com) e [GitHub Copilot](https://github.com/features/copilot) transformou a maneira como os desenvolvedores escrevem código. Essas ferramentas podem gerar funcionalidades inteiras, depurar problemas complexos e refatorar código em uma velocidade sem precedentes - mas sua eficácia depende muito do quanto elas entendem bem a sua base de código.

<a id="why-laravel-for-ai-development"></a>
### Por que Laravel para Desenvolvimento com IA?

As convenções opinativas do Laravel e sua estrutura bem definida o tornam um framework ideal para desenvolvimento assistido por IA. Quando você pede a um agente de IA para adicionar um controlador, ele sabe exatamente onde colocá-lo. Quando você precisa de uma nova migration, as convenções de nomenclatura e os locais dos arquivos são previsíveis. Essa consistência elimina as suposições que frequentemente fazem as ferramentas de IA errarem em frameworks mais flexíveis.

Além da organização de arquivos, a sintaxe expressiva e a documentação abrangente do Laravel fornecem aos agentes de IA o contexto de que precisam para gerar código preciso e idiomático. Funcionalidades como relacionamentos do Eloquent, form requests e middleware seguem padrões que os agentes conseguem entender e replicar de forma confiável. O resultado é um código gerado por IA que parece ter sido escrito por um desenvolvedor Laravel experiente, e não costurado a partir de trechos genéricos de PHP.

<a id="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost) fecha a lacuna entre os agentes de programação com IA e sua aplicação Laravel. O Boost é um servidor MCP (Model Context Protocol) equipado com mais de 15 ferramentas especializadas que fornecem aos agentes de IA um entendimento profundo da estrutura, do banco de dados, das rotas e muito mais da sua aplicação. Quando você instala o Boost, seu agente de IA se transforma de um assistente de código de propósito geral em um especialista em Laravel que entende a sua aplicação específica.

O Boost oferece três capacidades principais: um conjunto de ferramentas MCP para inspecionar e interagir com sua aplicação, diretrizes de IA componíveis criadas especificamente para o ecossistema Laravel, e uma poderosa API de documentação contendo mais de 17.000 itens de conhecimento específicos do Laravel.

<a id="installation"></a>
### Instalação

O Boost pode ser instalado em aplicações Laravel 10, 11, 12 e 13 que executam o PHP 8.1 ou superior. Para começar, instale o Boost como uma dependência de desenvolvimento:

```shell
composer require laravel/boost --dev
```

Depois de instalado, execute o instalador interativo:

```shell
php artisan boost:install
```

O instalador detectará automaticamente sua IDE e seus agentes de IA, permitindo que você selecione as integrações que fazem sentido para o seu projeto. O Boost gerará os arquivos de configuração necessários, como `.mcp.json` para editores compatíveis com MCP e arquivos de diretrizes para o contexto de IA.

> **Nota:**
> Arquivos de configuração gerados, como `.mcp.json`, `CLAUDE.md` e `boost.json`, podem ser adicionados com segurança ao seu `.gitignore` se você preferir que cada desenvolvedor configure seu próprio ambiente.

<a id="available-tools"></a>
### Ferramentas Disponíveis

O Boost expõe um conjunto abrangente de ferramentas para agentes de IA por meio do Model Context Protocol. Essas ferramentas permitem que os agentes entendam profundamente e interajam com sua aplicação Laravel:

<div class="content-list" markdown="1">

- **Introspecção de Aplicação** - Consulte suas versões de PHP e Laravel, liste os pacotes instalados e inspecione a configuração e as variáveis de ambiente da sua aplicação.
- **Ferramentas de Banco de Dados** - Inspecione o schema do seu banco de dados, execute queries somente leitura e entenda a estrutura dos seus dados sem sair da conversa.
- **Inspeção de Rotas** - Liste todas as rotas registradas com seus middleware, controladores e parâmetros.
- **Comandos Artisan** - Descubra os comandos Artisan disponíveis e seus argumentos, permitindo que os agentes sugiram e executem os comandos certos para sua tarefa.
- **Análise de Logs** - Leia e analise os arquivos de log da sua aplicação para ajudar a depurar problemas.
- **Logs do Navegador** - Acesse os logs e erros do console do navegador ao desenvolver com as ferramentas de frontend do Laravel.
- **Integração com o Tinker** - Execute código PHP no contexto da sua aplicação via Laravel Tinker, permitindo que os agentes testem hipóteses e verifiquem o comportamento.
- **Busca na Documentação** - Pesquise na documentação do ecossistema Laravel com resultados adaptados às versões dos pacotes instalados.

</div>

<a id="ai-guidelines"></a>
### Diretrizes de IA

O Boost inclui um conjunto abrangente de diretrizes de IA criadas especificamente para o ecossistema Laravel. Essas diretrizes ensinam os agentes de IA a escrever código Laravel idiomático, seguir as convenções do framework e evitar armadilhas comuns. As diretrizes são componíveis e conscientes da versão, o que significa que os agentes recebem instruções apropriadas para as versões exatas dos seus pacotes.

As diretrizes estão disponíveis para o próprio Laravel e mais de 16 pacotes do ecossistema Laravel, incluindo:

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x e 4.x)
- Inertia.js (variantes React, Svelte e Vue)
- Tailwind CSS (3.x e 4.x)
- Filament (3.x e 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- E muitos outros

</div>

Quando você executa `boost:install`, o Boost detecta automaticamente quais pacotes sua aplicação usa e monta as diretrizes relevantes nos arquivos de contexto de IA do seu projeto.

<a id="agent-skills"></a>
### Agent Skills

[Agent Skills](https://agentskills.io/home) são módulos de conhecimento leves e direcionados que os agentes podem ativar sob demanda ao trabalhar em domínios específicos. Ao contrário das diretrizes, que são carregadas previamente, as skills permitem que padrões detalhados e boas práticas sejam carregados apenas quando relevantes, reduzindo o inchaço do contexto e melhorando a relevância do código gerado por IA.

As skills estão disponíveis para pacotes populares do Laravel como Livewire, Inertia, Tailwind CSS, Pest e muito mais. Quando você executa `boost:install` e seleciona skills como uma funcionalidade, as skills são instaladas automaticamente com base nos pacotes detectados no seu `composer.json`.

<a id="documentation-search"></a>
### Busca na Documentação

O Boost inclui uma poderosa API de documentação que dá aos agentes de IA acesso a mais de 17.000 itens de documentação do ecossistema Laravel. Ao contrário de buscas genéricas na web, essa documentação é indexada, vetorizada e filtrada para corresponder às versões exatas dos seus pacotes.

Quando um agente precisa entender como uma funcionalidade funciona, ele pode pesquisar na API de documentação do Boost e receber informações precisas e específicas da versão. Isso elimina o problema comum de agentes de IA sugerirem métodos ou sintaxe obsoletos de versões mais antigas do framework.

<a id="agents-integration"></a>
### Integração com Agentes

O Boost se integra com IDEs populares e ferramentas de IA que suportam o Model Context Protocol. Para instruções detalhadas de configuração do Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot e Junie, consulte a seção [Configure Seus Agentes](../boost/#set-up-your-agents) da documentação do Boost.

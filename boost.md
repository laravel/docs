---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Boost

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Налаштування агентів](#set-up-your-agents)
    - [Оновлення ресурсів Boost](#keeping-boost-resources-updated)
- [MCP-сервер](#mcp-server)
    - [Доступні інструменти MCP](#available-mcp-tools)
    - [Ручна реєстрація MCP-сервера](#manually-registering-the-mcp-server)
- [Настанови для AI](#ai-guidelines)
    - [Доступні настанови для AI](#available-ai-guidelines)
    - [Додавання власних настанов для AI](#adding-custom-ai-guidelines)
    - [Перевизначення настанов Boost](#overriding-boost-ai-guidelines)
    - [Настанови для AI у сторонніх пакетах](#third-party-package-ai-guidelines)
- [Навички агентів](#agent-skills)
    - [Доступні навички](#available-skills)
    - [Власні навички](#custom-skills)
    - [Перевизначення навичок](#overriding-skills)
    - [Навички у сторонніх пакетах](#third-party-package-skills)
- [Настанови проти навичок](#guidelines-vs-skills)
- [API документації](#documentation-api)
- [Розширення Boost](#extending-boost)
    - [Додавання підтримки інших IDE та AI-агентів](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## Вступ

Laravel Boost пришвидшує розробку з допомогою AI, надаючи ключові настанови й навички агентів, які допомагають AI-агентам писати якісні застосунки Laravel відповідно до найкращих практик фреймворку.

Boost також надає потужний API документації екосистеми Laravel, що поєднує вбудований інструмент MCP із великою базою знань, яка містить понад 17 000 фрагментів інформації про Laravel, - усе це підсилено семантичним пошуком на ембедингах для точних результатів з урахуванням контексту. Boost вказує AI-агентам на кшталт Claude Code і Cursor користуватися цим API, щоб дізнаватися про найновіші можливості й найкращі практики Laravel.

<a name="installation"></a>
## Встановлення

Laravel Boost можна встановити через Composer:

```shell
composer require laravel/boost --dev
```

Далі встановіть MCP-сервер і настанови щодо написання коду:

```shell
php artisan boost:install
```

Команда `boost:install` згенерує відповідні файли настанов і навичок для тих агентів, яких ви обрали під час встановлення.

Коли Laravel Boost встановлено, ви готові писати код у Cursor, Claude Code чи будь-якому іншому AI-агенті на ваш вибір.

> [!NOTE]
> Сміливо додавайте згенерований конфігураційний файл MCP (`.mcp.json`), файли настанов (`CLAUDE.md`, `AGENTS.md`, `junie/` тощо) та конфігураційний файл `boost.json` до `.gitignore` вашого застосунку - ці файли автоматично перегенеровуються під час виконання `boost:install` і `boost:update`.

<a name="set-up-your-agents"></a>
### Налаштування агентів

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

```text tab=Gemini CLI
Gemini CLI support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
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

<a name="keeping-boost-resources-updated"></a>
### Оновлення ресурсів Boost

Вам, можливо, варто час від часу оновлювати локальні ресурси Boost (настанови для AI та навички), щоб вони відповідали найновішим версіям встановлених у вас пакетів екосистеми Laravel. Для цього скористайтеся артизан-командою `boost:update`.

```shell
php artisan boost:update
```

Ви також можете автоматизувати цей процес, додавши команду до скриптів Composer «post-update-cmd»:

```json
{
  "scripts": {
    "post-update-cmd": [
      "@php artisan boost:update --ansi"
    ]
  }
}
```

За замовчуванням команда `boost:update` оновлюватиме лише ті ресурси Boost, які вже опубліковано у вашому застосунку. Якщо ви хочете, щоб Boost просканував ваш застосунок на нововстановлені пакети й запропонував опублікувати відповідні настанови й навички, скористайтеся опцією `--discover`:

```shell
php artisan boost:update --discover
```

<a name="mcp-server"></a>
## MCP-сервер

Laravel Boost надає MCP-сервер (Model Context Protocol), який відкриває AI-агентам інструменти для взаємодії з вашим застосунком Laravel. Ці інструменти дають агентам змогу оглядати структуру застосунку, робити запити до бази даних, виконувати код тощо.

<a name="available-mcp-tools"></a>
### Доступні інструменти MCP

<div class="overflow-auto">

| Ім'я                 | Примітки                                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Application Info     | Читає версії PHP і Laravel, рушій бази даних, список пакетів екосистеми з версіями та моделі Eloquent       |
| Browser Logs         | Читає логи та помилки з браузера                                                                            |
| Database Connections | Оглядає доступні підключення до бази даних, зокрема стандартне                                              |
| Database Query       | Виконує запит до бази даних                                                                                 |
| Database Schema      | Читає схему бази даних                                                                                      |
| Get Absolute URL     | Перетворює відносні URI на абсолютні, щоб агенти генерували коректні URL                                    |
| Last Error           | Читає останню помилку з файлів логу застосунку                                                              |
| Read Log Entries     | Читає останні N записів логу                                                                                |
| Search Docs          | Робить запит до хостованого сервісу API документації Laravel, щоб отримати документацію за встановленими пакетами |

</div>

<a name="manually-registering-the-mcp-server"></a>
### Ручна реєстрація MCP-сервера

Іноді вам може знадобитися зареєструвати MCP-сервер Laravel Boost у вашому редакторі вручну. Реєструйте MCP-сервер із такими даними:

<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

Приклад JSON:

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

<a name="ai-guidelines"></a>
## Настанови для AI

Настанови для AI - це складані файли інструкцій, які завантажуються наперед, щоб дати AI-агентам ключовий контекст про пакети екосистеми Laravel. Ці настанови містять основні угоди, найкращі практики та специфічні для фреймворку патерни, які допомагають агентам генерувати послідовний і якісний код.

<a name="available-ai-guidelines"></a>
### Доступні настанови для AI

Laravel Boost містить настанови для AI для таких пакетів і фреймворків. Настанови `core` дають загальні поради AI щодо відповідного пакета, застосовні до всіх версій.

<div class="overflow-auto">

| Пакет             | Підтримувані версії    |
| ----------------- | ---------------------- |
| Core & Boost      | core                   |
| Laravel Framework | core, 10.x, 11.x, 12.x, 13.x |
| Livewire          | core, 2.x, 3.x, 4.x    |
| Flux UI           | core, free, pro        |
| Folio             | core                   |
| Herd              | core                   |
| Inertia Laravel   | core, 1.x, 2.x, 3.x    |
| Inertia React     | core, 1.x, 2.x, 3.x    |
| Inertia Vue       | core, 1.x, 2.x, 3.x    |
| Inertia Svelte    | core, 1.x, 2.x, 3.x    |
| MCP               | core                   |
| Pennant           | core                   |
| Pest              | core, 3.x, 4.x         |
| PHPUnit           | core                   |
| Pint              | core                   |
| Sail              | core                   |
| Tailwind CSS      | core, 3.x, 4.x         |
| Livewire Volt     | core                   |
| Wayfinder         | core                   |
| Enforce Tests     | conditional            |

</div>

> **Примітка:** щоб тримати настанови для AI актуальними, дивіться розділ [Оновлення ресурсів Boost](#keeping-boost-resources-updated).

<a name="adding-custom-ai-guidelines"></a>
### Додавання власних настанов для AI

Щоб доповнити Laravel Boost власними настановами для AI, додайте файли `.blade.php` чи `.md` до каталогу `.ai/guidelines/*` вашого застосунку. Ці файли автоматично потраплять до настанов Laravel Boost, коли ви виконаєте `boost:install`.

<a name="overriding-boost-ai-guidelines"></a>
### Перевизначення настанов Boost

Ви можете перевизначити вбудовані настанови Boost для AI, створивши власні настанови з такими самими шляхами до файлів. Коли ви створюєте власну настанову, шлях якої збігається зі шляхом наявної настанови Boost, Boost використає вашу версію замість вбудованої.

Наприклад, щоб перевизначити настанови Boost «Inertia React v2 Form Guidance», створіть файл `.ai/guidelines/inertia-react/2/forms.blade.php`. Коли ви виконаєте `boost:install`, Boost включить вашу настанову замість стандартної.

<a name="third-party-package-ai-guidelines"></a>
### Настанови для AI у сторонніх пакетах

Якщо ви підтримуєте сторонній пакет і хочете, щоб Boost включав настанови для AI щодо нього, додайте до пакета файл `resources/boost/guidelines/core.blade.php`. Коли користувачі вашого пакета виконають `php artisan boost:install`, Boost автоматично завантажить ваші настанови.

Настанови для AI мають коротко описувати, що робить ваш пакет, окреслювати потрібну структуру файлів чи угоди й пояснювати, як створювати чи використовувати його основні можливості (з прикладами команд або фрагментами коду). Тримайте їх стислими, дієвими й зосередженими на найкращих практиках, щоб AI міг генерувати правильний код для ваших користувачів. Ось приклад:

```php
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

<a name="agent-skills"></a>
## Навички агентів

[Навички агентів](https://agentskills.io/home) - це легкі цільові модулі знань, які агенти можуть активувати на вимогу, працюючи в конкретних доменах. На відміну від настанов, які завантажуються наперед, навички дозволяють підтягувати детальні патерни й найкращі практики лише тоді, коли вони доречні, - це зменшує роздування контексту й підвищує релевантність згенерованого AI коду.

Коли ви виконуєте `boost:install` і обираєте навички як можливість, вони встановлюються автоматично - за пакетами, виявленими у вашому `composer.json`. Наприклад, якщо ваш проєкт містить `livewire/livewire`, навичку `livewire-development` буде встановлено автоматично.

<a name="available-skills"></a>
### Доступні навички

<div class="overflow-auto">

| Навичка                    | Пакет          |
| -------------------------- | -------------- |
| fluxui-development         | Flux UI        |
| folio-routing              | Folio          |
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

> **Примітка:** щоб тримати навички актуальними, дивіться розділ [Оновлення ресурсів Boost](#keeping-boost-resources-updated).

<a name="custom-skills"></a>
### Власні навички

Щоб створити власні навички, додайте файл `SKILL.md` до каталогу `.ai/skills/{skill-name}/` вашого застосунку. Коли ви виконаєте `boost:update`, ваші навички буде встановлено разом із вбудованими навичками Boost.

Наприклад, щоб створити власну навичку для доменної логіки вашого застосунку:

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### Перевизначення навичок

Ви можете перевизначити вбудовані навички Boost, створивши власні навички з такими самими іменами. Коли ви створюєте власну навичку, ім'я якої збігається з іменем наявної навички Boost, Boost використає вашу версію замість вбудованої.

Наприклад, щоб перевизначити навичку Boost `livewire-development`, створіть файл `.ai/skills/livewire-development/SKILL.md`. Коли ви виконаєте `boost:update`, Boost включить вашу навичку замість стандартної.

<a name="third-party-package-skills"></a>
### Навички у сторонніх пакетах

Якщо ви підтримуєте сторонній пакет і хочете, щоб Boost включав навички щодо нього, додайте до пакета файл `resources/boost/skills/{skill-name}/SKILL.md`. Коли користувачі вашого пакета виконають `php artisan boost:install`, Boost автоматично встановить ваші навички відповідно до їхніх уподобань.

Навички Boost підтримують [формат Agent Skills](https://agentskills.io/what-are-skills) і мають бути оформлені як каталог із файлом `SKILL.md`, що містить YAML-хедер та інструкції в Markdown. Файл `SKILL.md` має містити обов'язковий хедер (`name` та `description`), а також може за бажання містити скрипти, шаблони й довідкові матеріали.

Навички мають окреслювати потрібну структуру файлів чи угоди й пояснювати, як створювати чи використовувати основні можливості (з прикладами команд або фрагментами коду). Тримайте їх стислими, дієвими й зосередженими на найкращих практиках, щоб AI міг генерувати правильний код для ваших користувачів:

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

<a name="guidelines-vs-skills"></a>
## Настанови проти навичок

Laravel Boost надає два різні способи дати AI-агентам контекст про ваш застосунок: **настанови** та **навички**.

**Настанови** завантажуються наперед при старті AI-агента й дають ключовий контекст про угоди та найкращі практики Laravel, які широко застосовні у всій вашій кодовій базі.

**Навички** активуються на вимогу під час роботи над конкретними завданнями й містять детальні патерни для окремих доменів (як-от компоненти Livewire чи тести Pest). Завантаження навичок лише за потреби зменшує роздування контексту й підвищує якість коду.

<div class="overflow-auto">

| Аспект          | Настанови                          | Навички                          |
| --------------- | ---------------------------------- | -------------------------------- |
| **Завантаження**| Наперед, присутні завжди           | На вимогу, коли доречні          |
| **Обсяг**       | Широкий, фундаментальний           | Вузький, під конкретне завдання  |
| **Призначення** | Основні угоди й найкращі практики  | Детальні патерни реалізації      |

</div>

<a name="documentation-api"></a>
## API документації

Laravel Boost містить API документації, який дає AI-агентам доступ до великої бази знань із понад 17 000 фрагментів інформації про Laravel. Цей API використовує семантичний пошук на ембедингах, щоб видавати точні результати з урахуванням контексту.

Інструмент MCP `Search Docs` дозволяє агентам робити запити до хостованого сервісу API документації Laravel і отримувати документацію за встановленими у вас пакетами. Настанови й навички Boost автоматично вкажуть вашому агенту користуватися цим API.

<div class="overflow-auto">

| Пакет             | Підтримувані версії |
| ----------------- | ------------------ |
| Laravel Framework | 10.x, 11.x, 12.x, 13.x |
| Filament          | 2.x, 3.x, 4.x, 5.x |
| Flux UI           | 2.x Free, 2.x Pro  |
| Inertia           | 1.x, 2.x           |
| Livewire          | 1.x, 2.x, 3.x, 4.x |
| Nova              | 4.x, 5.x           |
| Pest              | 3.x, 4.x           |
| Tailwind CSS      | 3.x, 4.x           |

</div>

<a name="extending-boost"></a>
## Розширення Boost

Boost працює з багатьма популярними IDE та AI-агентами одразу з коробки. Якщо ваш інструмент ще не підтримується, ви можете створити власного агента й інтегрувати його з Boost.

<a name="adding-support-for-other-ides-ai-agents"></a>
### Додавання підтримки інших IDE та AI-агентів

Щоб додати підтримку нової IDE чи AI-агента, створіть клас, який успадковує `Laravel\Boost\Install\Agents\Agent`, і реалізуйте один чи кілька таких контрактів - залежно від ваших потреб:

- `Laravel\Boost\Contracts\SupportsGuidelines` - додає підтримку настанов для AI.
- `Laravel\Boost\Contracts\SupportsMcp` - додає підтримку MCP.
- `Laravel\Boost\Contracts\SupportsSkills` - додає підтримку навичок агентів.

<a name="writing-the-agent"></a>
#### Написання агента

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

Приклад реалізації дивіться в [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php).

<a name="registering-the-agent"></a>
#### Реєстрація агента

Зареєструйте свого агента в методі `boot` класу `App\Providers\AppServiceProvider` вашого застосунку:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

Коли агента зареєстровано, він буде доступний для вибору під час виконання `php artisan boost:install`.

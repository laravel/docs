---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel AI SDK

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Конфігурація](#configuration)
    - [Власні базові URL](#custom-base-urls)
    - [Провайдери, сумісні з OpenAI](#openai-compatible-providers)
    - [Підтримка провайдерів](#provider-support)
- [Агенти](#agents)
    - [Промптинг](#prompting)
    - [Контекст розмови](#conversation-context)
    - [Структурований вивід](#structured-output)
    - [Вкладення](#attachments)
    - [Стримінг](#streaming)
    - [Бродкастинг](#broadcasting)
    - [Черги](#queueing)
    - [Інструменти](#tools)
    - [Інструменти файлового сховища](#file-storage-tools)
    - [MCP-інструменти](#mcp-tools)
    - [Інструменти провайдера](#provider-tools)
    - [Субагенти](#sub-agents)
    - [Middleware](#middleware)
    - [Анонімні агенти](#anonymous-agents)
    - [Конфігурація агента](#agent-configuration)
    - [Опції провайдера](#provider-options)
- [Схвалення інструментів людиною](#human-tool-approval)
    - [Повний потік схвалення](#complete-approval-flow)
- [Зображення](#images)
- [Аудіо (TTS)](#audio)
- [Транскрибування (STT)](#transcription)
- [Стислий переказ тексту](#text-summarization)
- [Ембединги](#embeddings)
    - [Мультимодальні ембединги](#multimodal-embeddings)
    - [Запити до ембедингів](#querying-embeddings)
    - [Кешування ембедингів](#caching-embeddings)
- [Переранжування](#reranking)
- [Файли](#files)
- [Векторні сховища](#vector-stores)
    - [Додавання файлів до сховищ](#adding-files-to-stores)
- [Резервні провайдери](#failover)
- [Тестування](#testing)
    - [Агенти](#testing-agents)
    - [Зображення](#testing-images)
    - [Аудіо](#testing-audio)
    - [Транскрибування](#testing-transcriptions)
    - [Ембединги](#testing-embeddings)
    - [Переранжування](#testing-reranking)
    - [Файли](#testing-files)
    - [Векторні сховища](#testing-vector-stores)
- [Події](#events)

<a name="introduction"></a>
## Вступ

[Laravel AI SDK](https://github.com/laravel/ai) дає уніфікований, виразний API для взаємодії з AI-провайдерами, як-от OpenAI, Anthropic, Gemini тощо. За допомогою AI SDK ви можете створювати розумних агентів з інструментами та структурованим виводом, генерувати зображення, синтезувати й транскрибувати аудіо, створювати векторні ембединги та багато іншого - і все це через узгоджений, дружній до Laravel інтерфейс.

<a name="installation"></a>
## Встановлення

Встановити Laravel AI SDK можна через Composer:

```shell
composer require laravel/ai
```

Далі вам слід опублікувати конфігураційний файл і файли міграцій AI SDK артизан-командою `vendor:publish`:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

Насамкінець виконайте міграції бази даних вашого застосунку. Це створить таблиці `agent_conversations` і `agent_conversation_messages`, які AI SDK використовує для зберігання розмов:

```shell
php artisan migrate
```

<a name="configuration"></a>
### Конфігурація

Ви можете визначити облікові дані своїх AI-провайдерів у конфігураційному файлі `config/ai.php` вашого застосунку або як змінні оточення у файлі `.env`:

```ini
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=
COHERE_API_KEY=
DEEPSEEK_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
OLLAMA_API_KEY=
OPENAI_API_KEY=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_URL=
OPENROUTER_API_KEY=
JINA_API_KEY=
VOYAGEAI_API_KEY=
XAI_API_KEY=
```

Моделі за замовчуванням для тексту, зображень, аудіо, транскрибування та ембедингів також можна налаштувати в конфігураційному файлі `config/ai.php` вашого застосунку.

<a name="custom-base-urls"></a>
### Власні базові URL

За замовчуванням Laravel AI SDK підключається безпосередньо до публічного API-ендпоїнта кожного провайдера. Однак вам може знадобитися спрямувати запити через інший ендпоїнт - наприклад, коли ви користуєтеся проксі-сервісом для централізованого керування API-ключами, реалізуєте обмеження частоти чи спрямовуєте трафік через корпоративний шлюз.

Ви можете налаштувати власні базові URL, додавши параметр `url` до конфігурації свого провайдера:

```php
'providers' => [
    'openai' => [
        'driver' => 'openai',
        'key' => env('OPENAI_API_KEY'),
        'url' => env('OPENAI_URL'),
    ],

    'anthropic' => [
        'driver' => 'anthropic',
        'key' => env('ANTHROPIC_API_KEY'),
        'url' => env('ANTHROPIC_BASE_URL'),
    ],
],
```

Це корисно, коли ви спрямовуєте запити через проксі-сервіс (як-от LiteLLM чи Azure OpenAI Gateway) або використовуєте альтернативні ендпоїнти.

Власні базові URL підтримуються для таких провайдерів: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI та OpenRouter.

<a name="openai-compatible-providers"></a>
### Провайдери, сумісні з OpenAI

Якщо ви користуєтеся API, сумісним з OpenAI, як-от LM Studio, vLLM, Together, Fireworks чи локальним шлюзом, ви можете налаштувати провайдер `openai-compatible`. Опція `url` обов'язкова, а опція `key` необов'язкова і, якщо присутня, надсилатиметься як bearer-токен:

```php
'providers' => [
    'local' => [
        'driver' => 'openai-compatible',
        'url' => env('LOCAL_AI_URL'),
        'key' => env('LOCAL_AI_API_KEY'),
    ],
],
```

Щойно провайдер налаштовано, ви можете використовувати його за іменем, як і будь-який інший:

```php
agent()->prompt('What is Laravel?', provider: 'local', model: 'local-model');
```

Ви також можете налаштувати для провайдера текстову модель за замовчуванням, щоб не передавати модель явно:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'text' => [
            'default' => env('LOCAL_AI_MODEL'),
        ],
    ],
],
```

Провайдери, сумісні з OpenAI, підтримують генерацію тексту, стримінг, інструменти, структурований вивід і вкладення зображень. Якщо ваш ендпоїнт потребує додаткових полів у тілі запиту, передайте їх через [опції провайдера](#provider-options).

<a name="provider-support"></a>
### Підтримка провайдерів

AI SDK підтримує різні провайдери для своїх можливостей. Наведена нижче таблиця підсумовує, які провайдери доступні для кожної можливості:

<div class="overflow-auto">

| Feature | Providers |
|---|---|
| Text | OpenAI, OpenAI Compatible, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter |
| Images | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter |
| TTS | OpenAI, ElevenLabs, Gemini |
| STT | OpenAI, ElevenLabs, Mistral, Gemini |
| Embeddings | OpenAI, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter |
| Reranking | Cohere, Jina, VoyageAI |
| Files | OpenAI, Anthropic, Gemini, Azure |

</div>

Enum `Laravel\Ai\Enums\Lab` можна використовувати для посилання на провайдерів у вашому коді замість звичайних рядків:

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::OpenAiCompatible;
Lab::Gemini;
// ...
```

<a name="agents"></a>
## Агенти

Агенти - це фундаментальний будівельний блок для взаємодії з AI-провайдерами в Laravel AI SDK. Кожен агент - це окремий PHP-клас, що інкапсулює інструкції, контекст розмови, інструменти й схему виводу, потрібні для взаємодії з великою мовною моделлю. Уявіть агента як спеціалізованого асистента - тренера з продажів, аналізатора документів, бота підтримки, - якого ви налаштовуєте один раз і промптите за потреби у своєму застосунку.

Створити агента можна артизан-командою `make:agent`:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

У згенерованому класі агента ви можете визначити системний промпт / інструкції, контекст повідомлень, доступні інструменти й схему виводу (якщо потрібно):

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\RetrievePreviousTranscripts;
use App\Models\History;
use App\Models\User;
use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Messages\Message;
use Laravel\Ai\Promptable;
use Stringable;

class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput
{
    use Promptable;

    public function __construct(public User $user) {}

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * Get the list of messages comprising the conversation so far.
     */
    public function messages(): iterable
    {
        return History::where('user_id', $this->user->id)
            ->latest()
            ->limit(50)
            ->get()
            ->reverse()
            ->map(function ($message) {
                return new Message($message->role, $message->content);
            })->all();
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RetrievePreviousTranscripts,
        ];
    }

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'feedback' => $schema->string()->required(),
            'score' => $schema->integer()->min(1)->max(10)->required(),
        ];
    }
}
```

<a name="prompting"></a>
### Промптинг

Щоб надіслати промпт агенту, спершу створіть екземпляр методом `make` чи звичайним інстанціюванням, а потім викличте `prompt`:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

Метод `make` створює вашого агента через контейнер, що дозволяє автоматичне впровадження залежностей. Ви також можете передати аргументи до конструктора агента:

```php
$agent = SalesCoach::make(user: $user);
```

Передавши до методу `prompt` додаткові аргументи, ви можете перевизначити провайдера, модель чи HTTP-тайм-аут за замовчуванням під час промптингу:

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 120,
);
```

<a name="conversation-context"></a>
### Контекст розмови

Якщо ваш агент реалізує інтерфейс `Conversational`, ви можете скористатися методом `messages`, щоб повернути попередній контекст розмови, якщо він є:

```php
use App\Models\History;
use Laravel\Ai\Messages\Message;

/**
 * Get the list of messages comprising the conversation so far.
 */
public function messages(): iterable
{
    return History::where('user_id', $this->user->id)
        ->latest()
        ->limit(50)
        ->get()
        ->reverse()
        ->map(function ($message) {
            return new Message($message->role, $message->content);
        })->all();
}
```

<a name="remembering-conversations"></a>
#### Запам'ятовування розмов

> **Warning:** Перш ніж користуватися трейтом `RemembersConversations`, вам слід опублікувати й виконати міграції AI SDK артизан-командою `vendor:publish`. Ці міграції створять потрібні таблиці бази даних для зберігання розмов.

Якщо ви хочете, щоб Laravel автоматично зберігав і завантажував історію розмов вашого агента, скористайтеся трейтом `RemembersConversations`. Цей трейт дає простий спосіб зберігати повідомлення розмови в базі даних без ручної реалізації інтерфейсу `Conversational`:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Concerns\RemembersConversations;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, Conversational
{
    use Promptable, RemembersConversations;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

Використовуючи трейт `RemembersConversations`, не визначайте метод `messages` у класі агента вручну. Якщо метод `messages` присутній, він матиме перевагу над реалізацією трейта, і історія розмови не завантажуватиметься з бази даних.

Щоб розпочати нову розмову для користувача, викличте метод `forUser` перед промптингом:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

ID розмови повертається у відповіді, і його можна зберегти для подальшого використання. Якщо ви хочете отримувати всі розмови користувача через Eloquent, додайте трейт `HasConversations` до своєї моделі користувача:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Ai\Concerns\HasConversations;

class User extends Authenticatable
{
    use HasConversations;
}
```

Щойно трейт додано до вашої моделі, ви можете отримувати розмови користувача й робити до них запити через зв'язок `conversations`:

```php
$conversations = $user->conversations()
    ->latest('updated_at')
    ->paginate(20);
```

Щоб продовжити наявну розмову, скористайтеся методом `continue`:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

Використовуючи трейт `RemembersConversations`, попередні повідомлення автоматично завантажуються й додаються до контексту розмови під час промптингу. Нові повідомлення (як користувача, так і асистента) автоматично зберігаються після кожної взаємодії.

<a name="conversation-participants"></a>
#### Учасники розмови

Хоча користувачі - найпоширеніші учасники розмов, розмови можуть належати будь-якій Eloquent-моделі. Скористайтеся методом `forParticipant`, щоб розпочати розмову для іншого типу моделі:

```php
$response = (new SalesCoach)
    ->forParticipant($team)
    ->prompt('Review our latest sales results.');
```

Morph-клас і первинний ключ учасника зберігаються разом з розмовою. Тому моделі різних типів з однаковим первинним ключем, як-от `User` з ID `1` і `Team` з ID `1`, мають окремі історії розмов. Метод `forUser` є аліасом до `forParticipant`.

Ви можете продовжити найновішу розмову учасника методом `continueLastConversation`:

```php
$response = (new SalesCoach)
    ->continueLastConversation($team)
    ->prompt('Tell me more about that.');
```

Продовжуючи конкретну розмову, передайте учасника до методу `continue`:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $team)
    ->prompt('Tell me more about that.');
```

Трейт `HasConversations` можна додати до будь-якої Eloquent-моделі, що бере участь у розмовах. Отриманий зв'язок `conversations` є поліморфним зв'язком, обмеженим типом і первинним ключем цієї моделі. Ви також можете звернутися до учасника, якому належить розмова, через зворотний зв'язок:

```php
$conversations = $team->conversations;

$participant = $conversation->participant;
```

Якщо ваш застосунок використовує кілька типів моделей-учасників, вам варто визначити [morph-мапу Eloquent](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types), щоб збережені типи учасників не були прив'язані до імен ваших класів моделей.

> [!WARNING]
> Метод `continue` не перевіряє, чи заданий учасник володіє розмовою. Ваш застосунок має авторизувати доступ до розмови, перш ніж продовжувати її.

<a name="structured-output"></a>
### Структурований вивід

Якщо ви хочете, щоб ваш агент повертав структурований вивід, реалізуйте інтерфейс `HasStructuredOutput`, який вимагає, щоб агент визначив метод `schema`:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

Промптуючи агента, який повертає структурований вивід, ви можете звертатися до отриманого `StructuredAgentResponse` як до масиву:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="structured-output-nested-objects"></a>
#### Вкладені об'єкти

Щоб визначити вкладений структурований вивід, скористайтеся методом `object` із замиканням:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
            'metadata' => $schema->object(fn ($schema) => [
                'confidence' => $schema->string()->enum(['low', 'medium', 'high'])->required(),
                'language' => $schema->string()->required(),
            ])->required(),
        ];
    }
}
```

<a name="structured-output-arrays-of-objects"></a>
#### Масиви об'єктів

Якщо ваш агент має повертати список структурованих елементів, поєднайте методи `array` та `object`:

```php
public function schema(JsonSchema $schema): array
{
    return [
        'feedback' => $schema->array()
            ->items(
                $schema->object(fn ($schema) => [
                    'comment' => $schema->string()->required(),
                    'score' => $schema->integer()->required(),
                ])
            )
            ->required(),
    ];
}
```

Якщо значення може відповідати одній з кількох схем, скористайтеся методом `anyOf`:

```php
public function schema(JsonSchema $schema): array
{
    return [
        'content' => $schema->anyOf([
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['article'])->required(),
                'title' => $schema->string()->required(),
            ]),
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['image'])->required(),
                'url' => $schema->string()->required(),
            ]),
        ])->required(),
    ];
}
```

<a name="attachments"></a>
### Вкладення

Промптуючи, ви також можете передати разом з промптом вкладення, щоб модель могла оглянути зображення й документи:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf') // Attach a document from a filesystem disk...
        Files\Document::fromPath('/home/laravel/transcript.md') // Attach a document from a local path...
        $request->file('transcript'), // Attach an uploaded file...
    ]
);
```

Так само клас `Laravel\Ai\Files\Image` можна використати, щоб прикріпити зображення до промпта:

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg') // Attach an image from a filesystem disk...
        Files\Image::fromPath('/home/laravel/photo.jpg') // Attach an image from a local path...
        $request->file('photo'), // Attach an uploaded file...
    ]
);
```

<a name="streaming"></a>
### Стримінг

Ви можете стримити відповідь агента, викликавши метод `stream`. Повернутий `StreamableAgentResponse` можна повернути з маршруту, щоб автоматично надіслати клієнту потокову відповідь (SSE):

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

Метод `then` можна використати, щоб передати замикання, яке буде викликано, коли всю відповідь буде передано клієнту:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Responses\StreamedAgentResponse;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->then(function (StreamedAgentResponse $response) {
            // $response->text, $response->events, $response->usage...
        });
});
```

Як альтернативу ви можете вручну проходити по потокових подіях:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Стримінг за протоколом Vercel AI SDK

Ви можете стримити події за [протоколом стримінгу Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol), викликавши метод `usingVercelDataProtocol` на потоковій відповіді:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```

<a name="broadcasting"></a>
### Бродкастинг

Ви можете бродкастити потокові події кількома способами. По-перше, ви можете просто викликати метод `broadcast` чи `broadcastNow` на потоковій події:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

Або ж ви можете викликати метод `broadcastOnQueue` агента, щоб поставити операцію агента в чергу й бродкастити потокові події, щойно вони стають доступними:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...'
    new Channel('channel-name'),
);
```

<a name="skipping-oversized-events"></a>
#### Пропуск завеликих подій

Деякі платформи бродкастингу обмежують WebSocket-повідомлення приблизно 10 КБ. Насичені даними потокові події, як-от великі результати інструментів, можуть перевищити це обмеження і зламати бродкастинг. Ви можете виключити конкретні типи подій з бродкастингу атрибутом `WithoutBroadcasting`:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\WithoutBroadcasting;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;
use Laravel\Ai\Streaming\Events\ToolCall;
use Laravel\Ai\Streaming\Events\ToolResult;

#[WithoutBroadcasting(ToolCall::class, ToolResult::class)]
class SearchAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```

Виключені події ніколи не бродкастяться, але їх усе одно зберігають у таблиці `agent_conversation_messages`, тож ваш фронтенд може завантажити повні дані інструментів після завершення потоку. Це працює як для бродкастингу через чергу (`broadcastOnQueue`), так і для синхронного (`broadcast` / `broadcastNow`).

<a name="queueing"></a>
### Черги

За допомогою методу `queue` агента ви можете надіслати йому промпт, але дозволити обробити відповідь у фоні, завдяки чому ваш застосунок залишатиметься швидким і чуйним. Методи `then` і `catch` можна використати, щоб зареєструвати замикання, які буде викликано, коли відповідь стане доступною або якщо станеться виняток:

```php
use Illuminate\Http\Request;
use Laravel\Ai\Responses\AgentResponse;
use Throwable;

Route::post('/coach', function (Request $request) {
    (new SalesCoach)
        ->queue($request->input('transcript'))
        ->then(function (AgentResponse $response) {
            // ...
        })
        ->catch(function (Throwable $e) {
            // ...
        });

    return back();
});
```

<a name="tools"></a>
### Інструменти

Інструменти можна використати, щоб дати агентам додаткову функціональність, якою вони можуть скористатися, відповідаючи на промпти. Створити інструменти можна артизан-командою `make:tool`:

```shell
php artisan make:tool RandomNumberGenerator
```

Згенерований інструмент буде розміщено в каталозі `app/Ai/Tools` вашого застосунку. Кожен інструмент містить метод `handle`, який агент викличе, коли йому знадобиться скористатися інструментом:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class RandomNumberGenerator implements Tool
{
    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'min' => $schema->integer()->min(0)->required(),
            'max' => $schema->integer()->required(),
        ];
    }
}
```

Щойно ви визначили свій інструмент, ви можете повернути його з методу `tools` будь-якого зі своїх агентів:

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        new RandomNumberGenerator,
    ];
}
```

<a name="similarity-search"></a>
#### Пошук за схожістю

Інструмент `SimilaritySearch` дозволяє агентам шукати документи, схожі на заданий запит, використовуючи векторні ембединги, збережені у вашій базі даних. Це корисно для retrieval-augmented generation (RAG), коли ви хочете дати агентам доступ до пошуку в даних вашого застосунку.

Найпростіший спосіб створити інструмент пошуку за схожістю - метод `usingModel` з Eloquent-моделлю, яка має векторні ембединги:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        SimilaritySearch::usingModel(Document::class, 'embedding'),
    ];
}
```

Перший аргумент - клас Eloquent-моделі, а другий - колонка, що містить векторні ембединги.

Ви також можете передати мінімальний поріг схожості між `0.0` і `1.0` та замикання для налаштування запиту:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

Для більшого контролю ви можете створити інструмент пошуку за схожістю з власним замиканням, яке повертає результати пошуку:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        new SimilaritySearch(using: function (string $query) {
            return Document::query()
                ->where('user_id', $this->user->id)
                ->whereVectorSimilarTo('embedding', $query)
                ->limit(10)
                ->get();
        }),
    ];
}
```

Ви можете змінити опис інструмента методом `withDescription`:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="file-storage-tools"></a>
### Інструменти файлового сховища

Фабрика інструментів `FileStorage` дозволяє дати агентам доступ до [диска файлової системи](/docs/{{version}}/filesystem) Laravel. Метод `all` повертає інструменти, які дозволяють агенту перелічувати, читати, оглядати, генерувати URL, записувати, видаляти й копіювати файли на заданому диску:

```php
use Laravel\Ai\Tools\FileStorage;

public function tools(): iterable
{
    return FileStorage::all('local');
}
```

Якщо ваш агент має мати змогу лише оглядати файли, скористайтеся методом `readOnly`:

```php
return FileStorage::readOnly('local');
```

Ці методи повертають `Illuminate\Support\Collection`, що дозволяє додатково відфільтрувати інструменти, які надаються агенту:

```php
use Laravel\Ai\Tools\Filesystem\DeleteFile;

return FileStorage::all('s3')
    ->reject(fn ($tool) => $tool instanceof DeleteFile);
```

<a name="mcp-tools"></a>
### MCP-інструменти

Якщо ваш застосунок використовує [Laravel MCP](/docs/{{version}}/mcp), ви можете дати своїм агентам інструменти, які надають сервери [Model Context Protocol](https://modelcontextprotocol.io). За допомогою [клієнта Laravel MCP](/docs/{{version}}/mcp#client) ви можете підключитися до віддаленого чи локального MCP-сервера й передати його інструменти безпосередньо своєму агенту.

> [!NOTE]
> MCP-інструменти потребують, щоб у вашому застосунку було встановлено пакет [Laravel MCP](/docs/{{version}}/mcp).

Оскільки метод `tools` MCP-клієнта повертає колекцію, розгорніть її в масив `tools` вашого агента оператором `...`:

```php
use App\Ai\Tools\RandomNumberGenerator;
use Laravel\Mcp\Client;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        ...Client::web('https://mcp.example.com')
            ->withToken($token)
            ->tools(),

        new RandomNumberGenerator,
    ];
}
```

AI SDK автоматично загортає кожен MCP-інструмент, щоб агент міг викликати його як будь-який інший. Ви також можете скористатися [іменованим MCP-клієнтом](/docs/{{version}}/mcp#named-clients):

```php
use Laravel\Mcp\Facades\Mcp;

public function tools(): iterable
{
    return [
        ...Mcp::client('github')->tools(),
    ];
}
```

Або підключитися до [локального MCP-сервера](/docs/{{version}}/mcp#client-connecting):

```php
use Laravel\Mcp\Client;

public function tools(): iterable
{
    return [
        ...Client::local('php', ['artisan', 'mcp:start'])->tools(),
    ];
}
```

Докладніше про створення й автентифікацію MCP-клієнтів, включно з bearer-токенами й OAuth, дивіться в [документації MCP-клієнта](/docs/{{version}}/mcp#client).

<a name="provider-tools"></a>
### Інструменти провайдера

Інструменти провайдера - це особливі інструменти, реалізовані нативно самими AI-провайдерами, які пропонують можливості на кшталт вебпошуку, завантаження URL і пошуку файлів. На відміну від звичайних інструментів, інструменти провайдера виконує сам провайдер, а не ваш застосунок.

Інструменти провайдера можна повертати з методу `tools` вашого агента.

<a name="web-search"></a>
#### Вебпошук

Інструмент провайдера `WebSearch` дозволяє агентам шукати в мережі інформацію в реальному часі. Це корисно для відповідей на питання про поточні події, свіжі дані чи теми, які могли змінитися після дати відсічення тренувальних даних моделі.

**Підтримувані провайдери:** Anthropic, OpenAI, Gemini, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```

Ви можете налаштувати інструмент вебпошуку, щоб обмежити кількість пошуків чи звузити результати до конкретних доменів:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

Щоб уточнити результати пошуку за місцем розташування користувача, скористайтеся методом `location`:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### Завантаження вебсторінок

Інструмент провайдера `WebFetch` дозволяє агентам завантажувати й читати вміст вебсторінок. Це корисно, коли вам потрібно, щоб агент проаналізував конкретні URL чи отримав докладну інформацію з відомих вебсторінок.

**Підтримувані провайдери:** Anthropic, Gemini

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```

Ви можете налаштувати інструмент завантаження вебсторінок, щоб обмежити кількість завантажень чи звузити його до конкретних доменів:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### Пошук файлів

Інструмент провайдера `FileSearch` дозволяє агентам шукати серед [файлів](#files), збережених у [векторних сховищах](#vector-stores). Це уможливлює retrieval-augmented generation (RAG), дозволяючи агенту шукати релевантну інформацію у ваших завантажених документах.

**Підтримувані провайдери:** OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```

Ви можете передати кілька ID векторних сховищ, щоб шукати в кількох сховищах:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

Якщо ваші файли мають [метадані](#adding-files-to-stores), ви можете відфільтрувати результати пошуку, передавши аргумент `where`. Для простих фільтрів на рівність передайте масив:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

Для складніших фільтрів ви можете передати замикання, яке отримує екземпляр `FileSearchQuery`:

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```

<a name="sub-agents"></a>
### Субагенти

Агентів також можна повертати з методу `tools` іншого агента. Коли агента повернуто як інструмент, батьківський агент може делегувати субагенту конкретне завдання й використати його відповідь, відповідаючи на початковий промпт. Це корисно, коли агенту загального призначення потрібен доступ до спеціалізованих агентів з власними інструкціями, інструментами, конфігурацією моделі чи вподобаннями щодо провайдера.

Наприклад, агент підтримки клієнтів міг би делегувати питання про право на повернення коштів окремому агенту з повернень:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

class CustomerSupportAgent implements Agent, HasTools
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You help customers with account, order, and billing questions. Delegate refund policy questions to the refunds specialist.';
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RefundsAgent,
        ];
    }
}
```

Щоб налаштувати, як субагент подається батьківському агенту, реалізуйте на субагенті інтерфейс `CanActAsTool` і визначте ім'я та опис для інструмента:

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\LookupOrder;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\CanActAsTool;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
class RefundsAgent implements Agent, CanActAsTool, HasTools
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a refunds specialist. Use order details and the refund policy to give concise eligibility guidance.';
    }

    /**
     * Get the agent's tool name.
     */
    public function name(): string
    {
        return 'refunds_specialist';
    }

    /**
     * Get the agent's tool description.
     */
    public function description(): string
    {
        return 'Determine whether an order is eligible for a refund and explain the next step.';
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new LookupOrder,
        ];
    }
}
```

Якщо субагент не реалізує `CanActAsTool`, Laravel використає базове ім'я класу агента як ім'я інструмента й загальний опис, який просить батьківського агента передати чіткий, самодостатній опис завдання. Кожен виклик субагента виконується ізольовано й не отримує історії розмови батьківського агента.

<a name="middleware"></a>
### Middleware

Агенти підтримують `middleware`, що дозволяє перехоплювати й змінювати промпти, перш ніж їх буде надіслано провайдеру. Створити `middleware` можна артизан-командою `make:agent-middleware`:

```shell
php artisan make:agent-middleware LogPrompts
```

Згенерований `middleware` буде розміщено в каталозі `app/Ai/Middleware` вашого застосунку. Щоб додати `middleware` до агента, реалізуйте інтерфейс `HasMiddleware` і визначте метод `middleware`, який повертає масив класів `middleware`:

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Middleware\LogPrompts;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasMiddleware;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasMiddleware
{
    use Promptable;

    // ...

    /**
     * Get the agent's middleware.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

Кожен клас `middleware` має визначати метод `handle`, який отримує `AgentPrompt` і `Closure` для передавання промпта наступному `middleware`:

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Laravel\Ai\Prompts\AgentPrompt;

class LogPrompts
{
    /**
     * Handle the incoming prompt.
     */
    public function handle(AgentPrompt $prompt, Closure $next)
    {
        Log::info('Prompting agent', ['prompt' => $prompt->prompt]);

        return $next($prompt);
    }
}
```

Ви можете скористатися методом `then` на відповіді, щоб виконати код після того, як агент завершить обробку. Це працює як для синхронних, так і для потокових відповідей:

```php
public function handle(AgentPrompt $prompt, Closure $next)
{
    return $next($prompt)->then(function (AgentResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```

<a name="anonymous-agents"></a>
### Анонімні агенти

Іноді вам може знадобитися швидко звернутися до моделі, не створюючи окремого класу агента. Ви можете створити спонтанного, анонімного агента функцією `agent`:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel')
```

Анонімні агенти також можуть давати структурований вивід:

```php
use Illuminate\Contracts\JsonSchema\JsonSchema;

use function Laravel\Ai\{agent};

$response = agent(
    schema: fn (JsonSchema $schema) => [
        'number' => $schema->integer()->required(),
    ],
)->prompt('Generate a random number less than 100')
```

<a name="agent-configuration"></a>
### Конфігурація агента

Ви можете налаштувати опції генерації тексту для агента за допомогою PHP-атрибутів. Доступні такі атрибути:

- `MaxSteps`: максимальна кількість кроків, які агент може зробити, користуючись інструментами.
- `MaxTokens`: максимальна кількість токенів, які модель може згенерувати.
- `Model`: модель, яку має використовувати агент.
- `Provider`: AI-провайдер (чи провайдери для резервування), який слід використовувати для агента.
- `Temperature`: температура семплювання для генерації (від 0.0 до 1.0).
- `Timeout`: HTTP-тайм-аут у секундах для запитів агента (за замовчуванням: 60).
- `TopP`: імовірність nucleus-семплювання для генерації (від 0.0 до 1.0).
- `UseCheapestModel`: використовувати найдешевшу текстову модель провайдера для оптимізації витрат.
- `UseSmartestModel`: використовувати найпотужнішу текстову модель провайдера для складних завдань.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Model;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Attributes\TopP;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
#[Model('claude-sonnet-5')]
#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Temperature(0.7)]
#[Timeout(120)]
#[TopP(0.9)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

Атрибути `UseCheapestModel` і `UseSmartestModel` дозволяють автоматично обрати найвигіднішу за ціною чи найпотужнішу модель для заданого провайдера, не вказуючи імені моделі. Це корисно, коли ви хочете оптимізувати витрати чи можливості для різних провайдерів:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // Will use the cheapest model (e.g., Haiku)...
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // Will use the most capable model (e.g., Opus)...
}
```

> [!NOTE]
> Модель, яку обирають `UseCheapestModel` і `UseSmartestModel`, може змінюватися між випусками Laravel AI SDK, оскільки провайдери випускають нові моделі. Зміна моделі може призвести до змін у поведінці, застарілих параметрів і суттєвої різниці у вартості. Якщо вам потрібна стабільна, передбачувана модель і ціна, вкажіть модель явно атрибутом `Model`.

<a name="provider-options"></a>
### Опції провайдера

Якщо вашому агенту потрібно передати специфічні для провайдера опції (як-от reasoning effort в OpenAI чи налаштування штрафів), реалізуйте контракт `HasProviderOptions` і визначте метод `providerOptions`:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasProviderOptions;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasProviderOptions
{
    use Promptable;

    // ...

    /**
     * Get provider-specific generation options.
     */
    public function providerOptions(Lab|string $provider): array
    {
        return match ($provider) {
            Lab::OpenAI => [
                'reasoning' => ['effort' => 'low'],
                'frequency_penalty' => 0.5,
                'presence_penalty' => 0.3,
            ],
            Lab::Anthropic => [
                'thinking' => ['budget_tokens' => 1024],
                'cache_control' => ['type' => 'ephemeral'],
            ],
            default => [],
        };
    }
}
```

Метод `providerOptions` отримує провайдера, який використовується зараз (enum `Lab` чи рядок), що дозволяє повертати різні опції для різних провайдерів. Це особливо корисно під час використання [резервування](#failover), оскільки кожен резервний провайдер може отримати власну конфігурацію.

Наведений вище приклад з Anthropic також вмикає [кешування промптів](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) через `cache_control`.

<a name="human-tool-approval"></a>
## Схвалення інструментів людиною

> [!WARNING]
> Схвалення інструментів потребує агента `Conversational`, історія розмови якого зберігається, щоб призупинений виклик можна було відновити. Трейт `RemembersConversations` забезпечує потрібне збереження.

Інструменти, що виконують чутливі чи незворотні дії, можуть потребувати схвалення людиною перед виконанням. Щоб зробити інструмент таким, що потребує схвалення, реалізуйте контракт `Approvable` і використайте трейт `InteractsWithApprovals`. Такі інструменти за замовчуванням потребують схвалення:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Illuminate\Support\Facades\Storage;
use Laravel\Ai\Concerns\InteractsWithApprovals;
use Laravel\Ai\Contracts\Approvable;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class DeleteFile implements Approvable, Tool
{
    use InteractsWithApprovals;

    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'Delete a file from storage.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        Storage::delete($request['path']);

        return "Deleted [{$request['path']}].";
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'path' => $schema->string()->required(),
        ];
    }
}
```

Щоб визначити, чи потрібне схвалення, на основі аргументів виклику інструмента, визначте на інструменті метод `needsApproval`. Цей метод може повернути булеве значення чи екземпляр `Approval`, який містить причину запиту на схвалення:

```php
use Laravel\Ai\Approvals\Approval;

/**
 * Determine whether the tool needs approval for the given request.
 */
protected function needsApproval(Request $request): Approval|bool
{
    return str_starts_with($request['path'], 'temporary/')
        ? false
        : Approval::required('This will permanently delete a file.');
}
```

Ви можете перевизначити вимогу схвалення для інструмента, повертаючи його з методу `tools` агента:

```php
public function tools(): iterable
{
    return [
        (new SendNotification)->withoutApproval(),
        (new DeleteFile)->requireApproval('Deletion review required.'),
    ];
}
```

Коли викликано інструмент, що потребує схвалення, агент призупиняється перед його виконанням. Ви можете оглянути очікувані схвалення у відповіді - вони містять ID кожного виклику інструмента, ім'я інструмента, аргументи й причину схвалення:

```php
$response = (new FileAssistant)
    ->forUser($user)
    ->prompt('Delete the old invoice.');

if ($response->hasPendingApprovals()) {
    foreach ($response->pendingApprovals as $approval) {
        // $approval->id
        // $approval->tool
        // $approval->arguments
        // $approval->reason
    }
}
```

Щоб відновити роботу агента, продовжте розмову й передайте екземпляр `Decisions`, що містить рішення для кожного очікуваного виклику інструмента. Рішення можуть схвалити виклик, відхилити його чи змінити його аргументи перед виконанням:

```php
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt(Decisions::from([
        'call_abc' => Decision::approve(),
        'call_ghi' => Decision::reject('The invoice must be retained.'),
    ]));
```

Булеві значення `true` і `false` можна використовувати як скорочення для схвалення й відхилення. Кожен очікуваний виклик інструмента має отримати рішення. Невідомі, відсутні чи вже розв'язані ID викликів інструментів спричинять виняток `ApprovalMismatchException`. Ви можете задати значення за замовчуванням для викликів без явного рішення методами `approveRemaining` чи `rejectRemaining`:

```php
$decisions = Decisions::from([
    'call_abc' => true,
])->rejectRemaining('Not approved.');

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt($decisions);
```

Відхилення з результатом, як-от `Decision::reject('Not approved.')`, повертається моделі, щоб вона могла продовжити відповідь. Відхилення без результату зупиняє цикл генерації після запису відхилення.

Схвалення інструментів підтримують методи `prompt`, `stream`, `queue`, `broadcast`, `broadcastNow` і `broadcastOnQueue`.

Під час стримінгу й бродкастингу призупинення представлене подією `tool_approval_request`. Використовуючи [протокол стримінгу Vercel AI SDK](#streaming-using-the-vercel-ai-sdk-protocol), запити на схвалення й результати випромінюються через нативні частини схвалення інструментів цього протоколу.

Для агентів у черзі отримана відповідь передається до колбека `then`, а Laravel також диспетчеризує подію `ToolApprovalRequested`.

Laravel зберігає результат схваленого інструмента, перш ніж попросити модель продовжити. Якщо генерація потім зазнає невдачі, схвалення вже розв'язане. Продовжте розмову звичайним текстовим промптом, а не надсилайте ті самі рішення про схвалення ще раз.

<a name="complete-approval-flow"></a>
### Повний потік схвалення

Наведені нижче маршрути демонструють повний потік схвалення. Маршрут `GET` повертає екран чату, а маршрут `POST` приймає або новий текстовий промпт, або рішення про схвалення з екрана чату. Цей приклад припускає, що модель `User` застосунку використовує трейт `HasConversations`:

```php
use App\Ai\Agents\FileAssistant;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Route;
use Illuminate\Validation\Rule;
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Models\Conversation;

Route::get('/chat/{conversation}', function (Request $request, Conversation $conversation) {
    Gate::authorize('view', $conversation);

    return view('chat', [
        'conversation' => $conversation,
    ]);
})->middleware('auth');

Route::post('/chat/{conversation}', function (Request $request, Conversation $conversation) {
    Gate::authorize('view', $conversation);

    $validated = $request->validate([
        'message' => ['nullable', 'string', 'required_without:decisions', 'prohibited_with:decisions'],
        'decisions' => ['nullable', 'array', 'required_without:message', 'prohibited_with:message'],
        'decisions.*.action' => ['required_with:decisions', Rule::in(['approve', 'reject'])],
        'decisions.*.result' => ['nullable', 'string'],
    ]);

    $prompt = isset($validated['decisions'])
        ? Decisions::from($validated->collect('decisions')->map(
            fn (array $decision) => match ($decision['action']) {
                'approve' => Decision::approve(),
                'reject' => Decision::reject($decision['result'] ?? null),
            }
        )->all())
        : $validated['message'];

    $response = (new FileAssistant)
        ->continue($conversation->id, as: $request->user())
        ->prompt($prompt);

    return [
        'conversation_id' => $response->conversationId,
        'status' => $response->hasPendingApprovals() ? 'awaiting_approval' : 'complete',
        'message' => $response->text,
        'approvals' => $response->pendingApprovals,
    ];
})->middleware('auth');
```

Коли статус відповіді - `awaiting_approval`, екран чату має відрендерити очікувані схвалення й надіслати вибір користувача на той самий ендпоїнт, використовуючи ID виклику інструмента як ключ кожного рішення:

```json
{
    "decisions": {
        "call_abc": {
            "action": "approve"
        },
        "call_def": {
            "action": "reject",
            "result": "The invoice must be retained."
        }
    }
}
```

Для звичайного повідомлення чату екран може натомість надіслати значення `message`:

```json
{
    "message": "Delete the old invoice."
}
```

<a name="images"></a>
## Зображення

Клас `Laravel\Ai\Image` можна використати для генерації зображень через провайдерів `openai`, `gemini` чи `xai`:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

Методи `square`, `portrait` і `landscape` можна використати, щоб керувати співвідношенням сторін зображення, а метод `quality` - щоб підказати моделі бажану якість готового зображення (`high`, `medium`, `low`). Метод `timeout` можна використати, щоб задати HTTP-тайм-аут у секундах:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

Ви можете прикріпити референсні зображення методом `attachments`:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Image;

$image = Image::of('Update this photo of me to be in the style of an impressionist painting.')
    ->attachments([
        Files\Image::fromStorage('photo.jpg'),
        // Files\Image::fromPath('/home/laravel/photo.jpg'),
        // Files\Image::fromUrl('https://example.com/photo.jpg'),
        // $request->file('photo'),
    ])
    ->landscape()
    ->generate();
```

Згенеровані зображення легко зберегти на диску за замовчуванням, налаштованому в конфігураційному файлі `config/filesystems.php` вашого застосунку:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

Генерацію зображень також можна поставити в чергу:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Responses\ImageResponse;

Image::of('A donut sitting on the kitchen counter')
    ->portrait()
    ->queue()
    ->then(function (ImageResponse $image) {
        $path = $image->store();

        // ...
    });
```

<a name="audio"></a>
## Аудіо

Клас `Laravel\Ai\Audio` можна використати для генерації аудіо із заданого тексту:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

Ви також можете згенерувати аудіо з рядка методом `toAudio`, доступним через клас `Stringable` у Laravel:

```php
use Illuminate\Support\Str;

$audio = Str::of('I love coding with Laravel.')->toAudio();
```

Методи `male`, `female` і `voice` можна використати, щоб визначити голос згенерованого аудіо:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

Так само метод `instructions` можна використати, щоб динамічно підказати моделі, як має звучати згенероване аудіо:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

Згенероване аудіо легко зберегти на диску за замовчуванням, налаштованому в конфігураційному файлі `config/filesystems.php` вашого застосунку:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

Генерацію аудіо також можна поставити в чергу:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Responses\AudioResponse;

Audio::of('I love coding with Laravel.')
    ->queue()
    ->then(function (AudioResponse $audio) {
        $path = $audio->store();

        // ...
    });
```

<a name="transcription"></a>
## Транскрибування

Клас `Laravel\Ai\Transcription` можна використати, щоб згенерувати транскрипт заданого аудіо:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

Метод `diarize` можна використати, щоб указати, що ви хочете отримати у відповіді діаризований транскрипт на додачу до сирого текстового, - це дасть доступ до транскрипту, сегментованого за мовцями:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

Генерацію транскриптів також можна поставити в чергу:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Responses\TranscriptionResponse;

Transcription::fromStorage('audio.mp3')
    ->queue()
    ->then(function (TranscriptionResponse $transcript) {
        // ...
    });
```

<a name="text-summarization"></a>
## Стислий переказ тексту

Ви можете стисло переказати текст методом `summarize`, доступним через клас `Stringable` у Laravel. За замовчуванням переказ міститиме не більше трьох речень і буде згенерований найдешевшою текстовою моделлю налаштованого провайдера:

```php
use Illuminate\Support\Str;

$summary = Str::of($article)->summarize();
```

Ви можете вказати максимальну кількість речень, провайдера, модель і тайм-аут, які використовуються для генерації переказу. Клас `Str` також пропонує статичну версію методу:

```php
use Laravel\Ai\Enums\Lab;

$summary = Str::of($article)->summarize(
    sentences: 4,
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 30,
);

$summary = Str::summarize($article, sentences: 4);
```

<a name="embeddings"></a>
## Ембединги

Ви можете легко згенерувати векторні ембединги для будь-якого рядка новим методом `toEmbeddings`, доступним через клас `Stringable` у Laravel:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

Як альтернативу ви можете скористатися класом `Embeddings`, щоб згенерувати ембединги для кількох вхідних значень одразу:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

Ви можете вказати розмірність і провайдера для ембедингів:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

<a name="multimodal-embeddings"></a>
### Мультимодальні ембединги

Окрім рядків, метод `Embeddings::for` приймає зображення, аудіо, документи й відео, що дозволяє генерувати ембединги для нетекстового вмісту. Gemini підтримує ембединги зображень, аудіо, документів і відео, а VoyageAI - ембединги зображень і відео:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

$response = Embeddings::for([
    'A vineyard at sunset.',
    Image::fromStorage('vineyard.jpg'),
    Video::fromPath('/home/laravel/tour.mp4'),
])->generate(Lab::Gemini);
```

Мультимодальні вхідні дані використовують ті самі [класи файлів, що й вкладення](#attachments). Ці файли можна створити з локального шляху, диска файлової системи, віддаленого URL чи вмісту в кодуванні Base64. Зображення, документи й відео також можна створити із завантажених файлів, а документи - із сирого рядкового вмісту:

```php
use Laravel\Ai\Files\Audio;
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

Image::fromPath('/home/laravel/photo.jpg');
Image::fromStorage('photo.jpg');
Image::fromUpload($request->file('photo'));

Audio::fromPath('/home/laravel/clip.mp3');
Audio::fromStorage('clip.mp3');
Audio::fromUpload($request->file('clip.mp3'));

Video::fromPath('/home/laravel/video.mp4');
Video::fromStorage('video.mp4');
Video::fromUpload($request->file('video'));

Document::fromUrl('https://example.com/report.pdf');
Document::fromString('Laravel is a PHP framework.', 'text/plain');
Document::fromUpload($request->file('report'));
```

> [!NOTE]
> VoyageAI не дозволяє змішувати медіа за віддаленим URL і медіа в кодуванні Base64 в одному запиті. Локальні, збережені й завантажені файли надсилаються як вміст у кодуванні Base64, а текстові вхідні дані можна поєднувати з будь-яким із цих джерел медіа. Зверніться до документації свого провайдера, щоб дізнатися, які мультимодальні моделі й вхідні дані доступні.

<a name="querying-embeddings"></a>
### Запити до ембедингів

Щойно ви згенерували ембединги, ви зазвичай зберігатимете їх у колонці `vector` своєї бази даних для подальших запитів. Laravel нативно підтримує векторні колонки в PostgreSQL через розширення `pgvector`. Для початку визначте колонку `vector` у своїй міграції, указавши кількість вимірів:

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536);
    $table->timestamps();
});
```

Ви також можете додати векторний індекс, щоб пришвидшити пошук за схожістю. Викликаючи `index` на векторній колонці, Laravel автоматично створить HNSW-індекс з косинусною відстанню:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

У своїй Eloquent-моделі вам слід привести векторну колонку до `array`:

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

Щоб шукати схожі записи, скористайтеся методом `whereVectorSimilarTo`. Цей метод фільтрує результати за мінімальною косинусною схожістю (між `0.0` і `1.0`, де `1.0` - ідентичність) і впорядковує результати за схожістю:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding` може бути масивом чисел з рухомою комою або звичайним рядком. Коли передано рядок, Laravel автоматично згенерує для нього ембединги:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

Якщо вам потрібно більше контролю, ви можете окремо скористатися нижчорівневими методами `whereVectorDistanceLessThan`, `selectVectorDistance` та `orderByVectorDistance`:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

Якщо ви хочете дати агенту можливість виконувати пошук за схожістю як інструмент, погляньте на документацію інструмента [Пошук за схожістю](#similarity-search).

> [!NOTE]
> Векторні запити наразі підтримуються лише на підключеннях PostgreSQL з розширенням `pgvector`.

<a name="caching-embeddings"></a>
### Кешування ембедингів

Генерацію ембедингів можна кешувати, щоб уникнути зайвих API-викликів для однакових вхідних даних. Щоб увімкнути кешування, встановіть параметр конфігурації `ai.caching.embeddings.cache` у `true`:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

Коли кешування увімкнено, ембединги кешуються на 30 днів. Ключ кешу базується на провайдері, моделі, розмірності та вхідному вмісті, що гарантує повернення закешованих результатів для однакових запитів і генерацію свіжих ембедингів для інших конфігурацій.

Ви також можете увімкнути кешування для конкретного запиту методом `cache`, навіть коли глобальне кешування вимкнено:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

Ви можете вказати власну тривалість кешування в секундах:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // Cache for 1 hour
    ->generate();
```

Метод `toEmbeddings` у Stringable також приймає аргумент `cache`:

```php
// Cache with default duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// Cache for a specific duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## Переранжування

Переранжування дозволяє переупорядкувати список документів за їхньою релевантністю до заданого запиту. Це корисно для покращення результатів пошуку завдяки семантичному розумінню:

Клас `Laravel\Ai\Reranking` можна використати для переранжування документів:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// Access the top result...
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (original position)
```

Метод `limit` можна використати, щоб обмежити кількість повернутих результатів:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### Переранжування колекцій

Для зручності колекції Laravel можна переранжувати макросом `rerank`. Перший аргумент указує, яке поле (чи поля) використовувати для переранжування, а другий - запит:

```php
// Rerank by a single field...
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// Rerank by multiple fields (sent as JSON)...
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// Rerank using a closure to build the document...
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

Ви також можете обмежити кількість результатів і вказати провайдера:

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: Lab::Cohere
);
```

<a name="files"></a>
## Файли

Клас `Laravel\Ai\Files` чи окремі класи файлів можна використати, щоб зберігати файли у вашого AI-провайдера для подальшого використання в розмовах. Це корисно для великих документів чи файлів, на які ви хочете посилатися багато разів, не завантажуючи їх щоразу заново:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// Store a file from a local path...
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// Store a file that is stored on a filesystem disk...
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// Store a file that is stored on a remote URL...
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

Ви також можете зберігати сирий вміст чи завантажені файли:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Store raw content...
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// Store an uploaded file...
$stored = Document::fromUpload($request->file('document'))->put();
```

Щойно файл збережено, ви можете посилатися на нього під час генерації тексту через агентів, замість завантажувати його заново:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...'
    attachments: [
        Files\Document::fromId('file-id') // Attach a stored document...
    ]
);
```

Щоб отримати раніше збережений файл, скористайтеся методом `get` на екземплярі файлу:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

Щоб видалити файл у провайдера, скористайтеся методом `delete`:

```php
Document::fromId('file-id')->delete();
```

За замовчуванням клас `Files` використовує AI-провайдера за замовчуванням, налаштованого в конфігураційному файлі `config/ai.php` вашого застосунку. Для більшості операцій ви можете вказати іншого провайдера аргументом `provider`:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```

Ви можете передати специфічні для провайдера опції завантаження методом `withProviderOptions`. Наприклад, ви можете задати `purpose` файлу в OpenAI:

```php
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/knowledge.txt')
    ->withProviderOptions(['purpose' => 'assistants'])
    ->put();
```

Щоб обмежити опції окремим провайдером, передайте замикання, яке отримує поточного провайдера:

```php
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/training.jsonl')
    ->withProviderOptions(fn (Lab|string $provider) => match ($provider) {
        Lab::OpenAI => ['purpose' => 'fine-tune'],
        default => [],
    })
    ->put();
```

<a name="using-stored-files-in-conversations"></a>
### Використання збережених файлів у розмовах

Щойно файл збережено у провайдера, ви можете посилатися на нього в розмовах агента методом `fromId` на класах `Document` чи `Image`:

```php
use App\Ai\Agents\DocumentAnalyzer;
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

$stored = Document::fromPath('/path/to/report.pdf')->put();

$response = (new DocumentAnalyzer)->prompt(
    'Summarize this document.',
    attachments: [
        Document::fromId($stored->id),
    ],
);
```

Так само на збережені зображення можна посилатися через клас `Image`:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Image;

$stored = Image::fromPath('/path/to/photo.jpg')->put();

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Image::fromId($stored->id),
    ],
);
```

<a name="vector-stores"></a>
## Векторні сховища

Векторні сховища дозволяють створювати придатні для пошуку колекції файлів, які можна використовувати для retrieval-augmented generation (RAG). Клас `Laravel\Ai\Stores` надає методи для створення, отримання й видалення векторних сховищ:

```php
use Laravel\Ai\Stores;

// Create a new vector store...
$store = Stores::create('Knowledge Base');

// Create a store with additional options...
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

Щоб отримати наявне векторне сховище за його ID, скористайтеся методом `get`:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

Щоб видалити векторне сховище, скористайтеся методом `delete` на класі `Stores` чи на екземплярі сховища:

```php
use Laravel\Ai\Stores;

// Delete by ID...
Stores::delete('store_id');

// Or delete via a store instance...
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
### Додавання файлів до сховищ

Щойно у вас є векторне сховище, ви можете додавати до нього [файли](#files) методом `add`. Файли, додані до сховища, автоматично індексуються для семантичного пошуку через [інструмент провайдера для пошуку файлів](#file-search):

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// Add a file that has already been stored with the provider...
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// Or, store and add a file in one step...
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> **Note:** Зазвичай, коли ви додаєте до векторних сховищ раніше збережені файли, повернутий ID документа збігатиметься з раніше призначеним ID файлу; однак деякі провайдери векторних сховищ можуть повернути новий, інший «ID документа». Тому рекомендується завжди зберігати обидва ID у своїй базі даних для подальшого використання.

Ви можете прикріпити до файлів метадані, додаючи їх до сховища. Ці метадані згодом можна використати для фільтрації результатів пошуку через [інструмент провайдера для пошуку файлів](#file-search):

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

Щоб прибрати файл зі сховища, скористайтеся методом `remove`:

```php
$store->remove('file_id');
```

Прибирання файлу з векторного сховища не видаляє його з [файлового сховища](#files) провайдера. Щоб прибрати файл з векторного сховища й остаточно видалити його з файлового сховища, скористайтеся аргументом `deleteFile`:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## Резервні провайдери

Промптуючи чи генеруючи інші медіа, ви можете передати масив провайдерів / моделей, щоб автоматично перемкнутися на резервного провайдера / модель, якщо на основному станеться збій сервісу чи спрацює обмеження частоти:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [Lab::OpenAI, Lab::Anthropic],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```

Перемикання на резерв відбувається лише тоді, коли видано `FailoverableException` - як-от обмеження частоти (`RateLimitedException`), перевантажений чи недоступний провайдер (`ProviderOverloadedException`) або нестача кредитів (`InsufficientCreditsException`). Звичайні помилки, як-от помилка валідації чи хибний запит, перемикання на резерв не спричинять.

Коли ви передаєте простий список провайдерів, як-от `[Lab::OpenAI, Lab::Anthropic]`, кожен провайдер використовує свою модель за замовчуванням. Щоб указати конкретну модель для кожного провайдера в ланцюжку резервування, передайте асоціативний масив з ключами за провайдерами, використовуючи `value` з enum `Lab` як ключ (випадки enum не можна використовувати напряму як ключі масивів PHP):

```php
use Laravel\Ai\Enums\Lab;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [
        Lab::Gemini->value => 'gemini-3-flash-preview',
        Lab::DeepSeek->value => 'deepseek-v4-pro',
    ],
);
```

<a name="testing"></a>
## Тестування

<a name="testing-agents"></a>
### Агенти

Щоб підробити відповіді агента під час тестів, викличте метод `fake` на класі агента. За бажанням ви можете передати масив відповідей чи замикання:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// Automatically generate a fixed response for every prompt...
SalesCoach::fake();

// Provide a list of prompt responses...
SalesCoach::fake([
    'First response',
    'Second response',
]);

// Dynamically handle prompt responses based on the incoming prompt...
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

Підробляючи агента, який повертає структурований вивід, ви можете передавати масиви як відповіді. Агент поверне структуровану відповідь із заданими даними:

```php
SalesCoach::fake([
    ['score' => 87],
]);
```

Ви також можете підробити відповідь, яка очікує на схвалення інструмента:

```php
use Laravel\Ai\Approvals\PendingApproval;
use Laravel\Ai\Responses\AgentResponse;

FileAssistant::fake([
    AgentResponse::fakeWithPendingApprovals([
        new PendingApproval(
            id: 'call_abc',
            tool: 'DeleteFile',
            arguments: ['path' => 'invoice.pdf'],
            reason: 'This will permanently delete a file.',
        ),
    ]),
]);

$response = (new FileAssistant)->prompt('Delete the invoice.');

$response->hasPendingApprovals(); // true
```

> **Note:** Коли `Agent::fake()` викликано на агенті, який повертає структурований вивід, а підроблений вивід не було задано явно, Laravel автоматично згенерує підроблені дані, що відповідають визначеній схемі виводу вашого агента.

Після промптингу агента ви можете робити твердження щодо отриманих промптів:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

Стверджуючи щодо продовження після схвалення, ви можете оглянути рішення про схвалення в промпті:

```php
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Prompts\AgentPrompt;

FileAssistant::fake();

(new FileAssistant)->prompt(Decisions::from([
    'call_abc' => true,
]));

FileAssistant::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->hasApprovalDecisions()
        && $prompt->approvalDecisions->get('call_abc')->isApproved();
});
```

Для викликів агентів через чергу скористайтеся методами тверджень для черги:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

Щоб пересвідчитися, що всі виклики агента мають відповідну підроблену відповідь, скористайтеся `preventStrayPrompts`. Якщо агента буде викликано без визначеної підробленої відповіді, буде видано виняток:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### Зображення

Генерацію зображень можна підробити, викликавши метод `fake` на класі `Image`. Щойно зображення підроблено, можна виконувати різні твердження щодо записаних промптів генерації зображень:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// Automatically generate a fixed response for every prompt...
Image::fake();

// Provide a list of prompt responses...
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

Після генерації зображень ви можете робити твердження щодо отриманих промптів:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

Для генерації зображень через чергу скористайтеся методами тверджень для черги:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

Щоб пересвідчитися, що всі генерації зображень мають відповідну підроблену відповідь, скористайтеся `preventStrayImages`. Якщо зображення буде згенеровано без визначеної підробленої відповіді, буде видано виняток:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### Аудіо

Генерацію аудіо можна підробити, викликавши метод `fake` на класі `Audio`. Щойно аудіо підроблено, можна виконувати різні твердження щодо записаних промптів генерації аудіо:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// Automatically generate a fixed response for every prompt...
Audio::fake();

// Provide a list of prompt responses...
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

Після генерації аудіо ви можете робити твердження щодо отриманих промптів:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

Для генерації аудіо через чергу скористайтеся методами тверджень для черги:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

Щоб пересвідчитися, що всі генерації аудіо мають відповідну підроблену відповідь, скористайтеся `preventStrayAudio`. Якщо аудіо буде згенеровано без визначеної підробленої відповіді, буде видано виняток:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### Транскрибування

Генерацію транскриптів можна підробити, викликавши метод `fake` на класі `Transcription`. Щойно транскрибування підроблено, можна виконувати різні твердження щодо записаних промптів генерації транскриптів:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// Automatically generate a fixed response for every prompt...
Transcription::fake();

// Provide a list of prompt responses...
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// Dynamically handle prompt responses based on the incoming prompt...
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

Після генерації транскриптів ви можете робити твердження щодо отриманих промптів:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

Для генерації транскриптів через чергу скористайтеся методами тверджень для черги:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

Щоб пересвідчитися, що всі генерації транскриптів мають відповідну підроблену відповідь, скористайтеся `preventStrayTranscriptions`. Якщо транскрипт буде згенеровано без визначеної підробленої відповіді, буде видано виняток:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### Ембединги

Генерацію ембедингів можна підробити, викликавши метод `fake` на класі `Embeddings`. Щойно ембединги підроблено, можна виконувати різні твердження щодо записаних промптів генерації ембедингів:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// Automatically generate fake embeddings of the proper dimensions for every prompt...
Embeddings::fake();

// Provide a list of prompt responses...
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// Dynamically handle prompt responses based on the incoming prompt...
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

Після генерації ембедингів ви можете робити твердження щодо отриманих промптів:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

Для генерації ембедингів через чергу скористайтеся методами тверджень для черги:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

Щоб пересвідчитися, що всі генерації ембедингів мають відповідну підроблену відповідь, скористайтеся `preventStrayEmbeddings`. Якщо ембединги буде згенеровано без визначеної підробленої відповіді, буде видано виняток:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### Переранжування

Операції переранжування можна підробити, викликавши метод `fake` на класі `Reranking`:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// Automatically generate a fake reranked responses...
Reranking::fake();

// Provide custom responses...
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

Після переранжування ви можете робити твердження щодо виконаних операцій:

```php
Reranking::assertReranked(function (RerankingPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->limit === 5;
});

Reranking::assertNotReranked(
    fn (RerankingPrompt $prompt) => $prompt->contains('Django')
);

Reranking::assertNothingReranked();
```

<a name="testing-files"></a>
### Файли

Файлові операції можна підробити, викликавши метод `fake` на класі `Files`:

```php
use Laravel\Ai\Files;

Files::fake();
```

Щойно файлові операції підроблено, ви можете робити твердження щодо завантажень і видалень, які сталися:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// Store files...
Document::fromString('Hello, Laravel!', mimeType: 'text/plain')
    ->as('hello.txt')
    ->put();

// Make assertions...
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain';
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

Щоб стверджувати щодо видалення файлів, ви можете передати ID файлу:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### Векторні сховища

Операції з векторними сховищами можна підробити, викликавши метод `fake` на класі `Stores`. Підробка сховищ також автоматично підробить [файлові операції](#files):

```php
use Laravel\Ai\Stores;

Stores::fake();
```

Щойно операції зі сховищами підроблено, ви можете робити твердження щодо створених чи видалених сховищ:

```php
use Laravel\Ai\Stores;

// Create store...
$store = Stores::create('Knowledge Base');

// Make assertions...
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

Щоб стверджувати щодо видалення сховищ, ви можете передати ID сховища:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

Щоб ствердити, що файли було додано до сховища чи прибрано з нього, скористайтеся методами тверджень на відповідному екземплярі `Store`:

```php
Stores::fake();

$store = Stores::get('store_id');

// Add / remove files...
$store->add('added_id');
$store->remove('removed_id');

// Make assertions...
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

Якщо файл зберігається у [файловому сховищі](#files) провайдера й додається до векторного сховища в межах одного запиту, ви можете не знати ID файлу у провайдера. У цьому разі ви можете передати до методу `assertAdded` замикання, щоб стверджувати щодо вмісту доданого файлу:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## Події

Laravel AI SDK диспетчеризує різноманітні [події](/docs/{{version}}/events), зокрема:

- `AddingFileToStore`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
- `CreatingStore`
- `EmbeddingsGenerated`
- `FileAddedToStore`
- `FileDeleted`
- `FileRemovedFromStore`
- `FileStored`
- `GeneratingAudio`
- `GeneratingEmbeddings`
- `GeneratingImage`
- `GeneratingTranscription`
- `ImageGenerated`
- `InvokingTool`
- `PromptingAgent`
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StoreCreated`
- `StoringFile`
- `StreamingAgent`
- `ToolApprovalRequested`
- `ToolApprovalResolved`
- `ToolInvoked`
- `TranscriptionGenerated`

Ви можете слухати будь-яку з цих подій, щоб логувати чи зберігати інформацію про використання AI SDK.

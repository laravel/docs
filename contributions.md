---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Посібник з внеску

- [Повідомлення про помилки](#bug-reports)
- [Питання щодо підтримки](#support-questions)
- [Обговорення розробки ядра](#core-development-discussion)
- [Яку гілку обрати?](#which-branch)
- [Скомпільовані ресурси](#compiled-assets)
- [Внески, згенеровані AI](#ai-generated-contributions)
- [Вразливості безпеки](#security-vulnerabilities)
- [Стиль коду](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [Кодекс поведінки](#code-of-conduct)

<a name="bug-reports"></a>
## Повідомлення про помилки

Щоб заохотити активну співпрацю, Laravel наполегливо радить надсилати pull request'и, а не просто повідомлення про помилки. Pull request'и розглядатимуться лише тоді, коли їх позначено як «ready for review» (тобто не в стані «draft») і всі тести для нових можливостей проходять. Застарілі неактивні pull request'и, залишені у стані «draft», будуть закриті за кілька днів.

Утім, якщо ви створюєте повідомлення про помилку, воно має містити заголовок і чіткий опис проблеми. Також варто додати якомога більше доречної інформації та приклад коду, що демонструє проблему. Мета повідомлення про помилку - полегшити вам і іншим відтворення помилки та розробку виправлення.

Пам'ятайте: повідомлення про помилки створюються з надією, що інші з такою самою проблемою зможуть співпрацювати з вами над її розв'язанням. Не очікуйте, що повідомлення автоматично привабить увагу або що хтось кинеться його виправляти. Створення повідомлення допомагає вам та іншим стати на шлях вирішення проблеми. Якщо хочете долучитися, можете допомогти, виправивши [будь-яку з помилок у наших трекерах](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). Щоб побачити всі issue Laravel, потрібно бути автентифікованим на GitHub.

Якщо під час роботи з Laravel ви помітили некоректний DocBlock або попередження PHPStan чи IDE, не створюйте issue на GitHub. Натомість надішліть pull request із виправленням.

Вихідний код Laravel розміщено на GitHub, і для кожного з проєктів Laravel є свій репозиторій:

<div class="content-list" markdown="1">

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
- [Laravel Livewire Starter Kit](https://github.com/laravel/livewire-starter-kit)
- [Laravel React Starter Kit](https://github.com/laravel/react-starter-kit)
- [Laravel Svelte Starter Kit](https://github.com/laravel/svelte-starter-kit)
- [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## Питання щодо підтримки

Трекери issue на GitHub не призначені для надання допомоги чи підтримки щодо Laravel. Натомість скористайтеся одним із таких каналів:

<div class="content-list" markdown="1">

- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
## Обговорення розробки ядра

Ви можете пропонувати нові можливості або покращення наявної поведінки Laravel на [дошці обговорень GitHub](https://github.com/laravel/framework/discussions) у репозиторії фреймворку. Якщо ви пропонуєте нову можливість, будьте готові реалізувати хоча б частину коду, потрібного для її втілення.

Неформальне обговорення помилок, нових можливостей і реалізації наявних відбувається в каналі `#internals` на [сервері Laravel у Discord](https://discord.gg/laravel). Тейлор Отвелл, супровідник Laravel, зазвичай присутній у каналі в будні з 8:00 до 17:00 (UTC-06:00 або America/Chicago) та епізодично в інший час.

<a name="which-branch"></a>
## Яку гілку обрати?

**Усі** виправлення помилок слід надсилати до найновішої версії, яка підтримує виправлення помилок (наразі `13.x`). Виправлення помилок **ніколи** не слід надсилати до гілки `master`, окрім випадків, коли вони виправляють можливості, що існують лише в майбутньому релізі.

**Незначні** можливості, **повністю зворотно сумісні** з поточним релізом, можна надсилати до останньої стабільної гілки (наразі `13.x`).

**Великі** нові можливості або можливості зі змінами, що порушують сумісність, завжди слід надсилати до гілки `master`, яка містить майбутній реліз.

<a name="compiled-assets"></a>
## Скомпільовані ресурси

Якщо ви надсилаєте зміну, яка вплине на скомпільований файл - як-от більшість файлів у `resources/css` чи `resources/js` репозиторію `laravel/laravel`, - не комітьте скомпільовані файли. Через їхній великий розмір супровідник не зможе реально їх перевірити. Цим можна скористатися, щоб впровадити зловмисний код у Laravel. Щоб запобігти цьому, усі скомпільовані файли генеруються й комітяться супровідниками Laravel.

<a name="ai-generated-contributions"></a>
## Внески, згенеровані AI

Ми цінуємо кожен pull request, надісланий до Laravel. Однак внески, здебільшого згенеровані AI без вдумливого перегляду й осмислення людиною, неприйнятні.

Якщо ви вирішили скористатися AI-інструментами для підготовки свого внеску, отриманий код **обов'язково** має бути ретельно переглянутий, протестований і зрозумілий вам перед надсиланням.

**Масове створення issue чи pull request'ів, повністю згенерованих AI, не буде терпітися.** Такі pull request'и закриватимуться без розгляду, а користувача, який їх надіслав, може бути заблоковано в репозиторії.

Ми заохочуємо контриб'юторів ознайомлюватися з наявною кодовою базою, взаємодіяти зі спільнотою та надсилати pull request'и, які відображають їхнє власне розуміння й уважне осмислення проблеми, яку вони розв'язують.

<a name="security-vulnerabilities"></a>
## Вразливості безпеки

Якщо ви виявили вразливість безпеки в Laravel, надішліть листа нашій команді безпеки на <a href="mailto:security@laravel.com">security@laravel.com</a>. Усі вразливості безпеки буде оперативно опрацьовано.

<a name="coding-style"></a>
## Стиль коду

Laravel дотримується стандарту кодування [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) та стандарту автозавантаження [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md).

<a name="phpdoc"></a>
### PHPDoc

Нижче наведено приклад коректного блоку документації Laravel. Зверніть увагу, що після атрибута `@param` іде два пробіли, тип аргументу, ще два пробіли й нарешті ім'я змінної:

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

Коли атрибути `@param` чи `@return` є надлишковими через використання нативних типів, їх можна прибрати:

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

Однак якщо нативний тип є узагальненим (generic), вкажіть узагальнений тип за допомогою атрибутів `@param` чи `@return`:

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

<a name="styleci"></a>
### StyleCI

Не хвилюйтеся, якщо стиль вашого коду не бездоганний! [StyleCI](https://styleci.io/) автоматично зіллє всі виправлення стилю до репозиторію Laravel після злиття pull request'ів. Це дозволяє нам зосередитися на змісті внеску, а не на стилі коду.

<a name="code-of-conduct"></a>
## Кодекс поведінки

Кодекс поведінки Laravel походить від кодексу поведінки Ruby. Про будь-які порушення кодексу поведінки можна повідомити Тейлору Отвеллу (taylor@laravel.com):

<div class="content-list" markdown="1">

- Учасники мають бути толерантними до протилежних поглядів.
- Учасники повинні стежити, щоб їхні висловлювання та дії були вільними від особистих нападів і принизливих зауважень на адресу інших.
- Тлумачачи слова й дії інших, учасники завжди мають припускати добрі наміри.
- Поведінка, яку можна обґрунтовано вважати домаганням, не буде терпітися.

</div>

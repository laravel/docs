---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Pint

- [Вступ](#introduction)
- [Встановлення](#installation)
- [Запуск Pint](#running-pint)
- [Налаштування Pint](#configuring-pint)
    - [Пресети](#presets)
    - [Правила](#rules)
    - [Виключення файлів і каталогів](#excluding-files-or-folders)
- [Неперервна інтеграція](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## Вступ

[Laravel Pint](https://github.com/laravel/pint) - це самобутній інструмент виправлення стилю коду PHP для мінімалістів. Pint побудований на [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) і дозволяє легко тримати стиль вашого коду чистим і послідовним.

Pint автоматично встановлюється в усі нові застосунки Laravel, тож ви можете користуватися ним одразу. За замовчуванням Pint не потребує жодної конфігурації й виправлятиме проблеми стилю у вашому коді, дотримуючись самобутнього стилю кодування Laravel.

<a name="installation"></a>
## Встановлення

Pint входить до останніх випусків фреймворку Laravel, тож встановлювати його зазвичай не потрібно. Проте для старіших застосунків ви можете встановити Laravel Pint через Composer:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Запуск Pint

Ви можете доручити Pint виправити проблеми стилю коду, викликавши бінарник `pint`, доступний у каталозі `vendor/bin` вашого проєкту:

```shell
./vendor/bin/pint
```

Якщо ви хочете запустити Pint у паралельному режимі (експериментальному) для кращої продуктивності, скористайтеся опцією `--parallel`:

```shell
./vendor/bin/pint --parallel
```

Паралельний режим також дозволяє вказати максимальну кількість процесів через опцію `--max-processes`. Якщо цю опцію не задано, Pint використає всі доступні ядра на вашій машині:

```shell
./vendor/bin/pint --parallel --max-processes=4
```

Ви також можете запустити Pint на конкретних файлах чи каталогах:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint покаже докладний список усіх файлів, які він оновив. Побачити ще більше деталей про зміни Pint можна, додавши до виклику опцію `-v`:

```shell
./vendor/bin/pint -v
```

Якщо ви хочете, щоб Pint просто перевірив ваш код на помилки стилю, не змінюючи файлів, скористайтеся опцією `--test`. Pint поверне ненульовий код виходу, якщо знайде хоч одну помилку стилю:

```shell
./vendor/bin/pint --test
```

Якщо ви хочете, щоб Pint змінював лише файли, які, за даними Git, відрізняються від указаної гілки, скористайтеся опцією `--diff=[branch]`. Це можна ефективно застосувати у вашому CI-середовищі (наприклад, у GitHub actions), щоб заощадити час, перевіряючи лише нові чи змінені файли:

```shell
./vendor/bin/pint --diff=main
```

Якщо ви хочете, щоб Pint змінював лише файли з незакомміченими змінами за даними Git, скористайтеся опцією `--dirty`:

```shell
./vendor/bin/pint --dirty
```

Якщо ви хочете, щоб Pint виправляв файли з помилками стилю, але водночас завершувався з ненульовим кодом виходу, коли якісь помилки було виправлено, скористайтеся опцією `--repair`:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Налаштування Pint

Як згадувалося раніше, Pint не потребує жодної конфігурації. Проте якщо ви хочете налаштувати пресети, правила чи каталоги для перевірки, створіть файл `pint.json` у кореневому каталозі вашого проєкту:

```json
{
    "preset": "laravel"
}
```

Крім того, якщо ви хочете використати `pint.json` з певного каталогу, додайте до виклику Pint опцію `--config`:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### Пресети

Пресети визначають набір правил, за якими виправляються проблеми стилю у вашому коді. За замовчуванням Pint використовує пресет `laravel`, який виправляє проблеми за самобутнім стилем кодування Laravel. Проте ви можете вказати інший пресет, передавши Pint опцію `--preset`:

```shell
./vendor/bin/pint --preset psr12
```

За бажання ви можете задати пресет і у файлі `pint.json` вашого проєкту:

```json
{
    "preset": "psr12"
}
```

Наразі Pint підтримує такі пресети: `laravel`, `per`, `psr12`, `symfony` та `empty`.

<a name="rules"></a>
### Правила

Правила - це настанови щодо стилю, за якими Pint виправлятиме проблеми у вашому коді. Як зазначено вище, пресети - це наперед визначені групи правил, які мають чудово пасувати більшості проєктів на PHP, тож зазвичай вам не доведеться перейматися окремими правилами всередині них.

Проте за бажання ви можете вмикати чи вимикати конкретні правила у своєму файлі `pint.json` або скористатися пресетом `empty` й описати правила з нуля:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "array_indentation": false,
        "new_with_parentheses": {
            "anonymous_class": true,
            "named_class": true
        }
    }
}
```

Pint побудований на [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer). Тому ви можете скористатися будь-яким з його правил, щоб виправити проблеми стилю у своєму проєкті: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="custom-rules"></a>
#### Власні правила

Окрім правил PHP CS Fixer, Pint надає власні правила з префіксом `Pint/`. За замовчуванням вони вимкнені, але ви можете ввімкнути їх у своєму файлі `pint.json`.

<a name="phpdoc-type-annotations-only"></a>
##### `Pint/phpdoc_type_annotations_only`

Це правило прибирає з вашого коду всі коментарі та прозу з докблоків, лишаючи тільки рядки з анотаціями `@` - як-от `@param`, `@return`, `@var`, `@phpstan-type` тощо:

```php
/**
 * Get the posts for the user. [tl! remove]
 * [tl! remove]
 * @return HasMany<Post, $this>
 */
public function posts(): HasMany
```

Однорядкові коментарі та блокові коментарі без анотацій `@` прибираються цілком. Якщо ви хочете зберегти конкретний коментар, додайте до нього префікс `@note`, `@warning` чи `@todo`:

```php
// @note This comment will be preserved.
```

Щоб увімкнути це правило, додайте його до свого файлу `pint.json`:

```json
{
    "preset": "laravel",
    "rules": {
        "Pint/phpdoc_type_annotations_only": true
    }
}
```

> [!NOTE]
> Це правило автоматично пропускає файли в каталозі `config`, адже конфігураційні файли зазвичай спираються на коментарі як на документацію.

<a name="excluding-files-or-folders"></a>
### Виключення файлів і каталогів

За замовчуванням Pint перевіряє всі файли `.php` у вашому проєкті, окрім тих, що в каталозі `vendor`. Якщо ви хочете виключити більше каталогів, скористайтеся опцією конфігурації `exclude`:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

Якщо ви хочете виключити всі файли, чиї імена відповідають заданому шаблону, скористайтеся опцією конфігурації `notName`:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

Якщо ви хочете виключити файл, указавши точний шлях до нього, скористайтеся опцією конфігурації `notPath`:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## Неперервна інтеграція

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Щоб автоматизувати лінтинг вашого проєкту через Laravel Pint, ви можете налаштувати [GitHub Actions](https://github.com/features/actions) запускати Pint щоразу, коли новий код потрапляє на GitHub. Спершу обов'язково надайте робочим процесам дозвіл «Read and write permissions» у GitHub за адресою **Settings > Actions > General > Workflow permissions**. Далі створіть файл `.github/workflows/lint.yml` з таким вмістом:

```yaml
name: Fix Code Style

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        php: [8.4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          tools: pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v6
```

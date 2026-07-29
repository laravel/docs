---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Sail

- [Вступ](#introduction)
- [Встановлення й налаштування](#installation)
    - [Перезбирання образів Sail](#rebuilding-sail-images)
    - [Налаштування аліаса в оболонці](#configuring-a-shell-alias)
- [Запуск і зупинка Sail](#starting-and-stopping-sail)
- [Виконання команд](#executing-sail-commands)
    - [Виконання команд PHP](#executing-php-commands)
    - [Виконання команд Composer](#executing-composer-commands)
    - [Виконання артизан-команд](#executing-artisan-commands)
    - [Виконання команд Node / NPM](#executing-node-npm-commands)
- [Робота з базами даних](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [Зберігання файлів](#file-storage)
- [Запуск тестів](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Перегляд листів](#previewing-emails)
- [CLI контейнера](#sail-container-cli)
- [Версії PHP](#sail-php-versions)
    - [Додаткові розширення PHP](#sail-php-extensions)
- [Версії Node](#sail-node-versions)
- [Публічний доступ до вашого сайту](#sharing-your-site)
- [Налагодження через Xdebug](#debugging-with-xdebug)
    - [Xdebug у CLI](#xdebug-cli-usage)
    - [Xdebug у браузері](#xdebug-browser-usage)
- [Налаштування](#sail-customization)

<a name="introduction"></a>
## Вступ

[Laravel Sail](https://github.com/laravel/sail) - це легкий інтерфейс командного рядка для роботи зі стандартним середовищем розробки Laravel на Docker. Sail дає чудову відправну точку, щоб будувати застосунок Laravel на PHP, MySQL і Redis без попереднього досвіду з Docker.

По суті, Sail - це файл `compose.yaml` і скрипт `sail`, що лежить у корені вашого проєкту. Скрипт `sail` надає CLI зі зручними методами для роботи з контейнерами Docker, описаними у файлі `compose.yaml`.

Laravel Sail підтримується на macOS, Linux і Windows (через [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)).

<a name="installation"></a>
## Встановлення й налаштування

Ви можете встановити Sail через менеджер пакетів Composer:

```shell
composer require laravel/sail --dev
```

Після встановлення Sail виконайте артизан-команду `sail:install`. Ця команда опублікує файл `compose.yaml` до кореня вашого застосунку й додасть до вашого файлу `.env` змінні оточення, потрібні для підключення до сервісів Docker:

```shell
php artisan sail:install
```

Нарешті, ви можете запустити Sail. Щоб дізнатися більше про роботу із Sail, читайте цю документацію далі:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Якщо ви користуєтеся Docker Desktop для Linux, скористайтеся контекстом Docker `default`, виконавши таку команду: `docker context use default`. Крім того, якщо ви натрапите на помилки прав доступу до файлів усередині контейнерів, вам може знадобитися встановити змінну оточення `SUPERVISOR_PHP_USER` у значення `root`.

<a name="adding-additional-services"></a>
#### Додавання додаткових сервісів

Якщо ви хочете додати ще один сервіс до наявної установки Sail, виконайте артизан-команду `sail:add`:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Використання Devcontainers

Якщо ви хочете розробляти всередині [Devcontainer](https://code.visualstudio.com/docs/remote/containers), додайте до команди `sail:install` опцію `--devcontainer`. Опція `--devcontainer` вкаже команді `sail:install` опублікувати до кореня вашого застосунку стандартний файл `.devcontainer/devcontainer.json `:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Перезбирання образів Sail

Іноді вам може знадобитися повністю перезібрати образи Sail, щоб переконатися, що всі пакети й програми в образі актуальні. Зробити це можна командою `build`:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### Налаштування аліаса в оболонці

За замовчуванням команди Sail викликаються через скрипт `vendor/bin/sail`, який входить до всіх нових застосунків Laravel:

```shell
./vendor/bin/sail up
```

Проте, замість того щоб раз у раз набирати `vendor/bin/sail`, ви можете налаштувати аліас в оболонці, який дозволить виконувати команди Sail простіше:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

Щоб аліас був доступний завжди, додайте його до конфігураційного файлу вашої оболонки в домашньому каталозі - як-от `~/.zshrc` чи `~/.bashrc`, - а потім перезапустіть оболонку.

Коли аліас налаштовано, ви можете виконувати команди Sail, просто набираючи `sail`. Далі в цій документації приклади припускають, що ви налаштували цей аліас:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Запуск і зупинка Sail

Файл `compose.yaml` у Laravel Sail описує різні контейнери Docker, які працюють разом, щоб допомогти вам будувати застосунки Laravel. Кожен із цих контейнерів - запис у конфігурації `services` вашого файлу `compose.yaml`. Контейнер `laravel.test` - головний контейнер застосунку, який його й віддаватиме.

Перш ніж запускати Sail, переконайтеся, що на вашому комп'ютері не працюють інші вебсервери чи бази даних. Щоб запустити всі контейнери Docker, описані у файлі `compose.yaml` вашого застосунку, виконайте команду `up`:

```shell
sail up
```

Щоб запустити всі контейнери Docker у фоні, стартуйте Sail у «відчепленому» (detached) режимі:

```shell
sail up -d
```

Коли контейнери застосунку запущено, ви можете відкрити проєкт у браузері за адресою http://localhost.

Щоб зупинити всі контейнери, просто натисніть Control + C. Або, якщо контейнери працюють у фоні, скористайтеся командою `stop`:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## Виконання команд

Коли ви користуєтеся Laravel Sail, ваш застосунок виконується всередині контейнера Docker і ізольований від вашого комп'ютера. Проте Sail дає зручний спосіб запускати різні команди щодо вашого застосунку - як-от довільні команди PHP, артизан-команди, команди Composer і Node / NPM.

**Читаючи документацію Laravel, ви часто бачитимете згадки команд Composer, Artisan і Node / NPM без Sail.** Ті приклади припускають, що ці інструменти встановлено на вашому комп'ютері. Якщо ви користуєтеся Sail як локальним середовищем розробки Laravel, виконуйте ці команди через Sail:

```shell
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### Виконання команд PHP

Команди PHP виконуються командою `php`. Звісно, вони виконуватимуться тією версією PHP, яку налаштовано для вашого застосунку. Щоб дізнатися більше про версії PHP, доступні в Laravel Sail, зверніться до [документації про версії PHP](#sail-php-versions):

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Виконання команд Composer

Команди Composer виконуються командою `composer`. Контейнер застосунку в Laravel Sail містить встановлений Composer:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Виконання артизан-команд

Артизан-команди Laravel виконуються командою `artisan`:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Виконання команд Node / NPM

Команди Node виконуються командою `node`, а команди NPM - командою `npm`:

```shell
sail node --version

sail npm run dev
```

За бажання ви можете скористатися Yarn замість NPM:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## Робота з базами даних

<a name="mysql"></a>
### MySQL

Як ви могли помітити, файл `compose.yaml` вашого застосунку містить запис для контейнера MySQL. Цей контейнер використовує [том Docker](https://docs.docker.com/storage/volumes/), тож дані у вашій базі зберігаються навіть при зупинці й перезапуску контейнерів.

Крім того, під час першого запуску контейнер MySQL створить для вас дві бази даних. Перша названа за значенням вашої змінної оточення `DB_DATABASE` і призначена для локальної розробки. Друга - окрема тестова база на ім'я `testing`, яка гарантує, що ваші тести не заважатимуть даним розробки.

Коли контейнери запущено, ви можете підключитися до екземпляра MySQL у своєму застосунку, встановивши змінну оточення `DB_HOST` у файлі `.env` вашого застосунку в значення `mysql`.

Щоб підключитися до бази MySQL вашого застосунку зі свого комп'ютера, скористайтеся графічним застосунком для керування базами - як-от [TablePlus](https://tableplus.com). За замовчуванням база MySQL доступна на `localhost`, порт 3306, а облікові дані відповідають значенням ваших змінних оточення `DB_USERNAME` та `DB_PASSWORD`. Або ж ви можете підключитися як користувач `root`, чиїм паролем також є значення змінної оточення `DB_PASSWORD`.

<a name="mongodb"></a>
### MongoDB

Якщо під час встановлення Sail ви обрали сервіс [MongoDB](https://www.mongodb.com/), файл `compose.yaml` вашого застосунку містить запис для контейнера [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/), який надає документну базу MongoDB з можливостями Atlas - як-от [пошукові індекси](https://www.mongodb.com/docs/atlas/atlas-search/). Цей контейнер використовує [том Docker](https://docs.docker.com/storage/volumes/), тож дані у вашій базі зберігаються навіть при зупинці й перезапуску контейнерів.

Коли контейнери запущено, ви можете підключитися до екземпляра MongoDB у своєму застосунку, встановивши змінну оточення `MONGODB_URI` у файлі `.env` вашого застосунку в значення `mongodb://mongodb:27017`. Автентифікацію за замовчуванням вимкнено, але ви можете задати змінні оточення `MONGODB_USERNAME` та `MONGODB_PASSWORD`, щоб увімкнути її перед запуском контейнера `mongodb`. Далі додайте облікові дані до рядка підключення:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

Для безшовної інтеграції MongoDB з вашим застосунком можна встановити [офіційний пакет, який підтримує MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/).

Щоб підключитися до бази MongoDB вашого застосунку зі свого комп'ютера, скористайтеся графічним інтерфейсом - як-от [Compass](https://www.mongodb.com/products/tools/compass). За замовчуванням база MongoDB доступна на `localhost`, порт `27017`.

<a name="redis"></a>
### Redis

Файл `compose.yaml` вашого застосунку містить також запис для контейнера [Redis](https://redis.io). Цей контейнер використовує [том Docker](https://docs.docker.com/storage/volumes/), тож дані у вашому екземплярі Redis зберігаються навіть при зупинці й перезапуску контейнерів. Коли контейнери запущено, ви можете підключитися до екземпляра Redis у своєму застосунку, встановивши змінну оточення `REDIS_HOST` у файлі `.env` вашого застосунку в значення `redis`.

Щоб підключитися до бази Redis вашого застосунку зі свого комп'ютера, скористайтеся графічним застосунком для керування базами - як-от [TablePlus](https://tableplus.com). За замовчуванням база Redis доступна на `localhost`, порт 6379.

<a name="valkey"></a>
### Valkey

Якщо під час встановлення Sail ви обрали сервіс Valkey, файл `compose.yaml` вашого застосунку міститиме запис для [Valkey](https://valkey.io/). Цей контейнер використовує [том Docker](https://docs.docker.com/storage/volumes/), тож дані у вашому екземплярі Valkey зберігаються навіть при зупинці й перезапуску контейнерів. Ви можете підключитися до цього контейнера у своєму застосунку, встановивши змінну оточення `REDIS_HOST` у файлі `.env` вашого застосунку в значення `valkey`.

Щоб підключитися до бази Valkey вашого застосунку зі свого комп'ютера, скористайтеся графічним застосунком для керування базами - як-от [TablePlus](https://tableplus.com). За замовчуванням база Valkey доступна на `localhost`, порт 6379.

<a name="meilisearch"></a>
### Meilisearch

Якщо під час встановлення Sail ви обрали сервіс [Meilisearch](https://www.meilisearch.com), файл `compose.yaml` вашого застосунку міститиме запис для цього потужного пошукового рушія, інтегрованого з [Laravel Scout](/docs/{{version}}/scout). Коли контейнери запущено, ви можете підключитися до екземпляра Meilisearch у своєму застосунку, встановивши змінну оточення `MEILISEARCH_HOST` у значення `http://meilisearch:7700`.

Зі свого комп'ютера ви можете відкрити вебпанель адміністрування Meilisearch, перейшовши у браузері за адресою `http://localhost:7700`.

<a name="typesense"></a>
### Typesense

Якщо під час встановлення Sail ви обрали сервіс [Typesense](https://typesense.org), файл `compose.yaml` вашого застосунку міститиме запис для цього блискавично швидкого пошукового рушія з відкритим кодом, який нативно інтегрований з [Laravel Scout](/docs/{{version}}/scout#typesense). Коли контейнери запущено, ви можете підключитися до екземпляра Typesense у своєму застосунку, задавши такі змінні оточення:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

Зі свого комп'ютера ви можете звертатися до API Typesense за адресою `http://localhost:8108`.

<a name="file-storage"></a>
## Зберігання файлів

Якщо ви плануєте зберігати файли в Amazon S3, коли ваш застосунок працює у продакшн-середовищі, вам, можливо, варто встановити сервіс [RustFS](https://rustfs.com) під час встановлення Sail. RustFS надає сумісний із S3 API, яким ви можете розробляти локально через драйвер файлового сховища `s3` у Laravel, не створюючи «тестових» бакетів у своєму продакшн-середовищі S3. Якщо ви оберете RustFS під час встановлення Sail, до файлу `compose.yaml` вашого застосунку буде додано секцію конфігурації RustFS.

За замовчуванням конфігураційний файл `filesystems` вашого застосунку вже містить конфігурацію диска `s3`. Окрім роботи з Amazon S3, цей диск можна використовувати з будь-яким сумісним із S3 сервісом зберігання файлів - як-от RustFS, - просто змінивши відповідні змінні оточення, що керують його конфігурацією. Наприклад, для RustFS конфігурація змінних оточення файлової системи має мати такий вигляд:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://rustfs:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
## Запуск тестів

Laravel надає чудову підтримку тестування одразу з коробки, і ви можете скористатися командою Sail `test`, щоб запустити [функціональні та юніт-тести](/docs/{{version}}/testing) свого застосунку. Будь-які опції CLI, які приймають Pest / PHPUnit, можна передати й команді `test`:

```shell
sail test

sail test --group orders
```

Команда Sail `test` рівносильна виконанню артизан-команди `test`:

```shell
sail artisan test
```

За замовчуванням Sail створить окрему базу `testing`, щоб ваші тести не заважали поточному стану вашої бази даних. У стандартній установці Laravel Sail також налаштує ваш файл `phpunit.xml` на використання цієї бази під час прогону тестів:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) надає виразний і простий у користуванні API для автоматизації браузера й тестування. Завдяки Sail ви можете запускати ці тести, не встановлюючи Selenium чи інші інструменти на своєму комп'ютері. Для початку розкоментуйте сервіс Selenium у файлі `compose.yaml` вашого застосунку:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

Далі переконайтеся, що сервіс `laravel.test` у файлі `compose.yaml` вашого застосунку має запис `depends_on` для `selenium`:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

Нарешті, ви можете запустити свій набір тестів Dusk, стартувавши Sail і виконавши команду `dusk`:

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Selenium на Apple Silicon

Якщо ваш комп'ютер має чип Apple Silicon, ваш сервіс `selenium` має використовувати образ `selenium/standalone-chromium`:

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## Перегляд листів

Стандартний файл `compose.yaml` у Laravel Sail містить запис сервісу для [Mailpit](https://github.com/axllent/mailpit). Mailpit перехоплює листи, надіслані вашим застосунком під час локальної розробки, і надає зручний вебінтерфейс, щоб ви могли переглядати їх у браузері. Із Sail стандартний хост Mailpit - `mailpit`, доступний на порту 1025:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Коли Sail працює, ви можете відкрити вебінтерфейс Mailpit за адресою http://localhost:8025

<a name="sail-container-cli"></a>
## CLI контейнера

Іноді вам може знадобитися відкрити сеанс Bash усередині контейнера вашого застосунку. Скористайтеся командою `shell`, щоб підключитися до контейнера застосунку, - так ви зможете оглянути його файли та встановлені сервіси, а також виконувати довільні команди оболонки всередині контейнера:

```shell
sail shell

sail root-shell
```

Щоб розпочати новий сеанс [Laravel Tinker](https://github.com/laravel/tinker), виконайте команду `tinker`:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## Версії PHP

Наразі Sail підтримує роботу вашого застосунку на PHP 8.5, 8.4, 8.3, 8.2, 8.1 чи PHP 8.0. Стандартна версія PHP у Sail наразі - PHP 8.5. Щоб змінити версію PHP, якою віддається ваш застосунок, оновіть визначення `build` контейнера `laravel.test` у файлі `compose.yaml` вашого застосунку:

```yaml
# PHP 8.5
context: ./vendor/laravel/sail/runtimes/8.5

# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

Крім того, вам, можливо, варто оновити ім'я `image`, щоб воно відображало версію PHP, яку використовує ваш застосунок. Ця опція також визначена у файлі `compose.yaml` вашого застосунку:

```yaml
image: sail-8.2/app
```

Оновивши файл `compose.yaml` вашого застосунку, перезберіть образи контейнерів:

```shell
sail build --no-cache

sail up
```

<a name="sail-php-extensions"></a>
### Додаткові розширення PHP

Образи середовища виконання Sail містять поширений набір розширень PHP. Якщо вашому застосунку потрібні додаткові розширення, ви можете встановити їх під час збирання образу, додавши до сервісу `laravel.test` у файлі `compose.yaml` вашого застосунку аргумент збірки `PHP_EXTENSIONS` зі значеннями через пробіл:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        PHP_EXTENSIONS: 'gmp imagick'
```

Оновивши файл `compose.yaml` вашого застосунку, перезберіть образи контейнерів.

<a name="sail-node-versions"></a>
## Версії Node

За замовчуванням Sail встановлює Node 24. Щоб змінити версію Node, яка встановлюється під час збирання образів, оновіть визначення `build.args` сервісу `laravel.test` у файлі `compose.yaml` вашого застосунку:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

Оновивши файл `compose.yaml` вашого застосунку, перезберіть образи контейнерів:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## Публічний доступ до вашого сайту

Іноді вам може знадобитися відкрити свій сайт публічно, щоб показати його колезі чи протестувати інтеграції з вебхуками. Щоб поділитися сайтом, скористайтеся командою `share`. Виконавши її, ви отримаєте випадкову адресу `laravel-sail.site`, за якою можна звертатися до вашого застосунку:

```shell
sail share
```

Відкриваючи сайт командою `share`, налаштуйте довірені проксі вашого застосунку методом `middleware` `trustProxies` у файлі `bootstrap/app.php`. Інакше хелпери генерування URL - як-от `url` і `route` - не зможуть визначити правильний HTTP-хост для генерування URL:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

Якщо ви хочете обрати піддомен для свого відкритого сайту, додайте опцію `subdomain` до команди `share`:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> Команда `share` працює на [Expose](https://github.com/beyondcode/expose) - сервісі тунелювання з відкритим кодом від [BeyondCode](https://beyondco.de).

<a name="debugging-with-xdebug"></a>
## Налагодження через Xdebug

Конфігурація Docker у Laravel Sail містить підтримку [Xdebug](https://xdebug.org/) - популярного й потужного налагоджувача для PHP. Щоб увімкнути Xdebug, переконайтеся, що ви [опублікували конфігурацію Sail](#sail-customization). Далі додайте до файлу `.env` вашого застосунку такі змінні, щоб налаштувати Xdebug:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

Далі переконайтеся, що ваш опублікований файл `php.ini` містить таку конфігурацію, щоб Xdebug активувався у вказаних режимах:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

Змінивши файл `php.ini`, не забудьте перезібрати образи Docker, щоб ваші зміни набрали чинності:

```shell
sail build --no-cache
```

#### Налаштування IP хоста на Linux

Усередині змінна оточення `XDEBUG_CONFIG` має значення `client_host=host.docker.internal`, щоб Xdebug був належно налаштований для Mac і Windows (WSL2). Якщо ваш комп'ютер працює на Linux і ви користуєтеся Docker 20.10+, `host.docker.internal` доступний, і ручне налаштування не потрібне.

Для версій Docker, старіших за 20.10, `host.docker.internal` на Linux не підтримується, тож вам доведеться задати IP хоста вручну. Для цього налаштуйте статичний IP для свого контейнера, описавши власну мережу у файлі `compose.yaml`:

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```

Задавши статичний IP, визначте змінну SAIL_XDEBUG_CONFIG у файлі .env вашого застосунку:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug у CLI

Команда `sail debug` дозволяє розпочати сеанс налагодження під час виконання артизан-команди:

```shell
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug у браузері

Щоб налагоджувати застосунок, працюючи з ним через веббраузер, дотримуйтеся [інструкцій Xdebug](https://xdebug.org/docs/step_debug#web-application) щодо запуску сеансу Xdebug із браузера.

Якщо ви користуєтеся PhpStorm, перегляньте документацію JetBrains про [налагодження без конфігурації](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html).

> [!WARNING]
> Laravel Sail покладається на `artisan serve`, щоб віддавати ваш застосунок. Команда `artisan serve` приймає змінні `XDEBUG_CONFIG` та `XDEBUG_MODE` лише починаючи з Laravel 8.53.0. Старіші версії Laravel (8.52.0 і нижче) не підтримують цих змінних і не приймуть налагоджувальних підключень.

<a name="sail-customization"></a>
## Налаштування

Оскільки Sail - це просто Docker, ви вільні налаштувати в ньому майже все. Щоб опублікувати власні Dockerfile Sail, виконайте команду `sail:publish`:

```shell
sail artisan sail:publish
```

Після виконання цієї команди Dockerfile та інші конфігураційні файли, які використовує Laravel Sail, потраплять до каталогу `docker` у корені вашого застосунку. Налаштувавши свою установку Sail, вам, можливо, варто змінити ім'я образу для контейнера застосунку у файлі `compose.yaml`. Після цього перезберіть контейнери застосунку командою `build`. Присвоєння унікального імені образу застосунку особливо важливе, якщо ви розробляєте через Sail кілька застосунків Laravel на одній машині:

```shell
sail build --no-cache
```

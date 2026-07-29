---
git: 946622229fa1d90052b7d51614a4a14a7156b9b0
---
# Laravel Octane

- [Вступ](#introduction)
- [Встановлення](#installation)
- [Вимоги до сервера](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Обслуговування вашого застосунку](#serving-your-application)
    - [Обслуговування застосунку через HTTPS](#serving-your-application-via-https)
    - [Обслуговування застосунку через Nginx](#serving-your-application-via-nginx)
    - [Відстеження змін у файлах](#watching-for-file-changes)
    - [Визначення кількості воркерів](#specifying-the-worker-count)
    - [Визначення максимальної кількості запитів](#specifying-the-max-request-count)
    - [Визначення максимального часу виконання](#specifying-the-max-execution-time)
    - [Перезавантаження воркерів](#reloading-the-workers)
    - [Зупинка сервера](#stopping-the-server)
- [Впровадження залежностей і Octane](#dependency-injection-and-octane)
    - [Впровадження контейнера](#container-injection)
    - [Впровадження запиту](#request-injection)
    - [Впровадження репозиторію конфігурації](#configuration-repository-injection)
- [Керування витоками пам'яті](#managing-memory-leaks)
- [Паралельні завдання](#concurrent-tasks)
- [Тіки та інтервали](#ticks-and-intervals)
- [Кеш Octane](#the-octane-cache)
- [Таблиці](#tables)

<a name="introduction"></a>
## Вступ

[Laravel Octane](https://github.com/laravel/octane) різко підвищує продуктивність вашого застосунку, обслуговуючи його за допомогою потужних серверів застосунків, зокрема [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src) і [RoadRunner](https://roadrunner.dev). Octane завантажує ваш застосунок один раз, тримає його в пам'яті, а потім подає йому запити на надзвуковій швидкості.

<a name="installation"></a>
## Встановлення

Octane можна встановити через менеджер пакетів Composer:

```shell
composer require laravel/octane
```

Після встановлення Octane ви можете виконати артизан-команду `octane:install`, яка встановить конфігураційний файл Octane у ваш застосунок:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## Вимоги до сервера

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev) - це сервер PHP-застосунків, написаний на Go, який підтримує сучасні вебможливості на кшталт early hints, стиснення Brotli та Zstandard. Коли ви встановлюєте Octane і обираєте FrankenPHP як свій сервер, Octane автоматично завантажить і встановить бінарник FrankenPHP за вас.

<a name="frankenphp-via-laravel-sail"></a>
#### FrankenPHP через Laravel Sail

Якщо ви плануєте розробляти застосунок за допомогою [Laravel Sail](/docs/{{version}}/sail), виконайте такі команди, щоб установити Octane і FrankenPHP:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

Далі скористайтеся артизан-командою `octane:install`, щоб установити бінарник FrankenPHP:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

Насамкінець додайте змінну оточення `SUPERVISOR_PHP_COMMAND` до визначення сервісу `laravel.test` у файлі `docker-compose.yml` вашого застосунку. Ця змінна оточення міститиме команду, якою Sail обслуговуватиме ваш застосунок через Octane замість девсервера PHP:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

Щоб увімкнути HTTPS, HTTP/2 і HTTP/3, застосуйте натомість такі зміни:

```yaml
services:
  laravel.test:
    ports:
        - '${APP_PORT:-80}:80'
        - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        - '443:443' # [tl! add]
        - '443:443/udp' # [tl! add]
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --host=localhost --port=443 --admin-port=2019 --https" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

Зазвичай до вашого Sail-застосунку на FrankenPHP слід звертатися через `https://localhost`, оскільки використання `https://127.0.0.1` потребує додаткового налаштування і [не рекомендується](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### FrankenPHP через Docker

Використання офіційних Docker-образів FrankenPHP може дати кращу продуктивність і доступ до додаткових розширень, яких немає у статичних інсталяціях FrankenPHP. Крім того, офіційні Docker-образи дозволяють запускати FrankenPHP на платформах, які він нативно не підтримує, наприклад на Windows. Офіційні Docker-образи FrankenPHP підходять як для локальної розробки, так і для продакшену.

Ви можете взяти наведений нижче Dockerfile за відправну точку для контейнеризації вашого Laravel-застосунку на FrankenPHP:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

Далі, під час розробки, ви можете скористатися таким файлом Docker Compose для запуску застосунку:

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --workers=1 --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

Якщо до команди `php artisan octane:start` явно передано опцію `--log-level`, Octane використовуватиме нативний логер FrankenPHP і, якщо не налаштовано інакше, видаватиме структуровані JSON-логи.

Докладніше про запуск FrankenPHP з Docker дивіться в [офіційній документації FrankenPHP](https://frankenphp.dev/docs/docker/).

<a name="frankenphp-caddyfile"></a>
#### Власна конфігурація Caddyfile

Використовуючи FrankenPHP, ви можете вказати власний Caddyfile за допомогою опції `--caddyfile` під час запуску Octane:

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

Це дозволяє налаштувати FrankenPHP поза межами параметрів за замовчуванням: додати власний `middleware`, налаштувати складнішу маршрутизацію чи задати власні директиви. Докладніше про синтаксис Caddyfile і параметри конфігурації дивіться в [офіційній документації Caddy](https://caddyserver.com/docs/caddyfile).

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev) працює на бінарнику RoadRunner, написаному на Go. Під час першого запуску сервера Octane на базі RoadRunner Octane запропонує завантажити й установити бінарник RoadRunner за вас.

<a name="roadrunner-via-laravel-sail"></a>
#### RoadRunner через Laravel Sail

Якщо ви плануєте розробляти застосунок за допомогою [Laravel Sail](/docs/{{version}}/sail), виконайте такі команди, щоб установити Octane і RoadRunner:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

Далі запустіть оболонку Sail і скористайтеся виконуваним файлом `rr`, щоб отримати останню Linux-збірку бінарника RoadRunner:

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

Потім додайте змінну оточення `SUPERVISOR_PHP_COMMAND` до визначення сервісу `laravel.test` у файлі `docker-compose.yml` вашого застосунку. Ця змінна оточення міститиме команду, якою Sail обслуговуватиме ваш застосунок через Octane замість девсервера PHP:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

Насамкінець переконайтеся, що бінарник `rr` є виконуваним, і зберіть свої образи Sail:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Якщо ви плануєте використовувати сервер застосунків Swoole для обслуговування вашого застосунку на Laravel Octane, вам потрібно встановити PHP-розширення Swoole. Зазвичай це робиться через PECL:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Якщо ви хочете використовувати сервер застосунків Open Swoole для обслуговування вашого застосунку на Laravel Octane, вам потрібно встановити PHP-розширення Open Swoole. Зазвичай це робиться через PECL:

```shell
pecl install openswoole
```

Використання Laravel Octane з Open Swoole дає ту саму функціональність, що й Swoole: паралельні завдання, тіки та інтервали.

<a name="swoole-via-laravel-sail"></a>
#### Swoole через Laravel Sail

> [!WARNING]
> Перш ніж обслуговувати застосунок на Octane через Sail, переконайтеся, що у вас остання версія Laravel Sail, і виконайте `./vendor/bin/sail build --no-cache` у кореневому каталозі вашого застосунку.

Як альтернативу ви можете розробляти свій застосунок на Octane зі Swoole за допомогою [Laravel Sail](/docs/{{version}}/sail) - офіційного середовища розробки Laravel на базі Docker. Laravel Sail містить розширення Swoole за замовчуванням. Однак вам усе одно потрібно буде підправити файл `docker-compose.yml`, який використовує Sail.

Для початку додайте змінну оточення `SUPERVISOR_PHP_COMMAND` до визначення сервісу `laravel.test` у файлі `docker-compose.yml` вашого застосунку. Ця змінна оточення міститиме команду, якою Sail обслуговуватиме ваш застосунок через Octane замість девсервера PHP:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

Насамкінець зберіть свої образи Sail:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Конфігурація Swoole

Swoole підтримує кілька додаткових параметрів конфігурації, які ви можете за потреби додати до свого конфігураційного файлу `octane`. Оскільки їх рідко доводиться змінювати, у файлі конфігурації за замовчуванням їх немає:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## Обслуговування вашого застосунку

Сервер Octane запускається артизан-командою `octane:start`. За замовчуванням ця команда використовуватиме сервер, указаний у параметрі конфігурації `server` вашого конфігураційного файлу `octane`:

```shell
php artisan octane:start
```

За замовчуванням Octane запустить сервер на порту 8000, тож ви зможете відкрити свій застосунок у браузері за адресою `http://localhost:8000`.

<a name="keeping-octane-running-in-production"></a>
#### Підтримання роботи Octane у продакшені

Якщо ви розгортаєте свій застосунок на Octane у продакшені, вам слід використовувати монітор процесів на кшталт Supervisor, щоб сервер Octane продовжував працювати. Приклад конфігураційного файлу Supervisor для Octane може виглядати так:

```ini
[program:octane]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/example.com/artisan octane:start --server=frankenphp --host=127.0.0.1 --port=8000
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/storage/logs/octane.log
stopwaitsecs=3600
```

<a name="serving-your-application-via-https"></a>
### Обслуговування застосунку через HTTPS

За замовчуванням застосунки, що працюють через Octane, генерують посилання з префіксом `http://`. Змінну оточення `OCTANE_HTTPS`, яка використовується в конфігураційному файлі `config/octane.php` вашого застосунку, можна встановити в `true`, коли ви обслуговуєте застосунок через HTTPS. Коли це значення конфігурації дорівнює `true`, Octane вкаже Laravel додавати до всіх згенерованих посилань префікс `https://`:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Обслуговування застосунку через Nginx

> [!NOTE]
> Якщо ви ще не готові керувати власною конфігурацією сервера або не почуваєтеся впевнено, налаштовуючи всі різноманітні сервіси, потрібні для роботи надійного застосунку на Laravel Octane, погляньте на [Laravel Cloud](https://cloud.laravel.com), який пропонує повністю керовану підтримку Laravel Octane.

У продакшен-середовищах вам слід обслуговувати застосунок на Octane за традиційним вебсервером на кшталт Nginx чи Apache. Це дозволить вебсерверу віддавати ваші статичні ассети, як-от зображення та стилі, а також керувати термінацією вашого SSL-сертифіката.

У наведеному нижче прикладі конфігурації Nginx віддаватиме статичні ассети сайту й проксіюватиме запити до сервера Octane, що працює на порту 8000:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen [::]:80;
    server_name domain.com;
    server_tokens off;
    root /home/forge/domain.com/public;

    index index.php;

    charset utf-8;

    location /index.php {
        try_files /not_exists @octane;
    }

    location / {
        try_files $uri $uri/ @octane;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    access_log off;
    error_log  /var/log/nginx/domain.com-error.log error;

    error_page 404 /index.php;

    location @octane {
        set $suffix "";

        if ($uri = /index.php) {
            set $suffix ?$query_string;
        }

        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://127.0.0.1:8000$suffix;
    }
}
```

<a name="watching-for-file-changes"></a>
### Відстеження змін у файлах

Оскільки ваш застосунок завантажується в пам'ять один раз під час запуску сервера Octane, будь-які зміни у файлах застосунку не з'являться, коли ви оновите сторінку у браузері. Наприклад, визначення маршрутів, додані до файлу `routes/web.php`, не діятимуть, доки сервер не буде перезапущено. Для зручності ви можете скористатися прапорцем `--watch`, щоб Octane автоматично перезапускав сервер за будь-яких змін у файлах вашого застосунку:

```shell
php artisan octane:start --watch
```

Перш ніж скористатися цією можливістю, переконайтеся, що у вашому локальному середовищі розробки встановлено [Node](https://nodejs.org). Крім того, вам слід установити у своєму проєкті бібліотеку відстеження файлів [Chokidar](https://github.com/paulmillr/chokidar):

```shell
npm install --save-dev chokidar
```

Налаштувати каталоги та файли, які слід відстежувати, можна за допомогою параметра конфігурації `watch` у конфігураційному файлі `config/octane.php` вашого застосунку.

<a name="specifying-the-worker-count"></a>
### Визначення кількості воркерів

За замовчуванням Octane запустить по одному воркеру запитів застосунку на кожне ядро процесора вашої машини. Ці воркери потім використовуватимуться для обслуговування вхідних HTTP-запитів, що надходять до вашого застосунку. Ви можете вручну вказати, скільки воркерів запускати, за допомогою опції `--workers` під час виклику команди `octane:start`:

```shell
php artisan octane:start --workers=4
```

Якщо ви використовуєте сервер застосунків Swoole, ви також можете вказати, скільки [«воркерів завдань»](#concurrent-tasks) слід запустити:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### Визначення максимальної кількості запитів

Щоб запобігти випадковим витокам пам'яті, Octane коректно перезапускає кожного воркера після того, як той обробив 500 запитів. Змінити це число можна за допомогою опції `--max-requests`:

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
### Визначення максимального часу виконання

За замовчуванням Laravel Octane встановлює максимальний час виконання вхідних запитів у 30 секунд через параметр `max_execution_time` у конфігураційному файлі `config/octane.php` вашого застосунку:

```php
'max_execution_time' => 30,
```

Це налаштування визначає максимальну кількість секунд, протягом яких вхідному запиту дозволено виконуватися, перш ніж його буде припинено. Значення `0` повністю вимикає обмеження часу виконання. Цей параметр конфігурації особливо корисний для застосунків, які обробляють довготривалі запити: завантаження файлів, обробку даних чи API-виклики до зовнішніх сервісів.

> [!WARNING]
> Змінивши конфігурацію `max_execution_time`, ви маєте перезапустити сервер Octane, щоб зміни набули чинності.

<a name="reloading-the-workers"></a>
### Перезавантаження воркерів

Ви можете коректно перезапустити воркери застосунку на сервері Octane командою `octane:reload`. Зазвичай це слід робити після розгортання, щоб щойно розгорнутий код завантажився в пам'ять і використовувався для обслуговування наступних запитів:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### Зупинка сервера

Зупинити сервер Octane можна артизан-командою `octane:stop`:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### Перевірка стану сервера

Перевірити поточний стан сервера Octane можна артизан-командою `octane:status`:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## Впровадження залежностей і Octane

Оскільки Octane завантажує ваш застосунок один раз і тримає його в пам'яті, обслуговуючи запити, під час розробки застосунку варто врахувати кілька застережень. Наприклад, методи `register` і `boot` сервіс-провайдерів вашого застосунку будуть виконані лише один раз, коли воркер запитів початково завантажується. На наступних запитах повторно використовуватиметься той самий екземпляр застосунку.

З огляду на це, будьте особливо обережні, впроваджуючи сервіс-контейнер застосунку чи запит до конструктора будь-якого об'єкта. Так цей об'єкт може мати застарілу версію контейнера чи запиту на наступних запитах.

Octane автоматично скидає між запитами будь-який стан самого фреймворку. Однак Octane не завжди знає, як скинути глобальний стан, створений вашим застосунком. Тому вам варто розуміти, як будувати застосунок так, щоб він дружив з Octane. Нижче ми розглянемо найпоширеніші ситуації, які можуть спричинити проблеми під час використання Octane.

<a name="container-injection"></a>
### Впровадження контейнера

Загалом вам слід уникати впровадження сервіс-контейнера застосунку чи екземпляра HTTP-запиту до конструкторів інших об'єктів. Наприклад, наступна прив'язка впроваджує весь сервіс-контейнер застосунку в об'єкт, прив'язаний як синглтон:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app);
    });
}
```

У цьому прикладі, якщо екземпляр `Service` буде створено під час завантаження застосунку, контейнер буде впроваджено в сервіс, і той самий контейнер утримуватиметься екземпляром `Service` на наступних запитах. Для вашого конкретного застосунку це **може** й не бути проблемою; однак це може призвести до того, що в контейнері несподівано бракуватиме прив'язок, доданих пізніше в циклі завантаження або наступним запитом.

Як обхідний шлях ви можете або перестати реєструвати прив'язку як синглтон, або впровадити в сервіс замикання-резолвер контейнера, яке завжди повертає поточний екземпляр контейнера:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

Глобальний хелпер `app` і метод `Container::getInstance()` завжди повертатимуть найновішу версію контейнера застосунку.

<a name="request-injection"></a>
### Впровадження запиту

Загалом вам слід уникати впровадження сервіс-контейнера застосунку чи екземпляра HTTP-запиту до конструкторів інших об'єктів. Наприклад, наступна прив'язка впроваджує весь екземпляр запиту в об'єкт, прив'язаний як синглтон:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app['request']);
    });
}
```

У цьому прикладі, якщо екземпляр `Service` буде створено під час завантаження застосунку, HTTP-запит буде впроваджено в сервіс, і той самий запит утримуватиметься екземпляром `Service` на наступних запитах. Тому всі заголовки, вхідні дані й дані рядка запиту будуть неправильними, як і решта даних запиту.

Як обхідний шлях ви можете або перестати реєструвати прив'язку як синглтон, або впровадити в сервіс замикання-резолвер запиту, яке завжди повертає поточний екземпляр запиту. Або ж - і це найбільш рекомендований підхід - просто передавати потрібну вашому об'єкту конкретну інформацію із запиту до одного з методів об'єкта під час виконання:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// Or...

$service->method($request->input('name'));
```

Глобальний хелпер `request` завжди повертатиме запит, який застосунок обробляє зараз, тому його безпечно використовувати у вашому застосунку.

> [!WARNING]
> Вказувати тип `Illuminate\Http\Request` у методах контролерів і замиканнях маршрутів цілком припустимо.

<a name="configuration-repository-injection"></a>
### Впровадження репозиторію конфігурації

Загалом вам слід уникати впровадження екземпляра репозиторію конфігурації до конструкторів інших об'єктів. Наприклад, наступна прив'язка впроваджує репозиторій конфігурації в об'єкт, прив'язаний як синглтон:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app->make('config'));
    });
}
```

У цьому прикладі, якщо значення конфігурації зміняться між запитами, цей сервіс не матиме доступу до нових значень, бо залежить від початкового екземпляра репозиторію.

Як обхідний шлях ви можете або перестати реєструвати прив'язку як синглтон, або впровадити в клас замикання-резолвер репозиторію конфігурації:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

Глобальний `config` завжди повертатиме найновішу версію репозиторію конфігурації, тому його безпечно використовувати у вашому застосунку.

<a name="managing-memory-leaks"></a>
### Керування витоками пам'яті

Пам'ятайте: Octane тримає ваш застосунок у пам'яті між запитами, тож додавання даних до статичного масиву призведе до витоку пам'яті. Наприклад, у наведеному нижче контролері є витік пам'яті, бо кожен запит до застосунку й далі додаватиме дані до статичного масиву `$data`:

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 */
public function index(Request $request): array
{
    Service::$data[] = Str::random(10);

    return [
        // ...
    ];
}
```

Розробляючи застосунок, будьте особливо уважні, щоб не створювати таких витоків пам'яті. Рекомендуємо стежити за споживанням пам'яті вашим застосунком під час локальної розробки, аби переконатися, що ви не додаєте нових витоків пам'яті до свого застосунку.

<a name="concurrent-tasks"></a>
## Паралельні завдання

> [!WARNING]
> Ця можливість потребує [Swoole](#swoole).

Використовуючи Swoole, ви можете виконувати операції паралельно за допомогою легких фонових завдань. Зробити це можна методом `concurrently` в Octane. Ви можете поєднати цей метод з деструктуризацією масивів PHP, щоб отримати результати кожної операції:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Паралельні завдання, які обробляє Octane, використовують «воркери завдань» Swoole і виконуються в зовсім іншому процесі, ніж вхідний запит. Кількість воркерів, доступних для обробки паралельних завдань, визначається директивою `--task-workers` команди `octane:start`:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

Викликаючи метод `concurrently`, не передавайте понад 1024 завдання - через обмеження, накладені системою завдань Swoole.

<a name="ticks-and-intervals"></a>
## Тіки та інтервали

> [!WARNING]
> Ця можливість потребує [Swoole](#swoole).

Використовуючи Swoole, ви можете зареєструвати операції-«тіки», які виконуватимуться кожні задані кілька секунд. Зареєструвати колбеки «тіків» можна методом `tick`. Першим аргументом методу `tick` має бути рядок з іменем тікера. Другим аргументом має бути callable, який викликатиметься із заданим інтервалом.

У цьому прикладі ми зареєструємо замикання, яке викликатиметься кожні 10 секунд. Зазвичай метод `tick` слід викликати в методі `boot` одного з сервіс-провайдерів вашого застосунку:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

За допомогою методу `immediate` ви можете вказати Octane викликати колбек тіка одразу під час початкового завантаження сервера Octane, а далі кожні N секунд:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Кеш Octane

> [!WARNING]
> Ця можливість потребує [Swoole](#swoole).

Використовуючи Swoole, ви можете скористатися драйвером кешу Octane, який дає швидкість читання й запису до 2 мільйонів операцій за секунду. Тому цей драйвер кешу - чудовий вибір для застосунків, яким потрібна екстремальна швидкість читання / запису від шару кешування.

Цей драйвер кешу працює на [таблицях Swoole](https://www.swoole.co.uk/docs/modules/swoole-table). Усі дані, збережені в кеші, доступні всім воркерам на сервері. Однак закешовані дані буде очищено під час перезапуску сервера:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Максимальну кількість записів, дозволену в кеші Octane, можна визначити в конфігураційному файлі `octane` вашого застосунку.

<a name="cache-intervals"></a>
### Інтервали кешу

Окрім звичних методів, які надає система кешування Laravel, драйвер кешу Octane пропонує кеші на основі інтервалів. Ці кеші автоматично оновлюються із заданим інтервалом і мають реєструватися в методі `boot` одного з сервіс-провайдерів вашого застосунку. Наприклад, наведений нижче кеш оновлюватиметься кожні п'ять секунд:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## Таблиці

> [!WARNING]
> Ця можливість потребує [Swoole](#swoole).

Використовуючи Swoole, ви можете визначати власні довільні [таблиці Swoole](https://www.swoole.co.uk/docs/modules/swoole-table) і працювати з ними. Таблиці Swoole дають екстремальну пропускну здатність, і дані в цих таблицях доступні всім воркерам на сервері. Однак дані в них буде втрачено під час перезапуску сервера.

Таблиці слід визначати в масиві конфігурації `tables` вашого конфігураційного файлу `octane`. Приклад таблиці, яка допускає максимум 1000 рядків, уже налаштований для вас. Максимальний розмір рядкових колонок можна задати, вказавши розмір колонки після її типу, як показано нижче:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

Щоб звернутися до таблиці, скористайтеся методом `Octane::table`:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Таблиці Swoole підтримують такі типи колонок: `string`, `int` і `float`.

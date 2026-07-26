---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Homestead

- [Вступ](#introduction)
- [Встановлення й налаштування](#installation-and-setup)
    - [Перші кроки](#first-steps)
    - [Налаштування Homestead](#configuring-homestead)
    - [Налаштування сайтів Nginx](#configuring-nginx-sites)
    - [Налаштування сервісів](#configuring-services)
    - [Запуск Vagrant-боксу](#launching-the-vagrant-box)
    - [Встановлення для окремого проєкту](#per-project-installation)
    - [Встановлення додаткового ПЗ](#installing-optional-features)
    - [Аліаси](#aliases)
- [Оновлення Homestead](#updating-homestead)
- [Щоденне використання](#daily-usage)
    - [Підключення через SSH](#connecting-via-ssh)
    - [Додавання нових сайтів](#adding-additional-sites)
    - [Змінні оточення](#environment-variables)
    - [Порти](#ports)
    - [Версії PHP](#php-versions)
    - [Підключення до баз даних](#connecting-to-databases)
    - [Резервні копії бази даних](#database-backups)
    - [Налаштування розкладу cron](#configuring-cron-schedules)
    - [Налаштування Mailpit](#configuring-mailpit)
    - [Налаштування Minio](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [Спільний доступ до вашого середовища](#sharing-your-environment)
- [Налагодження та профілювання](#debugging-and-profiling)
    - [Налагодження вебзапитів за допомогою Xdebug](#debugging-web-requests)
    - [Налагодження CLI-застосунків](#debugging-cli-applications)
    - [Профілювання застосунків за допомогою Blackfire](#profiling-applications-with-blackfire)
- [Мережеві інтерфейси](#network-interfaces)
- [Розширення Homestead](#extending-homestead)
- [Налаштування, специфічні для провайдера](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## Вступ

> [!WARNING]
> Laravel Homestead - це застарілий пакет, який більше активно не підтримується. Як сучасну альтернативу можна використати [Laravel Sail](/docs/{{version}}/sail).

Laravel прагне зробити приємним увесь досвід розробки на PHP, включно з вашим локальним середовищем розробки. [Laravel Homestead](https://github.com/laravel/homestead) - це офіційний, заздалегідь зібраний Vagrant-бокс, який дає вам чудове середовище розробки, не вимагаючи встановлювати PHP, вебсервер чи будь-яке інше серверне ПЗ на вашу локальну машину.

[Vagrant](https://www.vagrantup.com) дає простий та елегантний спосіб керувати віртуальними машинами й розгортати їх. Vagrant-бокси повністю одноразові. Якщо щось піде не так, ви можете знищити й перестворити бокс за кілька хвилин!

Homestead працює на будь-якій системі Windows, macOS чи Linux і містить Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node і все інше ПЗ, потрібне для розробки чудових Laravel-застосунків.

> [!WARNING]
> Якщо ви користуєтеся Windows, вам може знадобитися увімкнути апаратну віртуалізацію (VT-x). Зазвичай це можна зробити через BIOS. Якщо ви використовуєте Hyper-V в UEFI-системі, вам, можливо, також доведеться вимкнути Hyper-V, щоб отримати доступ до VT-x.

<a name="included-software"></a>
### Включене ПЗ

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- Ubuntu 22.04
- Git
- PHP 8.3
- PHP 8.2
- PHP 8.1
- PHP 8.0
- PHP 7.4
- PHP 7.3
- PHP 7.2
- PHP 7.1
- PHP 7.0
- PHP 5.6
- Nginx
- MySQL 8.0
- lmm
- Sqlite3
- PostgreSQL 15
- Composer
- Docker
- Node (With Yarn, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- Mailpit
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli

</div>

<a name="optional-software"></a>
### Додаткове ПЗ

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- Apache
- Blackfire
- Cassandra
- Chronograf
- CouchDB
- Crystal & Lucky Framework
- Elasticsearch
- EventStoreDB
- Flyway
- Gearman
- Go
- Grafana
- InfluxDB
- Logstash
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python
- R
- RabbitMQ
- Rust
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP extension)</small>
- Webdriver & Laravel Dusk Utilities

</div>

<a name="installation-and-setup"></a>
## Встановлення й налаштування

<a name="first-steps"></a>
### Перші кроки

Перш ніж запускати середовище Homestead, вам потрібно встановити [Vagrant](https://developer.hashicorp.com/vagrant/downloads), а також один із таких підтримуваних провайдерів:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

Усі ці програмні пакети мають прості візуальні інсталятори для всіх популярних операційних систем.

Щоб скористатися провайдером Parallels, вам потрібно встановити [плагін Parallels для Vagrant](https://github.com/Parallels/vagrant-parallels). Він безкоштовний.

<a name="installing-homestead"></a>
#### Встановлення Homestead

Встановити Homestead можна, склонувавши репозиторій Homestead на вашу хост-машину. Варто склонувати репозиторій у теку `Homestead` у вашому «домашньому» каталозі, адже віртуальна машина Homestead буде хостом для всіх ваших Laravel-застосунків. У цій документації ми називатимемо цей каталог вашим «каталогом Homestead»:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Склонувавши репозиторій Laravel Homestead, вам слід перейти на гілку `release`. Ця гілка завжди містить останній стабільний випуск Homestead:

```shell
cd ~/Homestead

git checkout release
```

Далі виконайте команду `bash init.sh` з каталогу Homestead, щоб створити конфігураційний файл `Homestead.yaml`. У файлі `Homestead.yaml` ви налаштовуватимете всі параметри своєї інсталяції Homestead. Цей файл буде розміщено в каталозі Homestead:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Налаштування Homestead

<a name="setting-your-provider"></a>
#### Вибір провайдера

Ключ `provider` у вашому файлі `Homestead.yaml` вказує, який провайдер Vagrant слід використовувати: `virtualbox` чи `parallels`:

    provider: virtualbox

> [!WARNING]
> Якщо ви користуєтеся Apple Silicon, потрібен провайдер Parallels.

<a name="configuring-shared-folders"></a>
#### Налаштування спільних тек

Властивість `folders` файлу `Homestead.yaml` перелічує всі теки, якими ви хочете поділитися зі своїм середовищем Homestead. Коли файли в цих теках змінюються, вони синхронізуватимуться між вашою локальною машиною та віртуальним середовищем Homestead. Ви можете налаштувати скільки завгодно спільних тек:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Користувачам Windows не варто використовувати синтаксис шляху `~/`, натомість слід указувати повний шлях до свого проєкту, наприклад `C:\Users\user\Code\project1`.

Вам завжди слід зіставляти окремі застосунки з власними теками, а не мапити один великий каталог, що містить усі ваші застосунки. Коли ви мапите теку, віртуальна машина має відстежувати весь дисковий ввід-вивід для *кожного* файлу в цій теці. Якщо у теці багато файлів, ви можете зіткнутися зі зниженою продуктивністю:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Ніколи не монтуйте `.` (поточний каталог), використовуючи Homestead. Через це Vagrant не змапить поточну теку до `/vagrant`, що зламає додаткові можливості й призведе до несподіваних результатів під час розгортання.

Щоб увімкнути [NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs), додайте до свого мапінгу теки опцію `type`:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Використовуючи NFS у Windows, варто розглянути встановлення плагіна [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd). Цей плагін підтримуватиме правильні дозволи користувача / групи для файлів і каталогів усередині віртуальної машини Homestead.

Ви також можете передати будь-які опції, які підтримують [синхронізовані теки](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) Vagrant, перелічивши їх під ключем `options`:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "rsync"
      options:
          rsync__args: ["--verbose", "--archive", "--delete", "-zz"]
          rsync__exclude: ["node_modules"]
```

<a name="configuring-nginx-sites"></a>
### Налаштування сайтів Nginx

Не знайомі з Nginx? Не біда. Властивість `sites` вашого файлу `Homestead.yaml` дозволяє легко змапити «домен» на теку у вашому середовищі Homestead. Приклад конфігурації сайту є у файлі `Homestead.yaml`. Знову ж таки, ви можете додати до свого середовища Homestead скільки завгодно сайтів. Homestead може бути зручним віртуалізованим середовищем для кожного Laravel-застосунку, над яким ви працюєте:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

Якщо ви зміните властивість `sites` після розгортання віртуальної машини Homestead, виконайте в терміналі команду `vagrant reload --provision`, щоб оновити конфігурацію Nginx на віртуальній машині.

> [!WARNING]
> Скрипти Homestead написані так, щоб бути максимально ідемпотентними. Однак, якщо ви стикаєтеся з проблемами під час розгортання, знищте й перезберіть машину командою `vagrant destroy && vagrant up`.

<a name="hostname-resolution"></a>
#### Резолвінг імен хостів

Homestead публікує імена хостів через `mDNS` для автоматичного резолвінгу хостів. Якщо ви встановите `hostname: homestead` у файлі `Homestead.yaml`, хост буде доступний за адресою `homestead.local`. macOS, iOS і десктопні дистрибутиви Linux підтримують `mDNS` за замовчуванням. Якщо ви користуєтеся Windows, вам потрібно встановити [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US).

Автоматичні імена хостів найкраще працюють для [встановлення для окремого проєкту](#per-project-installation). Якщо ви хостите кілька сайтів на одному екземплярі Homestead, ви можете додати «домени» ваших вебсайтів до файлу `hosts` на своїй машині. Файл `hosts` перенаправлятиме запити до ваших сайтів Homestead у вашу віртуальну машину Homestead. У macOS і Linux цей файл розташований у `/etc/hosts`. У Windows - у `C:\Windows\System32\drivers\etc\hosts`. Рядки, які ви додаєте до цього файлу, виглядатимуть так:

```text
192.168.56.56  homestead.test
```

Переконайтеся, що вказана IP-адреса - це та, яку задано у вашому файлі `Homestead.yaml`. Щойно ви додасте домен до файлу `hosts` і запустите Vagrant-бокс, ви зможете відкрити сайт у своєму браузері:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### Налаштування сервісів

Homestead запускає кілька сервісів за замовчуванням; однак ви можете налаштувати, які сервіси вмикати чи вимикати під час розгортання. Наприклад, ви можете увімкнути PostgreSQL і вимкнути MySQL, змінивши опцію `services` у своєму файлі `Homestead.yaml`:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

Указані сервіси буде запущено чи зупинено відповідно до їхнього порядку в директивах `enabled` і `disabled`.

<a name="launching-the-vagrant-box"></a>
### Запуск Vagrant-боксу

Щойно ви відредагуєте `Homestead.yaml` на свій смак, виконайте команду `vagrant up` зі свого каталогу Homestead. Vagrant завантажить віртуальну машину й автоматично налаштує ваші спільні теки та сайти Nginx.

Щоб знищити машину, скористайтеся командою `vagrant destroy`.

<a name="per-project-installation"></a>
### Встановлення для окремого проєкту

Замість встановлювати Homestead глобально й ділити ту саму віртуальну машину Homestead між усіма своїми проєктами, ви можете налаштувати окремий екземпляр Homestead для кожного проєкту, яким керуєте. Встановлення Homestead для окремого проєкту може бути корисним, якщо ви хочете постачати `Vagrantfile` разом зі своїм проєктом, щоб інші учасники проєкту могли виконати `vagrant up` одразу після клонування репозиторію проєкту.

Встановити Homestead у свій проєкт можна за допомогою менеджера пакетів Composer:

```shell
composer require laravel/homestead --dev
```

Щойно Homestead буде встановлено, викличте команду `make` з Homestead, щоб згенерувати `Vagrantfile` і файл `Homestead.yaml` для вашого проєкту. Ці файли буде розміщено в корені вашого проєкту. Команда `make` автоматично налаштує директиви `sites` і `folders` у файлі `Homestead.yaml`:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

Далі виконайте в терміналі команду `vagrant up` і відкрийте свій проєкт за адресою `http://homestead.test` у браузері. Пам'ятайте: вам усе одно потрібно буде додати запис для `homestead.test` (чи для обраного вами домену) до файлу `/etc/hosts`, якщо ви не користуєтеся автоматичним [резолвінгом імен хостів](#hostname-resolution).

<a name="installing-optional-features"></a>
### Встановлення додаткового ПЗ

Додаткове ПЗ встановлюється через опцію `features` у вашому файлі `Homestead.yaml`. Більшість можливостей вмикаються чи вимикаються булевим значенням, а деякі допускають кілька параметрів конфігурації:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
    - cassandra: true
    - chronograf: true
    - couchdb: true
    - crystal: true
    - dragonflydb: true
    - elasticsearch:
        version: 7.9.0
    - eventstore: true
        version: 21.2.0
    - flyway: true
    - gearman: true
    - golang: true
    - grafana: true
    - influxdb: true
    - logstash: true
    - mariadb: true
    - meilisearch: true
    - minio: true
    - mongodb: true
    - neo4j: true
    - ohmyzsh: true
    - openresty: true
    - pm2: true
    - python: true
    - r-base: true
    - rabbitmq: true
    - rustc: true
    - rvm: true
    - solr: true
    - timescaledb: true
    - trader: true
    - webdriver: true
```

<a name="elasticsearch"></a>
#### Elasticsearch

Ви можете вказати підтримувану версію Elasticsearch, яка має бути точним номером версії (major.minor.patch). Встановлення за замовчуванням створить кластер з іменем 'homestead'. Ніколи не віддавайте Elasticsearch більше ніж половину пам'яті операційної системи, тож переконайтеся, що ваша віртуальна машина Homestead має щонайменше вдвічі більше пам'яті, ніж виділено Elasticsearch.

> [!NOTE]
> Загляньте в [документацію Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current), щоб дізнатися, як налаштувати конфігурацію.

<a name="mariadb"></a>
#### MariaDB

Увімкнення MariaDB прибере MySQL і встановить MariaDB. MariaDB зазвичай є прямою заміною MySQL, тож у конфігурації бази даних вашого застосунку вам слід і далі використовувати драйвер бази даних `mysql`.

<a name="mongodb"></a>
#### MongoDB

Встановлення MongoDB за замовчуванням встановить ім'я користувача бази даних `homestead`, а відповідний пароль - `secret`.

<a name="neo4j"></a>
#### Neo4j

Встановлення Neo4j за замовчуванням встановить ім'я користувача бази даних `homestead`, а відповідний пароль - `secret`. Щоб відкрити браузер Neo4j, перейдіть за адресою `http://homestead.test:7474` у своєму вебпереглядачі. Порти `7687` (Bolt), `7474` (HTTP) і `7473` (HTTPS) готові обслуговувати запити від клієнта Neo4j.

<a name="aliases"></a>
### Аліаси

Ви можете додати Bash-аліаси до своєї віртуальної машини Homestead, змінивши файл `aliases` у своєму каталозі Homestead:

```shell
alias c='clear'
alias ..='cd ..'
```

Після оновлення файлу `aliases` вам слід перерозгорнути віртуальну машину Homestead командою `vagrant reload --provision`. Це гарантує, що ваші нові аліаси будуть доступні на машині.

<a name="updating-homestead"></a>
## Оновлення Homestead

Перш ніж починати оновлення Homestead, переконайтеся, що ви прибрали свою поточну віртуальну машину, виконавши таку команду у своєму каталозі Homestead:

```shell
vagrant destroy
```

Далі вам потрібно оновити вихідний код Homestead. Якщо ви клонували репозиторій, виконайте такі команди там, де ви його спочатку склонували:

```shell
git fetch

git pull origin release
```

Ці команди підтягують останній код Homestead з репозиторію GitHub, отримують останні теги, а потім переходять на останній тегований випуск. Останню стабільну версію можна знайти на [сторінці випусків Homestead на GitHub](https://github.com/laravel/homestead/releases).

Якщо ви встановили Homestead через файл `composer.json` свого проєкту, переконайтеся, що ваш файл `composer.json` містить `"laravel/homestead": "^12"`, і оновіть залежності:

```shell
composer update
```

Далі вам слід оновити Vagrant-бокс командою `vagrant box update`:

```shell
vagrant box update
```

Після оновлення Vagrant-боксу виконайте команду `bash init.sh` з каталогу Homestead, щоб оновити додаткові конфігураційні файли Homestead. Вас запитають, чи хочете ви перезаписати наявні файли `Homestead.yaml`, `after.sh` і `aliases`:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

Насамкінець вам потрібно буде перестворити свою віртуальну машину Homestead, щоб скористатися останньою інсталяцією Vagrant:

```shell
vagrant up
```

<a name="daily-usage"></a>
## Щоденне використання

<a name="connecting-via-ssh"></a>
### Підключення через SSH

Ви можете підключитися до своєї віртуальної машини через SSH, виконавши в терміналі команду `vagrant ssh` зі свого каталогу Homestead.

<a name="adding-additional-sites"></a>
### Додавання нових сайтів

Щойно ваше середовище Homestead розгорнуто й працює, ви можете захотіти додати нові сайти Nginx для інших своїх Laravel-проєктів. В одному середовищі Homestead можна запускати скільки завгодно Laravel-проєктів. Щоб додати новий сайт, додайте його до свого файлу `Homestead.yaml`.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> Перш ніж додавати сайт, переконайтеся, що ви налаштували [мапінг теки](#configuring-shared-folders) для каталогу проєкту.

Якщо Vagrant не керує вашим файлом «hosts» автоматично, вам, можливо, доведеться додати новий сайт і до цього файлу. У macOS і Linux цей файл розташований у `/etc/hosts`. У Windows - у `C:\Windows\System32\drivers\etc\hosts`:

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

Щойно сайт буде додано, виконайте в терміналі команду `vagrant reload --provision` зі свого каталогу Homestead.

<a name="site-types"></a>
#### Типи сайтів

Homestead підтримує кілька «типів» сайтів, що дозволяє легко запускати проєкти, не засновані на Laravel. Наприклад, ми можемо легко додати до Homestead застосунок Statamic, скориставшись типом сайту `statamic`:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

Доступні типи сайтів: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (за замовчуванням), `proxy` (для nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4` і `zf`.

<a name="site-parameters"></a>
#### Параметри сайту

Ви можете додати до свого сайту додаткові значення `fastcgi_param` для Nginx через директиву сайту `params`:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### Змінні оточення

Ви можете визначити глобальні змінні оточення, додавши їх до свого файлу `Homestead.yaml`:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

Після оновлення файлу `Homestead.yaml` обов'язково перерозгорніть машину командою `vagrant reload --provision`. Це оновить конфігурацію PHP-FPM для всіх встановлених версій PHP, а також оновить оточення для користувача `vagrant`.

<a name="ports"></a>
### Порти

За замовчуванням до вашого середовища Homestead прокидаються такі порти:

<div class="content-list" markdown="1">

- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443

</div>

<a name="forwarding-additional-ports"></a>
#### Прокидання додаткових портів

За бажанням ви можете прокинути до Vagrant-боксу додаткові порти, визначивши запис конфігурації `ports` у своєму файлі `Homestead.yaml`. Після оновлення файлу `Homestead.yaml` обов'язково перерозгорніть машину командою `vagrant reload --provision`:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

Нижче наведено список додаткових портів сервісів Homestead, які ви можете захотіти змапити зі своєї хост-машини на Vagrant-бокс:

<div class="content-list" markdown="1">

- **SSH:** 2222 &rarr; To 22
- **ngrok UI:** 4040 &rarr; To 4040
- **MySQL:** 33060 &rarr; To 3306
- **PostgreSQL:** 54320 &rarr; To 5432
- **MongoDB:** 27017 &rarr; To 27017
- **Mailpit:** 8025 &rarr; To 8025
- **Minio:** 9600 &rarr; To 9600

</div>

<a name="php-versions"></a>
### Версії PHP

Homestead підтримує роботу кількох версій PHP на одній віртуальній машині. Ви можете вказати, яку версію PHP використовувати для конкретного сайту, у своєму файлі `Homestead.yaml`. Доступні версії PHP: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2" і "8.3" (за замовчуванням):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Усередині вашої віртуальної машини Homestead](#connecting-via-ssh) ви можете використовувати будь-яку з підтримуваних версій PHP через CLI:

```shell
php5.6 artisan list
php7.0 artisan list
php7.1 artisan list
php7.2 artisan list
php7.3 artisan list
php7.4 artisan list
php8.0 artisan list
php8.1 artisan list
php8.2 artisan list
php8.3 artisan list
```

Ви можете змінити версію PHP за замовчуванням, яку використовує CLI, виконавши такі команди всередині своєї віртуальної машини Homestead:

```shell
php56
php70
php71
php72
php73
php74
php80
php81
php82
php83
```

<a name="connecting-to-databases"></a>
### Підключення до баз даних

База даних `homestead` налаштована як для MySQL, так і для PostgreSQL «з коробки». Щоб підключитися до своєї бази MySQL чи PostgreSQL з клієнта бази даних на хост-машині, підключайтеся до `127.0.0.1` на порт `33060` (MySQL) чи `54320` (PostgreSQL). Ім'я користувача й пароль для обох баз - `homestead` / `secret`.

> [!WARNING]
> Ці нестандартні порти слід використовувати лише під час підключення до баз даних з вашої хост-машини. У конфігураційному файлі `database` вашого Laravel-застосунку ви використовуватимете стандартні порти 3306 і 5432, оскільки Laravel працює _всередині_ віртуальної машини.

<a name="database-backups"></a>
### Резервні копії бази даних

Homestead може автоматично створювати резервні копії вашої бази даних, коли віртуальну машину Homestead знищують. Щоб скористатися цією можливістю, вам потрібен Vagrant 2.1.0 чи новіший. Або ж, якщо у вас старіша версія Vagrant, вам потрібно встановити плагін `vagrant-triggers`. Щоб увімкнути автоматичне резервне копіювання бази даних, додайте до свого файлу `Homestead.yaml` такий рядок:

```yaml
backup: true
```

Після налаштування Homestead експортуватиме ваші бази даних до каталогів `.backup/mysql_backup` і `.backup/postgres_backup` під час виконання команди `vagrant destroy`. Ці каталоги можна знайти в теці, куди ви встановили Homestead, або в корені вашого проєкту, якщо ви користуєтеся методом [встановлення для окремого проєкту](#per-project-installation).

<a name="configuring-cron-schedules"></a>
### Налаштування розкладу cron

Laravel дає зручний спосіб [планувати cron-завдання](/docs/{{version}}/scheduling), запускаючи щохвилини єдину артизан-команду `schedule:run`. Команда `schedule:run` перегляне розклад завдань, визначений у вашому файлі `routes/console.php`, щоб з'ясувати, які заплановані завдання виконати.

Якщо ви хочете, щоб команда `schedule:run` виконувалася для сайту Homestead, встановіть опцію `schedule` в `true` під час визначення сайту:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

Cron-завдання для сайту буде визначено в каталозі `/etc/cron.d` віртуальної машини Homestead.

<a name="configuring-mailpit"></a>
### Налаштування Mailpit

[Mailpit](https://github.com/axllent/mailpit) дозволяє перехоплювати вашу вихідну пошту й переглядати її, фактично не надсилаючи листи одержувачам. Для початку оновіть файл `.env` свого застосунку, щоб використовувати такі поштові налаштування:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Щойно Mailpit буде налаштовано, ви зможете відкрити панель Mailpit за адресою `http://localhost:8025`.

<a name="configuring-minio"></a>
### Налаштування Minio

[Minio](https://github.com/minio/minio) - це сервер об'єктного сховища з відкритим кодом і API, сумісним з Amazon S3. Щоб установити Minio, оновіть свій файл `Homestead.yaml`, додавши такий параметр конфігурації до секції [features](#installing-optional-features):

    minio: true

За замовчуванням Minio доступний на порту 9600. Ви можете відкрити панель керування Minio за адресою `http://localhost:9600`. Ключ доступу за замовчуванням - `homestead`, а секретний ключ за замовчуванням - `secretkey`. Звертаючись до Minio, завжди використовуйте регіон `us-east-1`.

Щоб користуватися Minio, переконайтеся, що ваш файл `.env` містить такі опції:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Щоб створити «S3»-бакети на базі Minio, додайте до свого файлу `Homestead.yaml` директиву `buckets`. Визначивши свої бакети, виконайте в терміналі команду `vagrant reload --provision`:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

Підтримувані значення `policy`: `none`, `download`, `upload` і `public`.

<a name="laravel-dusk"></a>
### Laravel Dusk

Щоб запускати тести [Laravel Dusk](/docs/{{version}}/dusk) усередині Homestead, увімкніть [можливість webdriver](#installing-optional-features) у своїй конфігурації Homestead:

```yaml
features:
    - webdriver: true
```

Після увімкнення можливості `webdriver` виконайте в терміналі команду `vagrant reload --provision`.

<a name="sharing-your-environment"></a>
### Спільний доступ до вашого середовища

Іноді ви можете захотіти поділитися тим, над чим зараз працюєте, з колегами чи клієнтом. Vagrant має вбудовану підтримку цього через команду `vagrant share`; однак вона не працюватиме, якщо у вашому файлі `Homestead.yaml` налаштовано кілька сайтів.

Щоб розв'язати цю проблему, Homestead містить власну команду `share`. Для початку [підключіться через SSH до своєї віртуальної машини Homestead](#connecting-via-ssh) командою `vagrant ssh` і виконайте команду `share homestead.test`. Ця команда відкриє спільний доступ до сайту `homestead.test` з вашого конфігураційного файлу `Homestead.yaml`. Замість `homestead.test` ви можете підставити будь-який інший налаштований сайт:

```shell
share homestead.test
```

Після виконання команди ви побачите екран Ngrok з журналом активності та публічно доступними URL для сайту зі спільним доступом. Якщо ви хочете вказати власний регіон, піддомен чи іншу опцію виконання Ngrok, додайте їх до своєї команди `share`:

```shell
share homestead.test -region=eu -subdomain=laravel
```

Якщо вам потрібно поділитися вмістом через HTTPS, а не HTTP, скористайтеся командою `sshare` замість `share`.

> [!WARNING]
> Пам'ятайте: Vagrant за своєю природою небезпечний, і, виконуючи команду `share`, ви відкриваєте свою віртуальну машину в інтернет.

<a name="debugging-and-profiling"></a>
## Налагодження та профілювання

<a name="debugging-web-requests"></a>
### Налагодження вебзапитів за допомогою Xdebug

Homestead підтримує покрокове налагодження через [Xdebug](https://xdebug.org). Наприклад, ви можете відкрити сторінку у браузері, і PHP підключиться до вашої IDE, дозволяючи оглядати й змінювати код, що виконується.

За замовчуванням Xdebug уже запущено й готово приймати з'єднання. Якщо вам потрібно увімкнути Xdebug у CLI, виконайте команду `sudo phpenmod xdebug` усередині своєї віртуальної машини Homestead. Далі дотримуйтеся інструкцій вашої IDE, щоб увімкнути налагодження. Насамкінець налаштуйте свій браузер запускати Xdebug через розширення чи [букмарклет](https://www.jetbrains.com/phpstorm/marklets/).

> [!WARNING]
> Xdebug змушує PHP працювати значно повільніше. Щоб вимкнути Xdebug, виконайте `sudo phpdismod xdebug` усередині своєї віртуальної машини Homestead і перезапустіть сервіс FPM.

<a name="autostarting-xdebug"></a>
#### Автозапуск Xdebug

Налагоджуючи функціональні тести, які роблять запити до вебсервера, простіше запускати налагодження автоматично, ніж змінювати тести так, щоб вони передавали власний заголовок чи cookie для запуску налагодження. Щоб змусити Xdebug стартувати автоматично, змініть файл `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` усередині своєї віртуальної машини Homestead і додайте таку конфігурацію:

```ini
; If Homestead.yaml contains a different subnet for the IP address, this address may be different...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### Налагодження CLI-застосунків

Щоб налагодити PHP CLI-застосунок, скористайтеся shell-аліасом `xphp` усередині своєї віртуальної машини Homestead:

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Профілювання застосунків за допомогою Blackfire

[Blackfire](https://blackfire.io/docs/introduction) - це сервіс для профілювання вебзапитів і CLI-застосунків. Він пропонує інтерактивний інтерфейс, який показує дані профілювання у графах викликів і на часових шкалах. Його створено для використання в розробці, staging і продакшені, без накладних витрат для кінцевих користувачів. Крім того, Blackfire перевіряє продуктивність, якість і безпеку коду та налаштувань `php.ini`.

[Blackfire Player](https://blackfire.io/docs/player/index) - це застосунок з відкритим кодом для вебкраулінгу, вебтестування та вебскрапінгу, який може працювати разом з Blackfire, щоб скриптувати сценарії профілювання.

Щоб увімкнути Blackfire, скористайтеся налаштуванням «features» у своєму конфігураційному файлі Homestead:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Облікові дані сервера й клієнта Blackfire [потребують облікового запису Blackfire](https://blackfire.io/signup). Blackfire пропонує різні способи профілювати застосунок, зокрема CLI-інструмент і розширення для браузера. Будь ласка, [перегляньте документацію Blackfire, щоб дізнатися більше](https://blackfire.io/docs/php/integrations/laravel/index).

<a name="network-interfaces"></a>
## Мережеві інтерфейси

Властивість `networks` файлу `Homestead.yaml` налаштовує мережеві інтерфейси для вашої віртуальної машини Homestead. Ви можете налаштувати скільки завгодно інтерфейсів:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

Щоб увімкнути [мостовий](https://developer.hashicorp.com/vagrant/docs/networking/public_network) інтерфейс, налаштуйте параметр `bridge` для мережі й змініть тип мережі на `public_network`:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

Щоб увімкнути [DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp), просто приберіть зі своєї конфігурації опцію `ip`:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

Щоб змінити пристрій, який використовує мережа, додайте до конфігурації мережі опцію `dev`. Значення `dev` за замовчуванням - `eth0`:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Розширення Homestead

Ви можете розширити Homestead за допомогою скрипта `after.sh` у корені свого каталогу Homestead. У цьому файлі ви можете додати будь-які shell-команди, потрібні для належного налаштування вашої віртуальної машини.

Налаштовуючи Homestead, Ubuntu може запитати вас, чи хочете ви зберегти оригінальну конфігурацію пакета, чи перезаписати її новим конфігураційним файлом. Щоб уникнути цього, використовуйте під час встановлення пакетів таку команду, аби не перезаписати конфігурацію, раніше записану Homestead:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### Користувацькі налаштування

Використовуючи Homestead у команді, ви можете захотіти підлаштувати Homestead під свій особистий стиль розробки. Для цього створіть файл `user-customizations.sh` у корені свого каталогу Homestead (у тому самому каталозі, що містить ваш файл `Homestead.yaml`). У цьому файлі ви можете зробити будь-які налаштування; однак `user-customizations.sh` не слід тримати під контролем версій.

<a name="provider-specific-settings"></a>
## Налаштування, специфічні для провайдера

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

За замовчуванням Homestead встановлює налаштування `natdnshostresolver` у `on`. Це дозволяє Homestead використовувати налаштування DNS вашої хост-операційної системи. Якщо ви хочете перевизначити цю поведінку, додайте до свого файлу `Homestead.yaml` такі параметри конфігурації:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

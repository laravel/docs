# Artisan 命令列

- [介紹](#introduction)
- [撰寫命令](#writing-commands)
    - [指令結構](#command-structure)
- [指令輸入與輸出](#command-io)
    - [定義期待的輸入](#defining-input-expectations)
    - [抽取輸入](#retrieving-input)
    - [為輸入加上提示](#prompting-for-input)
    - [撰寫輸出](#writing-output)
- [註冊命令](#registering-commands)
- [使用程式碼來呼叫命令](#calling-commands-via-code)

<a name="introduction"></a>
## 介紹

Artisan 是 Laravel 裡的一個命令列介面的名稱。當你在開發你的應用程式時，它提供了許多有用的命令來幫助你開發。它是由強大的 Symfony 終端元件所驅動的。你可以使用 list 命令來列出所有可以使用的 Artisan 命令:

    php artisan list

每個命令也包含了 "幫助" 畫面，它會顯示並敘述命令可以使用的參數及選擇。只要在指令前面加上 `help` 即可顯示幫助畫面:

    php artisan help migrate

<a name="writing-commands"></a>
## 撰寫命令

除了使用 Artisan 本身所提供的命令之外，你也可以建立自己客製化的命令來為你的應用程式工作。你可以選擇將你的客製化指令儲存在`app/Console/Commands` 資料夾，只要你的命令可以藉由 `composer.json` 的設定來自動載入，你也可以自由選擇你想要放置的地方。

你可以使用 `make:console` 這個 Artisan 命令來創造新的命令，這個命令會產生一個預設的腳本來幫助你開始撰寫:

    php artisan make:console SendEmails

上面的這個命令會產生一個放置在 `app/Console/Commands/SendEmails.php` 的類別。當創造命令時， `--command` 這個選擇可以用來指定要使用的終端命令名稱:

    php artisan make:console SendEmails --command=emails:send

<a name="command-structure"></a>
### 指令結構

一旦你的命令被產生，你應該填寫類別的 `signature` 和 `description` 這兩個屬性，它們會被顯示在 `list` 畫面:

當你的命令被執行的時候 `handle` 方法會被呼叫，因此你可以將任何的命令邏輯放置在這個方法中，讓我們來看看一個範例。

注意我們可以注入任何我們需要的依賴在建構子中，Laravel [service container](/docs/{{version}}/container) 將會自動注入任何有型別提示的依賴到建構子中。為了更好的程式碼重用性，使你的終端命令輕量，並讓它們緩載到應用程式服務來完成任務是一個好習慣。

    <?php

    namespace App\Console\Commands;

    use App\User;
    use App\DripEmailer;
    use Illuminate\Console\Command;
    use Illuminate\Foundation\Inspiring;

    class Inspire extends Command
    {
        /**
         * 命令列的名字及署名
         *
         * @var string
         */
        protected $signature = 'email:send {user}';

        /**
         * 命令列的敘述
         *
         * @var string
         */
        protected $description = 'Send drip e-mails to a user';

        /**
         * 滴灌電子郵件服務
         *
         * @var DripEmailer
         */
        protected $drip;

        /**
         * 創造新的命令實例
         *
         * @param  DripEmailer  $drip
         * @return void
         */
        public function __construct(DripEmailer $drip)
        {
            parent::__construct();

            $this->drip = $drip;
        }

        /**
         * 執行命令
         *
         * @return mixed
         */
        public function handle()
        {
            $this->drip->send(User::find($this->argument('user')));
        }
    }

<a name="command-io"></a>
## 指令輸入與輸出

<a name="defining-input-expectations"></a>
### 定義期待的輸入

當撰寫命令列時，從參數或是選擇來得到使用者的輸入是一種普遍的做法。藉由使用命令的 `signature` 屬性 Laravel 讓你很方便的定義希望從使用者得到的輸入， `signature` 屬性允許你用單獨、具表現力、與路由相似的語法，並用以定義命令的名字、參數及選擇。

所有提供給使用者的參數及選擇都在包在大括號中。如下方範例，此指令定義一個**必須的**參數：`user`：

    /**
     * 命令列的名字及署名
     *
     * @var string
     */
    protected $signature = 'email:send {user}';

你也可以使用選擇性的參數和定義預設的值給選擇性的參數:

    // 選擇性的參數...
    email:send {user?}

    // 選擇性的參數及預設的值...
    email:send {user=foo}

選擇，就跟參數一樣，同樣是使用者輸入的一種格式，不過當使用選擇時，需要加入兩個連字符 (`--`) 在命令列，我們可以像這樣子在署名中定義選擇:

    /**
     * 命令列的名字及署名
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue}';

在這個範例中，當呼叫 Artisan 指令時， `--queue` 這個選擇可以被明確的指定。如果 `--queue` 被當成輸入時，這個選擇的值會是 `true` ，如果沒有指定時，這個選擇的值將會是 `false`:

    php artisan email:send 1 --queue

你也可以藉由在這個選擇後面加個 `=` 來為選擇明確指定值:

    /**
     * 命令列的名字及署名
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue=}';

在這個範例中，使用者可以為這個選擇傳入一個值:

    php artisan email:send 1 --queue=default

你也可以指定預設值給選擇:

    email:send {user} {--queue=default}

#### 輸入的敘述

藉由加入冒號及敘述，你也可以為輸入參數及選擇加上敘述:

    /**
     * 命令列的名字及署名
     *
     * @var string
     */
    protected $signature = 'email:send
                            {user : 使用者的 ID }
                            {--queue= : 這個工作是否該進入隊列}';

<a name="retrieving-input"></a>
### 抽取輸入

當你的命令正在被執行時，你將需要存取參數及選擇。為了達到這個目的，你會需要使用 `argument` 及 `option` 方法:

使用 `argument` 方法來抽取參數的值:

    /**
     * 執行這個命令列
     *
     * @return mixed
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

如果你需要將所有的參數匯聚成一個陣列，只要簡單的呼叫 `argument` 即可，不需要加入任何輸入:

    $arguments = $this->argument();

而選擇的抽取就跟參數一樣簡單，除了使用的方法變為 `option` 。就像 `argument` 方法一樣，你可以呼叫 `option` 不加入任何輸入，即可抽取所有的
選擇並將之轉為一個 `array` :

    // 抽取特定的選擇
    $queueName = $this->option('queue');

    // 抽取所有選擇
    $options = $this->option();

如果參數或選擇不存在， 將會返回 `null`

<a name="prompting-for-input"></a>
### 為輸入加上提示

除了顯示輸出，你也可以在命令執行期間，要求使用者輸入值。 `ask` 方法將會用提供的問題來提示使用者，並且接受他們的輸入，並返回使用者的輸入回命令:

    /**
     * 執行這個命令列
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('你是名字是?');
    }

`secret` 方法就如同 `ask` 方法一般，但是使用者的輸入將不會顯示在命令列。這個方法適合的場景是輸入的值是敏感的資訊，例如密碼:

    $password = $this->secret('密碼是？');

#### 要求確認

如果你需要使用者做簡單的確認，你可以使用 `confirm` 方法。預設的情況時，這個方法會回傳 `false` ，然而，如果使用者對這個提示輸入 `y` ，那這個方法將會回傳 `true`

    if ($this->confirm('你希望繼續嗎? [y|N]')) {
        //
    }

#### 讓使用者做選擇

`anticipate` 方法可被用於使用自動完成來為你提供可能的選擇，使用者仍可以選擇任何答案，不管這些提供的選擇。

    $name = $this->anticipate('你的名字是?', ['泰勒', '戴爾']);

如果你需要提供使用者一系列事先定義的選擇，你可以使用 `choice` 方法，使用者選擇了答案的索引，但是答案會返回給你，你可以設定返回的預設值來防止沒有任何東西被選擇:

    $name = $this->choice('你的名字是?', ['泰勒', '戴爾'], false);

<a name="writing-output"></a>
### 撰寫輸出

使用 `info` 、 `comment` 、 `question` 和 `error` 方法來傳送輸出到終端。每個方法都有適當的 ANSI 顏色來表達它們的目的。

使用 `info` 方法來傳送資訊訊息給使用者，並以綠色呈現在終端。

    /**
     * 執行這個命令列
     *
     * @return mixed
     */
    public function handle()
    {
        $this->info('顯示我在畫面上');
    }

使用 `info` 方法來傳送錯誤訊息給使用者，並以紅色呈現在終端。

    $this->error('有東西出問題了！');

#### 表格佈局

`table` 方法讓格式化多 行/列 的資料變得簡單。只要傳送標頭和行到這個方法，寬跟高將會基於給的資料做動態的計算:

    $headers = ['Name', 'Email'];

    $users = App\User::all(['name', 'email'])->toArray();

    $this->table($headers, $users);

#### 進度條

對於需要長時間執行的任務，使用進度指示器將會有不錯的幫助。使用 output 物件，我們可以開始、前進、停止進度條，當開始執行時你需要定義總共有幾個階段，然後每階段完成後就讓進度條前進:

    $users = App\User::all();

    $bar = $this->output->createProgressBar(count($users));

    foreach ($users as $user) {
        $this->performTask($user);

        $bar->advance();
    }

    $bar->finish();


想得到更多資訊，請看看 [Symfony Progress Bar component documentation](http://symfony.com/doc/2.7/components/console/helpers/progressbar.html).

<a name="registering-commands"></a>
## 註冊命令

一旦你的命令完成，你需要先向 Artisan 註冊它，才可以使用它，註冊的檔案為 `app/Console/Kernel.php` 。

在這個檔案中，你會在 `commands` 屬性找到一整個名單的命令。只要加入類別的名稱到這個名單，當 Artisan 啟動時，所有條列在這個
屬性的命令，都會被 [service container](/docs/{{version}}/container) 解析並向 Artisan 註冊:

    protected $commands = [
        'App\Console\Commands\SendEmails'
    ];

<a name="calling-commands-via-code"></a>
## 使用程式碼呼叫命令

有時候你想在命令列介面外執行 Artisan 命令。例如，你希望在路由或控制器觸發 Artisan 命令。你只要在 `Artisan` facade 使用 `call` 方法來觸發。 `call` 方法的第一個參數為命令的名稱，第二個參數為陣列型態的命令輸入。退出碼將會被回傳：

    Route::get('/foo', function () {
        $exitCode = Artisan::call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

在 `Artisan` facade 使用 `queue` 方法，你甚至會將一堆 Artisan 命令放進隊列，好讓它們能在背景被你的 [queue workers](/docs/{{version}}/queues) 執行:

    Route::get('/foo', function () {
        Artisan::queue('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

If you need to specify the value of an option that does not accept string values, such as the `--force` flag on the `migrate:refresh` command, you may pass a boolean `true` or `false`:

    $exitCode = Artisan::call('migrate:refresh', [
        '--force' => true,
    ]);

### 在命令中呼叫其他命令

有時候，你會希望在命令中呼叫其他命令，你可以使用 `call` 方法來達成， `call` 方法接受命令名稱和陣列型態的命令輸入:

    /**
     * 執行這個命令列
     *
     * @return mixed
     */
    public function handle()
    {
        $this->call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    }

如果你想要呼叫其他命令並忽視所有它的輸出，你可以使用 `callSilent` 命令來完成。 `callSilent` 方法有和 `call` 方法一樣的署名:

    $this->callSilent('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);

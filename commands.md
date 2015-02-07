# Artisan 開發

- [簡介](#introduction)
- [建立自訂指令](#building-a-command)
- [註冊自訂指令](#registering-commands)

<a name="introduction"></a>
## 簡介

除了 Artisan 本身提供的指令之外，您也可以爲您的應用程式建立屬於你自己的指令。你可以將自訂指令存放在 `app/Console/commands` 目錄底下；然而，您也可以任意選擇存放位置，只要您的指令能夠被 `composer.json` 自動載入。

<a name="building-a-command"></a>
## 建立自訂指令

### 自動創建類別（Class）

要創建一個新的自訂指令，您可以使用 `make:console` 這個 Artisan 指令，這將會自動產生一個 Command stub 協助您開始創建您的自訂指令：

#### 自動創建一個新的指令類別

	php artisan make:console FooCommand

上面的指令將會協助你自動創建一個類別，並儲存為檔案 `app/Console/FooCommand.php`。

在創建自訂指令時，加上 `--command` 這個選項，將可以指定之後在終端機使用此自訂指令時，所要輸入的自訂指令名稱：

	php artisan make:console AssignUsers --command=users:assign

### 撰寫自訂指令

一旦你的自訂指令被創建後，你需要填寫自訂指令的 `名稱（name）` 與 `描述（description）`，您所填寫的內容將會被顯示在 Artisan 的 `list` 畫面中。

當您的自訂指令被執行時，將會呼叫 `fire` 方法，您可以在此為自訂指令加入任何的邏輯判斷。

### 參數與選項

你可以透過 `getArguments` 與 `getOptions` 為自訂指令自行定義任何需要的參數與選項。這兩個方法都會回傳一組指令陣列，並由選項陣列的清單所組成。

當定義 `arguments` 時，該陣列值的定義分別如下：

	array($name, $mode, $description, $defaultValue)

參數 `mode` 可以是下列其中一項： `InputArgument::REQUIRED` 或 `InputArgument::OPTIONAL`。

當定義 `options` 時，該陣列值的定義分別如下：

	array($name, $shortcut, $mode, $description, $defaultValue)

對選項而言，參數 `mode` 可以是下列其中一項：`InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`。

模式為 `VALUE_IS_ARRAY` 表示呼叫指令時可以多次使用此選項來傳入多個值：

	php artisan foo --option=bar --option=baz

模式為 `VALUE_NONE` 則表示將此選項純粹作為一種有或無的「開關」使用：

	php artisan foo --option

### 取得輸入值（參數與選項）

當您的自訂指令執行時，您需要讓您的應用程式可以存取到這些參數和選項的值，要做到這一點，您可以使用 `argument` 和 `option` 方法：

#### 取得自訂指令被輸入的參數

	$value = $this->argument('name');

#### 取得自訂指令被輸入的所有參數

	$arguments = $this->argument();

#### 取得自訂指令被輸入的選項

	$value = $this->option('name');

#### 取得自訂指令被輸入的所有選項

	$options = $this->option();

### 產生輸出

想要顯示資訊到終端螢幕上，您可以使用 `info`、`comment`、`question` 和 `error` 方法。每一種方法將會依據它所代表的目的，分別對應一種適當的 ANSI 顏色。

#### 顯示一般訊息到終端螢幕

	$this->info('Display this on the screen');

#### 顯示錯誤訊息到終端螢幕

	$this->error('Something went wrong!');

### 詢問式輸入

您也可以使用 `ask` 和 `confirm` 方法來提示使用者進行輸入：

#### 提示使用者進行輸入

	$name = $this->ask('What is your name?');

#### 提示使用者進行加密輸入

	$password = $this->secret('What is the password?');

#### 提示使用者進行確認

	if ($this->confirm('Do you wish to continue? [yes|no]'))
	{
		//
	}

您也可以指定一個預設值給 `confirm` 方法，可以是 `true` 或 `false`：

	$this->confirm($question, true);

### 呼叫其它指令

有時候您可能希望在您的指令內部呼叫其它指令，此時您可以使用 `call` 方法：

	$this->call('command:name', ['argument' => 'foo', '--option' => 'bar']);

<a name="registering-commands"></a>
## 註冊自訂指令

#### 註冊一個 Artisan 指令

一旦你的自訂指令撰寫完成後，你需要將它註冊於 Artisan 它才能被使用。這通常位於 `app/Console/Kernel.php` 這個檔案中。在此檔案的 `commands` 屬性，你會找到一份指令的清單。若要註冊你的自訂指令，很簡單的你只要將它加入清單中。當 Artisan 啟動時，被列於此屬性中的所有指令都將被 [IoC container](/docs/5.0/container) 解析，並且被註冊於 Artisan 。

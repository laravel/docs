# Artisan 開發

- [簡介](#introduction)
- [自訂指令](#building-a-command)
- [註冊指令](#registering-commands)
- [呼叫其它指令](#calling-other-commands)

<a name="introduction"></a>
## 簡介

除了 Artisan 本身提供的指令之外，您也可以建立與您的應用程式相關的指令，這些自建指令將會存放在 `app/commands` 目錄底下；然而，您可以任意選擇存放位置，只要您的指令能夠被 composer.json 給自動載入。

<a name="building-a-command"></a>
## 自訂指令

### 生成類

要創建一個新的指令，您可以使用 command:make 這個 Artisan 指令，這將產生一個指令存根協助您開始：

#### 產生一個新的指令類

	php artisan command:make FooCommand

預設情況下，生成的指令將被儲存在 `app/commands` 目錄；然而，您可以指定自訂路徑或命名空間：

	php artisan command:make FooCommand --path=app/classes --namespace=Classes

在創建指令時，加上 `--command` 這個選項，將可以指定這個指令的名稱：

	php artisan command:make AssignUsers --command=users:assign

### 撰寫自訂指令

當自訂指令生成後，您需在填寫指令的 `名稱` 與 `描述`，這部份將會顯示在指令列表清單的畫面上。

當您的自訂指令被執行時，將會呼叫 `fire` 方法，您可以在此加入任何的邏輯判斷。

### 參數與選項

`getArguments` 與 `getOptions` 方法是用來接收要傳入您的自訂指令的地方，這兩個方法都會回傳一組指令陣列，並由選項陣列清單所組成。

當定義 `arguments` 時，該陣列對應的值表示如下：

	array($name, $mode, $description, $defaultValue)

參數 `mode` 可以是下列其中一項： `InputArgument::REQUIRED` 或 `InputArgument::OPTIONAL`.

當定義 `options` 時，該陣列對應的值表示如下：

	array($name, $shortcut, $mode, $description, $defaultValue)

對選項而言, 參數 `mode` 可以是下列其中一項： `InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`.

該 `VALUE_IS_ARRAY` 模式表示呼叫指令時可以傳入多筆數值：

	php artisan foo --option=bar --option=baz

該 `VALUE_NONE` 模式表示將選項當作是"開關"

	php artisan foo --option

### 取得輸入

當您的指令執行時，您需要讓您的應用程式可以存取到這些參數和選項的值，
要做到這一點，您可以使用 `argument` 和 `option` 方法：

#### 取得自訂指令的輸入參數

	$value = $this->argument('name');

#### 取得所有自訂指令的輸入參數

	$arguments = $this->argument();

#### 取得自訂指令的輸入選項

	$value = $this->option('name');

#### 取得所有自訂指令的輸入選項

	$options = $this->option();

### 產生輸出

顯示資訊到終端上，您可以使用 `info`, `comment`, `question` 和`error`方法，每一種方法將會對應到一個 ANSI 顏色。

#### 顯示訊息到終端

	$this->info('Display this on the screen');

#### 顯示錯誤訊息到終端

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

<a name="registering-commands"></a>
## 註冊指令

#### 註冊一個 Artisan 指令

當您的自訂指令完成後，您需要向 Artisan 註冊才能使用，通常是在 `app/start/artisan.php` ，在此檔案內，你可以使用 `Artisan::add` 方法註冊該指令：

	Artisan::add(new CustomCommand);

#### 在 IoC Container 內註冊指令

如果您的自訂指令是在應用程式 [IoC container](/docs/ioc) 內註冊，您需要使用 `Artisan::resolve` 方法讓 Artisan 可以使用：

	Artisan::resolve('binding.name');

#### 在 Service Provider 內註冊指令

如果您需要從 service provider 註冊指令，您應該在 provider 的  `boot` 方法內呼叫 `commands` 方法，傳入 IoC container 綁定此指令：

	public function boot()
	{
		$this->commands('command.binding');
	}

<a name="calling-other-commands"></a>
## 呼叫其它指令

有時候您可能希望在您的指令內部呼叫其它指令，此時您可以使用 `call` 方法：

	$this->call('command:name', array('argument' => 'foo', '--option' => 'bar'));

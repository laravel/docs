# 郵件

- [設定](#configuration)
- [基本用法](#basic-usage)
- [內嵌附件](#embedding-inline-attachments)
- [郵件隊列](#queueing-mail)
- [郵件與本地端開發](#mail-and-local-development)

<a name="configuration"></a>
## 設定

Laravel 基於熱門的 [SwiftMailer](http://swiftmailer.org) 函式庫之上，提供了一個簡潔的 API。郵件設定檔為 `config/mail.php`，包含若干選項，讓您可以更改 SMTP  主機、連接埠、遤證，也可以讓您對函式庫傳送出去的所有訊息設定全域的 `from` 地址。您可使用任何您想要的 SMTP 伺服器。如果想使用 PHP `mail` 函式來寄送郵件，您可以將設定檔中的 `driver` 更改為 `mail`。您也可以使用 `sendmail`  驅動器。

### API 驅動

Laravel 也包含了 Mailgun 及 Mandrill HTTP API 的驅動。這些 API 通常比 SMTP  伺服器更簡單快速。這兩套驅動都需要在應用程式中安裝 Guzzle 4 HTTP 函式庫。您可在 `composer.josn` 中加入下列程式碼， 以便在專案中加入 Guzzle 4：

	"guzzlehttp/guzzle": "~4.0"

#### Mailgun 驅動

要使用 Mailgun 驅動，請將 `config/mail.php` 設定檔中的 `driver` 選項設定為 `mailgun`。接下來，若 `config/service.php` 設定檔還不存在於您的專案中，請建立此檔，並確認其包含下列選項：

	'mailgun' => array(
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	),

#### Mandrill 驅動

要使用 Mandrill 驅動，將 `config/mail.php` 設定檔中的 `driver` 選項設定為 `mandrill`。接下來，若 `config/service.php` 設定檔還不存在於您的專案中，請建立此檔，並確認其包含下列選項：

	'mandrill' => array(
		'secret' => 'your-mandrill-key',
	),

### 日誌驅動

若您的 `config/mail.php` 設定檔中的 `driver` 選項設定為 `log` ，所有的電子郵件都會被寫入日誌檔，而不會真正寄給任何收件者。這主要用於快速的本地端除錯及內容驗證。

<a name="basic-usage"></a>
## 基本用法

您可使用 `Mail::send` 方法來寄送電子郵件訊息：

	Mail::send('emails.welcome', array('key' => 'value'), function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

傳入 `send` 方法的第一個參數為郵件視圖的名稱。第二個是傳遞給該視圖的資料，通常是一個關聯式陣列，讓視圖可透過 `$key` 來取得資料項目。第三個參數是一個閉包，可以對 message 進行各種設定。

> **注意：** `$message` 變數總是會被傳入郵件視圖中，並且允許內嵌附件。因此最好避免在您的視圖本體中傳入 `message` 變數。 

除了 HTML 視圖外，您也可以指定使用純文字視圖：

	Mail::send(array('html.view', 'text.view'), $data, $callback);

或者，您可使用 `html` 或 `text` 作為鍵值來指定單一類型的視圖：

	Mail::send(array('text' => 'view'), $data, $callback);

您也可以在郵件訊息中指定其他選項，例如副本收件者或附件：

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');

		$message->attach($pathToFile);
	});

要附加檔案至 message 時，可以指定 MIME 的類型、顯示名稱：

	$message->attach($pathToFile, array('as' => $display, 'mime' => $mime));

若您只需寄送一個簡單的字串而非完整的視圖，可使用 `raw` 方法：

	Mail::raw('Text to e-mail', function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');
	});

> **注意：** 傳遞至 `Mail::send` 閉包的 message 實例是繼承了 SwiftMailer 的 message  類別，你可以呼叫該類別的任何方法來建立電子郵件訊息。

<a name="embedding-inline-attachments"></a>
## 內嵌附件

在電子郵件中嵌入內部圖像通常很麻煩；然而 Laravel 提供一個便利的方法讓您對電子郵件附加圖像，並取得相應的 CID。

#### 在郵件視圖中嵌入圖像

	<body>
		這是一張圖像：

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### 在郵件視圖中嵌入原始資料

	<body>
		這是一張從原始資料來的圖像：

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

請注意 `Mail` 類別總是會將 `$message` 變數傳遞給電子郵件視圖。

<a name="queueing-mail"></a>
## 郵件隊列

#### 將郵件訊息加入隊列

寄送電子郵件訊息會大幅延長應用程式的回應時間，因此許多開發者選擇將郵件訊息加入隊列並於背景發送。 Laravel  使用內建 [統一的 queue API](/docs/5.0/queues) ，讓您輕鬆地完成此工作。要將郵件訊息加入隊列，只要使用 `Mail` 類別的 `queue` 方法：

	Mail::queue('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

您也可以使用 `later` 方法來指定您希望延遲寄送郵件訊息的秒數：

	Mail::later(5, 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

若您想要指定特定的隊列或「管道」來加入訊息，您可使用 `queueOn` 以及 `laterOn` 方法：

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

<a name="mail-and-local-development"></a>
## 郵件與本地端開發

當開發寄送電子郵件的應用程式時，我們通常希望不要真的從本地端或開發環境寄出郵件。您可以使用 `Mail::pretend` 方法或將 `config/mail.php` 設定檔中的 `pretend` 選項設定為 `true`。在 `pretend`  模式下，訊息會改而寫入應用程式的日誌檔，而不會真的寄出給收件者。

若您想要實際閱覽測試的郵件，可考慮使用像是 [MailTrap](https://mailtrap.io) 的服務。

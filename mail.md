# 邮件

- [设置](#configuration)
- [基本用法](#basic-usage)
- [内嵌附件](#embedding-inline-attachments)
- [邮件队列](#queueing-mail)
- [邮件与本地端开发](#mail-and-local-development)

<a name="configuration"></a>
## 设置

Laravel 基于热门的 [SwiftMailer](http://swiftmailer.org) 函式库之上，提供了一个简洁的 API。邮件设置档为 `config/mail.php`，包含若干选项，让您可以更改 SMTP  主机、连接端口、遤证，也可以让您对函式库发送出去的所有消息设置全域的 `from` 地址。您可使用任何您想要的 SMTP 服务器。如果想使用 PHP `mail` 函式来寄送邮件，您可以将设置档中的 `driver` 更改为 `mail`。您也可以使用 `sendmail`  驱动器。

### API 驱动

Laravel 也包含了 Mailgun 及 Mandrill HTTP API 的驱动。这些 API 通常比 SMTP  服务器更简单快速。这两套驱动都需要在应用程序中安装 Guzzle 4 HTTP 函式库。您可在 `composer.josn` 中加入下列代码， 以便在专案中加入 Guzzle 4：

	"guzzlehttp/guzzle": "~4.0"

#### Mailgun 驱动

要使用 Mailgun 驱动，请将 `config/mail.php` 设置档中的 `driver` 选项设置为 `mailgun`。接下来，若 `config/service.php` 设置档还不存在于您的专案中，请建立此档，并确认其包含下列选项：

	'mailgun' => array(
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	),

#### Mandrill 驱动

要使用 Mandrill 驱动，将 `config/mail.php` 设置档中的 `driver` 选项设置为 `mandrill`。接下来，若 `config/service.php` 设置档还不存在于您的专案中，请建立此档，并确认其包含下列选项：

	'mandrill' => array(
		'secret' => 'your-mandrill-key',
	),

### 日志驱动

若您的 `config/mail.php` 设置档中的 `driver` 选项设置为 `log` ，所有的电子邮件都会被写入日志档，而不会真正寄给任何收件者。这主要用于快速的本地端除错及内容验证。

<a name="basic-usage"></a>
## 基本用法

您可使用 `Mail::send` 方法来寄送电子邮件消息：

	Mail::send('emails.welcome', array('key' => 'value'), function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

传入 `send` 方法的第一个参数为邮件视图的名称。第二个是传递给该视图的数据，通常是一个关联式数组，让视图可透过 `$key` 来取得数据项目。第三个参数是一个闭包，可以对 message 进行各种设置。

> **注意：** `$message` 变量总是会被传入邮件视图中，并且允许内嵌附件。因此最好避免在您的视图本体中传入 `message` 变量。 

除了 HTML 视图外，您也可以指定使用纯文本视图：

	Mail::send(array('html.view', 'text.view'), $data, $callback);

或者，您可使用 `html` 或 `text` 作为键值来指定单一类型的视图：

	Mail::send(array('text' => 'view'), $data, $callback);

您也可以在邮件消息中指定其他选项，例如副本收件者或附件：

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');

		$message->attach($pathToFile);
	});

要附加文件至 message 时，可以指定 MIME 的类型、显示名称：

	$message->attach($pathToFile, array('as' => $display, 'mime' => $mime));

若您只需寄送一个简单的字串而非完整的视图，可使用 `raw` 方法：

	Mail::raw('Text to e-mail', function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');
	});

> **注意：** 传递至 `Mail::send` 闭包的 message 实例是继承了 SwiftMailer 的 message  类别，你可以调用该类别的任何方法来建立电子邮件消息。

<a name="embedding-inline-attachments"></a>
## 内嵌附件

在电子邮件中嵌入内部图像通常很麻烦；然而 Laravel 提供一个便利的方法让您对电子邮件附加图像，并取得相应的 CID。

#### 在邮件视图中嵌入图像

	<body>
		这是一张图像：

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### 在邮件视图中嵌入原始数据

	<body>
		这是一张从原始数据来的图像：

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

请注意 `Mail` 类别总是会将 `$message` 变量传递给电子邮件视图。

<a name="queueing-mail"></a>
## 邮件队列

#### 将邮件消息加入队列

寄送电子邮件消息会大幅延长应用程序的回应时间，因此许多开发者选择将邮件消息加入队列并于背景发送。 Laravel  使用内置 [统一的 queue API](/docs/5.0/queues) ，让您轻松地完成此工作。要将邮件消息加入队列，只要使用 `Mail` 类别的 `queue` 方法：

	Mail::queue('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

您也可以使用 `later` 方法来指定您希望延迟寄送邮件消息的秒数：

	Mail::later(5, 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

若您想要指定特定的队列或「管道」来加入消息，您可使用 `queueOn` 以及 `laterOn` 方法：

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

<a name="mail-and-local-development"></a>
## 邮件与本地端开发

当开发寄送电子邮件的应用程序时，我们通常希望不要真的从本地端或开发环境寄出邮件。您可以使用 `Mail::pretend` 方法或将 `config/mail.php` 设置档中的 `pretend` 选项设置为 `true`。在 `pretend`  模式下，消息会改而写入应用程序的日志档，而不会真的寄出给收件者。

若您想要实际阅览测试的邮件，可考虑使用像是 [MailTrap](https://mailtrap.io) 的服务。

# 邮件

- [配置](#configuration)
- [基本用法](#basic-usage)
- [嵌入内联附件](#embedding-inline-attachments)
- [队列邮件](#queueing-mail)
- [邮件 & 本地开发环境](#mail-and-local-development)

<a name="configuration"></a>
## 配置

Laravel的邮件功能构建于流行的[SwiftMailer](http://swiftmailer.org)库之上，并提供了简介、高效的API。邮件配置信息在`app/config/mail.php`文件中，并提供了包含SMTP主机、端口和证书的配置选项，也可以为发送的邮件配置一个全局`from`（来自）地址。你可以使用任何的SMTP服务器。如果你希望使用PHP的`mail`函数来发送邮件，可以通过改变配置文件中的 `driver`为`mail`。另外还支持`sendmail` 。


<a name="basic-usage"></a>
## 基本用例

使用`Mail::send` 方法来发送一封邮件：

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

传入`send`方法的第一个参数为生成邮件体所用的视图名。第二个参数`$data`是要传入视图的数据，第三个参数为闭包，允许你为邮件配置各种选项。

> **注意：** `$message`变量总是会传递到邮件视图中，它允许你给该邮件内容添加内联附件。因此应该避免向视图中传递命名为`message`的变量。

> **注解：** 内联附件（Inline Attachment）：“内联附件”是指可以在邮件体中直接看到的附件，一般是文本或图片；“内联附件”与一般附件的区别在于：一般附件必须在点击之后才能查看。详细信息可以看[内联附件与一般附件的区别](http://www.mkyong.com/computer-tips/different-between-inline-and-attachment-in-email/)。

除了HTML视图，你还可以指定一个纯文本视图：

	Mail::send(array('html.view', 'text.view'), $data, $callback);

或者，你可以通过`html`或`text`关键字指定唯一一个视图类型：

	Mail::send(array('text' => 'view'), $data, $callback);

你还可以为邮件指定其他选项，例如邮件抄送者或者附件：

	Mail::send('emails.welcome', $data, function($m)
	{
		$m->from('us@example.com', 'Laravel');

		$m->to('foo@example.com')->cc('bar@example.com');

		$m->attach($pathToFile);
	});

当你为邮件添加附件时，可以指定MIME类型和/或展示名：

	$m->attach($pathToFile, array('as' => $display, 'mime' => $mime));

> **注意：** 传递给`Mail::send`闭包的消息对象实例继承自SwiftMailer类，因此，你可以调用任何该类的方法来构建邮件内容。

<a name="embedding-inline-attachments"></a>
## 嵌入内联附件

邮件中嵌入图片通常都很麻烦；幸好Laravel提供了很简便的方法来为你的邮件添加图片，并取得相应的CID。

**在邮件视图中嵌入内联图像**

	<body>
		Here is an image:

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

**在邮件视图中嵌入原始数据**

	<body>
		Here is an image from raw data:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

注意`$message`变量总会通过`Mail`类传递给邮件视图。

<a name="queueing-mail"></a>
## 队列邮件

由于发送邮件有可能会使应用程序需要花费较长的响应时间，许多开发者选择将邮件放入队列并在后台发送。Laravel内建了[统一队列 API](/docs/queue)来简化此功能。只需调用`Mail`类的`queue`方法就可以将邮件放入队列中：

**将一封邮件放入队列中**

	Mail::queue('emails.welcome', $data, function($m)
	{
		$m->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

你还可以使用`later`方法指定延迟多少秒再发送邮件：

	Mail::later(5, 'emails.welcome', $data, function($m)
	{
		$m->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

如果你想将邮件放到一个指定的队列或"管道" ，可以使用`queueOn`和`laterOn`方法：

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($m)
	{
		$m->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

<a name="mail-and-local-development"></a>
## 邮件 & 本地开发环境

当你开发需要发送邮件的应用时，在你本地或开发环境中通常需要禁用邮件发送功能。你可以通过调用`Mail::pretend` 方法或在 `app/config/mail.php` 配置文件中设置 `pretend` 选项为 `true` 达到这一目的。当邮件发送功能被置为 `pretend` 模式时，所有邮件都会被写入当前应用的log文件中，而不会发送给收件人。

**启用Pretend模式**

	Mail::pretend();
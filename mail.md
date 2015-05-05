# Mail

- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Working With Attachments](#working-with-attachments)
- [Queueing Mail](#queueing-mail)
- [Mail & Local Development](#mail-and-local-development)

<a name="configuration"></a>
## Configuration

Laravel provides a clean, simple API over the popular [SwiftMailer](http://swiftmailer.org) library. Laravel provides drivers for SMTP, Mailgun, Mandrill, Amazon SES, PHP's `mail` function and `sendmail`.

### Driver Prerequisuites

These drivers for API based mail systems such as Mailgun and Mandrill are often simpler and quicker than using SMTP servers. Both of these drivers require that the Guzzle 5 HTTP library be installed for your application. You can add Guzzle 5 to your project by adding the following line to your `composer.json` file:

	"guzzlehttp/guzzle": "~5.0"

#### Mailgun Driver

To use the Mailgun driver, first install Guzzle. Then, set the `driver` option to `mailgun` in your `config/mail.php` configuration file. Next, create a `config/services.php` configuration file if one does not already exist for your project. Verify that it contains the following options:

	'mailgun' => [
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	],

#### Mandrill Driver

To use the Mandrill driver, first install Guzzle. Then, set the `driver` option to `mandrill` in your `config/mail.php` configuration file. Next, create an `config/services.php` configuration file if one does not already exist for your project. Verify that it contains the following options:

	'mandrill' => [
		'secret' => 'your-mandrill-key',
	],

#### SES Driver

To use the Amazon SES driver, install the Amazon AWS SDK for PHP. You can install this library by adding the following line to your `composer.json` file's `require` section:

	"aws/aws-sdk-php": "~2.4"

Next, set the `driver` option to `ses` in your `config/mail.php` configuration file. Finally, create an `config/services.php` configuration file if one does not already exist for your project. Verify that it contains the following options:

	'ses' => [
		'key' => 'your-ses-key',
		'secret' => 'your-ses-secret',
		'region' => 'ses-region',  // e.g. us-east-1
	],

<a name="basic-usage"></a>
## Basic Usage

The `send` method on the `Mail` [facade](/docs/{{version}}/facades) is used to send an e-mail message:

	<?php namespace App\Http\Controllers;

	use Mail;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Send an e-mail reminder to the user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function sendEmailReminder(Request $request, $id)
		{
			$user = User::findOrFail($id);

			Mail::send('emails.reminder', ['user' => $user], function ($m) use ($user) {
				$m->to($user->email, $user->name)->subject('Your Reminder!');
			});
		}
	}

The first argument passed to the `send` method is the name of the view that should be used as the e-mail body.

The second is the data to be passed to the view, often as an associative array where the data items are available to the view by key. So, since we are passing an array containing the `user` key in the example above, we could display the user's name within our e-mail view using the following PHP code:

	<?php echo $user->name; ?>

> **Note:** A `$message` variable is always passed to e-mail views, and allows the inline embedding of attachments. So, it is best to avoid passing a `message` variable in your view payload.

#### Building The Message

The third argument is a Closure allowing you to specify various options on the e-mail message itself. Using this Closure you may specify other attributes of the message, such as carbon copies, bling carbon copies, etc:

	Mail::send('emails.welcome', $data, function ($message) {
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');
	});

Here is a list of the available methods on the `$message` message builder instance:

	$message->from($address, $name = null);
	$message->sender($address, $name = null);
	$message->to($address, $name = null);
	$message->cc($address, $name = null);
	$message->bcc($address, $name = null);
	$message->replyTo($address, $name = null);
	$message->subject($subject);
	$message->priority($level);
	$message->attach($pathToFile, array $options = []);

	// Attach a file from a raw $data string...
	$message->attachData($data, $name, array $options = []);

	// Get the underlying SwiftMailer message instance...
	$message->getSwiftMessage();

#### Plain Text E-Mails

You may also specify a plain text view to use in addition to an HTML view:

	Mail::send(['html.view', 'text.view'], $data, $callback);

Or, you may specify only one type of view using the `html` or `text` keys:

	Mail::send(['text' => 'view'], $data, $callback);

#### E-Mailing Raw Strings

If you just need to e-mail a simple string instead of an entire view, use the `raw` method:

	Mail::raw('Text to e-mail', function ($message) {
		//
	});

> **Note:** The message instance passed to a `Mail::send` Closure extends the SwiftMailer message class, allowing you to call any method on that class to build your e-mail messages.

<a name="working-with-attachments"></a>
## Working With Attachments

To add attachments to an e-mail, use the `attach` method on the `$message` object passed to your Closure:

	Mail::send('emails.welcome', $data, function ($message) {
		//

		$message->attach($pathToFile);
	});

When attaching files to a message, you may also specify the display name and / or MIME type:

	$message->attach($pathToFile, ['as' => $display, 'mime' => $mime]);

### Embedding Inline Attachments

#### Embedding An Image In An E-Mail View

Embedding inline images into your e-mails is typically cumbersome; however, Laravel provides a convenient way to attach images to your e-mails and retrieving the appropriate CID.

	<body>
		Here is an image:

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### Embedding Raw Data In An E-Mail View

	<body>
		Here is an image from raw data:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

Note that the `$message` variable is always passed to e-mail views by the `Mail` facade.

<a name="queueing-mail"></a>
## Queueing Mail

#### Queueing A Mail Message

Since sending e-mail messages can drastically lengthen the response time of your application, many developers choose to queue e-mail messages for background sending. Laravel makes this easy using its built-in [unified queue API](/docs/{{version}}/queues). To queue a mail message, simply use the `queue` method on the `Mail` facade:

	Mail::queue('emails.welcome', $data, function ($message) {
		//
	});

This method will automatically take care of pushing a job onto the queue to send the mail message in the background. Of course, you will need to [configure your queues](/docs/{{version}}/queues) before using this feature.

#### Delayed Sending Of Messages

You may also specify the number of seconds you wish to delay the sending of the mail message using the `later` method:

	Mail::later(5, 'emails.welcome', $data, function ($message) {
		//
	});

#### Pushing To Specific Queues

If you wish to specify a specific queue on which to push the message, you may do so using the `queueOn` and `laterOn` methods:

	Mail::queueOn('queue-name', 'emails.welcome', $data, function ($message) {
		//
	});

	Mail::laterOn('queue-name', 5, 'emails.welcome', $data, function ($message) {
		//
	});

<a name="mail-and-local-development"></a>
## Mail & Local Development

When developing an application that sends e-mail, it's usually desirable to disable the sending of messages from your local or development environment.

One solution is to use the `log` mail driver during local development. This driver will write all e-mail messages to your log files for inspection. For more information on configuring your application per environment, check out the [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

Alternatively, you may use a service like [Mailtrap](https://mailtrap.io) and the `smtp` driver to send your e-mail messages to a "dummy" mailbox where you may view them in a true e-mail client.

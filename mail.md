# Mail

- [Introduction](#introduction)
- [Sending Mail](#sending-mail)
    - [Attachments](#attachments)
    - [Inline Attachments](#inline-attachments)
    - [Queueing Mail](#queueing-mail)
- [Mail & Local Development](#mail-and-local-development)

<a name="introduction"></a>
## Introduction

Laravel provides a clean, simple API over the popular [SwiftMailer](http://swiftmailer.org) library. Laravel provides drivers for SMTP, Mailgun, Mandrill, Amazon SES, PHP's `mail` function, and `sendmail`, allowing you to quickly get started sending mail through a local or cloud based service of your choice.

### Driver Prerequisites

The API based drivers such as Mailgun and Mandrill are often simpler and faster than SMTP servers. All of the API drivers require that the Guzzle HTTP library be installed for your application. You may install Guzzle to your project by adding the following line to your `composer.json` file:

    "guzzlehttp/guzzle": "~5.3|~6.0"

#### Mailgun Driver

To use the Mailgun driver, first install Guzzle, then set the `driver` option in your `config/mail.php` configuration file to `mailgun`. Next, verify that your `config/services.php` configuration file contains the following options:

    'mailgun' => [
        'domain' => 'your-mailgun-domain',
        'secret' => 'your-mailgun-key',
    ],

#### Mandrill Driver

To use the Mandrill driver, first install Guzzle, then set the `driver` option in your `config/mail.php` configuration file to `mandrill`. Next, verify that your `config/services.php` configuration file contains the following options:

    'mandrill' => [
        'secret' => 'your-mandrill-key',
    ],

#### SES Driver

To use the Amazon SES driver, install the Amazon AWS SDK for PHP. You may install this library by adding the following line to your `composer.json` file's `require` section:

    "aws/aws-sdk-php": "~3.0"

Next, set the `driver` option in your `config/mail.php` configuration file to `ses`. Then, verify that your `config/services.php` configuration file contains the following options:

    'ses' => [
        'key' => 'your-ses-key',
        'secret' => 'your-ses-secret',
        'region' => 'ses-region',  // e.g. us-east-1
    ],

<a name="sending-mail"></a>
## Sending Mail

Laravel allows you to store your e-mail messages in [views](/docs/{{version}}/views). For example, to organize your e-mails, you could create an `emails` directory within your `resources/views` directory:

To send a message, use the `send` method on the `Mail` [facade](/docs/{{version}}/facades). The `send` method accepts three arguments. First, the name of a [view](/docs/{{version}}/views) that contains the e-mail message. Secondly, an array of data you wish to pass to the view. Lastly, a `Closure` callback which receives a message instance, allowing you to customize the recipients, subject, and other aspects of the mail message:

    <?php

    namespace App\Http\Controllers;

    use Mail;
    use App\User;
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

Since we are passing an array containing the `user` key in the example above, we could display the user's name within our e-mail view using the following PHP code:

    <?php echo $user->name; ?>

> **Note:** A `$message` variable is always passed to e-mail views, and allows the [inline embedding of attachments](#attachments). So, you should avoid passing a `message` variable in your view payload.

#### Building The Message

As previously discussed, the third argument given to the `send` method is a `Closure` allowing you to specify various options on the e-mail message itself. Using this Closure you may specify other attributes of the message, such as carbon copies, blind carbon copies, etc:

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

> **Note:** The message instance passed to a `Mail::send` Closure extends the SwiftMailer message class, allowing you to call any method on that class to build your e-mail messages.

#### Mailing Plain Text

By default, the view given to the `send` method is assumed to contain HTML. However, by passing an array as the first argument to the `send` method, you may specify a plain text view to send in addition to the HTML view:

    Mail::send(['html.view', 'text.view'], $data, $callback);

Or, if you only need to send a plain text e-mail, you may specify this using the `text` key in the array:

    Mail::send(['text' => 'view'], $data, $callback);

#### Mailing Raw Strings

You may use the `raw` method if you wish to e-mail a raw string directly:

    Mail::raw('Text to e-mail', function ($message) {
        //
    });

<a name="attachments"></a>
### Attachments

To add attachments to an e-mail, use the `attach` method on the `$message` object passed to your Closure. The `attach` method accepts the full path to the file as its first argument:

    Mail::send('emails.welcome', $data, function ($message) {
        //

        $message->attach($pathToFile);
    });

When attaching files to a message, you may also specify the display name and / or MIME type by passing an `array` as the second argument to the `attach` method:

    $message->attach($pathToFile, ['as' => $display, 'mime' => $mime]);

<a name="inline-attachments"></a>
### Inline Attachments

#### Embedding An Image In An E-Mail View

Embedding inline images into your e-mails is typically cumbersome; however, Laravel provides a convenient way to attach images to your e-mails and retrieving the appropriate CID. To embed an inline image, use the `embed` method on the `$message` variable within your e-mail view. Remember, Laravel automatically makes the `$message` variable available to all of your e-mail views:

    <body>
        Here is an image:

        <img src="<?php echo $message->embed($pathToFile); ?>">
    </body>

#### Embedding Raw Data In An E-Mail View

If you already have a raw data string you wish to embed into an e-mail message, you may use the `embedData` method on the `$message` variable:

    <body>
        Here is an image from raw data:

        <img src="<?php echo $message->embedData($data, $name); ?>">
    </body>

<a name="queueing-mail"></a>
### Queueing Mail

#### Queueing A Mail Message

Since sending e-mail messages can drastically lengthen the response time of your application, many developers choose to queue e-mail messages for background sending. Laravel makes this easy using its built-in [unified queue API](/docs/{{version}}/queues). To queue a mail message, use the `queue` method on the `Mail` facade:

    Mail::queue('emails.welcome', $data, function ($message) {
        //
    });

This method will automatically take care of pushing a job onto the queue to send the mail message in the background. Of course, you will need to [configure your queues](/docs/{{version}}/queues) before using this feature.

#### Delayed Message Queueing

If you wish to delay the delivery of a queued e-mail message, you may use the `later` method. To get started, simply pass the number of seconds by which you wish to delay the sending of the message as the first argument to the method:

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

When developing an application that sends e-mail, you probably don't want to actually send e-mails to live e-mail addresses. Laravel provides several ways to "disable" the actual sending of e-mail messages.

#### Log Driver

One solution is to use the `log` mail driver during local development. This driver will write all e-mail messages to your log files for inspection. For more information on configuring your application per environment, check out the [configuration documentation](/docs/{{version}}/installation#environment-configuration).

#### Universal To

Another solution provided by Laravel is to set a universal recipient of all e-mails sent by the framework. This way, all the emails generated by your application will be sent to a specific address, instead of the address actually specified when sending the message. This can be done via the `to` option in your `config/mail.php` configuration file:

    'to' => [
        'address' => 'dev@domain.com',
        'name' => 'Dev Example'
    ],

#### Mailtrap

Finally, you may use a service like [Mailtrap](https://mailtrap.io) and the `smtp` driver to send your e-mail messages to a "dummy" mailbox where you may view them in a true e-mail client. This approach has the benefit of allowing you to actually inspect the final e-mails in Mailtrap's message viewer.

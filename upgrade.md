# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="upgrade-9.0"></a>
## Upgrading To 9.0 From 8.x

<a name="application"></a>
### Application

<a name="the-application-contract"></a>
#### The `Application` Contract

**Likelihood Of Impact: Low**

The `storagePath` method of the `Illuminate\Contracts\Foundation\Application` interface has been updated to accept a `$path` argument. If you are implementing this interface you should update your implementation accordingly:

    public function storagePath($path = '');

<a name="mail"></a>
### Mail

<a name="symfony-mailer"></a>
#### Symfony Mailer

**Likelihood Of Impact: High**

SwiftMailer is discontinued as of December 2021 and was therefore replaced with Symfony Mailer 6.0 (See https://symfony.com/blog/the-end-of-swiftmailer). Because of this, SwiftMailer plugins and transports will no longer work with the new implementation.

##### Updated Content Methods

`send`, `html`, `text` & `plain` don't return the number of recipients anymore but an instance of `Illuminate\Mail\SentMessage` which contains the `Symfony\Component\Mailer\SentMessage` instance

##### Renamed Swift methods to Symfony

All Swift methods were renamed to an equivalent with Symfony in the method name. For example:

    // BEFORE
    $this->withSwiftMessage(function ($message) {
        $message->getHeaders()->addTextHeader(
            'Custom-Header', 'Header Value'
        );
    });

    // AFTER
    use Symfony\Component\Mime\Email;

    $this->withSymfonyMessage(function (Email $message) {
        $message->getHeaders()->addTextHeader(
            'Custom-Header', 'Header Value'
        );
    });

Please also take a look at the [Symfony Mailer Docs](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages) for all possible interactions with the Email message.

Here is a list of all Methods which need to be renamed if they are used:
    
    Message::getSwiftMessage();
    Message::getSymfonyMessage();

    Mailable::withSwiftMessage($callback);
    Mailable::withSymfonyMessage($callback);

    MailMessage::withSwiftMessage($callback);
    MailMessage::withSymfonyMessage($callback);

    Mailer::getSwiftMailer();
    Mailer::getSymfonyTransport();

    Mailer::setSwiftMailer($swift);
    Mailer::setSymfonyTransport(TransportInterface $transport);
    
    MailManager::createTransport($config);
    MailManager::createSymfonyTransport($config);

##### `Illuminate\Mail\Message`

The `Illuminate\Mail\Message` class now contains an instance of `Symfony\Component\Mime\Email` instead of `Swift_Message` so all forwarding calls in user-land will need to be updated. Here are some examples which were possible with SwiftMailer but are not possible anymore with Symfony Mailer (most people are probably using the Laravel style already):

    // IF YOU USED THIS
    $message
        ->setFrom('taylor@laravel.com')
        ->setTo('example@example.org')
        ->setSubject("Order Shipped")
        ->setBody(
            '<h1>HTML email</h1><p>Shows HTML tags if the client supports it.</p>',
            'text/html'
        )
        ->addPart(
            'Some Plain text in the email',
            'text/plain'
        );

    // YOU NEED TO CHANGE IT TO
    $email
        ->from('taylor@laravel.com')
        ->to('example@example.org')
        ->subject("Order Shipped")
        ->html('<h1>HTML email</h1><p>Shows HTML tags if the client supports it.</p>')
        ->text('Some Plain text in the email');

##### Removed `auth_mode` for SMTP

Setting the `auth_mode` in the mail config was removed, because the authentication mode can be automatically negotiated between the Mailer and the SMTP server.

##### Failed recipients

It's no longer possible to get a list of failed recipients. Instead, if an email is failed to send, and exception will be thrown.

##### Stream Options for SMTP transport

Setting stream options for the SMTP transport can no longer be done through an smtp key. Instead you need to set the options directly in the config. For example, when disabling TLS peer verification in `config/mail.php`:

    'smtp' => [
        // BEFORE
        'stream' => [
            'ssl' => [
                'verify_peer' => false,
            ],
        ],

        // AFTER
        'verify_peer' => false,
    ],

> {note} It is generally not advised to disable the Verification of SSL-Certificates because it introduces the possibiliets of Man-in-the-Middle attacks.

For more options you can take a look at the [Symfony Mailer Docs](https://symfony.com/doc/6.0/mailer.html#transport-setup)

##### Generated Messages ID's
SwiftMailer offered the ability to set a custom domain to generate Message ID's through register it to mime.idgenerator.idright. This is no longer possible with Symfony Mailer. Instead, Symfony Mailer will automatically generate a Message ID based on the sender and add it to a message automatically.

##### Removed Force Reconnection

It is no longer possible to force a reconnection (for example when the mailer is running through a daemon process). Instead, Symfony Mailer will properly attempt to reconnect the transport itself and error out if that fails.

##### Driver / Transport Prerequisites

`guzzlehttp/guzzle` can be removed if wanted (Still required to use with the HTTP Client and the ping methods on the scheduler). Symfony API mail transport will utilize `symfony/http` instead.

###### SES

`aws/aws-sdk-php` is not needed for SES Transport anymore and can be removed if wanted (Still required to use with the SQS queue driver and DynamoDb failed job storage). To continue using the SES Mailer you are required to use the underlying Symfony Amazon Mailer:

    composer require symfony/amazon-mailer

###### Mailgun

To continue using the Mailgun Mailer you are required to use the underlying Symfony Mailgun Mailer:

    composer require symfony/mailgun-mailer

###### Postmark

`wildbit/swiftmailer-postmark` needs to be removed because Laravel moved from SwiftMailer to Symfony Mailer. To continue using Postmark Mailer you are required to use the underlying Symfony Postmark Mailer:

    composer require symfony/postmark-mailer

<a name="queue"></a>
### Queue

<a name="the-opis-closure-library"></a>
#### The `opis/closure` Library

**Likelihood Of Impact: Low**

Laravel's dependency on `opis/closure` has been replaced by `laravel/serializable-closure`. This should not cause any breaking change in your application unless you are interacting with the `opis/closure` library directly. In addition, the previously deprecated `Illuminate\Queue\SerializableClosureFactory` and `Illuminate\Queue\SerializableClosure` classes have been removed. If you are interacting with `opis/closure` library directly or using any of the removed classes, you may use [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) instead.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) and choose which updates are important to you.

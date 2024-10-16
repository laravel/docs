# Mailtrap Driver

To use the [Mailtrap](https://mailtrap.io/) driver, install Mailtrap’s PHP SDK via Composer:
```
# With symfony http client (recommended)
composer require railsware/mailtrap-php symfony/http-client nyholm/psr7
```
```
# Or with guzzle http client
composer require railsware/mailtrap-php guzzlehttp/guzzle php-http/guzzle7-adapter
```

After installing the package, go to your application’s .env file and specify the *MAIL_MAILER* variable as *mailtrap*. Then, define *MAILTRAP_HOST* and *MAILTRAP_API_KEY*, as shown below:

```
MAIL_MAILER="mailtrap"
# for transactional emails
MAILTRAP_HOST="send.api.mailtrap.io"
MAILTRAP_API_KEY="YOUR_API_KEY_HERE"
# for bulk email sending 
MAILTRAP_HOST="bulk.api.mailtrap.io"
MAILTRAP_API_KEY="YOUR_API_KEY_HERE"
```

Lastly, add Mailtrap to the mailers array in your application's main configuration file (e.g., config/mail.php), like so:

```
'mailers' => [
    
            // start mailtrap transport
            'mailtrap' => [
                'transport' => 'mailtrap'
            ],
            // end mailtrap transport
    
    ]
```

To learn more about Mailtrap and see examples, read the [Mailtrap driver documentation](https://github.com/railsware/mailtrap-php/tree/main/src/Bridge/Laravel#usage). 

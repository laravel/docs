---
title: "Mail"
---

- [Introdução](#introduction)
    - [Configuração](#configuration)
    - [Pré-requisitos do Driver](#driver-prerequisites)
    - [Configuração de Failover](#failover-configuration)
    - [Configuração Round Robin](#round-robin-configuration)
- [Gerando Mailables](#generating-mailables)
- [Escrevendo Mailables](#writing-mailables)
    - [Configurando o Remetente](#configuring-the-sender)
    - [Configurando a View](#configuring-the-view)
    - [Dados da View](#view-data)
    - [Anexos](#attachments)
    - [Anexos Inline](#inline-attachments)
    - [Objetos Anexáveis](#attachable-objects)
    - [Cabeçalhos](#headers)
    - [Tags e Metadados](#tags-and-metadata)
    - [Personalizando a Mensagem do Symfony](#customizing-the-symfony-message)
- [Mailables em Markdown](#markdown-mailables)
    - [Gerando Mailables em Markdown](#generating-markdown-mailables)
    - [Escrevendo Mensagens em Markdown](#writing-markdown-messages)
    - [Personalizando os Componentes](#customizing-the-components)
- [Enviando E-mails](#sending-mail)
    - [Enfileirando E-mails](#queueing-mail)
- [Renderizando Mailables](#rendering-mailables)
    - [Visualizando Mailables no Navegador](#previewing-mailables-in-the-browser)
- [Localizando Mailables](#localizing-mailables)
- [Testes](#testing-mailables)
    - [Testando o Conteúdo do Mailable](#testing-mailable-content)
    - [Testando o Envio de Mailables](#testing-mailable-sending)
- [E-mail e Desenvolvimento Local](#mail-and-local-development)
- [Eventos](#events)
- [Transports Personalizados](#custom-transports)
    - [Transports Adicionais do Symfony](#additional-symfony-transports)

<a id="introduction"></a>
## Introdução

Enviar e-mails não precisa ser complicado. O Laravel fornece uma API de e-mail limpa e simples, baseada no popular componente [Symfony Mailer](https://symfony.com/doc/current/mailer.html). O Laravel e o Symfony Mailer fornecem drivers para enviar e-mails via SMTP, Cloudflare, Mailgun, Postmark, Resend, Amazon SES e `sendmail`, permitindo que você comece rapidamente a enviar e-mails por meio de um serviço local ou em nuvem de sua escolha.

<a id="configuration"></a>
### Configuração

Os serviços de e-mail do Laravel podem ser configurados através do arquivo de configuração `config/mail.php` da sua aplicação. Cada mailer configurado neste arquivo pode ter sua própria configuração única e até mesmo seu próprio "transport" único, permitindo que sua aplicação use diferentes serviços de e-mail para enviar determinadas mensagens. Por exemplo, sua aplicação pode usar o Postmark para enviar e-mails transacionais enquanto usa o Amazon SES para enviar e-mails em massa.

Dentro do seu arquivo de configuração `mail`, você encontrará um array de configuração `mailers`. Este array contém uma entrada de configuração de exemplo para cada um dos principais drivers / transports de e-mail suportados pelo Laravel, enquanto o valor de configuração `default` determina qual mailer será usado por padrão quando sua aplicação precisar enviar uma mensagem de e-mail.

<a id="driver-prerequisites"></a>
### Pré-requisitos do Driver / Transport

Os drivers baseados em API, como Mailgun, Postmark e Resend, costumam ser mais simples e rápidos do que enviar e-mails por meio de servidores SMTP. Sempre que possível, recomendamos que você use um desses drivers.

<a id="cloudflare-driver"></a>
#### Driver Cloudflare

Para usar o driver Cloudflare, instale o HTTP Client do Symfony via Composer:

```shell
composer require symfony/http-client
```

Em seguida, você precisará fazer duas alterações no arquivo de configuração `config/mail.php` da sua aplicação. Primeiro, defina seu mailer padrão como `cloudflare`:

```php
'default' => env('MAIL_MAILER', 'cloudflare'),
```

Segundo, adicione o seguinte array de configuração ao seu array de `mailers`:

```php
'cloudflare' => [
    'transport' => 'cloudflare',
],
```

Após configurar o mailer padrão da sua aplicação, adicione as seguintes opções ao seu arquivo de configuração `config/services.php`:

```php
'cloudflare' => [
    'account_id' => env('CLOUDFLARE_ACCOUNT_ID'),
    'key' => env('CLOUDFLARE_KEY'),
],
```

<a id="mailgun-driver"></a>
#### Driver Mailgun

Para usar o driver Mailgun, instale o transport Mailgun Mailer do Symfony via Composer:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

Em seguida, você precisará fazer duas alterações no arquivo de configuração `config/mail.php` da sua aplicação. Primeiro, defina seu mailer padrão como `mailgun`:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```

Segundo, adicione o seguinte array de configuração ao seu array de `mailers`:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

Após configurar o mailer padrão da sua aplicação, adicione as seguintes opções ao seu arquivo de configuração `config/services.php`:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```

Se você não estiver usando a [região do Mailgun](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview#mailgun-regions) dos Estados Unidos, pode definir o endpoint da sua região no arquivo de configuração `services`:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    'scheme' => 'https',
],
```

<a id="postmark-driver"></a>
#### Driver Postmark

Para usar o driver [Postmark](https://postmarkapp.com/), instale o transport Postmark Mailer do Symfony via Composer:

```shell
composer require symfony/postmark-mailer symfony/http-client
```

Em seguida, defina a opção `default` no arquivo de configuração `config/mail.php` da sua aplicação como `postmark`. Após configurar o mailer padrão da sua aplicação, certifique-se de que o arquivo de configuração `config/services.php` contém as seguintes opções:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```

Se você quiser especificar o message stream do Postmark que deve ser usado por um determinado mailer, pode adicionar a opção de configuração `message_stream_id` ao array de configuração do mailer. Este array de configuração pode ser encontrado no arquivo `config/mail.php` da sua aplicação:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```

Dessa forma, você também consegue configurar vários mailers do Postmark com message streams diferentes.

<a id="resend-driver"></a>
#### Driver Resend

Para usar o driver [Resend](https://resend.com/), instale o SDK PHP do Resend via Composer:

```shell
composer require resend/resend-php
```

Em seguida, defina a opção `default` no arquivo de configuração `config/mail.php` da sua aplicação como `resend`. Após configurar o mailer padrão da sua aplicação, certifique-se de que o arquivo de configuração `config/services.php` contém as seguintes opções:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```

<a id="ses-driver"></a>
#### Driver SES

Para usar o driver do Amazon SES, você deve primeiro instalar o AWS SDK para PHP da Amazon. Você pode instalar esta biblioteca via o gerenciador de pacotes Composer:

```shell
composer require aws/aws-sdk-php
```

Em seguida, defina a opção `default` no seu arquivo de configuração `config/mail.php` como `ses` e verifique se o seu arquivo de configuração `config/services.php` contém as seguintes opções:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```

Para utilizar [credenciais temporárias](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) da AWS por meio de um session token, você pode adicionar uma chave `token` à configuração do SES da sua aplicação:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```

Para interagir com os recursos de [gerenciamento de inscrições](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html) do SES, você pode retornar o cabeçalho `X-Ses-List-Management-Options` no array retornado pelo método [headers](#headers) de uma mensagem de e-mail:

```php
/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-List-Management-Options' => 'contactListName=MyContactList;topicName=MyTopic',
        ],
    );
}
```

Para enviar um e-mail por meio de um [tenant](https://docs.aws.amazon.com/ses/latest/dg/tenants.html) do SES, você pode retornar o cabeçalho `X-Ses-Tenant-Name` a partir do método `headers`. O Laravel passará o valor do cabeçalho como a opção `TenantName` para o SES ao enviar a mensagem:

```php
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-Tenant-Name' => 'tenant-id',
        ],
    );
}
```

Se você quiser definir [opções adicionais](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail) que o Laravel deve passar para o método `SendEmail` do AWS SDK ao enviar um e-mail, você pode definir um array `options` dentro da sua configuração `ses`:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'options' => [
        'ConfigurationSetName' => 'MyConfigurationSet',
        'EmailTags' => [
            ['Name' => 'foo', 'Value' => 'bar'],
        ],
    ],
],
```

<a id="failover-configuration"></a>
### Configuração de Failover

Às vezes, um serviço externo que você configurou para enviar os e-mails da sua aplicação pode estar fora do ar. Nesses casos, pode ser útil definir uma ou mais configurações de entrega de e-mail de reserva, que serão usadas caso seu driver de entrega principal esteja indisponível.

Para isso, você deve definir um mailer no arquivo de configuração `mail` da sua aplicação que use o transport `failover`. O array de configuração do mailer `failover` da sua aplicação deve conter um array de `mailers` que referenciam a ordem em que os mailers configurados devem ser escolhidos para a entrega:

```php
'mailers' => [
    'failover' => [
        'transport' => 'failover',
        'mailers' => [
            'postmark',
            'mailgun',
            'sendmail',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

Depois de configurar um mailer que usa o transport `failover`, você precisará definir o mailer de failover como seu mailer padrão no arquivo `.env` da sua aplicação para utilizar a funcionalidade de failover:

```ini
MAIL_MAILER=failover
```

<a id="round-robin-configuration"></a>
### Configuração Round Robin

O transport `roundrobin` permite distribuir a carga de envio de e-mails entre vários mailers. Para começar, defina um mailer no arquivo de configuração `mail` da sua aplicação que use o transport `roundrobin`. O array de configuração do mailer `roundrobin` da sua aplicação deve conter um array de `mailers` que referenciam quais mailers configurados devem ser usados para a entrega:

```php
'mailers' => [
    'roundrobin' => [
        'transport' => 'roundrobin',
        'mailers' => [
            'ses',
            'postmark',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```

Depois que o seu mailer round robin estiver definido, você deve configurá-lo como o mailer padrão utilizado pela sua aplicação, especificando o nome dele como valor da chave de configuração `default` no arquivo de configuração `mail` da sua aplicação:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```

O transport round robin seleciona aleatoriamente um mailer da lista de mailers configurados e, em seguida, passa para o próximo mailer disponível a cada e-mail subsequente. Em contraste com o transport `failover`, que ajuda a alcançar *[alta disponibilidade](https://en.wikipedia.org/wiki/High_availability)*, o transport `roundrobin` oferece *[balanceamento de carga](https://en.wikipedia.org/wiki/Load_balancing_(computing))*.

<a id="generating-mailables"></a>
## Gerando Mailables

Ao construir aplicações Laravel, cada tipo de e-mail enviado pela sua aplicação é representado por uma classe "mailable". Essas classes são armazenadas no diretório `app/Mail`. Não se preocupe se você não vir este diretório na sua aplicação, pois ele será gerado automaticamente quando você criar sua primeira classe mailable usando o comando Artisan `make:mail`:

```shell
php artisan make:mail OrderShipped
```

<a id="writing-mailables"></a>
## Escrevendo Mailables

Depois de gerar uma classe mailable, abra-a para que possamos explorar o seu conteúdo. A configuração de uma classe mailable é feita em vários métodos, incluindo os métodos `envelope`, `content` e `attachments`.

O método `envelope` retorna um objeto `Illuminate\Mail\Mailables\Envelope` que define o assunto e, às vezes, os destinatários da mensagem. O método `content` retorna um objeto `Illuminate\Mail\Mailables\Content` que define o [template Blade](/en/blade/) que será usado para gerar o conteúdo da mensagem.

<a id="configuring-the-sender"></a>
### Configurando o Remetente

<a id="using-the-envelope"></a>
#### Usando o Envelope

Primeiro, vamos explorar a configuração do remetente do e-mail. Ou, em outras palavras, de quem o e-mail será "enviado". Existem duas maneiras de configurar o remetente. A primeira é especificar o endereço "from" no envelope da sua mensagem:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```

Se desejar, você também pode especificar um endereço `replyTo`:

```php
return new Envelope(
    from: new Address('jeffrey@example.com', 'Jeffrey Way'),
    replyTo: [
        new Address('taylor@example.com', 'Taylor Otwell'),
    ],
    subject: 'Order Shipped',
);
```

<a id="using-a-global-from-address"></a>
#### Usando um Endereço `from` Global

No entanto, se a sua aplicação usar o mesmo endereço "from" para todos os seus e-mails, pode ser trabalhoso adicioná-lo a cada classe mailable que você gerar. Em vez disso, você pode especificar um endereço "from" global no arquivo de configuração `config/mail.php`. Este endereço será usado se nenhum outro endereço "from" for especificado na classe mailable:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```

Além disso, você pode definir um endereço "reply_to" global no arquivo de configuração `config/mail.php`:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```

<a id="configuring-the-view"></a>
### Configurando a View

Dentro do método `content` de uma classe mailable, você pode definir a `view`, ou seja, qual template deve ser usado ao renderizar o conteúdo do e-mail. Como cada e-mail normalmente usa um [template Blade](/en/blade/) para renderizar seu conteúdo, você tem todo o poder e a conveniência do motor de templates Blade ao construir o HTML do seu e-mail:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```

> **Nota:**
> Você pode querer criar um diretório `resources/views/mail` para armazenar todos os templates de e-mail; no entanto, você é livre para colocá-los onde quiser dentro do diretório `resources/views`.

<a id="plain-text-emails"></a>
#### E-mails em Texto Puro

Se você quiser definir uma versão em texto puro do seu e-mail, pode especificar o template de texto puro ao criar a definição `Content` da mensagem. Assim como o parâmetro `view`, o parâmetro `text` deve ser o nome de um template que será usado para renderizar o conteúdo do e-mail. Você é livre para definir tanto uma versão HTML quanto uma versão em texto puro da sua mensagem:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```

Por clareza, o parâmetro `html` pode ser usado como um alias do parâmetro `view`:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```

<a id="view-data"></a>
### Dados da View

<a id="via-public-properties"></a>
#### Via Propriedades Públicas

Normalmente, você vai querer passar alguns dados para a sua view que possam ser utilizados ao renderizar o HTML do e-mail. Existem duas maneiras de disponibilizar dados para a sua view. A primeira é que qualquer propriedade pública definida na sua classe mailable será automaticamente disponibilizada para a view. Assim, por exemplo, você pode passar dados para o construtor da sua classe mailable e atribuir esses dados a propriedades públicas definidas na classe:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```

Assim que os dados forem atribuídos a uma propriedade pública, eles estarão automaticamente disponíveis na sua view, então você pode acessá-los da mesma forma que acessaria quaisquer outros dados nos seus templates Blade:

```blade
<div>
    Price: {{ $order->price }}
</div>
```

<a id="via-the-with-parameter"></a>
#### Via o Parâmetro `with`:

Se você quiser personalizar o formato dos dados do seu e-mail antes de enviá-los ao template, pode passar manualmente os dados para a view por meio do parâmetro `with` da definição `Content`. Normalmente, você ainda passará os dados pelo construtor da classe mailable; no entanto, você deve definir esses dados como propriedades `protected` ou `private`, para que eles não sejam automaticamente disponibilizados para o template:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
            with: [
                'orderName' => $this->order->name,
                'orderPrice' => $this->order->price,
            ],
        );
    }
}
```

Assim que os dados forem passados pelo parâmetro `with`, eles estarão automaticamente disponíveis na sua view, então você pode acessá-los da mesma forma que acessaria quaisquer outros dados nos seus templates Blade:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```

<a id="attachments"></a>
### Anexos

Para adicionar anexos a um e-mail, você deve incluí-los no array retornado pelo método `attachments` da mensagem. Primeiro, você pode adicionar um anexo informando o caminho do arquivo ao método `fromPath` fornecido pela classe `Attachment`:

```php
use Illuminate\Mail\Mailables\Attachment;

/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file'),
    ];
}
```

Ao anexar arquivos a uma mensagem, você também pode especificar o nome de exibição e / ou o tipo MIME do anexo usando os métodos `as` e `withMime`:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a id="attaching-files-from-disk"></a>
#### Anexando Arquivos do Disco

Se você armazenou um arquivo em um dos seus [discos de sistema de arquivos](/en/filesystem/), pode anexá-lo ao e-mail usando o método de anexo `fromStorage`:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

É claro que você também pode especificar o nome e o tipo MIME do anexo:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

O método `fromStorageDisk` pode ser usado se você precisar especificar um disco de armazenamento diferente do disco padrão:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorageDisk('s3', '/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a id="raw-data-attachments"></a>
#### Anexos de Dados Brutos

O método de anexo `fromData` pode ser usado para anexar uma string bruta de bytes como anexo. Por exemplo, você pode usar este método se tiver gerado um PDF em memória e quiser anexá-lo ao e-mail sem gravá-lo em disco. O método `fromData` aceita uma closure que resolve os bytes dos dados brutos, além do nome que deve ser atribuído ao anexo:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
            ->withMime('application/pdf'),
    ];
}
```

<a id="inline-attachments"></a>
### Anexos Inline

Incorporar imagens inline nos seus e-mails costuma ser trabalhoso; no entanto, o Laravel oferece uma maneira conveniente de anexar imagens aos seus e-mails. Para incorporar uma imagem inline, use o método `embed` na variável `$message` dentro do seu template de e-mail. O Laravel disponibiliza automaticamente a variável `$message` para todos os seus templates de e-mail, então você não precisa se preocupar em passá-la manualmente:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```

> **Aviso:**
> A variável `$message` não está disponível em templates de mensagens de texto puro, já que essas mensagens não utilizam anexos inline.

<a id="embedding-raw-data-attachments"></a>
#### Incorporando Anexos de Dados Brutos

Se você já tiver uma string com dados brutos de imagem que deseja incorporar em um template de e-mail, pode chamar o método `embedData` na variável `$message`. Ao chamar o método `embedData`, você precisará fornecer um nome de arquivo que deve ser atribuído à imagem incorporada:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```

<a id="attachable-objects"></a>
### Objetos Anexáveis

Embora anexar arquivos às mensagens por meio de simples caminhos em string costume ser suficiente, em muitos casos as entidades anexáveis da sua aplicação são representadas por classes. Por exemplo, se a sua aplicação anexa uma foto a uma mensagem, ela também pode ter um model `Photo` que representa essa foto. Nesse caso, não seria conveniente passar simplesmente o model `Photo` para o método `attach`? Objetos anexáveis permitem fazer exatamente isso.

Para começar, implemente a interface `Illuminate\Contracts\Mail\Attachable` no objeto que será anexável às mensagens. Essa interface exige que sua classe defina um método `toMailAttachment` que retorna uma instância de `Illuminate\Mail\Attachment`:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * Get the attachable representation of the model.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```

Depois de definir seu objeto anexável, você pode retornar uma instância desse objeto a partir do método `attachments` ao construir uma mensagem de e-mail:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```

É claro que os dados dos anexos podem estar armazenados em um serviço remoto de armazenamento de arquivos, como o Amazon S3. Por isso, o Laravel também permite gerar instâncias de anexo a partir de dados armazenados em um dos [discos de sistema de arquivos](/en/filesystem/) da sua aplicação:

```php
// Create an attachment from a file on your default disk...
return Attachment::fromStorage($this->path);

// Create an attachment from a file on a specific disk...
return Attachment::fromStorageDisk('backblaze', $this->path);
```

Além disso, você pode criar instâncias de anexo a partir de dados que estão na memória. Para isso, forneça uma closure ao método `fromData`. A closure deve retornar os dados brutos que representam o anexo:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```

O Laravel também oferece métodos adicionais que você pode usar para personalizar seus anexos. Por exemplo, você pode usar os métodos `as` e `withMime` para personalizar o nome e o tipo MIME do arquivo:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```

<a id="headers"></a>
### Cabeçalhos

Às vezes, você pode precisar anexar cabeçalhos adicionais à mensagem enviada. Por exemplo, pode ser necessário definir um `Message-Id` personalizado ou outros cabeçalhos de texto arbitrários.

Para isso, defina um método `headers` na sua mailable. O método `headers` deve retornar uma instância de `Illuminate\Mail\Mailables\Headers`. Esta classe aceita os parâmetros `messageId`, `references` e `text`. É claro que você pode fornecer apenas os parâmetros de que precisa para a sua mensagem específica:

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        messageId: 'custom-message-id@example.com',
        references: ['previous-message@example.com'],
        text: [
            'X-Custom-Header' => 'Custom Value',
        ],
    );
}
```

<a id="tags-and-metadata"></a>
### Tags e Metadados

Alguns provedores de e-mail de terceiros, como o Mailgun e o Postmark, oferecem suporte a "tags" e "metadados" de mensagens, que podem ser usados para agrupar e rastrear os e-mails enviados pela sua aplicação. Você pode adicionar tags e metadados a uma mensagem de e-mail através da definição do seu `Envelope`:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        tags: ['shipment'],
        metadata: [
            'order_id' => $this->order->id,
        ],
    );
}
```

Se a sua aplicação estiver usando o driver Mailgun, você pode consultar a documentação do Mailgun para mais informações sobre [tags](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) e [metadados](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages). Da mesma forma, a documentação do Postmark também pode ser consultada para mais informações sobre o suporte deles a [tags](https://postmarkapp.com/blog/tags-support-for-smtp) e [metadados](https://postmarkapp.com/support/article/1125-custom-metadata-faq).

Se a sua aplicação estiver usando o Amazon SES para enviar e-mails, você deve usar o método `metadata` para anexar [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) à mensagem.

<a id="customizing-the-symfony-message"></a>
### Personalizando a Mensagem do Symfony

Os recursos de e-mail do Laravel são desenvolvidos pelo Symfony Mailer. O Laravel permite registrar callbacks personalizados que serão invocados com a instância de Message do Symfony antes do envio da mensagem. Isso lhe dá a oportunidade de personalizar profundamente a mensagem antes de ela ser enviada. Para isso, defina um parâmetro `using` na sua definição de `Envelope`:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        using: [
            function (Email $message) {
                // ...
            },
        ]
    );
}
```

<a id="markdown-mailables"></a>
## Mailables em Markdown

Mensagens mailable em Markdown permitem aproveitar os templates e componentes pré-construídos das [notificações por e-mail](/en/notifications/#mail-notifications) dentro das suas mailables. Como as mensagens são escritas em Markdown, o Laravel consegue renderizar templates HTML bonitos e responsivos para as mensagens, gerando automaticamente também uma versão em texto puro.

<a id="generating-markdown-mailables"></a>
### Gerando Mailables em Markdown

Para gerar uma mailable com um template Markdown correspondente, você pode usar a opção `--markdown` do comando Artisan `make:mail`:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```

Em seguida, ao configurar a definição `Content` da mailable dentro do seu método `content`, use o parâmetro `markdown` em vez do parâmetro `view`:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        markdown: 'mail.orders.shipped',
        with: [
            'url' => $this->orderUrl,
        ],
    );
}
```

<a id="writing-markdown-messages"></a>
### Escrevendo Mensagens em Markdown

Mailables em Markdown usam uma combinação de componentes Blade e sintaxe Markdown, que permitem construir facilmente mensagens de e-mail aproveitando os componentes de interface de e-mail pré-construídos do Laravel:

```blade
<x-mail::message>
# Order Shipped

Your order has been shipped!

<x-mail::button :url="$url">
View Order
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

> **Nota:**
> Não use indentação excessiva ao escrever e-mails em Markdown. Segundo os padrões do Markdown, os parsers de Markdown renderizam conteúdo indentado como blocos de código.

<a id="button-component"></a>
#### Componente Button

O componente button renderiza um link de botão centralizado. O componente aceita dois argumentos: um `url` e uma `color` opcional. As cores suportadas são `primary`, `success` e `error`. Você pode adicionar quantos componentes button quiser a uma mensagem:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```

<a id="panel-component"></a>
#### Componente Panel

O componente panel renderiza o bloco de texto fornecido dentro de um painel com uma cor de fundo ligeiramente diferente do restante da mensagem. Isso permite chamar a atenção para um determinado bloco de texto:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a id="table-component"></a>
#### Componente Table

O componente table permite transformar uma tabela Markdown em uma tabela HTML. O componente aceita a tabela Markdown como seu conteúdo. O alinhamento das colunas da tabela é suportado usando a sintaxe padrão de alinhamento de tabelas do Markdown:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a id="customizing-the-components"></a>
### Personalizando os Componentes

Você pode exportar todos os componentes de e-mail em Markdown para a sua própria aplicação, para personalização. Para exportar os componentes, use o comando Artisan `vendor:publish` para publicar a tag de asset `laravel-mail`:

```shell
php artisan vendor:publish --tag=laravel-mail
```

Este comando publicará os componentes de e-mail em Markdown no diretório `resources/views/vendor/mail`. O diretório `mail` conterá um diretório `html` e um diretório `text`, cada um com suas respectivas representações de cada componente disponível. Você é livre para personalizar esses componentes como quiser.

<a id="customizing-the-css"></a>
#### Personalizando o CSS

Depois de exportar os componentes, o diretório `resources/views/vendor/mail/html/themes` conterá um arquivo `default.css`. Você pode personalizar o CSS deste arquivo e seus estilos serão automaticamente convertidos em estilos CSS inline nas representações HTML das suas mensagens de e-mail em Markdown.

Se você quiser criar um tema completamente novo para os componentes Markdown do Laravel, pode colocar um arquivo CSS no diretório `html/themes`. Depois de nomear e salvar seu arquivo CSS, atualize a opção `theme` do arquivo de configuração `config/mail.php` da sua aplicação para corresponder ao nome do seu novo tema.

Para personalizar o tema de uma mailable específica, você pode definir a propriedade `$theme` da classe mailable com o nome do tema que deve ser usado ao enviar essa mailable.

<a id="sending-mail"></a>
## Enviando E-mails

Para enviar uma mensagem, use o método `to` na [facade](/en/facades/) `Mail`. O método `to` aceita um endereço de e-mail, uma instância de usuário ou uma coleção de usuários. Se você passar um objeto ou uma coleção de objetos, o mailer usará automaticamente as propriedades `email` e `name` deles ao determinar os destinatários do e-mail, então certifique-se de que esses atributos estejam disponíveis nos seus objetos. Depois de especificar os destinatários, você pode passar uma instância da sua classe mailable para o método `send`:

```php
<?php

namespace App\Http\Controllers;

use App\Mail\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Ship the order...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```

Você não se limita a especificar apenas os destinatários "to" ao enviar uma mensagem. Você pode definir os destinatários "to", "cc" e "bcc" encadeando os respectivos métodos:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```

<a id="looping-over-recipients"></a>
#### Iterando Sobre os Destinatários

Ocasionalmente, você pode precisar enviar uma mailable para uma lista de destinatários, iterando sobre um array de destinatários / endereços de e-mail. No entanto, como o método `to` acrescenta endereços de e-mail à lista de destinatários da mailable, cada iteração do loop enviará outro e-mail para todos os destinatários anteriores. Por isso, você deve sempre recriar a instância da mailable para cada destinatário:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```

<a id="sending-mail-via-a-specific-mailer"></a>
#### Enviando E-mail por um Mailer Específico

Por padrão, o Laravel enviará e-mails usando o mailer configurado como `default` no arquivo de configuração `mail` da sua aplicação. No entanto, você pode usar o método `mailer` para enviar uma mensagem usando uma configuração de mailer específica:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```

<a id="queueing-mail"></a>
### Enfileirando E-mails

<a id="queueing-a-mail-message"></a>
#### Enfileirando uma Mensagem de E-mail

Como o envio de e-mails pode afetar negativamente o tempo de resposta da sua aplicação, muitos desenvolvedores optam por enfileirar mensagens de e-mail para envio em segundo plano. O Laravel facilita isso usando sua [API de filas unificada](/en/queues/) integrada. Para enfileirar uma mensagem de e-mail, use o método `queue` na facade `Mail` depois de especificar os destinatários da mensagem:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```

Este método cuidará automaticamente de enviar um job para a fila, para que a mensagem seja enviada em segundo plano. Você precisará [configurar suas filas](/en/queues/) antes de usar este recurso.

<a id="delayed-message-queueing"></a>
#### Enfileiramento de Mensagens com Atraso

Se você quiser atrasar a entrega de uma mensagem de e-mail enfileirada, pode usar o método `later`. Como primeiro argumento, o método `later` aceita uma instância de `DateTime` indicando quando a mensagem deve ser enviada:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```

<a id="pushing-to-specific-queues"></a>
#### Enviando para Filas Específicas

Como todas as classes mailable geradas pelo comando `make:mail` utilizam a trait `Illuminate\Bus\Queueable`, você pode chamar os métodos `onQueue` e `onConnection` em qualquer instância de classe mailable, permitindo especificar a conexão e o nome da fila para a mensagem:

```php
$message = (new OrderShipped($order))
    ->onConnection('sqs')
    ->onQueue('emails');

Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue($message);
```

Alternativamente, você pode especificar a conexão e a fila usando os atributos `Connection` e `Queue` na classe mailable:

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('emails')]
class OrderShipped extends Mailable
{
    // ...
}
```

<a id="queueing-by-default"></a>
#### Enfileirando por Padrão

Se você tiver classes mailable que sempre devem ser enfileiradas, pode implementar o contrato `ShouldQueue` na classe. Assim, mesmo que você chame o método `send` ao enviar o e-mail, a mailable ainda será enfileirada, pois implementa o contrato:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```

<a id="queued-mailables-and-database-transactions"></a>
#### Mailables Enfileirados e Transações de Banco de Dados

Quando mailables enfileiradas são despachadas dentro de transações de banco de dados, elas podem ser processadas pela fila antes que a transação de banco de dados tenha sido confirmada (commit). Quando isso acontece, quaisquer atualizações que você tenha feito em models ou registros do banco de dados durante a transação podem ainda não estar refletidas no banco de dados. Além disso, quaisquer models ou registros de banco de dados criados dentro da transação podem não existir no banco de dados. Se a sua mailable depender desses models, podem ocorrer erros inesperados quando o job que envia a mailable enfileirada for processado.

Se a opção de configuração `after_commit` da sua conexão de fila estiver definida como `false`, você ainda pode indicar que uma determinada mailable enfileirada deve ser despachada somente após todas as transações de banco de dados abertas terem sido confirmadas, chamando o método `afterCommit` ao enviar a mensagem de e-mail:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```

Alternativamente, você pode chamar o método `afterCommit` a partir do construtor da sua mailable:

```php
<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable implements ShouldQueue
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> **Nota:**
> Para saber mais sobre como contornar esses problemas, consulte a documentação sobre [jobs enfileirados e transações de banco de dados](/en/queues/#jobs-and-database-transactions).

<a id="queued-email-failures"></a>
#### Falhas em E-mails Enfileirados

Quando um e-mail enfileirado falha, o método `failed` da classe mailable enfileirada será invocado, caso ele esteja definido. A instância de `Throwable` que causou a falha do e-mail enfileirado será passada para o método `failed`:

```php
<?php

namespace App\Mail;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Throwable;

class OrderDelayed extends Mailable implements ShouldQueue
{
    use SerializesModels;

    /**
     * Handle a queued email's failure.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```

<a id="rendering-mailables"></a>
## Renderizando Mailables

Às vezes, você pode querer capturar o conteúdo HTML de uma mailable sem enviá-la. Para isso, você pode chamar o método `render` da mailable. Este método retornará o conteúdo HTML avaliado da mailable como uma string:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```

<a id="previewing-mailables-in-the-browser"></a>
### Visualizando Mailables no Navegador

Ao projetar o template de uma mailable, é conveniente visualizar rapidamente a mailable renderizada no navegador, como um template Blade típico. Por isso, o Laravel permite retornar qualquer mailable diretamente de uma closure de rota ou de um controller. Quando uma mailable é retornada, ela será renderizada e exibida no navegador, permitindo visualizar rapidamente o seu design sem precisar enviá-la para um endereço de e-mail real:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```

<a id="localizing-mailables"></a>
## Localizando Mailables

O Laravel permite enviar mailables em um locale diferente do locale atual da requisição e até lembrará desse locale caso o e-mail seja enfileirado.

Para isso, a facade `Mail` oferece um método `locale` para definir o idioma desejado. A aplicação mudará para este locale quando o template da mailable estiver sendo avaliado e, em seguida, voltará ao locale anterior quando a avaliação for concluída:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```

<a id="user-preferred-locales"></a>
#### Locales Preferidos do Usuário

Às vezes, as aplicações armazenam o locale preferido de cada usuário. Ao implementar o contrato `HasLocalePreference` em um ou mais dos seus models, você pode instruir o Laravel a usar esse locale armazenado ao enviar e-mails:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

Depois de implementar a interface, o Laravel utilizará automaticamente o locale preferido ao enviar mailables e notificações para o model. Portanto, não há necessidade de chamar o método `locale` ao usar esta interface:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```

<a id="testing-mailables"></a>
## Testes

<a id="testing-mailable-content"></a>
### Testando o Conteúdo do Mailable

O Laravel oferece uma variedade de métodos para inspecionar a estrutura da sua mailable. Além disso, o Laravel fornece vários métodos práticos para testar se a sua mailable contém o conteúdo esperado:

```php tab=Pest
use App\Mail\InvoicePaid;
use App\Models\User;

test('mailable content', function () {
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
});
```

```php tab=PHPUnit
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content(): void
{
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
}
```

Como você deve esperar, as asserções "HTML" verificam se a versão HTML da sua mailable contém uma determinada string, enquanto as asserções "text" verificam se a versão em texto puro da sua mailable contém uma determinada string.

<a id="testing-mailable-sending"></a>
### Testando o Envio de Mailables

Sugerimos testar o conteúdo das suas mailables separadamente dos seus testes que verificam se uma determinada mailable foi "enviada" para um usuário específico. Normalmente, o conteúdo das mailables não é relevante para o código que você está testando, e basta verificar que o Laravel foi instruído a enviar uma determinada mailable.

Você pode usar o método `fake` da facade `Mail` para impedir que e-mails sejam enviados. Depois de chamar o método `fake` da facade `Mail`, você pode verificar se mailables foram solicitadas para envio a usuários e até inspecionar os dados que as mailables receberam:

```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // Perform order shipping...

    // Assert that no mailables were sent...
    Mail::assertNothingSent();

    // Assert that a mailable was sent...
    Mail::assertSent(OrderShipped::class);

    // Assert a mailable was sent twice...
    Mail::assertSent(OrderShipped::class, 2);

    // Assert a mailable was sent to an email address...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // Assert a mailable was sent to multiple email addresses...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // Assert a mailable was not sent...
    Mail::assertNotSent(AnotherMailable::class);

    // Assert a mailable was sent twice...
    Mail::assertSentTimes(OrderShipped::class, 2);

    // Assert that a mailable was sent exactly once...
    Mail::assertSentOnce(OrderShipped::class);

    // Assert 3 total mailables were sent...
    Mail::assertSentCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Mail::fake();

        // Perform order shipping...

        // Assert that no mailables were sent...
        Mail::assertNothingSent();

        // Assert that a mailable was sent...
        Mail::assertSent(OrderShipped::class);

        // Assert a mailable was sent twice...
        Mail::assertSent(OrderShipped::class, 2);

        // Assert a mailable was sent to an email address...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // Assert a mailable was sent to multiple email addresses...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // Assert a mailable was not sent...
        Mail::assertNotSent(AnotherMailable::class);

        // Assert a mailable was sent twice...
        Mail::assertSentTimes(OrderShipped::class, 2);

        // Assert that a mailable was sent exactly once...
        Mail::assertSentOnce(OrderShipped::class);

        // Assert 3 total mailables were sent...
        Mail::assertSentCount(3);
    }
}
```

Se você estiver enfileirando mailables para envio em segundo plano, deve usar o método `assertQueued` em vez de `assertSent`:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertQueuedOnce(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```

Você também pode verificar o número total de mailables que foram enviadas ou enfileiradas usando o método `assertOutgoingCount`:

```php
Mail::assertOutgoingCount(3);
```

Você pode passar uma closure para os métodos `assertSent`, `assertNotSent`, `assertQueued` ou `assertNotQueued` para verificar se uma mailable foi enviada e atende a um determinado "teste de verdade". Se pelo menos uma mailable enviada atender ao teste fornecido, a asserção será bem-sucedida:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

Ao chamar os métodos de asserção da facade `Mail`, a instância de mailable aceita pela closure fornecida expõe métodos úteis para examinar a mailable:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...') &&
           $mail->hasMetadata('order_id', $mail->order->id) &&
           $mail->usesMailer('ses');
});
```

A instância de mailable também inclui vários métodos úteis para examinar os anexos de uma mailable:

```php
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```

Você deve ter notado que existem dois métodos para verificar que um e-mail não foi enviado: `assertNotSent` e `assertNotQueued`. Às vezes, você pode querer verificar que nenhum e-mail foi enviado **ou** enfileirado. Para isso, você pode usar os métodos `assertNothingOutgoing` e `assertNotOutgoing`:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a id="mail-and-local-development"></a>
## E-mail e Desenvolvimento Local

Ao desenvolver uma aplicação que envia e-mails, provavelmente você não quer enviar e-mails de verdade para endereços reais. O Laravel oferece várias maneiras de "desativar" o envio real de e-mails durante o desenvolvimento local.

<a id="log-driver"></a>
#### Driver de Log

Em vez de enviar seus e-mails, o driver de e-mail `log` gravará todas as mensagens de e-mail nos seus arquivos de log para inspeção. Normalmente, esse driver só seria usado durante o desenvolvimento local. Para mais informações sobre como configurar sua aplicação por ambiente, consulte a [documentação de configuração](/en/configuration/#environment-configuration).

<a id="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

Alternativamente, você pode usar um serviço como [HELO](https://usehelo.com) ou [Mailtrap](https://mailtrap.io) e o driver `smtp` para enviar suas mensagens de e-mail para uma caixa de correio "fictícia", onde você pode visualizá-las em um cliente de e-mail de verdade. Essa abordagem tem a vantagem de permitir inspecionar os e-mails finais no visualizador de mensagens do Mailtrap.

Se você estiver usando o [Laravel Sail](/en/sail/), pode visualizar suas mensagens usando o [Mailpit](https://github.com/axllent/mailpit). Quando o Sail estiver em execução, você pode acessar a interface do Mailpit em: `http://localhost:8025`.

<a id="using-a-global-to-address"></a>
#### Usando um Endereço `to` Global

Por fim, você pode especificar um endereço "to" global invocando o método `alwaysTo` oferecido pela facade `Mail`. Normalmente, esse método deve ser chamado a partir do método `boot` de um dos service providers da sua aplicação:

```php
use Illuminate\Support\Facades\Mail;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```

Ao usar o método `alwaysTo`, quaisquer endereços "cc" ou "bcc" adicionais nas mensagens de e-mail serão removidos.

<a id="events"></a>
## Eventos

O Laravel dispara dois eventos ao enviar mensagens de e-mail. O evento `MessageSending` é disparado antes de uma mensagem ser enviada, enquanto o evento `MessageSent` é disparado depois que a mensagem foi enviada. Lembre-se de que esses eventos são disparados quando o e-mail está sendo *enviado*, e não quando ele é enfileirado. Você pode criar [listeners de eventos](/en/events/) para esses eventos dentro da sua aplicação:

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * Handle the event.
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```

<a id="custom-transports"></a>
## Transports Personalizados

O Laravel inclui vários transports de e-mail; no entanto, você pode querer escrever seus próprios transports para entregar e-mails por meio de outros serviços que o Laravel não suporta nativamente. Para começar, defina uma classe que estenda a classe `Symfony\Component\Mailer\Transport\AbstractTransport`. Em seguida, implemente os métodos `doSend` e `__toString` no seu transport:

```php
<?php

namespace App\Mail;

use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Create a new Mailchimp transport instance.
     */
    public function __construct(
        protected ApiClient $client,
    ) {
        parent::__construct();
    }

    /**
     * {@inheritDoc}
     */
    protected function doSend(SentMessage $message): void
    {
        $email = MessageConverter::toEmail($message->getOriginalMessage());

        $this->client->messages->send(['message' => [
            'from_email' => $email->getFrom(),
            'to' => collect($email->getTo())->map(function (Address $email) {
                return ['email' => $email->getAddress(), 'type' => 'to'];
            })->all(),
            'subject' => $email->getSubject(),
            'text' => $email->getTextBody(),
        ]]);
    }

    /**
     * Get the string representation of the transport.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```

Depois de definir seu transport personalizado, você pode registrá-lo por meio do método `extend` oferecido pela facade `Mail`. Normalmente, isso deve ser feito dentro do método `boot` do `AppServiceProvider` da sua aplicação. Um argumento `$config` será passado para a closure fornecida ao método `extend`. Esse argumento conterá o array de configuração definido para o mailer no arquivo de configuração `config/mail.php` da sua aplicação:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        $client = new ApiClient;

        $client->setApiKey($config['key']);

        return new MailchimpTransport($client);
    });
}
```

Depois que seu transport personalizado estiver definido e registrado, você pode criar uma definição de mailer no arquivo de configuração `config/mail.php` da sua aplicação que utilize o novo transport:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```

<a id="additional-symfony-transports"></a>
### Transports Adicionais do Symfony

O Laravel oferece suporte a alguns transports de e-mail mantidos pelo Symfony, como Mailgun e Postmark. No entanto, você pode querer estender o Laravel com suporte a transports adicionais mantidos pelo Symfony. Você pode fazer isso instalando o mailer do Symfony necessário via Composer e registrando o transport no Laravel. Por exemplo, você pode instalar e registrar o mailer do Symfony "Brevo" (antigamente "Sendinblue"):

```shell
composer require symfony/brevo-mailer symfony/http-client
```

Depois que o pacote do mailer Brevo estiver instalado, você pode adicionar uma entrada com suas credenciais de API do Brevo ao arquivo de configuração `services` da sua aplicação:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```

Em seguida, você pode usar o método `extend` da facade `Mail` para registrar o transport no Laravel. Normalmente, isso deve ser feito dentro do método `boot` de um service provider:

```php
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('brevo', function () {
        return (new BrevoTransportFactory)->create(
            new Dsn(
                'brevo+api',
                'default',
                config('services.brevo.key')
            )
        );
    });
}
```

Depois que o seu transport estiver registrado, você pode criar uma definição de mailer no arquivo de configuração `config/mail.php` da sua aplicação que utilize o novo transport:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```

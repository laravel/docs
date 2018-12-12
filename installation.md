# Install ပြုလုပ်ခြင်း


- [Install ပြုလုပ်ခြင်း](#installation)
    - [Server လိုအပ်ချက်များ](#server-requirements)
    - [Laravel ကို Install ပြုလုပ်ခြင်း](#installing-laravel)
    - [Configuration](#configuration)
- [Web Server Configuration](#web-server-configuration)
    - [URL လှလှလေးလိုချင်တယ်](#pretty-urls)

<a name="installation"></a>
## Install ပြုလုပ်ခြင်း

> {video} Laracasts provides a [free, thorough introduction to Laravel](http://laravelfromscratch.com) for newcomers to the framework. It's a great place to start your journey.

<a name="server-requirements"></a>
### Server လိုအပ်ချက်များ

Laravel framework မှာ system လိုအပ်ချက်တစ်ချို့ရှိပါတယ်။ ထိုလိုအပ်ချက်များကိုဖြည့်ဆည်းပေးဖို့ Laravel မှပြုလုပ်ထားတဲ့ virtual machine [Laravel Homestead](/docs/{{version}}/homestead) တစ်ရှိပါတယ်၊ ဒါကြောင့်မလို့ သင့် Local Development အတွက် Homestead ကိုအသုံးပြုဖို့အကြံပြုထောက်ခံပါသည်။

သို့သော်လည်း သင်က Homestead မသုံးလိုဘူးဆိုလျှင် သင့် server ကအောက်ဖော်ပြပါ လိုအပ်ချက်များနှင့်ကိုက်ညီပါသလားဆိုတာကိုကြည့်ရမှာဖြစ်ပါတယ် -

<div class="content-list" markdown="1">
- PHP >= 7.1.3
- OpenSSL PHP Extension
- PDO PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension
- Ctype PHP Extension
- JSON PHP Extension
- BCMath PHP Extension
</div>

<a name="installing-laravel"></a>
### Laravel အား Install ပြုလုပ်ခြင်း

Laravel က dependencies တွေကိုစီမံခန့်ခွဲဖို့ရာအတွက် [Composer](https://getcomposer.org) ကိုအသုံးပြုပါသည်။ ထို့ကြောင့် Laravel ကိုအသုံးမပြုခင် သင့်စက်မှာ Composer အရင်ဆုံး install လုပ်ထားရပါ့မည်။

#### Laravel Installer မှတစ်ဆင့် Install ပြုလုပ်ခြင်း

ပထမဦးစွာ အောက်ဖော်ပြပါ command အတိုင်း Composer အသုံးပြုပြီး Laravel installer ကို download လုပ်ပါ - 

    composer global require laravel/installer

Composer ရဲ့ vendor directory ကို system-wide bin directory ဖြစ်အောင်အောက်ဖော်ပြပါ code ကို သင့်ရဲ့ PATH ဖြစ်တဲ့ `~/.bash_profile` သို့မဟုတ် `~/.bashrc` မှာကူးယူထည့်သွင်းပါ။ ထို့နောက် `source ~/.bash_profile` သို့မဟုတ် `soruce ~/.bashrc` ဆိုပြီး active လုပ်ပေးလိုက်ပါ။

```
export PATH=~/.composer/vendor/bin:$PATH
```

Install လုပ်လို့ပြီးသွားပြီဆိုလျှင်၊ `laravel new` command က laravel installation အသစ်စက်စက်တစ်ခုကို သင်သတ်မှတ်တဲ့ directory မှာ install လုပ်မှာဖြစ်ပါတယ်။ ဥပမာအားဖြင့် `laravel new blog` က `blog` ဆိုတဲ့ directory ထဲမှာ Laravel ရဲ့လိုအပ်တဲ့ depencies တွေနှင့်အတူ laravel ကို install လုပ်သွားမှာဖြစ်ပါတယ် -

    laravel new blog


#### Composer Create-Project မှတစ်ဆင့် Install ပြုလုပ်နည်း

နောက်တစ်နည်းအားဖြင့် Composer ရဲ့ `create-project` command ကိုအသုံးပြုပြီးတော့ install ပြုလုပ်နိုင်ပါတယ် -

    composer create-project --prefer-dist laravel/laravel blog

#### Local Development Server

သင့်စက်မှာ PHP install ပြုလုပ်ထားပြီးလျှင် PHP ရဲ့ built-in ပါတဲ့ development server ကိုအသုံးပြုပြီးတော့ သင့် application ကို serve လုပ်နိုင်ပါတယ်။ server command က development server ကို `http://localhost:8000` မှာစတင်စေမှာဖြစ်ပါတယ် - 

    php artisan serve

ဒါပေါ့ပိုမိုအားကောင်းတဲ့ development options တွေဖြစ်တဲ့ [Homestead](/docs/{{version}}/homestead) နှင့် [Valet](/docs/{{version}}/valet) တို့လည်းရှိပါတယ်။

<a name="configuration"></a>
### Configuration

#### Public Directory

သင် Laravel ကို install လုပ်ပြီးတဲ့အခါမှာတော့ သင့် web server ရဲ့ document / web root ကို `public` directory ကို configure ဖို့လိုအပ်ပါ့မည်။ public directory ထဲမှာရှိတဲ့ `index.php` က သင့် application ဆီလာတဲ့ HTTP requests တွေအားလုံးရဲ့ front controller အဖြစ် serve လုပ်မှာဖြစ်ပါတယ်။

#### Configuration Files

Laravel framework ရဲ့ configuration files တွေအားလုံးဟာ `config` directory ထဲမှာ store လုပ်ထားမှာဖြစ်ပါတယ်။ Option တစ်ခုချင်းဆီအတွက်ဘာလုပ်ရမလဲဆိုတာအားလုံးရေးထားပြီးသားဖြစ်တဲ့အတွက် options တွေနှင့်ရင်းနှီးသွားအောင် စိတ်ကြိုက် files တွေဆီသွားပြီးမွှေနှောက်ကြည့်လိုက်ပါတော့။

#### Directory Permissions

Laravel ကို install လုပ်ပြီးတဲ့အခါမှာတော့ permission တစ်ချို့ configure ဖို့လိုအပ်ပါလိမ့်မယ်။ `storage` directory နှင့် `bootstrap/cache` directory တွေကို web server သို့မဟုတ် Laravel မှာ writable ဖြစ်ဖို့လိုအပ်ပါ့မယ် အဲ့လိုမဟုတ်လျှင် Laravel က Run မှာမဟုတ်ပါဘူး။ သင်က Homestead](/docs/{{version}}/homestead) virtual machine သုံးတယ်ဆိုလျှင် ထို permissions တွေကအဆင်သင့်ပြင်ဆင်ပြီးသားပါ။

#### Application Key

Laravel ကို install လုပ်ပြီးနောက်ထပ်အဓိကလုပ်သင့်တာကတော့ သင့် application key ရဲ့ random string ကို set လုပ်တာပါဘဲ။  သင်က Laravel ကို Laravel Installer ကနေ သို့မဟုတ် Composer ကနေ install လုပ်ထားတာဆိုလျှင် `php artisan key:generate` command ကိုသုံးပြီးတော့ အဲ့ဒီ့ key ကသင့်အတွက် set လုပ်ထားပြီးပါပြီ။

ပုံမှန်အားဖြအဲ့ key က 32 charaters ရှိပါတယ်။ `.env` ထဲမှာအဲ့ဒီ့ key ကို set လုပ်နိုင်ပါတယ်။ သင်က `.env.example` ကို `.env` အဖြစ်အမည်မပြောင်းရသေးလျှင်အခုဘဲပြောင်းသင့်ပါတယ်။ **application key က set မလုပ်ရသေးဘူးဆိုလျှင် သင့် user ရဲ့ session သို့မဟုတ် encrypted data တွေကခြုံမှာမဟုတ်ပါဘူး။**

#### အပိုဆောင်း Configuration များ 

Laravel မှာတစ်ခြား configuration ထွေထွေထူးထူးလုပ်စရာမလိုပါဘူး။ သင့်စိတ်ကြိုက် development စတင်နိုင်ပါပြီ။ သို့သော်လည်း `config/app.php` fille နှင့် ထို file ထဲက documencation ကို သင်ပြန်လည်သုံးသပ်ဖို့လိုအပ်ပါလိမ့်မယ်။ အဲ့ဒီ့ file မှာ options တွေများစွာပါဝင်ပါတယ်။ ဥပမာ `timezone` နှင့် `locale` တို့လိုသင့် Application ပေါ်မူတည်ပြီးပြောင်းနိုင်တာမျိုးတွေပေါ့။ 

သင့်အနေဖြင့် Laravel ၏နောက်ထပ်အစိတ်အပိုင်းများကို configure လုပ်ချင်လုပ်နိုင်ပါတယ်၊ ဥပမာ - 

<div class="content-list" markdown="1">
- [Cache](/docs/{{version}}/cache#configuration)
- [Database](/docs/{{version}}/database#configuration)
- [Session](/docs/{{version}}/session#configuration)
</div>

<a name="web-server-configuration"></a>
## Web Server Configuration

<a name="pretty-urls"></a>
### URL လှလှလေးလိုချင်တယ်

#### Apache မှာဆို URL အောင်ဘယ်လိုလုပ်လို့ရမလဲ

Framework ထဲက `public/.htaccess` ကို URL မှာ `index.php` မပါအောင်ဖျောက်ထားပေးမှာဖြစ်ပါတယ်။ တကယ်လို့သင့် ရဲ့ Laravel application က Apache ကိုသုံးတယ်ဆိုရင် mod_rewrite ကို enable လုပ်ဖို့မမေ့ပါနဲ့ဦး။

တကယ်လို့ `.htaccess` file က သင့် Application မှာအလုပ်မလုပ်ဘူးဆိုရင် အောက်ကတစ်ခုကိုစမ်းကြည့်လိုက်ပါ:

    Options +FollowSymLinks -Indexes
    RewriteEngine On

    RewriteCond %{HTTP:Authorization} .
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^ index.php [L]

#### Nginx

Nginx မှာဆိုရင်အောက်ကညွှန်ကြားချက်ကို လိုက်လုပ်လိုက်တာနဲ့ URL လှလှလေးတွေရပါတယ်

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

သင်က [Homestead](/docs/{{version}}/homestead) တို့ [Valet](/docs/{{version}}/valet)တို့သုံးတာဆိုလျှင် URL လှလှလေးဖြစ်ဖို့လုပ်ပြီးသားပါ။

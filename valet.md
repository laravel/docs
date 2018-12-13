# Laravel Valet

- [Introduction](#introduction)
- [Valet Or Homestead](#valet-or-homestead)
- [Installation](#installation)
- [Upgrading](#upgrading)
- [Serving Sites](#serving-sites)
- [The "Park" Command](#the-park-command)
- [The "Link" Command](#the-link-command)
- [Securing Sites With TLS](#securing-sites)
- [Sharing Sites](#sharing-sites)
- [Custom Valet Drivers](#custom-valet-drivers)
- [Local Drivers](#local-drivers)
- [Other Valet Commands](#other-valet-commands)

<a name="introduction"></a>
## Introduction

Valet ဆိုသည်မှာ Mac အတွက် ရိုးရှင်းသော Laravel Development environment ဖြစ်ပါတယ်။ Vargrant အသုံးပြုရန်မလိုအပ်သလို '/etc/hosts' ဖိုင်များမလိုအပ်ပါ။ သင့်ရဲ့ site များကို local tunnel များအသုံးပြုပြီး အခြားသူများကို မ ျှဝေလို့ရပါတယ်။ ကျွန်တော်တို့လဲ နှစ်သက်ပါတယ်။

Laravel Valet ဟာ သင်ရဲ့စက်ဖွင့်လိုက်တာနဲ့ [Nginx](https://www.nginx.com/) ကိုနောက်ကွယ်ကနေ အမြဲ run နေအောင် ပြုလုပ်ပေးထားပါတယ်။ ထို့နောက်မှာ [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq) ကိုအသုံးပြုပြီး သင့်ရဲ့ site များကို `*.test` domain နဲ့ ချိတ်ဆက်ပေးထားပါတယ်။

အခြားနည်းနဲ့ပြောရရင် Ram 7MB လောက်အသုံးပြုပြီး Laravel Developemnt environment အတွက် မြန်ဆန်အောင်ပြုလုပ်ပေးထားတာပါ။ Valet ဟာ Vagrant သို့မဟုတ် Homestead တို့ကိုအစားထိုးဖို့လောက်အထိတော့ ပြီးပြည့်စုံမှုမရှိပါဘူး။ ဒါပေမယ့် အခြေခံလိုအပ်ချက်တွေ အတွက်အသုံးပြုရတာလွယ်ကူချင်ရင်၊ speed မြန်မြန် ဒါမှမဟုတ် Ram Limit ရှိတဲ့ စက်တွေအတွက်တော့ ကောင်းမွန်တဲ့ ရွေးချယ်မှုပါ။

အောက်ပါအရာများကတော့ Valet Support ပေးတာတွေပါ။ ဒါတွေပဲလို့ ကန့်သတ်ထားတာတော့မဟုတ်ပါဘူး။

<div class="content-list" markdown="1">
- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [Jigsaw](http://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)
</div>

However, you may extend Valet with your own [custom drivers](#custom-valet-drivers).
သင့်ရဲ့ [ကိုယ်ပိုင် drivers](#custom-valet-drivers) တွေကို အသုံးပြုပြီး Valet ကိုထပ်မံ တိုးချဲ့နိုင်ပါတယ်။

<a name="valet-or-homestead"></a>
### Valet လား Homestead

အားလုံးသိကြတဲ့အတိုင်းပါပဲ, Laravel က [Homestead](/docs/{{version}}/homestead) နဲ့လဲ local Laravel development environment တည်ဆောက်လို့ရပါတယ်။ Homestead နဲ့ Valet က local development အတွက် ဦးတည်ရာရည်ရွယ်ချက်များပေါ်မူတည်ပြီး ကွဲပြားပါတယ်။ Homestead ဟာ Nginx configuration တွေကို အသင့်ပါတဲ့ Ubuntu Virtual machine တစ်ခု တည်ဆောက်ပေးပါတယ်။ သင့်ရဲ့ Window/Linux system မှာ ပြည့်စုံတဲ့ Linux development environment တစ်ခုလိုချင်တယ်ဆိုရင်တော့ Homestead ဟာ ကောင်းမွန်တဲ့ရွေးချယ်မှုပါပဲ။ 

Valet ဟာ Mac အတွက်ပဲသီးသန့်အထောက်အပံ့ပေးတာပါ။ ပြီးတော့ သင့်ရဲ့စက်ထဲကို PHP နဲ့ database server install လုပ်ဖို့လိုအပ်ပါတယ်။ ဒါတွေကို [Homebrew](http://brew.sh/) ရဲ့ commands တွေဖြစ်တဲ့ `brew install php` နဲ့ `brew install mysql` တို့ကို အသုံးပြုပြီး လွယ်ကူစွာ ထည့်သွင်းနိုင်ပါတယ်။ Valet က resource အနည်းဆုံးအသုံးပြုပြီး local development ကို အမြန်ဆန်ဆုံးဖြစ်အောင်စွမ်းဆောင်ပေးနိုင်ပါတယ်။ ဒါကြောင့်မို့ အရမ်းပြည့်စုံတဲ့ development environment မျိုးမဟုတ်ပဲ PHP/MySQL လောက်ပဲ အသုံးပြုမယ့် developer တွေအတွက် ကောင်းမွန်စေပါတယ်။ 

Valet နဲ့ Homestead နှစ်မျိုးလုံးဟာ သင့်ရဲ့ Laravel development environment တည်ဆောက်မှုအတွက် ကောင်းမွန်တဲ့ ရွေးချယ်မှုပါ။ သင့်နှစ်သက်ရာ ၊ သင့်ရဲ့ team လိုအပ်ချက်ပေါ်မူတည်ပြီး နှစ်သက်ရာရွေးချယ်နိုင်ပါတယ်။ 

<a name="installation"></a>
## Install ပြုလုပ်ခြင်း

**Valet ထည့်သွင်းဖို့အတွက် macOS နဲ့ [Homebrew](http://brew.sh/) လိုအပ်ပါတယ်။ installation မပြုလုပ်ခင်မှာ သင့်ရဲ့စက်မှာ Apache သို့မဟုတ် Nginx အစရှိတဲ့ program တွေက port 80 ကိုအသုံးပြုထားခြင်း ရှိ၊မရှိ ဦးစွာစစ်ဆေးပါ။**

<div class="content-list" markdown="1">
- `brew update` command ကိုအသုံးပြုပြီး [Homebrew](http://brew.sh/) နောက်ဆုံး version ရရှိစေရန် install သို့မဟုတ် update ပြုလုပ်ပါ။
- Homebrew မှတစ်ဆင့် `brew install php@7.2` command ကို အသုံးပြုပြီး PHP 7.2 ကို install လုပ်ပါ။
[Composer](https://getcomposer.org) install လုပ်ပါ။
- `~/.composer/vendor/bin` directory ကို သင့် system ရဲ့ "PATH" မှာရှိအောင် ပြုလုပ်ထားပါ။ ထို့နောက် Composer မှတစ်ဆင့် `composer global require laravel/valet` command ကိုအသုံးပြုပြီး Valet ကို install လုပ်ပါ။ 
- `valet install` command ကို Run ခြင်းဖြင့် Valet နဲ့ DnMasq ကို install ပြုလုပ်ပြီး သင့်ရဲ့ system စတင်တာနဲ့ Valet ကို အလုပ်လုပ်စေမှာဖြစ်ပါတယ်။
</div>

Valet ကို install လုပ်ပြီးလ ျှင် terminal မှာ `*.test` နဲ့ domain တစ်ခုခုကို ping ကြည့်ပါ။ ဥပမာ `ping foobar.test`။ တကယ်လို့ Valet သာ မှန်မှန်ကန်ကန် install လုပ်သွားတယ်ဆိုရင် သင့်ရဲ့ domain က `127.0.0.1` မှာ respond လုပ်မှာဖြစ်ပါတယ်။

Valet ဟာ သင့်ရဲ့စက် boot လုပ်တာနဲ့ သူ့ရဲ့ လုပ်ဆောင်ချက်တွေကို အလိုအလျောက် စတင်ပါတယ်။ Valet ကို တစ်ခါပြည့်စုံစွာ install လုပ်ပြီးတာနဲ့ `valet start` သို့မဟုတ် `valet install` တို့လို command တွေကို ထပ်ရိုက်စရာမလိုတော့ပါဘူး။

#### အခြား Domain ပြောင်းလဲအသုံးပြုခြင်း

ပုံသေအားဖြင့် Valet က သင့်ရဲ့ project မှာ `.test` TLD အသုံးပြုအောင် လုပ်ဆောင်ပေးထားပါတယ်။ တကယ်လို့ သင်ဟာ အခြား domain တစ်ခုခု အသုံးပြုချင်တယ်ဆိုရင် `valet domain tld-name` command ကိုအသုံးပြုပြီး ပြောင်းလဲနိုင်ပါတယ်။

ဥပမာအားဖြင့် သင်က `.test` အစား `.app` သုံးချင်တယ်ဆိုရင် `valet domain app` command ကို run လိုက်တာနဲ့ Valet က သင့်ရဲ့ project ကို `*.app` မှာ အသုံးပြုလို့ရအောင် အလိုအလေ ျှာက်ပြောင်းလဲပေးပါတယ်။

#### Database

သင်ဟာ database သုံးဖို့ လိုအပ်တယ်ဆိုရင် `brew install mysql@5.7` ကို command line မှာ run ပြီး install လုပ်နိုင်ပါတယ်။ MySQL install လုပ်ပြီးပြီဆိုရင် `brew services start mysql@5.7` command ကိုသုံးပြီး server start နိုင်ပါတယ်။ ထို့နောက် `127.0.0.1` မှာ root usernme နဲ့ password ကို အလွတ်ထားပြီး database ကို ချိတ်ဆက်နိုင်ပါတယ်။

<a name="upgrading"></a>
### Upgrading

Terminal မှာ `composer global update` command ကို run ပြီး valet installation ကို update လုပ်နိုင်ပါတယ်။ upgrade လုပ်ပြီးရင် `valet install` command ကို run ခြင်းအားဖြင့် Valet ဟာ လိုအပ်ရင် သင့်ရဲ့ configuration file တွေကို ဖြည့်စွက် upgrade လုပ်ပေးနိုင်ပါတယ်။

#### Valet 2.0 သို့ upgrade လုပ်ခြင်း

Valet 2.0 ကိုပြောင်းတဲ့အခါမှာ Valet ဟာ အခြေခံ web server ကို Caddy မှ Nginx သို့ပြောင်းလဲခဲ့ပါတယ်။ version 2.0 ကို upgrade မလုပ်ခင်မှာ အောက်ပါ command များကို run ပြီး ရှိနှင့်ပြီးသား Canddy ကိုအသုံးပြုထားတဲ့ လုပ်ဆောင်ချက်များကို stop and uninstall ပြုလုပ်ပါ။ 


valet stop
valet uninstall

ထို့နောက် Valet ရဲ့ နောက်ဆုံး version ကို upgrade လုပ်နိုင်ပါသည်။ Valet ကို install လုပ်တဲ့ပေါ်မှာ မူတည်ပြီး Git သို့မဟုတ် composer ကို အသုံးပြုသွားမှာဖြစ်ပါတယ်။ သင်ဟာ composer ကို အသုံးပြုပြီး install လုပ်မယ်ဆိုရင် အောက်ပါ command ကို အသုံးပြုပြီး composer ရဲ့ နောက်ဆုံး major version ကို ရယူနိုင်ပါတယ်။

composer global require laravel/valet

ထို့နောက် အောက်ပါ`install` command တွေကို သုံးပြီး valet ရဲ့ source code အသစ်ကို download ရယူနိုင်ပါတယ်။

valet install
valet restart

Upgrade လုပ်ပြီးလ ျှင် သင့်ရဲ့ site များကို re-park သို့မဟုတ် re-link လုပ်ပေးရန်လိုအပ်နိုင်ပါတယ်။ 

<a name="serving-sites"></a>
## Site များကို serving ပြုလုပ်ခြင်း

Valet install ပြီးလ ျှင်တော့ sites များကို စတင်ဖို့ အဆင်သင့်ဖြစ်ပါပြီ။ `park` and `link` command နှစ်ခုကို အသုံးပြုပြီး သင့်ရဲ့ Laravel site တွေကို စတင်အသုံးပြုလို့ရအောင် Valet က ဆောင်ရွက်ပေးပါတယ်။

<a name="the-park-command"></a>
**`park` Command အသုံးပြုခြင်း**

<div class="content-list" markdown="1">
- သင့်ရဲ့ Mac မှာ new directory အသစ်ဆောက်ပါ။ ဥပမာ `mkdir ~/Sites`။ ထို့နောက် `cd ~/Sites`။ ပြီးလ ျှင် `valet park` အား run ခြင်းဖြင့် သင့်ရဲ့ လက်ရှိ working directory ရှိ site များကို Valet လုပ်ဆောင်ချက်များ ရရှိစေမှာဖြစ်ပါတယ်။
- ထို့နောက် Laravel site အသစ်တစ်ခုကို အထက်ပါ directory တွင် create လုပ်ပါ။ ဥပမာ `laravel new blog`။
- သင့်ရဲ့ browser မှာ `http://blog.test` ကိုဖွင့်ပါ။
</div>

အထက်ပါလုပ်ဆောင်ချက်များ ပြီးစီးပါက သင့်ရဲ့ "parked" directory မှာရှိတဲ့ Laravel project တွေက `http://folder-name.test` လိုမျိုး အလိုအလေ ျှာက် serve လုပ်ပေးမှာဖြစ်ပါတယ်။

<a name="the-link-command"></a>
**`link` Command အသုံးပြုခြင်း**

`link` command ကိုလဲ သင့်ရဲ့ laravel site တွေ serve လုပ်ဖို့အသုံးပြုနိုင်ပါတယ်။ အဲ့ဒီ့ command က သင်က directory တစ်ခုလုံးမဟုတ်ပဲ directory ထဲက site တစ်ခုတည်းကို serve လုပ်ချင်တဲ့အခါမှာ အသုံးဝင်ပါတယ်။

<div class="content-list" markdown="1">
- ဒီ command ကိုသုံးဖို့အတွက် terminal မှာ သင့်ရဲ့ သက်ဆိုင်ရာ project ကို ညွှန်းပြီး `valet link app-name` ဟုအသုံးပြုနိုင်ပါသည်။ Valet ဟာ သင့်ရဲ့ working directory ကို point ထားတဲ့ `~/.config/valet/Sites` မှာ အမှတ်အသား Link တစ်ခု အဖြစ် create လုပ်ပေးသွားမှာဖြစ်ပါတယ်။
-`link` command ကို run ပြီးလ ျှင် သင့် browser မှာ `http://app-name.test` ဖြင့် access လုပ်လို့ရပါပြီ။
</div>

သင့်စက်ထဲရှိ valet နှင့်ချိတ်ဆက်ထားသော directory များကို `valet links` command အား run ခြင်းဖြင့် ကြည့်ရှုနိုင်ပါတယ်။ ချိတ်ဆက်ထားသော project အား valet နှင့် ချိတ်ဆက်ထားခြင်းမှပယ်ဖျက်ရန် `valet unlink app-name` command အား အသုံးပြုနိုင်ပါတယ်။

> {မှတ်ချက်} `valet link` command အား project တစ်ခုတည်းကို multiple (sub)domains များ serve လုပ်ရန်အတွက်လဲ သုံးနိုင်ပါတယ်။ subdomain သို့မဟုတ် အခြား domain ချိတ်ဆက်ရန် `valet link subdomain.app-name` command ကို သင့်ရဲ့ project folder directory မှာ run ရမှာဖြစ်ပါတယ်။

<a name="securing-sites"></a>
**Securing Sites With TLS**

ပုံသေအားဖြင့် Valet ဟာ site များကို plain HTTP ပေါ်မှာ serve လုပ်ပါတယ်။ တကယ်လို့ သင်က site တစ်ခုကို HTTP/2 အသုံးပြုထားတဲ့ encrypted TSL မှာ serve လုပ်ချင်တယ်ဆိုရင် `secure` command ကို အသုံးပြုနိုင်ပါတယ်။ ဥပမာ - သင့်ရဲ့ site ကို Valet က `laravel.test` မှာ serve လုပ်ထားတယ်ဆိုပါစို့၊ သင်ဟာ အောက်ပါ command ကို run ခြင်းဖြင့် သင့်ရဲ့ site ကို secure လုပ်နိုင်ပါတယ်။

valet secure laravel

site တစ်ခုကို plain HTTP ပေါ်မှာ serve လုပ်ဖို့အတွက် "unsecure" ပြန်လုပ်ချင်တယ်ဆိုရင် `unsecure` command ကို အသုံးပြုနိုင်ပါတယ်။ ဒီ command ဟာ `secure` command ကို အသုံးပြုသလိုပဲ သင် unsecure လုပ်ချင်တဲ့ host name ကို ထည့်ပေးရမှာဖြစ်ပါတယ်။

valet unsecure laravel

<a name="sharing-sites"></a>
## Sharing Sites

Valet ဟာ သင့်ရဲ့ စက်က local site တွေကိုတောင် ကမ္ဘာပေါ်မှာ မ ျှဝေလို့ရပါတယ်။ နောက်ထပ်အခြား software ထပ်ထည့်စရာမလိုပဲ valet ကိုတစ်ကြိမ်ထည့်သွင်းထားရုံနှင့် အဆိုပါလုပ်ဆောင်ချက်ကို ရရှိမှာဖြစ်ပါတယ်။

Site တစ်ခုကို မ ျှဝေဖို့အတွက် terminal မှာ သင့်ရဲ့ site directory ကိုညွှန်းပြီး `valet share` command ကို run ရမှာဖြစ်ပါတယ်။ သင့် site ကို မ ျှဝေသုံးစွဲနိုင်တဲ့ URL က clipboard မှာ ထည့်သွင်းသွားပြီး သင့်ရဲ့ browser မှာ paste လုပ်ပြီး ကြည့်ရှုနိုင်ဖို့ အဆင်သင့်ဖြစ်နေမှာပါ။

သင့် site ကို မ ျှဝေသုံးစွဲခွင့်ပြုခြင်းအား ရပ်ဆိုင်းဖို့အတွက် `Control + C` ကို နှိပ်ပြီး မ ျှဝေသုံးစွဲခြင်းအား ရပ်ဆိုင်းနိုင်ပါတယ်။

> {မှတ်ချက်} `valet share` command ဟာ အခုထိတော့ `valet secure` command အသုံးပြုပြီး လုံခြုံအောင်မပြုလုပ်ထားတဲ့ site တွေအတွက်တော့ အထောက်အပံ့ပေးမှာမဟုတ်ပါဘူး။

<a name="custom-valet-drivers"></a>
## Custom Valet Drivers

သင်ဟာ Valet က အထောက်အပံ့မပေးသေးတဲ့ Framework သို့မဟုတ် CMS တွေအသုံးပြုထားတဲ့ PHP application တွေအတွက် သင့်ရဲ့ ကိုယ်ပိုင် Valet "driver" ကိုပြုလုပ်နိုင်ပါတယ်။ သင် valet ကို install ပြုလုပ်ချိန်မှာ `SampleValetDriver.php` file ပါဝင်တဲ့ `~/.config/valet/Drivers` directory ကို တည်ဆောက်လိုက်ပြီးဖြစ်ပါတယ်။ အဆိုပါ file မှာ ကိုယ်ပိုင် driver တစ်ခု ဘယ်လိုတည်ဆောက်ရမလဲ ဆိုတာကို ရှင်းလင်းပြသထားတဲ့ ဥပမာ driver တစ်ခုပါဝင်ပါတယ်။ သင့်အနေနဲ့ ကိုယ်ပိုင် driver တစ်ခု တည်ဆောက်ဖို့အတွက် `serves`, `isStaticFile`, နဲ့ `frontControllerPath` ဆိုတဲ့ နည်းလမ်း ၃ မျိုးပဲ လုပ်ဆောင်ရမှာပါ။

အထက်ပါနည်းလမ်း ၃ မျိုးလုံးဟာ `$sitePath`, `$siteName`, နဲ့ `$uri` ဆိုတဲ့တန်ဖိုးတွေကို လက်ခံပါတယ်။ `$sitePath` ဆိုတာကတော့ သင့်ရဲ့ စက်မှာ serve လုပ်နေတဲ့ site ရဲ့ လမ်းကြောင်းအပြည့်အစုံပါ။ ဥပမာ - `/Users/Lisa/Sites/my-project`။ `$siteName` ဆိုတာကတော့ domain (`my-project`) ရဲ့ "host" / "site name" အပိုင်း ဖြစ်ပါတယ်။ `$uri` ကတော့ ဝင်လာမယ့် request ရဲ့ URI (`/foo/bar`) ဖြစ်ပါတယ်။

သင်ဟာ သင့်ရဲ့ ကိုယ်ပိုင် Valet driver ကိုတည်ဆောက်ပြီးပြီဆိုရင် `FrameworkValetDriver.php` ရဲ့ အမည်ပေးချက်များကို လိုက်နာပြီး `~/.config/valet/Drivers` directory  အောက်မှာ ထည့်သွင်းပါ။

ကိုယ်ပိုင် Valet driver အတွက် Method တစ်ခုခြင်းစီကို ဘယ်လိုတည်ဆောက်ရမလဲဆိုတာ သိဖို့အတွက် ဥပမာအနေနဲ့ တည်ဆောက်ထားတာကို ကြည့်ကြပါစို့။

#### The `serves` Method

သင့်ရဲ့ driver ဟာ ဝင်ရောက်လာတဲ့ request တွေကို ထိန်းချုပ်နိုင်တယ်ဆိုရင် `serves` method ဟာ `true` ကို return ပြန်သင့်ပါတယ်။ မဟုတ်ရင်တော့ `false` ကို return ပြန်ရမှာဖြစ်ပါတယ်။ ဒါကြောင့် method အတွင်းမှာ ပေးထားတဲ့ `$sitePath` မှာ သင် serve လုပ်ချင်တဲ့ project အမျိုးအစား ပါဝင်ခြင်းရှိမရှိ ဆုံးဖြတ်ဖို့ ကြိုးစားရမှာပါ။

ဥပမာအားဖြင့် ကျွန်တော်တို့ဟာ `WordPressValetDriver` ကိုရေးသားနေတယ် ဆိုကြပါစို့။ ကျွန်တော်တို့ ရဲ့ `serves` method ဟာ အောက်ပါအတိုင်းဖြစ်ရမှာပါ :

/**
* Determine if the driver serves the request.
*
* @param  string  $sitePath
* @param  string  $siteName
* @param  string  $uri
* @return bool
*/
public function serves($sitePath, $siteName, $uri)
{
return is_dir($sitePath.'/wp-admin');
}

#### The `isStaticFile` Method

`isStaticFile` method ဟာ image သို့မဟုတ် stylesheet လိုမျိုး "static" ဖြစ်တဲ့ file တွေ အတွက် ဝင်ရောက်လာတဲ့ request တွေအတွက် ဆုံးဖြတ်ရမှာဖြစ်ပါတယ်။ တကယ်လို့ file static ဖြစ်တယ်ဆိုရင် ဒီ method က သင့်စက်မှာရှိတဲ့ အဆိုပါ static file အတွက် မှန်ကန်ပြည့်စုံတဲ့ လမ်းကြောင်း(path) တစ်ခုကို return ပြန်ပေးမှာဖြစ်ပါတယ်။ တကယ်လို့ ဝင်လာတဲ့ request က static file မဟုတ်ဘူးဆိုရင် `false` အနေနဲ့ return ပြန်ပေးရပါမယ်: 

/**
* Determine if the incoming request is for a static file.
*
* @param  string  $sitePath
* @param  string  $siteName
* @param  string  $uri
* @return string|false
*/
public function isStaticFile($sitePath, $siteName, $uri)
{
if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
return $staticFilePath;
}

return false;
}

> {note} The `isStaticFile` method will only be called if the `serves` method returns `true` for the incoming request and the request URI is not `/`.
> {မှတ်ချက်} ဝင်လာတဲ့ request URI က `/` မဟုတ်လို့ `serve` method ဘက်က `ture` ဆိုပြီး return ပြန်လာတဲ့အခါမှသာ `isStaticFile` method ဟာ အလုပ်လုပ်မှာဖြစ်ပါတယ်။

#### The `frontControllerPath` Method

`frontControllerPath` method ဟာ ပြည့်စုံမှန်ကန်တဲ့ လမ်းကြောင်း(path) ကို သင့် application ရဲ့ "front controller" ဖြစ်တဲ့ "index.php" file သို့မဟုတ် အလားတူ file တစ်ခုခုကို retun ပြန်ပေးရမှာဖြစ်ပါတယ်။ 

/**
* Get the fully resolved path to the application's front controller.
*
* @param  string  $sitePath
* @param  string  $siteName
* @param  string  $uri
* @return string
*/
public function frontControllerPath($sitePath, $siteName, $uri)
{
return $sitePath.'/public/index.php';
}

<a name="local-drivers"></a>
### Local Drivers

တကယ်လို့ သင်ဟာ application တစ်ခုတည်းအတွက်ပဲ သင့်ရဲ့ ကိုယ်ပိုင် Valet driver ကို အသုံးပြုချင်တယ်ဆိုရင် သင့် application ရဲ့ root directory မှာ `LocalValetDriver.php` file ကို တည်ဆောက်ပါ။ သင့်ရဲ့ ကိုယ်ပိုင် driver ဟာ အခြေခံ `ValetDriver` class ဒါမှမဟုတ် `LaravelValetDriver` လိုမျိုး ရှိနှင့်ပြီးသား တိကျတဲ့ application driver လိုမျိုးကို extend လုပ်နိုင်ပါတယ်။ 

class LocalValetDriver extends LaravelValetDriver
{
/**
* Determine if the driver serves the request.
*
* @param  string  $sitePath
* @param  string  $siteName
* @param  string  $uri
* @return bool
*/
public function serves($sitePath, $siteName, $uri)
{
return true;
}

/**
* Get the fully resolved path to the application's front controller.
*
* @param  string  $sitePath
* @param  string  $siteName
* @param  string  $uri
* @return string
*/
public function frontControllerPath($sitePath, $siteName, $uri)
{
return $sitePath.'/public_html/index.php';
}
}

<a name="other-valet-commands"></a>
## Other Valet Commands

Command  | ရည်ရွယ်ချက်
------------- | -------------
`valet forget` | "parked" လုပ်ထားတဲ့ directory တစ်ခုကို parked directory စာရင်းကနေပယ်ဖျက်နိုင်ဖို့ အသုံးပြုရတဲ့ command ဖြစ်ပါတယ်။
`valet paths` | "parked" လုပ်ထားတဲ့ လမ်းကြောင်းတွေ(paths) အားလုံးကို ကြည့်နိုင်ရန်အတွက် command ဖြစ်ပါတယ်။
`valet restart` | Valet လုပ်ဆောင်ချက်များကို Restart လုပ်ပေးမှာဖြစ်ပါတယ်။
`valet start` | Valet လုပ်ဆောင်ချက်များကို Start လုပ်ပေးမှာဖြစ်ပါတယ်။
`valet stop` | Valet လုပ်ဆောင်ချက်များကို Stop လုပ်ပေးမှာဖြစ်ပါတယ်။
`valet uninstall` | Valet နှင့်တကွ လုပ်ဆောင်ချက်များကို Uninstall လုပ်ပေးမှာဖြစ်ပါတယ်။

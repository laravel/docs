# Laravel Homestead

- [簡介](#introduction)
- [安裝與設定](#installation-and-setup)
    - [前置動作](#first-steps)
    - [設定 Homestead](#configuring-homestead)
    - [啟動 Vagrant Box](#launching-the-vagrant-box)
    - [根據專案各別安裝](#per-project-installation)
    - [安裝 MariaDB](#installing-mariadb)
- [常見用法](#daily-usage)
    - [全域存取 Homestead](#accessing-homestead-globally)
    - [透過 SSH 連接](#connecting-via-ssh)
    - [連接資料庫](#connecting-to-databases)
    - [增加更多網站](#adding-additional-sites)
    - [設定 Cron 排程器](#configuring-cron-schedules)
    - [連接埠](#ports)
    - [分享你的環境](#sharing-your-environment)
- [網路介面卡](#network-interfaces)
- [更新 Homestead](#updating-homestead)
- [舊版本](#old-versions)
- [提供者個別設定](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 簡介

Laravel 致力於讓 PHP 開發體驗更愉快，也包含你的本地開發環境。[Vagrant](https://www.vagrantup.com) 提供了一個簡單、優雅的方式來管理與供應虛擬機器。

Laravel Homestead 是一個官方預載的 Vagrant box，提供你一個美好的開發環境，你不需要在你的本機電腦安裝 PHP、HHVM、網頁伺服器或任何伺服器軟體。不用擔心搞亂你的系統！Vagrant box 可以搞定一切。如果有什麼地方爛掉了，你可以在幾分鐘內快速的砍掉並重建虛擬機器！

Homestead 可以在任何 Windows、Mac 或 Linux 系統上面執行，裡面包含了 Nginx 網頁伺服器、PHP 7.1、MySQL、Postgres、Redis、Memcached、Node，以及所有你在使用 Laravel 開發各種精彩的應用程式時所需要的軟體。

> {note} 如果您是 Windows 的使用者，您可能需要啟用硬體虛擬化(VT-x)。這通常需要透過 BIOS 來啟用它。假如您使用的 Hyper-V 是在 UEFI 系統上，為了使用 VT-x 您可能需同時地禁用 Hyper-V。 

<a name="included-software"></a>
### 內建軟體	

- Ubuntu 16.04
- Git
- PHP 7.1
- Nginx
- MySQL
- MariaDB
- Sqlite3
- Postgres
- Composer
- Node (包含 Yarn, Bower, Grunt, 和 Gulp)
- Redis
- Memcached
- Beanstalkd
- Mailhog
- ngrok

<a name="installation-and-setup"></a>
## 安裝與設定

<a name="first-steps"></a>
### 前置動作

在啟動你的 Homestead 環境之前，你必須先安裝 [VirtualBox 5.1](https://www.virtualbox.org/wiki/Downloads) 或 [VMWare](https://www.vmware.com) 或 [Parallels](http://www.parallels.com/products/desktop/) 以及 [Vagrant](https://www.vagrantup.com/downloads.html)。這些軟體在各個常用的平台都有提供易用的視覺化安裝程式。

如果要使用Parallels，你需要安裝 [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels)。這是免費的。

#### 安裝 Homestead Vagrant Box

當 VirtualBox / VMware 以及 Vagrant 安裝完成後，你可以在終端機以下列指令將 `laravel/homestead` 這個 box 安裝進你的 Vagrant 程式中。下載 box 會花你一點時間，時間長短將依據你的網路速度決定：

    vagrant box add laravel/homestead

如果此指令執行失敗了，請確保你安裝的 Vargrant 是最新版。

#### 安裝 Homestead

你可以簡單地透過複製(clone)儲存庫的方式來安裝 Homestead。建議可將儲存庫複製至你的「home」目錄中的 `Homestead` 資料夾，如此一來 Homestead box 將能提供主機服務給你所有的 Laravel 專案：

    cd ~

    git clone https://github.com/laravel/homestead.git Homestead

你應該查看 Homestead 被tagged的版本，因為 `master` 分支不會總是處於穩定狀態，你可以在 
[Github Release Page] (https://github.com/laravel/homestead/releases)上找到最新的穩定版:

    cd Homestead

    // Clone the desired release...
    git checkout v4.0.5

當你複製完 Homestead 儲存庫，即可在 Homestead 目錄中執行 `bash init.sh` 指令來建立 `Homestead.yaml` 設定檔。 `Homestead.yaml` 檔案將會被放置在 Homestead 目錄中：

    // Mac / Linux...
    bash init.sh

    // Windows...
    init.bat

<a name="configuring-homestead"></a>
### 設定 Homestead

#### 設定提供者

在 `Homestead.yaml` 檔案中的 `provider` 是用來設定你想要使用哪一個 Vagrant 提供者，像是：`virtualbox`，`vmware_fusion`， `vmware_workstation`或 `parallels`。你可以根據喜好來決定提供者：

    provider: virtualbox

#### 設定共享目錄

你可以在 `Homestead.yaml` 檔案的 `folders` 屬性裡列出所有你想與 Homestead 環境共享的目錄。這些目錄中的檔案若有更動，它們將會同步更動在你的本機電腦與 Homestead 環境。你可以將多個共享目錄都設定於此：

    folders:
        - map: ~/Code
          to: /home/vagrant/Code

若要啟用 [NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html)，你只需要在共享目錄的設定值中加入一個簡單的參數：

    folders:
        - map: ~/Code
          to: /home/vagrant/Code
          type: "nfs"

你也可以透過 Vagrant's [Synced Folders](https://www.vagrantup.com/docs/synced-folders/basic_usage.html)，將想帶入的任何選項
列在 `options`關鍵字下方

    folders:
        - map: ~/Code
          to: /home/vagrant/Code
          type: "rsync"
          options:
              rsync__args: ["--verbose", "--archive", "--delete", "-zz"]
              rsync__exclude: ["node_modules"]


#### 設定 Nginx 網站

對 Nginx 不熟悉嗎？沒關係。`sites` 屬性幫助你可以輕易的指定「網域」對應至 homestead 環境中的目錄。在 `Homestead.yaml` 檔案中已包含一個網站設定範例。同樣的，你可以增加數個網站到 Homestead 環境中。Homestead 可以為每個你正在開發中的 Laravel 專案提供方便的虛擬化環境：

    sites:
        - map: homestead.app
          to: /home/vagrant/Code/Laravel/public

在配置 Homestead box 之後，若有更改 `sites` 屬性，你應該重新執行配置指令 `vagrant reload --provision`  來更新虛擬機裡的 Nginx 設定。

#### Hosts 檔案

你必須為 Nginx 網站在你機器中的 `hosts` 檔案增加「網域」。`hosts` 檔案會將你對 Homestead 網站的請求重導至 Homestead 機器。在 Mac 或 Linux 上，該檔案通常會存放在 `/etc/hosts`。在 Windows 上，則存放於 `C:\Windows\System32\drivers\etc\hosts`。你增加至該檔案的內容看起來會像這樣：

    192.168.10.10  homestead.app

務必確認 IP 位置與你的 `Homestead.yaml` 檔案中設定相同。一旦將網域設定在 `hosts` 檔案之後，你就可以透過網頁瀏覽器造訪網站！

    http://homestead.app

<a name="launching-the-vagrant-box"></a>
### 啟動 Vagrant Box

當你編輯完 `Homestead.yaml`後，開啟終端機，進入 Homestead 目錄，並執行 `vagrant up` 指令。Vagrant 就會自將虛擬主機啟動並自動設定共享目錄和 Nginx 網站。

如果要移除虛擬機器，可以使用 `vagrant destroy --force` 指令。

<a name="per-project-installation"></a>
### 根據專案各別安裝

有別於將 Homestead 安裝成全域環境且讓所有的專案共用同一個 Homestead box，你可以各別為每一個專案獨立配置一個 Homstead。如果你希望直接在專案裡傳遞 `Vagrantfile`，那麼替每個專案安裝 Homestead 即是你可以考慮的方式，這將會允許其他人可以簡單地執行 `vagrant up` 即能開始工作於此專案。

使用 Composer 將 Homestead 直接安裝至你的專案中：

    composer require laravel/homestead --dev

一旦 Homestead 安裝完畢，你可以使用 `make` 指令產生 `Vagrantfile` 與 `Homestead.yaml` 存放於專案的根目錄。這個 `make` 指令將會自動配置 `sites` 及 `folders` 於 `Homestead.yaml` .

Mac / Linux:

    php vendor/bin/homestead make

Windows:

    vendor\\bin\\homestead make

接著，在終端機中執行 `vagrant up` 指令，並透過網頁瀏覽器造訪 `http://homestead.app` 。再次提醒，你仍然需要在 `/etc/hosts` 裡設定 `homestead.app` 或其他想要使用的網域。

<a name="installing-mariadb"></a>
### 安裝 MariaDB

如果您偏好 MariaDB 而不是 MySQL，可以在 `Homestead.yaml` 檔案中加入 `mariadb` 選項。這選項會移除 MySQL 並同時安裝 MariaDB。 MariaDB 是 MySQL 的一個直接替代品，所以在你的環境設定中的資料庫驅動程式仍然需使用 `mysql`：

    box: laravel/homestead
    ip: "192.168.20.20"
    memory: 2048
    cpus: 4
    provider: virtualbox
    mariadb: true

<a name="daily-usage"></a>
## 常見用法

<a name="accessing-homestead-globally"></a>
### 全域存取 Homestead

有時你可能想從任何地方 `vagrant up` 你的 Homestead 機器。你可以在 Mac / Linux 上增加簡單的 Bash 函式至你的 Bash 設定檔來做到。 在 Windows 上，你可以添加一個 "batch" 檔案到你的 `PATH`。此函式會自動指到你的 Homestead 安裝位置，能讓你在系統的任何位置執行任意的 Vagrant 指令：

#### Mac / Linux

    function homestead() {
        ( cd ~/Homestead && vagrant $* )
    }

確保函式中 `~/Homestead` 路徑為你實際 Homestead 的安裝位置。一旦函式被設定後，你可以在系統的任何位置執行像是 `homestead up` 或 `homestead ssh` 的指令。

#### Windows

在你的機器上的任何地方建立一個 `homestead.bat` batch檔案，並包含以下內容:

    @echo off

    set cwd=%cd%
    set homesteadVagrant=C:\Homestead

    cd /d %homesteadVagrant% && vagrant %*
    cd /d %cwd%

    set cwd=
    set homesteadVagrant=

確認你有將腳本中的路徑 `C:\Homestead` 調整成你 Homesteam 的安裝位置。建立完檔案之後，把此檔案位置加入你的 `PATH`。你就可以從系統上的任何地方執行像是 `homestead up` 或 `homestead ssh` 的指令。

<a name="connecting-via-ssh"></a>
### 透過 SSH 連接

你可以在終端機裡進入你的 Homestead 目錄，並執行 `vagrant ssh` 指令藉此以 SSH 連上你的虛擬主機。

但是，你可能會經常需要透過 SSH 連上你的 Homestead 主機，因此你可以考慮在你的本機電腦上創建一個上述的「Bash 函式」來快速 SSH 至 Homestead box。

<a name="connecting-to-databases"></a>
### 連接資料庫

`homestead` 的資料庫設定了 MySQL 與 Postgres 兩種資料庫。為了方便使用，Laravel 的 `.env` 檔案預設會設定框架會使用此資料庫。

如果想要從本機資料庫client端連接你的 MySQL 或 Postgres 資料庫，你應該連接 `127.0.0.1` 連接埠 `33060` (MySQL) 或 `54320` (Postgres)。資料庫的帳號及密碼皆為 `homestead` / `secret`.

> {note} 在本機電腦你應該只使用這些非標準的連接埠來連接資料庫。因為當 Laravel 執行於虛擬主機中時，你會在 Laravel 的資料庫設定檔使用預設的 3306 及 5432 連接埠。

<a name="adding-additional-sites"></a>
### 增加更多網站

Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your Laravel applications. You can run as many Laravel installations as you wish on a single Homestead environment. To add an additional site, simply add the site to your `Homestead.yaml` file:

    sites:
        - map: homestead.app
          to: /home/vagrant/Code/Laravel/public
        - map: another.app
          to: /home/vagrant/Code/another/public

If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well:

    192.168.10.10  homestead.app
    192.168.10.10  another.app

Once the site has been added, run the `vagrant reload --provision` command from your Homestead directory.

<a name="site-types"></a>
#### Site Types

Homestead supports several types of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Symfony application to Homestead using the `symfony2` site type:

    sites:
        - map: symfony2.app
          to: /home/vagrant/Code/Symfony/public
          type: symfony2

The available site types are: `apache`, `laravel` (the default), `proxy`, `silverstripe`, `statamic`, and `symfony2`.

<a name="configuring-cron-schedules"></a>
### 設定 Cron 排程器

Laravel 提供了便利的方式來[排程 Cron 任務](/docs/{{version}}/scheduling)，透過 `schedule:run` Artisan 指令，排程便會在每分鐘被執行。`schedule:run` 指令會檢查定義在你 `App\Console\Kernel` 類別中排程的任務，判斷哪個任務該被執行。

如果你想為 Homestead 網站使用 `schedule:run`  指令，你可以在定義網站時設置 `schedule` 選項為 `true`：

    sites:
        - map: homestead.app
          to: /home/vagrant/Code/Laravel/public
          schedule: true

該網站的 Cron 任務會被定義於虛擬機器的 `/etc/cron.d` 資料夾中。

<a name="ports"></a>
### 連接埠

以下的連接埠預設將會被轉發至 Homestead 環境：

- **SSH:** 2222 &rarr; 轉發至 22
- **HTTP:** 8000 &rarr; 轉發至 80
- **HTTPS:** 44300 &rarr; 轉發至 443
- **MySQL:** 33060 &rarr; 轉發至 3306
- **Postgres:** 54320 &rarr; 轉發至 5432
- **Postgres:** 54320 &rarr; Forwards To 5432
- **Mailhog:** 8025 &rarr; Forwards To 8025

#### 轉發更多連接埠

你可以轉發更多額外的連接埠給 Vagrant box，同時也可指定連接埠的通訊協定：

    ports:
        - send: 93000
          to: 9300
        - send: 7777
          to: 777
          protocol: udp

<a name="sharing-your-environment"></a>
### 分享你的環境

有時候你可能會希望和合作夥伴分享你現在的工作環境或者分享到一個client上。Vagrant有一個內建的方法，透過 `vagrant share` 支援這個功能;然而，如果你有多個網站同時使用你的 `Homestead.yaml` 檔案，這功能將無法使用。

要解決這個問題，Homestead 加入了自己的 `share` 指令。開始前，透過 `vagrant ssh` 連線到你的 Homestead 機器然後執行 `share homestead.app`。這會從你的 `Homestead.yaml` 分享 `homestead.app` 網站。當然，你可以將 `homestead.app`替換成任何其他網站。

    share homestead.app

執行這個指令之後，你將會看到一個 Ngrok 視窗，其中包含著活動記錄和共享網站的公開存取網址。如果你想指定一個自定的區域、子網域或者其他 Ngrok runtime 選項，你可以加入到 `share` 下:

    share homestead.app -region=eu -subdomain=laravel

> {note} 記住, Vagrant 本質上是不安全的，當你執行 `share` 指令，你將暴露你的虛擬機器在網路上。

<a name="network-interfaces"></a>
## 網路介面卡

`Homestead.yaml` 檔案中的 `networks` 屬性，用來配置 Homestead 環境中的網路介面卡。你可以依需求配置多張介面卡：

    networks:
        - type: "private_network"
          ip: "192.168.10.20"

啟用 [橋接模式](https://www.vagrantup.com/docs/networking/public_network.html) 介面卡，設定 `bridge` 屬性，並且更改 network type 屬性為 `public_network`:

    networks:
        - type: "public_network"
          ip: "192.168.10.20"
          bridge: "en1: Wi-Fi (AirPort)"

啟用 [DHCP模式](https://www.vagrantup.com/docs/networking/public_network.html)，只要從設定中移除 `ip` 屬性：

    networks:
        - type: "public_network"
          bridge: "en1: Wi-Fi (AirPort)"

<a name="updating-homestead"></a>
## 更新 Homestead

你可以用兩步驟更新 Homestead。首先，你應該先使用 `vagrant box update` 更新你的 Vagrant box:

    vagrant box update

接著，你需要更新 Homestead 原始碼。如果你已經複製了儲存庫，你可以簡單的在儲存庫的位置透過 `git pull origin master` 更新。

如果你已經透過專案的 `composer.json` 安裝 Homestead，你應該確保 `composer.json` 檔案包含 `"laravel/homestead": "^4"` 然後更新你的dependencies:

    composer update

<a name="old-versions"></a>
## 舊版本

你可以簡單的覆寫 Homesteam 使用的 box 的版本，透過加入下面一行到你的 `Homestead.yaml` 檔案:

    version: 0.6.0

An example:

    box: laravel/homestead
    version: 0.6.0
    ip: "192.168.20.20"
    memory: 2048
    cpus: 4
    provider: virtualbox

當你想用 Homestead box 舊版本時，你需要使用與 Homestead 原始碼相容的版本。下面表格列出的是支援的 box 版本與其使用的 Homestead 原始碼版本和提供的 PHP 版本:

|   | Homestead Version | Box Version |
|---|---|---|
| PHP 7.0 | 3.1.0 | 0.6.0 |
| PHP 7.1 | 4.0.0 | 1.0.0 |

<a name="provider-specific-settings"></a>
## Provider Specific Settings

<a name="provider-specific-virtualbox"></a>
### VirtualBox

預設的設定中，Homestead 設定 `natdnshostresolver` 為 `on`。這允許 Hoemstead 使用你作業系統的 DNS 設定。如果你想要覆寫這個動作，加入下面幾行到你的 `Homestead.yaml` 檔案:

    provider: virtualbox
    natdnshostresolver: off

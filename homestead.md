# Laravel Homestead

- [簡介](#introduction)
- [安裝與設定](#installation-and-setup)
    - [前置動作](#first-steps)
    - [配置 Homestead](#configuring-homestead)
    - [啟動 Vagrant box](#launching-the-vagrant-box)
    - [根據專案分別安裝](#per-project-installation)
- [常見用法](#daily-usage)
    - [透過 SSH 連接](#connecting-via-ssh)
    - [連接資料庫](#connecting-to-databases)
    - [增加更多網站](#adding-additional-sites)
    - [連接埠](#ports)
    - [Bash 別名](#bash-aliases)
- [Blackfire 分析器](#blackfire-profiler)

<a name="introduction"></a>
## 簡介

Laravel 致力於讓 PHP 開發體驗更愉快，也包含你的本地開發環境。[Vagrant](http://vagrantup.com) 提供了一個簡單、優雅的方式來管理與供應虛擬機器。

Laravel Homestead 是一個官方預載的 Vagrant「box」，提供你一個美好的開發環境，你不需要在你的本機電腦安裝 PHP、HHVM、網頁伺服器或任何伺服器軟體。不用擔心搞亂你的系統！Vagrant box 可以搞定一切。如果有什麼地方爛掉了，你可以在幾分鐘內快速的砍掉並重建虛擬機器！

Homestead 可以在任何 Windows、Mac 或 Linux 上面運行，裡面包含了 Nginx 網頁伺服器、PHP 5.6、MySQL、Postgres、Redis、Memcached、Node，以及所有你在使用 Laravel 開發各種精彩的應用程式時所需要的軟體。

> **附註：** 如果您是 Windows 的使用者，您可能需要啟用硬體虛擬化（VT-x）。這通常需要透過 BIOS 來啟用它。

Homestead 目前是建置且測試於 Vagrant 1.7。

<a name="included-software"></a>
### 內建軟體

- Ubuntu 14.04
- PHP 5.6
- HHVM
- Nginx
- MySQL
- Postgres
- Node (With PM2, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- [Laravel Envoy](/docs/{{version}}/envoy)
- [Blackfire Profiler](#blackfire-profiler)

<a name="installation-and-setup"></a>
## 安裝與設定

<a name="first-steps"></a>
### 前置動作

在啟動你的 Homestead 環境之前，你必須先安裝 [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 或 [VMWare](http://www.vmware.com) 以及 [Vagrant](http://www.vagrantup.com/downloads.html). 這些軟體在各平台都有提供易用的視覺化安裝程式。

若要使用 VMware provider，你需要同時購買 VMware Fusion / Workstation 及 [VMware Vagrant plug-in](http://www.vagrantup.com/vmware) 的軟體授權。使用 VMware 可以在共享資料夾上獲得較快的性能。

#### 安裝 Homestead Vagrant box

當 VirtualBox / VMware 以及 Vagrant 安裝完成後，你可以在終端機以下列指令將 'laravel/homestead' 這個 box 安裝進你的 Vagrant 程式中。下載 box 會花你一點時間，時間長短將依據你的網路速度決定：

    vagrant box add laravel/homestead

如果執行上面的指令失敗，代表你使用的可能是舊版的 Vagrant，它需要補上完整的 URL：

    vagrant box add laravel/homestead https://atlas.hashicorp.com/laravel/boxes/homestead

#### 手動克隆 Homestead 資源庫

你可以簡單地透過手動克隆資源庫的方式來安裝 Homestead。建議可將資源庫克隆至你的 "home" 目錄中的 `Homestead` 資料夾，如此一來 Homestead box 將能提供主機服務給你所有的 Laravel 專案：

    git clone https://github.com/laravel/homestead.git Homestead

一旦你克隆完 Homestead 資源庫，即可在 Homestead 目錄中執行 `bash init.sh` 指令來創建 `Homestead.yaml` 設定檔。 `Homestead.yaml` 這個檔案將會被放置在你的 `~/.homestead` 目錄中：

    bash init.sh

<a name="configuring-homestead"></a>
### 配置 Homestead

#### 設定你的 Provider

在 `Homestead.yaml` 檔案中的 `provider` 參數是用來設定你想要使用哪一個 Vagrant provider： `virtualbox`、`vmware_fusion` 或 `vmware_workstation`。你可以根據你的喜好來決定 provider：

    provider: virtualbox

#### 設定你的 SSH 金鑰

你還需要將你的 public SSH 金鑰的路徑，配置在 `Homestead.yaml` 檔案中。你沒有 SSH 金鑰？在 Mac 和 Linux 下，你可以利用下面的指令來創建一組 SSH 金鑰：

    ssh-keygen -t rsa -C "you@homestead"

在 Windows 下，你需要安裝 [Git](http://git-scm.com/) 並且使用包含在 Git 裡的 `Git Bash` 來執行上述的指令。另外你也可以使用 [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) 和 [PuTTYgen](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)。

一旦你創建了一組 SSH 金鑰，記得在你的 `Homestead.yaml` 檔案中的 `authorize` 屬性去設定 public 金鑰的路徑。

#### 設定共享資料夾

你可以在 `Homestead.yaml` 檔案的 `folders` 屬性裡列出所有你想與你的 Homestead 環境共享的資料夾。這些資料夾中的檔案若有更動，它們將會同步更動在你的本機電腦與 Homestead 環境。你可以將多個你所需要的共享資料夾都設定於此：

    folders:
        - map: ~/Code
          to: /home/vagrant/Code

若要啟用 [NFS](http://docs.vagrantup.com/v2/synced-folders/nfs.html)，你只需要在共享資料夾的設定值中加入一個簡單的參數：

    folders:
        - map: ~/Code
          to: /home/vagrant/Code
          type: "nfs"

#### 設定 Nginx 網站

對 Nginx 不熟悉嗎？沒關係。`sites` 屬性幫助你可以輕易的指定一個 `網域` 對應至 homestead 環境中的一個目錄。在 `Homestead.yaml` 檔案中已內含一個網站設定的範本。同樣的，你可以增加數個你所需要的網站到你的 Homestead 環境中。Homestead 可以為每個你正在開發中的 Laravel 專案提供方便的虛擬化環境：

    sites:
        - map: homestead.app
          to: /home/vagrant/Code/Laravel/public

你可以將 `hhvm` 屬性設定為 `true` 讓 Homestead 裡面的任一個網站改用 [HHVM](http://hhvm.com)：

    sites:
        - map: homestead.app
          to: /home/vagrant/Code/Laravel/public
          hhvm: true

若要造訪網站，每一個網站預設的連接埠分別是 HTTP 連接埠 8000 及 HTTPS 連接埠 44300。

#### 關於 Hosts 檔案

不要忘了在將你在 Nginx sites 中所新增的「網域」也新增至你本機電腦的 `hosts` 裡！ `hosts` 檔案會將你所發出的請求重導至你在 Homestead 環境中設定的本地網域。在 Mac 或 Linux 上，該檔案通常會存放在 `/etc/hosts`。在 Windows 上，則存放於 `C:\Windows\System32\drivers\etc\hosts`。你要設定於檔案中的內容類似如下：

    192.168.10.10  homestead.app

務必確認 IP 位置與 `Homestead.yaml` 檔案中設定的相同。一旦你將網域設定在 `hosts` 檔案之後，你就可以透過網頁瀏覽器造訪你的網站！

    http://homestead.app

<a name="launching-the-vagrant-box"></a>
### 啟動 Vagrant box

當你根據你的喜好編輯完 `Homestead.yaml` 後，在終端機裡進入你的 Homestead 目錄並執行 `vagrant up` 指令。Vagrant 就會將虛擬主機啟動並自動設定你的共享資料夾和 Nginx 網站。

如果要移除虛擬機器，可以使用 `vagrant destroy --force` 指令。

<a name="per-project-installation"></a>
### 根據專案分別安裝

有別於將 Homestead 安裝成全域環境且讓所有的專案共用同一個 Homestead box，你可以各別為每一個專案獨立配置一個 Homstead。如果你希望直接在專案裡傳遞 `Vagrantfile`，那麼替每個專案安裝 Homestead 即是你可以考慮的方式，這將會允許其他人可以簡單地執行 `vagrant up` 即能開始工作於此專案。

你可以使用 Composer 將 Homestead 直接安裝至你的專案中：

    composer require laravel/homestead

一旦 Homestead 安裝完畢，你可以使用 `make` 指令產生 `Vagrantfile` 與 `Homestead.yaml` 存放於專案的根目錄。這個 `make` 指令將會自動配置 `sites` 及 `folders` 於 `Homestead.yaml` ：

Mac / Linux:

    php vendor/bin/homestead make

Windows:

        vendor\bin\homestead make

接著，執行在終端機中執行 `vagrant up` 並透過網頁瀏覽器造訪 `http://homestead.app`。再次提醒，你仍然需要在 `/etc/hosts` 裡設定 `homestead.app` 或其他想要使用的網域。

<a name="daily-usage"></a>
## 常見用法

<a name="connecting-via-ssh"></a>
### 透過 SSH 連接

你可以在終端機裡進入你的 Homestead 目錄並執行 `vagrant ssh` 指令藉此以 SSH 連上你的虛擬主機。

但是，你可能會經常需要透過 SSH 連上你的 Homestead 主機，因此你可以考慮在你的本機電腦上創建一個「別名」來快速連上 Homestead box。一旦你創建這個別名，你可以輕易地透過「vm」這個指令從你的電腦以 SSH 連上你的 Homestead 主機：

    alias vm="ssh vagrant@127.0.0.1 -p 2222"

<a name="connecting-to-databases"></a>
### 連接資料庫

在 `Homestead` 中，已經預裝了 MySQL 與 Postgres 兩種資料庫。為了方便使用，Laravel 在 `local` 的資料庫設定值中已經預設將其設定完成。

如果想要從本機電腦上透過 Navicat 或者是 Sequel Pro 連接 MySQL 或 Postgres 資料庫，你可以連接 `127.0.0.1` 的連接埠 33060 (MySQL) 或 54320 (Postgres)。而帳號密碼分別是 `homestead` / `secret`。

> **附註：** 從本機電腦你應該只能使用這些非標準的連接埠來連接資料庫。因為當 Laravel 運行於虛擬主機時，在 Laravel 的資料庫設定值中依然是設定使用預設的 3306 及 5432 連接埠。

<a name="adding-additional-sites"></a>
### 增加更多網站

一旦 Homestead 環境配置完畢且運行後，你可能會想要為 Laravel 應用程式增加更多的 Nginx 網站。你可以在單一個 Homestead 環境中運行非常多 Laravel 安裝程式。只要在 `Homestead.yaml` 檔中增加另一個網站設定後，接著在終端機中進入到你的 Homestead 目錄並執行 `vagrant provision` 指令，即可增加另一個網站。

<a name="ports"></a>
### 連接埠

以下的連接埠將會被轉發至 Homestead 環境：

- **SSH:** 2222 &rarr; 轉發至 22
- **HTTP:** 8000 &rarr; 轉發至 80
- **HTTPS:** 44300 &rarr; 轉發至 443
- **MySQL:** 33060 &rarr; 轉發至 3306
- **Postgres:** 54320 &rarr; 轉發至 5432

#### 轉發更多連接埠

如果你希望，你也可以藉著指定連接埠的通訊協定來轉發更多額外的連接埠給 Vagrant box：

    ports:
        - send: 93000
          to: 9300
        - send: 7777
          to: 777
          protocol: udp

<a name="bash-aliases"></a>
### Bash 別名

若要增加 Bash 別名至你的 Homestead box，只需要編輯 Homestead 目錄中的 `aliases` 檔案。這些別名會在 Homestead box 啟動時自動定義。

<a name="blackfire-profiler"></a>
## Blackfire 分析器

由 SensioLabs 推出的 [Blackfire 分析器](https://blackfire.io) 能協助你自動收集程式運行時的相關數據，像是 RAM、CPU time 及 disk I/O。若想在 Homestead 中替你的應用程式使用這個分析器是非常容易的。

在 Homestead box 中同樣已經預裝好所有需要的套件，很簡單地你只需要在 `Homestead.yaml` 檔案中設定你的 Blackfire **Server ID 及 token 即可：

    blackfire:
        - id: your-server-id
          token: your-server-token
          client-id: your-client-id
          client-token: your-client-token

一旦你設定完 Blackfire 的認證，在你的 Homestead 目錄下執行 `vagrant provision` 來重新配置 box。當然，請務必閱讀 [Blackfire 使用文件](https://blackfire.io/getting-started) 來學習如何在你的網頁瀏覽器上安裝 Blackfire 擴充套件。

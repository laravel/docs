# Laravel Homestead

- [導覽](#introduction)
- [內建軟體](#included-software)
- [安裝與設定](#installation-and-setup)
- [Daily Usage](#daily-usage)
- [Ports](#ports)

<a name="introduction"></a>
## 導覽

Laravel 致力於讓 PHP 開發體驗更愉快，也包含你的本地開發環境。[vagrant](http://vagrantup.com) 一個簡單、優雅的方式來管理與供應虛擬機器。

Laravel Homestead 是一個官方預載的 Vagrant “封裝包”，提供你一個美好的開發環境，不需要你在你的本機端安裝 PHP、網頁伺服器或任何伺服器軟體。不用擔心搞亂你的系統！Vagrant 封裝包完全搞定。如果有什麼地方爛掉了，你只要砍掉重來即可。

Homestead 可以在任何 Windows, Mac 或 Linux 上面運行，裏面包含了 Nginx 網頁伺服器、PHP 5.5、MySQL、Postgres、Redis、Memcached 還有所有你要開發精彩的 Laravel 應用程式所需的軟體。

Homestead 建置且測試於 Vagrant 1.6 上。

<a name="included-software"></a>
## 內建軟體

- Ubuntu 14.04
- PHP 5.5
- Nginx
- MySQL
- Postgres
- Node (With Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- [Laravel Envoy](/docs/ssh#envoy-task-runner)
- Fabric + HipChat Extension

<a name="installation-and-setup"></a>
## 安裝與設定

### 安裝 VirtualBox 與 Vagrant

在啟動你的 Homestead 環境之前，你必須先安裝 [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 和 [Vagrant](http://www.vagrantup.com/downloads.html). 兩套軟體在各平台都有提供易用的視覺化安裝程式。

### 增加 Vagrant 封裝包

當 VirtualBox 和 Vagrant 安裝完成後，你可以在終端機以下列命令將 'laravel/homestead' 封裝包安裝進你的 Vagrant 安裝程式中。下載封裝包會花你一點時間，看你的網路速度決定：

	vagrant box add laravel/homestead

### 複製 Homestead 程式源

一旦封裝包已經被加進你的 Vagrant 安裝程式後，你必須複製並下載該程式源並放置於一個集中的 `Homestead` 目錄中，目錄中放置所有你的 Laravel 專案，如此 homestead 封裝包就可以運行你所有的 Laravel（和 PHP）專案。

	git clone https://github.com/laravel/homestead.git Homestead

### 設定你的 SSH 金鑰

再來你要編輯在程式源里的 `Homestead.yaml`。你可以在檔案中設定你的 SSH 公開金鑰，以及你主要機器與 Homestead 虛擬機器之間的共享目錄。

你沒有 SSH 金鑰? 在 Mac 和 Linux 下，你可以利用下面的指令來創建一個 SSH 金鑰組:

	ssh-keygen -t rsa -C "your@email.com"

在 Windows 下，你需要安裝 [Git](http://git-scm.com/) 並且使用包含在 Git 裏的 `Git Bash` 來執行上述的指令。另外你也可以使用 [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) 和 [PuTTYgen](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)。

一旦你創建了一個 SSH 金鑰，記得在你的 `Homestead.yaml` 檔案中的 `authorize` 屬性指明金鑰路徑。

### 設定你的共享資料夾

`Homestead.yaml` 檔案中的 `folders` 屬性列出所有你想跟你的 Homestead 環境共享的資料夾列表。這些資料夾中的檔案若有更動，他們將會同步在你的本機與 Homestead 環境裡。你可以將你需要的共享資料夾都設定進去。

### 設定你的 Nginx 站台

對 Nginx 不熟悉? 沒關係。`sites` 屬性允許你簡單的對應一個 `網域` 到一個你 homestead 環境中的目錄。一個範例的站台設定被在 `Homestead.yaml` 檔案中。同樣的，你可以加任何你需要的站台到你的 Homestead 環境中。Homestead 可以作為你進行中專案的一個方便虛擬化環境。

### Bash Aliases

如果要增加 Bash aliases 到你的 Homestead 封裝包中，只要加到 Homestead 目錄最上層的 `aliases` 檔案中。

### 啟動 Vagrant 封裝包

當你根據你的喜好編輯完 `Homestead.yaml` 後，在終端機裡，從 Homestead 目錄裡執行 `vagrant up` 指令。Vagrant 將會將虛擬機器開機，並且自動設定你的共享目錄和 Nginx 站台。

為了你的 Nginx 站台，別忘記在你的機器的 `hosts` 檔將"網域"加進去。`hosts` 檔會將你的本地網域的站台請求重導至你的 Homestead 環境中。在 Mac 和 Linux，該檔案放在 `/etc/hosts`。在 Windows 環境中，它被放置在 `C:\Windows\System32\drivers\etc\hosts`。你要加進去的內容類似如下：

	127.0.0.1  homestead.app

一旦你將網域加進你的 `hosts` 檔案中，你家可以從埠 8000 透過你的瀏覽器存取到你的站台。

	http://homestead.app:8000

繼續讀下去，你會學到如何連結到你的資料庫。

<a name="daily-usage"></a>
## Daily Usage

### 透過 SSH 連接

要透過 SSH 連接你的 Homestead 環境，你需要使用你設定在 `Homestead.yaml` 檔案中的 SSH 金鑰連接 `127.0.0.1` 的埠 2222。你也可以輕易的從你的 `Homestead` 目錄下執行 `vagrant ssh` 命令來連接。

如果你想要更簡便，你可以將下面的 alias 加到你的 `~/.bash_aliases` 或是 `~/.bash_profile` 中：

	alias vm='ssh vagrant@127.0.0.1 -p 2222'

### 連結你的資料庫

在 `Homestead` 封裝包中，MySQL 與 Postgres 兩套資料庫都已預裝其中。為了更簡便，Laravel 的 `local` 資料庫設定已經預設將其設定完成。

如果你想要從你的本機上透過 Navicat 或者是 Sequel Pro 連接你的 MySQL 或者 Postgres 資料庫，你可以連接 `127.0.0.1` 的 埠 33060 (MySQL) 或 54320 (Postgres)。而帳號密碼分別是 `homestead` / `secret`。

> **附註:** 你應該怎使用這些非標準的埠從本機來連結你的資料庫。 You will use the default 3306 and 5432 ports in your Laravel database configuration file since Laravel is running _within_ the Virtual Machine.

### 增加更多的站台

一旦你的 Homestead 環境上架且運行後，你可能會需要為你的 Laravel 應用程式增加夠多的 Nginx 站台。你可以在單一個 Homestead 環境中運行非常多 Laravel 安裝程式。兩個方式可以達到：第一，你可以在你的 `Homestead.yaml` 檔案中增加站台然後執行 `vagrant provision`。

另外，你也可以使用放在你的 Homestead 環境中的 `serve` 指令檔。你需要 SSH 進入你的 Homestead 環境中，並執行下列命令：

	serve domain.app /home/vagrant/Code/path/to/public/directory

> **附註:** 在執行 `serve` 指令過後，別忘記將新的站台加進你本機的 `hosts` 檔案中。

<a name="ports"></a>
## 連接埠

以下的埠將會被重導至你的 Homestead 環境：

- **SSH:** 2222 -> Forwards To 22
- **HTTP:** 8000 -> Forwards To 80
- **MySQL:** 33060 -> Forwards To 3306
- **Postgres:** 54320 -> Forwards To 5432

# Laravel Homestead

- [Introdução](#introduction)
- [Instalação & Configuração](#installation-and-setup)
	- [Primeiros Passos](#first-steps)
	- [Configurando o Homestead](#configuring-homestead)
	- [Executando o Vagrant Box](#launching-the-vagrant-box)
- [Uso Diário](#daily-usage)
	- [Conectando via SSH](#connecting-via-ssh)
	- [Conectando aos Bancos de Dados](#connecting-to-databases)
	- [Adicionando Sites](#adding-additional-sites)
	- [Portas](#ports)
- [Blackfire Profiler](#blackfire-profiler)

<a name="introduction"></a>
## Introdução

O Laravel tenta fazer sua experiência em desenvolver aplicações PHP prazeirosa, incluindo seu ambiente de desenvolvimento Local. O [Vagrant](http://vagrantup.com) provê uma maneira simples e elegante de gerenciar e provisionar Máquinas Virtuais.

O Laravel Homestead é uma pré-empacotada Vagrant Box oficial que provê a você um ambiente de desenvolvimento maravilhoso que não obriga vocÊ a ter de instalar PHP, HHVM, um servidor Web e outros softwares na sua máquina local. Não precisa mais se preocupar em bagunçar seu sistema operacional! As Vagrant Box são completamente desacopladas do seu sitema operacional. Se algo der errado, você pode destruir e recriar uma nova Homestead em minutos!

Homestead pode ser executado em sistemas Windows, Mac e Linux e inclui o servidor Web Nginx, PHP 5.6, Postgres, MySQL, Redis, Memcached, Node e todas as outras coisas que você precisa para desenvolver aplicações Laravel impressionantes.

> **Nota:** Se você está usando Windows, você pode precisar ativar a Virtualização de Hardware (VT-x). Isso geralmente é ativado nas configurações da sua BIOS.

Homestead é atualmente construido e testado usando Vagrant 1.7.

<a name="included-software"></a>
### Software Incluídos

- Ubuntu 14.04
- PHP 5.6
- HHVM
- Nginx
- MySQL
- Postgres
- Node (com PM2, Bower, Grunt e Gulp)
- Redis
- Memcached
- Beanstalkd
- [Laravel Envoy](/docs/{{version}}/envoy)
- [Blackfire Profiler](#blackfire-profiler)

<a name="installation-and-setup"></a>
## Instalação & Configuração

<a name="first-steps"></a>
### Primeiros Passos

Antes de executar seu ambiente Homestead, você precisa instalar o [VirtualBox](https://www.virtualbox.org/wiki/Downloads) ou [VMWare](http://www.vmware.com) e também o [Vagrant](http://www.vagrantup.com/downloads.html). Todos esses softwares e pacotes disponibilizam instaladores visuais fáceis de usar para os sistemas operacionais mais populares.

Para usar o VMware, vocÊ precisa comprar o VMware Fusion/Desktop e o [VMware Vagrant plug-in](http://www.vagrantup.com/vmware). O WMware tem a melhor performance com pastas compartilhadas pronta para uso.

#### Instalando a Homestead Vagrant Box

Depois de instalar sua VirtualBox / VMware e Vagrant, você pode adicionar a Vagrant Box `laravel/homestead` à sua instalação do Vagrant usando a seguinte linha de comando no seu terminal. Isso levará algum tempo para baixar, dependendo da sua velocidade de conexão com a internet:

	vagrant box add laravel/homestead

Se esse comando falhar, você deve ter uma versão antiga do Vagrant, e ela obriga a esquever a URL completa:

	vagrant box add laravel/homestead https://atlas.hashicorp.com/laravel/boxes/homestead

#### Clonando o Repositório do Homestead

Você pode isntalar o Homestead simplesmente clonando o repositório. Considere cloná-lo em uma pasta chamanda `Homestead` no diretório do seu usuário, assim o Homestead Box servirá como hospedeiro de todas os seus projetos Laravel:

	git clone https://github.com/laravel/homestead.git Homestead

Depois de clonar o repositório do Homestead, execute o comando `bash init.sh` a partir do diretório do Homestead para criar o arquivo de configuração `Homestead.yaml`. O arquivo `Homestead.yaml` será criado no diretório `~/.homestead`:

	bash init.sh

<a name="configuring-homestead"></a>
### Configurando o Homestead

#### Selecionando o Provedor (provider)

A chave `provider` no seu arquivo `Homestead.yaml` indica que tipo de provedor Vagrant você deve usar: `virtualbox` ou `wmware_fusion`. Você deve configurá-la com o provedor que você preferir (e que tiver instalado):

	provider: virtualbox

#### Configurando sua Chave SSH

No arquivo `Homestead.yaml` você também pode configurar o caminho para sua chave SSH. Você não tem uma chave SSH? No Mac e Linux você pode criar um par de chaves SSH usando o seguinte comando:

	ssh-keygen -t rsa -C "you@homestead"

No Windows, você pode precisar instalar o [Git](http://git-scm.com/) e usar o Shell "Git Bash" que vem na instalação para gerar o par de chaves SSH. Alternativamente, você também pode usar o [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) e [PuTTYgen](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

Depois de criar suas chaves SSH, você deve especificar o caminho da sua chave pública na propriedade `authorize` do arquivo `Homestead.yaml`.

#### Configurando Pastas Compartilhadas

A propriedade `folders` do arquivo `Homestead.yaml` lista todas as pastas que vocÊ gostaria de compartilhar com o seu ambiente Homestead. Quando os arquivos nessas pastas forem modificados, eles serão sincronizados entre sua máquina local e o ambiente Homestead. Você pode configurar quantas pastas você achar necessário:

	folders:
	    - map: ~/Code
	      to: /home/vagrant/Code

Para ativar o [NFS](http://docs.vagrantup.com/v2/synced-folders/nfs.html), você só precisar adicionar a seguinte flag a sua configuração de pastas compartilhadas:

	folders:
	    - map: ~/Code
	      to: /home/vagrant/Code
	      type: "nfs"

#### Configurando Sites Nginx

Não está familiarizado com o Nginx? Não tem problema. A propriedade `sites` permite a você facilmente mapear um "domínio" para uma pasta dentro do ambiente Homestead. Um exemplo de configuração está no `Homestead.yaml`. E novamente, vocÊ pode adicionar quantos sites você precisar no ambiente Homestead. O Homestead serve como um conveniente e virtualizado ambiente para cada projeto Laravel que você está trabalhando:

	sites:
	    - map: homestead.app
	      to: /home/vagrant/Code/Laravel/public

Você também pode  fazer qualquer site na Homestead usar [HHVM](http://hhvm.com) configurando a opção `hhvm` para `true`:

	sites:
	    - map: homestead.app
	      to: /home/vagrant/Code/Laravel/public
	      hhvm: true

Por padrão, cada site estará acessível via HTTP pela porta 8000 e HTTPS 44300.

#### O Arquivo de Hosts

Não se esqueça de adicionar "domínios" para seus sites Nginx no arquivo `hosts` da sua máquina! Esse arquivo irá redirecionar todas as requisições da sua máquina local para os domínios no ambiente Homestead. No Mac e Linux este arquivo é localizado em `/etc/hosts`. No windows, ele é localizado em `C:\Windows\System32\drivers\etc\hosts`. As linhas que você adicionar devem se parecer com a seguinte:

	192.168.10.10  homestead.app

Certifique-se de que o endereço IP listado é o mesmo que está no seu arquivo de configuração `Homestead.yaml`. Depois de adicionar o domínio no arquivo `hosts`, você poderá acessar seu site pelo navegador web!

	http://homestead.app

<a name="launching-the-vagrant-box"></a>
### Executando a Vagrant Box

Depois de editar o arquivo `Homestead.yaml` ao seu gosto, execute o comando `vagrant up` a partir do seu diretório Homestead. Você iniciará a máquina virtual e automaticamente configurar suas pastas compartilhadas e sites Nginx.

Para destuir sua máquina, você pode usar o comando `vagrant destroy --force`.

<a name="daily-usage"></a>
## Uso Diário

<a name="connecting-via-ssh"></a>
### Conectando Via SSH

Você pode conectar-se via SSH na sua máquina virtual usando o comando `vagrant ssh` no terminal a partir do diretório do Homestead.

Mas, você provavelmente precisará se conectar via SSH à sua máquina Homestead frequentemente, considere criar um "alias" (atalho para comando) na sua máquina para rapidamente se conectar a sua Homestead Box via SSH. Uma vez criado esse atalho, você pode simplesmente usar o comando "vm" de qualquer diretório do seu sistema:

	alias vm="ssh vagrant@127.0.0.1 -p 2222"

<a name="connecting-to-databases"></a>
### Conectando aos Bancos de Dados

Um banco de dados `homestead` é configurado para MySQL e Postgres pronto para uso. Para sua conveniência, toda instalação do Laravel já vem configurada para usar esta conexão por padrão.

Para conectar com seu banco de dados MySQL ou Postgres a partir da sua máquina via Navicat ou Sequel Pro, você pode conectar ao host `127.0.0.1` e porta 33060 (MySQL) ou 54320 (Postgres). O nome de usuário e senha para ambos é `homestead` / `secret`.

> **Nota:** Você só deve usar as portas não-padrão quando se conecta ao banco de dados a partir da sua máquina. Você usará as portas padrão 3306 e 5432 nos arquivos de configuração de banco de dados do Laravel que está rodando _dentro_ da Máquina Virtual.

<a name="adding-additional-sites"></a>
### Adicionando Sites

Depois que seu ambiente Homestead estiver provisionado e rodando, você pode querer adicionar sites Nginx para suas aplicações Laravel. Você pode executar quantas instalações você quiser com um único ambiente Homestead. Para adicionar mais sites, simplesmente adicione o  site ao seu arquivo `Homestead.yaml` e então execute no terminal o comando `vagrant provision` a partir do diretório do Homestead.

> **Nota:**  Esse procedimento é destrutivo. Quando executar o comando `provision`, todos os seus bancos de dados serão recriados.


<a name="ports"></a>
### Portas

Por padrão, as seguitnes portas são redirecionadas para seu ambiente Homestead:

- **SSH:** 2222 &rarr; 22
- **HTTP:** 8000 &rarr; 80
- **HTTPS:** 44300 &rarr; 443
- **MySQL:** 33060 &rarr; 3306
- **Postgres:** 54320 &rarr; 5432

#### Redirecinando Portas Adicionais

Se você desejar, você pode redireionar outras portas para sua Vagrant Box, assim como especificar seus protocolos:

	ports:
	    - send: 93000
	      to: 9300
	    - send: 7777
	      to: 777
	      protocol: udp

<a name="blackfire-profiler"></a>
## Blackfire Profiler

[Blackfire Profiler](https://blackfire.io) automaticamente obtém dados sobre a execução do seu código, como RAM, tempo de CPU e I/O do disco. O Homestead torna fácil usar esse profiler para suas aplicações.

Todos os pacotes apropriados já vem instalados na sua Homestead Box, você só precisa configurar o ID do Blackfire **Server** e token no seu arquivo `Homestead.yaml`:

	blackfire:
	    - id: your-server-id
	      token: your-server-token
	      client-id: your-client-id
	      client-token: your-client-token

Depois de configurar as credenciais do Blackfire , re-provisione sua box usando o ocmando `vagrant provision` a partir do diretório do Homestead. E é claro, esteja seguro de revisar a [Documentação do Blackfire](https://blackfire.io/getting-started) para aprender a como isntalar extensões do Blackfire para seu navegador web.

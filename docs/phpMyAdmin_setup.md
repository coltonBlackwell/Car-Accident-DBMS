# ✅ Step-by-Step Setup Guide for phpMyAdmin

## 🔧 Prerequisites:

Ensure you have the following installed: 

- Apache2
- MySQL Server
- PHP

Install it all at once if you haven't:\
```sh 
sudo apt update
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql
```

### 🚀 Step 1: Install phpMyAdmin

```sh
sudo apt install phpmyadmin
```

- During installation: 
    - Choose apache2 when prompted
    - Select **Yes** to configure the database for phpMyAdmin with **dbconfig-common**.
    - Enter your MySQL root password when asked.

### ⚙️ Step 2: Enable phpMyAdmin in Apache

If its not auto enabled:

```sh 
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin
sudo systemctl reload apache2
```

### 🌐 Step 3: Access phpMyAdmin in Browser

Open your browser and go to: 
```sh 
http://localhost/phpmyadmin
```

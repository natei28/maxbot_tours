# maxbot_tours
Бот помошник, сбор заявок на турпутевки

## Запуск проекта

### Устанавливаем Git и клонируем проект с GitHub

1. Обновляем пакеты
```
apt update
apt upgrade
```
2. Устанавливаем Git. генерируем ssh-ключ, открытый ключ вставляем в github:
```
apt install git
ssh-keygen -t rsa
```
3. Клонируем проект с Github
```
git clone git@github.com:natei28/maxbot_tours.git
```
### Устанавливаем необходимые сервисы
1. Запускаем настройку и установку Docker+postgres+pgadmin+requiriments.txt
```
chmod -x install_my_services.sh
./install_my_services.sh
```
### Настройка webhook
1. Установить Nginx certbot
```
sudo apt install nginx certbot -y
```
2. Настройка Nginx, пример конфига /etc/nginx/sites-available/bot
```
server {
    listen 80;
    server_name lili-ufa.ru;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen 80;
    server_name lili-ufa.ru;

    ssl_certificate /etc/letsencrypt/live/lili-ufa.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lili-ufa.ru/privkey.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10m;
    }
}
```
2. Активировать сайт и проверить конфиг
```
sudo ln -s /etc/nginx/sites-available/bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
3. Получить сертификаты Let`s Encrypt
```
sudo certbot --nginx -d lili-ufa.ru
```

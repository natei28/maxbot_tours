#!/bin/bash

array_y_n=("y" "n")

# Шаг 1
echo -e "Шаг 1. Обновляем пакеты 'apt'? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    apt update
fi

# Шаг 2
echo -e "Шаг 2. Устанавливаем ca-certificates и curl? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    sudo apt install ca-certificates curl
fi

# Шаг 3
# Создаём каталог для ключей APT
# В каталоге /etc/apt/keyrings будут храниться ключи репозиториев. 
# Ключи требуются для проверки подлинности загружаемых пакетов.
#
echo -e "Шаг 3. Создаём каталог для ключей APT '/etc/apt/keyrings'?(y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    sudo install -m 0755 -d /etc/apt/keyrings
fi


# Шаг 4
# Скачиваем GPG-ключ из официального репозитория Docker
# сохраняет его в /etc/apt/keyrings/docker.asc:
# Назначаем права доступа на ключ
#
echo -e "Шаг 4. Скачиваем, сохраняем GPG-ключ, назначанм права доступа? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
fi



# Шаг 5 
# Добавляем репозиторий Docker в источники APT
#
echo -e "Шаг 5. Добавляем репозиторий Docker в источники APT? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
fi


# Шаг 6
# Обновляем пакеты
#
echo -e "Шаг 6. Обновляем пакеты? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    sudo apt update
fi


# Шаг 7 
# Устанавливаем последнюю версию Docker и его компоненты
# Добавляем пользователя в группу docker
echo -e "Шаг 7. Устанавливаем последнюю версию Docker \nи добавляем пользователя в группу docker? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
    sudo docker version
    docker --version
fi


# Шаг 8
# создаем директорию для данных сервиса pgamin
# назначим её владельцем юзера 5050 
# (понадобятся права суперюзера):
echo -e "Шаг 8. Создаём директорию для pgamin и назначим \nее владельцем юзера 5050? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    mkdir -p ./.pgadmin_data
    sudo chown -R 5050:5050 ./.pgadmin_data/
fi


# Шаг 9
# Устанавливаем пакет python3-venv, python3-pip
# 
echo -e "Шаг 9. Устанавливаем python3-venv и python3-pip? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    apt install python3-venv
    apt install python3-pip
fi

# Шаг 10
# Создаем и активируем виртуальное окружение .my_venv
# 
echo -e "Шаг 10. Создаем и активируем виртуальное окружение .my_venv? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    python3 -m venv .my_venv
    source .my_venv/bin/activate
fi


# Шаг 11
# Устанавливаем зависимости requirements.txt
# 
echo -e "Шаг 11. Устанавливаем зависимости requirements.txt? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    pip install -r requirements.txt
fi


# Шаг 12
# Поднимаем сервисы в docker-e
# 
echo -e "Шаг 12. Поднимаем сервисы в docker-e (docker-compose.yml)? (y/n)"
read

while [[ ! " ${array_y_n[@]} " =~ " $REPLY " ]]
  do echo -e "Неверный ввод, введите 'y' или 'n'"
    read 
  done

if [[ "$REPLY" == "y" || "$REPLY" == "" ]]
  then
    docker compose up
fi

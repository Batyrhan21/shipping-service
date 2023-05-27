#!/bin/sh
Red='\033[0;31m'
Green='\033[0;32m'
Yellow='\033[0;33m'
NC='\033[0m'

echo "Привет, разраб!"
echo
echo "Что я могу?"
echo
echo "А вот что:"
echo "1. Запустить билд?"
echo "2. Просто запустить? (миграций не будет)"

read -n1 -p "Что выберешь? [1,2] " doit
echo
case $doit in  
  1) echo -e "${Red} Запускаю Dockerfile! ${NC}"
    cd ../docker
    docker-compose -f docker-compose.yml -f dev/docker-compose-dev.yml up --build;;
  2) echo -e "${Green} Запускаю проект! ${NC}"
    cd ../docker
    docker-compose -f docker-compose.yml -f dev/docker-compose-dev.yml up;;
  *) echo -e "${Yellow} Такого варианта нет, читать не умеешь? ${NC}" ;; 
esac
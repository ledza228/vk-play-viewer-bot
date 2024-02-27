> #### RU

### Скрипт для накрутки зрителей на VK Play live, сервиса для трансляций от вк.
***
### Принцип работы:
  Сервис считает зрителей на основе количества websocket подключений, которые были зарегистрированы к какому-то стриму. Достаточно с одного и того же 
  ip создать любое количество соединений, отправить авторизационные даные (token) и подписаться на стрим. 
  При разрыве websocket соединения вы перестаете считаться зрителем. 
  Сейчас внутри token хранится ip, с которого он был получен. И зарегестрироваться на стрим более чем 2 раза токенами с одинаковыми ip не получится. Поэтому необходим proxy, который и собирет токены с уникальными ip адресами
  
### Как запустить:

    pip install -r requirements.txt
    python3 main.py <имя_канала> [<кол-во_зрителей>]
  
  Пример:
  
    python3 main.py mychanelname 100
  
  по умолчанию количество зрителей - 10

  <br/>

#### Прокси:

  На данный момент работают `socks5`, `http` и `https` прокси.
  Они берутся из файла, который позже указывается в аргументах запуска
  (Лучше всего использовать socks5)

  Пример:
    
    python3 main.py mychannel 100 --socks5 filename.txt
    python3 main.py mychannel --http filename.txt

  `--http` - использует `https` или `http` прокси
  `--socks5` - использует `socks5` прокси

  Пример в файле `proxy.txt` это socks5 прокси.
  Взять прокси можно вот тут: https://checkerproxy.net/getAllProxy

  <br/>
  <br/>
  
  > #### ENG
 
 ### Cheat viewers script for Vk Play live (VK service for streaming)
 ***
 
 ### Principle of work
   The service counts viewers based on websocket connection amounts, which were registered for certain stream. No matter how much ip you are using. 
   You just need to create websocket connection, send auth data (token) and subscribe on stream. If the connection was disconnected, you are not counting as viewer.
   upd: now token contains IP field, and you will not be able to register for the stream more than 2 times with tokens with the same ip. Therefore, a proxy is needed, which collects tokens with unique ip addresses
    
### How to run:
    pip install -r requirements.txt
    python3 main.py <chanel_name> [<viewers_amount>]
  
  Example:
  
      python3 main.py mychanelname 100

By default viewers_amount value is 10
 

#### Proxies:

  There is `socks5`, `http`, `https` proxies that works with script.
  The proxies are taken from the file that is specified in the script startup arguments
  (socks5 working better, please use it)

  Example:
    
    python3 main.py mychannel 100 --socks5 filename.txt
    python3 main.py mychannel --http filename.txt

  `--http` - start using `https` or `http` proxy
  `--socks5` - start using `socks5` proxy

  Example in `proxy.txt` file is socks5 proxy.
  Get free proxy you can from this link: https://checkerproxy.net/getAllProxy


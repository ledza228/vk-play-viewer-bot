> #### RU

### Скрипт для накрутки зрителей на VK Play live, сервиса для трансляций от вк.
***
### Принцип работы:
  Сервис считает зрителей на основе количества websocket подключений, которые были зарегистрированы к какому-то стриму. Достаточно с одного и того же 
  ip создать любое количество соединений, отправить авторизационные даные (token) и подписаться на стрим. 
  При разрыве websocket соединения вы перестаете считаться зрителем. 
  
### Как запустить:

    pip install -r requirements.txt
    python3 <имя_канала> [<кол-во_зрителей>]
  
  Пример:
  
    python3 mychanelname 100
  
  по умолчанию количество зрителей - 10
  
  
  <br/>
  <br/>
  
  > #### ENG
 
 ### Cheat viewers script for Vk Play live (VK service for streaming)
 ***
 
 ### Principle of work
   The service counts viewers based on websocket connection amounts, which were registered for certain stream. No matter how much ip you are using. 
   You just need to create websocket connection, send auth data (token) and subscribe on stream. If the connection was disconnected, you are not counting as viewer.
    
### How to run:
    pip install -r requirements.txt
    python3 <chanel_name> [<viewers_amount>]
  
  Example:
  
      python3 mychanelname 100

By default viewers_amount value is 10
 

# wb-project

## Установка

Для работы требуется Python 3.10+. Скопируйте проект и установите зависимости:

```
pip install -r sys.txt
```
## Логика работы

У нас есть желаемый товар, который нужно найти, с помощью данного приложения можно упростить себе жизнь :)

## Техническая часть 

Данный парсер производит поиск по запросу из url, парсит по опредленным категориям, такие как:
```
'id', 'название', 'цена', 'бренд', 'скидка', 'рейтинг', 'в наличии', 'id продавца', 'изображения',"отзывы с текстом", "рейтинг"
```

После создается csv-файл, где храняться все наши запросы
![image](https://github.com/sdv301/wb-project/assets/68203784/cdc9a044-f003-42fd-80bb-e65c0ad837b7)

Также имеется графический интерфейс, который использует библеотеку "customtkinter", для улучшения визуального вида. Можно использовать обычный tkinter, но он скучный и самый простой по интерфейсу.

![image](https://github.com/sdv301/wb-project/assets/68203784/894c5363-a66f-4ff0-9ca3-e99197f80378)


# Version 1.00

Добавленны изменение в графическом интерфейсе.

![image](https://github.com/sdv301/wb-project/assets/68203784/894c5363-a66f-4ff0-9ca3-e99197f80378)


import requests

s_city = "Moscow,RU"

appid = "41d513a70f68bc0257a91a727ed20f40"

res = requests.get("http://api.openweathermap.org/data/2.5/weather",
        params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})

data = res.json()

print("Город:", s_city)
print("Погодные условия:", data['weather'][0]['description'])
print("Скорость ветра:", data['wind']['speed'])
print("Видимость:", data['visibility'])
print("============================")


res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
        params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Недельный прогноз погоды:")
for i in data['list']:
    print("Дата:", i['dt_txt'], "\r\nТемпературa:",
    '{0:3.0f}'.format(i['main']['temp']), "\r\nПогодные условия:", i['weather'][0]['description'], "\r\nСкорость ветра:", i['wind']['speed'],
    "\r\nВидимость:", i['visibility'], "\n____________________________")
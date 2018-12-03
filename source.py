import vk_api
import random
import weather

vk = vk_api.VkApi(token='6caeaaa2c858209287af9e595e16e540bb4e577fa1d2de8e9f54f0af62161e9f893dfcda67eef0071df4f')

def send(id, message):
    vk.method("messages.send",
              {"peer_id": id, "message": message, "random_id": random.randint(0, 9223372036854775807)})

while True:
    messages = vk.method("messages.getConversations", {"filter":"unread"})
    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]
        user = "юзер"
        body = messages["items"][0]["last_message"]
        if body['text'].lower() == "привет":
            send(id, "Привет, " + user)
        elif body['text'].lower() == "покажи погоду":
            message = "Вот температура в городе Москва на 10 дней:\n"
            week = weather.getweather("москва")
            for day in week:
                message += "В " + day['name'] + " " + day['date'] + " днем температура достингет " + day['temp_day'] + ", а вечером " + day['temp_night'] + ".\n"
            send(id, message)
        elif body['text'].lower().find("покажи погоду в городе ") != -1:
            town = body['text'].lower()[23:]
            message = "Вот температура в городе "+body['text'][23:]+" на 10 дней:\n"
            week = weather.getweather(town)
            if week != None:
                for day in week:
                    message += "В " + day['name'] + " " + day['date'] + " днем температура достингет " + day['temp_day'] + ", а вечером " + day['temp_night'] + ".\n"
            else:
                message = "К сожалению, город не найден. Возможно, вы написали название не в именительном падеже."
            send(id, message)
        elif body['text'].lower() == "пока":
            send(id, "Удачи, "+user+"!")
        else:
            send(id, "Я глюпый бот, не понимаю тебя :(")

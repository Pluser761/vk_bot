import vk_api
import random
import weather

vk = vk_api.VkApi(token='6caeaaa2c858209287af9e595e16e540bb4e577fa1d2de8e9f54f0af62161e9f893dfcda67eef0071df4f')

while True:
    messages = vk.method("messages.getConversations", {"filter":"unread"})
    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]
        body = messages["items"][0]["last_message"]
        if body['text'].lower() == "привет":
            vk.method("messages.send", {"peer_id":id, "message":"Привет!", "random_id": random.randint(0, 9223372036854775807)})
        elif body['text'].lower() == "покажи погоду":
            message = "Вот температура на 10 дней:\n"
            week = weather.getweather()
            for day in week:
                message += "В " + day['name'] + " " + day['date'] + " днем температура достингет " + day['temp_day'] + ", а вечером " + day['temp_night'] + ".\n"
            vk.method("messages.send", {"peer_id":id, "message":message, "random_id": random.randint(0, 9223372036854775807)})
        elif body['text'].lower().find("покажи погоду в городе ") != -1:
            town = body['text'].lower()[23:]
            message = "Вот температура в городе "+body['text'][23:]+" на 10 дней:\n"
            week = weather.getweathertown(town)
            if week != None:
                for day in week:
                    message += "В " + day['name'] + " " + day['date'] + " днем температура достингет " + day['temp_day'] + ", а вечером " + day['temp_night'] + ".\n"
            else:
                message = "К сожалению, город не найден. Возможно, вы написали название не в именительном падеже."
            vk.method("messages.send", {"peer_id":id, "message":message, "random_id": random.randint(0, 9223372036854775807)})
        elif body['text'].lower() == "пока":
            vk.method("messages.send", {"peer_id":id, "message": "Удачи!", "random_id": random.randint(0, 9223372036854775807)})
        else:
            vk.method("messages.send", {"peer_id":id, "message": "Я глюпый бот, не понимаю тебя :(", "random_id": random.randint(0, 9223372036854775807)})

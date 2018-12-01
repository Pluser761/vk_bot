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
            message = "Вот тебе температура в Москве на 10 дней:\n"
            week = weather.getweather()
            for day in week:
                message += "В " + day['name'] + ", " + day['date'] + ", температура " + day['temp'] + ".\n"
            vk.method("messages.send", {"peer_id":id, "message":message, "random_id": random.randint(0, 9223372036854775807)})
        elif body['text'].lower().find("покажи погоду в ") == 0:
            town = body['text'].lower()[16:]
            message = "Вот тебе температура в "+body['text']+" на 10 дней:\n"
            week = weather.getweathertown(town)
            for day in week:
                message += "В " + day['name'] + ", " + day['date'] + ", температура " + day['temp'] + ".\n"
            vk.method("messages.send", {"peer_id":id, "message":message, "random_id": random.randint(0, 9223372036854775807)})
        elif body['text'].lower() == "пока":
            vk.method("messages.send", {"peer_id":id, "message": "Удачи!", "random_id": random.randint(0, 9223372036854775807)})
        else:
            vk.method("messages.send", {"peer_id":id, "message": "Я глюпый бот, не понимаю тебя :(", "random_id": random.randint(0, 9223372036854775807)})

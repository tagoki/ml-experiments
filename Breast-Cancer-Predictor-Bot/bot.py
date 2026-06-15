import telebot
import shared
from log_reg import logistik_reg

TOKEN = '8072667336:AAHBqIJEi_ePYE6EsrbQEVl3Rtpf2_5txXQ'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
        "👋 Привет!\n\n"
        "Я — бот, который может предсказать вероятность наличия рака груди 🩺\n"
        "Для этого мне понадобятся *30 параметров опухоли*.\n\n"
        "📊 Вот полный список признаков, которые тебе нужно будет ввести через запятую:\n\n"
        "🔹 *radius (mean)* — средний радиус опухоли\n"
        "🔹 *texture (mean)* — средняя текстура поверхности\n"
        "🔹 *perimeter (mean)* — средний периметр опухоли\n"
        "🔹 *area (mean)* — средняя площадь опухоли\n"
        "🔹 *smoothness (mean)* — средняя гладкость поверхности\n"
        "🔹 *compactness (mean)* — средняя компактность опухоли\n"
        "🔹 *concavity (mean)* — средняя вогнутость контура\n"
        "🔹 *concave points (mean)* — среднее число вогнутых точек\n"
        "🔹 *symmetry (mean)* — средняя симметрия\n"
        "🔹 *fractal dimension (mean)* — средняя фрактальная размерность\n\n"
        "🔸 *radius (se)* — стандартная ошибка радиуса\n"
        "🔸 *texture (se)* — стандартная ошибка текстуры\n"
        "🔸 *perimeter (se)* — стандартная ошибка периметра\n"
        "🔸 *area (se)* — стандартная ошибка площади\n"
        "🔸 *smoothness (se)* — стандартная ошибка гладкости\n"
        "🔸 *compactness (se)* — стандартная ошибка компактности\n"
        "🔸 *concavity (se)* — стандартная ошибка вогнутости\n"
        "🔸 *concave points (se)* — стандартная ошибка вогнутых точек\n"
        "🔸 *symmetry (se)* — стандартная ошибка симметрии\n"
        "🔸 *fractal dimension (se)* — стандартная ошибка фрактальной размерности\n\n"
        "🔺 *radius (worst)* — худший (максимальный) радиус\n"
        "🔺 *texture (worst)* — худшая текстура\n"
        "🔺 *perimeter (worst)* — худший периметр\n"
        "🔺 *area (worst)* — худшая площадь\n"
        "🔺 *smoothness (worst)* — худшая гладкость\n"
        "🔺 *compactness (worst)* — худшая компактность\n"
        "🔺 *concavity (worst)* — худшая вогнутость\n"
        "🔺 *concave points (worst)* — худшее количество вогнутых точек\n"
        "🔺 *symmetry (worst)* — худшая симметрия\n"
        "🔺 *fractal dimension (worst)* — худшая фрактальная размерность\n\n"
        "📥 Отправь команду /predict и введи значения через запятую:\n"
        "`пример: 14.2, 20.3, 90.1, ..., 0.06`\n\n"
        "Я всё обработаю и скажу результат 📡",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['predict'])
def predict_bot(message):
    bot.send_message(message.chat.id, '✍️ Введите 30 параметров опухоли через запятую:')
    bot.register_next_step_handler(message, data_for_log_reg)
    
def data_for_log_reg(message):
    numbers = message.text.split(',')
    
    if len(numbers) != 30:
        bot.send_message(message.chat.id, 'Пожалуйста, запустите снова команду и введите 30 значений')
        return
    
    shared.data = [float(num.strip()) for num in numbers]
    
    result = logistik_reg(shared.data)[0]
    
    if result == 0:
        bot.send_message(message.chat.id,"🔴У вас злокачественная опухоль")
    else:
        bot.send_message(message.chat.id, "🟢У вас доброкачественная опухоль")


bot.infinity_polling()
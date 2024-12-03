from keyboards.reply.search_movie_button import request_movie
from loader import bot
from states.move_search_states import SearchInfo
from telebot.types import Message
from api.request_search_films import search_movie_api


@bot.message_handler(commands=['movie_search'])
def start_search(message: Message) -> None:
    bot.set_state(message.from_user.id, SearchInfo.name_film, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.username}, Введи название фильма!')


@bot.message_handler(state=SearchInfo.name_film)
def get_name_film(message: Message) -> None:

    bot.send_message(message.from_user.id, 'Спасибо записал!\nТеперь введи жанр фильма: ')
    bot.set_state(message.from_user.id, SearchInfo.genre_film, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_film'] = message.text
    print(f'Received message: {data["name_film"]}')

@bot.message_handler(state=SearchInfo.genre_film)
def get_genre_film(message: Message) -> None:

    bot.send_message(message.from_user.id, 'Отлично записал!\nТеперь введи кол-во вариантов фильма: ')
    bot.set_state(message.from_user.id, SearchInfo.output_options, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['genre_film'] = message.text
    print(f'Received message: {data["name_film"]}')
    print(f'Received message: {data["genre_film"]}')

@bot.message_handler(state=SearchInfo.output_options)
def get_output_options(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Замечательно, записал!')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['output_options'] = int(message.text)
        bot.send_message(message.from_user.id, f'Ваш запрос получился таким:\n'
                                               f'Название фильма: {data["name_film"]}\n'
                                               f'Жанр: {data["genre_film"]}\n'
                                               f'Кол-во вариантов фильма: {data["output_options"]}\n'
                                               f'Теперь нажмите кнопку найти для поиска фильма!',
                                                reply_markup=request_movie())
    else:
        bot.send_message(message.from_user.id, 'Количество должно быть числом!')
    print(f'Received message: {data["name_film"]}')
    print(f'Received message: {data["genre_film"]}')
    print(f'Received message: {data["output_options"]}')

@bot.message_handler(func=lambda message: message.text == 'Найти')
def get_search_movie(message: Message) -> None:
    print("Search button handler triggered")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        name = data['name_film']
        genre = data['genre_film']
        limit = data['output_options']
    print(f"Retrieved data: name={name}, genre={genre}, limit={limit}")
    if not name or not genre or not limit:
        bot.send_message(message.from_user.id, 'Кажется, данные не были сохранены. Попробуйте снова.')
        return

    movies = search_movie_api(name, genre, limit)
    print(f'Movies found: {movies}')
    if movies:
        for movie in movies:
            title = movie.get('title')
            year = movie.get('year')
            description = movie.get('description')
            poster_url = movie.get('posterUrl')

            message_text = f'Название: {title}\nОписание: {description}\nГод: {year}\n'

            if poster_url:
                message_text += f'\nФото: {poster_url}'
            bot.send_message(message.from_user.id, message_text)
    else:
        bot.send_message(message.from_user.id, 'Извините, фильм не найден по вашему запросу')

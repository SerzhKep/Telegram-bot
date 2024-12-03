from telebot.handler_backends import State, StatesGroup


class SearchInfo(StatesGroup):
    name_film = State()
    genre_film = State()
    output_options = State()
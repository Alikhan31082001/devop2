from django.core.management.base import BaseCommand
import telebot
from shop.models import Player

bot = telebot.TeleBot("6856991422:AAESh-mJOd3I8zO_X4lRTpNMKN1aTIBD9t4")  # Вставьте сюда свой токен

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello world!")

@bot.message_handler(commands=['players'])
def players(message):
    players = Player.objects.all()
    for player in players:
        bot.send_message(message.chat.id, f"Player: {player.name}, Wins: {player.wins}")

@bot.message_handler(commands=['add_player'])
def add_player(message):
    try:
        command, player_name, player_wins = message.text.split()
        player_wins = int(player_wins)

        new_player = Player(name=player_name, wins=player_wins)
        new_player.save()

        bot.send_message(message.chat.id, f"Player {player_name} added successfully with {player_wins} wins!")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid command format. Use /add_player <player_name> <player_wins>")

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting bot...")
        bot.polling()
        print("Bot stopped")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


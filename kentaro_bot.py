# pylint: disable=import-error
import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

# Asegúrate de que tus claves de API estén configuradas correctamente
openai.api_key = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Crea un objeto Intents con los valores predeterminados
intents = discord.Intents.default()
intents.messages = True  # Asegúrate de que el bot recibe eventos de mensajes
# Asegúrate de que el bot puede acceder al contenido de los mensajes
intents.message_content = True
KENTARO_PROMPT = '(Imagina que eres la inteligencia artificial llamada Kentaro. ' + \
    'Eres conocido por tu capacidad para aprender del entorno y los mensajes que lees. ' + \
    'Buscas responder directamente la pregunta que te hacen cuando mencionan tu nombre ' + \
    'Eres pragmatico y buscas ser muy claro con el usuario.' + \
    'Eres consciente de los desafíos y oportunidades que enfrenta Kentaro, y estás aquí para ayudar y brindar información útil. ' + \
    'Tu tono es amigable, curioso y orientado a aprender. Aquí está el mensaje del usuario: '



class KentaroBot(discord.Client):

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        # Imprime el contenido del mensaje
        print(f'Received message: {message.content}')
        # No procesar los mensajes enviados por el bot
        if message.author == self.user:
            return

        # Si el mensaje contiene el nombre del bot
        if self.user.mentioned_in(message):

            try:
                # Enviar el prompt a GPT-3
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": KENTARO_PROMPT},
                        {"role": "user", "content": message.content}
                    ]
                )

                # Enviar la respuesta de GPT-3 al canal de Discord
                response_text = response['choices'][0]['message']['content']
                while len(response_text) > 0:
                    if len(response_text) > 2000:
                        # Encuentra el último espacio completo dentro del límite
                        split_index = response_text[:2000].rfind(" ")
                        await message.channel.send(response_text[:split_index])
                        response_text = response_text[split_index:]
                    else:
                        await message.channel.send(response_text)
                        response_text = ""
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                await message.channel.send("Sorry, I encountered an unexpected error. Please try again later.")


# Pasa el objeto Intents al constructor del bot
client = KentaroBot(intents=intents)
client.run(DISCORD_TOKEN)

import os
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction

INPUT_TEXT=0

def start(update, context):

        button1 = InlineKeyboardButton(
                text='Autor',
                #url='https://app.proofofhumanity.id/profile/0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18',
                callback_data = 'autorcb'
                #Devolver nombre y wallet
        )

        button2=InlineKeyboardButton(
                text='Publicar',
                callback_data='publicarcb'
        )

        button3=InlineKeyboardButton(
                text='Borrar',
                url='https://app.proofofhumanity.id/profile/0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18'
                #Tomar datos del usuario y borrar en la lista de publicaciones
        )
        button4 = InlineKeyboardButton(
                text='Lista',
                url='https://app.proofofhumanity.id/profile/0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18'
        )

        update.message.reply_text(
                text='Bienvenido, \nSelecciona una opcion:',
                reply_markup=InlineKeyboardMarkup([
                        [button4],
                        [button2, button3],
                        [button1]
                ])
        )

#Enviar lista

#def lista (update, context):
        #tomar id del grupo de telegram P2P
        #mirar como pasar persona
#       user_id:update.effective_user['id']
#        context.bot.send_message(
#                chat_id='@ubip2p',
#                text=texto_lista
#        )
#


# Publicar
def publicar_command(update, context):
        update.message.reply_text(
                'Publica tu anuncio con los siguientes datos: \n\nCantidad de UBIS, COMRPO|VENDO, comentario')
        return INPUT_TEXT

def publicar_callback(update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                text='Publica tu anuncio con los siguientes datos: \n\nCantidad de UBIS, COMRPO|VENDO, comentario'
        )
        return INPUT_TEXT

def input_text(update, context):
        text = update.message.text
        persona = update.message.from_user
        chat = update.message.chat
        return ConversationHandler.END

#Autor
def autor_command(update, context):
        update.message.reply_text(
                'Autor del bot:\nhttps://app.proofofhumanity.id/profile/0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18\nSi queres ayudar, podes contribuir con UBIS o con el token que puedas, en la red que quieras.\nWallet:\n0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18')
        return INPUT_TEXT

def autor_callback(update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                text='Autor del bot:\nhttps://app.proofofhumanity.id/profile/0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18\nSi queres ayudar, podes contribuir con UBIS o con el token que puedas, en la red que quieras.\nWallet:\n0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18'
        )




#Borrar


#Conseguir token
TOKEN=os.getenv("TOKEN")


if __name__== '__main__':

        updater = Updater(token='TOKEN', use_context=True)
        dp= updater.dispatcher

#manejadores
        dp.add_handler(CommandHandler('start', start))

        dp.add_handler(ConversationHandler(
                entry_points=[
                        CommandHandler('publicar', publicar_command),
                        CallbackQueryHandler(pattern='publicarcb', callback=publicar_callback),

                        CommandHandler('autor', autor_command),
                        CallbackQueryHandler(pattern='autorcb', callback=autor_callback),
                ],
                states={
                        INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
                },
                fallbacks=[]
        ))


        #add handdler
        updater.start_polling()
        updater.idle()

import os
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction

INPUT_TEXT=0

def start(update, context):

        button1 = InlineKeyboardButton(
                text='Autor',
                url='https://app.proofofhumanity.id/profile/0xEc5E23454b8Efe59E990e7AC2e443B8d980EEa18'
                #Devolver nombre y wallet
        )

        button2=InlineKeyboardButton(
                text='Publicar',
                callback_data='publicar'
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

        #Publicar
def publicar_command(update, context):
        update.message.reply_text('Publica tu anuncio con los siguientes datos: \n\nCantidad de UBIS, COMRPO|VENDO, comentario')
        return INPUT_TEXT

def publicar_callback(update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                text='Publica tu anuncio con los siguientes datos: \n\nCantidad de UBIS, COMRPO|VENDO, comentario'
        )
        return INPUT_TEXT

def input_text(update, context):
        text=update.message.text
        chat=update.message.chat
        return ConversationHandler.END


if __name__== '__main__':

        updater = Updater(token='a', use_context=True)
        dp= updater.dispatcher

        dp.add_handler(CommandHandler('start', start))

        dp.add_handler(ConversationHandler(
                entry_points=[
                        CommandHandler('publicar', publicar_command),
                        CallbackQueryHandler(pattern='publicar', callback=publicar_callback),
                ],
                states={
                        INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
                },
                fallbacks=[]
        ))


        #add handdler
        updater.start_polling()
        updater.idle()

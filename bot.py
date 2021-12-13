from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction
#Google
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd

INPUT_TEXT=0

# Google
nSHEET='publi'
SPREAD_KEY='SPREAD'
CREDS_JSON = 'access-key.json'
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDS_JSON,
        scope
)
client = gspread.authorize(creds)
gsheet = client.open_by_key(SPREAD_KEY)

#termina Google
def start(update, context):
        user = update.message.from_user.username
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
                callback_data='listacb'
        )

        update.message.reply_text(
                f'Bienvenido {update.message.from_user.username}, \nSelecciona una opcion:',
                reply_markup=InlineKeyboardMarkup([
                        [button4],
                        [button2, button3],
                        [button1]
                ])
        )
#Enviar lista

def lista_command (update, context):
#       tomar id del grupo de telegram P2P
#       mirar como pasar persona
#        user_id:update.effective_user['id']
#        context.bot.send_message(
#               chat_id='@ubip2p',

        '''
        columna 1
        itemss = get_items()
        for a in itemss:
                update.message.reply_text(a)
        '''
        items = get_items()
        update.message.reply_text(f'{items}')
#TO-DO: Sacar id de pandas y primer fila.
#TO-DO: Poner @ antes del nombre

def lista_callback(update, context):
        query = update.callback_query
        query.answer()
        items = get_items()
        query.edit_message_text('Lista:')
        query.message.reply_text(
                f'{items}'
        )
#TO-DO: Sacar id de pandas y primer fila.

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


#Fin
def fin_conv(update, context):
        return ConversationHandler.END

#Google
def get_items():
        items = get_sheet(nSHEET)
        return items

#Toma los valores de la segunda columna
def get_sheetcol(sheet_name):
        sheet = gsheet.worksheet(sheet_name)
        items = sheet.col_values(2)
        return items

#anterior (toma todos los valores como lsita de listas)
def get_sheet(sheet_name):
        sheet = gsheet.worksheet(sheet_name)
        items = pd.DataFrame(sheet.get_all_records())
        return items


def store_publi(update,context):
        text = update.message.text
        user = update.message.from_user.username
        chat = update.message.chat

        sheet = gsheet.worksheet(nSHEET)
        clients = pd.DataFrame(get_sheet(nSHEET))
        cond = sheet.findall(user)

        if (cond == []):
                sheet.add_rows(1)
                sheet.append_row([text,user])
                update.message.reply_text(f'El anuncio ha sido creado.')
        else:
                update.message.reply_text(f'Ya existe un anuncio hecho al nombre de @{user}.\nBorralo para publicar uno nuevo.')
        return ConversationHandler.END



if __name__== '__main__':

        updater = Updater(token='TOKEN', use_context=True)
        dp= updater.dispatcher

#manejadores
        dp.add_handler(CommandHandler('start', start))

        dp.add_handler(ConversationHandler(
                entry_points=[
                        CommandHandler('autor', autor_command),
                        CallbackQueryHandler(pattern='autorcb', callback=autor_callback),

                        CommandHandler('lista', lista_command),
                        CallbackQueryHandler(pattern='listacb', callback=lista_callback),
                ],
                states={
                        INPUT_TEXT: [MessageHandler(Filters.text, fin_conv)]
                },
                fallbacks=[]
        ))

        dp.add_handler(ConversationHandler(
                entry_points=[
                        CommandHandler('publicar', publicar_command),
                        CallbackQueryHandler(pattern='publicarcb', callback=publicar_callback),
                ],
                states = {
                        INPUT_TEXT: [MessageHandler(Filters.text, store_publi)]
                 },
                 fallbacks = []
        ))

        #add handdler
        updater.start_polling()
        updater.idle()

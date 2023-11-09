import asyncio
from create_bot import dp, bot
from data_base import sqlite_db_chanall, post_opl, date_opl
from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from aiocryptopay import AioCryptoPay, Networks

load_dotenv()

PAY = os.getenv("PAY")


async def send_invoice(user_id, channel, tariff, data, text, photo,sost):
    global sos
    global id
    global chanal
    global tarif
    global data_user
    global text_user
    global photo_user
    sos = sost
    id = user_id
    chanal = channel
    tarif = tariff
    data_user = data
    text_user = text
    photo_user = photo
    print('FFF')
    print(id, chanal, tarif, data_user, text_user)
    amount = int(sqlite_db_chanall.price_slc(chanal, tarif))
    print(amount)
    amount = amount*100
    await bot.send_invoice(
        chat_id=id,
        title='Покупка рекламы',
        description='Покупка рекламы',
        payload='invoice_payload',
        provider_token=PAY,
        currency='RUB',
        prices=[types.LabeledPrice(label='Покупка рекламы', amount=amount)]
    )


@dp.pre_checkout_query_handler()
async def pre_checkout_query_handler(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state: FSMContext):
    if sos == 1:
        payment_info = message.successful_payment
        invoice_payload = payment_info.invoice_payload
        print(invoice_payload)
        print(tarif)
        if tarif != 'На месяц':
            print(data_user)
            await date_opl.sql_add_command(chanal, data_user)
        else:
            new_date_obj0 = datetime.strptime(data_user, '%d:%m:%Y')
            new_date_obj0.strftime('%d:%m:%Y')
            formatted_date0 = new_date_obj0.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date0)
            new_date_obj1 = new_date_obj0 + timedelta(days=7)
            new_date_obj1.strftime('%d:%m:%Y')
            formatted_date1 = new_date_obj1.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date1)
            new_date_obj2 = new_date_obj1 + timedelta(days=7)
            new_date_obj2.strftime('%d:%m:%Y')
            formatted_date2 = new_date_obj2.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date2)
            new_date_obj3 = new_date_obj2 + timedelta(days=7)
            new_date_obj3.strftime('%d:%m:%Y')
            formatted_date3 = new_date_obj3.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date3)
            new_date_obj4 = new_date_obj3 + timedelta(days=7)
            new_date_obj4.strftime('%d:%m:%Y')
            formatted_date4 = new_date_obj4.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date4)
        await post_opl.sql_add_command(id, chanal, tarif, data_user,
                                       text_user, photo_user)
        await bot.send_message(id, "Спасибо за оплату!")
    else:
        print('Оплачено из админки ')
        payment_info = message.successful_payment
        invoice_payload = payment_info.invoice_payload
        print(invoice_payload)
        user_id = message.from_user.id
        print(tarif)
        if tarif != 'На месяц':
            print(data_user)
            await date_opl.sql_add_command(chanal, data_user)
        else:
            new_date_obj0 = datetime.strptime(data_user, '%d:%m:%Y')
            new_date_obj0.strftime('%d:%m:%Y')
            formatted_date0 = new_date_obj0.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date0)
            new_date_obj1 = new_date_obj0 + timedelta(days=7)
            new_date_obj1.strftime('%d:%m:%Y')
            formatted_date1 = new_date_obj1.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date1)
            new_date_obj2 = new_date_obj1 + timedelta(days=7)
            new_date_obj2.strftime('%d:%m:%Y')
            formatted_date2 = new_date_obj2.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date2)
            new_date_obj3 = new_date_obj2 + timedelta(days=7)
            new_date_obj3.strftime('%d:%m:%Y')
            formatted_date3 = new_date_obj3.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date3)
            new_date_obj4 = new_date_obj3 + timedelta(days=7)
            new_date_obj4.strftime('%d:%m:%Y')
            formatted_date4 = new_date_obj4.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal, formatted_date4)
        await post_opl.sql_add_command(id, chanal, tarif, data_user,
                                       text_user, photo_user)
        await bot.send_message(id, "Спасибо за оплату!")


async def crypto(user_id, channel, tariff, data, text, photo, valute):
    global valute_c
    global id_c
    global chanal_c
    global tarif_c
    global data_user_c
    global text_user_c
    global photo_user_c
    valute_c = valute
    id_c = user_id
    chanal_c = channel
    tarif_c = tariff
    data_user_c = data
    text_user_c = text
    photo_user_c = photo
    print('CCC')
    print(id_c, chanal_c, tarif_c, data_user_c, text_user_c)
    amount = int(sqlite_db_chanall.price_slc(chanal_c, tarif_c))
    print('Я здесь Crypto')
    crypto = AioCryptoPay(token='121562:AAFUy1NdIINcNA4aRrb7PSOrxg0HU3kvBgN', network=Networks.MAIN_NET)
    try:
        amount = await crypto.get_amount_by_fiat(summ=amount, asset=f'{valute_c}', target='RUB')
        invoice = await crypto.create_invoice(asset=f'{valute_c}', amount=amount)
        await bot.send_message(id_c, invoice.pay_url)
        print(invoice.pay_url)
        invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
        print(invoices.status)
        while invoices.status != 'paid':
            await asyncio.sleep(60)
            invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
        if tarif_c != 'На месяц':
            print(data_user_c)
            await date_opl.sql_add_command(chanal_c, data_user_c)
        else:
            new_date_obj0 = datetime.strptime(data_user_c, '%d:%m:%Y')
            new_date_obj0.strftime('%d:%m:%Y')
            formatted_date0 = new_date_obj0.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal_c, formatted_date0)
            new_date_obj1 = new_date_obj0 + timedelta(days=7)
            new_date_obj1.strftime('%d:%m:%Y')
            formatted_date1 = new_date_obj1.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal_c, formatted_date1)
            new_date_obj2 = new_date_obj1 + timedelta(days=7)
            new_date_obj2.strftime('%d:%m:%Y')
            formatted_date2 = new_date_obj2.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal_c, formatted_date2)
            new_date_obj3 = new_date_obj2 + timedelta(days=7)
            new_date_obj3.strftime('%d:%m:%Y')
            formatted_date3 = new_date_obj3.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal_c, formatted_date3)
            new_date_obj4 = new_date_obj3 + timedelta(days=7)
            new_date_obj4.strftime('%d:%m:%Y')
            formatted_date4 = new_date_obj4.strftime('%d:%m:%Y')
            await date_opl.sql_add_command(chanal_c, formatted_date4)
        await post_opl.sql_add_command(id_c, chanal_c, tarif_c, data_user_c,
                                       text_user_c, photo_user_c)
        await bot.send_message(id_c, "Спасибо за оплату!")
    finally:
        await crypto.close()




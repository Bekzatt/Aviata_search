import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bs4 import BeautifulSoup
import airports
import config
from aiogram_calendar import SimpleCalendar, DialogCalendar, simple_cal_callback, dialog_cal_callback
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import database
from userState import userState, userReg

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

inlineBtnBack = InlineKeyboardButton('Артқа', callback_data="t:back")
inlineBtnForward = InlineKeyboardButton('Алға', callback_data="t:forward")
async def getPage(user, message, state):
    PATH = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=PATH)
    fdate =  user[5][:user[5].index(' ')].replace("-","")
    await message.answer('Билеттер іздестірілуде..')
    if user[2] is False:
        sdate = user[6][:user[6].index(' ')].replace("-","")#datetime.strptime(user[6][:user[6].index(' ')], '%Y-%m-%d')
        url = f"https://aviata.kz/aviax/search/{user[3]}-{user[4]}{fdate}{user[4]}-{user[3]}{sdate}1000E?source=None&widget=0"
    else:
        url = f"https://aviata.kz/aviax/search/{user[3]}-{user[4]}{fdate}1000E?source=None&widget=0"
    driver.get(url)
    print(url)
    await asyncio.sleep(10)
    with open(f"{str(user[0])}.html", 'w', encoding="UTF-8") as file:
        file.write(driver.page_source)
    with open(f"{str(user[0])}.html", 'r', encoding="UTF-8") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, features="lxml")
        tickets = soup.find('div', class_='flex flex-col')
        ticks = tickets.find_all('div', class_='rounded offers-groups-item mb-4')
        tickets_list = []
        if user[2] is False:
            for t in ticks:
                tick = {}
                if t.find('div', class_='flex absolute top-0 left-0') is not None:
                    tick['special']=t.find('div', class_='flex absolute top-0 left-0').text
                else: tick['special']=None
                flights = t.find_all('div',class_='offer-flight')
                counter = 0
                for flight in flights:
                    if counter == 0:
                        tick['departure_company']=flight.find('span', class_='text-xs').text
                        tick['departure_day']=(flight.find('div', class_='ml-2')).find('div', class_='pb-1 text-xs text-black').text
                        tick['departure_time']=(flight.find('div', class_='ml-2')).find('strong', class_='font-semibold text-2xl leading-none').text
                        tick['flight_time']=(flight.find('div', class_='mx-auto w-48')).find('div',class_='text-center text-xs text-gray-700').text
                        spans = (flight.find('div', class_='mx-auto w-48')).find_all('span')
                        c = 0
                        for sp in spans:
                            if c==0:
                                tick['departure_city']=sp.text
                            if c==1:
                                tick['arrival_city']=sp.text
                            c+=1
                        tick['arrival_day']=(flight.find('div', class_='')).find('div', class_='relative pb-1 text-xs text-black').text
                        tick['arrival_time'] = (flight.find('div', class_='')).find('strong', class_='font-semibold text-2xl leading-none').text
                    if counter == 1:
                        tick['return_departure_company'] = flight.find('span', class_='text-xs').text
                        tick['return_departure_day'] = (flight.find('div', class_='ml-2')).find('div',
                                                                                         class_='pb-1 text-xs text-black').text
                        tick['return_departure_time'] = (flight.find('div', class_='ml-2')).find('strong',
                                                                                          class_='font-semibold text-2xl leading-none').text
                        tick['return_flight_time'] = (flight.find('div', class_='mx-auto w-48')).find('div',
                                                                                               class_='text-center text-xs text-gray-700').text
                        spans = (flight.find('div', class_='mx-auto w-48')).find_all('span')
                        c = 0
                        for sp in spans:
                            if c == 0:
                                tick['return_departure_city'] = sp.text
                                print(sp.text)
                            if c == 1:
                                tick['return_arrival_city'] = sp.text
                                print(sp.text + 'M')
                            c += 1
                        tick['return_arrival_day'] = (flight.find('div', class_='')).find('div',
                                                                                   class_='relative pb-1 text-xs text-black').text
                        tick['return_arrival_time'] = (flight.find('div', class_='')).find('strong',
                                                                                    class_='font-semibold text-2xl leading-none').text
                    counter+=1
                tick['price'] = t.find('strong', class_='text-2xl font-semibold leading-none').text
                tickets_list.append(tick)
        else:
            for t in ticks:
                tick = {}
                if t.find('div', class_='flex absolute top-0 left-0') is not None:
                    tick['special']=t.find('div', class_='flex absolute top-0 left-0').text
                else: tick['special']=None
                flights = t.find_all('div',class_='offer-flight')
                for flight in flights:
                    tick['departure_company']=flight.find('span', class_='text-xs').text
                    tick['departure_day']=(flight.find('div', class_='ml-2')).find('div', class_='pb-1 text-xs text-black').text
                    tick['departure_time']=(flight.find('div', class_='ml-2')).find('strong', class_='font-semibold text-2xl leading-none').text
                    tick['flight_time']=(flight.find('div', class_='mx-auto w-48')).find('div',class_='text-center text-xs text-gray-700').text
                    spans = (flight.find('div', class_='mx-auto w-48')).find_all('span')
                    c = 0
                    for sp in spans:
                        if c==0:
                            tick['departure_city']=sp.text
                        if c==1:
                            tick['arrival_city']=sp.text
                        c+=1
                    tick['arrival_day']=(flight.find('div', class_='')).find('div', class_='relative pb-1 text-xs text-black').text
                    tick['arrival_time'] = (flight.find('div', class_='')).find('strong', class_='font-semibold text-2xl leading-none').text
                tick['price'] = t.find('strong', class_='text-2xl font-semibold leading-none').text
                tickets_list.append(tick)
    async with state.proxy() as data:
        data['tickets']=tickets_list
        if len(tickets_list)!=0:
            await userReg.tickets_found.set()
            await message.answer('Билеттер табылды!', reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add('Көру'))
        else:
            await message.answer('Сіздің таңдаған уақытқа өкінішке орай билеттер табылмады')
    driver.quit()

@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    if database.getUser(message.from_user.id) is None:
        await message.answer(f'Сәлеметсіз бе, {message.from_user.username}, Avia ticket saler ге қош келдіңіз!\n'
                             f'Билеттерді іздестіру үшін алдымен төмендегі сұрақтарға жауап беріңіз.')
        await userState.name.set()
        await message.answer(f'Аты-жөніңізді жазыңыз:')
    else:
        user = database.getUser(message.from_user.id)
        async with state.proxy() as data:
            data['name'] = user[1]
        kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add('Билет іздеу')
        await message.answer(f'Сәлеметсіз бе, {str(user[1])}, Avia ticket saler ге қош келдіңіз!', reply_markup=kb)
        await userReg.registered.set()


@dp.message_handler(text=['Көру'], state=userReg.tickets_found)
async def showTickets(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ls = []
        for ticket in data['tickets']:
            m = ""
            print(ticket)
            if ticket['special'] is not None:
                m+=f"<i>{ticket['special']}</i>\n"
            try:
                m+=f"<b>Ұшып кету:</b> \n" \
                   f"Әуе компания: {ticket['departure_company']}\n" \
                   f"Ұшатын уақыты: {ticket['departure_day']} {ticket['departure_time']}\n" \
                   f"Ұшу уақыты: {ticket['flight_time']}\n" \
                   f"{ticket['departure_city']} -> {ticket['arrival_city']}\n" \
                   f"Ұшып бару уақыты: {ticket['arrival_day']} {ticket['arrival_time']}\n"
            except:
                m+=f"<b>Ұшып кету:</b> \n" \
                   f"Әуе компания: {ticket['departure_company']}\n" \
                   f"Ұшатын уақыты: {ticket['departure_day']} {ticket['departure_time']}\n" \
                   f"Ұшу уақыты: {ticket['flight_time']}\n" \
                   f"Ұшып бару уақыты: {ticket['arrival_day']} {ticket['arrival_time']}\n"

            if "return_departure_company" in ticket.keys():
                try:
                    m+=f"<b>Ұшып келу:</b> \n" \
                       f"Әуе компания: {ticket['return_departure_company']}\n" \
                       f"Ұшатын уақыты: {ticket['return_departure_day']} {ticket['return_departure_time']}\n" \
                       f"Ұшу уақыты: {ticket['return_flight_time']}\n" \
                       f"{ticket['return_departure_city']} -> {ticket['return_arrival_city']}\n" \
                       f"Ұшып бару уақыты: {ticket['return_arrival_day']} {ticket['return_arrival_time']}\n"
                except:
                    m+=f"<b>Ұшып келу:</b> \n" \
                       f"Әуе компания: {ticket['return_departure_company']}\n" \
                       f"Ұшатын уақыты: {ticket['return_departure_day']} {ticket['return_departure_time']}\n" \
                       f"Ұшу уақыты: {ticket['return_flight_time']}\n" \
                       f"Ұшып бару уақыты: {ticket['return_arrival_day']} {ticket['return_arrival_time']}\n"

            m+=f'Бағасы: {ticket["price"]}\n'


            ls.append(m)
        data['messages']=ls
        data['tickindex']=0
        await message.answer(ls[0],reply_markup=InlineKeyboardMarkup().add(*[inlineBtnBack,inlineBtnForward]), parse_mode='HTML')



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('t:'),state='*')
async def ticket_info(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data == 't:back':
            if data['tickindex'] == 0:
                await callback_query.answer("Бұл бірінші билет")
            else:
                data['tickindex'] -= 1
                await callback_query.message.edit_text(data['messages'][data['tickindex']], reply_markup=InlineKeyboardMarkup().add(*[inlineBtnBack, inlineBtnForward]), parse_mode='HTML')
        else:
            if len(data['messages'])-1 == data['tickindex']:
                await callback_query.answer("Бұл соңғы билет")
            else:
                data['tickindex'] += 1
                await callback_query.message.edit_text(data['messages'][data['tickindex']], reply_markup=InlineKeyboardMarkup().add(*[inlineBtnBack, inlineBtnForward]), parse_mode='HTML')

@dp.message_handler(text=['Билет табу'], state=userReg.search_ticket)
async def searchTicket(message: types.Message, state: FSMContext):
    user = database.getUser(message.from_user.id)
    asyncio.create_task(getPage(user, message, state))


@dp.message_handler(text=['Билет іздеу'], state=userReg.registered)
async def start_v2(message: types.Message, state: FSMContext):
    await userState.source.set()
    async with state.proxy() as data:
        data['reg'] = True
    await message.answer(f'Қай қаладан ұшасыз?')


@dp.message_handler(state=userState.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Қай қаладан ұшасыз?')
    await userState.source.set()


@dp.message_handler(state=userState.source)
async def source(message: types.Message, state: FSMContext):
    if message.text.lower() in airports.cities.keys():
        async with state.proxy() as data:
            data['source'] = airports.cities[message.text.lower()]
        await userState.next()
        await message.answer('Қай қалаға ұшасыз?')
    else:
        kb = InlineKeyboardMarkup()
        ls = []
        btns = []
        counter = 0
        for city in airports.cities.keys():
            if airports.cities[city] not in ls:
                counter += 1
                ls.append(airports.cities[city])
                btns.append(InlineKeyboardButton(city.capitalize(), callback_data='city:' + city.capitalize()))
                if counter == 3:
                    kb.row(*btns)
                    btns = []
                    counter = 0
        await message.reply('Қала есімі дұрыс емес. Ұшатын мекен анықталмады!\n'
                            'Қайтадан теріп көріңіз, немесе төмендегі тізімнен таңдаңыз.')
        await message.answer('Қай қаладан ұшасыз?', reply_markup=kb)
        await userState.source.set()


@dp.message_handler(state=userState.dest)
async def dest(message: types.Message, state: FSMContext):
    if message.text.lower() in airports.cities.keys():
        async with state.proxy() as data:
            if airports.cities[message.text.lower()] != data['source']:
                data['dest'] = airports.cities[message.text.lower()]
                await userState.next()
                kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                    *(['Бір жақты', 'Екі жақты']))
                r = await message.answer('Рейс типі:', reply_markup=kb)
                data['r'] = r
            else:
                await message.answer('Таңдалған қалалар екі түрлі болуы міндетті!\n'
                                     'Қай қалаға ұшасыз?')
                await userState.dest.set()
                return
    else:
        kb = InlineKeyboardMarkup()
        ls = []
        btns = []
        counter = 0
        for city in airports.cities.keys():
            async with state.proxy() as data:
                if airports.cities[city] not in ls and data['source'] != airports.cities[city]:
                    counter += 1
                    ls.append(airports.cities[city])
                    btns.append(InlineKeyboardButton(city.capitalize(), callback_data='tocity:' + city.capitalize()))
                    if counter == 3:
                        kb.row(*btns)
                        btns = []
                        counter = 0
        await message.reply('Қала есімі дұрыс емес. ұшып баратын мекен анықталмады!\n'
                            'Қайтадан теріп көріңіз, немесе төмендегі тізімнен таңдаңыз.')
        await message.answer('Қай қалаға ұшасыз?', reply_markup=kb)
        await userState.dest.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('tocity:'), state=userState.dest)
async def dest_rep(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(callback_query.message.text + '\n\n'
                                                                         '<b>>' + callback_query.data.replace('tocity:',
                                                                                                              '') + '</b>',
                                           reply_markup=None, parse_mode='HTML')
    await userState.type.set()
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(*(['Бір жақты', 'Екі жақты']))
    r = await callback_query.message.answer('Рейс типі:', reply_markup=kb)
    async with state.proxy() as data:
        data['dest'] = airports.cities[callback_query.data.replace('tocity:', '').lower()]
        data['r'] = r


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('city:'), state=userState.source)
async def source_rep(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(callback_query.message.text + '\n\n'
                                                                         '<b>>' + callback_query.data.replace('city:',
                                                                                                              '') + '</b>',
                                           reply_markup=None, parse_mode='HTML')
    async with state.proxy() as data:
        data['source'] = airports.cities[callback_query.data.replace('city:', '').lower()]
    await userState.next()
    await callback_query.message.answer('Қай қалаға ұшасыз?')


@dp.message_handler(text=['Бір жақты'], state=userState.type)
async def oneDirect(message: types.Message, state: FSMContext):
    await message.answer('Ұшу күнін белгілеңіз', reply_markup=await SimpleCalendar().start_calendar())
    async with state.proxy() as data:
        data['type'] = 'one'
    await userState.flight_date.set()


@dp.message_handler(text=['Екі жақты'], state=userState.type)
async def oneDirect(message: types.Message, state: FSMContext):
    await message.answer('Ұшу күнін белгілеңіз', reply_markup=await SimpleCalendar().start_calendar())
    async with state.proxy() as data:
        data['type'] = 'two'
    await userState.next()


@dp.callback_query_handler(simple_cal_callback.filter(), state=userState.flight_date)
async def flight_date(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['flight_date'] = date
            await callback_query.message.edit_text("Ұшу күні: <b>" + date.strftime("%b %d %Y") + "</b>",
                                                   parse_mode='HTML')
            if data['type'] == 'two':
                await callback_query.message.answer('Ұшып келу күнін белгілеңіз',
                                                    reply_markup=await SimpleCalendar().start_calendar())
                await userState.return_date.set()
            else:
                database.setUser(callback_query.from_user.id, data)
                await bot.send_message(callback_query.from_user.id, 'Профиль толтырылды!',
                                       reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                        resize_keyboard=True).add('Билет табу'))
                await userReg.search_ticket.set()


@dp.callback_query_handler(simple_cal_callback.filter(), state=userState.return_date)
async def return_date(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            await callback_query.message.edit_text("Ұшып келу күні: <b>" + date.strftime("%b %d %Y") + "</b>",
                                                   parse_mode='HTML')
            data['return_date'] = date
            database.setUser(callback_query.from_user.id, data)
            await userReg.search_ticket.set()
            await bot.send_message(callback_query.from_user.id, 'Профиль толтырылды!',
                                   reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                                       'Билет табу'))


executor.start_polling(dp, skip_updates=True)

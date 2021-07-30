from pizza import bot, dp, categories
from aiogram.types import Message, CallbackQuery, LabeledPrice, InputMediaPhoto
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.message import ContentType
from aiogram import types
import datetime
import asyncio
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://Vladimir:kGQa9Xf6dT9cpp6@mycluster.wsthj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster.testdb
coll = db.active_tables
deliver = db.active_delivery
users = db.users
black = db.black

category_callback = CallbackData("food", "category", "dop_prefix")
mounths = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
room = 'AgACAgIAAxkBAAIbaWECUzRUL3fLep3-289Sapv6mLklAAK0sjEb3SsQSN79xZaeJA7nAQADAgADcwADIAQ'

phone_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = KeyboardButton(text="Отправить номер телефона", request_contact=True)
phone_keyboard.add(button_phone)

location_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Посмотреть на карте 🔍', url='https://www.google.ru/maps/place/KAIF+Provenance/@55.7623109,37.61288,19z/data=!4m5!3m4!1s0x46b54bbd4f406b65:0x8a3cdb6c29efb80c!8m2!3d55.7622237!4d37.6135624')]])

class WBMenu(StatesGroup):
	basket = State()
	table_state = State()
	blacklist = State()
	support = State()
	admin_support = State()

async def search_tables(client_day, client_time, tables):

	free_tables = []
	close_tables = []


	for table in tables:
		if table['start'] == client_time or table['start'] - 1 == client_time or table['start'] + 1 == client_time:
			close_tables.append(table['table'])
			

	for free_table in range(1, 16):
		if free_table in close_tables:
			pass
		else:
			free_tables.append(free_table)

	return free_tables

async def search_times(client_day):
	tables = coll.find({'day': client_day}, {'table': 1, 'start': 1})

	free_times = []

	for time in range(8, 23):
		free_tables = await search_tables(client_day, time, tables)
		if free_tables == []:
			pass
		else:
			free_times.append(time)

	return free_times

async def search_days():

	free_days = []

	for day in range(1, 15):
		my_datetime = datetime.datetime.now()
		client_day = my_datetime + datetime.timedelta(days = day)
		client_day = int(client_day.strftime("%d"))

		free_times = await search_times(client_day)
		if free_times == []:
			free_days.append(0)
		else:
			free_days.append(client_day)

	return free_days


pizza_button = InlineKeyboardButton(text='Пицца 🍕', callback_data = "food:pizza:selector")
burger_button = InlineKeyboardButton(text='Бургеры 🍔', callback_data = "food:burgers:selector")
snack_button = InlineKeyboardButton(text='Снеки 🍟', callback_data = "food:snacks:selector")
drink_button = InlineKeyboardButton(text='Напитки 🥤', callback_data = "food:drinks:selector")

category_battons = {'pizza': pizza_button, 'burgers': burger_button, 'snacks': snack_button, 'drinks': drink_button}

helper = 'Заказать доставку: /delivery 🍕\n'
helper += 'Забронировать столик: /book 🥂\n'
helper += 'Задать вопрос: /support\n'
helper += 'Где мы находимся: /location\n'
helper += 'Контактный номер телефона: 88005553535 📞'

@dp.message_handler(Command('start')) #запуск
async def welcome(message: Message):
	my_user = users.find({'telegram': message.from_user.id}, {'telegram': 1})
	blacklist_user = black.find({'telegram': message.from_user.id}, {'telegram': 1})
	if blacklist_user.count() == 0:
		if my_user.count() == 0:
			await bot.send_message(chat_id=message.from_user.id, text='Вы ещё не авторизованы? 🧐 Отправьте свой номер телефона. Это не займет больше 2 секунд.', reply_markup=phone_keyboard)
		else:
			await bot.send_message(chat_id=message.from_user.id, text=f'Привет {message.from_user["first_name"]}, готов заказать или забронировать столик?😁\nКак это работает: /help')

@dp.message_handler(content_types=['contact'])
async def get_phone(message: Message):
	if message.contact is not None:
		phone= str(message.contact.phone_number)

		users.insert_one({
			'user_name': message['from']['first_name'],
			'telegram': message.from_user.id,
			'phone_number': phone
			})

		await bot.send_message(message.chat.id, 'Вы успешно авторизовались!😎', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(Command('location')) #расположение
async def get_location(message: Message):
	await bot.send_photo(message.chat.id, photo='AgACAgIAAxkBAAIb9mEC7RLUJ7e8hLpJC_bGX7YpbmtEAAKFtjEb3SsYSO7PMkvLNq5hAQADAgADcwADIAQ', caption='Ул. Большая Дмитровка, 13, Москва (этаж 3)', reply_markup=location_keyboard)

@dp.message_handler(Command('blacklist')) #черный список
async def get_add_blacklist(message: Message):
	if message.from_user.id == 1187668903:
		await message.answer('Введите id пользователя:')
		await WBMenu.blacklist.set()

@dp.message_handler(state=WBMenu.blacklist) #принять пост
async def get_add_blacklist_2(message: Message):
	blacklist_user = black.find({'telegram': message.text}, {'telegram': 1})
	if blacklist_user.count() == 0:
		black.insert_one({'telegram': int(message.text)})
	else:
		await message.answer('Этот пользователь уже в черном списке')
	await state.finish()	

@dp.message_handler(Command('support')) #Задать вопрос
async def client_support(message: Message):
	blacklist_user = black.find({'telegram': message.from_user.id}, {'telegram': 1})
	if blacklist_user.count() == 0:
		my_user = users.find({'telegram': message.from_user.id}, {'telegram': 1})
		if my_user.count() == 0:
			await bot.send_message(chat_id=message.from_user.id, text='Вы ещё не авторизованы? 🧐 Отправьте свой номер телефона. Это не займет больше 2 секунд.', reply_markup=phone_keyboard)
		else:
			await message.answer('Введите вопрос который хотели бы задать:')
			await WBMenu.support.set()

@dp.message_handler(state=WBMenu.support) #принять вопрос админу
async def send_question(message: Message, state: FSMContext):
	await state.finish()
	await bot.send_message(chat_id=message.from_user.id, text='Вопрос рассматривается...')
	support_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '✉️ Ответить ✉️', callback_data = f"reply{message.from_user.id}")]])
	await bot.send_message(chat_id=1187668903, text=f'Вопрос от {message.from_user["first_name"]} {message.from_user["last_name"]}\nId:{message.from_user.id}\n{message.text}', reply_markup=support_menu)

@dp.callback_query_handler(text_contains="reply") #принять ответ клиенту
async def admin_support(call: CallbackQuery, state: FSMContext):
	await call.message.edit_reply_markup()
	user_id = call["data"][5:]
	await bot.send_message(chat_id=call["from"]["id"], text='Введите ответ на вопрос:')
	await WBMenu.admin_support.set()
	await state.update_data(id=user_id)

@dp.message_handler(state=WBMenu.admin_support) #ответить клиенту
async def send_answer(message: Message, state: FSMContext):
	data = await state.get_data()
	user_id = data.get("id")
	await state.finish()
	await bot.send_message(chat_id=user_id, text=f'Администратор:\n{message.text}')

@dp.message_handler(Command('help')) #help
async def get_help(message: Message):
	blacklist_user = black.find({'telegram': message.from_user.id}, {'telegram': 1})
	if blacklist_user.count() == 0:
		await bot.send_message(chat_id=message.from_user.id, text=helper)

@dp.message_handler(Command('delivery')) #запуск
async def get_delivery(message: Message, state: FSMContext):
	#print(message)
	blacklist_user = black.find({'telegram': message.from_user.id}, {'telegram': 1})
	if blacklist_user.count() == 0:

		my_user = users.find({'telegram': message.from_user.id}, {'telegram': 1})

		if my_user.count() == 0:
			await bot.send_message(chat_id=message.from_user.id, text='Вы ещё не авторизованы? 🧐 Отправьте свой номер телефона. Это не займет больше 2 секунд.', reply_markup=phone_keyboard)
		else:
			my_food = categories['pizza'][0]
			await state.update_data(category='pizza', item=0, bascket={'items': [], 'all_price': 0})
				#print(message)
			deliv_menu = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='⬅️ Назад', callback_data = "back"), InlineKeyboardButton(text='Вперед ➡️', callback_data = "next")],
				[InlineKeyboardButton(text='Добавить', callback_data = "add")],
				[InlineKeyboardButton(text='Категории:', callback_data = "button")],
				[burger_button, snack_button, drink_button]
				#[InlineKeyboardButton(text='Корзина 🛒', callback_data = "basket")]
				])
			await bot.send_photo(chat_id=message.from_user.id, photo=my_food['item_id'], caption=f'<b>{my_food["name"]}</b>\n{my_food["description"]}\nЦена: {my_food["price"]} ₽', reply_markup=deliv_menu)

@dp.callback_query_handler(text='delivery')
async def get_delivery_callback(call: CallbackQuery, state: FSMContext):
	bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)

	my_user = users.find({'telegram': call['from']['id']}, {'telegram': 1})

	if my_user.count() == 0:
		await bot.send_message(chat_id=call['from']['id'], text='Вы ещё не авторизованы? 🧐 Отправьте свой номер телефона. Это не займет больше 2 секунд.', reply_markup=phone_keyboard)
	else:
		my_food = categories['pizza'][0]
		await state.update_data(category='pizza', item=0, bascket={'items': [], 'all_price': 0})
		deliv_menu = InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text='⬅️ Назад', callback_data = "back"), InlineKeyboardButton(text='Вперед ➡️', callback_data = "next")],
			[InlineKeyboardButton(text='Добавить', callback_data = "add")],
			[InlineKeyboardButton(text='Категории:', callback_data = "button")],
			[burger_button, snack_button, drink_button]
			])
		await bot.send_photo(chat_id=call['from']['id'], photo=my_food['item_id'], caption=f'<b>{my_food["name"]}</b>\n{my_food["description"]}\nЦена: {my_food["price"]} ₽', reply_markup=deliv_menu)


@dp.callback_query_handler(text='next')
async def next(call: CallbackQuery, state: FSMContext):
	#print(call)
	food_battons = []
	data = await state.get_data()
	category = data.get("category")
	item = data.get("item") + 1
	bascket = data.get("bascket")

	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)

	if len(categories[category]) - 1 < item:
		item = 0

	for button in category_battons:
		if button == category:
			pass
		else:
			food_battons.append(category_battons[button])

	my_food = categories[category][item]
	await state.update_data(category=category, item=item, bascket=bascket)

	delivery_keyboard = [
	[InlineKeyboardButton(text='⬅️ Назад', callback_data = "back"), InlineKeyboardButton(text='Вперед ➡️', callback_data = "next")],
	[InlineKeyboardButton(text='Добавить', callback_data = "add")],
	[InlineKeyboardButton(text='Категории:', callback_data = "button")],
	food_battons
	]

	if len(bascket['items']) != 0:
		count_of_products = 0
		for count in bascket['items']:
			count_of_products += count['quantity']
		delivery_keyboard.append([InlineKeyboardButton(text=f'Корзина({count_of_products}) 🛒', callback_data = "basket")])

	deliv_menu = InlineKeyboardMarkup(inline_keyboard=delivery_keyboard)

	await bot.send_photo(chat_id=call['from']['id'], photo=my_food['item_id'], caption=f'<b>{my_food["name"]}</b>\n{my_food["description"]}\nЦена: {my_food["price"]} ₽', reply_markup=deliv_menu)

@dp.callback_query_handler(text='back')
async def back(call: CallbackQuery, state: FSMContext):
	food_battons = []
	data = await state.get_data()
	category = data.get("category")
	item = data.get("item") - 1
	bascket = data.get("bascket")

	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)

	if 0 > item:
		item = len(categories[category]) - 1

	for button in category_battons:
		if button == category:
			pass
		else:
			food_battons.append(category_battons[button])

	my_food = categories[category][item]
	await state.update_data(category=category, item=item, bascket=bascket)

	delivery_keyboard = [
	[InlineKeyboardButton(text='⬅️ Назад', callback_data = "back"), InlineKeyboardButton(text='Вперед ➡️', callback_data = "next")],
	[InlineKeyboardButton(text='Добавить', callback_data = "add")],
	[InlineKeyboardButton(text='Категории:', callback_data = "button")],
	food_battons
	]

	if len(bascket['items']) != 0:
		count_of_products = 0
		for count in bascket['items']:
			count_of_products += count['quantity']
		delivery_keyboard.append([InlineKeyboardButton(text=f'Корзина({count_of_products}) 🛒', callback_data = "basket")])

	deliv_menu = InlineKeyboardMarkup(inline_keyboard=delivery_keyboard)

	await bot.send_photo(chat_id=call['from']['id'], photo=my_food['item_id'], caption=f'<b>{my_food["name"]}</b>\n{my_food["description"]}\nЦена: {my_food["price"]} ₽', reply_markup=deliv_menu)

@dp.callback_query_handler(category_callback.filter(dop_prefix="selector"))
async def set_category(call: CallbackQuery, callback_data: dict, state: FSMContext):
	food_battons = []
	my_category = callback_data.get("category")
	data = await state.get_data()
	bascket = data.get("bascket")

	await state.update_data(category=my_category, item=0, bascket=bascket)

	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)

	for button in category_battons:
		if button == my_category:
			pass
		else:
			food_battons.append(category_battons[button])

	my_food = categories[my_category][0]

	delivery_keyboard = [
	[InlineKeyboardButton(text='⬅️ Назад', callback_data = "back"), InlineKeyboardButton(text='Вперед ➡️', callback_data = "next")],
	[InlineKeyboardButton(text='Добавить', callback_data = "add")],
	[InlineKeyboardButton(text='Категории:', callback_data = "button")],
	food_battons
	]

	if len(bascket['items']) != 0:
		count_of_products = 0
		for count in bascket['items']:
			count_of_products += count['quantity']
		delivery_keyboard.append([InlineKeyboardButton(text=f'Корзина({count_of_products}) 🛒', callback_data = "basket")])

	deliv_menu = InlineKeyboardMarkup(inline_keyboard=delivery_keyboard)

	await bot.send_photo(chat_id=call['from']['id'], photo=my_food['item_id'], caption=f'<b>{my_food["name"]}</b>\n{my_food["description"]}\nЦена: {my_food["price"]} ₽', reply_markup=deliv_menu)

@dp.callback_query_handler(text='add')
async def get_add(call: CallbackQuery, state: FSMContext):
	food_battons = []
	data = await state.get_data()
	bascket = data.get("bascket")
	category = data.get("category")
	item = data.get("item")

	new_item = {'category': category, 'item': item, 'quantity': 1}

	item_key = False

	#if new_item in bascket['items']:
	for product in bascket['items']:
		if product['category'] == new_item['category'] and product['item'] == new_item['item']:
			product['quantity'] = product['quantity'] + 1
			bascket['all_price'] = bascket['all_price'] + categories[category][item]['price']
			item_key = True
			print('true')

	if item_key == False:
		bascket['items'].append(new_item)
		bascket['all_price'] = bascket['all_price'] + categories[category][item]['price']

	await state.update_data(category=category, item=item, bascket=bascket)

	for button in category_battons:
		if button == category:
			pass
		else:
			food_battons.append(category_battons[button])

	delivery_keyboard = [
	[InlineKeyboardButton(text='⬅️ Назад', callback_data = "back"), InlineKeyboardButton(text='Вперед ➡️', callback_data = "next")],
	[InlineKeyboardButton(text='Добавить', callback_data = "add")],
	[InlineKeyboardButton(text='Категории:', callback_data = "button")],
	food_battons
	]

	if len(bascket['items']) != 0:
		count_of_products = 0
		for count in bascket['items']:
			count_of_products += count['quantity']
		delivery_keyboard.append([InlineKeyboardButton(text=f'Корзина({count_of_products}) 🛒', callback_data = "basket")])

	deliv_menu = InlineKeyboardMarkup(inline_keyboard=delivery_keyboard)

	await call.message.edit_reply_markup(deliv_menu)

	await call.answer(text="Добавлено")
	print(bascket['items'])
	print(bascket['all_price'])

@dp.callback_query_handler(text='basket')
async def get_basket(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	basket = data.get("bascket")

	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)

	my_keyboard = []
	cheque_message = ''
	item_counter = 0

	for my_item in basket['items']:
		item_price = categories[my_item['category']][my_item['item']]['price'] * my_item['quantity']
		item_name = categories[my_item['category']][my_item['item']]['name']
		cheque_message += f'{item_name} x{my_item["quantity"]} - {item_price} ₽\n'
		item_button = [InlineKeyboardButton(text=f"{item_name} x{my_item['quantity']} - {item_price} ₽", callback_data = "button")]
		my_keyboard.append(item_button)
		tool_buttons = [
		InlineKeyboardButton(text='+', callback_data = f"food:{item_counter}:plus"),
		InlineKeyboardButton(text='-', callback_data = f"food:{item_counter}:minus"),
		InlineKeyboardButton(text='❌', callback_data = f"food:{item_counter}:canc")
		]
		my_keyboard.append(tool_buttons)

		item_counter += 1

	confirm_button = [InlineKeyboardButton(text="Назад", callback_data = "delivery"), InlineKeyboardButton(text="Подтвердить", callback_data = "confirm")]
	my_keyboard.append(confirm_button)

	check_menu = InlineKeyboardMarkup(inline_keyboard=my_keyboard)
	
	cheque_message += f'Итого: {basket["all_price"]}\nИзменить:'	
	await bot.send_message(chat_id=call['from']['id'], text=cheque_message, reply_markup=check_menu)

@dp.callback_query_handler(category_callback.filter(dop_prefix="plus"))
async def get_plus(call: CallbackQuery, callback_data: dict, state: FSMContext):
	basket_item_id = int(callback_data.get("category"))
	data = await state.get_data()
	basket = data.get("bascket")
	category = data.get("category")
	item = data.get("item")

	basket['items'][basket_item_id]['quantity'] = basket['items'][basket_item_id]['quantity'] + 1

	basket['all_price'] = basket['all_price'] + categories[basket['items'][basket_item_id]['category']][basket['items'][basket_item_id]['item']]['price']

	my_keyboard = []
	cheque_message = ''
	item_counter = 0

	for my_item in basket['items']:
		item_price = categories[my_item['category']][my_item['item']]['price'] * my_item['quantity']
		item_name = categories[my_item['category']][my_item['item']]['name']
		cheque_message += f'{item_name} x{my_item["quantity"]} - {item_price} ₽\n'
		item_button = [InlineKeyboardButton(text=f"{item_name} x{my_item['quantity']} - {item_price} ₽", callback_data = "button")]
		my_keyboard.append(item_button)
		tool_buttons = [
		InlineKeyboardButton(text='+', callback_data = f"food:{item_counter}:plus"),
		InlineKeyboardButton(text='-', callback_data = f"food:{item_counter}:minus"),
		InlineKeyboardButton(text='❌', callback_data = f"food:{item_counter}:canc")
		]
		my_keyboard.append(tool_buttons)

		item_counter += 1

	confirm_button = [InlineKeyboardButton(text="Назад", callback_data = "delivery"), InlineKeyboardButton(text="Подтвердить", callback_data = "confirm")]
	my_keyboard.append(confirm_button)

	check_menu = InlineKeyboardMarkup(inline_keyboard=my_keyboard)

	cheque_message += f'Итого: {basket["all_price"]}\nИзменить:'	
	await state.update_data(category=category, item=item, bascket=basket)
	await bot.edit_message_text(chat_id=call['from']['id'], message_id=call.message.message_id, text=cheque_message, reply_markup=check_menu)
	#await call.message.edit_reply_markup(check_menu)
	#await bot.send_message(chat_id=call['from']['id'], text='Чек:', reply_markup=check_menu)

@dp.callback_query_handler(category_callback.filter(dop_prefix="minus"))
async def get_minus(call: CallbackQuery, callback_data: dict, state: FSMContext):
	basket_item_id = int(callback_data.get("category"))
	data = await state.get_data()
	basket = data.get("bascket")
	category = data.get("category")
	item = data.get("item")

	if basket['items'][basket_item_id]['quantity'] == 1:
		basket['all_price'] = basket['all_price'] - categories[basket['items'][basket_item_id]['category']][basket['items'][basket_item_id]['item']]['price']
		basket['items'].pop(basket_item_id)

	else:
		basket['items'][basket_item_id]['quantity'] = basket['items'][basket_item_id]['quantity'] - 1
		basket['all_price'] = basket['all_price'] - categories[basket['items'][basket_item_id]['category']][basket['items'][basket_item_id]['item']]['price']
	

	if len(basket['items']) == 0:
		await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)
		await state.finish()
	else:
		my_keyboard = []
		cheque_message = ''
		item_counter = 0

		for my_item in basket['items']:
			item_price = categories[my_item['category']][my_item['item']]['price'] * my_item['quantity']
			item_name = categories[my_item['category']][my_item['item']]['name']
			cheque_message += f'{item_name} x{my_item["quantity"]} - {item_price} ₽\n'
			item_button = [InlineKeyboardButton(text=f"{item_name} x{my_item['quantity']} - {item_price} ₽", callback_data = "button")]
			my_keyboard.append(item_button)
			tool_buttons = [
			InlineKeyboardButton(text='+', callback_data = f"food:{item_counter}:plus"),
			InlineKeyboardButton(text='-', callback_data = f"food:{item_counter}:minus"),
			InlineKeyboardButton(text='❌', callback_data = f"food:{item_counter}:canc")
			]
			my_keyboard.append(tool_buttons)

			item_counter += 1

		confirm_button = [InlineKeyboardButton(text="Назад", callback_data = "delivery"), InlineKeyboardButton(text="Подтвердить", callback_data = "confirm")]
		my_keyboard.append(confirm_button)

		check_menu = InlineKeyboardMarkup(inline_keyboard=my_keyboard)

		cheque_message += f'Итого: {basket["all_price"]}\nИзменить:'	
		await state.update_data(category=category, item=item, bascket=basket)
		await bot.edit_message_text(chat_id=call['from']['id'], message_id=call.message.message_id, text=cheque_message, reply_markup=check_menu)

@dp.callback_query_handler(category_callback.filter(dop_prefix="canc"))
async def get_cancel(call: CallbackQuery, callback_data: dict, state: FSMContext):
	basket_item_id = int(callback_data.get("category"))
	data = await state.get_data()
	basket = data.get("bascket")
	category = data.get("category")
	item = data.get("item")

	basket['all_price'] = basket['all_price'] - categories[basket['items'][basket_item_id]['category']][basket['items'][basket_item_id]['item']]['price'] * basket['items'][basket_item_id]['quantity']
	basket['items'].pop(basket_item_id)

	if len(basket['items']) == 0:
		await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)
		await state.finish()
	else:
		my_keyboard = []
		cheque_message = ''
		item_counter = 0

		for my_item in basket['items']:
			item_price = categories[my_item['category']][my_item['item']]['price'] * my_item['quantity']
			item_name = categories[my_item['category']][my_item['item']]['name']
			cheque_message += f'{item_name} x{my_item["quantity"]} - {item_price} ₽\n'
			item_button = [InlineKeyboardButton(text=f"{item_name} x{my_item['quantity']} - {item_price} ₽", callback_data = "button")]
			my_keyboard.append(item_button)
			tool_buttons = [
			InlineKeyboardButton(text='+', callback_data = f"food:{item_counter}:plus"),
			InlineKeyboardButton(text='-', callback_data = f"food:{item_counter}:minus"),
			InlineKeyboardButton(text='❌', callback_data = f"food:{item_counter}:canc")
			]
			my_keyboard.append(tool_buttons)

			item_counter += 1

		confirm_button = [InlineKeyboardButton(text="Назад", callback_data = "delivery"), InlineKeyboardButton(text="Подтвердить", callback_data = "confirm")]
		my_keyboard.append(confirm_button)

		check_menu = InlineKeyboardMarkup(inline_keyboard=my_keyboard)

		await state.update_data(category=category, item=item, bascket=basket)
		cheque_message += f'Итого: {basket["all_price"]}\nИзменить:'	
		await bot.edit_message_text(chat_id=call['from']['id'], message_id=call.message.message_id, text=cheque_message, reply_markup=check_menu)

@dp.callback_query_handler(text='confirm')
async def get_pay(call: CallbackQuery, state: FSMContext):
	await call.message.edit_reply_markup()
	data = await state.get_data()
	basket = data.get("bascket")
	PRICES = []

	for label in basket['items']:
		PRICES.append(LabeledPrice(f"{categories[label['category']][label['item']]['name']} ({label['quantity']})", categories[label['category']][label['item']]['price'] * label['quantity'] * 100))

	await bot.send_invoice(chat_id=call['from']['id'], title='Заказ из нашей пиццерии', description='Идет оформление онлайн-заказа...', payload='some-invoice-payload-for-our-internal-use', provider_token='381764678:TEST:22597',
	 currency='rub', prices=PRICES, start_parameter='time-machine-example',
	 need_phone_number=True, need_shipping_address=True,
	 is_flexible=False
	 )
	await state.finish()

@dp.pre_checkout_query_handler(lambda query: True)
async def process_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
	if pre_checkout_query.order_info.shipping_address.country_code == 'RU':
		if pre_checkout_query.order_info.shipping_address.city == 'Москва':
			await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
		else:
			await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=False, error_message='Доставка распространяется только на Москву')
	else:
		await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=False, error_message='Доставка распространяется только по России')

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT) #запуск
async def successful_payment(message: Message):
	my_datetime = datetime.datetime.now()
	yesturday = int(my_datetime.strftime("%d"))

	deliver.insert_one({
		'name': message['from']['first_name'],
		'phone': message.successful_payment.order_info.phone_number,
		'address': message.successful_payment.order_info.shipping_address.street_line1,
		'day': yesturday
		})

	await message.answer('Заказ оплачен!')
	await message.answer('Ваш заказ будет доставлен в течении 45 минут. Ожидайте... 🕔')


@dp.message_handler(Command('book')) #запуск
async def get_booking(message: Message):
	blacklist_user = black.find({'telegram': message.from_user.id}, {'telegram': 1})
	if blacklist_user.count() == 0:
		my_user = users.find({'telegram': message.from_user.id}, {'telegram': 1})
		if my_user.count() == 0:
			await bot.send_message(chat_id=message.from_user.id, text='Вы ещё не авторизованы? 🧐 Отправьте свой номер телефона. Это не займет больше 2 секунд.', reply_markup=phone_keyboard)
		else:
			day = int(datetime.datetime.now().strftime("%m"))
			mounth = mounths[day - 1]#
			days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
			inline_days = []
			day_of_week = int(datetime.datetime.now().strftime("%w"))

			for lol in range(day_of_week):
				a_day = days_of_week.pop(0)
				days_of_week.append(a_day)

			for name_week in days_of_week:
				inline_days.append(InlineKeyboardButton(text = name_week, callback_data = "but"))

			book_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = mounth, callback_data = "button")], inline_days, []], row_width=7)

			free_days = await search_days()

			for a in free_days:
				if a == 0:
					ikb = InlineKeyboardButton(text = ' ', callback_data = "button")
				else:
					ikb = InlineKeyboardButton(text = a, callback_data = f"food:{a}:work_date")
				book_keyboard.insert(ikb)

			
			await message.answer('Выберите день бронирования: ', reply_markup=book_keyboard)

@dp.callback_query_handler(text='book')
async def get_booking_callback(call: CallbackQuery):
	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)
	blacklist_user = black.find({'telegram': call['from']['id']}, {'telegram': 1})
	if blacklist_user.count() == 0:
		my_user = users.find({'telegram': call['from']['id']}, {'telegram': 1})
		if my_user.count() == 0:
			await bot.send_message(chat_id=call['from']['id'], text='Вы ещё не авторизованы? 🧐 Отправьте свой номер телефона. Это не займет больше 2 секунд.', reply_markup=phone_keyboard)
		else:
			day = int(datetime.datetime.now().strftime("%m"))
			mounth = mounths[day - 1]#
			days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
			inline_days = []
			day_of_week = int(datetime.datetime.now().strftime("%w"))

			for lol in range(day_of_week):
				a_day = days_of_week.pop(0)
				days_of_week.append(a_day)

			for name_week in days_of_week:
				inline_days.append(InlineKeyboardButton(text = name_week, callback_data = "but"))

			book_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = mounth, callback_data = "button")], inline_days, []], row_width=7)

			free_days = await search_days()

			for a in free_days:
				if a == 0:
					ikb = InlineKeyboardButton(text = ' ', callback_data = "button")
				else:
					ikb = InlineKeyboardButton(text = a, callback_data = f"food:{a}:work_date")
				book_keyboard.insert(ikb)

			
			await call.message.answer('Выберите день бронирования: ', reply_markup=book_keyboard)

@dp.callback_query_handler(category_callback.filter(dop_prefix="work_date"))
async def get_booking_time(call: CallbackQuery, callback_data: dict, state: FSMContext):
	date = int(callback_data.get("category"))

	free_times = await search_times(date)

	book_keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Назад', callback_data = "book")], []], row_width=4)#[InlineKeyboardButton(text = '⬅️ Назад', callback_data = f"day:{proc}:0:0:0:0:idate")]
	for times in free_times:
		ikb = InlineKeyboardButton(text = str(times) + ':00', callback_data = f"food:{times}:work_hour")
		book_keyboard_2.insert(ikb)

	#book_keyboard_2.append([])

	await state.update_data(date=date, hour=0, table=0)

	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)
	await bot.send_message(chat_id=call['from']['id'], text='Выберите время:', reply_markup=book_keyboard_2)

@dp.callback_query_handler(category_callback.filter(dop_prefix="work_hour"))
async def get_booking_table(call: CallbackQuery, callback_data: dict, state: FSMContext):
	hour = int(callback_data.get("category"))
	data = await state.get_data()
	date = data.get("date")
 
	tables = coll.find({'day': date}, {'table': 1, 'start': 1})
	print(date, hour)

	free_tables = await search_tables(date, hour, tables)

	book_keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Назад', callback_data = f"food:{date}:work_date")], []], row_width=4)
	for table in free_tables:
		ikb = InlineKeyboardButton(text = str(table), callback_data = f"food:{table}:work_table")
		book_keyboard_3.insert(ikb)	

	await state.update_data(date=date, hour=hour, table=0)

	await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)
	await bot.send_photo(chat_id=call['from']['id'], photo=room, caption='Выберите столик', reply_markup=book_keyboard_3)


@dp.callback_query_handler(category_callback.filter(dop_prefix="work_table"))
async def get_confirm_booking(call: CallbackQuery, callback_data: dict, state: FSMContext):
	table = int(callback_data.get("category"))
	data = await state.get_data()
	date = data.get("date")
	hour = data.get("hour")

	#await bot.delete_message(chat_id=call['from']['id'], message_id=call.message.message_id)

	my_datetime = datetime.datetime.now()
	yesturday = int(my_datetime.strftime("%d"))
	mounth = int(my_datetime.strftime("%m"))
	if int(date) < yesturday:
		mounth += 1

	if len(str(mounth)) == 1:
		mounth = '0' + str(mounth)

	confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Назад', callback_data = f"food:{hour}:work_hour")], [InlineKeyboardButton(text = 'Подтвердить', callback_data = f"conf")]])
	await state.update_data(date=date, hour=hour, table=table)

	await bot.edit_message_caption(chat_id=call['from']['id'], message_id=call.message.message_id, caption=f'Бронирование:\nДата бронирования: {date}.{mounth}\nВремя: {str(hour) + ":00"}\nCтолик: №{table}\nВремя с момента начала брони будет активно в течении 2 часов.', reply_markup=confirm_keyboard)


@dp.callback_query_handler(text='conf')
async def send_conf(call: CallbackQuery, state: FSMContext):
	await call.message.edit_reply_markup()

	data = await state.get_data()
	date = data.get("date")
	hour = data.get("hour")
	table = data.get("table")

	await call.answer(text='Бронирование подтверждено', show_alert=True)
	await bot.send_message(chat_id=1187668903, text=f'Бронирование:\nИмя: {call["from"]["first_name"], call["from"]["last_name"]}\nДата бронирования: {date}\nВремя: {str(hour) + ":00"}\nCтолик: №{table}')
	coll.insert_one({
		'name': call["from"]["first_name"],
		'phone': '000',
		'start': hour,
		'finish': hour + 2,
		'day': date,
		'table': table
		})

async def day_checker(wait):
	while True:
		await asyncio.sleep(wait)
		my_datetime = datetime.datetime.now()
		yesturday = int(my_datetime.strftime("%d"))

		if yesturday == 1:
			coll.delete_many({'day': 28})
			coll.delete_many({'day': 29})
			coll.delete_many({'day': 30})
			coll.delete_many({'day': 31})

			deliver.delete_many({'day': 28})
			deliver.delete_many({'day': 29})
			deliver.delete_many({'day': 30})
			deliver.delete_many({'day': 31})

			print('delete_many 1')
		else:
			coll.delete_many({'day': yesturday - 1})

			deliver.delete_many({'day': yesturday - 1})

			print('delete_many -1')


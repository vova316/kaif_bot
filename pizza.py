import asyncio
from aiogram import Bot, Dispatcher , executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot('1265769369:AAHLQMOAuEztBsioqwmtJbjRpby_47JAi2A', parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
#loop = asyncio.get_event_loop()

gumburger_id = 'AgACAgIAAxkBAAIaLGD_C6xh8zx1RLkAAa6zjU15-7cvVgAC7LUxG1dT-EvJJyFIYTdUCgEAAwIAA3MAAyAE'
royal_id = 'AgACAgIAAxkBAAIaLWD_DCchgRhD7blhYgWQgY_sGZmQAALutTEbV1P4S5XKMVwctVOjAQADAgADcwADIAQ'
bigmac_id = 'AgACAgIAAxkBAAIaLmD_DI-FJf6BoUvLXl9vbh70cEsqAALxtTEbV1P4Sw7TNFNnldypAQADAgADcwADIAQ'
big_teasty_id = 'AgACAgIAAxkBAAIaL2D_DOIR8ZP8uA7t-OxOGeYbeeDJAAL6tTEbV1P4S1tmzVBGSKwzAQADAgADcwADIAQ'
panini_id = 'AgACAgIAAxkBAAIaMGD_DS0ru5F3sj5zuQ8I5V_A_H8LAAL7tTEbV1P4Sxy7wHBji4nEAQADAgADcwADIAQ'

fri_id = 'AgACAgIAAxkBAAIaMWD_E0aNcmORe5zm3lHvkrUONka8AAL-tTEbV1P4SyC2l_BJbnB0AQADAgADcwADIAQ'
naggets_id = 'AgACAgIAAxkBAAIaMmD_E5PDPVnpEXspNQ9OpxLW7DObAAIBtjEbV1P4S2kG2FLm34Z5AQADAgADcwADIAQ'
strips_id = 'AgACAgIAAxkBAAIaM2D_E_cIU7-1p55MgnVjRrLo8B1IAAICtjEbV1P4S0RAFh6-7K_sAQADAgADcwADIAQ'
shrimp_id = 'AgACAgIAAxkBAAIaNGD_FFYITcJd5e1tlyAx5ouwBSXGAAIEtjEbV1P4SyJ5e7ZVKtnHAQADAgADcwADIAQ'
cheese_id = 'AgACAgIAAxkBAAIaNWD_FKNzHtrqda7O4yND8JUJ0YhSAAIFtjEbV1P4S-zpPMs6UrCWAQADAgADcwADIAQ' 

cola_id ='AgACAgIAAxkBAAIaN2D_3rTvP98CZj8ynJgFslMS6kcDAAJmtDEbV1MAAUjy8gG5SMQvrgEAAwIAA3MAAyAE'
fanta_id = 'AgACAgIAAxkBAAIaOGD_3wABAjZQvw0LMbS4JC3vl2cunwACZ7QxG1dTAAFI-XCYLZvAl60BAAMCAANzAAMgBA'
sprite_id = 'AgACAgIAAxkBAAIaOWD_3yrY-jMqgIJ-uyV4HPJns6HrAAJotDEbV1MAAUgKVVb6TTicDwEAAwIAA3MAAyAE'
lipton_id = 'AgACAgIAAxkBAAIaOmD_31uhYxZhL-GkCCSqAAHwbNsxMwACarQxG1dTAAFIzqkRfZkccYkBAAMCAANzAAMgBA'
pepsi_id = 'AgACAgIAAxkBAAIaO2D_35djul_UK-xiqFaynWKqEIqpAAJstDEbV1MAAUi3mdD3poMHDwEAAwIAA3MAAyAE'

margarita_id = 'AgACAgIAAxkBAAIaPGD_4FeFymXtOWsf0z-BKcRSsdoFAAJutDEbV1MAAUgMo1rKViaVYgEAAwIAA3MAAyAE'
piperony_id = 'AgACAgIAAxkBAAIaPWD_4JAeZiKTcpSguIunFh-DyIhrAAJvtDEbV1MAAUiDRdPVXzEbYgEAAwIAA3MAAyAE'
hm_id = 'AgACAgIAAxkBAAIaPmD_4MOcoP7F5fxIPfguMjueR6q1AAJytDEbV1MAAUjWihIFPMpYRwEAAwIAA3MAAyAE'
mashrooms_id = 'AgACAgIAAxkBAAIaP2D_4Q4Z1XfGyF2EIMhS3yfPp3W6AAJ0tDEbV1MAAUjn7EVAhRsL0wEAAwIAA3MAAyAE'
meat_id = 'AgACAgIAAxkBAAIaQGD_4WH1fKDphURYFtcrG-rDbOvUAAJ2tDEbV1MAAUg9pRhoUm7dYgEAAwIAA3MAAyAE'

gumburger = {'name': 'Гамбургер', 'description': 'Рубленый бифштекс из 100% говядины, приправленный солью и перцем на гриле, карамелизованная булочка с кетчупом, горчицей, луком и маринованным огурчиком.', 'item_id': gumburger_id, 'price': 50}
royal = {'name': 'Роял', 'description': 'Сочный бифштекс из натуральной говядины, приготовленный на гриле, карамелизованная булочка с кунжутом, два ломтика сыра «Чеддер», кетчуп, горчица, свежий лук и маринованные огурчики.', 'item_id': royal_id, 'price': 150}
bigmac = {'name': 'Биг Мак', 'description': 'Большой бургер с двумя рублеными бифштексами из 100% говядины на булочке с кунжутом, поджаренной в тостере, маринованными огурчиками, луком, свежим салатом «Айсберг», ломтиком плавленого сыра «Чеддер» и специальным соусом «Биг Мак».', 'item_id': bigmac_id, 'price': 150}
big_teasty = {'name': 'Биг Тейсти', 'description': 'Это сандвич с большим, рубленым бифштексом из 100% говядины на большой булочке с кунжутом. Особенный вкус сандвичу придают три кусочка сыра «эмменталь», два ломтика помидора, свежий салат, лук и соус "Биг Тейсти" с дымком.', 'item_id': big_teasty_id, 'price': 250}
panini = {'name': 'Панини Тоскана', 'description': '2 мясных бифштекса из 100% говядины, ароматная лепешка-пита со специями, пряный салат Руккола, помидор, свежий лук, сыр Эмменталь и базиликовый соус', 'item_id': panini_id, 'price': 190}

fri = {'name': 'Картошка фри', 'description': 'Вкусные, обжаренные в растительном фритюре и слегка посоленные палочки картофеля.', 'item_id': fri_id, 'price': 70}
naggets = {'name': 'Наггетсы (9 шт.)', 'description': 'Неподражаемые Чикен Макнаггетс 9 шт.  - это сочное 100% белое куриное мясо в хрустящей панировке со специями. Только натуральная курочка без искусственных красителей и ароматизаторов и без консервантов.', 'item_id': naggets_id, 'price': 100}
strips = {'name': 'Стрипсы (7 шт.)', 'description': 'Стрипсы 7 шт. – сочная, нежная курица в хрустящей панировке. Попробуйте новые стрипсы от Макдоналдс из 100% белого мяса!', 'item_id': strips_id, 'price': 190}
cheese = {'name': 'Сырные палочки (3 шт.)', 'description': 'Вкуснейшие сырные палочки, обжаренные в хрустящей панировке. Сочетание сыров Моцарелла, Гауда, Чеддер и Пармезан', 'item_id': cheese_id, 'price': 100}
shrimp = {'name': 'Креветки (9 шт.)', 'description': 'Жареные тигровые креветки в хрустящей панировке. Легко. Изысканно. Вкусно', 'item_id': shrimp_id, 'price': 325}

cola = {'name': 'Кока-Кола', 'description': 'Прохладительный газированный напиток «Кока-Кола»®.', 'item_id': cola_id, 'price': 80}
pepsi = {'name': 'Пэпси', 'description': 'Прохладительный газированный напиток «Pepsi»®.', 'item_id': pepsi_id, 'price': 80}
fanta = {'name': 'Фанта', 'description': 'Прохладительный газированный напиток Фанта®.', 'item_id': fanta_id, 'price': 80}
sprite = {'name': 'Спрайт', 'description': 'Прохладительный газированный напиток Спрайт®.', 'item_id': sprite_id, 'price': 80}
lipton = {'name': 'Чай Липтон', 'description': 'Прохладительный напиток.', 'item_id': lipton_id, 'price': 80}

margarita = {'name': 'Пицца Маргарита', 'description': 'тесто, соус «Томатный», сыр «Моцарелла», томаты, базилик', 'item_id': margarita_id, 'price': 435}
piperony = {'name': 'Пицца Пепперони', 'description': 'тесто, соус «Томатный», сыр «Моцарелла», колбаса «Пепперони»', 'item_id': piperony_id, 'price': 435}
hm = {'name': 'Ветчина-Грибы', 'description': 'Тесто, соус томатный, ветчина, шампиньоны, перец болгарский, сыр "Моцарелла", соус сметанный', 'item_id': hm_id, 'price': 500}
mashrooms = {'name': 'Пицца Грибная', 'description': 'Тесто, сыр "Моцарелла", шампиньоны, соус "Ранч", соус сметанный', 'item_id': mashrooms_id, 'price': 500}
meat = {'name': 'Пицца Мясной пир', 'description': 'Тесто, соус томатный, соус сметанный, колбаса "Пепперони", карбонад, ветчина, томаты, бекон, колбаски "Охотничьи", сыр "Моцарелла"', 'item_id': meat_id, 'price': 560}

categories = {'pizza': [margarita, piperony, hm, mashrooms, meat], 'burgers': [gumburger, royal, bigmac, big_teasty, panini], 'snacks': [fri, naggets, strips, cheese, shrimp], 'drinks': [cola, pepsi, fanta, sprite, lipton]}

if __name__ == '__main__':
	from pizza_bot import dp
	from pizza_bot import day_checker
	dp.loop.create_task(day_checker(86400))
	executor.start_polling(dp)#, loop=loop 
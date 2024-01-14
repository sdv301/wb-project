import tkinter
import requests
import csv
import re
from models import Items, Feedback
import customtkinter
import threading
from loguru import logger

__version__ = 1.00


class ParseWB:
    def __init__(self, url: str):
        self.seller_id = self.__get_seller_id(url)

    @staticmethod
    def __get_item_id(url: str):
        regex = "(?<=catalog/).+(?=/detail)"
        item_id = re.search(regex, url)[0]
        return item_id

    def __get_seller_id(self, url):
        response = requests.get(url=f"https://card.wb.ru/cards/detail?nm={self.__get_item_id(url=url)}")
        seller_id = Items.model_validate(response.json()["data"])
        return seller_id.products[0].supplierId

    def parse(self):
        _page = 1
        self.__create_csv()
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/sellers/catalog?dest=-1257786&supplier={self.seller_id}&page={_page}',
            )
            _page += 1
            items_info = Items.model_validate(response.json()["data"])
            if not items_info.products:
                break
            self.__get_images(items_info)
            self.__feedback(items_info)
            self.__save_csv(items_info)

    @staticmethod
    def __create_csv():
        with open("wb_data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ['id', 'название', 'цена', 'бренд', 'скидка', 'рейтинг', 'в наличии', 'id продавца', 'изображения',
                 "отзывы с текстом", "рейтинг"])

    @staticmethod
    def __save_csv(items: Items):
        with open("wb_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id,
                                 product.name,
                                 product.salePriceU,
                                 product.brand,
                                 product.sale,
                                 product.rating,
                                 product.volume,
                                 product.supplierId,
                                 product.image_links,
                                 product.feedback_count,
                                 product.valuation
                                 ])

    @staticmethod
    def __get_images(item_model: Items):
        for product in item_model.products:
            _short_id = product.id // 100000
            """Используем match/case для определения basket на основе _short_id"""
            if 0 <= _short_id <= 143:
                basket = '01'
            elif 144 <= _short_id <= 287:
                basket = '02'
            elif 288 <= _short_id <= 431:
                basket = '03'
            elif 432 <= _short_id <= 719:
                basket = '04'
            elif 720 <= _short_id <= 1007:
                basket = '05'
            elif 1008 <= _short_id <= 1061:
                basket = '06'
            elif 1062 <= _short_id <= 1115:
                basket = '07'
            elif 1116 <= _short_id <= 1169:
                basket = '08'
            elif 1170 <= _short_id <= 1313:
                basket = '09'
            elif 1314 <= _short_id <= 1601:
                basket = '10'
            elif 1602 <= _short_id <= 1655:
                basket = '11'
            elif 1656 <= _short_id <= 1919:
                basket = '12'
            else:
                basket = '13'

            """Делаем список всех ссылок на изображения и переводим в строку"""
            link_str = "".join([
                f"  https://basket-{basket}.wb.ru/vol{_short_id}/part{product.id // 1000}/{product.id}/images/big/{i}.jpg;  "
                for i in range(1, product.pics + 1)])
            product.image_links = link_str
            link_str = ''

    @staticmethod
    def __feedback(item_model: Items):
        for product in item_model.products:
            url = f"https://feedbacks1.wb.ru/feedbacks/v1/{product.root}"
            res = requests.get(url=url)
            if res.status_code == 200:
                feedback = Feedback.model_validate(res.json())
                product.feedback_count = feedback.feedbackCountWithText
                product.valuation = feedback.valuation


if __name__ == "__main__":
    ParseWB("https://www.wildberries.ru/catalog/141217830/detail.aspx").parse()


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class app(customtkinter.CTk):
    def __init__(app):
        super().__init__()
        app.geometry("680x590")
        app.width_entry_field = 500
        app.resizable(width=True, height=True)
        app.title(f"Parser Wildberries v. {__version__}")
        app.is_run = False
        app.main_windows_init()
        app.logger_widget_init()

        #Центрируем окно относительно экрана"""
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        window_width = app.winfo_width()
        window_height = app.winfo_height()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        app.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    def main_windows_init(app):
        #Инициализация всех полей"""
        app.token_label = customtkinter.CTkLabel(app, text="id")
        app.token_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        app.token_entry = customtkinter.CTkEntry(app, width=app.width_entry_field, placeholder_text="Введите id вашего Товара")
        app.token_entry.grid(row=0, column=1, pady=5, sticky='w')

        app.token_label = customtkinter.CTkLabel(app, text="Название:")
        app.token_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        app.token_entry = customtkinter.CTkEntry(app, width=app.width_entry_field, placeholder_text="Введите Название вашего Товара")
        app.token_entry.grid(row=1, column=1, pady=5, sticky='w')

        app.token_label = customtkinter.CTkLabel(app, text="Цена:")
        app.token_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        app.token_entry = customtkinter.CTkEntry(app, width=app.width_entry_field, placeholder_text="Введите Цену вашего Товара")
        app.token_entry.grid(row=2, column=1, pady=5, sticky='w')

        app.token_label = customtkinter.CTkLabel(app, text="Рейтинг:")
        app.token_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        app.token_entry = customtkinter.CTkEntry(app, width=app.width_entry_field, placeholder_text="Введите Рейтинг вашего Товара")
        app.token_entry.grid(row=3, column=1, pady=5, sticky='w')

        app.url_label = customtkinter.CTkLabel(app, text="Url:")
        app.url_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        app.url_entry = customtkinter.CTkEntry(app, width=app.width_entry_field, placeholder_text="Ссылка с которой нужно начинать")
        app.url_entry.grid(row=5, column=1, pady=5, sticky='w')

        app.clear_button = customtkinter.CTkButton(app, text="X", width=1, command=lambda: app.url_entry.delete(0, 1000))
        app.clear_button.grid(row=5, column=3)
        # кнопка "Старт"
        app.start_btn()


    def start_scraping(app):
        """Кнопка старт. Запуск"""
        """Если URL все-таки не заполнен"""
        url = app.url_entry.get()
        if not url:
            logger.info("Внимание! URL - обязательный параметр. Пример ссылки:")
            logger.info("https://www.wildberries.ru/catalog/152404224/detail.aspx")
            return
        """Прячем кнопку старт"""
        app.is_run = True
        app.start_button.configure(text='Работает', state='disabled')
        app.start_button.destroy()
        logger.info("Начинаем поиск")

        """Размещаем кнопку Стоп"""
        app.stop_button = customtkinter.CTkButton(app, text="Стоп", command=app.stop_scraping)
        app.stop_button.grid(row=9, column=0, padx=5, pady=5, sticky="ew")

        """Основной цикл"""
        while app.is_run:
            app.run_parse()
            if not app.is_run: break
            logger.info("Проверка завершена")


        """Убираем кнопку Стоп и создаем старт"""
        logger.info("Успешно остановлено")
        app.stop_button.destroy()
        app.start_btn()

    def start_btn(app):
        #Кнопка старт. Старт работы
        app.start_button = customtkinter.CTkButton(app, text="Старт", command=lambda: app.is_run or threading.Thread(target=app.start_scraping).start())
        app.start_button.grid(row=9, column=1, pady=5, padx=(0, 6), sticky="ew")

    def stop_scraping(app):
        #Кнопка стоп. Остановка работы"""
        logger.info("Идет остановка. Пожалуйста, подождите")
        app.is_run = False
        app.stop_button.configure(text='Останавливаюсь', state='disabled')

    def logger_widget_init(app):
        #Инициализация логирования в widget
        app.log_widget = customtkinter.CTkTextbox(app, wrap="word", width=650, height=300, text_color="#00ff26")
        app.log_widget.grid(row=10, padx=5, pady=(10, 0), column=0, columnspan=2)
        logger.add(app.logger_text_widget, format="{time:HH:mm:ss} - {message}")
        logger.info("Запуск Parser Валберис")
        logger.info("Чтобы начать работу, проверьте, чтобы поле URL было заполненными,""остальное на Ваше усмотрение.")
        logger.info("Удачного поиска !!!")

    def logger_text_widget(app, message):
        #Логирование в log_widget (окно приложения)"""
        app.log_widget.insert(tkinter.END, message)
        app.log_widget.see(tkinter.END)

    def run_parse(app):
        user_url = app.url_entry.get()

        # Создаем экземпляр парсера и запускаем парсинг
        parser = ParseWB(user_url)
        parser.parse()

if __name__ == '__main__':
    app().mainloop()

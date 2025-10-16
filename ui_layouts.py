from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.core.window import Window
from datetime import datetime
from ui_controls import create_button, create_label, create_input_field, ProductItem, SuggestionItem

# Устанавливаем минимальный размер для мобильных устройств
Window.minimum_width = dp(300)
Window.minimum_height = dp(500)


class CenteredBoxLayout(BoxLayout):
    """Центрированный layout для экранов авторизации"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(20)]
        self.spacing = dp(20)
        self.size_hint = (0.9, 0.8)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}


class MainLayout(ScreenManager):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        # Начинаем с экрана авторизации
        self.add_widget(LoginScreen(name='login', logic=logic))
        self.add_widget(RegisterScreen(name='register', logic=logic))
        self.add_widget(MainScreen(name='main', logic=logic))
        self.add_widget(CreateListScreen(name='create_list', logic=logic))
        self.add_widget(JoinListScreen(name='join_list', logic=logic))
        self.add_widget(ListInfoScreen(name='list_info', logic=logic))
        self.add_widget(AddItemScreen(name='add_item', logic=logic))
        self.add_widget(HistoryScreen(name='history', logic=logic))
        self.add_widget(SuggestionsScreen(name='suggestions', logic=logic))


class LoginScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        # Главный контейнер с центрированием
        main_layout = BoxLayout(orientation='vertical', padding=dp(20))

        # Пустое пространство сверху для центрирования
        main_layout.add_widget(BoxLayout(size_hint_y=0.2))

        # Центрированный контейнер для формы
        center_layout = CenteredBoxLayout()

        center_layout.add_widget(create_label("ВХОД В СИСТЕМУ", dp(32), (1, 1, 1, 1)))

        # Поле логина
        self.username_input = create_input_field("Имя пользователя")
        self.username_input.size_hint_y = None
        self.username_input.height = dp(60)
        center_layout.add_widget(self.username_input)

        # Поле пароля
        self.password_input = TextInput(
            hint_text="Пароль",
            size_hint_y=None,
            height=dp(60),
            multiline=False,
            password=True,
            font_size=dp(18),
            padding=[dp(15), dp(15)]
        )
        center_layout.add_widget(self.password_input)

        # Кнопка входа
        login_btn = create_button("ВОЙТИ", (0.2, 0.6, 0.8, 1), dp(60))
        login_btn.bind(on_press=self.login)
        center_layout.add_widget(login_btn)

        # Кнопка регистрации
        register_btn = create_button("РЕГИСТРАЦИЯ", (0.4, 0.4, 0.4, 1), dp(50))
        register_btn.bind(on_press=self.goto_register)
        center_layout.add_widget(register_btn)

        self.message = create_label("", dp(16), (1, 1, 1, 1))
        center_layout.add_widget(self.message)

        main_layout.add_widget(center_layout)

        # Пустое пространство снизу
        main_layout.add_widget(BoxLayout(size_hint_y=0.2))

        self.add_widget(main_layout)

    def on_enter(self):
        """Очищаем поля при входе на экран"""
        self.username_input.text = ""
        self.password_input.text = ""
        self.message.text = ""

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username and password:
            if self.logic.login_user(username, password):
                self.message.text = "Успешный вход!"
                # Обновляем главный экран
                main_screen = self.manager.get_screen('main')
                main_screen.update_user_info()
                main_screen.load_user_lists()
                self.manager.current = 'main'
            else:
                self.message.text = "Неверные данные"
        else:
            self.message.text = "Заполните все поля"

    def goto_register(self, instance):
        self.manager.current = 'register'


class RegisterScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        # Главный контейнер с центрированием
        main_layout = BoxLayout(orientation='vertical', padding=dp(20))

        # Пустое пространство сверху для центрирования
        main_layout.add_widget(BoxLayout(size_hint_y=0.1))

        # Центрированный контейнер для формы
        center_layout = CenteredBoxLayout()

        center_layout.add_widget(create_label("РЕГИСТРАЦИЯ", dp(32), (1, 1, 1, 1)))

        # Поле логина
        self.username_input = create_input_field("Имя пользователя")
        self.username_input.size_hint_y = None
        self.username_input.height = dp(60)
        center_layout.add_widget(self.username_input)

        # Поле пароля
        self.password_input = TextInput(
            hint_text="Пароль",
            size_hint_y=None,
            height=dp(60),
            multiline=False,
            password=True,
            font_size=dp(18),
            padding=[dp(15), dp(15)]
        )
        center_layout.add_widget(self.password_input)

        # Подтверждение пароля
        self.confirm_input = TextInput(
            hint_text="Подтвердите пароль",
            size_hint_y=None,
            height=dp(60),
            multiline=False,
            password=True,
            font_size=dp(18),
            padding=[dp(15), dp(15)]
        )
        center_layout.add_widget(self.confirm_input)

        # Кнопка регистрации
        register_btn = create_button("ЗАРЕГИСТРИРОВАТЬСЯ", (0.2, 0.8, 0.4, 1), dp(60))
        register_btn.bind(on_press=self.register)
        center_layout.add_widget(register_btn)

        # Кнопка назад
        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), dp(50))
        back_btn.bind(on_press=self.goto_login)
        center_layout.add_widget(back_btn)

        self.message = create_label("", dp(16), (1, 1, 1, 1))
        center_layout.add_widget(self.message)

        main_layout.add_widget(center_layout)

        # Пустое пространство снизу
        main_layout.add_widget(BoxLayout(size_hint_y=0.1))

        self.add_widget(main_layout)

    def on_enter(self):
        """Очищаем поля при входе на экран"""
        self.username_input.text = ""
        self.password_input.text = ""
        self.confirm_input.text = ""
        self.message.text = ""

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_input.text.strip()

        if not username or not password:
            self.message.text = "Заполните все поля"
            return

        if password != confirm:
            self.message.text = "Пароли не совпадают"
            return

        if len(password) < 4:
            self.message.text = "Пароль должен быть не менее 4 символов"
            return

        if self.logic.register_user(username, password):
            self.message.text = "Регистрация успешна! Теперь войдите в систему"
            self.manager.current = 'login'
        else:
            self.message.text = "Пользователь уже существует"

    def goto_login(self, instance):
        self.manager.current = 'login'


class MainScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # Заголовок с информацией о пользователе
        self.user_info = Label(
            text=f"СОВМЕСТНЫЕ СПИСКИ\nПользователь: {self.logic.get_current_username()}",
            font_size=dp(20),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(80),
            halign='center',
            text_size=(None, None)
        )
        layout.add_widget(self.user_info)

        # Информация о текущем списке
        self.list_info = Label(
            text="Выберите список покупок",
            font_size=dp(16),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        layout.add_widget(self.list_info)

        # Кнопка выхода
        logout_btn = create_button("ВЫЙТИ", (0.8, 0.3, 0.3, 1), height=dp(50))
        logout_btn.bind(on_press=self.logout)
        layout.add_widget(logout_btn)

        # Панель управления списками
        list_management = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))

        create_list_btn = Button(
            text="СОЗДАТЬ",
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14)
        )
        create_list_btn.bind(on_press=self.goto_create_list)
        list_management.add_widget(create_list_btn)

        join_list_btn = Button(
            text="ПРИСОЕДИНИТЬСЯ",
            background_color=(0.2, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14)
        )
        join_list_btn.bind(on_press=self.goto_join_list)
        list_management.add_widget(join_list_btn)

        leave_list_btn = Button(
            text="ПОКИНУТЬ",
            background_color=(0.8, 0.4, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14)
        )
        leave_list_btn.bind(on_press=self.leave_current_list)
        list_management.add_widget(leave_list_btn)

        layout.add_widget(list_management)

        # Выбор списка
        layout.add_widget(Label(
            text="Ваши списки:",
            font_size=dp(16),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(30)
        ))

        # Область прокрутки списков
        scroll_lists = ScrollView(size_hint_y=0.3)
        self.lists_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.lists_layout.bind(minimum_height=self.lists_layout.setter('height'))
        scroll_lists.add_widget(self.lists_layout)
        layout.add_widget(scroll_lists)

        # Прокручиваемая область для списка товаров
        scroll = ScrollView()
        self.list_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        layout.add_widget(scroll)

        # Кнопки управления
        buttons = [
            ("ДОБАВИТЬ ТОВАР", self.goto_add, (0, 0.6, 0, 1)),
            ("ОЧИСТИТЬ СПИСОК", self.clear_list, (0.8, 0.2, 0, 1)),
            ("ИСТОРИЯ ПОКУПОК", self.goto_history, (0.2, 0.4, 0.8, 1)),
            ("УМНЫЕ ПРЕДЛОЖЕНИЯ", self.goto_suggestions, (1, 0.5, 0, 1)),
        ]

        for text, callback, color in buttons:
            btn = create_button(text, color, height=dp(50))
            btn.bind(on_press=callback)
            layout.add_widget(btn)

        self.add_widget(layout)
        self.update_display()

    def update_user_info(self):
        """Обновляет информацию о пользователе"""
        self.user_info.text = f"СОВМЕСТНЫЕ СПИСКИ\nПользователь: {self.logic.get_current_username()}"

    def load_user_lists(self):
        """Загружает списки пользователя"""
        self.lists_layout.clear_widgets()
        lists = self.logic.get_user_lists()

        if not lists:
            empty_label = Label(
                text="У вас пока нет списков\nСоздайте новый или присоединитесь",
                font_size=dp(14),
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height=dp(80)
            )
            self.lists_layout.add_widget(empty_label)
            return

        for list_data in lists:
            list_id, list_name, owner_id, owner_name, share_code = list_data
            is_owner = owner_id == self.logic.db.get_current_user_id()

            list_item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), spacing=dp(5))

            # Кнопка выбора списка
            owner_indicator = "(Владелец)" if is_owner else ""
            list_btn = Button(
                text=f"{list_name}\nВладелец: {owner_name} {owner_indicator}",
                size_hint_x=0.55,
                background_color=(0.3, 0.5, 0.7, 1) if is_owner else (0.4, 0.4, 0.6, 1),
                color=(1, 1, 1, 1),
                font_size=dp(12)
            )
            list_btn.bind(on_press=lambda instance, lid=list_id: self.select_list(lid))

            # Кнопка информации о списке
            info_btn = Button(
                text="ИНФО",
                size_hint_x=0.2,
                background_color=(0.3, 0.5, 0.8, 1),
                font_size=dp(14)
            )
            info_btn.bind(on_press=lambda instance, lid=list_id: self.show_list_info(lid))

            # Кнопка удаления списка (только для владельца)
            delete_btn = Button(
                text="УДАЛИТЬ",
                size_hint_x=0.25,
                background_color=(0.8, 0.2, 0.2, 1),
                font_size=dp(14)
            )
            delete_btn.bind(on_press=lambda instance, lid=list_id, lname=list_name: self.delete_list(lid, lname))
            delete_btn.disabled = not is_owner

            list_item_layout.add_widget(list_btn)
            list_item_layout.add_widget(info_btn)
            list_item_layout.add_widget(delete_btn)

            self.lists_layout.add_widget(list_item_layout)

    def select_list(self, list_id):
        """Выбирает список для работы"""
        self.logic.set_current_list(list_id)
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info
            members = self.logic.get_list_members()
            self.list_info.text = f"{list_name} (Участников: {len(members)})"
            self.update_display()

    def show_list_info(self, list_id):
        """Показывает информацию о списке"""
        self.logic.set_current_list(list_id)
        list_info_screen = self.manager.get_screen('list_info')
        list_info_screen.update_info()
        self.manager.current = 'list_info'

    def delete_list(self, list_id, list_name):
        """Удаляет список"""

        def confirm_delete(instance):
            result = self.logic.delete_shopping_list(list_id)
            print(result)
            self.load_user_lists()
            if self.logic.current_list_id == list_id:
                self.logic.current_list_id = None
                self.list_info.text = "Выберите список покупок"
                self.update_display()
            popup.dismiss()

        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(
            text=f'Удалить список\n"{list_name}"?\n\nЭто действие нельзя отменить!',
            font_size=dp(18),
            color=(1, 1, 1, 1),
            halign='center'
        ))

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))

        yes_btn = Button(
            text='УДАЛИТЬ',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=dp(16)
        )
        no_btn = Button(
            text='ОТМЕНА',
            background_color=(0.4, 0.4, 0.4, 1),
            font_size=dp(16)
        )

        yes_btn.bind(on_press=confirm_delete)
        no_btn.bind(on_press=lambda x: popup.dismiss())

        buttons_layout.add_widget(yes_btn)
        buttons_layout.add_widget(no_btn)
        content.add_widget(buttons_layout)

        popup = Popup(
            title='Удаление списка',
            content=content,
            size_hint=(0.8, 0.4),
            separator_height=dp(1)
        )
        popup.open()

    def leave_current_list(self, instance):
        """Покидает текущий список"""
        if self.logic.current_list_id:
            result = self.logic.leave_current_list()
            print(result)
            self.list_info.text = "Выберите список покупок"
            self.load_user_lists()
            self.update_display()

    def logout(self, instance):
        self.logic.logout_user()
        self.manager.current = 'login'

    def update_display(self):
        self.list_layout.clear_widgets()

        if not self.logic.current_list_id:
            empty_label = Label(
                text="Выберите список покупок\n\nСоздайте новый список или выберите существующий",
                font_size=dp(18),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(120),
                halign='center'
            )
            self.list_layout.add_widget(empty_label)
            return

        products = self.logic.get_current_list()
        if not products:
            empty_label = Label(
                text="Список покупок пустой\n\nДобавьте товары через кнопку ниже",
                font_size=dp(18),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(120),
                halign='center'
            )
            self.list_layout.add_widget(empty_label)
            return

        for product_data in products:
            if len(product_data) >= 4:
                product_id, product_name, category, order = product_data[:4]
                created_by = product_data[4] if len(product_data) > 4 else None
                bought_by = product_data[5] if len(product_data) > 5 else None
            else:
                product_id, product_name = product_data
                category = 'Другое'
                created_by = bought_by = None

            item = ProductItem(product_id, product_name, category, self.logic, self, created_by, bought_by)
            self.list_layout.add_widget(item)

    def goto_create_list(self, instance):
        self.manager.current = 'create_list'

    def goto_join_list(self, instance):
        self.manager.current = 'join_list'

    def goto_add(self, instance):
        if self.logic.current_list_id:
            self.manager.current = 'add_item'
        else:
            print("Сначала выберите список")

    def clear_list(self, instance):
        if self.logic.current_list_id:
            result = self.logic.clear_all_items()
            print(result)
            self.update_display()
        else:
            print("Сначала выберите список")

    def goto_history(self, instance):
        if self.logic.current_list_id:
            history_screen = self.manager.get_screen('history')
            history_screen.update_display()
            self.manager.current = 'history'
        else:
            print("Сначала выберите список")

    def goto_suggestions(self, instance):
        if self.logic.current_list_id:
            suggestions_screen = self.manager.get_screen('suggestions')
            suggestions_screen.update_display()
            self.manager.current = 'suggestions'
        else:
            print("Сначала выберите список")


class CreateListScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        main_layout = BoxLayout(orientation='vertical', padding=dp(20))
        main_layout.add_widget(BoxLayout(size_hint_y=0.2))

        center_layout = CenteredBoxLayout()
        center_layout.add_widget(create_label("СОЗДАТЬ СПИСОК", dp(24), (1, 1, 1, 1)))

        # Поле ввода названия
        self.list_name_input = create_input_field("Название списка")
        self.list_name_input.size_hint_y = None
        self.list_name_input.height = dp(60)
        center_layout.add_widget(self.list_name_input)

        # Кнопка создания
        create_btn = create_button("СОЗДАТЬ", (0, 0.8, 0, 1), dp(60))
        create_btn.bind(on_press=self.create_list)
        center_layout.add_widget(create_btn)

        self.message = create_label("", dp(16), (1, 1, 1, 1))
        center_layout.add_widget(self.message)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), dp(50))
        back_btn.bind(on_press=self.go_back)
        center_layout.add_widget(back_btn)

        main_layout.add_widget(center_layout)
        main_layout.add_widget(BoxLayout(size_hint_y=0.2))

        self.add_widget(main_layout)

    def on_enter(self):
        """Очищаем поля при входе на экран"""
        self.list_name_input.text = ""
        self.message.text = ""

    def create_list(self, instance):
        list_name = self.list_name_input.text.strip()

        if list_name:
            list_id, result = self.logic.create_shared_list(list_name)
            self.message.text = result
            if list_id:
                list_info = self.logic.get_current_list_info()
                if list_info:
                    share_code = list_info[4]
                    self.show_share_code(share_code)
                self.list_name_input.text = ""
                main_screen = self.manager.get_screen('main')
                main_screen.load_user_lists()
                main_screen.select_list(list_id)
        else:
            self.message.text = "Введите название списка!"

    def show_share_code(self, share_code):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.add_widget(Label(
            text='Список создан!\nКод для присоединения:',
            font_size=dp(18),
            color=(1, 1, 1, 1),
            halign='center'
        ))

        code_label = Label(
            text=f'{share_code}',
            font_size=dp(32),
            color=(0, 1, 0, 1),
            halign='center'
        )
        content.add_widget(code_label)

        content.add_widget(Label(
            text='Поделитесь этим кодом с друзьями',
            font_size=dp(14),
            color=(0.8, 0.8, 0.8, 1),
            halign='center'
        ))

        copy_btn = Button(
            text='КОПИРОВАТЬ',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=dp(16)
        )

        ok_btn = Button(
            text='ЗАКРЫТЬ',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.4, 0.4, 0.4, 1),
            font_size=dp(16)
        )

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        buttons_layout.add_widget(copy_btn)
        buttons_layout.add_widget(ok_btn)
        content.add_widget(buttons_layout)

        popup = Popup(
            title='Код для присоединения',
            content=content,
            size_hint=(0.8, 0.5)
        )

        def copy_code(instance):
            Clipboard.copy(share_code)

        copy_btn.bind(on_press=copy_code)
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'


class JoinListScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        main_layout = BoxLayout(orientation='vertical', padding=dp(20))
        main_layout.add_widget(BoxLayout(size_hint_y=0.2))

        center_layout = CenteredBoxLayout()
        center_layout.add_widget(create_label("ПРИСОЕДИНИТЬСЯ", dp(24), (1, 1, 1, 1)))

        self.code_input = create_input_field("Код списка (8 символов)")
        self.code_input.size_hint_y = None
        self.code_input.height = dp(60)
        center_layout.add_widget(self.code_input)

        join_btn = create_button("ПРИСОЕДИНИТЬСЯ", (0.2, 0.4, 0.8, 1), dp(60))
        join_btn.bind(on_press=self.join_list)
        center_layout.add_widget(join_btn)

        self.message = create_label("", dp(16), (1, 1, 1, 1))
        center_layout.add_widget(self.message)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), dp(50))
        back_btn.bind(on_press=self.go_back)
        center_layout.add_widget(back_btn)

        main_layout.add_widget(center_layout)
        main_layout.add_widget(BoxLayout(size_hint_y=0.2))

        self.add_widget(main_layout)

    def on_enter(self):
        self.code_input.text = ""
        self.message.text = ""

    def join_list(self, instance):
        share_code = self.code_input.text.strip()
        if share_code:
            result = self.logic.join_shared_list(share_code)
            self.message.text = result
            if "Успех" in result:
                self.code_input.text = ""
                main_screen = self.manager.get_screen('main')
                main_screen.load_user_lists()
                self.manager.current = 'main'
        else:
            self.message.text = "Введите код списка!"

    def go_back(self, instance):
        self.manager.current = 'main'


class ListInfoScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout.add_widget(create_label("ИНФОРМАЦИЯ О СПИСКЕ", dp(24), (1, 1, 1, 1)))

        self.list_info_label = Label(
            text="",
            font_size=dp(16),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(100),
            text_size=(dp(350), None),
            halign='center'
        )
        layout.add_widget(self.list_info_label)

        # Кнопка для показа кода
        self.code_btn = create_button("ПОКАЗАТЬ И СКОПИРОВАТЬ КОД", (0.3, 0.5, 0.8, 1), height=dp(50))
        self.code_btn.bind(on_press=self.show_code)
        layout.add_widget(self.code_btn)

        # Участники списка
        layout.add_widget(create_label("Участники:", dp(16), (1, 1, 1, 1)))

        scroll_members = ScrollView(size_hint_y=0.4)
        self.members_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.members_layout.bind(minimum_height=self.members_layout.setter('height'))
        scroll_members.add_widget(self.members_layout)
        layout.add_widget(scroll_members)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), height=dp(50))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_info(self):
        """Обновляет информацию при входе на экран"""
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info
            current_user_id = self.logic.db.get_current_user_id()

            info_text = f"{list_name}\n"
            info_text += f"Владелец: {owner_name}\n"
            info_text += f"Код: {share_code}" if owner_id == current_user_id else "Код: доступен владельцу"

            self.list_info_label.text = info_text

            # Показываем/скрываем кнопку кода в зависимости от прав
            self.code_btn.disabled = (owner_id != current_user_id)

            # Показываем участников
            self.members_layout.clear_widgets()
            members = self.logic.get_list_members()
            for member in members:
                is_owner = (member == owner_name)
                member_text = f"{member} (владелец)" if is_owner else f"{member}"
                member_label = Label(
                    text=member_text,
                    size_hint_y=None,
                    height=dp(30),
                    color=(1, 1, 1, 1),
                    font_size=dp(14)
                )
                self.members_layout.add_widget(member_label)

    def show_code(self, instance):
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info

            content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

            content.add_widget(Label(
                text=f'Код для присоединения к списку\n"{list_name}":',
                font_size=dp(18),
                color=(1, 1, 1, 1),
                halign='center'
            ))

            code_label = Label(
                text=f'{share_code}',
                font_size=dp(32),
                color=(0, 1, 0, 1),
                halign='center'
            )
            content.add_widget(code_label)

            content.add_widget(Label(
                text='\nПоделитесь этим кодом с друзьями',
                font_size=dp(14),
                color=(0.8, 0.8, 0.8, 1),
                halign='center'
            ))

            # Кнопка копирования
            copy_btn = Button(
                text='КОПИРОВАТЬ КОД',
                size_hint_y=None,
                height=dp(50),
                background_color=(0.2, 0.6, 0.8, 1)
            )

            # Кнопка закрытия
            ok_btn = Button(
                text='ЗАКРЫТЬ',
                size_hint_y=None,
                height=dp(50),
                background_color=(0.4, 0.4, 0.4, 1)
            )

            buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
            buttons_layout.add_widget(copy_btn)
            buttons_layout.add_widget(ok_btn)
            content.add_widget(buttons_layout)

            popup = Popup(
                title='Код для присоединения',
                content=content,
                size_hint=(0.8, 0.5)
            )

            def copy_code(instance):
                Clipboard.copy(share_code)
                self.show_success_message("Код скопирован в буфер обмена!")

            copy_btn.bind(on_press=copy_code)
            ok_btn.bind(on_press=popup.dismiss)

            popup.open()

    def show_success_message(self, message):
        """Показывает сообщение об успешном копировании"""
        popup = Popup(
            title='Успех',
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'


class AddItemScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout.add_widget(create_label("ДОБАВИТЬ ТОВАР", dp(24), (1, 1, 1, 1)))

        # Информация о текущем списке
        self.current_list_info = Label(
            text="",
            font_size=dp(14),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.current_list_info)

        # Кнопка повтора последнего товара
        self.repeat_btn = create_button("Повторить последний товар", (0.5, 0.3, 0.8, 1), height=dp(50))
        self.repeat_btn.bind(on_press=self.repeat_last_product)
        layout.add_widget(self.repeat_btn)

        # Информация о последнем товаре
        self.last_product_info = Label(
            text="",
            font_size=dp(14),
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.last_product_info)

        # Поле ввода названия
        self.input_field = create_input_field("Введите название товара")
        layout.add_widget(self.input_field)

        # Выбор категории с выпадающим списком
        category_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        category_label = Label(text="Категория:", size_hint_x=0.3, color=(1, 1, 1, 1), font_size=dp(16))
        category_layout.add_widget(category_label)

        # Кнопка выбора категории
        self.category_btn = Button(
            text="Другое",
            size_hint_x=0.7,
            background_color=(0.3, 0.5, 0.7, 1),
            font_size=dp(16)
        )
        self.category_btn.bind(on_press=self.show_category_dropdown)
        category_layout.add_widget(self.category_btn)

        layout.add_widget(category_layout)

        # Создаем выпадающий список категорий
        self.category_dropdown = DropDown()
        categories = self.logic.get_quick_categories()

        for category in categories:
            btn = Button(
                text=category,
                size_hint_y=None,
                height=dp(44),
                background_color=(0.4, 0.4, 0.6, 1),
                font_size=dp(16)
            )
            btn.bind(on_press=lambda btn_instance, cat=category: self.select_category(cat))
            self.category_dropdown.add_widget(btn)

        # Кнопка добавления
        add_btn = create_button("ДОБАВИТЬ ТОВАР", (0, 0.8, 0, 1), height=dp(60))
        add_btn.bind(on_press=self.add_item)
        layout.add_widget(add_btn)

        self.message = create_label("", dp(16), (1, 1, 1, 1))
        layout.add_widget(self.message)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), height=dp(50))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        """Очищаем поля при входе на экран"""
        self.input_field.text = ""
        self.category_btn.text = "Другое"
        self.message.text = ""
        self.update_info()

    def show_category_dropdown(self, instance):
        """Показывает выпадающий список категорий"""
        self.category_dropdown.open(instance)

    def select_category(self, category):
        """Выбирает категорию из выпадающего списка"""
        self.category_btn.text = category
        self.category_dropdown.dismiss()

    def update_info(self, *args):
        """Обновляет информацию о списке и последнем товаре"""
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info
            self.current_list_info.text = f"Список: {list_name}"

        last_product = self.logic.get_last_purchased_product()
        if last_product:
            self.last_product_info.text = f"Последний купленный: {last_product}"
            self.repeat_btn.disabled = False
        else:
            self.last_product_info.text = "История покупок пуста"
            self.repeat_btn.disabled = True

    def repeat_last_product(self, instance):
        """Добавляет последний купленный товар в список"""
        last_product = self.logic.get_last_purchased_product()
        if last_product:
            self.input_field.text = last_product
            self.message.text = f"'{last_product}' готов к добавлению"
        else:
            self.message.text = "Нет истории покупок"

    def add_item(self, instance):
        product_name = self.input_field.text.strip()
        category = self.category_btn.text

        if product_name:
            result = self.logic.add_item(product_name, category)
            self.message.text = result
            if "Успех" in result:
                self.input_field.text = ""
                # Сбрасываем категорию на "Другое"
                self.category_btn.text = "Другое"
                self.manager.get_screen('main').update_display()
        else:
            self.message.text = "Введите название товара!"

    def go_back(self, instance):
        self.manager.current = 'main'


class HistoryScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Информация о текущем списке
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_name = list_info[1]
            layout.add_widget(create_label(f"ИСТОРИЯ ПОКУПОК: {list_name}", dp(24), (1, 1, 1, 1)))
        else:
            layout.add_widget(create_label("ИСТОРИЯ ПОКУПОК", dp(24), (1, 1, 1, 1)))

        scroll = ScrollView()
        self.history_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        layout.add_widget(scroll)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), height=dp(50))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_display(self):
        self.history_layout.clear_widgets()

        if not self.logic.current_list_id:
            empty_label = Label(
                text="Выберите список покупок для просмотра истории",
                font_size=dp(18),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(100),
                text_size=(dp(350), None),
                halign='center',
                valign='middle'
            )
            self.history_layout.add_widget(empty_label)
            return

        history = self.logic.get_purchase_history()

        if not history:
            empty_label = Label(
                text="История покупок пуста\n\nОтмечайте товары купленными",
                font_size=dp(18),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(100),
                text_size=(dp(350), None),
                halign='center',
                valign='middle'
            )
            self.history_layout.add_widget(empty_label)
        else:
            for item in history:
                product_name, category, bought_by, bought_date = item
                bought_by_text = bought_by if bought_by else "Неизвестно"

                # Форматируем дату для лучшего отображения
                if bought_date:
                    try:
                        # Преобразуем строку даты в читаемый формат
                        date_obj = datetime.strptime(bought_date, '%Y-%m-%d %H:%M:%S')
                        formatted_date = date_obj.strftime('%d.%m.%Y %H:%M')
                    except:
                        formatted_date = bought_date
                else:
                    formatted_date = "Дата неизвестна"

                item_text = f"{product_name}\n"
                item_text += f"Категория: {category}\n"
                item_text += f"Купил: {bought_by_text}\n"
                item_text += f"Дата: {formatted_date}"

                item_label = Label(
                    text=item_text,
                    font_size=dp(14),
                    size_hint_y=None,
                    height=dp(80),
                    color=(1, 1, 1, 1),
                    text_size=(dp(350), None),
                    halign='left',
                    valign='middle'
                )
                self.history_layout.add_widget(item_label)

    def go_back(self, instance):
        self.manager.current = 'main'


class SuggestionsScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Информация о текущем списке
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_name = list_info[1]
            layout.add_widget(create_label(f"ПРЕДЛОЖЕНИЯ: {list_name}", dp(24), (1, 1, 1, 1)))
        else:
            layout.add_widget(create_label("УМНЫЕ ПРЕДЛОЖЕНИЯ", dp(24), (1, 1, 1, 1)))

        scroll = ScrollView()
        self.suggestions_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(10))
        self.suggestions_layout.bind(minimum_height=self.suggestions_layout.setter('height'))
        scroll.add_widget(self.suggestions_layout)
        layout.add_widget(scroll)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1), height=dp(50))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_display(self):
        self.suggestions_layout.clear_widgets()
        suggestions = self.logic.get_smart_suggestions()

        if not suggestions:
            empty_label = Label(
                text="Нет предложений\n\nСоветы появятся после покупок",
                font_size=dp(18),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(100),
                text_size=(dp(350), None),
                halign='center',
                valign='middle'
            )
            self.suggestions_layout.add_widget(empty_label)
        else:
            for item in suggestions:
                product_name = item[0]
                count = item[1]

                suggestion_item = SuggestionItem(
                    product_name=product_name,
                    count=count,
                    logic=self.logic,
                    suggestions_screen=self
                )
                self.suggestions_layout.add_widget(suggestion_item)

    def go_back(self, instance):
        self.manager.current = 'main'

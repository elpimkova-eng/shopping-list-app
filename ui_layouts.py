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
from datetime import datetime
from ui_controls import create_button, create_label, create_input_field, ProductItem, SuggestionItem


class MainLayout(ScreenManager):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
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

        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(create_label("ВХОД", 32, (1, 1, 1, 1)))

        self.username_input = create_input_field("Имя пользователя")
        layout.add_widget(self.username_input)

        self.password_input = TextInput(
            hint_text="Пароль",
            size_hint_y=None,
            height=40,
            multiline=False,
            password=True
        )
        layout.add_widget(self.password_input)

        login_btn = create_button("ВОЙТИ", (0.2, 0.6, 0.8, 1))
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        register_btn = create_button("РЕГИСТРАЦИЯ", (0.4, 0.4, 0.4, 1))
        register_btn.bind(on_press=self.goto_register)
        layout.add_widget(register_btn)

        self.message = create_label("", 16, (1, 1, 1, 1))
        layout.add_widget(self.message)

        self.add_widget(layout)

    def on_enter(self):
        self.username_input.text = ""
        self.password_input.text = ""
        self.message.text = ""

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username and password:
            if self.logic.login_user(username, password):
                self.message.text = "Успешный вход!"
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

        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(create_label("РЕГИСТРАЦИЯ", 32, (1, 1, 1, 1)))

        self.username_input = create_input_field("Имя пользователя")
        layout.add_widget(self.username_input)

        self.password_input = TextInput(
            hint_text="Пароль",
            size_hint_y=None,
            height=40,
            multiline=False,
            password=True
        )
        layout.add_widget(self.password_input)

        self.confirm_input = TextInput(
            hint_text="Подтвердите пароль",
            size_hint_y=None,
            height=40,
            multiline=False,
            password=True
        )
        layout.add_widget(self.confirm_input)

        register_btn = create_button("ЗАРЕГИСТРИРОВАТЬСЯ", (0.2, 0.8, 0.4, 1))
        register_btn.bind(on_press=self.register)
        layout.add_widget(register_btn)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.goto_login)
        layout.add_widget(back_btn)

        self.message = create_label("", 16, (1, 1, 1, 1))
        layout.add_widget(self.message)

        self.add_widget(layout)

    def on_enter(self):
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

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.user_info = Label(
            text=f"УМНЫЙ СПИСОК ПОКУПОК\nПользователь: {self.logic.get_current_username()}",
            font_size=30,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=60,
            halign='center'
        )
        layout.add_widget(self.user_info)

        self.list_info = Label(
            text="Выберите список покупок",
            font_size=16,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=40,
            halign='center'
        )
        layout.add_widget(self.list_info)

        logout_btn = create_button("ВЫЙТИ", (0.8, 0.3, 0.3, 1), height=40)
        logout_btn.bind(on_press=self.logout)
        layout.add_widget(logout_btn)

        list_management = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)

        create_list_btn = create_button("СОЗДАТЬ", (0.2, 0.6, 0.2, 1), height=40)
        create_list_btn.bind(on_press=self.goto_create_list)
        list_management.add_widget(create_list_btn)

        join_list_btn = create_button("ПРИСОЕДИНИТЬСЯ", (0.2, 0.4, 0.8, 1), height=40)
        join_list_btn.bind(on_press=self.goto_join_list)
        list_management.add_widget(join_list_btn)

        leave_list_btn = create_button("ПОКИНУТЬ", (0.8, 0.4, 0.2, 1), height=40)
        leave_list_btn.bind(on_press=self.leave_current_list)
        list_management.add_widget(leave_list_btn)

        layout.add_widget(list_management)

        layout.add_widget(create_label("Ваши списки:", 16, (1, 1, 1, 1)))

        scroll_lists = ScrollView(size_hint_y=0.4)
        self.lists_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.lists_layout.bind(minimum_height=self.lists_layout.setter('height'))
        scroll_lists.add_widget(self.lists_layout)
        layout.add_widget(scroll_lists)

        scroll = ScrollView()
        self.list_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        layout.add_widget(scroll)

        buttons = [
            ("ДОБАВИТЬ ТОВАР", self.goto_add, (0, 0.6, 0, 1)),
            ("ОЧИСТИТЬ СПИСОК", self.clear_list, (0.8, 0.2, 0, 1)),
            ("ИСТОРИЯ ПОКУПОК", self.goto_history, (0.2, 0.4, 0.8, 1)),
            ("УМНЫЕ ПРЕДЛОЖЕНИЯ", self.goto_suggestions, (1, 0.5, 0, 1)),
        ]

        for text, callback, color in buttons:
            btn = create_button(text, color)
            btn.bind(on_press=callback)
            layout.add_widget(btn)

        self.add_widget(layout)
        self.update_display()

    def update_user_info(self):
        self.user_info.text = f"УМНЫЙ СПИСОК ПОКУПОК\nПользователь: {self.logic.get_current_username()}"

    def load_user_lists(self):
        self.lists_layout.clear_widgets()
        lists = self.logic.get_user_lists()

        if not lists:
            empty_label = Label(
                text="У вас пока нет списков\nСоздайте новый или присоединитесь к существующему",
                font_size=14,
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height=60
            )
            self.lists_layout.add_widget(empty_label)
            return

        for list_data in lists:
            list_id, list_name, owner_id, owner_name, share_code = list_data
            is_owner = owner_id == self.logic.db.get_current_user_id()

            list_item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=70, spacing=5)

            owner_indicator = "(Владелец)" if is_owner else ""
            list_btn = Button(
                text=f"{list_name}\nВладелец: {owner_name} {owner_indicator}",
                size_hint_x=0.55,
                background_color=(0.3, 0.5, 0.7, 1) if is_owner else (0.4, 0.4, 0.6, 1),
                color=(1, 1, 1, 1),
                font_size=14
            )
            list_btn.bind(on_press=lambda instance, lid=list_id: self.select_list(lid))

            info_btn = Button(
                text="Инфо",
                size_hint_x=0.2,
                background_color=(0.3, 0.5, 0.8, 1),
                font_size=14
            )
            info_btn.bind(on_press=lambda instance, lid=list_id: self.show_list_info(lid))

            delete_btn = Button(
                text="Удалить",
                size_hint_x=0.25,
                background_color=(0.8, 0.2, 0.2, 1),
                font_size=14
            )
            delete_btn.bind(on_press=lambda instance, lid=list_id, lname=list_name: self.delete_list(lid, lname))
            delete_btn.disabled = not is_owner

            list_item_layout.add_widget(list_btn)
            list_item_layout.add_widget(info_btn)
            list_item_layout.add_widget(delete_btn)

            self.lists_layout.add_widget(list_item_layout)

    def select_list(self, list_id):
        self.logic.set_current_list(list_id)
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info
            members = self.logic.get_list_members()
            self.list_info.text = f"{list_name} (Участников: {len(members)})"
            self.update_display()

    def show_list_info(self, list_id):
        self.logic.set_current_list(list_id)
        list_info_screen = self.manager.get_screen('list_info')
        list_info_screen.update_info()
        self.manager.current = 'list_info'

    def delete_list(self, list_id, list_name):

        def confirm_delete(instance):
            result = self.logic.delete_shopping_list(list_id)
            print(result)
            self.load_user_lists()
            if self.logic.current_list_id == list_id:
                self.logic.current_list_id = None
                self.list_info.text = "Выберите список покупок"
                self.update_display()
            popup.dismiss()

        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(
            text=f'Вы уверены, что хотите удалить список\n"{list_name}"?\n\nЭто действие нельзя отменить!',
            font_size=16,
            color=(1, 1, 1, 1),
            halign='center'
        ))

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        yes_btn = Button(text='ДА, УДАЛИТЬ', background_color=(0.8, 0.2, 0.2, 1))
        no_btn = Button(text='ОТМЕНА', background_color=(0.4, 0.4, 0.4, 1))

        yes_btn.bind(on_press=confirm_delete)
        no_btn.bind(on_press=lambda x: popup.dismiss())

        buttons_layout.add_widget(yes_btn)
        buttons_layout.add_widget(no_btn)
        content.add_widget(buttons_layout)

        popup = Popup(title='Удаление списка', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def leave_current_list(self, instance):
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
            empty_label = create_label("Выберите список покупок\n\nСоздайте новый список или выберите существующий", 18,
                                       (1, 1, 1, 1))
            empty_label.height = 100
            self.list_layout.add_widget(empty_label)
            return

        products = self.logic.get_current_list()
        if not products:
            empty_label = create_label("Список покупок пустой\n\nДобавьте товары через кнопку ниже", 18, (1, 1, 1, 1))
            empty_label.height = 100
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

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(create_label("СОЗДАТЬ НОВЫЙ СПИСОК", 24, (1, 1, 1, 1)))

        self.list_name_input = create_input_field("Введите название списка")
        layout.add_widget(self.list_name_input)

        create_btn = create_button("СОЗДАТЬ СПИСОК", (0, 0.8, 0, 1))
        create_btn.bind(on_press=self.create_list)
        layout.add_widget(create_btn)

        self.message = create_label("", 16, (1, 1, 1, 1))
        layout.add_widget(self.message)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
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
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)

        content.add_widget(Label(
            text=f'Список создан!\n\nКод для присоединения:\n',
            font_size=18,
            color=(1, 1, 1, 1),
            halign='center'
        ))

        code_label = Label(
            text=f'{share_code}',
            font_size=32,
            color=(0, 1, 0, 1),
            halign='center'
        )
        content.add_widget(code_label)

        content.add_widget(Label(
            text='\nПоделитесь этим кодом с друзьями,\nчтобы они могли присоединиться к списку',
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            halign='center'
        ))

        copy_btn = Button(
            text='КОПИРОВАТЬ КОД',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.8, 1)
        )

        ok_btn = Button(
            text='ЗАКРЫТЬ',
            size_hint_y=None,
            height=50,
            background_color=(0.4, 0.4, 0.4, 1)
        )

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        buttons_layout.add_widget(copy_btn)
        buttons_layout.add_widget(ok_btn)
        content.add_widget(buttons_layout)

        popup = Popup(
            title='Код для присоединения',
            content=content,
            size_hint=(0.8, 0.6)
        )

        def copy_code(instance):
            Clipboard.copy(share_code)
            self.show_success_message("Код скопирован в буфер обмена!")

        copy_btn.bind(on_press=copy_code)
        ok_btn.bind(on_press=popup.dismiss)

        popup.open()

    def show_success_message(self, message):
        popup = Popup(
            title='Успех',
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'


class JoinListScreen(Screen):
    def __init__(self, name, logic):
        super().__init__(name=name)
        self.logic = logic

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(create_label("ПРИСОЕДИНИТЬСЯ К СПИСКУ", 24, (1, 1, 1, 1)))

        self.code_input = create_input_field("Введите код списка (8 символов)")
        layout.add_widget(self.code_input)

        join_btn = create_button("ПРИСОЕДИНИТЬСЯ", (0.2, 0.4, 0.8, 1))
        join_btn.bind(on_press=self.join_list)
        layout.add_widget(join_btn)

        self.message = create_label("", 16, (1, 1, 1, 1))
        layout.add_widget(self.message)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

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
                # Обновляем главный экран
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

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(create_label("ИНФОРМАЦИЯ О СПИСКЕ", 24, (1, 1, 1, 1)))

        self.list_info_label = Label(
            text="",
            font_size=16,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=100,
            text_size=(350, None),
            halign='center'
        )
        layout.add_widget(self.list_info_label)

        self.code_btn = create_button("ПОКАЗАТЬ И СКОПИРОВАТЬ КОД", (0.3, 0.5, 0.8, 1), height=40)
        self.code_btn.bind(on_press=self.show_code)
        layout.add_widget(self.code_btn)

        layout.add_widget(create_label("Участники:", 16, (1, 1, 1, 1)))

        scroll_members = ScrollView(size_hint_y=0.4)
        self.members_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.members_layout.bind(minimum_height=self.members_layout.setter('height'))
        scroll_members.add_widget(self.members_layout)
        layout.add_widget(scroll_members)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_info(self):
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info
            current_user_id = self.logic.db.get_current_user_id()

            info_text = f"{list_name}\n"
            info_text += f"Владелец: {owner_name}\n"
            info_text += f"Код: {share_code}" if owner_id == current_user_id else "Код: доступен владельцу"

            self.list_info_label.text = info_text

            self.code_btn.disabled = (owner_id != current_user_id)

            self.members_layout.clear_widgets()
            members = self.logic.get_list_members()
            for member in members:
                is_owner = (member == owner_name)
                member_text = f"{member} (владелец)" if is_owner else f"{member}"
                member_label = Label(
                    text=member_text,
                    size_hint_y=None,
                    height=30,
                    color=(1, 1, 1, 1),
                    font_size=14
                )
                self.members_layout.add_widget(member_label)

    def show_code(self, instance):
        list_info = self.logic.get_current_list_info()
        if list_info:
            list_id, list_name, owner_id, owner_name, share_code = list_info

            content = BoxLayout(orientation='vertical', padding=20, spacing=15)

            content.add_widget(Label(
                text=f'Код для присоединения к списку\n"{list_name}":',
                font_size=18,
                color=(1, 1, 1, 1),
                halign='center'
            ))

            code_label = Label(
                text=f'{share_code}',
                font_size=32,
                color=(0, 1, 0, 1),
                halign='center'
            )
            content.add_widget(code_label)

            content.add_widget(Label(
                text='\nПоделитесь этим кодом с друзьями',
                font_size=14,
                color=(0.8, 0.8, 0.8, 1),
                halign='center'
            ))

            copy_btn = Button(
                text='КОПИРОВАТЬ КОД',
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.6, 0.8, 1)
            )

            ok_btn = Button(
                text='ЗАКРЫТЬ',
                size_hint_y=None,
                height=50,
                background_color=(0.4, 0.4, 0.4, 1)
            )

            buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
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

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(create_label("ДОБАВИТЬ ТОВАР", 24, (1, 1, 1, 1)))

        self.current_list_info = Label(
            text="",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.current_list_info)

        self.repeat_btn = create_button("Повторить последний товар", (0.5, 0.3, 0.8, 1), height=40)
        self.repeat_btn.bind(on_press=self.repeat_last_product)
        layout.add_widget(self.repeat_btn)

        self.last_product_info = Label(
            text="",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.last_product_info)

        self.input_field = create_input_field("Введите название товара")
        layout.add_widget(self.input_field)

        category_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        category_label = Label(text="Категория:", size_hint_x=0.3, color=(1, 1, 1, 1))
        category_layout.add_widget(category_label)

        self.category_btn = Button(
            text="Другое",
            size_hint_x=0.7,
            background_color=(0.3, 0.5, 0.7, 1)
        )
        self.category_btn.bind(on_press=self.show_category_dropdown)
        category_layout.add_widget(self.category_btn)

        layout.add_widget(category_layout)

        self.category_dropdown = DropDown()
        categories = self.logic.get_quick_categories()

        for category in categories:
            btn = Button(
                text=category,
                size_hint_y=None,
                height=44,
                background_color=(0.4, 0.4, 0.6, 1)
            )
            btn.bind(on_press=lambda btn_instance, cat=category: self.select_category(cat))
            self.category_dropdown.add_widget(btn)

        add_btn = create_button("ДОБАВИТЬ ТОВАР", (0, 0.8, 0, 1))
        add_btn.bind(on_press=self.add_item)
        layout.add_widget(add_btn)

        self.message = create_label("", 16, (1, 1, 1, 1))
        layout.add_widget(self.message)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        self.input_field.text = ""
        self.category_btn.text = "Другое"
        self.message.text = ""
        self.update_info()

    def show_category_dropdown(self, instance):
        self.category_dropdown.open(instance)

    def select_category(self, category):
        self.category_btn.text = category
        self.category_dropdown.dismiss()

    def update_info(self, *args):
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

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        list_info = self.logic.get_current_list_info()
        if list_info:
            list_name = list_info[1]
            layout.add_widget(create_label(f"ИСТОРИЯ ПОКУПОК: {list_name}", 24, (1, 1, 1, 1)))
        else:
            layout.add_widget(create_label("ИСТОРИЯ ПОКУПОК", 24, (1, 1, 1, 1)))

        scroll = ScrollView()
        self.history_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        layout.add_widget(scroll)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_display(self):
        self.history_layout.clear_widgets()

        if not self.logic.current_list_id:
            empty_label = Label(
                text="Выберите список покупок для просмотра истории",
                font_size=18,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=100,
                text_size=(350, None),
                halign='center',
                valign='middle'
            )
            self.history_layout.add_widget(empty_label)
            return

        history = self.logic.get_purchase_history()

        if not history:
            empty_label = Label(
                text="История покупок пуста\n\nОтмечайте товары купленными",
                font_size=18,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=100,
                text_size=(350, None),
                halign='center',
                valign='middle'
            )
            self.history_layout.add_widget(empty_label)
        else:
            for item in history:
                product_name, category, bought_by, bought_date = item
                bought_by_text = bought_by if bought_by else "Неизвестно"

                if bought_date:
                    try:
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
                    font_size=14,
                    size_hint_y=None,
                    height=80,
                    color=(1, 1, 1, 1),
                    text_size=(350, None),
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

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        list_info = self.logic.get_current_list_info()
        if list_info:
            list_name = list_info[1]
            layout.add_widget(create_label(f"ПРЕДЛОЖЕНИЯ: {list_name}", 24, (1, 1, 1, 1)))
        else:
            layout.add_widget(create_label("УМНЫЕ ПРЕДЛОЖЕНИЯ", 24, (1, 1, 1, 1)))

        scroll = ScrollView()
        self.suggestions_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.suggestions_layout.bind(minimum_height=self.suggestions_layout.setter('height'))
        scroll.add_widget(self.suggestions_layout)
        layout.add_widget(scroll)

        back_btn = create_button("НАЗАД", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_display(self):
        self.suggestions_layout.clear_widgets()
        suggestions = self.logic.get_smart_suggestions()

        if not suggestions:
            empty_label = Label(
                text="Нет предложений\n\nСоветы появятся после покупок",
                font_size=18,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=100,
                text_size=(350, None),
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
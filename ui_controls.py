from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


def create_button(text, color, height=50):
    return Button(
        text=text,
        background_color=color,
        color=(1, 1, 1, 1),
        size_hint_y=None,
        height=height
    )


def create_label(text, font_size=24, color=(1, 1, 1, 1)):
    return Label(
        text=text,
        font_size=font_size,
        color=color,
        size_hint_y=None,
        valign='top'
    )


def create_input_field(hint_text):
    return TextInput(
        hint_text=hint_text,
        size_hint_y=None,
        height=40,
        multiline=False
    )


class ProductItem(BoxLayout):
    def __init__(self, product_id, product_name, category, logic, main_screen, created_by=None, bought_by=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.logic = logic
        self.main_screen = main_screen
        self.created_by = created_by
        self.is_bought = bought_by is not None

        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 70
        self.padding = [10, 5]
        self.spacing = 10

        delete_btn = Button(
            text="Удалить",
            size_hint_x=0.25,
            background_color=(0.8, 0, 0, 1),
            font_size=14
        )
        delete_btn.bind(on_press=self.delete_product)

        center_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)

        name_label = Label(
            text=product_name,
            font_size=18,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1),
            text_size=(200, None)
        )

        info_text = f"{category}"
        if self.is_bought:
            info_text += f" Куплен"
        elif self.created_by:
            current_user = self.logic.get_current_username()
            info_text += f" {current_user}"

        info_label = Label(
            text=info_text,
            font_size=12,
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='middle',
            text_size=(200, None)
        )

        center_layout.add_widget(name_label)
        center_layout.add_widget(info_label)

        self.bought_btn = Button(
            text="Куплено" if self.is_bought else "Купить",
            size_hint_x=0.25,
            background_color=(0, 0.6, 0, 1) if self.is_bought else (0, 0.8, 0, 1),
            font_size=14
        )
        self.bought_btn.bind(on_press=self.mark_bought)

        self.add_widget(delete_btn)
        self.add_widget(center_layout)
        self.add_widget(self.bought_btn)

    def mark_bought(self, instance):
        print(f"Нажата кнопка купить для товара {self.product_id}")
        result = self.logic.toggle_bought(self.product_id)
        print(f"Результат: {result}")
        self.main_screen.update_display()

    def delete_product(self, instance):
        result = self.logic.delete_item(self.product_id)
        print(f"Удаление товара: {result}")
        self.main_screen.update_display()


class SuggestionItem(BoxLayout):
    def __init__(self, product_name, count, logic, suggestions_screen, **kwargs):
        super().__init__(**kwargs)
        self.product_name = product_name
        self.count = count
        self.logic = logic
        self.suggestions_screen = suggestions_screen

        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.padding = [10, 5]
        self.spacing = 10

        info_label = Label(
            text=f"{product_name}\n(куплен {count} раз)",
            size_hint_x=0.7,
            font_size=16,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1),
            text_size=(250, None)
        )

        add_btn = Button(
            text="Добавить",
            size_hint_x=0.3,
            background_color=(0, 0.7, 0, 1),
            color=(1, 1, 1, 1)
        )
        add_btn.bind(on_press=self.add_to_list)

        self.add_widget(info_label)
        self.add_widget(add_btn)

    def add_to_list(self, instance):
        result = self.logic.add_suggestion(self.product_name)
        print(result)
        self.suggestions_screen.manager.current = 'main'
        main_screen = self.suggestions_screen.manager.get_screen('main')
        main_screen.update_display()
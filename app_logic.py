from database import Database


class AppLogic:
    def __init__(self):
        self.db = Database()
        self.current_list_id = None

    def register_user(self, username, password):
        return self.db.register_user(username, password)

    def login_user(self, username, password):
        return self.db.login_user(username, password)

    def logout_user(self):
        self.db.logout_user()
        self.current_list_id = None

    def is_logged_in(self):
        return self.db.is_logged_in()

    def get_current_username(self):
        if not self.is_logged_in():
            return "Гость"

        username = self.db.get_current_username()
        return username if username else "Пользователь"

    def create_shared_list(self, list_name):
        if not self.is_logged_in():
            return None, "Сначала войдите в систему"

        list_id = self.db.create_shopping_list(list_name)
        if list_id:
            self.current_list_id = list_id
            return list_id, f"Список '{list_name}' создан"
        return None, "Ошибка создания списка"

    def join_shared_list(self, list_id):
        if not self.is_logged_in():
            return "Сначала войдите в систему"

        success = self.db.join_shopping_list(list_id)
        if success:
            self.current_list_id = list_id
            return f"Вы присоединились к списку"
        return "Не удалось присоединиться к списку"

    def get_user_lists(self):
        if not self.is_logged_in():
            return []
        return self.db.get_user_shopping_lists()

    def set_current_list(self, list_id):
        self.current_list_id = list_id

    def get_current_list_info(self):
        if not self.current_list_id:
            return None
        return self.db.get_list_info(self.current_list_id)

    def delete_shopping_list(self, list_id):
        if not self.is_logged_in():
            return "Сначала войдите в систему"

        success = self.db.delete_shopping_list(list_id)
        if success:
            if self.current_list_id == list_id:
                self.current_list_id = None
            return "Список удален"
        return "Ошибка удаления списка"

    def add_item(self, product_name, category='Другое'):
        if not self.is_logged_in():
            return "Сначала войдите в систему"
        if not self.current_list_id:
            return "Выберите или создайте список покупок"

        success = self.db.add_product(self.current_list_id, product_name, category)
        return f"'{product_name}' добавлен" if success else "Ошибка"

    def get_current_list(self):
        if not self.is_logged_in() or not self.current_list_id:
            return []
        return self.db.get_shopping_list(self.current_list_id)

    def toggle_bought(self, product_id):
        if not self.is_logged_in():
            return "Сначала войдите в систему"

        success = self.db.toggle_bought_status(product_id)
        return "Статус товара изменен" if success else "Ошибка"

    def delete_item(self, product_id):
        if not self.is_logged_in():
            return "Сначала войдите в систему"
        success = self.db.delete_product(product_id)
        return "Товар удален" if success else "Ошибка"

    def clear_all_items(self):
        if not self.is_logged_in() or not self.current_list_id:
            return "Сначала войдите в систему и выберите список"
        count = self.db.clear_shopping_list(self.current_list_id)
        return f"Список очищен, удалено {count} товаров"

    def get_purchase_history(self):
        if not self.is_logged_in() or not self.current_list_id:
            return []
        history = self.db.get_purchase_history(self.current_list_id)
        print(f"История покупок из БД для списка {self.current_list_id}: {len(history)} записей")
        return history

    def get_smart_suggestions(self):
        if not self.is_logged_in() or not self.current_list_id:
            return []
        suggestions = self.db.get_smart_suggestions(self.current_list_id)
        print(f"Умные предложения из БД для списка {self.current_list_id}: {len(suggestions)}")
        return suggestions

    def get_last_purchased_product(self):
        if not self.is_logged_in() or not self.current_list_id:
            return None
        last_product = self.db.get_last_purchased_product(self.current_list_id)
        print(f"Последний купленный товар для списка {self.current_list_id}: {last_product}")
        return last_product

    def add_suggestion(self, product_name):
        if not self.is_logged_in() or not self.current_list_id:
            return "Сначала войдите в систему и выберите список"
        success = self.db.add_suggestion_to_list(self.current_list_id, product_name)
        return f"'{product_name}' добавлен в список" if success else "Ошибка"

    def get_list_members(self):
        if not self.current_list_id:
            return []
        return self.db.get_list_members(self.current_list_id)

    def leave_current_list(self):
        if self.current_list_id:
            self.db.leave_shopping_list(self.current_list_id)
            self.current_list_id = None
        return "Вы вышли из списка"

    def get_quick_categories(self):
        return [
            "Фрукты", "Овощи", "Молочные", "Хлеб",
            "Мясо", "Рыба", "Сладости", "Напитки",
            "Хозтовары", "Аптека", "Детское", "Бакалея",
            "Заморозка", "Гигиена", "Снеки", "Другое"
        ]
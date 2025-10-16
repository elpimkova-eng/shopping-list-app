import sqlite3
from datetime import datetime
import hashlib
import uuid


class Database:
    def __init__(self):
        self.db_name = "shopping_list.db"
        self.current_user_id = None
        self.current_username = None
        self.init_database()

    def get_connection(self):
        try:
            return sqlite3.connect(self.db_name)
        except Exception as e:
            print(f"Ошибка БД: {e}")
            return None

    def init_database(self):
        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()

            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Таблица списков покупок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shopping_lists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    owner_id INTEGER NOT NULL,
                    share_code TEXT UNIQUE,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (owner_id) REFERENCES users (id)
                )
            ''')

            # Таблица участников списков
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS list_members (
                    list_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (list_id, user_id),
                    FOREIGN KEY (list_id) REFERENCES shopping_lists (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Таблица товаров
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shopping_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    list_id INTEGER NOT NULL,
                    product_name TEXT NOT NULL,
                    category TEXT DEFAULT 'Другое',
                    sort_order INTEGER DEFAULT 0,
                    created_by INTEGER NOT NULL,
                    bought_by INTEGER,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    bought_date TIMESTAMP,
                    FOREIGN KEY (list_id) REFERENCES shopping_lists (id),
                    FOREIGN KEY (created_by) REFERENCES users (id),
                    FOREIGN KEY (bought_by) REFERENCES users (id)
                )
            ''')

            # Таблица истории покупок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchase_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    list_id INTEGER NOT NULL,
                    product_name TEXT NOT NULL,
                    category TEXT DEFAULT 'Другое',
                    bought_by INTEGER,
                    bought_date TIMESTAMP,
                    FOREIGN KEY (list_id) REFERENCES shopping_lists (id),
                    FOREIGN KEY (bought_by) REFERENCES users (id)
                )
            ''')

            conn.commit()
            print("База данных инициализирована")
            return True
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
            return False
        finally:
            conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()
            password_hash = self.hash_password(password)

            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            print(f"Пользователь {username} зарегистрирован")
            return True
        except sqlite3.IntegrityError:
            print("Пользователь уже существует")
            return False
        except Exception as e:
            print(f"Ошибка регистрации: {e}")
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()
            password_hash = self.hash_password(password)

            cursor.execute(
                "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            result = cursor.fetchone()

            if result:
                self.current_user_id = result[0]
                self.current_username = result[1]
                print(f"Пользователь {username} вошел в систему")
                return True
            else:
                print("Неверные учетные данные")
                return False
        except Exception as e:
            print(f"Ошибка входа: {e}")
            return False
        finally:
            conn.close()

    def logout_user(self):
        print(f"Пользователь {self.current_username} вышел из системы")
        self.current_user_id = None
        self.current_username = None

    def get_current_user_id(self):
        return self.current_user_id

    def get_current_username(self):
        return self.current_username

    def is_logged_in(self):
        return self.current_user_id is not None

    def create_shopping_list(self, list_name):
        if not self.is_logged_in():
            return None

        conn = self.get_connection()
        if not conn: return None

        try:
            cursor = conn.cursor()
            share_code = str(uuid.uuid4())[:8].upper()

            cursor.execute(
                "INSERT INTO shopping_lists (name, owner_id, share_code) VALUES (?, ?, ?)",
                (list_name, self.current_user_id, share_code)
            )
            list_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO list_members (list_id, user_id) VALUES (?, ?)",
                (list_id, self.current_user_id)
            )

            conn.commit()
            print(f"Создан список '{list_name}' с кодом {share_code}")
            return list_id
        except Exception as e:
            print(f"Ошибка создания списка: {e}")
            return None
        finally:
            conn.close()

    def join_shopping_list(self, share_code):
        if not self.is_logged_in():
            return False

        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()

            # Находим список по коду (без учета регистра)
            cursor.execute("SELECT id FROM shopping_lists WHERE UPPER(share_code) = ?", (share_code.upper(),))
            result = cursor.fetchone()

            if not result:
                print("Список с таким кодом не найден")
                return False

            list_id = result[0]

            # Проверяем, не является ли пользователь уже участником
            cursor.execute(
                "SELECT 1 FROM list_members WHERE list_id = ? AND user_id = ?",
                (list_id, self.current_user_id)
            )
            if cursor.fetchone():
                print("Вы уже участник этого списка")
                return False

            # Добавляем пользователя как участника
            cursor.execute(
                "INSERT INTO list_members (list_id, user_id) VALUES (?, ?)",
                (list_id, self.current_user_id)
            )

            conn.commit()
            print(f"Пользователь присоединился к списку {list_id}")
            return True
        except Exception as e:
            print(f"Ошибка присоединения к списку: {e}")
            return False
        finally:
            conn.close()

    def get_user_shopping_lists(self):
        if not self.is_logged_in():
            return []

        conn = self.get_connection()
        if not conn: return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sl.id, sl.name, sl.owner_id, u.username, sl.share_code
                FROM shopping_lists sl
                JOIN list_members lm ON sl.id = lm.list_id
                JOIN users u ON sl.owner_id = u.id
                WHERE lm.user_id = ?
                ORDER BY sl.created_date DESC
            ''', (self.current_user_id,))

            lists = cursor.fetchall()
            print(f"Найдено {len(lists)} списков для пользователя")
            return lists
        except Exception as e:
            print(f"Ошибка получения списков: {e}")
            return []
        finally:
            conn.close()

    def get_list_info(self, list_id):
        conn = self.get_connection()
        if not conn: return None

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sl.id, sl.name, sl.owner_id, u.username, sl.share_code
                FROM shopping_lists sl
                JOIN users u ON sl.owner_id = u.id
                WHERE sl.id = ?
            ''', (list_id,))

            return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка получения информации о списке: {e}")
            return None
        finally:
            conn.close()

    def delete_shopping_list(self, list_id):
        if not self.is_logged_in():
            return False

        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()

            # Проверяем, является ли пользователь владельцем
            cursor.execute("SELECT owner_id FROM shopping_lists WHERE id = ?", (list_id,))
            result = cursor.fetchone()

            if not result or result[0] != self.current_user_id:
                print("Только владелец может удалить список")
                return False

            # Удаляем все связанные данные
            cursor.execute("DELETE FROM shopping_items WHERE list_id = ?", (list_id,))
            cursor.execute("DELETE FROM purchase_history WHERE list_id = ?", (list_id,))
            cursor.execute("DELETE FROM list_members WHERE list_id = ?", (list_id,))
            cursor.execute("DELETE FROM shopping_lists WHERE id = ?", (list_id,))

            conn.commit()
            print(f"Список {list_id} удален")
            return True
        except Exception as e:
            print(f"Ошибка удаления списка: {e}")
            return False
        finally:
            conn.close()

    def get_list_members(self, list_id):
        conn = self.get_connection()
        if not conn: return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.username 
                FROM list_members lm
                JOIN users u ON lm.user_id = u.id
                WHERE lm.list_id = ?
            ''', (list_id,))

            members = [row[0] for row in cursor.fetchall()]
            print(f"Найдено {len(members)} участников списка {list_id}")
            return members
        except Exception as e:
            print(f"Ошибка получения участников: {e}")
            return []
        finally:
            conn.close()

    def add_product(self, list_id, product_name, category='Другое'):
        if not self.is_logged_in():
            print("Пользователь не авторизован")
            return False

        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(sort_order) FROM shopping_items WHERE list_id = ?", (list_id,))
            max_order = cursor.fetchone()[0] or 0

            cursor.execute(
                "INSERT INTO shopping_items (list_id, product_name, category, sort_order, created_by) VALUES (?, ?, ?, ?, ?)",
                (list_id, product_name, category, max_order + 1, self.current_user_id)
            )
            conn.commit()
            print(f"Добавлен товар '{product_name}' в список {list_id}")
            return True
        except Exception as e:
            print(f"Ошибка добавления товара: {e}")
            return False
        finally:
            conn.close()

    def get_shopping_list(self, list_id):
        if not self.is_logged_in():
            print("Пользователь не авторизован")
            return []

        conn = self.get_connection()
        if not conn: return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, product_name, category, sort_order, created_by, bought_by
                FROM shopping_items 
                WHERE list_id = ? AND bought_by IS NULL
                ORDER BY sort_order
            ''', (list_id,))
            products = cursor.fetchall()
            print(f"Найдено {len(products)} товаров в списке {list_id}")
            return products
        except Exception as e:
            print(f"Ошибка получения списка товаров: {e}")
            return []
        finally:
            conn.close()

    def toggle_bought_status(self, product_id):
        if not self.is_logged_in():
            print("Пользователь не авторизован")
            return False

        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()

            # Получаем текущий статус товара
            cursor.execute("SELECT list_id, product_name, category, bought_by FROM shopping_items WHERE id = ?",
                           (product_id,))
            product = cursor.fetchone()

            if not product:
                print("Товар не найден")
                return False

            list_id, product_name, category, current_bought_by = product

            # Получаем текущее время в правильном формате
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if current_bought_by is None:
                # Отмечаем как купленный с явным указанием времени
                cursor.execute(
                    "UPDATE shopping_items SET bought_by = ?, bought_date = ? WHERE id = ?",
                    (self.current_user_id, current_time, product_id)
                )

                # Добавляем в историю покупок с явным указанием времени
                cursor.execute(
                    "INSERT INTO purchase_history (list_id, product_name, category, bought_by, bought_date) VALUES (?, ?, ?, ?, ?)",
                    (list_id, product_name, category, self.current_user_id, current_time)
                )
                print(f"Товар '{product_name}' отмечен как купленный")
            else:
                # Отменяем покупку
                cursor.execute(
                    "UPDATE shopping_items SET bought_by = NULL, bought_date = NULL WHERE id = ?",
                    (product_id,)
                )
                print(f"Статус покупки товара '{product_name}' отменен")

            conn.commit()
            return True

        except Exception as e:
            print(f"Ошибка переключения статуса покупки: {e}")
            return False
        finally:
            conn.close()

    def delete_product(self, product_id):
        if not self.is_logged_in():
            return False

        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM shopping_items WHERE id = ?", (product_id,))
            conn.commit()
            print(f"Товар {product_id} удален")
            return True
        except Exception as e:
            print(f"Ошибка удаления товара: {e}")
            return False
        finally:
            conn.close()

    def clear_shopping_list(self, list_id):
        if not self.is_logged_in():
            return 0

        conn = self.get_connection()
        if not conn: return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM shopping_items WHERE list_id = ? AND bought_by IS NULL", (list_id,))
            count = cursor.fetchone()[0]
            cursor.execute("DELETE FROM shopping_items WHERE list_id = ? AND bought_by IS NULL", (list_id,))
            conn.commit()
            print(f"Список {list_id} очищен, удалено {count} товаров")
            return count
        except Exception as e:
            print(f"Ошибка очистки списка: {e}")
            return 0
        finally:
            conn.close()

    def get_purchase_history(self, list_id):
        if not self.is_logged_in():
            return []

        conn = self.get_connection()
        if not conn: return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ph.product_name, ph.category, u.username, ph.bought_date
                FROM purchase_history ph
                LEFT JOIN users u ON ph.bought_by = u.id
                WHERE ph.list_id = ?
                ORDER BY ph.bought_date DESC
            ''', (list_id,))
            history = cursor.fetchall()
            print(f"Найдено {len(history)} записей в истории покупок")
            return history
        except Exception as e:
            print(f"Ошибка получения истории: {e}")
            return []
        finally:
            conn.close()

    def get_smart_suggestions(self, list_id):
        if not self.is_logged_in():
            return []

        conn = self.get_connection()
        if not conn: return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT product_name, COUNT(*) as count 
                FROM purchase_history 
                WHERE list_id = ?
                GROUP BY product_name 
                ORDER BY count DESC 
                LIMIT 5
            ''', (list_id,))
            suggestions = cursor.fetchall()
            print(f"Найдено {len(suggestions)} предложений")
            return suggestions
        except Exception as e:
            print(f"Ошибка получения предложений: {e}")
            return []
        finally:
            conn.close()

    def add_suggestion_to_list(self, list_id, product_name):
        return self.add_product(list_id, product_name)

    def get_last_purchased_product(self, list_id):
        if not self.is_logged_in():
            return None

        conn = self.get_connection()
        if not conn: return None

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT product_name 
                FROM purchase_history 
                WHERE list_id = ? 
                ORDER BY bought_date DESC 
                LIMIT 1
            ''', (list_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Ошибка получения последнего товара: {e}")
            return None
        finally:
            conn.close()

    def leave_shopping_list(self, list_id):
        if not self.is_logged_in():
            return False

        conn = self.get_connection()
        if not conn: return False

        try:
            cursor = conn.cursor()

            # Удаляем пользователя из участников
            cursor.execute(
                "DELETE FROM list_members WHERE list_id = ? AND user_id = ?",
                (list_id, self.current_user_id)
            )

            # Если пользователь был владельцем, передаем владение другому участнику
            cursor.execute("SELECT owner_id FROM shopping_lists WHERE id = ?", (list_id,))
            owner_id = cursor.fetchone()[0]

            if owner_id == self.current_user_id:
                # Находим другого участника
                cursor.execute(
                    "SELECT user_id FROM list_members WHERE list_id = ? AND user_id != ? LIMIT 1",
                    (list_id, self.current_user_id)
                )
                new_owner = cursor.fetchone()

                if new_owner:
                    cursor.execute(
                        "UPDATE shopping_lists SET owner_id = ? WHERE id = ?",
                        (new_owner[0], list_id)
                    )
                    print(f"Владелец списка {list_id} изменен на {new_owner[0]}")
                else:
                    # Если участников больше нет, удаляем список
                    cursor.execute("DELETE FROM shopping_lists WHERE id = ?", (list_id,))
                    print(f"Список {list_id} удален (нет участников)")

            conn.commit()
            print(f"Пользователь покинул список {list_id}")
            return True
        except Exception as e:
            print(f"Ошибка выхода из списка: {e}")
            return False
        finally:
            conn.close()

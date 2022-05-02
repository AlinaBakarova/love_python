import sqlite3

class FDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addUser(self, name, psw, a, b, c):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE handle LIKE '{name}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким handle уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?)", (name, psw, a, b, c))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    def addFriend(self, name, user):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE handle = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            f = res['friends']
            if user not in f:
                f = f + " " + user

            data = (f, {name})

            self.__cur.execute(f"UPDATE users SET friends = ? WHERE handle = ?", (f, name))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    '''
    def toMessage(self, name, komu, num):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE handle = ? LIMIT 1", name)
            res = self.__cur.fetchone()
            f = res['to_friend']
            if num == 1:
                f = f + " :)"
            elif num == 2:
                f = f + " :("
            elif num == 3:
                f = f + " ^_^"

            data = (f, {name})

            self.__cur.execute(f"UPDATE users SET to_friend = ? WHERE handle = ?", (f, name))





            self.__cur.execute(f"SELECT * FROM users WHERE handle = ? LIMIT 1", komu)
            res2 = self.__cur.fetchone()
            f2 = res2['from_friend']
            if num == 1:
                f = f + " :)"
            elif num == 2:
                f = f + " :("
            elif num == 3:
                f = f + " ^_^"

            data = (f2, {komu})

            self.__cur.execute(f"UPDATE users SET from_friend = ? WHERE handle = ?", (f2, komu))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    '''

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получания данных из БД" + str(e))

        return False

    def getUserByName(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE handle = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получания данных из БД" + str(e))

        return False
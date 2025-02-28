from .entities.User import User

class ModelUser():

    @classmethod
    def login(cls, db, user):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT * FROM user WHERE email = %s'

            cursor.execute(sql, (user.email,))
            row = cursor.fetchone()
            if row:
                id = row[0]
                email = row[1]
                password = User.check_password(row[3], user.password)
                username = row[2]

                user = User(id, email, password, username)

                return user
            else:
                return None

        except Exception as e:

            raise Exception(e)


    @classmethod
    def get_by_id(cls, db, id):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, email, username FROM user WHERE id = %s'

            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                email = row[1]
                username = row[2]

                logged_user = User(id, email, None, username)

                return logged_user
            else:
                return None

        except Exception as e:

            raise Exception(e)
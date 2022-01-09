from flask_mysqldb import MySQL

class DBHelper:
    db = MySQL()

    @staticmethod
    def init_app(application):
        DBHelper.db.init_app(application)

    @staticmethod
    def run_query(query):
        cursor = DBHelper.db.connection.cursor()
        cursor.execute(f'''{query}''')
        DBHelper.db.connection.commit()
        response = cursor.fetchall()
        cursor.close()

        if response != None:
            return response
        return None
from dbseeder import database

def main():
    db = database.Database(host="localhost", user="root", password="password", database="seed")
    # db.makeSeed(rows_num=100)
    db.clearAndMakeSeed(rows_num=100)

if __name__ == "__main__":
    main()
import mysql.connector


def connect_dataBase():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="anis")
        mycursor = mydb.cursor()
        #query =" SELECT name FROM persons"
        name = ("Khalil Kasbi", )
        query = ("INSERT INTO  persons (name) VALUES (%s)")
        mycursor.execute(query,name)
            
        mydb.commit()
            
       
      
       
        
def main():
    connect_dataBase();
        
if __name__=="__main__":
    main()
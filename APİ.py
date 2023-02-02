import requests
import mysql.connector
# Mock dosyalarından yanıtları almak için kullanılan kısım
response1 = requests.get('http://www.mocky.io/v2/5d47f24c330000623fa3ebfa')
response2 = requests.get('http://www.mocky.io/v2/5d47f235330000623fa3ebf7')
list1 = response1.json()
list2 = response2.json()
# Mock yanıtlarını rahat kullanabilmek için liste haline çeviriliyor
newlist = []
for i in list1:
    if "zorluk" in i:
        zorluk = i["zorluk"]
    else:
        zorluk = -1
    if "sure" in i:
        sure = i["sure"]
    else:
        sure = -1
    if "id" in i:
        id = i["id"]
    else:
        id = ""
    dict1 = {
        'TaskZorluk' : zorluk,
        'TaskSure'   : sure,
        'TaskID'     : id
    }
    newlist.append(dict1)
temp = 0
for i in list2:
    if "level" in i['Business Task '+ str(temp)]:
        zorluk = i['Business Task '+ str(temp)]['level']
    else:
        zorluk = -1
    if "estimated_duration" in i['Business Task '+ str(temp)]:
        sure = i['Business Task '+ str(temp)]["estimated_duration"]
    else:
        sure = -1

    dict2 = {
        'TaskZorluk' : zorluk,
        'TaskSure'   : sure,
        'TaskID'     : "Business Task " +str(temp)
    }
    temp = temp + 1
    newlist.append(dict2)

# DB bağlantısı ile listler local bir DB'e  atılıyor
localdb= mysql.connector.connect(
    host='localhost',
    user='root',
    password='umut1234',
    port='3306',
    database='todotask',
)
mycursor = localdb.cursor()
sql= "INSERT INTO tasks (TaskID,TaskZorluk,TaskSure) VALUES (%s,%s,%s)"
values=[]
for i in newlist:
    val=(
     i['TaskID'],
     i['TaskZorluk'],
     i['TaskSure'],
    )
    values.append(val)
mycursor.executemany(sql,values)
localdb.commit()
mycursor.close()
localdb.close()

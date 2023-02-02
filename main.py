from flask import Flask, render_template, request
import mysql.connector

# Verileri almak için DB bağlantısı kullanılıyor
localdb= mysql.connector.connect(
    host='localhost',
    user='root',
    password='umut1234',
    port='3306',
    database='todotask',
)
app = Flask(__name__)

@app.route("/",methods =["GET", "POST"])
def Page():
    xtemp=0
    dev1list= []    # DB'den toplu halde gelen verileri developerların zorluk derecelerine göre paylaştırmak için oluşturulmuş listeler
    dev2list = []
    dev3list = []
    dev4list = []
    dev5list = []
    mycursor = localdb.cursor()
    mycursor.execute("SELECT * FROM tasks ORDER BY TaskZorluk ASC,TaskSure DESC")
    data = mycursor.fetchall()
    mycursor.close()
    for i in data:
        if data[xtemp][1] == 1:
            dev1list.append(data[xtemp])
        if data[xtemp][1] == 2:
            dev2list.append(data[xtemp])
        if data[xtemp][1] == 3:
            dev3list.append(data[xtemp])
        if data[xtemp][1] == 4:
            dev4list.append(data[xtemp])
        if data[xtemp][1] == 5:
            dev5list.append(data[xtemp])
        xtemp=xtemp+1
    Dev1week = devcalculate(dev1list)
    Dev2week = devcalculate(dev2list)
    Dev3week = devcalculate(dev3list)
    Dev4week = devcalculate(dev4list)
    Dev5week = devcalculate(dev5list)
    headings = ("Task ID","Zorluk","Sure")
    return render_template("MainPage.html",Dev1week=Dev1week,Dev2week=Dev2week,Dev3week=Dev3week,Dev4week=Dev4week,Dev5week=Dev5week,headings=headings)

# Haftalık 45 saat çalışma kısıtlamasının sağlandığı fonksiyon
# Temelde 3 Koşul üzerinden ilerlemektedir ve büyükten küçüğe olan istenin başından taskları toplayarak devam eder
# Koşul 1:  Task toplamı haftalık çalışma süresini geçmemişse bir sonrakini toplamak üzere devam eder
# Koşul 2:  Task toplamı haftalık çalışma sürenine eşitse yeni haftaya geçer ve toplamı 0'lar
# Koşul 3:  Yeni eklenecek değerle task toplamı haftalık çalışma süresini geçiyorsa onun yerine alternatifleri aradığı kısım
def devcalculate(devlist):
    weekly = 45     # haftalık 45 saat çalışmanın sabiti
    week = []       # haftanın genel akışını göz alarak oluşturulan yeni developer listesi
    toplam = 0      # weekly değişkeni ile 45 saat kıyaslaması yapılan aratoplam değişkeni
    toplamSaat = 0  # hafta boyunca kaç saat çalışıldığının hesaplandığı değişken
    weekcount=("---","week","---")
    for i in devlist:
        toplamSaat += i[2]
    print(toplamSaat)
    for i in devlist:
        if toplam+i[2] < weekly:
            toplam += i[2]
            week.append(i)
            continue
        if toplam+i[2] == weekly:
            week.append(i)
            week.append(weekcount)
            toplam = 0
        if toplam+i[2] > weekly:
            temp =  weekly - toplam
            for y in devlist:
                if y[2] == temp:
                    toplam += y[2]
                    week.append(y)
                    week.append(weekcount)
                    devlist.remove(y)
                    toplam = 0
                    week.append(i)
                    toplam += i[2]
                    break
            if toplam+i[2] > weekly:
                week.append(weekcount)
                toplam = 0
                week.append(i)
                toplam += i[2]
    toplamval={"Toplam Task Suresi",
               toplamSaat,
    }
    week.append(toplamval)
    return week

if __name__ == '__main__':
 app.run()

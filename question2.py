import os
import random
import sqlite3

from pyrogram import filters, Client

bot_ = Client("Question_Bot___", api_id=000000, api_hash="",
              bot_token="")

folder_path = {'/starttestaz': ['Az-Dili', 'Az-Dili Cavablar', 'Az_Dili'],
               '/starttestmath': ['Math', 'Math Cavablar', 'Math'],
               '/starttesteng': ['Eng', 'Eng Cavablar', 'English']}


open_share = False
@bot_.on_message(filters.text & filters.private)
def writing_bot(bot, msg):
    global open_share
    database = sqlite3.connect("database.db")
  
    if msg.from_user.id == 5420622167 and msg.text == '/close':
        open_share = False
        msg.reply("Bu özəllik bağlandı.")
        return
    elif msg.from_user.id == 5420622167 and msg.text == "/openshareinfo":
        msg.reply("Userlərə göndərəcəyin mesajı yaz.")
        open_share = True
    elif open_share and msg.from_user.id == 5420622167:
        for i in database.execute("SELECT UserId FROM Users").fetchall()[0]:
            bot.send_message(i,msg.text)
        msg.reply("Mesaj göndərildi.")
        open_share = False
    elif database.execute(F"SELECT * FROM Waiting_Answer WHERE UserId = {msg.from_user.id}").fetchone() is not None:
        if database.execute(f"SELECT TrueandFalse FROM Waiting_Answer WHERE UserId = {msg.from_user.id}").fetchone()[
            0] == 1:
            if msg.text == '/giveanswer':
                msg.reply("Bu əmri bir dəfə işlətmisən. İndi isə cavabları göndər")
                return
            msg.reply("Cavabın qeydə alındı.")
            answer_ = ""
            with open(database.execute(F"SELECT Answer FROM Answer WHERE UserId = '{msg.from_user.id}'").fetchone()[0],
                      'r', encoding='utf-8') as f: 
                for i in f:
                    answer_ += i.lower()
            answer = answer_.split()
            your_answer = msg.text.lower().split()
            result = ["", ""]
            c = []
            try:
                for q in your_answer:
                    c.append(int(q[:q.index(".")]))
                for i in range(1, 11):
                    if not i in c:
                        your_answer.append(f"{i}.-")
                your_answer = sorted(your_answer)
                your_answer.insert(len(your_answer), your_answer[1])
                your_answer.remove(your_answer[1])
                for i in range(0, len(your_answer)):
                    if your_answer[i] == answer[i]:
                        result[0] += (answer[i][:answer[i].index('.')] + " ")
                    else:
                        result[1] += (answer[i][:answer[i].index('.')] + " ")
            except:
                msg.reply(
                    "Cavabları yoxlayanda problem yarandı. Cavabları yenidən düzgün göndər. Nöqtələrə də fikir ver.")
                return  
            msg.reply("Cavablar:\n" + answer_.upper())
            msg.reply(f"Düzlərin: {result[0]}\n"
                      f"Səhvlərin: {result[1]}")
            msg.reply(
                f"""Düzlərinin sayı: {len(result[0].split(' ')) - 1}\nSəhvlərin sayı:{len(result[1].split(' ')) - 1}""")
            database.execute(
                F"DELETE FROM Answer WHERE UserId = '{msg.from_user.id}'")  
            if database.execute(f"SELECT * FROM UserLuck WHERE UserId LIKE '{msg.from_user.id}%'").fetchone() is None:
                database.execute(
                    F"INSERT INTO UserLuck VALUES('{msg.from_user.id}','1','{len(result[0].split(' ')) - 1}','{len(result[1].split(' ')) - 1}')")
            else:
                db_answer = database.execute(
                    F"SELECT TestLength,TrueVariant,FalseVariant FROM UserLuck WHERE UserId LIKE '{msg.from_user.id}'").fetchone()
                database.execute(
                    F"UPDATE UserLuck SET  TestLength = {db_answer[0] + 1} WHERE UserId LIKE '{msg.from_user.id}%'")
                database.execute(
                    F"UPDATE UserLuck SET  TrueVariant = {db_answer[1] + len(result[0].split(' ')) - 1} WHERE UserId LIKE '{msg.from_user.id}%'")
                database.execute(
                    F"UPDATE UserLuck SET  FalseVariant = {db_answer[2] + len(result[1].split(' ')) - 1} WHERE UserId LIKE '{msg.from_user.id}%'")
            if "@"+msg.from_user.username != \
                    database.execute(f"SELECT UserName FROM Users WHERE UserId LIKE '{msg.from_user.id}%'").fetchone()[
                        0]:
                database.execute(
                    f"UPDATE Users SET UserName = '@{msg.from_user.username}' WHERE UserId LIKE '{msg.from_user.id}%'")
            database.execute(f"DELETE FROM Waiting_Answer WHERE UserId = '{msg.from_user.id}'")

    elif msg.text == '/start':
        if database.execute(f"SELECT UserId FROM Users WHERE UserId Like '{msg.chat.id}%'").fetchone() is None:
            database.execute(
                F"INSERT INTO Users VALUES('@{msg.from_user.username}','{msg.from_user.first_name}','{msg.from_user.last_name}','{msg.chat.id}')")
        if msg.from_user.username is not None:
            full_name = "@" + msg.from_user.username
            database.execute(
                f"UPDATE Users SET UserName='@{msg.from_user.username}'  WHERE UserId LIKE '{msg.from_user.id}%'")
        else:
            full_name = msg.from_user.first_name
            if msg.from_user.last_name is not None:
                full_name += " " + msg.from_user.last_name
            database.execute(
                f"UPDATE Users SET UserName='@{msg.from_user.username}'  WHERE UserId LIKE '{msg.from_user.id}%'")
            database.execute(
                f"UPDATE Users SET FirstName='{msg.from_user.first_name}'  WHERE UserId LIKE '{msg.from_user.id}%'")
            database.execute(
                f"UPDATE Users SET Surname='{msg.from_user.last_name}'  WHERE UserId LIKE '{msg.from_user.id}%'")
        msg.reply(f"Salam {full_name}. Məndən testlər işləmək üçün yaralana bilərsən. Ətraflı məlumat üçün:\n"
                  f"/help yaz.")

    elif msg.text == '/lookatdb' and msg.from_user.id == 5420622167:
        users_ = ""
        a = database.execute("SELECT * FROM Users").fetchall()
        for i in a:
            users_ += F"Username: {i[0]}, Ad: {i[1]}, Soyad: {i[2]},UserId: {i[3]}\n"
        msg.reply("Users:\n"
                  f"{users_}")
        users_luck = ""
        a = database.execute("SELECT * FROM UserLuck").fetchall()
        for k in a:
            users_luck += f"Userİd: {k[0]}, Test sayı: {k[1]}, Doğru cavablar sayı:{k[2]}, Səhv cavabların sayı:{k[3]}\n"
        msg.reply("UsersLuck:\n"
                  f"{users_luck}")
        msg.reply("Teslərin sayı:\n"
                  f"Az-Dili: {len(os.listdir('Az-Dili'))} test\n"
                  f"Riyaziyyat: {len(os.listdir('Math'))} test\n"
                  f"Ingilis: {len(os.listdir('Eng'))} test")
    elif msg.text == '/help':
        if msg.from_user.id == 5420622167:
            msg.reply("Əmrlərim:\n"
                      "/start - Botun işləyib-işləmədiyini yoxlayar.\n"
                      "/starttestaz - Bu əmr Azərbaycan dili testinə başlamaq üçündür.\n"
                      "/starttestmath - Bu əmr Riyaziyyat testinə başlamaq üçündür.\n"
                      "/starttesteng - Bu əmr İngilis dili testinə başlamaq üçündür.\n"
                      "/giveanswer - Bu əmr ilə siz testin cavablarını bota göndərirsiniz. Və bot cavabları yoxlayır.\n"
                      "/myluck - Bu əmr ilə etdiyin test sayını və düzlər və səhvləri görə bilərsiniz.\n"
                      "/about - Bot haqqında məlumata baxa bilərsiniz.\n"
                      "/lookatdb - Database oxumaq üçündür.\n"
                      "/openshareinfo - Botun İstifadəçilərinə mesaj göndərmə özəlliyini açır.\n"
                      "/close - Botun İstifadəçilərinə mesaj göndərmə özəlliyini bağlayır.")
        else:
            msg.reply("Əmrlərim:\n"
                      "/start - Botun işləyib-işləmədiyini yoxlayar.\n"
                      "/starttestaz - Bu əmr Azərbaycan dili testinə başlamaq üçündür.\n"
                      "/starttestmath - Bu əmr Riyaziyyat testinə başlamaq üçündür.\n"
                      "/starttesteng - Bu əmr İngilis dili testinə başlamaq üçündür.\n"
                      "/giveanswer - Bu əmr ilə siz testin cavablarını bota göndərirsiniz. Və bot cavabları yoxlayır.\n"
                      "/myluck - Bu əmr ilə etdiyin test sayını və düzlər və səhvləri görə bilərsiniz.\n Bu hər aydan bir sıfırlanır."
                      "/about - Bot haqqında məlumata baxa bilərsiniz.\n"
                      "")
    elif msg.text == '/about':
        msg.reply("Programming language: Python\n"
                  "Bot owner: @codejavascript\n"
                  "Əlaqə üçün @codejavascript - ə yaza bilərsiniz.")

    elif msg.text == '/giveanswer':
        if database.execute(F"SELECT * FROM Answer WHERE UserId = '{msg.from_user.id}'").fetchone() is not None:
            msg.reply("Cavabları mənə bu formatda at.\n"
                      "1.a 2.b. Hər bir cavabdan sonra boşluq işarəsi qoyun. Və hər bir sualın nömrəsindən sonra '.' işarəsi qoyun.\n"
                      "Əgər yazılanları etməsəniz yoxlanış zamanı problemlərə rast gələ bilərsiniz.")
            msg.reply('Cavabları yaz.Sonra mənə göndər.')
            database.execute(f"INSERT INTO Waiting_Answer VALUES('{msg.from_user.id}','1')")
        else:
            msg.reply("Sən bu dəqiqə test etmirsən.")
    elif msg.text == '/myluck':
        db_ = database.execute(
            f"SELECT TestLength, TrueVariant, FalseVariant FROM UserLuck WHERE UserId LIKE '{msg.from_user.id}%'").fetchone()
        msg.reply("Sənin nəticələrin:\n"
                  f"Cəmi test sayı:{db_[0]}\n"
                  f"Cəmi düzgün cavablar: {db_[1]}\n"
                  f"Cəmi səhv cavablar: {db_[2]}")
    if database.execute(f"SELECT * FROM Answer WHERE UserId='{msg.from_user.id}'").fetchone() is None:
        if msg.text in folder_path.keys():
            if len(database.execute(
                    F"SELECT Test_Name FROM {folder_path[msg.text][2]} WHERE UserId Like '{msg.from_user.id}%'").fetchall()) < len(
               os.listdir(folder_path[msg.text][0])):
                tests_ = os.listdir(folder_path[msg.text][0])
                for i in database.execute(
                        F"SELECT Test_Name FROM {folder_path[msg.text][2]} WHERE UserId LIKE '{msg.from_user.id}'").fetchall():
                    tests_.remove(i[0].split('/')[1])
               
                test = folder_path[msg.text][0] + "/" + random.choice(tests_)
                database.execute(f"INSERT INTO {folder_path[msg.text][2]} VALUES('{msg.from_user.id}','{test}')")
                if test.endswith(".png") or test.endswith(".jpg"):
                        bot.send_photo(msg.chat.id, photo=open(test, 'rb'))
                else:
                        with open(test, "r", encoding="utf-8") as d:
                            msg.reply(d.read())
                
                a="/cavablar"+test[test.index('s')+2:test.index('.')]+'.txt'
                database.execute(
                    F"INSERT INTO Answer VALUES('{msg.from_user.id}','{folder_path[msg.text][1] + a }')")
                msg.reply(
                    "Testi et. Qeyd: Testi qurtarmamış /starttestaz,/starttestmath,/starttesteng əmrlərini işlədə bilməzsən. İşlətsən belə bu əmrlər işləməyəcək.Cavabları yolatmaq üçün /giveanswer yaz.")
            else:    
             msg.reply(
                    f"Sən {len(os.listdir(folder_path[msg.text][0]))} testin {len(os.listdir(folder_path[msg.text][0]))}-da bitirmisən.")

    database.commit()


print("Online")
bot_.run()

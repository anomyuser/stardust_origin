from asyncio.log import logger
import pymysql as sql, random, numpy as np, discord, stardust as sd, os


#DB연결
conn = sql.connect(
    host=(os.getenv("localhost")),
    user=(os.getenv("user")), 
    password=(os.getenv("pass")),
    charset='utf8',
    autocommit=True)
cur = conn.cursor() #구문 실행용 커서

#___init___
def init():
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS mydb")
        cur.execute("use mydb")
        cur.execute(sd.createTbluser)
        cur.execute(sd.createTblfood)
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        conn.commit()

    '''try:
        if (cur.execute("select count(*) from user") < 0):
            cur.execute(sd.guestlist)
            conn.commit()
            print("유저 테이블 생성 완료")
        #return 'Success'
    except: 
        print("user table exception")
        print(Exception)
        return 'Fail'
    try:
        if (cur.execute("select count(*) from food") < 0):
            cur.execute(sd.foodlist)
            conn.commit()
            print("음식 테이블 생성 완료")
        #return 'Success'
    except:
        print("food table exception")
        print(Exception)
        return 'Fail' '''
    return None

#정해진 시간에 작업 (아침 7시 술 깸)
def job():
    try : 
        print("도수 리셋")
        cur.execute("set sql_safe_updates=0;")
        cur.execute("update user set achol=0")
        conn.commit()
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        conn.commit()

def tbdel(name):
    try:
        cur.execute("drop table ?", (name,))
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        conn.commit()

def adduser(ctx,id,name,roomnum):
    cur = conn.cursor()
    global cnt
    cnt = 1
    null = 'NULL'
    id = repr(id)
    check = user_check(id) #유저가 기존에 존재하는지 확인
    if roomnum == 0 : 
        roomnum = int(000 + cnt)
        cnt = cnt+1
    rcheck = getaRoom(id, roomnum)
    if check == 0 & rcheck == 0:
        try:
            cur.execute(f"insert into user values ('{id}','{name}',0,0,{null},{roomnum})")
            print("유저추가완료")
            embed = discord.Embed(title = ':wave: 등록', description = "호텔 스타더스트에 방문하신 것을 환영합니다, %s님. \n방명록에 이름이 적혔습니다. \n이미 객실이 있으시다면 편히 쉬시고, 아직 객실을 배정받지 못하셨다면 공지를 확인해주세요." %name, color = sd.green)
            embed.set_footer(text = f"{sd.nick(ctx)}")
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/1298120779967238187/1298250323890016266/-.png?ex=6718e155&is=67178fd5&hm=e8d4f1c1629dd83a45ce005871a98e499c729dabac855b709a0af4cd3bb25a8a&=&format=webp&quality=lossless')
        except Exception as e:
            logger.error("=============")
            logger.error(e)
            logger.exception(e)
            embed = discord.Embed(title = ':x: 오류', description = '이런! 죄송합니다. 아직 명부를 받아오지 못했습니다.\n걱정마세요, 지배인이 금방 가져올 거예요.\n{ctx.message.author.mention}', color=discord.Color.red())
        finally :
            conn.commit()
            cur.close()
            conn.close()
            return embed           
        
    elif check == 1 :
        embed = discord.Embed(title = ':x: 중복', description = '죄송하지만, 손님은 이미 방명록에 이름이 등록되어 있습니다.', color=discord.Color.red())
        embed.set_footer(text = f"{sd.nick(ctx)}")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/1298120779967238187/1298250323890016266/-.png?ex=6718e155&is=67178fd5&hm=e8d4f1c1629dd83a45ce005871a98e499c729dabac855b709a0af4cd3bb25a8a&=&format=webp&quality=lossless')
    elif rcheck == 1 :
        embed = discord.Embed(title = ':x: 중복', description = '이런! 선택한 호실이 이미 예약되었습니다.\n 다시 예약을 도와드리겠습니다.', color=discord.Color.red())
        embed.set_footer(text = f"{sd.nick(ctx)}")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/1298120779967238187/1298250323890016266/-.png?ex=6718e155&is=67178fd5&hm=e8d4f1c1629dd83a45ce005871a98e499c729dabac855b709a0af4cd3bb25a8a&=&format=webp&quality=lossless')
    return embed

def getaRoom(id, rnum):
    try :
        alr_exist = []
        print("room Number 중복체크중")
        cur.execute("SELECT roomnum FROM user WHERE userid = %s" %id)
        rows = cur.fetchall() #위에서 필터링한 num 저장
        #정보가 들어있다면 리스트에 num이 포함되어 있을 것이다.
        for i in rows :
            alr_exist.append(i[0])
            print("리스트 체크중..")
        if rnum not in alr_exist :
            print("존재하지 않음.")
            return 0
        elif rnum in alr_exist :
            print("존재함.")
            return 1
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        conn.close()

def deluser(id):
    try:
        cur.execute("delete from user where userid =%s" %id)
        return 'Success'
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
        return 'Fail'
    finally :
        conn.commit()
        conn.close()
    
#유저정보 조회 함수
def user_check(id):
    try:
        id = str(id)
        alr_exist = []
        print("userid 중복체크중")
        cur.execute("SELECT userid FROM user WHERE userid = %s" %id)
        rows = cur.fetchall() #위에서 필터링한 id 저장
        #회원정보가 들어있다면 리스트에 id가 포함되어 있을 것이다.
        for i in rows :
            alr_exist.append(i[0])
            print("리스트 체크중..")
        if id not in alr_exist :
            print("존재하지 않음.")
            return 0
        elif id in alr_exist :
            print("존재함.")
            return 1
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        conn.commit()
    
def seluser(id):
    try:
        if user_check(id) == 0:
            return 'Fail'
        cur.execute("select name, achol, coin, desct, roomnum from user where userid=%s" %id,)
        row = cur.fetchone()
        print("유저조회완료")
        return row
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
        return 'Fail'
    finally :
        conn.commit()
    
#유저정보 수정 함수
def moduser(id, *args):

    cur = conn.cursor()
    try:
        name = args[name]
        desc = args[desc]
        """for value in args:
            arr = value"""
        #다시확인중!!
        if  name != 'name' and desc == 'desc':
            cur.execute("update user set name=%s where userid=%s" %name, id)
            conn.commit()
        if desc != 'desc' and name == 'name':
            cur.execute("update user set desct=%s where userid=%s" %desc, id,)
            conn.commit()
        '''if roomnum != roomnum:
            cur.execute("update user set roomnum=? where userid=?", (roomnum, id,))'''
        print("유저정보수정완료")
        return 'Success'
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
        return 'Fail'
    finally :
        conn.commit()
        cur.close()
        conn.close()

def menuChoice(tbl):
    cur = conn.cursor()
    try:
        if tbl == 1: #음식인 경우
            menuarr = [cur.execute("select * from food where f_group = 'food'")]
        elif tbl == 2: #음료인 경우
            menuarr = [cur.execute("select * from food where f_group = 'drink'")]
        elif tbl == 3: #바텐더 호출
            menuarr = [cur.execute("select * from food where f_group = 'achol'")]
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        conn.commit()
        cur.close()
        conn.close()
        return menuarr

def modAchol(id, achol): #알콜도수 합산 함수, name char(20) achol int)
    cur = conn.cursor()
    hvachol = cur.execute("select achol from user where userid=%s" %id,)
    sum = hvachol+achol
    try:
        cur.execute("update user set achol=? where userid=%s" %id,)
        return sum
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
        return 0
    finally :
        conn.commit()
        cur.close()
        conn.close()

#코인관리

def checkCoin(id):
    try:
        cur = conn.cursor()
        name, mycoin = cur.execute("select name, coin from user where userid=%s" %id,)
        return name, mycoin
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
        return None
    finally :
        conn.commit()
        cur.close()
        conn.close()
    

def modCoin(id, coin):
    try:
        #코인 합산
        cur = conn.cursor()
        ck = checkCoin(id)
        name = ck['name']
        mycoin = ck['mycoin']
        if name is None:
            return Exception
        
        sumcoin = coin + mycoin
        cur.execute(f"update user set coin = {sumcoin} where userid={id}")
        print(f"코인 합산 완료: 원래 가지고 있던 코인 {mycoin}\n 이번에 획득한 코인 : {coin}")
        embed = discord.Embed(title = ':coin:', description = f"{name} 고객님의 현재 소지금:{sumcoin}", color = 0xffc0cb)
        embed.set_footer(text = f"코인 변동 : {sumcoin} - {mycoin} = {sumcoin-mycoin}")
        return embed
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
        print("=============")
        print("코인수정실패")
        embed = discord.Embed(title = ':x:', description = f"{name} 고객님의 현재 소지금:{sumcoin}", color = 0xffc0cb)
        embed.set_footer(text = "코인 업데이트에 실패했습니다. 무슨 일일까요? \n지배인이 곧 해결해줄 거에요.")
        return embed
    finally :
        conn.commit()
        cur.close()
        conn.close()
'''
def closeDb():
    cur.close()
    conn.close()
'''
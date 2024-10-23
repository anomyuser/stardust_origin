'''
import discord, random, numpy as np, dbconnect, asyncio, stardust as sd, os #,schedule, time
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("token")
#serverId = os.getenv("serverId")
intents=discord.Intents.default()
client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='~', intents=intents)
#bot = interactions.Client(TOKEN, default_scope=serverId)
class aclient(discord.Client):
    def __init__(self):
         super().__init__(intents=discord.Intents.all())
         self.synced = False
    async def on_ready(self):
         await self.wait_until_ready()
         if not self.synced: 
             self.synced = True

@tree.command(name='hello', description="봇이 'Hello!'를 출력합니다.", scope=serverId)
async def slash(interaction: discord.Interaction):
     await interaction.response.send_message("Hello!", ephemeral=False)



'''
from asyncio.log import logger
import discord, random, numpy as np, dbconnect, asyncio, stardust as sd, os #,schedule, time
from dotenv import load_dotenv
from discord.ext import commands

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = discord.Client(intents=discord.Intents.all())
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv("token")

'''

@bot.event
async def on_ready():
        await tree.sync()
'''
#intents=discord.Intents.default()
intents.message_content = True
#client = discord.client


@bot.event
async def on_ready():#봇이 로딩되었거나 재로딩 되는 경우 실행되는 이벤트 / 봇 상태 변경
    
    online = discord.Activity()
    await bot.change_presence(status=discord.Status.online, activity=online)
    dbconnect.init()
    print("가동 완료")

#관리자용 메뉴
@bot.command(name="퇴근")
async def bye(ctx):
    # 봇 상태 변경
    online = discord.Activity()
    await bot.change_presence(status=discord.Status.offline)
    print("봇 상태 변경:오프라인")
    try:
        close(ctx)
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    print("작동 중지")

@bot.command(name="dbclose")
async def close(ctx):
    dbconnect.cur.close()
    dbconnect.conn.close()

@bot.command(name="세팅")
async def setting(ctx):
    try:
        yn = dbconnect.init()
        await ctx.channel.send("기본 세팅이 완료되었어요!")
    except Exception as e:
        await ctx.channel.send("기본 세팅에 실패했어요.")
        logger.error("=============")
        logger.error(e)
        logger.exception(e)

@bot.command(name="테이블삭제")
async def delete_table(ctx, tbname):
    try:
        dbconnect.tbdel()
    except Exception as e:
        await ctx.channel.send("테이블 삭제에 실패했어요.")
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        dbconnect.conn.commit()
        dbconnect.cur.close()
        dbconnect.conn.close()
        return None

@bot.command(name="유저삭제")
async def delete_user(ctx, id):
    try:  
        dbconnect.deluser(id)
        await ctx.channel.send("유저 삭제가 완료되었어요!")
    except Exception as e:
        await ctx.channel.send("유저 삭제에 실패했어요.")
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    finally :
        dbconnect.conn.commit()
        dbconnect.cur.close()
        dbconnect.conn.close()

#유저 컨택스트 메뉴
'''
@tree.command(name='체크인', description='고객님의 숙박 정보를 등록합니다.')
@app_commands.describe(name='이름', roomnum = '방번호')'''

@bot.command(aliases=["체크인", "등록", "가입", "숙박"])
async def checkin(ctx, roomnum=0):
      print("체크인함수들어옴")
      #id = sd.id(ctx)
      id = sd.id(ctx)
      #서버닉네임에서 [] 안의 문자열만 추출함
      name = (sd.nick(ctx).split('[')[1]).split(']')[0]
      print(name)
      '''if(roomnum.isdigit() == 0):
        await ctx.channel.send("호실은 숫자 형식으로 입력하세요.")'''
      result = dbconnect.adduser(ctx, id, name, roomnum)
      await ctx.channel.send(embed=result)
      await ctx.channel.send(ctx.message.author.mention)
      
#봇 가동 명령어 (메뉴, 주사위, 도움, 한잔, 청소, 상담)

@bot.command(aliases=['프로필', '내정보', '나', '거울', '정보', '소개'])
async def infoUser(ctx):
    userInfo = []
    if dbconnect.seluser(sd.id(ctx)) == 'Fail':
        await ctx.channel.send("먼저 체크인해주세요.")
        return None
    row = dbconnect.seluser(sd.id(ctx)) #name, achol, coin, desct, roomnum
    print("리스트 체크중..")
    for i in row:
        userInfo.append(i)
    #소개말
    if userInfo[3] == None or userInfo[3] == 'Null':
        desc = '소개말이 없습니다.'
    else : 
        desc = userInfo[3]
    if userInfo[2] == None or userInfo[2] == 'Null':
        coin = '0'
    else : 
        coin = userInfo[2]
    if userInfo[1] == None or userInfo[1] == 'Null':
        achol = '0'
    else : 
        achol = userInfo[1]
    #상태 구현
    if userInfo[1] == None or userInfo[1] == 'Null':
        acolor =sd.green
        status = '오늘은 아직 술을 마신 적이 없습니다.'
    else:
        status, acolor = sd.acholMsg(achol)
    embed=discord.Embed(title = f"{userInfo[0]} 고객님", description = f"{desc}",color=acolor)
    #await message.channel.send(embed=discord.Embed(title="그러세요!", color=discord.Color.blue()))
    #embed.add_field(name='> 칭호', value='업데이트 중입니다')
    embed.add_field(name='> 보유코인', value=f"\t{coin}coin")
    embed.add_field(name='> 체크인 호수', value=f"\tRoom {userInfo[4]}")
    embed.add_field(name='> 혈중 알콜농도', value=f"\t{achol}%")
    embed.set_footer(text = f"{status}")

    await ctx.channel.send(embed=embed)

@bot.command(name='정보수정', description="변경할 내용을 입력하세요.") 
async def modUser(ctx, desc):
    infoUser(ctx)
    name = 'name'
    await ctx.channel.send("현재는 이름과 자기소개만 내용 변경이 가능합니다.\n변경할 내용을 입력하세요. (응답대기시간:30초)")
    async def check(m):#보낸사람과 채널 동일한지 체크
        return m.author == ctx.author and m.channel == ctx.channel
    msg= await bot.wait_for("message", check=check, timeout=30) #입력 기다림
    if (sd.check(ctx, msg)):
        if msg.content == "이름":
            try:
                await ctx.channel.send("변경할 이름을 입력하세요. (취소:q)") 
                #임베드 수정
                name = await bot.wait_for("message", check=check, timeout=30).content
                if name == "q" or name == "\n":
                    await ctx.channel.send("취소되었습니다.")
                    await asyncio.sleep(5)
                    await target.delete()
                    return None
            except asyncio.exceptions.TimeoutError:
                await ctx.channel.send("시간이 초과되었습니다.\n**처음부터 다시 시도하세요.")
            except Exception as e:
                logger.error("=============")
                logger.error(e)
                logger.exception(e)
            return None
        asyncio.sleep(10)
        if msg.content == "자기소개":
            try:
                async def check(m):#보낸사람과 채널 동일한지 체크
                    return m.author == ctx.author and m.channel == ctx.channel
                await ctx.channel.send("변경할 소개글을 입력하세요. (취소:q)")
                desc= await bot.wait_for("message", check=check, timeout=100).content
                if desc == "q" or desc == "\n":
                    target = await ctx.channel.send("취소되었습니다.")
                    await asyncio.sleep(5)
                    await target.delete()
                    return None
            except asyncio.exceptions.TimeoutError:
                await ctx.channel.send("시간이 초과되었습니다.\n다시 시도하세요.")
            except Exception as e:
                logger.error("=============")
                logger.error(e)
                logger.exception(e)
        ''' if msg.content == "방번호":
            try:
            await ctx.channel.send("바꾸실 방을 입력하세요. (취소:q)")
            msg = await bot.wait_for("message", check=check, timeout=100)
            roomnum = msg.content
            if desc == "q":
                await ctx.channel.send("취소되었습니다.")
                return None        
                
            except asyncio.exceptions.TimeoutError:
                await ctx.channel.send("시간이 초과되었습니다.\n**처음부터 다시 시도하세요.")
                '''
        if dbconnect.moduser(sd.id(ctx), name, desc) == 'Success':
            await ctx.channel.send("정보가 업데이트되었습니다.")
            infoUser(ctx)
        else :
            await ctx.channel.send("업데이트에 실패했습니다.\n지배인에게 문의하세요.")
            return None

@bot.command(name='메뉴', description="세계 최고의 셰프가 최고급 요리를 대접합니다.") 
async def 메뉴(ctx):
    '''mainmenu = random.choice(np.concatenate([main]))
    sidemenu = random.choice(np.concatenate([side, side2]))
    drink = random.choice(np.concatenate([drink_alcohol, drink_nonalcohol]))
    '''
    mainmenu = dbconnect.menuChoice(1)
    sidemenu = dbconnect.menuChoice(1)
    drink = dbconnect.menuChoice(2)
    target = await ctx.channel.send("오늘의 메뉴는 .")
    target.edit('오늘의 메뉴는 ..')
    await asyncio.sleep(1)
    target.edit ('오늘의 메뉴는 ...')
    await asyncio.sleep(1)
    target.edit ('오늘의 메뉴는 %s, ' %mainmenu)
    await asyncio.sleep(1)
    target.edit ('오늘의 메뉴는 %s, %s ' %mainmenu, sidemenu)
    await asyncio.sleep(1)
    target.edit ('오늘의 메뉴는 %s, %s, %s ' %mainmenu, sidemenu, drink)
    await asyncio.sleep(1)
    target.edit ('오늘의 메뉴는  %s, %s, %s  입니다.\n맛있게 드십시오.' %mainmenu, sidemenu, drink)
    
    return None

@bot.command(name='주사위', description="승리할 경우 배팅한 금액의 2배를 받습니다.")
#@app_commands.describe(coin='배팅액') 
async def dice(ctx,coin=1000):
    
    if coin < 990:
       await ctx.channel.send("1000 coin 이하로 배팅할 수 없습니다.")        
       return 
    #딜러 주사위
    target = ctx.channel.send(discord.Embed(title = "##주사위게임", description= "배팅한 금액:%s" %coin))
    await ctx.channel.send(embed=embed)
    target.add_field(name='> 진행 : ', value = "딜러가 주사위를 굴립니다.")
    #await ctx.channel.send("딜러가 주사위를 굴립니다.")
    numarr = [i for i in range(1, 6)]
    n1 = random.choice[numarr]
    n2 = random.choice[numarr]
    n3 = random.choice[numarr]
    snum_deal = n1+n2+n3
    target.add_field(name='> 🎲1')
    target
    await asyncio.sleep(1)
    target.add_field(name='> 🎲2')
    target
    await asyncio.sleep(1)
    target.add_field(name='> 🎲3')
    await asyncio.sleep(1)
    target.edit(name='> 🎲1', value = str(n1))
    await asyncio.sleep(5)
    target.edit(name='> 🎲2', value = str(n2))
    await asyncio.sleep(5)
    target.edit(name='> 🎲3', value = str(n3))
    await asyncio.sleep(5)
    
    await ctx.channel.send("```diff\n딜러의 주사위 합계:\n %d\n```" %snum_deal)

    #주사위 굴리는 함수
    target.edit(title = "주사위를 굴려주세요.")
    msg = await ctx.channel.send(embed=target)
    await msg.add_reaction("🎲")

    target.add_field(name='> 🎲1', value = "")
    target.add_field(name='> 🎲2', value = "")
    target.add_field(name='> 🎲3', value = "")
    
    msg = await ctx.channel.send(embed=target)
    await msg.add_reaction("🎲")

    result = sd.on_reaction_add('🎲', sd.id(ctx))
    if result >= 0 :
        await ctx.channel.sand('시간이 초과되었습니다.')
    else :
        await ctx.channel.sand('주사위를 굴렸습니다!')
        numarr = [i for i in range(1, 6)]
        n1 = random.choice[numarr]
        n2 = random.choice[numarr]
        n3 = random.choice[numarr]
        snum_user = n1+n2+n3

        target.edit(name='> 🎲1', value = str(n1))
        await asyncio.sleep(5)
        target.edit(name='> 🎲2', value = str(n2))
        await asyncio.sleep(5)
        target.edit(name='> 🎲3', value = str(n3))
        await asyncio.sleep(5)
        target.add_field(name='> 당신의 주사위 합계', value = snum_user)
        
        if snum_deal > snum_user:
            await ctx.channel.send("```diff\n 졌습니다\n 잃은 코인 : %d\n```" %snum_user)
        elif snum_user > snum_deal:
            await ctx.channel.send("```diff\n 이겼습니다!! \n 얻은 코인 : %d\n```" %snum_user*2)
        else : return
    return None


@bot.command(aliases=['한잔','바텐더','술줘','술','술한잔'],description="술 한 잔을 주문합니다.")
#@tree.command(name='한잔', description="술 한 잔을 주문합니다.") 
async def 바(ctx):
    #drink = random.choice(np.concatenate([sd.drink_alcohol, sd.drink_nonalcohol]))
    drink = dbconnect.menuChoice(2)
    rnd_num = random.randint(1, 10)
    embed = discord.Embed(title = '바텐더', description='당신께 드릴 최고의 한 잔은...')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1298120779967238187/1298194445182701568/-.png?ex=6718ad4b&is=67175bcb&hm=77396cc7fe7c1bb706dd5d038fc531e1cbf29f72d695220c1ad4d75352bd7dea&')
    em = await ctx.channel.send_message(embed=embed)
    await asyncio.sleep(5)
    em.edit(title='바텐더', description="당신께 드릴 최고의 한 잔은...*%s*입니다.\n" %drink)
    
    #알콜합산 구현 필요
    sum = dbconnect.modAchol(sd.id(ctx), rnd_num)
    if sum == 'Fail':
        await ctx.channel.send_message("이런! 실수로 쏟아버리고 말았다...\n바텐더의 표정이 차가워졌다. \n*혈중알콜농도 변화 없음*", ephemeral=False)
        return None
    
    embed.add_field(name='', value='이럴수가, 엄청나게 맛있다!\n조금 취하고 말았다...\n혈중알콜농도 = %d' %sum)
    return None

@bot.command(name='청소', description='요청하신 개수만큼 메세지를 지웁니다.') 
#@app_commands.describe(num='청소할 개수')
async def maid(ctx,num=1):
    if isinstance(num, int) == True:
        await ctx.channel.purge(limit=int(num))
        embed=discord.Embed(
            title="🧹메이드",
            description=(f'청소가 완료되었습니다!\n"**{num}개**의 메시지를 삭제했습니다.\n아휴, 치우느라 힘들어 죽는줄... 핫! \n그, 그럼 쾌적한 하루 보내세요!'))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1298120779967238187/1298184609703661619/-.jpg?ex=6718a422&is=671752a2&hm=13f6184a8fc7649e8468b72d50210b0459a4cfac459b364acf8041a7592a3c37&=&format=webp")
        target = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await target.delete()
    else:
        await ctx.channel.send("올바른 값을 입력해주세요.")

@bot.command(name='상담', description='어려운 일을 결정할 수 있게 조언해 드려요.')
async def teller(ctx):
    #사용자 입력 부분 구현 필요
    embed=discord.Embed(
        title="🔮점쟁이",
        description='저에게 물어보고 싶은 것이 있으시다고 들었습니다.\n제 복채는 비싼 편입니다만....\n오늘만 특별히 공짜로 봐드리죠.\n > 질문이 뭐죠? ')
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1298120779967238187/1298184636655992832/-.jpg?ex=6718a428&is=671752a8&hm=f0f35add174150c60a80a010b445cef093914db13f9b197b1028897cd2b50656&=&format=webp")
    target = await ctx.channel.send(embed=embed)
    await asyncio.sleep(5)
    async def check(m):#보낸사람과 채널 동일한지 체크
        return m.author == ctx.author and m.channel == ctx.channel
    try: 
        msg = await bot.wait_for("message", check=check, timeout=50)
        if (sd.check(ctx, msg)):
            await asyncio.sleep(2)
            jum = await ctx.channel.send(content = f'당신의 고민은 {msg.content} 로군요.')
            await asyncio.sleep(2)
            jum.edit(content = f'잘 보이지 않는군요....')
            await asyncio.sleep(2) 
            jum.edit(content = f'저를 도와 수정구슬을 좀 닦아주시겠습니까?')

            #수정구슬 미니게임   
            async def check(reaction, user):
                return user == msg.author and str(reaction.emoji) == '🔮'
            #클리커게임을 만들고싶엇는데..아직  미구현...
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                
                await bot.wait_for('reaction_add', check=check, timeout=50)
                await asyncio.sleep(2)
                jum.edit(content = f'*점쟁이가 수정구슬을 들여다보았다.*')
                await asyncio.sleep(4)
                jum.edit(content = f'{random.choice(sd.ansArr)}.')
                await asyncio.sleep(3)
                jum.edit(content = f'제가 드릴 수 있는 답은...')
                await asyncio.sleep(1)
                rndNum = random.randrange(1, 13)

                await ctx.channel.send_message(embed=discord.Embed(sd.luckMsg(rndNum, target)))
            except asyncio.TimeoutError:
                #await 
                jum.edit(content = '')
            else:
                #await 
                '''
              if rndNum==1:
            await ctx.channel.send(embed=discord.Embed(title="그러세요!", color=discord.Color.blue()))
        elif rndNum==2:
            await ctx.channel.send(embed=discord.Embed(title="언젠가는.", color=discord.Color.pink()))
        elif rndNum==3:
            await ctx.channel.send(embed=discord.Embed(title="가만히 있으세요.", color=discord.Color.yellow()))
        elif rndNum==4:
            await ctx.channel.send(embed=discord.Embed(title="전혀 아닙니다.", color=discord.Color.red()))
        elif rndNum==5:
            await ctx.channel.send(embed=discord.Embed(title="그건 어려운 일이에요.", color=discord.Color.orange()))
        elif rndNum==6:
            await ctx.channel.send(embed=discord.Embed(title="지금이 바로 그때예요.", color=discord.Color.green()))
        elif rndNum==7:
            await ctx.channel.send(embed=discord.Embed(title="장애물을 잘 헤쳐나가세요.", color=discord.Color.orange()))
        elif rndNum==8:
            await ctx.channel.send(embed=discord.Embed(title="당신은 어떻게 생각하시나요?", color=discord.Color.purple()))
        elif rndNum==9:
            await ctx.channel.send(embed=discord.Embed(title="다시 한 번 말해주세요.", color=discord.Color.purple()))
        elif rndNum==10:
            await ctx.channel.send(embed=discord.Embed(title="뭘 망설이시는 거죠?", color=discord.Color.green()))
        elif rndNum==11:
            await ctx.channel.send(embed=discord.Embed(title="지금은 때가 아니에요", color=discord.Color.yellow()))
        else:
            await ctx.channel.send(embed=discord.Embed(title="아니요.", color=discord.Color.red()))'''
    except Exception as e:
        logger.error("=============")
        logger.error(e)
        logger.exception(e)
    return None

@bot.command(name='도움', description="사용 가능한 명령어를 안내합니다.") 
async def help(ctx):
    # 채널 명령어를 안내합니다
    embed=discord.Embed(title = '##호텔 직원 이용 가이드\n\n', description = '-이렇게 말씀하시면 즉각 안내하겠습니다.\n\n', color=discord.Color.purple())
    embed.add_field(name='', value='\n\n> **🔑\t체크인 (호실) **\n\n\t처음 방문하셨나요? 데스크에서 체크인해주세요. \n~체크인, ~체크인 999)\n\n**> 📃\t프로필, 나, 내정보**\n\t고객님의 정보를 확인합니다. \n추가 명령어: 정보수정\n\n**> 🍴\t메뉴, 식사, 밥줘**\n\t미슐랭 3스타의 우수한 셰프들이 고객님 취향에 딱 맞춘 최고급 메뉴를 요리해드립니다.\n\n**> 🍹\t한잔,바텐더,술줘,술,술한잔**\n\t바텐더가 내주는 그날의 한 잔으로 분위기에 취해보세요.(도수 기능 구현중)\n\n**> 🧹\t청소 (개수)**\n\t채팅방이 어지러우신가요? 숙련된 메이드가 바로 정리해드리겠습니다. \n~청소, ~청소 10 \n\n**> 🔮\t상담**\n\t전세계를 돌며 왕족들의 운명을 점쳤다는 유명한 점술가가 저희 호텔에 묵고 있습니다. \n 궁금한 걸 물어보시면 대답해주실지도 모르겠네요.')
    embed.set_footer(text= '명령어 안내 : 모든 명령어의 앞에는 ~을 붙여 사용합니다.')
    await ctx.channel.send(embed=embed)
'''
async def run():
    async with bot:
        await bot.start(TOKEN, reconnect=True)
'''
bot.run(TOKEN)


'''
@client.event
async def on_error(event, args, kwargs):
	if event == "on_message": #on_message에서 발생했을때 작동합니다.
    message = args[0] #args값에는 여러개가 들어올수도 있으니, 첫번째껏만 잡아줍니다.
    exc = sys.exc_info() #sys를 활용해서 에러를 확인합니다.
    message.channel.send(str(exc[0].__name__) + "" + str(exc[1])) #그 에러를 출력합니다.
	return
schedule.every().day.at("08:00").do(dbconnect.job())
while True:
    schedule.run_pending()
    time.sleep(1)

    '''
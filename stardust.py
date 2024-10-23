from asyncio.log import logger
import discord, random, numpy as np, dbconnect, asyncio #, create_actionrow, create_button
from discord.ext import commands

#변수관리
main = ["갈비탕", "해물찜", "스테이크", "수제버거", "마라탕","쌈밥", "훈제오리", "연어", "낙곱새", "월남쌈", "간장게장", "김치찌개", "떡볶이", "우거지국", "봉골레파스타"]
side = ["사과", "양배추샐러드", "카프리제", "버터옥수수"]
side2 = ["사과", "양배추샐러드", "카프리제", "버터옥수수"]
#drink_alcohol = ["샹베르탱", "클로 드 부조", "그랑 에세조", "로마네 콩티", "메르퀴레이","몽라셰", "블랑 드 누아","로제 데 리세", "돔 페리뇽", "막걸리", "피치 크러쉬", "블루하와이", "테킬라 선라이즈", "마가리타", "스크류 드라이버", "마티니", "블러디 메리", "소주", "독일맥주", "칭따오", "연태고량주", "이과두주", "보드카", "뱀술"]

drink_nonalcohol = ["에스프레소", "아메리카노", "카푸치노", "마끼아또", "라떼","요구르트", "물", "우유", "핫초코", "블랙밀크티", "옥수수수염차", "콜라", "사이다", "유자레몬티", "몬스터", "오렌지주스", "토마토주스", "에스프레소","논알콜 마티니"]

def id(ctx): return ctx.message.author.id
#def nick(ctx): return ctx.message.author.nick
def nick(ctx): return ctx.message.author.display_name
    
blue = discord.Color.blue()
red = discord.Color.red()
orange = discord.Color.orange()
purple = discord.Color.purple()
dkpurple = discord.Color.dark_purple()
dkred = discord.Color.dark_red()
gold = discord.Color.gold()
green = discord.Color.green()
yellow = discord.Color.yellow()

#sql 구문 관리

createTbluser = "create table IF NOT EXISTS user (userid varchar(255) primary key, name varchar(50), achol int, coin int, desct varchar(255), roomnum int);"
createTblfood = "create table IF NOT EXISTS food (name varchar(30), desct varchar(100), f_group varchar(50), Fachol int, acholYn boolean)"
#insertGuestlist = "insert into user values('haraseu.','퀘이드',0,0,'',''),('._.chaa._.','카일룸',0,0,'',''),('goaengryeong','유 신',0,0,'',''),('littsiee','수퍼소닉',0,0,'',''),('hyuian.','로베라',0,0,'',''),('151515hz_','멜리온',0,0,'',''),('su4g','페로즈',0,0,'',''),('birmancats0','아말',0,0,'',''),('rurina_0w0','나인',0,0,'',''), ('__nopotato','아샤',0,0,'','')"
insertFoodlist = "insert into food values ('라면','자꾸 땡기는 이 맛은 뭐지?','food',-5,1),('콩나물국','하, 시원하다....','food',-5,1),('우거지국','자꾸만 밥이 들어간다!','food',-10,1),('해장국','얼큰하다..해장이 되는 것 같다.,','food',-10,1),('숙취해소제','정신이 확 깬다!','achol',-30,1),('샹베르탱','','achol',13,1),('클로 드 부조','','achol',13,1),('그랑 에세조','','achol',13,1),('로마네 콩티','','achol',13,1),('메르퀴레이','','achol',13,1),('몽라셰','','achol',13,1),('블랑 드 누아','','achol',13,1),('로제 데 리세','','achol',13,1),('돔 페리뇽','','achol',13,1),('막걸리','','achol',15,1),('피치 크러쉬','','achol',4,1),('블루하와이','','achol',20,1),('테킬라 선라이즈','','achol',15,1),('마가리타','','achol',20,1),('스크류 드라이버','','achol',15,1),('마티니','','achol',20,1),('블러디 메리','','achol',10,1),('소주','','achol',17,1),('독일맥주','','achol',4,1),('칭따오','','achol',4,1),('연태고량주','','achol',50,1),('이과두주','','achol',56,1),('보드카','','achol',40,1),('뱀술','','achol',60,1),('압생트','','achol',65,1),('바카디','','achol',75,1),('스피리터스','','achol',96,1),('에버클리어','','achol',95,1),('브뤼클라딕x4','','achol',92,1)"
selectGuestlist = ""
selectachollist = ""

mysql = """host='127.0.0.1', user='root', password='root'"""

#텍스트관리
ansArr = ['아주 힘드셨겠어요.', '흠, 별 것도 아닌 일로...','네? 다른 생각하느라 거의 안 듣고 있었습니다.','첫눈에 반했습니다... 혹시 애인 있으십니까?\n 아차, 이게 아니지.','오늘 저녁엔 뭘 먹을까..']

#판단
async def check(ctx, m):#보낸사람과 채널 동일한지 체크
    return m.author == ctx.author and m.channel == ctx.channel
'''
async def check(ctx):#보낸사람과 채널 동일한지 체크
    return m.author == ctx.author and m.channel == ctx.channel
'''

#이벤트 관리


#if message.content == "DM":
#    await message.author.send("안녕하세요!")

#버튼관리
'''def btnClick():
    #const embed = new EmbedBuilder().setTitle("Hi")

    const button = new ActionRowBuilder().addComponents(
        new ButtonBuilder()
            .setCustomId("update-embed")
            .setLabel("Update Embed")
            .setStyle(ButtonStyle.Primary)
    )

    interaction.reply({
        embeds: [ embed ],
        components: [ button ],
    })'''

#이모지리액션관리
'''
async def on_reaction_add(reaction, user):
    try:
        await bot.wait_for("message", check=check, timeout=30)
        if user.bot == 1: #봇이면 패스
            return 0
        if str(reaction.emoji) == f"{reaction}":
            return user == message.author and str(reaction.emoji) == '🎲'
    except asyncio.TimeoutError:
       return -1

async def chkreact(reaction, check):
    try:
       reaction = await bot.wait_for('reaction_add', timeout=30, check=check)
    except asyncio.TimeoutError:
       await ctx.channel.sand('시간이 초과되었습니다.')
       return None
    return str(reaction.emoji) == ''
'''
#문구관리
def acholMsg(achol):
    if achol < 10:
        acholColor = green
        status = random['(멀쩡합니다.)', '(조금 심심합니다.)', '(따분합니다.)', '(졸린 것 같습니다.)', '(재미있습니다.)']
    elif achol >= 10 and achol < 30:
        acholColor = blue
        status = random.choice['기분 좋다~(평소와 다를 바 없습니다. 얼굴이 붉어지고 자꾸 웃음이 나오는 것 빼곤...)', 
                               '하아암... 좀 취했나?', 
                               '기분 최고다!!', 
                               '(이유 없이 즐거워서 마주치는 사람들마다 뽀뽀해주고 싶은 기분이다.)',
                               '한 잔 더!!',
                               '(술이 들어가니 누구와 이야기해도 즐겁습니다.)',
                               '(갑갑한 옷을 살짝 풀어헤칩니다.)']
    elif achol >= 30 and achol < 40:
        acholColor = yellow
        status = random.choice['왜 이렇게 많이 마셨지? 어지러워...', 
                               '아직 버틸 수 있어!',
                               '(했던 말을 자꾸 반복하고, 혀 짧은 사람처럼 발음이 꼬인 채입니다.)', 
                               '눈이 반쯤 감겨 있습니다.', 
                               '응? 너 누군데? (분명 아는 얼굴인데 알아보지 못합니다.)']
    elif achol >= 40 and achol < 50:
        acholColor = orange
        status = random.choice['아.. 더워... 머리 아파...(혀를 빼물고 헥헥거립니다.)',
                               '나랑 같이 갈래~? 헤헤헤...(웃음이 헤퍼집니다.)', 
                               '흑..흑흑...(너무너무 슬퍼서 아무것도 하고 싶지 않습니다.)', 
                               '후후후... (안 취한 것 같죠? 걸으면 자꾸 넘어져서 앉아있는 거예요.)']
    elif achol >= 50 and achol < 70:
        acholColor = red
        status = random.choice['하아... 하아...(얼굴이 붉어지고 땀이 흥건합니다.)', 
                               '**아, 몸이 뜨거워!** (속에서 불길이 일어나는 것처럼 몸이 뜨겁습니다.)', 
                               '**덥다, 더워!** (아무나 붙잡고 식혀달라고 하고 싶은 심정입니다. 이미 반쯤 탈의한 상태네요.)', 
                               '*응? 음냐음냐... 여기가 어디였더라? 난 누구지?*', 
                               '(*쿠울... 쿨...*)',
                               '히끅... 히끅... (조용히 울고 있습니다.)',
                               '끄러니까아~ 내가 마리야...(뭐가 그렇게 억울한 거죠? 꼬장을 부립니다.)',
                               '야! 너 말 다했어? (아무한테나 시비를 걸고 싶은 기분입니다.)',
                               '진짜 첫눈에 반할 정도로... 너무 예뻐서...(그림에게 말을 걸고 있습니다.)',
                               '왈! 왈왈! (**개**)',
                               '즐겁다, 너무 즐거워! 미친 사람처럼 웃으며 춤을 춥니다.', 
                               '과거의 일이 떠올라 죽을 정도로 슬픕니다. 오늘 안에 울음을 그치긴 어려워 보입니다.']
    elif achol >= 80 and achol < 90:
        acholColor = purple
        status = random.choice['토할 것 같다... 아니, 죽을 것 같아...', 
                               '(이젠 한계야! 세상이 빙빙 돕니다.)', 
                               '혼자서 걸을 수 없고, 제대로 말할 수 없습니다.)', 
                               '나 진짜 큰일 난 것 같은데... 우욱!', 
                               '(실신)',
                               '(어디다 부딪친 건지 머리에서 피가 흐르고 있지만 느끼지 못하는 것 같습니다.)']
    elif achol >= 90:
        acholColor = dkred
        status = random.choice['으웁...(**털썩**)', '(말을 걸어도 아무 대답이 없다.)', '대자연으로! 모든 걸 벗어 던졌다.']
    return status, acholColor


async def luckMsg(rndNum, target):
    try:
        if rndNum==1:
            await target.edit(embed=discord.Embed(title="그러세요!", color=discord.Color.blue()))
        elif rndNum==2:
            await target.edit(embed=discord.Embed(title="언젠가는.", color=discord.Color.pink()))
        elif rndNum==3:
            await target.edit(embed=discord.Embed(title="가만히 있으세요.", color=discord.Color.yellow()))
        elif rndNum==4:
            await target.edit(embed=discord.Embed(title="전혀 아닙니다.", color=discord.Color.red()))
        elif rndNum==5:
            await target.edit(embed=discord.Embed(title="그건 어려운 일이에요.", color=discord.Color.orange()))
        elif rndNum==6:
            await target.edit(embed=discord.Embed(title="지금이 바로 그때예요.", color=discord.Color.green()))
        elif rndNum==7:
            await target.edit(embed=discord.Embed(title="장애물을 잘 헤쳐나가세요.", color=discord.Color.orange()))
        elif rndNum==8:
            await target.edit(embed=discord.Embed(title="복잡하네요. 당신은 어떻게 생각하시나요?", color=discord.Color.purple()))
        elif rndNum==9:
            await target.edit(embed=discord.Embed(title="다시 한 번 말해주세요.", color=discord.Color.purple()))
        elif rndNum==10:
            await target.edit(embed=discord.Embed(title="뭘 망설이시는 거죠?", color=discord.Color.green()))
        elif rndNum==11:
            await target.edit(embed=discord.Embed(title="지금은 때가 아니에요", color=discord.Color.yellow()))
        elif rndNum==11:
            await target.edit(embed=discord.Embed(title="나중엔 후회할걸요!!", color=discord.Color.green()))
        else:
            await target.edit(embed=discord.Embed(title="아니요.", color=discord.Color.red()))
    except Exception as e:
        logger.log(e)
    finally :
        return target

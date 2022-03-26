import discord, json
from discord.ext import commands
import asyncio, time, ctypes
from datetime import datetime,timedelta
import requests, random, string
import os, urllib
from cultureland import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
config = json.loads(open("config.json", "r", encoding="utf-8-sig").read())
접두사 = config["접두사"]
사람토큰 = config["사람토큰"]
상메무한반복 = config["상메무한반복"]
상메1 = config["상메1"]
상메2 = config["상메2"]
상메3 = config["상메3"]
방송상메 = config["방송상메"]
컬쳐아디 = config["컬쳐아디"]
컬쳐비번 = config["컬쳐비번"]
계좌정보 = config["계좌정보"]
api키 = config["api키"]
api도메인 = config["api도메인"]
폰번호 = config["폰번호"]
intents = discord.Intents.all()
command_prefix = 접두사
bot = commands.Bot(self_bot=True, command_prefix=command_prefix,intents=intents)

token = 사람토큰
def serverinfo(server):
    g = bot.get_guild(int(server))
    gname = g.name
    gm = g.member_count
    a = f'> **{gname} : {gm}명**'
    return a

def getinfo(id):
    url = f"https://discordapp.com/api/users/{id}"
    he = {
        "Authorization": token
    }
    res = requests.get(url, headers=he)
    r = res.json()
    return r
@bot.event
async def on_ready():
    print(f"Login Success {bot.user}")
    if 상메무한반복 == True:
        while True:
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=상메1))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=상메2))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=상메3))
            await asyncio.sleep(10)
    else:
        await bot.change_presence(activity=discord.Streaming(name=방송상메, url="https://www.twitch.tv/faker"))

@bot.command()
async def ping(ctx):
    await ctx.send(f'> **__pong__** {round(bot.latency*1000)} ms')

@bot.command()
async def 계좌(ctx):
    await ctx.message.delete()
    await ctx.send(f'> **{계좌정보}**')

@bot.command()
async def 봇(ctx, *, rec):
    await ctx.message.delete()
    await ctx.send(f'> https://discord.com/oauth2/authorize?client_id={rec}&permissions=8&scope=bot')

@bot.command()
async def 정보(ctx, *, id):
    try:
        try:
            m = id
            m1 = m.split('@')[1]
            m2 = m1.split('>')[0]
            id = m2.split('!')[1]
        except:
            id = id
        res = getinfo(id)
        name = res['username']
        de = res['discriminator']
        icon = res['avatar']
        ba = res['banner_color']
        if icon != None:
            if "a_" in icon:
                iconurl = f"https://cdn.discordapp.com/avatars/{id}/{icon}.gif?size=1024"
            else:
                iconurl = f"https://cdn.discordapp.com/avatars/{id}/{icon}.png?size=1024"
        else:
            iconurl = "https://cdn.discordapp.com/embed/avatars/0.png"
        member = await bot.fetch_user(int(id))
        date_format = "%Y년 %m월 %d일 %H시 %M분 %S초"
        aa = member.created_at.strftime(date_format)
        banner = res['banner']
        if banner != None:
            if "a_" in banner:
                bannerurl = f"https://cdn.discordapp.com/banners/{id}/{banner}.gif?size=1024"
                await ctx.reply(f'> `유저이름` : {name}#{de}\n'
                                f'> `유저아이디` : {id}\n'
                                f'> `프로필` : ||{iconurl}||\n'
                                f'> `가입한날` : {aa}\n'
                                f'> `배너색` : {ba}\n'
                                f'> `배너사진` : ||{bannerurl}||')
            else:
                bannerurl = f"https://cdn.discordapp.com/banners/{id}/{banner}.png?size=1024"
                await ctx.reply(f'> `유저이름` : {name}#{de}\n'
                                f'> `유저아이디` : {id}\n'
                                f'> `프로필` : ||{iconurl}||\n'
                                f'> `가입한날` : {aa}\n'
                                f'> `배너색` : {ba}\n'
                                f'> `배너사진` : {bannerurl}')
        else:
            await ctx.reply(f'> `유저이름` : {name}#{de}\n'
                            f'> `유저아이디` : {id}\n'
                            f'> `프로필` : ||{iconurl}||\n'
                            f'> `가입한날` : {aa}\n'
                            f'> `배너색` : {ba}\n'
                            f'> `배너사진` : None')
    except:
        await ctx.reply("> 존재하지않는 사용자입니다.")

@bot.command()
@commands.has_permissions(ban_members = True)
async def 벤(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"> {member} 님을 `성공적으로` __영구차단하였습니다.__")

@bot.command(name="벤해제", help="유저를 벤 해제합니다.")
@commands.has_permissions(administrator=True)
async def _unban(ctx, *, member_id: int):
    await ctx.guild.unban(discord.Object(id=member_id))
    await ctx.send(f"> <@{member_id}> 님을 `성공적으로` __차단해제하였습니다.__")

@bot.command(name="역할생성", help="뒤에 있는 역할 이름으로 역할을 생성합니다.")
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'역할 `{name}` 이 만들어졌습니다.')

@bot.command()
async def 숨기기(ctx, link):
    await ctx.message.delete()
    await ctx.send(f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
                                   f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|||"
                                   f"|​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||"
                                   f"​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||"
                                   f"​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||"
                                   f"​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ "
                                   f"{link}")
@bot.command(pass_context=True)
async def 역할(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"> `{user}`님에게 `{role.name}`역할이 성공적으로 지급되었습니다.")

@bot.command()
async def 채널(ctx):
    if ctx.guild != None:
        await ctx.send(f"> `{ctx.guild}` -> `{ctx.channel}` -> `{ctx.channel.id}`")
    else:
        await ctx.send(f"> `{ctx.channel}` -> `{ctx.channel.id}`")

@bot.command()
async def 시간(ctx):
    y = datetime.now().year
    m = datetime.now().month
    d = datetime.now().day
    h = datetime.now().hour
    min = datetime.now().minute
    await ctx.reply(f'> 시간정보 : __{y}년 {m}월 {d}일 {h}시 {min}분__')

@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount):
    if int(amount) <= 10:
        await ctx.channel.purge(limit=int(amount))
        await ctx.send(f"> `{amount}`개 청소가 __완료되었습니다__")
    else:
        await ctx.send(f"> `{amount}`개는 셀프봇으로 청소하기에 너무 __큰숫자입니다.__\n\n> `10`개 __이하로__ 입력해주세요.")

@bot.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    msg = await ctx.send(f"> **`오류`가 발생하였습니다.**\n\n> __{error}__")
    await msg.add_reaction('❌')

@bot.command()
async def 상메(ctx, *, text):
  await bot.change_presence(activity=discord.Game(name=f'{text}'))
  await ctx.send(f"> 상태메시지가 `{text}`로 성공적으로 __변경되었습니다.__")

@bot.command()
async def 주사위(ctx):
    com = random.choice(["1", "2", "3", "4", "5", "6"])
    await ctx.send(f"{ctx.author.mention}님 랜덤주사위 결과는 {com}입니다 🎲")

@bot.command()
async def 루트(ctx, *, dd):
    a = ("{:g}".format(int(dd) ** (1 / 2)))
    await ctx.reply(f"> `{a}`")

@bot.command()
async def 약수(ctx, *, n):
    i = 1
    list_a = []
    if len(str(n)) <= 5:
        while i <= int(n):
            if int(n) % i == 0:
                list_a.append(i)
            i += 1
    await ctx.reply(f"> `{list_a}`")

@bot.command()
async def 명령어(ctx):
    await ctx.reply(
             "> `파싱` = 파싱에 관련된 명령어들을 보실수있습니다."
             "\n> `토큰` = 토큰에 관련된 명령어들을 보실수있습니다."
             "\n> `컬쳐랜드` = 컬쳐랜드에 관련된 명령어들을 보실수있습니다."
             "\n> `서버관리` = 서버관리에 관한 명령어들을 보실수있습니다."
             "\n> `그외` = 그외 잡다한 명령어들을 보실수있습니다."
            f"\n> \n> **Powered by 망치**\n> __접두사__ = {command_prefix}") #수정ㄴ
@bot.command()
async def 그외(ctx):
    await ctx.reply("> `ping` = 컴의 `핑`을 확인할수있습니다."
             "\n> `계좌` = 설정해논 `계좌`를 명령어로 불러옵니다."
             "\n> `봇` `봇아이디` = 봇아이디로 `봇초대링크`를 만들어서 불러옵니다."
             "\n> `상메` `바꿀상메` = `상태메시지`를 적은 메시지로 바꿉니다."
             "\n> `서버` `서버아이디` = 서버아이디에 해당한 서버의 `인원수`를 불러옵니다."
             "\n> `채널` = 명령어를 쓴 `채널`의 정보를 불러옵니다."
             "\n> `시간` = 명령어를 쓴 `시간`의 정보를 불러옵니다."
             "\n> `루트` `숫자` = 숫자의 `제곱근`을 불러옵니다."
             "\n> `약수` `숫자` = 숫자의 `약수`를 불러옵니다."
             "\n> `웹훅생성` = 메시지를 친 채널의 `웹훅`을 `생성`합니다."
             "\n> `정보` `멘션혹은 아이디` = 대상의 `정보`를 불러옵니다."
             "\n> `검색` `검색할것` = 검색할것을 봇이 네이버에 `검색`하고 스샷해서 보여줍니다"
             "\n> `웹` `웹주소` = 웹주소의 `웹 소스를 파싱`해서 html파일형태로 출력합니다."
            "\n> `서버정보`= 명령어를 한 서버의 `서버정보`를 불러옵니다."
            "\n> `링크` `링크주소` = 링크주소를 들어가서 `스샷`후 보여줍니다."
            "\n> `구글링` `검색할것`= 검색할것을 구글에 검색후 `스샷`해서 보여줍니다."
            "\n> `gif` `검색할것`= 검색할것을 gif로 나태냅니다."
            "\n> `도배` `도배할내용` `도배할수` = 도배할수만큼 도배할내용으로 `도배`합니다.")
@bot.command()
async def 파싱(ctx):
    await ctx.reply(
                   "> `멤버파싱`= 명령어를 한 서버의 `멤버`를 긁어옵니다."
                   "\n> `채널파싱`= 명령어를 한 서버의 `채널`을 긁어옵니다."
                   "\n> `역할파싱`= 명령어를 한 서버의 `역할`를 긁어옵니다."
                   "\n> `이모지파싱`= 명령어를 한 서버의 `이모지`를 긁어옵니다."
                   "\n> `서버복사` = 명령어를 한 서버를 복사합니다.")
@bot.command()
async def 토큰(ctx):
    await ctx.reply(
             "> `토큰만` `이멜:비번:토큰` = 받은토큰을 `토큰만` 출력합니다."
             "\n> `토큰체킹` `토큰` = 받은토큰을 `체킹`하여 사용가능한지 나타냅니다."
            "\n> `토큰정보` `토큰` = 토큰의 `정보`를 불러옵니다."
             "\n> `토큰보기` `멘션` = 멘션한 유저의 ~~가짜~~토큰을 불러옵니다."
            "\n> `토큰로그인` `토큰` = 토큰을 로그인후 스샷해옵니다.")
@bot.command()
async def 컬쳐랜드(ctx):
    await ctx.reply(
             "> `문상` `핀번호` = 핀번호로 문상을 `충전`합니다."
             "\n> `돈` = 설정한 컬쳐랜드아이디의 `잔액`을 불러옵니다."
             "\n> `출금` `액수` = 액수만큼 문상을 `출금`합니다.")
@bot.command()
async def 서버관리(ctx):
    await ctx.reply(
    "> `청소` `숫자` = 숫자만큼 해당채널의 메시지를 `청소`합니다."
    "\n> `벤` `유저멘션` = 멘션당한유저를 서버에서 `영구차단`합니다."
    "\n> `벤해제` `유저아이디` = 유저아이디에 해당하는 유저를 서버에서 `영구차단해제`를 합니다."
    "\n> `역할생성` `역할이름` = 역할이름으로 된 역할을 `생성`합니다."
    "\n> `역할` `유저멘션` `역할이름` = 역할이름으로 된 역할을 멘션당한 유저에게 `지급`합니다.")
@bot.command()
async def 서버복사(ctx):
    msg = await ctx.reply(f'> 복사당할 서버 `생성중` ...')
    url = f"https://canary.discord.com/api/v8/guilds"
    headers = {
        "authorization": token
    }
    payload = {"name": ctx.guild.name}
    res = requests.post(url, headers=headers, json=payload)
    r = res.json()
    await msg.edit(content=f'> 복사당할 서버 생성완료 ✅')
    id = r['id']
    TOKEN = token  # 자신의 디스코드 토큰 쓰기

    COPY_GUILD = ctx.guild.id  # 복사할 서버 아이디쓰기

    RESULT_GUILD = id  # 복사당할 서버 아이디 쓰기

    # ==================================================================
    API_BASE = "https://discord.com/api/v9"

    def isRatelimit(obj):
        if obj.get("global", None) != None:
            return True, obj.get("retry_after", 0.0)
        else:
            return False, 0

    headers = {
        "authorization": TOKEN
    }

    result_channels = requests.get(f"{API_BASE}/guilds/{RESULT_GUILD}/channels", headers=headers).json()
    result_roles = requests.get(f"{API_BASE}/guilds/{RESULT_GUILD}/roles", headers=headers).json()
    for channel in result_channels:
        while True:
            delete_channel = requests.delete(f"{API_BASE}/channels/{channel['id']}", headers=headers).json()
            ratelimit, sleep = isRatelimit(delete_channel)
            if ratelimit:
                time.sleep(sleep)
            else:
                break
    await msg.edit(content=f'> 복사당할 서버 채널정리 완료 ✅')
    for channel in result_roles:
        while True:
            delete_channel = requests.delete(f"{API_BASE}/guilds/{RESULT_GUILD}/roles/{channel['id']}", headers=headers)
            try:
                delete_channel = delete_channel.json()
            except:
                delete_channel = {}
            ratelimit, sleep = isRatelimit(delete_channel)
            if ratelimit:
                time.sleep(sleep)
            else:
                break
    await msg.edit(content=f'> 복사당할 서버 역할정리 완료 ✅')
    original_channels = requests.get(f"{API_BASE}/guilds/{COPY_GUILD}/channels", headers=headers).json()
    original_roles = requests.get(f"{API_BASE}/guilds/{COPY_GUILD}/roles", headers=headers).json()

    original_guild = requests.get(f"{API_BASE}/guilds/{COPY_GUILD}", headers=headers).json()

    system_channel = original_guild.get("system_channel_id")
    if system_channel == None:
        system_channel = 0

    new_system_channel = 0

    category_channels = []
    channels = []

    for channel in original_channels:
        if channel["type"] == 4:
            category_channels.append(channel)
        else:
            channels.append(channel)
    await msg.edit(content=f'> 복사할 서버 채널파싱 완료 ✅')

    original_roles.sort(key=lambda x: x["position"], reverse=True)
    for role in original_roles:
        while True:
            if role["managed"]:
                break
            if int(role["id"]) == int(COPY_GUILD):
                for i in range(len(channels)):
                    par = channels[i].get("permission_overwrites")
                    if par:
                        for j in range(len(par)):
                            if par[j]["id"] == role["id"]:
                                channels[i]["permission_overwrites"][j]["id"] = RESULT_GUILD
                break
            obj = role
            create_role = requests.post(f"{API_BASE}/guilds/{RESULT_GUILD}/roles", json=obj, headers=headers).json()
            ratelimit, sleep = isRatelimit(create_role)
            if ratelimit:
                time.sleep(sleep)
            else:
                for i in range(len(channels)):
                    par = channels[i].get("permission_overwrites")
                    if par:
                        for j in range(len(par)):
                            if par[j]["id"] == role["id"]:
                                channels[i]["permission_overwrites"][j]['id'] = create_role['id']
                for i in range(len(category_channels)):
                    par = category_channels[i].get("permission_overwrites")
                    if par:
                        for j in range(len(par)):
                            if par[j]["id"] == role["id"]:
                                category_channels[i]["permission_overwrites"][j]["id"] = create_role["id"]
                break
    await msg.edit(content=f'> 복사당할 서버 역할생성 완료 ✅')

    for category in category_channels:
        while True:
            obj = category
            del obj["guild_id"]
            create_channel = requests.post(f"{API_BASE}/guilds/{RESULT_GUILD}/channels", json=obj,
                                           headers=headers).json()
            ratelimit, sleep = isRatelimit(create_channel)
            if ratelimit:
                time.sleep(sleep)
            else:
                for i in range(len(channels)):
                    par = channels[i].get("parent_id")
                    if par:
                        if par == category["id"]:
                            channels[i]["parent_id"] = create_channel["id"]
                break
    await msg.edit(content=f'> 복사당할 서버 카테고리생성 완료 ✅')
    for channel in channels:
        try:
            while True:
                obj = channel
                del obj["guild_id"]

                create_channel = requests.post(f"{API_BASE}/guilds/{RESULT_GUILD}/channels", json=obj,
                                               headers=headers).json()
                ratelimit, sleep = isRatelimit(create_channel)
                if ratelimit:
                    time.sleep(sleep)
                else:
                    if obj["id"] == system_channel:
                        new_system_channel = create_channel["id"]
                    break
        except:
            pass
    await msg.edit(content=f'> 복사당할 서버 채널생성 완료 ✅')
    res = requests.get(f"https://discordapp.com/api/v9/guilds/{RESULT_GUILD}", headers=headers).json()
    id = res['id']
    sv = bot.get_guild(int(id))
    await ctx.reply(f'{sv} 서버가 생성되었습니다. 확인해주세요')
@bot.command()
async def 토큰만(ctx, *, tk):
    open('tokens.txt', 'w')
    with open('tokens.txt','w') as f:
        f.write(tk)
    with open('tokens.txt','r') as f:
        tokens=f.read().split('\n')
    go=[]
    for token in tokens:
        try:
            if not token=='':
                tokenone=token.split(':')[2]
        except:
            print('이메일:비밀번호:토큰 순으로 입력해주세요')
            print('========================================================')
            exit()
        go.append(tokenone)
    with open('tokens.txt','w') as f:
        f.write('\n'.join(go))
    await ctx.send(file=discord.File(f"tokens.txt"))
    os.remove(f"tokens.txt")

@bot.command()
async def 토큰체킹(ctx, *, token):
    try:
        token = token.split(":")[2]
    except:
        token = token
    headers = {'Content-Type': 'application/json', 'authorization': token}
    url = "https://discordapp.com/api/v6/users/@me/library"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        await ctx.reply(f"> 이 토큰은 사용가능합니다. :key: ")
    else:
        await ctx.reply("> 이 토큰은 사용불가능합니다. :lock:")

@bot.command()
async def 문상(ctx, *, msg):
    try:
        jsondata = {"token": api키, "id": 컬쳐아디, "pw": 컬쳐비번, "pin": msg}
        res = requests.post(api도메인, json=jsondata)
    except:
        try:
            await ctx.reply("> 문화상품권 충전 실패\n> \n> 일시적인 서버 오류입니다.\n> 잠시 후 다시 시도해주세요.")
        except:
            pass
        return None
    res = res.json()
    if res["result"] == True:
        try:
            culture_fee = int(0)
            culture_amount = int(res["amount"])
            culture_amount_after_fee = culture_amount - int(culture_amount * (culture_fee / 100))
            await ctx.reply(
                f"> 문화상품권 충전 성공\n> \n> 핀코드: `{msg}`\n> 금액: `{culture_amount}`원\n> 충전한 금액: `{culture_amount_after_fee}`")
        except:
            pass

    else:
        await ctx.reply("> 문화상품권 충전 실패\n> \n> 실패 사유 : " + res["reason"])
@bot.command()
async def 충전(ctx, *, msg):
    try:
        jsondata = {"token": api키, "id": 컬쳐아디, "pw": 컬쳐비번, "pin": msg}
        res = requests.post(api도메인, json=jsondata)
    except:
        try:
            await ctx.reply("> 문화상품권 충전 실패\n> \n> 일시적인 서버 오류입니다.\n> 잠시 후 다시 시도해주세요.")
        except:
            pass
        return None
    res = res.json()
    if res["result"] == True:
        try:
            culture_fee = int(0)
            culture_amount = int(res["amount"])
            culture_amount_after_fee = culture_amount - int(culture_amount * (culture_fee / 100))
            await ctx.reply(
                f"> 문화상품권 충전 성공\n> \n> 핀코드: `{msg}`\n> 금액: `{culture_amount}`원\n> 충전한 금액: `{culture_amount_after_fee}`")
        except:
            pass

    else:
        await ctx.reply("> 문화상품권 충전 실패\n> \n> 실패 사유 : " + res["reason"])
@bot.command()
async def 이모지(ctx, *, mes):
    msg = await ctx.send(f"{mes}")
    await msg.add_reaction('🎁')

@bot.command()
async def 출금(ctx, *, money): #자동출금소스와 연동
    id = 컬쳐아디
    pw = 컬쳐비번
    phone = 폰번호
    re = cultureland(id,pw,phone,money)
    a = re.login()
    print(a)
    if a[0] == False:
        return
    res = re.gift()
    await ctx.reply(res)

@bot.command()
async def 돈(ctx): #자동출금소스와 연동
    id = 컬쳐아디
    pw = 컬쳐비번
    phone = 폰번호
    money = '1000'
    re = cultureland(id,pw,phone,money)
    a = re.login()
    if a[0] == False:
        return
    res = re.getcash()
    await ctx.reply(res)
@bot.command()
async def 웹훅생성(ctx):
    if ctx.author.guild_permissions.administrator:
        ch = bot.get_channel(int(ctx.channel.id))
        webhook = await ch.create_webhook(name=ctx.author, reason='배너봇 자동개설')
        await ctx.reply('웹훅 생성해왔습니다\n' + webhook.url)
    else:
        await ctx.send("{}, 당신은 권한이 없습니다! ".format(ctx.author.mention))
@bot.command()
async def 도배(ctx, content, count:int):
    API_BASE = "https://discord.com/api/v9"
    headers = {
        "authorization": token
    }
    for i in range(count):
        requests.post(f"{API_BASE}/channels/{ctx.channel.id}/messages", headers=headers, json={'content': content})
@bot.command()
async def 토큰정보(ctx, *, token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    g = requests.get('https://discord.com/api/v6/users/@me/guilds', headers=headers)
    c = requests.get('https://discord.com/api/v6/users/@me/channels', headers=headers)
    if r.status_code == 200:
        try:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            nitro = bool(r.json()['premium_type'])
            bio = r.json()['bio']
            av = r.json()['avatar']
            banner = r.json()['banner']
            ba = r.json()['banner_color']
            if banner != None:
                if "a_" in banner:
                    banner = f"https://cdn.discordapp.com/banners/{userID}/{banner}.gif?size=1024"
                else:
                    banner = f"https://cdn.discordapp.com/banners/{userID}/{banner}.png?size=1024"
            if av != None:
                if "a_" in av:
                    av = f"https://cdn.discordapp.com/avatars/{userID}/{av}.gif?size=1024"
                else:
                    av = f"https://cdn.discordapp.com/avatars/{userID}/{av}.png?size=1024"
            guild = len(g.json())
            dm = len(c.json())
            if bio != "":
                await ctx.reply(f"""
                                                > ✅유저이름 : `{userName}`
                                                > ✅유저아이디 : `{userID}`
                                                > ✅전화번호 : `{phone}`
                                                > ✅이메일 : `{email}`
                                                > ✅2차인증 : `{mfa}`
                                                > ✅니트로 : `{nitro}`
                                                > ✅프로필 : ||{av}||
                                                > ✅배너사진 : ||{banner}||
                                                > ✅배너색 : {ba}
                                                > ✅들어간서버수 : `{guild}`
                                                > ✅디엠내역수 : `{dm}`
                                                > ✅유저소개 : \n```cs\n{bio}```
                                                """)
            else:
                await ctx.reply(f"""
                                > ✅유저이름 : `{userName}`
                                > ✅유저아이디 : `{userID}`
                                > ✅전화번호 : `{phone}`
                                > ✅이메일 : `{email}`
                                > ✅2차인증 : `{mfa}`
                                > ✅니트로 : `{nitro}`
                                > ✅프로필 : ||{av}||
                                > ✅배너사진 : ||{banner}||
                                > ✅배너색 : {ba}
                                > ✅들어간서버수 : `{guild}`
                                > ✅디엠내역수 : `{dm}`
                                > ✅유저소개 : 유저소개가 없습니다.
                                """)
        except:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            bio = r.json()['bio']
            av = r.json()['avatar']
            if av != None:
                if "a_" in av:
                    av = f"https://cdn.discordapp.com/avatars/{userID}/{av}.gif?size=1024"
                else:
                    av = f"https://cdn.discordapp.com/avatars/{userID}/{av}.png?size=1024"
            guild = len(g.json())
            dm = len(c.json())
            banner = r.json()['banner']
            ba = r.json()['banner_color']
            if banner != None:
                if "a_" in banner:
                    banner = f"https://cdn.discordapp.com/banners/{userID}/{banner}.gif?size=1024"
                else:
                    banner = f"https://cdn.discordapp.com/banners/{userID}/{banner}.png?size=1024"
            if bio != "":
                await ctx.reply(f"""
                                > ✅유저이름 : `{userName}`
                                > ✅유저아이디 : `{userID}`
                                > ✅전화번호 : `{phone}`
                                > ✅이메일 : `{email}`
                                > ✅2차인증 : `{mfa}`
                                > ✅니트로 : `False`
                                > ✅프로필 : ||{av}||
                                > ✅배너사진 : ||{banner}||
                                > ✅배너색 : {ba}
                                > ✅들어간서버수 : `{guild}`
                                > ✅디엠내역수 : `{dm}`
                                > ✅유저소개 : \n```cs\n{bio}```
                                """)
            else:
                await ctx.reply(f"""
                > ✅유저이름 : `{userName}`
                > ✅유저아이디 : `{userID}`
                > ✅전화번호 : `{phone}`
                > ✅이메일 : `{email}`
                > ✅2차인증 : `{mfa}`
                > ✅니트로 : False
                > ✅프로필 : ||{av}||
                > ✅배너사진 : ||{banner}||
                > ✅배너색 : {ba}
                > ✅들어간서버수 : `{guild}`
                > ✅디엠내역수 : `{dm}`
                > ✅유저소개 : 유저소개가 없습니다.
                """)
    else:
        await ctx.reply("> 토큰이 유효하지 않습니다.")
@bot.command()
async def 서버정보(ctx):
        id = ctx.guild.id
        g = bot.get_guild(int(id))
        gname = g.name
        gm = g.member_count
        gi = g.icon
        gv = g.verification_level
        gf = bool(g.mfa_level)
        gb = g.banner
        gp = g.premium_tier
        date_format = "%Y년 %m월 %d일 %H시 %M분 %S초"
        gj = g.created_at.strftime(date_format)
        if gi != None:
            if "a_" in gi:
                iconurl = f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{gi}.gif?size=1024"
            else:
                iconurl = f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{gi}.png?size=1024"
            if gb != None:
                if "a_" in gi:
                    bannerurl = f"https://cdn.discordapp.com/banners/{ctx.guild.id}/{gb}.gif?size=1024"
                else:
                    bannerurl = f"https://cdn.discordapp.com/banners/{ctx.guild.id}/{gb}.png?size=1024"
                await ctx.reply(f"""
                > 서버이름 : `{gname}`
                > 서버아이디 : `{id}`
                > 서버인원 : `{gm}`
                > 서버생성일 : `{gj}`
                > 서버부스트단계 : `{gp}`
                > 서버아이콘 : ||{iconurl}||
                > 서버보안 : `{gv}`
                > 서버2차보안 : `{gf}`
                > 서버배너 : ||{bannerurl}||
                """)
            else:
                await ctx.reply(f"""
                                > 서버이름 : `{gname}`
                                > 서버아이디 : `{id}`
                                > 서버인원 : `{gm}`
                                > 서버생성일 : `{gj}`
                                > 서버부스트단계 : `{gp}`
                                > 서버아이콘 : ||{iconurl}||
                                > 서버보안 : `{gv}`
                                > 서버2차보안 : `{gf}`
                                > 서버배너 : {gb}
                                """)
        else:
            if gb != None:
                if "a_" in gi:
                    bannerurl = f"https://cdn.discordapp.com/banners/{ctx.guild.id}/{gb}.gif?size=1024"
                else:
                    bannerurl = f"https://cdn.discordapp.com/banners/{ctx.guild.id}/{gb}.png?size=1024"
                await ctx.reply(f"""
                                > 서버이름 : `{gname}`
                                > 서버아이디 : `{id}`
                                > 서버인원 : `{gm}`
                                > 서버생성일 : `{gj}`
                                > 서버부스트단계 : `{gp}`
                                > 서버아이콘 : ||{gi}||
                                > 서버보안 : `{gv}`
                                > 서버2차보안 : `{gf}`
                                > 서버배너 : ||{bannerurl}||
                                """)
            else:
                await ctx.reply(f"""
                                                > 서버이름 : `{gname}`
                                                > 서버아이디 : `{id}`
                                                > 서버인원 : `{gm}`
                                                > 서버생성일 : `{gj}`
                                                > 서버부스트단계 : `{gp}`
                                                > 서버아이콘 : ||{gi}||
                                                > 서버보안 : `{gv}`
                                                > 서버2차보안 : `{gf}`
                                                > 서버배너 : {gb}
                                                """)
@bot.command()
async def 멤버파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching Members...**")
    guild_id = f"{ctx.guild.id}"
    channel_id = f"{ctx.channel.id}"
    try:
        import discum
    except ModuleNotFoundError:
        print("모듈이 없어서 다운후 리턴함.")
        os.system("pip install discum")
        await msg.edit(content="> 모듈이 없어서 제가 깔았습니다.\n> \n> 다시 시도해주세요. :)")
    bot = discum.Client(token=token, log=False)

    def close_after_fetching(resp, guild_id):
        if bot.gateway.finishedMemberFetching(guild_id):
            len(bot.gateway.session.guild(guild_id).members)
            bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
            bot.gateway.close()

    def get_members(guild_id, channel_id):
        bot.gateway.fetchMembers(guild_id, channel_id, keep='all', wait=0)
        bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
        bot.gateway.run()
        bot.gateway.resetSession()
        return bot.gateway.session.guild(guild_id).members

    members = get_members(guild_id=guild_id, channel_id=channel_id)

    info = [

    ]
    try:
        os.makedirs(f"Parse/{guild_id}")
    except:
        pass
    for member in members:
        user = members[str(member)]
        userinfo = {
            "id": member,
            "username": user["username"] + "#" + user["discriminator"],
        }
        info.append(userinfo)

    ids = []
    for member in info:
        ids.append(member["username"] + f' ({member["id"]})')
    open(f"Parse/{guild_id}.txt", "w",encoding='utf-8-sig').write("\n".join(ids))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"Parse/{guild_id}.txt"))
@bot.command()
async def 이모지파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching emoji...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.emojis
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('emojiparse.txt', 'w', encoding='utf-8-sig')
    with open('emojiparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"emojiparse.txt"))
    os.remove(f"emojiparse.txt")
@bot.command()
async def 채널파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching Channel...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.channels
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('channelparse.txt', 'w', encoding='utf-8-sig')
    with open('channelparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"channelparse.txt"))
    os.remove(f"channelparse.txt")
@bot.command()
async def 역할파싱(ctx):
    msg = await ctx.reply("⚙️ **Fetching Role...**")
    target = []
    g = bot.get_guild(int(ctx.guild.id))
    g = g.roles
    print(g)
    for i in range(1000):
        try:
            human = g[i]
            target.append(human.name + f'({human.id})')
        except:
            break
    open('roleparse.txt', 'w', encoding='utf-8-sig')
    with open('roleparse.txt', 'w', encoding='utf-8-sig') as f:
        f.write(",\n".join(target))
    await msg.edit(content="✅ 파싱 완료")
    await ctx.send(file=discord.File(f"roleparse.txt"))
    os.remove(f"roleparse.txt")
@bot.command()
async def 메시지파싱(ctx, c:int):
    id = ctx.channel.id
    channel = bot.get_channel(id)
    f = open(f"msgparse.txt", "w", encoding="utf-8-sig")
    async for message in channel.history(limit=c):
        if message.content != None:
            f.write(
                f"{message.author.name}#{message.author.discriminator} : {message.content} ({message.created_at.strftime('%Y년%m월%d일 %H시%M분%S초')})\n")
        if message.attachments != []:
            for attach in message.attachments:
                f.write(
                    f"{message.author.name}#{message.author.discriminator} : {message.content} ({message.created_at.strftime('%Y년%m월%d일 %H시%M분%S초')}) 파일 : {attach.url}\n")
    f.close()
    await ctx.reply(file=discord.File("msgparse.txt"))
    os.remove("msgparse.txt")

@bot.command()
async def 개인청소(ctx, c:int):
    id = ctx.channel.id
    channel = bot.get_channel(id)
    API_BASE = "https://discord.com/api/v9"
    headers = {
        "authorization": token
    }
    async for message in channel.history(limit=c+1):
        if message.content != None:
            if str(message.author.id) != str(ctx.author.id):
                c += 2
    print(c)
    async for message in channel.history(limit=c):
        if message.content != None:
            print(message.author.id)
            if str(message.author.id) == str(ctx.author.id):
                try:
                    requests.delete(f"{API_BASE}/channels/{ctx.channel.id}/messages/{message.id}", headers=headers)
                except:
                    pass
    await ctx.reply("> 개인말만 청소 완료")
@bot.command(pass_context=True)
async def gif(ctx, *, msg: str):
        gif = 'https://giphy.com/search/'
        await ctx.reply(gif + msg.lower().replace(" ", "-") )
@bot.command()
async def 링크(ctx, *, url):
    msg = await ctx.reply(f"> 잠시 기다려주세요...\n> \n> {url} 에 접속중입니다. :mag: ")
    options = Options()
    options.add_argument('headless')
    browser = webdriver.Chrome("./chromedriver.exe", options=options)
    browser.get(url)
    await msg.edit(content=f"> {url} 접속완료✅")
    screenshot = browser.save_screenshot("망치천재" + '.png')
    await msg.edit(content=f"> 이미지 스샷완료✅")
    browser.quit()
    await ctx.send(file=discord.File("망치천재" + '.png'))
    os.remove("망치천재" + '.png')
@bot.command()
async def 토큰로그인(ctx, *, token):
    msg = await ctx.reply(f"> 잠시 기다려주세요...\n> \n> 디스코드에 접속중입니다. :mag: ")
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://discord.com/login')
    js = 'function login(token) {setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`}, 50);setTimeout(() => {location.reload();}, 500);}'
    time.sleep(3)
    driver.execute_script(js + f'login("{token}")')
    await msg.edit(content=f"> 토큰로그인 완료✅")
    await msg.edit(content=f"> 디스코드 로딩중... :infinity: ")
    time.sleep(7)
    screenshot = driver.save_screenshot("망치천재" + '.png')
    await msg.edit(content=f"> 이미지 스샷완료✅")
    driver.quit()
    await ctx.send(file=discord.File("망치천재" + '.png'))
    os.remove("망치천재" + '.png')

@bot.command()
async def 구글링(ctx, *, 검색할것):
    msg = await ctx.reply(f"> 잠시 기다려주세요...\n> \n> {검색할것}를 검색중입니다 :mag: ")
    naver_url = "https://google.com"
    browser = webdriver.Chrome("./chromedriver.exe")
    browser.get(naver_url)
    await msg.edit(content=f"> 구글 접속완료✅")
    검색창 = browser.find_element_by_css_selector("body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input")
    검색창.send_keys(검색할것)
    검색창.send_keys(Keys.ENTER)
    await msg.edit(content=f"> {검색할것} 검색완료✅")
    browser.save_screenshot("망치천재" + '.png')
    await msg.edit(content=f"> 이미지 스샷완료✅")
    await ctx.send(file=discord.File("망치천재" + '.png'))
    browser.quit()
    os.remove("망치천재" + '.png')
@bot.command()
async def 검색(ctx, *, 검색할것):
    msg = await ctx.reply(f"> 잠시 기다려주세요...\n> \n> {검색할것}를 검색중입니다 :mag: ")
    naver_url = "https://naver.com"

    options = Options()

    if 검색할것 != "코로나":
        options.add_argument('headless')
        options.add_argument('--start-maximized')
        browser = webdriver.Chrome("./chromedriver.exe", options=options)
        browser.get(naver_url)
        await msg.edit(content=f"> 네이버 접속완료✅")
        time.sleep(2)
        검색창 = browser.find_element_by_css_selector("#query")
        검색창.send_keys(검색할것)
        검색창.send_keys(Keys.ENTER)
        await msg.edit(content=f"> {검색할것} 검색완료✅")
        time.sleep(2)
        screenshot = browser.save_screenshot("망치천재" + '.png')
        await msg.edit(content=f"> 이미지 스샷완료✅")
        browser.quit()
        await ctx.send(file=discord.File("망치천재" + '.png'))
        os.remove("망치천재" + '.png')
    else:
        options.add_argument('headless')
        options.add_argument('--start-maximized')
        browser = webdriver.Chrome("./chromedriver.exe", options=options)
        browser.get(naver_url)
        await msg.edit(content=f"> 네이버 접속완료✅")
        time.sleep(2)
        검색창 = browser.find_element_by_css_selector("#query")
        검색창.send_keys(검색할것)
        검색창.send_keys(Keys.ENTER)
        await msg.edit(content=f"> {검색할것} 검색완료✅")
        time.sleep(2)
        element1 = browser.find_element_by_class_name('status_info')
        element_png = element1.screenshot_as_png
        with open("망치천재" + '.png', "wb") as file:
            file.write(element_png)
        await msg.edit(content=f"> 이미지 스샷완료✅")
        browser.quit()
        await ctx.send(file=discord.File("망치천재" + '.png'))
        os.remove("망치천재" + '.png')
@bot.command()
async def 웹(ctx, url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    open('parse.html', 'w', encoding='utf-8-sig')
    with open('parse.html', 'w', encoding='utf-8-sig') as f:
        f.write(str(soup))
    await ctx.send(file=discord.File(f"parse.html"))
    os.remove(f"parse.html")

@bot.command()
async def 토큰보기(ctx, *, target):
    first = ('').join(random.choices(string.ascii_letters + string.digits, k=24))
    second = ('').join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=6))
    end = ('').join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=25))
    token = f"OT{first}.{second}.{end}"
    await ctx.reply(f"> {target}님의 토큰입니다.\n> \n> {token}")

bot.run(token, bot=False)

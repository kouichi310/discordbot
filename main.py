import discord
import asyncio
import os
import time
import discord
from mutagen.mp3 import MP3
import youtube_dl
from apiclient.discovery import build
from datetime import datetime
import random
import json
from collections import OrderedDict
from discord.ext import tasks
import serch_twitter
import  tweepy
from key_tweepy import key_tweepy_proc
from os.path import join, dirname
from dotenv import load_dotenv
com = {}
sintyo = {}
sintyo_time = {}
kensyo = {}
api_key = str(os.environ["YOUTUBE_API"])
with open("abc.json", "r") as json_file:
    sintyo = json.load(json_file)
with open("abc_t.json", "r") as json_file:
    sintyo_time = json.load(json_file)
with open("ken.json", "r") as json_file:
    kensyo = json.load(json_file)
with open("com.json", "r") as json_file:
    com = json.load(json_file)
api = key_tweepy_proc()
set_count = 1
redy_t = time.time()
zen = 0
zen_2 = 0
@tasks.loop(seconds=60)
async def loop():

def get_videos_search(keyword):
    youtube = build('youtube', 'v3', developerKey=api_key)
    youtube_query = youtube.search().list(q=keyword, part='id,snippet', maxResults=1)
    youtube_res = youtube_query.execute()
    return youtube_res.get('items', [])

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl':  "sample_music" + '.%(ext)s',
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
         'preferredquality': '192'},
        {'key': 'FFmpegMetadata'},
    ],
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
sound_dict = {"soren":"bgm.mp3","youtube":"sample_music.mp3","heiten":"heiten.mp3"}
discord_token = str(os.environ["DISCORD_TOKEN"])# Discordbotのアクセストークンを入力
vc_id = 705439556140531819 # 特定のボイスチャンネルを指定
youtube_url = 'https://www.youtube.com/watch?v=FIw-HUP7XK0' # youtubeのURLを指定
client = discord.Client()

def check(m):
            return m.content == 'hello' and m.channel == channel

async def start_music():
    voice_client = await (client.get_channel(vc_id)).connect(reconnect=False)
    voice_client.play(discord.FFmpegPCMAudio(source=sound_dict["youtube"]))
    sleep_time = MP3(sound_dict["youtube"]).info.length + 0.25
    await asyncio.sleep(sleep_time)
    await voice_client.disconnect(force=True)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="botは正常稼働しています"))
    print("ok")

@client.event
async def on_message(message):
    if message.content.startswith("粛清"):
        voice_client = await (client.get_channel(vc_id)).connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio(source=sound_dict["soren"]))
        sleep_time = MP3(sound_dict["soren"]).info.length + 0.25
        await asyncio.sleep(sleep_time)
        await voice_client.disconnect(force=True)
    if  message.content == '/youtube':
        if sintyo[str(message.author.id)] > 9:    
            print("123")
            await message.channel.send("検索したいワードを入力してください")
            abc = await client.wait_for("message")
            dfg = abc.content
            dfg_str = str(dfg)
            result = get_videos_search(dfg_str)
            for item in result:
                if item['id']['kind'] == 'youtube#video':
                    print(item['snippet']['title'])
                    print('https://www.youtube.com/watch?v=' + item['id']['videoId'])
                    url_re = 'https://www.youtube.com/watch?v=' + item['id']['videoId'] + "&sp=EgIQAQ%253D%253D"
                else:
                    print("No video")
            title_you = "```" + item['snippet']['title'] + "```\n"
            await message.channel.send(title_you)
            await message.channel.send("ダウンロード中\n")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_re])
            await message.channel.send("ダウンロード完了\n")
            await message.channel.send("再生開始\n")
            voice_client = await (client.get_channel(vc_id)).connect(reconnect=False)
            voice_client.play(discord.FFmpegPCMAudio(source=sound_dict["youtube"]))
            sleep_time = MP3(sound_dict["youtube"]).info.length + 0.25
            await asyncio.sleep(sleep_time)
            await voice_client.disconnect(force=True)
        else:
            await message.channel.send("お前にはまだこの機能は早い。出直してきな！")
    if  message.content == "/再開":
        await message.channel.send("再生します")
        message.guild.voice_client.resume()
    if  message.content == "/一時停止":
        await message.channel.send("停止します")
        message.guild.voice_client.pause()
    if  message.content == "/停止":
        await message.channel.send("停止します")
        message.guild.voice_client.stop()
        voice_client = await (client.get_channel(vc_id)).connect(reconnect=False)
        await voice_client.disconnect(force=True)
    if  message.content.startswith("/進捗申請:") or message.content.startswith("/pro"):
        msg_co = message.content
        msg_co = msg_co.replace("/進捗申請:","")
        msg_co = msg_co.replace("/pro","")
        mes_id = str(message.author.id)
        if mes_id in sintyo:
            print("add")
            now_time = time.time()
            if now_time - sintyo_time[mes_id] > 3600:
                sintyo[mes_id] +=1
                sintyo_time[mes_id] = time.time()
                await message.channel.send(message.author.mention + "\n進捗承りました\n```" + msg_co + "```")
                with open("abc.json", 'w') as outfile:
                    json.dump(sintyo, outfile)
                with open("abc_t.json", 'w') as outfile:
                    json.dump(sintyo_time, outfile)
            else:
                nownowtime = 60 - ((time.time() - sintyo_time[mes_id]) / 60)
                await message.channel.send(message.author.mention + "\n進捗申請は一時間に一回のみです" + "\n前回の申請時刻は"+ str(datetime.fromtimestamp(sintyo_time[mes_id])) + "です" + "\nあと" + str(nownowtime) + "分で申請できます")
        else:
            print("newmem")
            sintyo[mes_id] = 1
            sintyo_time[mes_id] = time.time()
            with open("abc.json", 'w') as outfile:
                json.dump(sintyo, outfile)
            with open("abc_t.json", 'w') as outfile:
                json.dump(sintyo_time, outfile)
            await message.channel.send(message.author.mention + "\n進捗承りました\n```" + msg_co + "```")
    if  message.content.startswith("/進捗確認"):
        re_sintyo = ""
        sintyo_so = sorted(sintyo.items(), key=lambda x:x[1], reverse=True)
        sintyo_di = dict(sintyo_so)
        for k, v, in sintyo_di.items():
            k = str(k)
            v = str(v)
            mensyon_m = await client.fetch_user(k)
            mensyon = mensyon_m.name
            re_sintyo += mensyon + " ```進捗数:" + v + "```"
        embed = discord.Embed(title="進捗ポイント一覧",description=re_sintyo,color=0xff0000)
        await message.channel.send(embed=embed)
    if  message.content.startswith("/丁半"):
        await message.channel.send("この機能は進捗ポイントを使いますよろしいですか？(Y/N)")
        abc = await client.wait_for("message")
        dfg = abc.content
        dfg_str = str(dfg)
        if dfg_str == "Y":
            await message.channel.send("掛け金をどうぞ")
            abc = await client.wait_for("message")
            dfg = abc.content
            dfg_int = int(dfg)
            if sintyo[str(message.author.id)] >= dfg_int:
                sintyo[str(message.author.id)] -= dfg_int
                await message.channel.send("丁半どっちにする？")
                abc = await client.wait_for("message")
                dfg = abc.content
                dfg_str = str(dfg)
                if dfg_str == "丁":
                    ans = random.randint(0,1)
                    if ans == 0:
                        await message.channel.send("結果は丁大当たり！！")
                        sintyo[str(message.author.id)] += 2*dfg_int
                    else:
                        await message.channel.send("残念半　はずれ！")
                if dfg_str == "半":
                    ans = random.randint(0,1)
                    if ans == 0:
                        await message.channel.send("結果は半大当たり！！")
                        sintyo[str(message.author.id)] += 2*dfg_int
                    else:
                        await message.channel.send("残念丁　はずれ！")
            else:
                await message.channel.send("掛け金が所持金より大きいよ！やり直し！")
                return
        else:
            await message.channel.send("また来てね")
            return
    if message.content == "/tws":
        await message.channel.send("検索ワードを入力")
        abc = await client.wait_for("message")
        dfg = abc.content
        
        results = api.search(q=dfg, count=set_count)
        for result in results:
            username = result.user._json['screen_name']
            status_n = result._json['id']
            url_r = "https://twitter.com/" + username + "/status/" + str(status_n)
        await message.channel.send(url_r)
    if message.content == "/毎日ジャンボ":
        await message.channel.send("何番にするんだい？(2桁)")
        abc = await client.wait_for("message")
        dfg = abc.content
        dfg_str = str(dfg)
        sintyo[str(message.author.id)] -= 3
        await message.author.send("```" + dfg + "```番だね！！")
        await message.author.send("この画面をスクリーンショットしておいてね！\nしてないと無効だよ！")
    if message.content == "/334":
        dt_now = datetime.now()
        dt_now = str(dt_now)
        await message.channel.send(message.author.mention + "```" + dt_now + "```です")
        await message.channel.send("なんでや、阪神関係ないやろ！")
    if message.content == "/check":
        abc = client.latency
        abc = str(abc*1000)
        await message.channel.send(abc + "ms")
    if  message.content.startswith("/gives"):
        b = message.content
        dfg = b.replace("/gives ","")
        fgh = dfg.replace("<@!","")
        fgh2 = fgh.replace("<@","")
        jkl = fgh2.replace(">","")
        await message.channel.send("何ポイント送る？")
        abc = await client.wait_for("message")
        po_i = abc.content
        po_i = int(po_i)
        cnf = int(jkl)
        print(cnf)
        user = client.get_user(cnf)
        if po_i < 0:
            await message.channel.send("減らせねーよばーか")
            return
        sintyo[str(message.author.id)] -= po_i
        sintyo[jkl] += po_i
        embed=discord.Embed(title="ポイント転送", description="ポイントの転送を行いました", color=0xff0000)
        embed.add_field(name= user.name + "に", value=str(po_i) + "ポイント", inline=False)
        embed.set_footer(text="ポイント管理者")
        await message.channel.send(embed=embed)
    if message.content.startswith("/チート"):
        if message.author.id == 676319964776366080:
            b = message.content.replace("/チート ","")
            await message.channel.send("ポイントを付与します")
            sintyo["676319964776366080"] = int(b)
        else:
            await message.channel.send("所持金を没収します。\nはっはっは、だまされたなｗｗｗｗ")
            print(sintyo[str(message.author.id)])
    if message.content == "/終末時計":
        await message.channel.send("あと30分です")
    if message.content.startswith("/make"):
        id_m = message.author.id
        b = message.content.replace("/make ","")
        if b == "":
            await message.channel.send("もう一度おやりください")
            return
        if b in com:
            await message.channel.send("すでに登録されてる為、上書きします")
        await message.channel.send("何を送る？")
        while True:
            abc = await client.wait_for("message")
            if abc.author.id == id_m:
                mes = abc.content
                print("終わり")
                break
            print("次")
        print(mes)
        if mes in com:
            await message.channel.send("暴走の恐れがあるので登録できません")
            return
        com[b] = mes
        print(com[b])
        await message.channel.send(b+"を"+mes + "に設定しました。")
        with open("com.json", 'w') as outfile:
            json.dump(com, outfile)
    if message.content in com:
        await message.channel.send(com[message.content])
    if message.content == "/exit":
        exit()
    if message.content.startswith("/delete"):
        b = message.content.replace("/delete","")
        com.pop[b]
loop.start()
client.run(discord_token)
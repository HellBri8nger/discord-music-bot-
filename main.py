import discord
from discord.ext import commands as disect
import asyncio
from youtube_dl import YoutubeDL
import embeds
from discord.ui import Select, View
from youtube_search import YoutubeSearch
import json

Prefix = "-"
bot = disect.Bot(command_prefix=Prefix, intents=discord.Intents.all(), case_insensitive=True, self_bot=False)
song_list = []
voice_client = ()
song_names = []
forqueue = ''
duration = []
searchlist = ''
tempvar = []
results = []
urls = []
search_names = []
yt = 'https://youtube.com'
sd = 'Song Duration: '

ytdl_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {'options': "-vn"}
ytdl = YoutubeDL(ytdl_options)

def forque():
    global forqueue
    if forqueue == '':
        for i in range(len(song_names)):
            forqueue = forqueue + '**__'
            forqueue = forqueue + str(i + 1)
            forqueue = forqueue + '.'
            forqueue = forqueue + str(song_names[i])
            forqueue = forqueue + '__**'
            forqueue = forqueue + '\n'
    else:
        forqueue = ''
        forque()

@bot.command()
async def display(ctx):
    playing = discord.Embed(
        title='Now Playing: '+song_names[0],
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=playing)

@bot.command()
async def coinflip(ctx):
    flipcoin = asyncio.create_task(embeds.displaycoinflip(ctx))

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Streaming(name="The death of criminals",url='https://www.youtube.com/watch?v=g1PePr8hAsc&t%27'))

lopsong = 0
@bot.command()
async def loop(ctx):
    global lopsong

    if lopsong == 0:
        loopsong = asyncio.create_task(embeds.displaylooping(ctx))
        lopsong = 1
    else:
        loopoff = asyncio.create_task(embeds.displayloopoff(ctx))
        lopsong = 0


@bot.command()
async def songfunc(ctx):
    looop = asyncio.get_event_loop()
    data = await looop.run_in_executor(None, lambda: ytdl.extract_info(song_list[0], download=False))

    song = data['url']
    print('The song is %s seconds long' %data['duration'])
    source = discord.FFmpegPCMAudio(song, **ffmpeg_options,
                                    executable=r'C:\Users\rikki\Documents\code2\musicbot\ffmpeg\bin\ffmpeg.exe')

    print('playing')
    if not voice_client.is_playing():
        showplayingnow = asyncio.create_task(display(ctx))
        fut = asyncio.Future()
        voice_client.play(source, after=fut.set_result)
        await fut
        await asyncio.sleep(2)
        print('waiting')
        if lopsong == 0:
            song_list.pop(0)
            song_names.pop(0)
        forque()
    else:
        print('Tried to play while already playing')

    for i in range(len(song_list)):
        global task
        task = asyncio.create_task(songfunc(ctx))


@bot.command()
async def play(ctx):
    try:
        author_channel = ctx.author.voice.channel
    except:
        await ctx.send('Get inside a voice channel fool')

    if author_channel is None:
        await ctx.send('Get inside a voice channel bitch')
    else:
        try:
            global voice_client
            voice_client = await ctx.author.voice.channel.connect()

        except Exception as err:
            if author_channel is None:
                await ctx.send('Get inside a vc bitch')
            print(err)

        if len(song_list) <= 0:
            await ctx.send('No songs in the queue, add them using the add function')
        else:
            global task
            task = asyncio.create_task(songfunc(ctx))

@bot.command()
async def add(ctx, *, url=None):
    if url == None:
        await ctx.channel.send('Send a youtube url you mongol')

    try:
        url1 = url.startswith('https://www.youtube') or ('https://youtube')

        if url1 is False:
            await ctx.channel.send('Ever heard of a Youtube url? yeah send that maybe')
        else:
            global song_list, song_names
            song_list.append(url)
            added = asyncio.create_task(embeds.displayadded(ctx))
            print(song_list)

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song_names.append(data['title'])
            forque()

    except Exception as err:
        print(err)


@bot.command()
async def displayqueue(ctx):
    try:
        queue1 = discord.Embed(
            title='Queue',
            colour=discord.Colour.dark_gold(),
            description=forqueue

        )
        queue1.set_footer(text='Now Playing: ' + song_names[0])

        await ctx.send(embed=queue1)

    except:
        queue1 = discord.Embed(
            title='Queue is Empty',
            colour=discord.Colour.dark_gold()
        )
        await ctx.send(embed=queue1)

@bot.command()
async def queue(ctx):
    que = asyncio.create_task(displayqueue(ctx))
    forqueue = ''
    print(forqueue)

@bot.command()
async def skip(ctx):
    ctx.voice_client.stop()
    paused = asyncio.create_task(embeds.displayskip(ctx))
    song_list.pop(0)
    song_names.pop(0)
    global task
    task = asyncio.create_task(songfunc(ctx))

@bot.command()
async def dc(ctx):
    await ctx.voice_client.disconnect()
    disconnected = asyncio.create_task(embeds.displaydisconnected(ctx))


@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()
    paused = asyncio.create_task(embeds.displaypause(ctx))


@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()
    resumed = asyncio.create_task(embeds.displayresume(ctx))

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down bot!")
    await bot.close()

def srchlist():
    global searchlist
    searchlist = ''
    print(searchlist)
    for i in range(len(search_names)):
        searchlist = searchlist + '``'
        searchlist = searchlist + str(i + 1)
        searchlist = searchlist + '.'
        searchlist = searchlist + '``'
        searchlist = searchlist + str(search_names[i])
        searchlist = searchlist + '\n\n'

@bot.command()
async def search(ctx, *, srch=None):
    global searchlist, duration, search_names
    if srch == None:
        await ctx.send('What am I supposed to search for? Specify something')

    else:
        results = YoutubeSearch(srch, max_results=10).to_dict()
        search_names.clear()
        for i in range(len(results)):
            tempvar = json.loads(json.dumps(results[i]))
            search_names.append(tempvar['title'])
        searchlist = ''
        print(searchlist)
        srchlist()

        duration.clear()
        for i in range(len(results)):
            tempvar2 = json.loads(json.dumps(results[i]))
            duration.append(tempvar2['duration'])

        urls.clear()
        for i in range(len(results)):
            tempvar3 = json.loads(json.dumps(results[i]))
            urls.append(tempvar3['url_suffix'])

        searchembed = asyncio.create_task(select(ctx))

@bot.command()
async def select(ctx):
    global song_names, duration, searchlist

    qs1 = discord.Embed(
        title='Tracks',
        colour=discord.Colour.dark_gold(),
        description=searchlist

    )

    slc = Select(
        placeholder="Choose a song",
        options=[
            discord.SelectOption(
                label='1.' + search_names[0],
                description='Song Duration: ' + duration[0],
                value=yt + urls[0]
            ),
            discord.SelectOption(
                label='2.' + search_names[1],
                description='Song Duration: ' + duration[1],
                value=yt + urls[1]
            ),
            discord.SelectOption(
                label='3.' + search_names[2],
                description='Song Duration: ' + duration[2],
                value=yt + urls[2]
            ),
            discord.SelectOption(
                label='4.' + search_names[3],
                description='Song Duration: ' + duration[3],
                value=yt + urls[3]
            ),
            discord.SelectOption(
                label='5.' + search_names[4],
                description='Song Duration: ' + duration[4],
                value=yt + urls[4]
            ),
            discord.SelectOption(
                label='6.' + search_names[5],
                description='Song Duration: ' + duration[5],
                value=yt + urls[5]
            ),
            discord.SelectOption(
                label='7.' + search_names[6],
                description='Song Duration: ' + duration[6],
                value=yt + urls[6]
            ),
            discord.SelectOption(
                label='8.' + search_names[7],
                description='Song Duration: ' + duration[7],
                value=yt + urls[7]
            ),
            discord.SelectOption(
                label='9.' + search_names[8],
                description='Song Duration: ' + duration[8],
                value=yt + urls[8]
            ),
            discord.SelectOption(
                label='10.' + search_names[9],
                description='Song Duration: ' + duration[9],
                value=yt + urls[9]
            )
        ]
    )

    async def mycallback(interaction):
        await interaction.response.defer(thinking=False)  # fails if this isn't used P.S: learn about interactions later
        added = asyncio.create_task(embeds.displayadded(ctx))
        lep = asyncio.get_event_loop()
        data = await lep.run_in_executor(None, lambda: ytdl.extract_info(slc.values[0], download=False))

        print(slc.values)
        song_names.append(data['title'])
        song_list.append(slc.values[0])
        forque()

    slc.callback = mycallback
    show = View()
    show.add_item(slc)

    await ctx.send(embed=qs1, view=show)


bot.run("INSERT TOKEN")

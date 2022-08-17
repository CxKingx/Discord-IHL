import os
import discord
#import datetime,timedelta
from datetime import datetime,timedelta
#import pytz
#import time
from discord.ext import commands, tasks
from DotaQue import QueSystem

my_secret = os.environ['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())
newQue = QueSystem()


@bot.event
async def on_ready():
    print('We have logged in as  {0.user}'.format(bot))


@bot.command(name='test', help='Hello')
async def test(ctx):
    #print(ctx)

    list1 = ['241817188665786369','703509731951640578','306836076641910785','689507286695018526']
    list2 = ['241817188665786369','689507286695018526','285002675462995968','847019941211144213']
    #await ctx.send(f'Hello 🎉 {ctx.message.author.name}!')
    intersection = set(list1).intersection(list2)
    print(list(intersection))

@tasks.loop(minutes =1)
async def CheckQPeriodically():
    #print('doin smth')
    #channel = bot.get_channel(979033486340010015) #Cx Bot Test
    guild = bot.get_guild(1002116096033308723)

    today = datetime.today()  # 22:20
    #await channel.send("Check Every 1 minutes \n The current time in Jakarta is :" + str(today))

    QueCopy = newQue.ParticipantDict
    for x in QueCopy:
        #print('Check User expiry')
        if today>x[1]:
            #await channel.send('removing <@!' + str(x[0]) + '> \n')
            #print('removing dis')

            newQue.RemoveData(x)
            embedVar = newQue.EditQueMessage()
            await newQue.messageObject.edit(embed=embedVar)

            if bot.get_user(int(x[0])) is not None:
                #print('success send')
                member = bot.get_user(int(x[0]))
                #member = guild.get_member(str(x[0]))
                try:
                    await member.send('You have been removed automatically for timerug prevention, requeue if you still want to join')
                except:
                    print('Failed to Send Message')


# @bot.command(name='getTime', help='Hello')
# async def getTime(ctx):
#     current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
#     today = datetime.today() #22:20
#
#     timeAft = today + timedelta(minutes=25) #22:45
#     MaxTime = today - timedelta(minutes=30) # 21:50
#     #today   = today + timedelta(minutes=30) #22:50
#     print("The current time in Jakarta is :", current_time)
#     await ctx.send("The current time in Jakarta is :"+str(current_time))
#     await ctx.send("30min Aft is " + str(timeAft))
#     await ctx.send("30min B4 is " + str(MaxTime))
#
#     if today>MaxTime:
#         await ctx.send("Past the Max Time")
#
#     #if today>timeeB4:
#         #await ctx.send("its definitely after")
#     #curr_time = time.strftime("%H:%M:%S", time.localtime())
#     #print("Current Time is :", curr_time)
#     #await ctx.send("Current Time is : "+str(curr_time))
#
#     #time.sleep(5)
#
#     #curr_time2 = time.strftime("%H:%M:%S", time.localtime())
#     #print("Current Time is :", curr_time2)
#     #await ctx.send("Current Time is : " + str(curr_time2))
#
#     #await ctx.send("Cur time minus = "+ int(curr_time)+" 2 "+int(curr_time2)+" = "+(int(curr_time)-int(curr_time2)))


@bot.command(name='delmsg' , hidden=True)
async def delmsg(ctx, messageID):
    await ctx.message.delete()
    original = await ctx.channel.fetch_message(messageID)
    # newmsg = message.channel.fetch_message(split_message[1])
    await original.delete()


@bot.command(name='endQ', help='End a Dota Que')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def endQ(ctx):
    if newQue.QueExist:
        channel = bot.get_channel(newQue.ChannelID)
        await newQue.messageObject.delete()
        newQue.ResetQue()
    else:
        await ctx.send('no que to end')
    CheckQPeriodically.stop()




@bot.command(name='startQ', help='Start a Dota Que')
#@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def startQ(ctx):
    newQue.SetChannelID(1002156714365296701)
    newQue.ResetQue()
    # drazz ev = 979725539243880498
    # test ev = 997895036509364274
    # goblin = 1002156714365296701
    #Kuul Tesat = 847409872324657153

    # guild = bot.get_guild(846380741209620480) #846380741209620483 gen 979033486340010015 bot
    channel = bot.get_channel(newQue.ChannelID)
    embedVar = newQue.StartQue()
    messageObject = await channel.send(embed=embedVar)
    emoji = '<:watamepog:781536094591123546>'
    await messageObject.add_reaction(emoji)

    print('Que message id is ' + str(messageObject.id))
    newQue.RegisterMessage(messageObject)

    CheckQPeriodically.start()

@bot.command(name='pingQ', help='Ping the Queres')
@commands.cooldown(1, 30, commands.BucketType.user)
async def pingQ(ctx):
    print(newQue.QueLimit)
    print(len(newQue.ParticipantDict))
    remaining_Slot = newQue.QueLimit - len(newQue.ParticipantDict)
    await ctx.send(
        ' <@&1002124426696994857> +' + str(remaining_Slot) + ' go to <#' + str(newQue.ChannelID) + '> to join the que')


@bot.command(name='getQ', help='Get Current Que')
async def getQ(ctx):
    embedVar = newQue.GetCurrentQue()
    await ctx.send(embed=embedVar)


# @bot.command(name='refreshQ', help='Refresh Current Que')
# async def refreshQ(ctx):
#     await newQue.messageObject.delete()
#     channel = bot.get_channel(newQue.ChannelID)
#
#     # embedVar = newQue.StartQue()
#     embedVar = newQue.EditQueMessage()
#     messageObject = await channel.send(embed=embedVar)
#     emoji = '<:watamepog:781536094591123546>'
#     await messageObject.add_reaction(emoji)
#
#     print('Que message id is ' + str(messageObject.id))
#     newQue.RegisterMessage(messageObject)


# @bot.command(name='removeQ', help='Remove a user in the Current Que')
# @commands.has_role("mod")
# async def remove(ctx, user: discord.Member = None):
#     print(user)
#     if user:
#         print('removing user')
#         newQue.RemoveUser(user)
#         embedVar = newQue.EditQueMessage()
#         # print('mesg object is'+ str(newQue.messageObject))
#         await newQue.messageObject.edit(embed=embedVar)
#     else:
#         ctx.send('no user removed')


@bot.event
async def on_raw_reaction_add(payload):
    #print(payload.message_id)
    channel = bot.get_channel(newQue.ChannelID)
    today = datetime.today()  # 22:20
    MaxTimeRemove = today + timedelta(minutes=30)  # 22:45
    guild = bot.get_guild(payload.guild_id)

    if payload.member.id != bot.user.id:
        print('its a user')
        if str(payload.message_id) == str(newQue.messageObject.id):
            if newQue.CheckUserInQue(payload.user_id):
                print('nothing')
            else:

                newQue.AddData((payload.user_id,MaxTimeRemove))

                if (newQue.CheckPop()):
                    await newQue.messageObject.delete()
                    await channel.send('Queue has popped ,participants are')
                    await channel.send(newQue.PopQue())
                    #reset Que
                    newQue.ResetQue()
                    embedVar = newQue.StartQue()
                    messageObject = await channel.send(embed=embedVar)
                    emoji = '<:watamepog:781536094591123546>'
                    await messageObject.add_reaction(emoji)
                    print('Que message id is ' + str(messageObject.id))
                    newQue.RegisterMessage(messageObject)
                else:
                    embedVar = newQue.EditQueMessage()
                    await newQue.messageObject.edit(embed=embedVar)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    channel = bot.get_channel(979033486340010015)

    #print('ReactMSG ID = ' + str(payload.message_id) + ' QueMSGID= ' + str(newQue.messageObject.id))
    if str(payload.message_id) == str(newQue.messageObject.id):

        UsertoRemove = newQue.GetUser(member)
        newQue.RemoveData(UsertoRemove)

        embedVar = newQue.EditQueMessage()
        await newQue.messageObject.edit(embed=embedVar)


@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    # split_message = user_message.split()
    channel = str(message.channel.name)
    channelID = str(message.channel.id)
    # channel_nsfw = message.channel.is_nsfw()
    #print(f'{username}: {user_message} ({channel})')
    # if message.author == bot.user:
    # return
    if message.author == bot.user:
        return

    await bot.process_commands(message)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
bot.run(my_secret)

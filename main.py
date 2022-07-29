import os
import discord
from discord.ext import commands
from DotaQue import QueSystem

my_secret = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())

newQue = QueSystem()
lowQue = QueSystem()
highQue = QueSystem()


@bot.event
async def on_ready():
    print('We have logged in as  {0.user}'.format(bot))
    # print('alo')


@bot.command(name='test', help='Hello')
async def test(ctx):
    #print(ctx)
    #print(str(ctx))
    #print(message)
    list1 = ['241817188665786369','703509731951640578','306836076641910785','689507286695018526']
    list2 = ['241817188665786369','689507286695018526','285002675462995968','847019941211144213']
    #await ctx.send(f'Hello 🎉 {ctx.message.author.name}!')
    intersection = set(list1).intersection(list2)
    print(list(intersection))


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


@bot.command(name='endQH', help='End a Dota Que')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def endQH(ctx):
    if highQue.QueExist:
        channel = bot.get_channel(newQue.ChannelID)
        await highQue.messageObject.delete()
        highQue.ResetQue()
    else:
        await ctx.send('no que to end')


@bot.command(name='endQL', help='End a Dota Que')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def endQL(ctx):
    if lowQue.QueExist:
        channel = bot.get_channel(newQue.ChannelID)
        await lowQue.messageObject.delete()
        lowQue.ResetQue()
    else:
        await ctx.send('no que to end')


@bot.command(name='startQ', help='Start a Dota Que')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def startQ(ctx):
    newQue.SetChannelID(1002156714365296701)
    newQue.ResetQue()
    # drazz ev = 979725539243880498
    # test ev = 997895036509364274
    # thread ev = 999545012918419526
    # AU All = 999547326211305542
    # AU 2 ALL = 999592344556929125

    # guild = bot.get_guild(846380741209620480) #846380741209620483 gen 979033486340010015 bot
    channel = bot.get_channel(newQue.ChannelID)
    embedVar = newQue.StartQue()
    messageObject = await channel.send(embed=embedVar)
    emoji = '<:watamepog:781536094591123546>'
    await messageObject.add_reaction(emoji)

    print('Que message id is ' + str(messageObject.id))
    newQue.RegisterMessage(messageObject)


@bot.command(name='startQH', help='Start a Dota Que')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def startQHigh(ctx):
    highQue.SetChannelID(999592351255253052)
    highQue.ResetQue()
    #drazz High = 998586010143293470
    # test high = 998140272007454740
    # AU High = 999547705590300692
    # AU2 High = 999592351255253052

    # guild = bot.get_guild(846380741209620480) #846380741209620483 gen 979033486340010015 bot
    channel = bot.get_channel(highQue.ChannelID)

    embedVar = highQue.StartQue()
    messageObject = await channel.send(embed=embedVar)
    emoji = '<:watamepog:781536094591123546>'
    await messageObject.add_reaction(emoji)

    print('Que message id is ' + str(messageObject.id))
    highQue.RegisterMessage(messageObject)


@bot.command(name='startQL', help='Start a Dota Que')
@commands.has_any_role("MOD", 'mod', 'Moderators', 'Admin','Goblin king','Goblin giants')
async def startQLow(ctx):
    lowQue.SetChannelID(999592483942060043)
    lowQue.ResetQue()
    # drazz low = 998586036106043444
    # test low = 998140316601307216
    # AU Low = 999547464325546024
    # AU2 Low = 999592483942060043

    channel = bot.get_channel(lowQue.ChannelID)

    embedVar = lowQue.StartQue()
    messageObject = await channel.send(embed=embedVar)
    emoji = '<:watamepog:781536094591123546>'
    await messageObject.add_reaction(emoji)

    print('Que message id is ' + str(messageObject.id))
    lowQue.RegisterMessage(messageObject)


@bot.command(name='pingQ', help='Ping the Queres')
async def pingQ(ctx):
    remaining_Slot = newQue.QueLimit - len(newQue.CurrentQue)
    await ctx.send(
        '<@&997892212882931872> +' + str(remaining_Slot) + ' go to <#' + str(newQue.ChannelID) + '> to join the que')


@bot.command(name='getQ', help='Get Current Que')
async def getQ(ctx):
    embedVar = newQue.GetCurrentQue()
    await ctx.send(embed=embedVar)


@bot.command(name='refreshQ', help='Refresh Current Que')
async def refreshQ(ctx):
    await newQue.messageObject.delete()
    channel = bot.get_channel(newQue.ChannelID)

    # embedVar = newQue.StartQue()
    embedVar = newQue.EditQueMessage()
    messageObject = await channel.send(embed=embedVar)
    emoji = '<:watamepog:781536094591123546>'
    await messageObject.add_reaction(emoji)

    print('Que message id is ' + str(messageObject.id))
    newQue.RegisterMessage(messageObject)


@bot.command(name='removeQ', help='Remove a user in the Current Que')
@commands.has_role("mod")
async def remove(ctx, user: discord.Member = None):
    print(user)
    if user:
        print('removing user')
        newQue.RemoveUser(user)
        embedVar = newQue.EditQueMessage()
        # print('mesg object is'+ str(newQue.messageObject))
        await newQue.messageObject.edit(embed=embedVar)
    else:
        ctx.send('no user removed')


@bot.event
async def on_raw_reaction_add(payload):
    print(payload)
    print(payload.message_id)
    channel = bot.get_channel(newQue.ChannelID)
    channelLow = bot.get_channel(lowQue.ChannelID)
    channelHigh = bot.get_channel(highQue.ChannelID)
    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name="Immortal")
    role2 = discord.utils.get(guild.roles, name="IHL blacklist")
    if payload.member.id != bot.user.id:
        print('its a user')
        if str(payload.message_id) == str(newQue.messageObject.id):
            if newQue.CheckUserInQue(payload.user_id):
                print('nothing')
            else:
                newQue.AddUser(payload.user_id)
                if (newQue.CheckPop()):
                    await newQue.messageObject.delete()
                    await channel.send('Queue has popped ,participants are')
                    await channel.send(newQue.PopQue())

                    #Check High and Low and remove ppl from there
                    PoppedQue = newQue.CurrentQue
                    HighQueCopy = highQue.CurrentQue
                    LowQueCopy = lowQue.CurrentQue

                    highMultiple = set(PoppedQue).intersection(HighQueCopy)
                    lowMultiple = set(PoppedQue).intersection(LowQueCopy)

                    if highMultiple:
                        for x in highMultiple:
                            highQue.RemoveUserInt(x)
                            embedVar = highQue.EditQueMessage()
                            # print('mesg object is'+ str(newQue.messageObject))
                        await highQue.messageObject.edit(embed=embedVar)

                    if lowMultiple:
                        for x in lowMultiple:
                            lowQue.RemoveUserInt(x)
                            embedVar = lowQue.EditQueMessage()
                            # print('mesg object is'+ str(newQue.messageObject))
                        await lowQue.messageObject.edit(embed=embedVar)

                    #reset Que
                    newQue.ResetQue()
                    # embedVar = newQue.StartQue()
                    # messageObject = await channel.send(embed=embedVar)
                    # emoji = '<:watamepog:781536094591123546>'
                    # await messageObject.add_reaction(emoji)
                    # print('Que message id is ' + str(messageObject.id))
                    # newQue.RegisterMessage(messageObject)
                else:
                    embedVar = newQue.EditQueMessage()
                    await newQue.messageObject.edit(embed=embedVar)
        # High Q is Popped
        elif str(payload.message_id) == str(highQue.messageObject.id):
            if highQue.CheckUserInQue(payload.user_id):
                print('nothing')
            else:
                highQue.AddUser(payload.user_id)
                if (highQue.CheckPop()):
                    await highQue.messageObject.delete()
                    await channelHigh.send('Queue has popped ,participants are')
                    await channelHigh.send(highQue.PopQue())
                    # Check Everyone and Low and remove ppl from there
                    PoppedQue = highQue.CurrentQue
                    EveryoneCopy = newQue.CurrentQue
                    LowQueCopy = lowQue.CurrentQue

                    EvMultiple = set(PoppedQue).intersection(EveryoneCopy)
                    lowMultiple = set(PoppedQue).intersection(LowQueCopy)
                    if EvMultiple:
                        for x in EvMultiple:
                            newQue.RemoveUserInt(x)
                            embedVar = newQue.EditQueMessage()
                            # print('mesg object is'+ str(newQue.messageObject))
                        await newQue.messageObject.edit(embed=embedVar)

                    if lowMultiple:

                        for x in lowMultiple:
                            lowQue.RemoveUserInt(x)
                            embedVar = lowQue.EditQueMessage()
                         # print('mesg object is'+ str(newQue.messageObject))
                        await lowQue.messageObject.edit(embed=embedVar)
                    # reset Que
                    highQue.ResetQue()
                    # embedVar = highQue.StartQue()
                    # messageObject = await channelHigh.send(embed=embedVar)
                    # emoji = '<:watamepog:781536094591123546>'
                    # await messageObject.add_reaction(emoji)
                    # print('Que message id is ' + str(messageObject.id))
                    # highQue.RegisterMessage(messageObject)
                else:
                    embedVar = highQue.EditQueMessage()
                    await highQue.messageObject.edit(embed=embedVar)
        # Low Q is popped
        elif str(payload.message_id) == str(lowQue.messageObject.id):
            if lowQue.CheckUserInQue(payload.user_id):
                print('nothing')
            else:
                lowQue.AddUser(payload.user_id)
                if (lowQue.CheckPop()):
                    await lowQue.messageObject.delete()
                    await channelLow.send('Queue has popped ,participants are')
                    await channelLow.send(lowQue.PopQue())
                    # Check High and Everyone and remove ppl from there
                    PoppedQue = lowQue.CurrentQue
                    EveryoneCopy = newQue.CurrentQue
                    HighQueCopy = highQue.CurrentQue

                    EvMultiple = set(PoppedQue).intersection(EveryoneCopy)
                    HighMultiple = set(PoppedQue).intersection(HighQueCopy)
                    if EvMultiple:
                        for x in EvMultiple:
                            newQue.RemoveUserInt(x)
                            embedVar = newQue.EditQueMessage()
                            # print('mesg object is'+ str(newQue.messageObject))
                        await newQue.messageObject.edit(embed=embedVar)
                    if HighMultiple:
                        for x in HighMultiple:
                            highQue.RemoveUserInt(x)
                            embedVar = highQue.EditQueMessage()
                            # print('mesg object is'+ str(newQue.messageObject))
                        await highQue.messageObject.edit(embed=embedVar)
                    # reset Que
                    lowQue.ResetQue()
                    # embedVar = lowQue.StartQue()
                    # messageObject = await channelLow.send(embed=embedVar)
                    # emoji = '<:watamepog:781536094591123546>'
                    # await messageObject.add_reaction(emoji)
                    # print('Que message id is ' + str(messageObject.id))
                    # lowQue.RegisterMessage(messageObject)
                else:
                    embedVar = lowQue.EditQueMessage()
                    await lowQue.messageObject.edit(embed=embedVar)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    channel = bot.get_channel(979033486340010015)
    # print('paylod is '+str(payload))
    print('ReactMSG ID = ' + str(payload.message_id) + ' QueMSGID= ' + str(newQue.messageObject.id))
    if str(payload.message_id) == str(newQue.messageObject.id):
        print(newQue.CurrentQue)
        newQue.RemoveUser(member)
        embedVar = newQue.EditQueMessage()
        # print('mesg object is'+ str(newQue.messageObject))
        await newQue.messageObject.edit(embed=embedVar)
    elif str(payload.message_id) == str(highQue.messageObject.id):
        print(highQue.CurrentQue)
        highQue.RemoveUser(member)
        embedVar = highQue.EditQueMessage()
        # print('mesg object is'+ str(newQue.messageObject))
        await highQue.messageObject.edit(embed=embedVar)
    elif str(payload.message_id) == str(lowQue.messageObject.id):
        print(lowQue.CurrentQue)
        lowQue.RemoveUser(member)
        embedVar = lowQue.EditQueMessage()
        # print('mesg object is'+ str(newQue.messageObject))
        await lowQue.messageObject.edit(embed=embedVar)
    # print('remove reaction')


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

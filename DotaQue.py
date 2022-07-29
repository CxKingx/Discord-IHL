import discord


class QueSystem:

    def __init__(self):
        self.QueExist = False
        self.CurrentQue = []
        self.TimeoutTime = 30
        self.PreviousQue = []
        self.messageObject = 0
        self.QueLimit = 4
        self.ChannelID = 1002156714365296701

        # 981448589115023420 ATDL
        # 979725539243880498 #Draz
        # Goblin

    def SetChannelID(self, newID):
        self.ChannelID = newID

    def StartQue(self):
        print('Starting Que')  # Current Q:
        embedVar = discord.Embed(title="Current Q: ", description='Press the reaction to join ', color=0x00ff00)
        self.QueExist=True
        return embedVar

    def RegisterMessage(self, QueMessageID):
        self.messageObject = QueMessageID
        return

    def CheckUserInQue(self, UserID):
        if any(str(x) == str(UserID) for x in self.CurrentQue):
            print('have same so no add')
            return True
        else:
            print('adding')
            return False
            # self.AddUser(UserID)

    def CheckPop(self):
        if len(self.CurrentQue) >= self.QueLimit:
            return True
        else:
            return False

    def AddUser(self, UserID):
        self.CurrentQue.append(str(UserID))
        # print('cur que is ')
        # print(self.CurrentQue)

    #Remove by mentioning
    def RemoveUser(self, User):
        print('removed from que ' + str(User.id))
        self.CurrentQue.remove(str(User.id))

        # print('cur que is ')
        # print(self.CurrentQue)
        return

    def RemoveUserInt(self, UserID):
        print('removed from que ' + str(UserID))
        self.CurrentQue.remove(str(UserID))

        # print('cur que is ')
        # print(self.CurrentQue)
        return

    def GetCurrentQue(self):
        embedVar = discord.Embed(title="Current Q: " + str(len(self.CurrentQue)) + '/' + str(self.QueLimit),
                                 description='<#'+str(self.ChannelID)+'> to join Que', color=0x00ff00)
        quelist = ''
        if len(self.CurrentQue):
            for x in self.CurrentQue:
                # print(x)
                quelist = quelist + ' <@!' + x + '> \n'
            print(quelist)
            embedVar.add_field(name='\u200b', value=quelist, inline=False)
        else:
            embedVar.add_field(name='\u200b', value='\u200b', inline=False)
        return embedVar

    def EditQueMessage(self):

        embedVar = discord.Embed(title="Current Q: " + str(len(self.CurrentQue)) + '/' + str(self.QueLimit),
                                 description='Press the reaction to join ', color=0x00ff00)
        quelist = ''
        if len(self.CurrentQue):
            for x in self.CurrentQue:
                # print(x)
                quelist = quelist + ' <@!' + x + '> \n'
            print(quelist)
            embedVar.add_field(name='\u200b', value=quelist, inline=False)
        else:
            embedVar.add_field(name='\u200b', value='\u200b', inline=False)
        return embedVar

    def PopQue(self):
        # Put currentQue to Past Que
        # send message
        PopMsg = ''
        for x in self.CurrentQue:
            # print(x)
            PopMsg = PopMsg + ' <@!' + x + '> \n'
        return PopMsg

    def ResetQue(self):
        self.QueExist = False
        self.CurrentQue = []
        self.TimeoutTime = 30
        self.PreviousQue = []
        self.messageObject = 0
        self.QueLimit = 4

import discord


class QueSystem:

    def __init__(self):
        self.QueExist = False
        self.CurrentQue = []
        self.TimeoutTime = 30
        self.PreviousQue = []
        self.messageObject = 0
        self.QueLimit = 10
        self.ChannelID = 1002156714365296701
        self.ParticipantDict = []
        # Goblin 1002156714365296701

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
        if any(str(x[0]) == str(UserID) for x in self.ParticipantDict):
        #if any(str(x) == str(UserID) for x in self.CurrentQue):
            print('have same so no add')
            return True
        else:
            print('adding')
            return False
            # self.AddUser(UserID)

    def CheckPop(self):
        if len(self.ParticipantDict) >= self.QueLimit:
            return True
        else:
            return False


    def AddData(self, UserData):
        print('Added Tuple')
        self.ParticipantDict.append(UserData)
        return

    def RemoveData(self, User):
        print('removed from Tuple que ' + str(User))
        self.ParticipantDict.remove(User)
        return

    def GetUser(self,User):
        print('Get User')
        for x in self.ParticipantDict:
            if str(x[0]) == str(User.id):
                #print('found to remove')
                return x



    def GetCurrentQue(self):
        embedVar = discord.Embed(title="Current Q: " + str(len(self.ParticipantDict)) + '/' + str(self.QueLimit),
                                 description='<#'+str(self.ChannelID)+'> to join Que', color=0x00ff00)
        #print(self.ParticipantDict)
        #for x in self.ParticipantDict:
            #print('x0 is '+str(x[0])+' x1 is '+str(x[1]))
            #print('Types  x0 is ' + type(x[0]) + ' x1 is ' + type(x[1]))
        quelist = ''
        if len(self.ParticipantDict):
            for x in self.ParticipantDict:
                # print(x)
                quelist = quelist + ' <@!' + str(x[0]) + '> \n'
            print(quelist)
            embedVar.add_field(name='\u200b', value=quelist, inline=False)
        else:
            embedVar.add_field(name='\u200b', value='\u200b', inline=False)
        return embedVar


    def EditQueMessage(self):

        embedVar = discord.Embed(title="Current Q: " + str(len(self.ParticipantDict)) + '/' + str(self.QueLimit),
                                 description='Press the reaction to join ', color=0x00ff00)
        quelist = ''
        if len(self.ParticipantDict):
            for x in self.ParticipantDict:
                # print(x)
                quelist = quelist + ' <@!' + str(x[0]) + '> \n'
            print(quelist)
            embedVar.add_field(name='\u200b', value=quelist, inline=False)
        else:
            embedVar.add_field(name='\u200b', value='\u200b', inline=False)
        return embedVar

    def PopQue(self):
        # send message
        PopMsg = ''
        for x in self.ParticipantDict:
            # print(x)
            PopMsg = PopMsg + ' <@!' + str(x[0]) + '> \n'
        return PopMsg

    def ResetQue(self):
        self.QueExist = False
        self.CurrentQue = []
        self.TimeoutTime = 30
        self.PreviousQue = []
        #self.messageObject = 0
        self.QueLimit = 10
        self.ParticipantDict = []

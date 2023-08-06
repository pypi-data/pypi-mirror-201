import asyncio
from enkanetwork import EnkaNetworkAPI,Assets
import asyncio,random,os,datetime
from .src.utils.CreatBannerSix import generationSix
from .src.utils.CreatBannerFive import generationFive
from .src.utils.CreatBannerTree import generationTree
from .src.utils.CreatBannerTwo import generationTwo, creatUserInfo
from .src.utils.CreatBannerOne import generationOne, signature, openUserImg 
from .src.utils.CreatBannerFour import generationFour
from .src.utils.CreatBannerSeven import generationSeven
from .src.utils.userProfile import creatUserProfile
from .src.utils.ArtifactRate import get_artifact_rate

from .src.utils.openFile import change_Font


from .src.utils.translation import translationLang,supportLang
from .enc_error import ENCardError
from .src.modal.enkacardCread import EnkaCardCread, EnkaCardCharters

async def upload():
    async with EnkaNetworkAPI(user_agent= "ENC Library: 2.2.5") as ena:
        await ena.update_assets()

def uidCreat(uids):
    if type(uids) == int or type(uids) == str:
        return str(uids).replace(' ', '').split(",")[0]
    else:
        raise ENCardError(5,"The UIDS parameter must be a number or a string. To pass multiple UIDs, separate them with commas.\nExample: uids = 55363")

async def saveBanner(uid,res,name):
    data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
    path = os.getcwd()
    try:
        os.mkdir(f'{path}/AioEnkaImg')
    except:
        pass
    try:
        os.mkdir(f'{path}/AioEnkaImg/{uid}')
    except:
        pass
    res.save(f"{path}/AioEnkaImg/{uid}/{name}_{data}.png")


def sortingArt(result,uid):
    enc_card = {uid: {}}
    for key in result:
        for keys in key:       
            if not keys in enc_card[uid]:
                enc_card[uid][keys] = key[keys]

    return enc_card

def sorting(result):
    enc_card = {}
    for key in result:
        if not key["uid"] in enc_card:
            enc_card[key["uid"]] = {}
        if not key["name"] in enc_card[key["uid"]]:
            enc_card[key["uid"]][key["name"]] = {"img": key["card"], "id": key["id"]}

    return enc_card
    '''
    enc_card = {"uid": None, "cards": []}
    for key in result:
        if enc_card["uid"] == None:
            enc_card["uid"] = key["uid"]
        enc_card["cards"].append(EnkaCardCharters(**key["cards"]))    
    result = EnkaCardCread(**enc_card)'''
    
    return result



class ENC:
    
    def __init__(self,lang = "ru", characterImgs = None,
            img = None, characterName = None, adapt = False,
            randomImg = False, hide = False, save = False, nameCards = False, splashArt = False, miniInfo = True, agent = "Library: 2.2.5") :
        self.USER_AGENT = f"ENC {agent}"
        if lang in supportLang:
            if lang != "kh":
                self.assets = Assets(lang=lang)
                self.lang = lang
                self.translateLang = translationLang[self.lang]
                change_Font(0)
            else:
                self.typelang = 1
                self.assets = Assets(lang="en")
                self.lang = "en"
                self.translateLang = translationLang[self.lang]
                change_Font(1)

        else:
            raise ENCardError(6,"Dislike language List of available languages: en, ru, vi, th, pt, kr, jp, zh, id, fr, es, de, chs, cht, kh.\nRead more in the documentation: https://github.com/DEViantUA/EnkaNetworkCard")
        self.splashArt = splashArt
        self.nameCards = nameCards
        self.adapt = adapt
        self.save = save
        self.hide = hide
        self.characterName = characterName
        self.img = None
        self.dopImg = img
        self.randomImg = randomImg
        self.characterImgs = characterImgs
        self.miniInfo = miniInfo
        self.backgrounds = None
        if characterImgs:
            if isinstance(characterImgs, dict):
                chImg = {}
                for key in characterImgs:
                    if not key in chImg:
                        chImg[key.lower()] = characterImgs[key]
                self.characterImgs = chImg
            else:
                raise ENCardError(4,"The charterImg parameter must be a dictionary, where the key is the name of the character, and the parameter is an image.\nExample: charterImg = {'Klee': 'img.png'} or {'Klee': 'img.png', 'Xiao': 'img2.jpg', ...}")
        
        if characterName:
            if isinstance(characterName, str):
                self.characterName = characterName.lower().replace(' ', '').split(",")
            else:
                raise ENCardError(3,"The name parameter must be a string, to pass multiple names, list them separated by commas.\nExample: name = 'Klee' or name = 'Klee, Xiao'")

        if isinstance(img, list):
            if self.randomImg:
                if len(img) > 1:
                    self.img = img
                else:
                   raise ENCardError(2, "The list of images must consist of 2 or more.\nExample: img = ['1.png','2.png', ...]") 
            else:
                raise ENCardError(1, "For a list of images, you need to pass the randomImg parameter\nExample: randomImg = True")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def profile(self,enc, teample = 1, image = True):
        for key in enc:
            profile = enc[key].player
            uid = key
            break
        itog = await creatUserProfile(image,profile,self.translateLang,self.hide,uid,self.assets,teample)

        return itog

    async def enc(self,uids = None):
        result = {}
        uid = uidCreat(uids)
        async with EnkaNetworkAPI(user_agent = self.USER_AGENT, lang=self.lang) as client:
            if not uid in result:
                result[uid] = None
            r = await client.fetch_user(uid)
            if r.characters:
                result[uid] = r
        return result

    async def characterImg(self,name):
        if name in self.characterImgs:
            self.img = await openUserImg(self.characterImgs[name])
        else:
            self.img = None

    async def artifact(self,enc, template = 1, artifactType = ""):
        task = []
        if artifactType != "":
            if type(artifactType) == str:
                artifactType = str(artifactType).replace(' ', '').split(",")
                artifactTypeList = []
                for key in artifactType:
                    if key.lower() == "flower":
                        artifactTypeList.append("EQUIP_BRACER")
                    elif key.lower() == "feather":
                        artifactTypeList.append("EQUIP_NECKLACE")

                    elif key.lower() == "sands":
                        artifactTypeList.append("EQUIP_SHOES")

                    elif key.lower() == "goblet":
                        artifactTypeList.append("EQUIP_RING")
                    elif key.lower() == "circlet":
                        artifactTypeList.append("EQUIP_DRESS")
                if len(artifactTypeList) == 0:
                    return ENCardError(10,"Invalid parameter passed: artifactType\n\nAvailable values: Flower,Feather,Sands,Goblet,Circlet\nTo get all types, leave the field blank.")
            else:
                return ENCardError(10,"Invalid parameter passed: artifactType\n\nAvailable values: Flower,Feather,Sands,Goblet,Circlet\nTo get all types, leave the field blank.")
        else:
            artifactTypeList = ["EQUIP_BRACER","EQUIP_NECKLACE","EQUIP_SHOES","EQUIP_RING","EQUIP_DRESS"]
        for uid in enc:
            r = enc[uid]
            if not r:
                continue
            if template != 1:
                template = 1
            for charter in r.characters:
                imageCharter = charter.image.icon.url
                if self.characterName:
                    if not charter.name.replace(' ', '').lower() in self.characterName:
                        continue
                    else:
                        task.append(get_artifact_rate(charter,template,artifactTypeList,imageCharter))
                else:
                    task.append(get_artifact_rate(charter,template,artifactTypeList,imageCharter))
        s = await asyncio.gather(*task)
        
        return sortingArt(s,uid)

    async def creat(self, enc, template = 1, background = None, cards = None):
        if not self.img and self.dopImg:
            self.img = await openUserImg(self.dopImg)
            self.randomImg = False
        template = int(template)
        task = []
        if template in [1,2,3,5,7]:
            for uid in enc:
                r = enc[uid]
                if not r:
                    continue
                if template == 1:
                    signatureRes = signature(self.hide,uid)
                elif template == 2:
                    signatureRes = await creatUserInfo(self.hide,uid,r.player,self.translateLang)
                else:
                    if self.hide:
                        signatureRes = "UID: Hide"
                    else:
                        signatureRes = f"UID: {uid}"
                for key in r.characters:
                    if self.characterName:
                        if not key.name.replace(' ', '').lower() in self.characterName:
                            continue
                    if self.characterImgs:
                        await self.characterImg(key.name.lower())

                    if self.nameCards and template == 2:
                        signatureRes = await creatUserInfo(self.hide,uid,r.player,self.translateLang,key.image.icon.filename.replace("CostumeFloral","").split("AvatarIcon_")[1],self.nameCards)
                    
                    if self.randomImg:
                        task.append(self.generation(key,await openUserImg(random.choice(self.img)),uid,signatureRes,template, r.player))
                    else:
                        task.append(self.generation(key,self.img,uid,signatureRes,template, r.player))

            result = await asyncio.gather(*task)
            return sorting(result)
        elif template == 6:
            return await self.teampleSix(enc,cards)
        else:
            if background != None:
                background = await openUserImg(background)
            return await self.teampleFour(enc,background,cards)

    async def generation(self,charter,img,uid,signatureRes,teample = 1, player = None):
        if teample == 1:
            result = await generationOne(charter,self.assets,img,self.adapt,signatureRes,self.translateLang["lvl"],self.splashArt)
        elif teample == 2:
            result =  await generationTwo(charter,self.assets,img,self.adapt,signatureRes,self.translateLang,self.splashArt)
        elif teample == 5:
            result =  await generationFive(charter,self.assets,img, self.translateLang["lvl"],self.splashArt,signatureRes)
        elif teample == 7:
            result =  await generationSeven(charter,self.assets,img, self.translateLang,self.splashArt,signatureRes,player, typelang = self.typelang) 
        else:
            result =  await generationTree(charter,self.assets,img,self.adapt,signatureRes,self.translateLang,self.splashArt)
        if self.save:
            await saveBanner(uid,result, charter.name)
        return {"uid": uid, "name": charter.name, "card": result, "id": charter.id}
        #return {"uid": uid, "cards": {"name": charter.name, "card": result, "id": charter.id}} #NEW VERSION

    async def teampleSix(self,enc,cards):
        charterList = []
        result = {"1-4": None, "5-8": None}
        task = []
        if type(cards) != dict:
            cards = None
        for uid in enc:
            r = enc[uid]
            if not r:
                continue
            if self.hide:
                signatureRes = "UID: Hide"
            else:
                signatureRes = f"UID: {uid}"
            for key in r.characters:
                if self.characterImgs:
                    await self.characterImg(key.name.lower())
                if self.characterName:
                    if not key.name.replace(' ', '').lower() in self.characterName:
                        continue
                charterList.append([key,self.img])
                if len(charterList) == 4:
                    task.append(generationSix(charterList,self.assets,self.translateLang,signatureRes, cards))
                    charterList = []
            if charterList != []:
                task.append(generationSix(charterList,self.assets,self.translateLang,signatureRes, cards))
            if len(task) == 2:
                result["1-4"], result["5-8"] = await asyncio.gather(*task)
            else:
                result["1-4"] = await task[0]  

        if self.save:
            for key in result:
                await saveBanner(uid,result[key],key)
        return {"uid": uid,"card": result}

    async def teampleFour(self,enc,background,cards):
        charterList = []
        result = {"1-4": None, "5-8": None}
        task = []
        if type(cards) != dict:
            cards = None
        for uid in enc:
            r = enc[uid]
            if not r:
                continue
            if self.hide:
                signatureRes = "UID: Hide"
            else:
                signatureRes = f"UID: {uid}"
            for key in r.characters:
                if self.characterImgs:
                    await self.characterImg(key.name.lower())
                if self.characterName:
                    if not key.name.replace(' ', '').lower() in self.characterName:
                        continue
                charterList.append([key,self.img])
                if len(charterList) == 4:
                    task.append(generationFour(charterList,self.assets,self.translateLang,self.miniInfo,r.player.nickname,signatureRes, background, cards))
                    charterList = []
            if charterList != []:
                task.append(generationFour(charterList,self.assets,self.translateLang,self.miniInfo,r.player.nickname,signatureRes,background, cards))
            if len(task) == 2:
                result["1-4"], result["5-8"] = await asyncio.gather(*task)
            else:
                result["1-4"] = await task[0]  

        if self.save:
            for key in result:
                await saveBanner(uid,result[key],key)
        return {"uid": uid,"card": result}



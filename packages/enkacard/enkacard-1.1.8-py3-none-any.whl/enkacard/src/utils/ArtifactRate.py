from . import Generation as gen
from .FunctionsPill import imagSize,imgD
from PIL import ImageDraw,Image
from . import openFile as of
from . import options as op
import math,asyncio
from enkanetwork import EquipmentsType,DigitType


async def get_proc(x):
    if x == 0:
        return of.proc_None_rate
    elif x == 1:
        return of.proc_0_rate
    elif x == 2:
        return of.proc_25_rate
    elif x == 3:
        return of.proc_50_rate
    elif x == 4:
        return of.proc_75_rate
    else:
        return of.proc_100_rate

poitions = [
    266,
    310,
    354,
    400
]

poitionsSub = [
    263,
    307,
    351,
    397
]

poitionsCount = [
    253,
    297,
    341,
    385
]

async def convert_name(x):
    if x == "EQUIP_BRACER":
        return "flower"
    elif x == "EQUIP_NECKLACE":
        return "feather"
    elif x == "EQUIP_SHOES":
        return "sands"
    elif x == "EQUIP_RING":
        return "goblet"
    elif x == "EQUIP_DRESS":
        return "circlet"



async def generator_artifact(name,raiting,name_set,name_charter,icon,substats,props,imageStats,stats,lvl,imageCharter):
    CRIT_DMG = 0
    CRIT_RATE = 0
    bg = await gen.open_bg_artifact(raiting)
    bg.alpha_composite(of.frame_artifact_rate,(0,0))
    icon = await imgD(icon)
    bg.alpha_composite(icon.resize((183,183)),(254,55))
    i = 0
    
    for sub in substats:
        sub_name = sub.name
        sub_value = f"{sub.value}{'%' if sub.type == DigitType.PERCENT else ''}"
        countProc = 0
        ida = sub.prop_id

        if sub.prop_id == "FIGHT_PROP_CRITICAL_HURT":
            CRIT_DMG += sub.value
        if sub.prop_id == "FIGHT_PROP_CRITICAL":
            CRIT_RATE +=sub.value

        for p in props:
            if p.prop_id == ida:
                countProc += 1          
        procImage = await get_proc(countProc)
        iconSub = gen.getIconAdd(sub.prop_id, icon = True, size = (20,21))

        bg.alpha_composite(iconSub,(16, poitionsSub[i]))
        bg.alpha_composite(procImage,(245, poitions[i]))
        bg.alpha_composite(imageStats,(26, 113))



        d = ImageDraw.Draw(bg)
        
        d.text((388,poitionsCount[i]), f"+{countProc}", font = op.fontSize(12), fill=(139,255,199,255))

        x = op.fontSize(15).getlength(sub_value)
        d.text((int(393-x),poitionsSub[i]), sub_value, font = op.fontSize(15), fill=op.coloring)
        d.text((44,poitionsSub[i]), sub_name, font = op.fontSize(15), fill=op.coloring)
        x = op.fontSize(21).getlength(name)
        d.text((int(204-x/2),18), name, font = op.fontSize(21), fill=op.coloring)
        d.text((16,68), name_set, font = op.fontSize(17), fill=op.coloring)
        x = op.fontSize(21).getlength(name_charter)
        d.text((int(223-x/2),460), name_charter, font = op.fontSize(21), fill=op.coloring)
        d.text((72,115), stats, font = op.fontSize(30), fill=op.coloring)
        x = op.fontSize(21).getlength(lvl)
        d.text((int(52-x/2),166), lvl, font = op.fontSize(21), fill=op.coloring)

        imageCharters = await imgD(imageCharter)
        imageCharters = imageCharters.resize((61,67))
        bgCharter = of.bg_charter_art.copy()
        bgCharter = Image.composite(bgCharter,imageCharters,of.maska_charter_art.convert("L"))

        bg.alpha_composite(bgCharter,(0,427))

        tcvR = float('{:.2f}'.format(CRIT_DMG + (CRIT_RATE*2)))   
        i += 1
    TCV = f"{tcvR}CV"
    d.text((29,198), TCV, font = op.fontSize(21), fill=op.coloring)

    return bg



async def get_artifact_rate(info, teample, artType,imageCharter):
    artImgList = {info.name: {}}
    for key in filter(lambda x: x.type == EquipmentsType.ARTIFACT, info.equipments):
        if str(key.detail.artifact_type.value) in artType:
            name = key.detail.name
            raiting = key.detail.rarity
            name_set = key.detail.artifact_name_set
            icon = key.detail.icon.url
            stat = f"{key.detail.mainstats.value}{'%' if key.detail.mainstats.type == DigitType.PERCENT else ''}"
            lvl = f"+{key.level}"
            imageStats = gen.getIconAdd(key.detail.mainstats.prop_id, icon = True, size = (36,36))
            if teample == 1:
                artImg = await generator_artifact(name,raiting,name_set,info.name,icon,key.detail.substats, key.props,imageStats,stat,lvl,imageCharter)

            nameType = await convert_name(str(key.detail.artifact_type.value))
            if not nameType in artImgList[info.name]:
                artImgList[info.name][nameType] = artImg
    return artImgList
# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import ImageFont
from . import openFile

coloring = (255,255,255,255)

def fontSize(t):
    return ImageFont.truetype(openFile.font, t)

#t32 = ImageFont.truetype(font, 32) fontSize(32)
#t24 = ImageFont.truetype(font, 24) fontSize(24)
#t18 = ImageFont.truetype(font, 18) fontSize(18)
#t17 = ImageFont.truetype(font, 17) fontSize(17)
#t15 = ImageFont.truetype(font, 15) fontSize(15)
#t12 = ImageFont.truetype(font, 12) fontSize(12)

stat_perc = {3, 6, 9, 11, 12, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 3002, 3004, 3005, 3007, 3008, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3018, 3019, 3020, 3021, 3024}
IconAddTrue = ["FIGHT_PROP_PHYSICAL_ADD_HURT","FIGHT_PROP_HEAL_ADD","FIGHT_PROP_GRASS_ADD_HURT","FIGHT_PROP_FIRE_ADD_HURT","FIGHT_PROP_MAX_HP","FIGHT_PROP_CUR_ATTACK","FIGHT_PROP_CUR_DEFENSE","FIGHT_PROP_ELEMENT_MASTERY","FIGHT_PROP_CRITICAL","FIGHT_PROP_CRITICAL_HURT","FIGHT_PROP_CHARGE_EFFICIENCY","FIGHT_PROP_ELEC_ADD_HURT","FIGHT_PROP_ROCK_ADD_HURT","FIGHT_PROP_ICE_ADD_HURT","FIGHT_PROP_WIND_ADD_HURT","FIGHT_PROP_WATER_ADD_HURT"]
dopStatAtribute = {"FIGHT_PROP_MAX_HP": "BASE_HP", "FIGHT_PROP_CUR_ATTACK":"FIGHT_PROP_BASE_ATTACK","FIGHT_PROP_CUR_DEFENSE":"FIGHT_PROP_BASE_DEFENSE"}
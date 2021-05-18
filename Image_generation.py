from PIL import Image, ImageDraw, ImageFont
import requests
import discord
import io
class LevelIMG:
    def __init__(self, ProfileIMG,Username,exp,lvl,difficulty,rank):
        self.ProfileIMG = ProfileIMG
        self.Username = Username
        self.exp = exp
        self.lvl = lvl
        self.difficulty = difficulty
        self.rank = rank
    @property
    def drawIMG(self):
        # creating canvas
        img = Image.new('RGB', (934, 282), color = (21,23,26))
        d = ImageDraw.Draw(img)
        # getting profile pic and drawing it
        avatarSize = 200
        avatarImg = Image.open(requests.get(self.ProfileIMG, stream=True).raw)
        avatarImg = avatarImg.resize((avatarSize,avatarSize))

        circle_image = Image.new('L', (avatarSize, avatarSize))
        circle_draw = ImageDraw.Draw(circle_image)
        circle_draw.ellipse((0, 0, avatarSize, avatarSize), fill=255)
        
        # getting username and tag
        userName,tag = self.Username.split('#')
        
        ## font for username
        font = ImageFont.truetype('fonts/arial.ttf',45)
        ## font for user tag
        tag_font = ImageFont.truetype('fonts/arial.ttf',30)
        ## width and height of username
        t_width , t_ht = d.textsize(userName,font=font)
        ## width and ht of tag
        tag_width, tag_ht = d.textsize(tag,font=tag_font)

        ## position of avatar
        avatarX = (934-avatarSize)//15
        avatarY = (282-avatarSize)//2


        ## position of username
        x = avatarX + 230
        y = (282-t_ht)//2

        ## text and values for xp
        di = self.difficulty
        #print(di)
        a = self.difficulty+(self.lvl-1)*di
        XP=""
        if a > 1000:
            convert = a/1000
            convertEXP = round(self.exp/1000,2)
            if self.exp>1000:
                XP = f"{convertEXP}k/{convert}k XP"
            else:
                XP = f"{self.exp}/{convert}k XP"
        else:
            XP = f"{self.exp}/{a} XP"
        XP_w, XP_ht = d.textsize(XP,font=font)


        LVL = f"Level: {self.lvl}"
        LVL_w, LVL_ht = d.textsize(LVL,font=font)


        RNK = f"Rank: {self.rank}"
        RNK_w , RNK_ht = d.textsize(RNK,font=font)

        d.text( (avatarX + 230, y), userName, fill=(255,255,255), font=font)
        d.text((t_width+x,y+15), " #"+tag, fill=(81,81,81), font=tag_font)
        d.text((920-XP_w,250-XP_ht),XP,fill=(0,255,185),font=font)
        d.text((920-LVL_w,10),LVL,fill=(255,255,255),font=font)
        d.text((920-RNK_w-LVL_w-20,10),RNK,fill=(0,255,185),font=font)
       
        if di == 100:
            percentVal1 = self.exp - ((self.lvl-1)*di)
            percent = (percentVal1/di)*934
            d.rectangle([0,272,percent,282],fill=(0,255,185))
        if di != 100:
            percentVal1 = self.exp - ((self.lvl-1)*di)
            percent = (percentVal1/di)*100
            bar_to_be_filled = (percent/100)*934
            d.rectangle([0,272,bar_to_be_filled,282],fill=(0,255,185))
        img.paste(avatarImg, (avatarX,avatarY),circle_image)
        with io.BytesIO() as image_binary:
            img.save(image_binary,"PNG")
            image_binary.seek(0)
            return discord.File(fp=image_binary, filename='image.png')
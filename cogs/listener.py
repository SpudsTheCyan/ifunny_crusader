import discord
import urllib
import numpy as np
import cv2

from discord.ext import commands

class IFunnyDetector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # function to hadle embedded links as well as real images
    # def watermark_detector(image_url = None, attachment = None):
    #     if image_url is None and attachment is None:
    #         return None
    #     else:
    #         # gets image and makes it grayscale
    #         if attachment is not None:
    #             image = await attachment.read()
            
    #         arr = np.fromstring(og_img, dtype=np.uint8)
    #         img = cv2.imdecode(arr, -1) # 'Load it as it is' https://stackoverflow.com/questions/21061814/how-can-i-read-an-image-from-an-internet-url-in-python-cv2-scikit-image-and-mah

    #         # compares the picture with the ifunny watermark
    #         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # http://www.learningaboutelectronics.com/Articles/How-to-match-an-image-embedded-in-another-image-Python-OpenCV.php
    #         template = cv2.imread("ifunny_watermark.jpg", 0)
    #         result = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)

    #         # determines if the ifunny watermark is in the image
    #         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #         if min_val < 0.01: # found this code from google ai
    #             return True
    #         else:
    #             return False

    @commands.Cog.listener()
    async def on_message(self, message):
        # gets the url to every attachment in the message
        if message.attachments != []:
            for i in message.attachments:
                try:
                    # gets image and makes it grayscale
                    og_img = await i.read()
                    arr = np.fromstring(og_img, dtype=np.uint8)
                    img = cv2.imdecode(arr, -1) # 'Load it as it is' https://stackoverflow.com/questions/21061814/how-can-i-read-an-image-from-an-internet-url-in-python-cv2-scikit-image-and-mah

                    # compares the picture with the ifunny watermark
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # http://www.learningaboutelectronics.com/Articles/How-to-match-an-image-embedded-in-another-image-Python-OpenCV.php
                    template = cv2.imread("ifunny_watermark.jpg", 0)
                    result = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)

                    # determines if the ifunny watermark is in the image
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if min_val < 0.01: # found this code from google ai
                        await message.reply("**IFUNNY DETECTED**\n**ANTI-CRINGE COUNTERMEASURES DEPLOYED**")
                except cv2.error:
                    pass




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(IFunnyDetector(bot)) # add the cog to the bot
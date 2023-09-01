#listener.py
import logging
from typing import Union

import cv2
import discord
import numpy as np
import requests
from discord.ext import commands


# makes a filter for logs
class DebugFilter(logging.Filter):
	def filter(self, record):
		return not record.levelno == logging.DEBUG

class IFunnyDetector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def image_checker(self, file:Union[discord.Attachment, discord.message.Message]) -> bool:
        """Takes an attachment or a message as an argument and returns a bool based on weather it is an image or not

        Args:
            attachment (discord.Attachment | discord.message.Message): Either an attachment or a link.
        """
        match type(file):
            case discord.message.Attachment:
                if str(file.content_type)[0:5] =="image":
                    return True
                else:
                    return False
            case discord.message.Message:
                if (file.content[-4:] == ".jpg" or file.content[-4:] == ".png") and file.content[0:8] == "https://": # does it start with https and end with .jpg or .png?
                    return True
                else:
                    return False
            case _:
                return False
            
    # function to handle embedded links as well as real images
    async def watermark_detector(self, image: Union[discord.Attachment, str]):
        match type(image):
            case discord.message.Attachment:
                image_bytes = await image.read()
            case discord.message.Message:
                response = requests.get(image.content)
                image_bytes = response.content
            case _:
                raise Exception("Invalid parameter!")

        arr = np.fromstring(string=image_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is' https://stackoverflow.com/questions/21061814/how-can-i-read-an-image-from-an-internet-url-in-python-cv2-scikit-image-and-mah

        # compares the picture with the ifunny watermark
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # http://www.learningaboutelectronics.com/Articles/How-to-match-an-image-embedded-in-another-image-Python-OpenCV.php
        template = cv2.imread("ifunny_watermark.jpg", 0)
        result = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)

        # determines if the ifunny watermark is in the image
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if min_val < 0.01: # found this code from google ai
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        messageSent = False
        # gets the url to every attachment in the message
        if message.attachments != []:
            for attachment in message.attachments:
                if not messageSent:
                    if self.image_checker(attachment): # is it a valid image?
                        watermarkDetected = await self.watermark_detector(attachment)
                        if watermarkDetected: # does it have the watermark?
                            await message.reply("**IFUNNY DETECTED**\n**ANTI-CRINGE COUNTERMEASURES DEPLOYED**")
                            messageSent = True
        elif not messageSent:
            if self.image_checker(message): # is it a valid image?
                watermarkDetected = await self.watermark_detector(message)
                if watermarkDetected: # does it have the watermark?
                    await message.reply("**IFUNNY DETECTED**\n**ANTI-CRINGE COUNTERMEASURES DEPLOYED**")
                    messageSent = True

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(IFunnyDetector(bot)) # add the cog to the bot
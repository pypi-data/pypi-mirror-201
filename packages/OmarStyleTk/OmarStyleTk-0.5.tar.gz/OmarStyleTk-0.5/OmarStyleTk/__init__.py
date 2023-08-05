from PIL import ImageTk, Image
import requests
import datetime
import os

class Omar_TK():
    tt = []
    
    def im_Tk(self,imgg):
        try:

            url = imgg
            response = requests.get(url)
        except:
            exit()
        now = datetime.datetime.now()

        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

        im = f"{hour}{minute}{second}ldownload.jpeg"
        with open(im, "wb") as f:
            f.write(response.content)
            Omar_TK.tt.append(im)

        img = Image.open(im)
        photo = ImageTk.PhotoImage(img)
        return photo

    def Close(self):
        rm = Omar_TK.tt
        for file in rm:
            try:
                # print(rm)
                os.remove(file)
            except:
                pass
import wx
import sys
import requests
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO


# The subscription key for the Azure service
subscription_key = "XXXXXXX"
assert subscription_key


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer()
        sizer = wx.GridSizer(2, 2, 2, 2)
        btn1 = wx.Button(panel, label='Load Picture')
        btn2 = wx.Button(panel, label='Exit')
        sizer.AddMany([btn1, btn2])
        hbox.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizer(hbox)
        btn1.Bind(wx.EVT_BUTTON, self.ShowMessage1)
        btn2.Bind(wx.EVT_BUTTON, self.ShowMessage2)
        self.SetSize((250, 100))
        self.SetTitle('Cognitive Service')
        self.Centre()


    def ShowMessage1(self, event):
        frame = wx.Frame(None, -1, 'win.py')
        frame.SetDimensions(0, 0, 100, 50)
        openFileDialog = wx.FileDialog(frame, "Open", "", "", "Pictures (*.jpg;*.png)|*.jpg;*.png|JPG files (*.jpg)|*.jpg", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        image_local = openFileDialog.GetPath()
        print("Local file to be submitted is {0}".format(image_local))
        vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/"
        analyze_url = vision_base_url + "analyze"
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description,Color'}

        image_data = open(image_local, "rb").read()
        data = {'url': image_local}
        response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most relevant caption for the image is obtained from the 'description' property.
        analysis = response.json()
        print(json.dumps(response.json()))
        image_caption = analysis["description"]["captions"][0]["text"].capitalize()

        image = Image.open(BytesIO(image_data))
        plt.imshow(image)
        plt.axis("off")
        _ = plt.title(image_caption, size="x-large", y=-0.1)
        plt.show()
        openFileDialog.Destroy()

    def ShowMessage2(self, event):
        sys.exit(0)


def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

# EOF

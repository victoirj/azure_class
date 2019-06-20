import wx
import sys
import requests
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO

# The subscription key for the Azure service
subscription_key = "XXXXXX"
assert subscription_key


def get_emotion(emotions):
    print("----- Emotions: {0}".format(emotions))
    out_str = "["
    for emotion in emotions:
        print("Key: {0} Value:{1}".format(emotion,emotions.get(emotion)))
        if emotions.get(emotion) > 0.8:
            out_str = out_str + " " +  emotion
    out_str = out_str + "]"
    return out_str


def get_hair_color(hairColor):
    print("----- hairColor length: {0}".format(len(hairColor)))
    out_str = "["
    for item in hairColor:
        print(item)
        key = item.get('color')
        value = item.get('confidence')
        if value > 0.8:
            out_str = out_str + " " + key
    out_str = out_str + "]"
    return out_str

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

        vision_base_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/"
        analyze_url = vision_base_url + "detect"
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        params = {'returnFaceId': 'true', 'returnFaceLandmarks': 'false', 'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise' }

        image_data = open(image_local, "rb").read()
        data = {'url': image_local}
        response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most relevant caption for the image is obtained from the 'description' property.
        analysis = response.json()
        print(json.dumps(response.json()))
        face_attributes = analysis[0].get('faceAttributes')
        pic_age = face_attributes.get('age')
        pic_gender = face_attributes.get('gender')
        # if pic_gender == "female":
        #    pic_age = "young"
        pic_emotion = face_attributes.get('emotion')
        # pic_hair_color = face_attributes.get('hair').get('bald')
        pic_hair_color = face_attributes.get('hair').get('hairColor')

        image_caption = "Age:{0} Gender:{1} Emotion:{2} Hair:{3}".format(pic_age, pic_gender, get_emotion(pic_emotion), get_hair_color(pic_hair_color))

        # Display the image and overlay it with the caption.
        # image = Image.open(BytesIO(requests.get(image_url).content))
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

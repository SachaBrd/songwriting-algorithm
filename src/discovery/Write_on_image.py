from PIL import Image, ImageFont, ImageDraw

img = Image.open("../../assets/tab.png")

font = ImageFont.truetype(font='Arial.ttf', size=20)

d1 = ImageDraw.Draw(img)
d1.text((50, 25), "5", fill=(0, 0, 0), font=font)
d1.text((80, 37), "3", fill=(0, 0, 0), font=font)
img.show()

img.save("../../assets/img_bin/generated_tab.jpg")
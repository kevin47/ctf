#!/usr/bin/python
from PIL import Image, ImageDraw

img = Image.open('stego.png').convert('RGB')
draw = ImageDraw.Draw(img)
#img2 = Image.open('original.jpg').convert('RGB')

ans = ''
for y in range(150, 247):
	for x in range(img.width/8):
		tmp = 0
		for k in range(8):
			tmp <<= 1
			color, t = img.getpixel((x*8+7-k, y)), 0
			if (x*8+7-k)&1: t = color[0]&1
			else: t = color[2]&1
			tmp += t
		ans += chr(tmp)
print ans

	#	draw.point((x, y), (t, t, t))
#img.save('edited.png', 'PNG')



# 图片剪切问题
```
img = Image.open("./data/cut/xx.jpg")
print(img.size)
cropped = img.crop((0, 0, 512, 128))  # (left, upper, right, lower)
cropped.save("./data/cut/cut.jpg")
```

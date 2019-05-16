import pixelhouse as ph
from greasepaint import eyeliner, eyeshadow

vaporwave_pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"]
f_jpg = "data/source_images/tessa1.jpg"

def crop_eyes(canvas, f_save):
    canvas = canvas.copy()
    canvas.img = canvas.img[200:270, 122:340]
    return canvas.save(f_save)
    

canvas = ph.load(f_jpg)
crop_eyes(canvas, "docs/images/eyes0.jpg")

canvas = eyeliner(canvas)
crop_eyes(canvas, "docs/images/eyes1.jpg").show()
canvas.resize(.5).save("docs/images/tessa1_liner.jpg")

for k,p in enumerate(vaporwave_pal):
    canvas = eyeshadow(f_jpg, color=p)
    crop_eyes(canvas, f"docs/images/eyes{k+2}.jpg")

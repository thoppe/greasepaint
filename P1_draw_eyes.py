from greasepaint import eyeliner, eyeshadow

vaporwave_pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"]
f_jpg = "data/source_images/tessa1.jpg"

canvas = eyeliner(f_jpg)
canvas.show()
canvas.resize(0.5).save('docs/images/tessa1_eyeliner.png')


for p in vaporwave_pal:
    eyeshadow(f_jpg, color=p).show()

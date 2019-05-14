from greasepaint import eyeliner, eyeshadow

vaporwave_pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"]
f_jpg = "data/source_images/tessa1.jpg"

eyeliner(f_jpg).show()

for p in vaporwave_pal:
    eyeshadow(f_jpg, color=p).show()

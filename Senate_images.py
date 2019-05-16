import pixelhouse as ph
from greasepaint import eyeliner, eyeshadow
import glob, os, random

F_IMG = glob.glob('projects/Senate/images/*')
target_width = 600
vaporwave_pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"]

save_dest = 'projects/Senate/modified_images/'

for f in F_IMG[:]:
    f_save = os.path.join(save_dest, os.path.basename(f))

    if os.path.exists(f_save):
        continue

    print(f_save)
    
    
    c = ph.load(f)
    fx = 600.0/c.shape[0]
    c = c.resize(fx)

    c2 = eyeliner(c)
    color = random.choice(vaporwave_pal)
    c3 = eyeshadow(c2, color=color, opacity=.6)
   
    canvas = ph.hstack([c,c2,c3])
    canvas.save(f_save)


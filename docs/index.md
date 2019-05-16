% Title: greasepaint demo
% Author: Travis Hoppe

!!(https://source.unsplash.com/3P6E2y2lyus class="light")

...bg-white
..aligncenter

### .text-data **greasepaint** 
#### a budding python library to manipulate faces
<br>
..text-intro
https://github.com/thoppe/greasepaint
..

-----

% Triple dots indicate a slide level class
....bg-black

..wrap
### New hobby
falling and missing

..div ![](images/flying.jpg) ![](images/trapeze.webp)


--------

!!(https://source.unsplash.com/O6TrpoUjrls class="dark")

...align-right.bg-white 

..size-50.wrap

# .text-landing TSNY IFW:
## Intensive Flying Workshop

.line

Ten week course on flying trapeze.
Ends with a public performance with troupe.
Each troupe has a "theme".
Ours was glam rock. 👨‍🎤

-----
!!(images/troupe.jpg class="light")

...align-left.bg-black.slide-top
..slide-top
### Look at all the makeup.

-----
...wrap 
### .text-data **greasepaint**
A python library to modify faces.


    pip install greasepaint

<br>

```
from greasepaint import eyeliner
eyeliner("docs/images/tessa.jpg").show()
```
<br>

..div
![](images/tessa1_src.jpg)
![](images/tessa1_liner.jpg)


-----
...wrap 

.wrap ![](images/eyes0.jpg) ![](images/eyes1.jpg)

<br>

```
from greasepaint import eyeshadow

vaporwave_pal = ["#FF6AD5", "#C774E8", "#AD8CFF", "#8795E8", "#94D0FF"]

def crop_eyes(canvas, f_save):
    canvas = canvas.copy()
    canvas.img = canvas.img[200:270, 122:340]
    canvas.save(f_save)


for k,p in enumerate(vaporwave_pal):
    canvas = eyeshadow("tessa1.jpg", color=p)
    crop_eyes(canvas, f"docs/images/eyes{k+2}.jpg")
```
<br>

..wrap
![](images/eyes2.jpg)
![](images/eyes3.jpg)
![](images/eyes4.jpg)
![](images/eyes5.jpg)


-----
...wrap
### .text-landing **body modifications**
..wrap
![](images/tessa1_src.jpg)  ![](images/tessa1_third_eye.png)
..
### .text-landing **body modifications**

_Poisson Image Editing FTW_

-----
...wrap
# Who needs more glam?
<br>

-----

...wrap
# Who needs more glam?
<br>
### The United States Senate.

-----

...wrap
# Pat Toomey
<br>
..wrap ![](images/Pat_Toomey.jpg)

-----

...wrap
# Rand Paul
<br>
..wrap ![](images/Rand_Paul.jpg)

-----

...wrap
# John Kennedy
<br>
..wrap ![](images/John_Kennedy.jpg)

-----

...wrap
# Tim Scott
<br>
..wrap ![](images/Tim_Scott.jpg)

-----

...wrap
# Bernie Sanders
<br>
..wrap ![](images/Bernie_Sanders.jpg)

-----

..wrap

## **Thanks, you!**
#### Contribute, or suggest an issue at
## [https://github.com/thoppe/greasepaint](https://github.com/thoppe/greasepaint)


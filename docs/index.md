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

-----

% Triple dots indicate a slide level class
...bg-black

### New hobby
.wrap falling and missing
.wrap.container ![](images/flying.jpg) ![](images/trapeze.webp)


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
reetr
tre
...align-left.bg-black
re
# _markdown_
### Basic [Markdown](https://daringfireball.net/projects/markdown/syntax)
<br>

+ **bold** `**text**`
+ *fire* `*text*`
+ _emph_ `_text_`

-----
!!(https://source.unsplash.com/pmX9BkDDr_A class="dark")

...align-left.bg-black

# _emoji_
### standard emoji and [font-awesome](http://fontawesome.io/)
<br>

..text-intro
+ `:battery:` :battery:
+ `:heart_eyes:` :heart_eyes:
+ `::meetup::` ::meetup::
+ `::ra::` ::ra:: 

-----
!!(https://source.unsplash.com/5mZ_M06Fc9g class="dark")
...bg-apple ...align-left

# _math support_
LaTeX rendered inline with [KaTex](https://github.com/Khan/KaTeX)  

.line

### $P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$
<br>
`$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$`

-----
!!(https://source.unsplash.com/7BiMECHFgFY)
...align-left.bg-black.fullscreen

..bg-white.wrap
# _pretty code blocks_
Syntax highlighting Google's [code prettify](https://github.com/google/code-prettify). Code blocks are context-aware.

```
sort [] = []
sort (x:xs) = sort lower ++ [x] ++ sort higher
    where
        lower = filter (< x) xs
        higher = filter (>= x) xs
```
<br>
```
// to convert prefix to postfix
main() {
  char c = getchar();
  (c == '+' || c == '-' || c == '*' || c == '/') ? main(), main() : 0;
  putchar(c);
} 
```

------
!!(https://cdn.shutterstock.com/shutterstock/videos/15778135/preview/stock-footage-office-chair-race-slow-motion-young-guys-have-fun-in-the-office-during-a-break-games-of-businessm.mp4)

..slide-top
## _looping background animations_
Embed/hotlink any video file (thanks [Shutterstock](https://www.shutterstock.com/)!)

-----

!!(https://source.unsplash.com/U5rMrSI7Pn4 class="light")

...slide-bottom.bg-black

..content-center.text-shadow
## .text-landing **A pug and an Equation**
### $$i \hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat H \Psi(\mathbf{r},t)$$
  
this slide looks important right? It's not!

Oh look, an inline $x^2$ equation.

------

...bg-apple
..wrap

## .text-data Thanks, you!
#### Contribute at
## [https://github.com/thoppe/miniprez](https://github.com/thoppe/miniprez)


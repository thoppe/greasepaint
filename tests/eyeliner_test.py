import pytest
import pixelhouse as ph
import greasepaint as gp

@pytest.fixture
def test_canvas():
    canvas = ph.load("tests/tessa1.jpg")
    return canvas

def test_eyeliner(test_canvas):
    # This only tests if the image changed
    dst = gp.eyeliner(test_canvas)
    assert( not (dst.img == test_canvas.img).all() )

def test_eyeshadow(test_canvas):
    # This only tests if the image changed
    dst = gp.eyeshadow(test_canvas, color='r')
    assert( not (dst.img == test_canvas.img).all() )

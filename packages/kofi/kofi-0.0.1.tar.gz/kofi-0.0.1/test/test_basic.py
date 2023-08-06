import kofi
import nose

def test_polylinear():
    """
    via: https://github.com/Sweelol/spectra/issues/4
    """
    colors = ['yellow', 'red', 'black']
    domain = [0, 50, 100]
    color_scale = kofi.scale(colors).domain(domain)
    r = color_scale.range(5)
    results = [ c.hexcode for c in r ]
    goal = ['#ffff00', '#ff8000', '#ff0000', '#800000', '#000000']
    assert(results == goal)

@nose.tools.raises(ValueError)
def test_polylinear_fail():
    colors = ['yellow', 'red', 'black']
    domain = [ 0, 50 ] # Domain has one too few items
    kofi.scale(colors).domain(domain)

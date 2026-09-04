"""Draws the site's ink marks.

Run from the repository root to regenerate them:

    python3 tools/marks.py

Every mark is built the same way: sample a shape, jitter the points, run them
through a Catmull-Rom spline. The randomness is seeded, so the marks are stable
between runs — change a seed and that mark is redrawn by a slightly different
hand. Output goes to _includes/{marks,thread,deckle,grass,spark}.html, plus
the one mark that lives in the stylesheet: the stroke drawn under a hovered book
title, which is patched into _includes/styles.html as a data URI.
"""
import math
import random
import re
import urllib.parse


def catmull(points, closed=False):
    """Catmull-Rom through points -> cubic bezier path string."""
    p = points[:]
    if closed:
        p = [points[-1]] + points + [points[0], points[1]]
    else:
        p = [points[0]] + points + [points[-1]]
    d = "M %.1f %.1f" % (p[1][0], p[1][1])
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i-1], p[i], p[i+1], p[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6.0, p1[1] + (p2[1]-p0[1])/6.0)
        c2 = (p2[0] - (p3[0]-p1[0])/6.0, p2[1] - (p3[1]-p1[1])/6.0)
        d += " C %.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return d

# ---------------------------------------------------------------- thread
def thread(seed=7, h=1200, w=60, steps=22, wander=13):
    rng = random.Random(seed)
    pts = []
    x = w / 2
    for i in range(steps + 1):
        t = i / steps
        y = t * h
        # slow drift + gentle noise, settles near centre at both ends
        env = math.sin(math.pi * t) ** 0.6
        x = w/2 + env * (math.sin(t * 5.1 + 0.7) * wander + rng.uniform(-3.2, 3.2))
        pts.append((x, y))
    return catmull(pts)

# ---------------------------------------------------------------- rule
def rule(seed, w=120, h=6, steps=16, amp=1.5):
    rng = random.Random(seed)
    y0 = h * 0.55
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = t * w
        y = y0 + math.sin(t * 6.4 + seed) * amp * 0.7 + rng.uniform(-amp, amp) * 0.55
        # ends lift slightly, like a pen leaving the page
        y -= (t ** 3) * 0.5
        pts.append((x, y))
    return catmull(pts)

# ---------------------------------------------------------------- deckle
def deckle(seed=3, w=1200, h=18, steps=54):
    rng = random.Random(seed)
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = t * w
        y = h * 0.55 + math.sin(t * 21) * 1.6 + math.sin(t * 6.3 + 1.1) * 2.4 + rng.uniform(-2.0, 2.0)
        pts.append((x, y))
    return catmull(pts)

# ---------------------------------------------------------------- grass
def blade_points(rng, x, ground, h):
    """One blade of grass: up from the ground, leaning as it goes."""
    lean = rng.uniform(-1, 1) * h * 0.30
    pts = [(x, ground),
           (x + lean * 0.32, ground - h * 0.55),
           (x + lean, ground - h)]
    if h > 12:                      # taller blades get one more bend in them
        pts.insert(2, (x + lean * 0.74, ground - h * 0.85))
    return [(px + rng.uniform(-0.16, 0.16), py + rng.uniform(-0.16, 0.16))
            for px, py in pts]


def grass(seed=31, w=1200, ground=30, blades=130, heads=10):
    """A band of grass along the torn edge, a few stems gone to seed.

    Grass grows in clumps rather than at even spacing, so the blades are
    drawn around a handful of centres with real gaps left between them.
    """
    rng = random.Random(seed)
    out = []
    while len(out) < blades:
        cx = rng.uniform(-10, w + 10)
        spread = rng.uniform(12, 46)
        tall = rng.random() < 0.35   # some clumps run taller than others
        for _ in range(rng.randint(3, 9)):
            if len(out) >= blades:
                break
            x = cx + rng.gauss(0, spread * 0.5)
            h = rng.uniform(10.0, 19.0) if tall else rng.uniform(3.5, 11.0)
            out.append(catmull(blade_points(rng, x, ground, h)))

    for i in range(heads):
        x = (i + 0.5) * w / float(heads) + rng.uniform(-30, 30)
        stem = blade_points(rng, x, ground, rng.uniform(21.0, 27.0))
        out.append(catmull(stem))
        # the head: a spray of fine rays, so it reads as seed and not stick
        tx, ty = stem[-1]
        for _ in range(rng.randint(5, 7)):
            a = math.radians(-90 + rng.uniform(-62, 62))
            r = rng.uniform(3.0, 5.2)
            out.append(catmull([(tx, ty),
                                (tx + r * math.cos(a), ty + r * math.sin(a))]))
    return out


# ---------------------------------------------------------------- spark
def spark(seed=12, box=24):
    """A small starburst, the mote that recurs all through fable."""
    rng = random.Random(seed)
    c = box / 2.0
    out = []
    for i in range(8):
        a = math.radians(i * 45 + rng.uniform(-4, 4))
        r0 = 1.5 + rng.uniform(-0.3, 0.3)
        r1 = (8.4 if i % 2 == 0 else 5.2) + rng.uniform(-0.7, 0.7)
        out.append(catmull([
            (c + r0 * math.cos(a) + rng.uniform(-0.2, 0.2),
             c + r0 * math.sin(a) + rng.uniform(-0.2, 0.2)),
            (c + (r0 + r1) / 2 * math.cos(a) + rng.uniform(-0.25, 0.25),
             c + (r0 + r1) / 2 * math.sin(a) + rng.uniform(-0.25, 0.25)),
            (c + r1 * math.cos(a) + rng.uniform(-0.2, 0.2),
             c + r1 * math.sin(a) + rng.uniform(-0.2, 0.2))]))
    return out


# Stroked marks. No `vector-effect`: a non-scaling stroke makes the browser
# measure dashes in screen space, which breaks the pathLength-normalised
# ink-in. Stroke widths are set per mark in the stylesheet, in symbol units.
S = ('<path pathLength="100" fill="none" stroke="currentColor" '
     'stroke-linecap="round" stroke-linejoin="round" d="%s"/>')

out = ['<!-- Ink marks, all generated: jittered points run through a Catmull-Rom\n'
       '     spline, so no two are quite identical. Stroked marks carry\n'
       '     pathLength="100" so one CSS rule can ink any of them in. -->',
       '<svg class="sprite" aria-hidden="true" focusable="false" width="0" height="0">\n  <defs>']

for i in (1, 2):
    out.append('    <symbol id="m-rule-%d" viewBox="0 0 120 6" preserveAspectRatio="none">%s</symbol>'
               % (i, S % rule(i * 5)))
out.append('  </defs>\n</svg>')
open('_includes/marks.html', 'w').write("\n".join(out) + "\n")

open('_includes/thread.html', 'w').write(
    '<!-- The thread: one continuous pen line running the height of the page. -->\n'
    '<svg class="thread" aria-hidden="true" focusable="false" viewBox="0 0 60 1200" preserveAspectRatio="none">\n'
    '  %s\n</svg>\n' % (S % thread()))

open('_includes/deckle.html', 'w').write(
    '<!-- Torn bottom edge of the sheet. -->\n'
    '<svg class="deckle" aria-hidden="true" focusable="false" viewBox="0 0 1200 18" preserveAspectRatio="none">\n'
    '  %s\n</svg>\n' % (S % deckle()))

# The grass runs to well over a hundred paths, so its blades drop the shared
# stroke attributes and inherit them from the stylesheet instead; only the
# pathLength the ink-in needs is kept. It also scales uniformly rather than
# stretching, because a sheared blade stops looking like a blade.
BLADE = '<path pathLength="100" d="%s"/>'

open('_includes/grass.html', 'w').write(
    '<!-- Grass growing along the torn edge, drawn one blade at a time. -->\n'
    '<svg class="mark grass" aria-hidden="true" focusable="false" viewBox="0 0 1200 30">\n'
    '  %s\n</svg>\n' % ("".join(BLADE % d for d in grass())))

open('_includes/spark.html', 'w').write(
    '<!-- The mark at the foot of the text: a small starburst. -->\n'
    '<svg class="mark spark" aria-hidden="true" focusable="false" viewBox="0 0 24 24">\n'
    '  %s\n</svg>\n' % ("".join(S % d for d in spark())))

# The hover underline is a CSS background rather than a mark in the page, so
# it has to be written into the stylesheet itself.
squiggle = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 6' preserveAspectRatio='none'>"
            "<path fill='none' stroke='%235c5a32' stroke-width='1' stroke-linecap='round' d='"
            + rule(9) + "'/></svg>")
uri = 'url("data:image/svg+xml,' + urllib.parse.quote(squiggle, safe="'=:/,%") + '")'
css = open('_includes/styles.html').read()
css, n = re.subn(r'url\("data:image/svg\+xml,[^"]*"\)', lambda m: uri, css)
assert n == 1, "expected exactly one data URI in the stylesheet, found %d" % n
open('_includes/styles.html', 'w').write(css)

print("ok")

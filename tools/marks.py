"""Draws the site's ink marks.

Run from the repository root to regenerate them:

    python3 tools/marks.py

Every mark is built the same way: sample a shape, jitter the points, run them
through a Catmull-Rom spline. The randomness is seeded, so the marks are stable
between runs — change a seed and that mark is redrawn by a slightly different
hand. Output goes to _includes/{marks,thread,deckle}.html, plus the one
mark that lives in the stylesheet: the stroke drawn under a hovered book
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

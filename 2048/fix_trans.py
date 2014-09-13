import numpy
from PIL import Image
import sys

i = Image.open(sys.argv[1]).convert('RGBA')
a = numpy.fromstring(i.tostring(), dtype=numpy.uint8)

a_layer = a[3::4]
for n, a_channel in enumerate(a_layer):
    a[4 * n] = 255
    a[4 * n + 1] = 255
    a[4 * n + 2] = 255

j = Image.fromstring('RGBA', i.size, a.tostring())
j.save(sys.argv[2])

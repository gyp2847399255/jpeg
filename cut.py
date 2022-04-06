import numpy
from skimage import io

image = io.imread("images/demo.bmp")
data = numpy.array(image, dtype=float)
print(data.shape)
data = data.clip(0, 255)
#data = numpy.delete(data, [0, 1, 1330, 1331], axis=0)
#data = numpy.delete(data, [0, 1, 498, 499], axis=0)
io.imsave("demo.bmp", data)

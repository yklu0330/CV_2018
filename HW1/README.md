## Task 1: Hybrid Image

![](http://latex.codecogs.com/gif.latex?S_2)

### Implementation procedure
- First, obtain the images and check whether the images are the same size. If they have different sizes, resize the smaller one to the bigger one.
- The idea for image hybridization is to combine a low-pass filtered image with another high-pass filtered image.
- First, transform the original image to the low-pass filtered image by using the gaussian_filter function. There is a parameter freq, which is called the “cutoff frequency”, controls how much frequency to leave in the transformed image and affects the blurriness of the low-pass filtered image.
- Then generate a high-pass filtered version of another image by subtracting a blurred version of the image itself.
- Finally, blend two images by adding them together.

<div align=center>
<img src="https://i.imgur.com/5jfwiqH.jpg" width=80%>
</div>

### Experimental results

<div align=center>
<img src="https://i.imgur.com/9rnCfGt.jpg" width=80%>
<img src="https://i.imgur.com/DhGPAPz.jpg" width=80%>
<img src="https://i.imgur.com/thIutOP.jpg" width=80%>
<img src="https://i.imgur.com/ZYWyNVZ.jpg" width=80%>
</div>



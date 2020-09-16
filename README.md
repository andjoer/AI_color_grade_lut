# Creating color lookup tables with AI
Creating color LUTs with artificial intelligence

This repository contains

- a modified version of the pix2pix version created by the Tensorflow authors so that the resulting models are smaller
- a notebook that takes an image and a tensorflow model and creates a color lookup table with it
- a Flask app with a Web based UI

A working version of the Flask app can be found here:  ec2-3-136-61-119.us-east-2.compute.amazonaws.com

The scope of this repository is
- show that the pix2pix GAN is applicable for a variety of tasks that are not classic image to image conversion. 
- demonstrate how to use a model that produces low fidelity images (low resolution and artefacts) to get a high fidelity, production ready output
- enable people who never saw code to experiment and train their own models since the code does not need to be toched

# Create training data
- In order to train the model you need to prepare the training data as it was done in the original pix2pix paper. The model gets trained by showing it the image how it should be color graded (the "ground truth") and the input that should be color graded. These images are combined together beside each other in one image, while the ground truth in on the left and the input is on the right. If you use the network with the reduced input size of 64 pixel, it should look like in the image below. A sample image could be found in the "generate training data" folder.

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/Training_images.jpg?raw=true">
</p>

- In order to get the training data the idea is not grade input images in order to generate the ground truth. It is better to use frames from movies that are graded as ground truth and to mess them up with random operations in order to generate some fake input. I have added an after effects file that does this in the "generate training data" folder. But this is for sure not the optimum, so please feel motivated to look for better ways in or outside of after effects of manipulating the ground truth. You will see that you need to think about what you are teaching the network. If you have a dark and blueish ground truth and this is your desired result, you should nevertheless not only give the network too bright and warm images because otherwise it will learn to make the images cooler and darker in general - even if they are too dark. 

# Below is a user guide for people who are absolutly new to using Jupyter notebooks and Google Colab

- go to the Notebook you would like to use (for training 64pix2pix) and open in Colab

<p align="center">
  <img width="823" height="476" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/open_colab.jpg?raw=true">
</p>



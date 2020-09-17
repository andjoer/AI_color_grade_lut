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

# Algorithm

Color lookup tables are lists of triplets that can be interpreted as n x n x n x 3 matrices, in other words, it contains n^3 coordinates of color values. Through interpolation they represent an function R^3 to R^3 that is mapping intput colors to output colors. That's why it is possible to represent any (primary) colorcorrection with a single LUT file. 

The idea behind this color grading approach is to start with something existing, namely the pix2pix network (originally written by Phillip Isola Jun-Yan Zhu Tinghui Zhou Alexei A. Efros) and adopt it to this task. Indeed the pix2pix algorithms learns pretty fast to grade the footage but has the downside that it is only able to process 256x256 pixels images and is not free of artefacts. By using the basic machine learing algorithm of knn interpolation it is possible to determine the LUT that is needed to correct the input image into the predicted output of the pix2pix network. (Fun Fact: if someone publishes a before/after image he basically publishes the LUT). Due to the interpolation artefacts are compensated and the LUT can be applied to images of any size. 

However it needs to be mentioned that due to the fact, that pix2pix is not invented for this task, it is not the fastest algorithm. The generator is hour-glass shaped and first "interprets" an 256x256x3 pixel image and afterwards generates an image of same dimension. So the generating parts generates at first something way more complex then a LUT. 

That is why I decided to make the network smaller and take 64x64x3 images. The downside of course is that it "sees" less details. But according to my obeservations it still performs well. If we look at a 16x16x16 points LUT, it has 16x16x16x3 = 4096x3 values which is the same as a 64x64x3 = 4096x3 image. However the complexity is higher then in a 8x8x8 points LUT. 


# Create training data
- In order to train the model you need to prepare the training data as it was done in the original pix2pix paper. The model gets trained by showing it the image how it should be color graded (the "ground truth") and the input that should be color graded. These images are combined together beside each other in one image, while the ground truth in on the left and the input is on the right. If you use the network with the reduced input size of 64 pixel, belows sizes would be sufficient. However you may also upload higher resolution images since they get resized in the code. A sample image could be found in the "generate training data" folder.

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/Training_images.jpg?raw=true">
</p>

- In order to generate the training data the idea is not grade input images in order to generate the ground truth. It is better to use frames from movies that are graded as ground truth and to mess them up with random operations in order to generate some fake input. I have added an after effects file that does this in the "generate training data" folder. But this is for sure not the optimum, so please feel motivated to look for better ways in or outside of after effects of manipulating the ground truth. You will see that you need to think about what you are teaching the network. If you have a dark and blueish ground truth and this is your desired result, you should nevertheless not only give the network too bright and warm images because otherwise it will learn to make the images cooler and darker in general - even if they are too dark. 

- If this is setup you need to export an image sequence in jpg format. 

- As always when you train an AI model you have to split the images into a train and a test folder. I would say approx. 20% of the images should go into the test folder and the rest should go into the train folder. The test and the train folder need to be in one folder that can have an arbitrary name. But the train and the test folder need to have exactly these names. 

<p align="center">
  <img width="711" height="166" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/folder_structure.JPG?raw=true">
</p>


<p align="center">
  <img width="761" height="760" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/image_sequence.JPG?raw=true">
</p>

- finally the complete folder (above named "example") needs to be zipped. 

# Below is a user guide for people who are absolutly new to using Jupyter notebooks and Google Colab

- go to the Notebook you would like to use (for training 64pix2pix) and open in Colab

<p align="center">
  <img width="823" height="476" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/open_colab.jpg?raw=true">
</p>

- press on the folder icon and drag/dropped your zipped folder into the empty space

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/Upload_train.JPG?raw=true">
</p>

- press "Run all"

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/Run_all_train.jpg">
</p>

- now you basically just need to wait. If you scroll down you can observe the training progress

<p align="center">
  <img width="963" height="397" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/training_scroll.JPG?raw=true">
</p>

- once the training is finished your model will will be saved and you can download it. This model can be used in the second notebook in order to create the LUT

<p align="center">
  <img width="717" height="454" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/training_done.JPG?raw=true">
</p>

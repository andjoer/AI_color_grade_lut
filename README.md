# Creating color lookup tables with AI
By using this repository you can create LUTs in the .cube format that can be read by most image editing or color grading software.

All is set up in Google Colab - it can be tried out in the browser without any knowledge about programming and installing software.

This repository contains

- a modified version of the pix2pix version created by the Tensorflow authors so that the resulting models are smaller
- a notebook that takes an image and a tensorflow model and creates a color lookup table with it
- a Flask app with a Web based UI

The scope of this repository is
- show that the pix2pix GAN is applicable for a variety of tasks that are not classic image to image conversion. 
- demonstrate how to use a model that produces low fidelity images (low resolution and artefacts) to get a high fidelity, production ready output
- enable people who never saw code to experiment and train their own models since the code does not need to be toched

## Algorithm

Color lookup tables are lists of triplets that can be interpreted as n x n x n x 3 matrices, in other words, it contains n^3 coordinates of color values. Through interpolation they represent an function R^3 to R^3 that is mapping intput colors to output colors. That's why it is possible to represent any (primary) colorcorrection with a single LUT file. 

The idea behind this color grading approach is to start with something existing, namely the pix2pix network (originally written by Phillip Isola Jun-Yan Zhu Tinghui Zhou Alexei A. Efros) and adopt it to this task. Indeed the pix2pix algorithms learns pretty fast to grade the footage but has the downside that it is only able to process 256x256 pixels images and is not free of artefacts. By using the basic machine learing algorithm of knn interpolation it is possible to determine the LUT that is needed to correct the input image into the predicted output of the pix2pix network. (Fun Fact: if someone publishes a before/after image he basically publishes the LUT). Due to the interpolation artefacts are compensated and the LUT can be applied to images of any size. 

However it needs to be mentioned that due to the fact, that pix2pix is not invented for this task, it is not the fastest algorithm. The generator is hour-glass shaped and first "interprets" an 256x256x3 pixel image and afterwards generates an image of same dimension. So the generating parts generates at first something way more complex then a LUT. 

That is why I decided to make the network smaller and take 64x64x3 images. The downside of course is that it "sees" less details. But according to my obeservations it still performs well. If we look at a 16x16x16 points LUT, it has 16x16x16x3 = 4096x3 values which is the same as a 64x64x3 = 4096x3 image. However the complexity is higher then in a 8x8x8 points LUT. If you want to experiment with this you need ground truth LUTs. So I added a notebook in the repository that generates the LUTs between your input and ground truth images - "BatchPix2LUT". 

For further experimentation you can use the 128pixel network that processes the images width 128*128 pixels. Maybe you are wondering if it is a good idea to make it asymmetrical so that the network gets more information but produces only the few color samples that are needed to produce the LUT. I have enclosed a notebook for this as well - it works, but you actually don't save much. 

# Pix2LUT

I have also created a discriminator and a generator network in the gan structure that are taking (256x256 pixels) as input and are returning directly a color LUT (8^3*3; 1D). This is work in progress and experimental. For training use the same images as you would upload to pix2pix or to batch_pix2lut. Just put all LUTs generated with the batch-notebook in the train images and the test images (you don't need to split it, just put all in both folders - not very nice, but it is work in progress) and upload them zipped into the colab. During training instead of output images the notebook displays the reduced mean difference between the generated LUTs and the ground truth LUTs.

In order to get a feeling if the output result is good you have to consider: The input images are 8bit, so basially they have a tollerance of +- 0.002. One solution would be to create a "mean" LUT, like a neutral LUT that does nothing. The mean difference between most of the LUTs and this standard LUT is around 0.12. Below you may see the training results. 

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/gan_loss.jpg?raw=true">
</p>

In the next image an actual application of the generated LUT is displayed. The network is trained on the look of Game of Thrones S8 E2. The images are blurred in order to avoid copyright issues. As you could see, the skinn tones are slightly too saturated and too yellow. The explanation is that in the same scene the skin of Daenerys Targaryen has this skin tone in the close-up shots. This is an in general observable behaviour: If there are more looks within the training data, the model selects one that matches the input the best. 

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/Result_pix2LUT.jpg?raw=true">
</p>

Since a 3D LUT can be interpreted not only as just target points but also as 3 channel correction values on a nxnxn grid, I tried to remain the hourglass shape of the generator and deconvolute the result-vector of the convolutions in 3D (plut 3 channel) space. It works, but so far I did not observe an advantage. 

## One model that can generate any look

Although the training times are ok and often not many Epochs are needed, it is a bit suboptimal that you need to prepare the training data for every look. But there is a way to make one model for all looks: If you do it in reverse. 

I have already begun to train a model (neutral.h5) that removes any look from the footage. By reversing input and output in the model_img2LUT algorithm the result is a LUT that gives the neutralized footage the look. So once you apply the LUT on your (neutralized) footage, it will have the same look. It is important to mention that due to a lack of time I did not train this model well. But feel free to do better: As ground truth you need to take neutral footage, either from your own stock or e.g. TV news. Then you apply random LUTs/presets/gradings in order to generate the input files. With these pairs you can train the network above. 

The downside is the problem that every preset or LUTs have: the LUT is not optimized for your footage. So the LUT is only for the look, but not for the correction. It might be a bit better if you apply the neutralize model also on your input footage in order to correct it to the same neutral basis. However if you have colors in your footage that were not present in the reference footage it might not help. 

If you have trained your model to neutralize looks, you need to set reverse = True in the model_img2LUT notebook. (for those who are new to python: True needs to be written with capital "T") 

## Conclusion 

It is easy to apply existing AI algorithms for color correction/grading. With the pix2LUT GAN a method is demonstrated that generates a list of data from an image. For simplicity reasons this algorithm creates easy to read LUTs. However it should be no problem to replace this lists with lists of slider positions of any color correcting software. If it is possible (which in most cases is possible) that the slider positions of two consecutive corrections can be cumulated by an algorithm to one position, any look can be achived with one trained model that neutralizes any look. 

# User guide

## Create training data
- In order to train the model you need to prepare the training data as it was done in the original pix2pix paper. The model gets trained by showing it the image how it should be color graded (the "ground truth") and the input that should be color graded. These images are combined together beside each other in one image, while the ground truth in on the left and the input is on the right. If you use the network with the reduced input size of 64 pixel, belows sizes would be sufficient. However you may also upload higher resolution images since they get resized in the code. A sample image could be found in the "generate training data" folder.

<p align="center">
  <img width="600" height="600" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/Training_images.jpg?raw=true">
</p>

- In order to generate the training data the idea is not grade input images in order to generate the ground truth. It is better to use frames from movies that are graded as ground truth and to mess them up with random operations in order to generate some fake input. I have added an after effects file that does this in the "generate training data" folder. But this is for sure not the optimum, so please feel motivated to look for better ways in or outside of after effects of manipulating the ground truth. You will see that you need to think about what you are teaching the network. If you have a dark and blueish ground truth and this is your desired result, you should nevertheless not only give the network too bright and warm images because otherwise it will learn to make the images cooler and darker in general - even if they are too dark. 

- If this is setup you need to export an image sequence in jpg format. The amount of training images should be around 1000

- As always when you train an AI model you have to split the images into a train and a test folder. I would say approx. 20% of the images should go into the test folder and the rest should go into the train folder. The test and the train folder need to be in one folder that can have an arbitrary name. But the train and the test folder need to have exactly these names. 

<p align="center">
  <img width="711" height="166" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/folder_structure.JPG?raw=true">
</p>


<p align="center">
  <img width="761" height="760" src="https://github.com/ajcommercial/AI_color_grade_lut/blob/master/screenshots/image_sequence.JPG?raw=true">
</p>

- finally the complete folder (above named "example") needs to be zipped. 

## Train the model and generate the LUT

- Upload the training data into the 64pix2pix notebook and start the training
- Download the model
- Upload the model and the image that should be trained into the pix2LUT notebook
- Generate and download the LUT

## Below is a user guide for people who are absolutly new to using Jupyter notebooks and Google Colab

- go to the Notebook you would like to use (for training 64pix2pix or 128pix2pix) and open in Colab

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

- Open the Notebook model_img2LUT (like you did with the other notebook)
- Upload the model and the image you would like to grade (for download procedure see above)
- Start the program (like above "run all")
- Wait until you see the generated .cube file in the content folder
- Download the .cube file and apply it in any program that can apply LUTs (Photoshop, Premiere, Resolve etc.)

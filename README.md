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


<h1 align="center">Generation of Super Resolution Images using
Deep Neural Networks</h1>

<p align="center">
<img src="Images/nrsc_logo.png" width="" height="">
</p>

## Abstract:
Super Resolution Images are required to properly perceive the intricacies of any given image. Satellite imaging is one such domain where details of an image must be preserved extremely carefully since image quality decreases drastically at high magnification. Due to developments in the disciplines of computer vision and deep learning, super-resolution which tries to increase image resolution by computational means has advanced recently. Convolutional neural networks built on a range of architectures, such as autoencoders, generative adversarial networks, and residual networks, have been used to tackle the issue. Few studies concentrate on single or multi-band analytic satellite imaging, whereas the majority of research focuses on the processing of images with simply RGB colour channels. Super resolution is a highly important and significant operation that must be carried out carefully in the realm of remote sensing. This work proposes a cutting-edge architecture AutoEn-GAN for the super-resolution of satellite images by blending autoencoders with an adversarial setting. All of the models’ output is compared to the recently developed SR GAN, SR-ResNet, and EDSR models, and the traditional super-resolution benchmark using bicubic interpolation. Results of the AutoEn-GAN super-resolution method show a significant improvement over other state of the art methodologies such as SR-GAN. 

<p align="center">
<img src="RRSC Images/RRSC East new.png" width="" height="">
<p>RRSC - East Campus (Newtown, Kolkata)</p>
</p>


## Overall Framework


<div align="center"><img src="Images/Full Diagram.png" width="600" height=""></div>

## Model :

AutoEn-GAN Model Architecture

<div align="center"><img src="Images/AE_GAN.png" width="600" height=""></div>

Residual Block 

<div align="center"><img src="Images/Comperison_Model.png" width="600" height=""></div>

Model Training

<div align="center"><img src="Images/Training AEGAN.png" width="600" height=""></div>


## Results:

<div align="center"><img src="Images/img-after.jpeg" width="600" height="""></div>

Sample patches of all images after transfer learning and training of the model(a) Input Image, (b) Bicubic Interpolation, (c) EDSR, (d) SR(PRE), (e) SR(GAN), (f) Proposed Model, (g) Original Image

<div align="center"><img src="Images/after training.jpg" width="600" height="""></div>

Comparison of the matrices (A) PSNR Values, (B) SSIM Values, (C) RMSE Values



## AutoEn-GAN App:
<div align="center"><img src="Images/APP.png" width="600" height=""></div>

## Internship Certificate:
<p align="center">
<img src="Images/Certificate.png" width="650" height="">
</p>
  

## Quick Links:


[![report](https://img.shields.io/badge/Final-Report-brightgreen)](https://github.com/abhimanyubhowmik/Internship_Repository_RRSC_East-ISRO/blob/main/Reports/Final_Report_RRSC_East.pdf) 
[![LOR](https://img.shields.io/badge/Internship-LOR-blue)](https://github.com/abhimanyubhowmik/Internship_Repository_RRSC_East-ISRO/blob/main/Documents/Letter%20of%20Recomendation.pdf) 
[![manual](https://img.shields.io/badge/Installation-Manual-red)](https://github.com/abhimanyubhowmik/Internship_Repository_RRSC_East-ISRO/blob/main/Documents/Installation%20Manual.pdf)
[![slides](https://img.shields.io/badge/Presentation-Slides-yellow)](https://docs.google.com/presentation/d/1mL79WjyZKTuVd0xXJUCqsT4LImveNArbrmySNEe2f4o/edit?usp=sharing) 


## References Used:
- https://arxiv.org/abs/1609.04802
- https://arxiv.org/abs/1707.02921
- https://arxiv.org/abs/2203.09445
- https://www.uni-goettingen.de/de/document/download/e3004c6e53ca2fa0a30d53d98a52c24e.pdf/MA_Freudenberg.pdf

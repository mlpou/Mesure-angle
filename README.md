# Mesure-angle
# Context
FleYe calibration method is aimed to generate a general equation representing the angle formed by a light source and a camera at a variable altitude. The data obtained by applying this data analysis is useful to the model ILLUMINA developed by the professor Martin Aubé  (http://obsand.org/wiki/index.php?n=Prof.IllumEn). It is used to grasp a better understanding of the impact of light pollution in the environnement. To obtain data, the FleYe system is attached to a stratospheric balloon. FleYe is a 12 camera positioned to create a half-sphère shape, allowing it to cover and take pictures of the ground for 360 degrees. These flights are done during the night to better detect the light sources. During these flights, FleYe takes photos of the region beneath itself. These photos are then analysed with FleYe calibration method. 

# Material
- iPano RS232" camera mount (its command set is part of the repository (iPano RS232 Command.pdf))
- 3D printed adaptator for the FleYe to fit on the mount
- Tripod (we used a bonifoto)
- Raspberry pi
- Red LED
- Breadboard

# Procedures
The first step of the calibration is a photo capture. The FleYe has to capture a reference point at different known relative angles. It was decided that the reference point would be fixed, and that the FleYe would move to create those angles. The FleYe was set on the iPano camera mount with our adaptator, wich was placed on the tripod. Our referance point was a red LED that was suspended to the ceiling on a breadboard, but any small source of light could work. It is important that the LED is the only source of light in the room, because otherwise the analysis could be biaised. We recomand a to choose a room with no window and to tape cardboard on the sides of the door. The FleYe was connected to a raspberry pi that would control the photo capture. We took 12 960 pictures, so a SD card or a hard drive is recommended if there is not enough storage on the pi itself. Then, in order to obtain the most reliable result, the LED has to be centered with the FleYe's center camera. In our case, it was camera C on raspberri pi 172.20.4.162. The program "Photo.py" take a picture only with the center camera and transfers it to the raspberry pi. Then, "centuring.py" returns the emplacement of the center of mass of the light from the LED with an array presenting its x and y position. The ideal value would be (2028, 1520) but we accepted a 50 to 75 pixel error on each value. Once it was centered, the program "Control.py" is ready to be lauched. "Control.py" uses the "Ipano.py" serial method developed by Alexandre Simoneau (original repository : https://github.com/alsimoneau/ipano.git) which is based on the command set (iPano RS232 Command.pdf) and converts it into python fonctions. The right port has to be defined when seting the ipano object. It sould will be printed each time the code runs. There also might be some ajustement to make with the paths troughout the whole code. Finally, the amount of pictures to be taken, the angles' precision is controlled and the pause time between the captures is are determined by the input parameters of the "measures" fonction. "altIteration", the first parameter, determines the number of altitude angles that the mount will take. "altPrecision", the second parameter, determines the space in degree in between each altitude angle. The mount will distribute evenly the captures on both sides of the zenith. Make sure that the maximum angle that the mount will take (altIteration*altPrecision/2) is lower that 45 degrees, because it is the physical limit of the mount. "azIteration" determines the number of azimuth angles the mount will take for each altitude angle. "pauseTime" determines the pause time take between each set of pictures (we recomand not using a value under 5). The whole capture process will take many hours/days depending on how many pictures will be taken. We used used "measures(90,1,12,5)" for a total of 1080 pictures and we estimated that it took a bit more than 24 hours. All the pictures will be stored in a directory called "data" under the following organisation :

data -> pi's ID -> camera letter

Once the pictures are taken, they have to be analysed. The programs "data_analysis" and "data_analysis_mc" create a second degree polynomial regression. "data_analysis" uses the brightest pixel as a reference value and "data_analysis_mc" uses the mass center of the bright pixels as a reference value. We recomand using the mass center, as it is more acurate. The variables "alt", "precision" and "az" correspond to "alIteration", "altPrecision" and "azIteration" from "Control.py". It is important that they corespond. The "analysis" fonction sould be called with each camera's path so that they all get a regression. A text file we be created in the same path. The "polyRelation2" fonction returns coefficients from the polynomial regression between the x and y pixel position of the light and the altitude and latitude angles.
The indexes corespond to the following : 

    0 -> Constant
    
    1 -> x coefficient
    
    2 -> x^2 coefficient
    
    3 -> y coefficient
    
    4 -> y^2 coefficient
    
The first array is the altitude's regression and the second is the azimuth's regression. 

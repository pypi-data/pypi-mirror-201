# faciesteller
faciesteller is a Python package as Techlog plug-in, which automate facies classifaction from borehole image. 


## installation
To install faciesteller, you need to navigate to Python3 folder of Techlog using command prompt.
The usual Techlog Python3 folder address likes this: "C:\Program Files\Schlumberger\Techlog Version\Python3".
Code in: python.exe -m pip install faciesteller and hit execute, that is it.


## usage
The model has been trained with Resnet50 using local FMI image and geolgical interpretation. It might be used in same geological area with caution, while local expertise is very important and advised though. 

To successfully predict faices, need to have the training model (model.h5) in the following address:
C:\Users\username\AppData\Roaming\Schlumberger\Techlog\model\model.h5

As for pratical manipulation, it requires to open a new python eiditor in Techlog and paste below coding inside, add three rows for inputs in paramters area. The rows are CSV path for depth data, img path for FMI image and well name.

Code to use in python script area:

from faciesteller.faciesteller import FaciesClassifier

fc = FaciesClassifier(csv_path, img_path, well_name)
df_csv, img_array = fc.load_data()
print("DataFrame shape: ", df_csv.shape, 
	"\nImagearray shape: ", img_array.shape)
	
df_output = fc.imagetochunk(df_csv, img_array)

df_predict = fc.predict(df_output)
print(df_predict)


## contributing
If you'd like to contribute to faciesteller, please contact me.


## license
My Package is licensed under the MIT License. See LICENSE for more information.
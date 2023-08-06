# faciescanner
faciescanner is a Python package as Techlog plug-in, which automate facies classifaction from borehole image. 


## installation
To install faciescanner, you need to navigate to Python3 folder of Techlog using command prompt.
The usual Techlog Python3 folder address likes this: "C:\Program Files\Schlumberger\Techlog Version\Python3".
Code in: python.exe -m pip install faciescanner and hit execute, that is it.


## usage
The model has been trained with EfficientNetB4 pre-trained model using local FMI image and geolgical interpretation. It might be used in same geological area with caution, while local expertise is very important and advised though. 


As for pratical manipulation, it requires to open a new python eiditor in Techlog and paste below coding inside, add image array and depth in paramters area. The parameters name should be consistent with python coding.

Code to use in python script area:

from faciescanner.data_input import DataInput

di = DataInput(FMI_STAT_FULL,TDEP)
df_output, X = di.image2chunk()
df_pred = di.predict(df_output, X)
di.create_new_zone(df_pred)

Hit Launch in PythonScript menu of Techlog, result will be avlaible under well in Techlog.


## contributing
If you'd like to contribute to faciescanner, please contact me.


## license
My Package is licensed under the MIT License. See LICENSE for more information.
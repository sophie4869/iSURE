Github Page: https://github.com/sophie4869/iSURE

Python: 2.7.6

MATLAB: R2014a

## /HR: Heart rate detection
### google-glass-sensors
This is the Google Glass project on Android Studio to record sensor data. It writes to ```sensordata0.txt``` on Glass, and can also post the data online. Change the 444 line of ``/google-glass-sensors/app/src/main/java/com/morkout/locationsensors/SensorActivity.java`` to the address of poSensorData.php file on your server.
### rate.m
This is the MATLAB program that calculates the heart rate based on data file. From MATLAB, import the data and change the variable names to ``t``, ``x``, ``y`` and ``z``.
### HR_offline.py
Run this script to detect heart rate from data file. Change the data file path in line 14.
### poSensorData.php
This posts sensor data to database. Change the database configuration to use. Don't forget to change the address of this php file in the Google Glass app.
### HR_realtime.py
Change the database configuration in line 12 to use. This reads heart rate in real-time.
### insert.py
A script to insert local data to the database. Change the configuration on line 5.
### hello.py
A simple example of using SL4A.
## /HAR: Human activity recognition
### FeatureExtraction.py
This scripts extracts selected features from .csv data file. You can then convert the result to .arff format to use in Weka.
> _Notice: this script calculates statistic features(mean, variance, etc). Make sure that the input data file is of single label data. Combine different label data into a single .csv file AFTER the use of this script, and then convert to .arff file._

1. Copy this to the path where the train set and test set are
2. Run ```python  path_to_data_set path_to_result.csv```
3. Make sure the ``csv2arff`` class is in the same directory. Convert resulted ```.csv``` file to ```.arff``` file by: ```java csv2arff path_to_csv path_to_arff```
4. Now you can use ```.arff``` file in Weka. Enjoy!



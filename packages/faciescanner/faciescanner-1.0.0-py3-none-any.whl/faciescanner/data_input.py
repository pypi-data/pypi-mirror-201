import base64
import time
import io
import dataikuapi
import numpy as np
import pandas as pd
import TechlogDatabase as db

from typing import List
from PIL import Image


# Define class to wrap differnt functions for FaciesClassifier
class DataInput:
    def __init__(self, img_array, depth):
        self.img_array = img_array
        self.depth = depth
        
    def timer_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            return result
        return wrapper
        
    @staticmethod
    def tech2np(tech_array):
        """
        Converts a Techlog array to a numpy array.
        Args:
            tech_array(Techlog.Data.Array): The Techlog array to be converted.    
        Returns:
            np_array(numpy.ndarray): the converted numpy array.
        """    
        nrows = tech_array.referenceSize()
        ncols = tech_array.columnCount()
        np_array = np.zeros((nrows,ncols), dtype='float64')
        for i in range(nrows):
            np_array[i] = tech_array.valueList(i)
        return np_array        
    
    @staticmethod
    def get_zone_values(df_pred):
        """
        Given a prediction dataframe containing facies value, return start depth and 
        predicted facies value for each new facies zone.
        Args:
            df_pred(pandas.DataFrame): pandas dataframe containing predicted facies values, 
        with columns 'start_depth' and 'predicted_facies'.
        Returns:
            interval_list(list): a list of start_depth values for each new facies zone.
            zone_list(list): a list of predicted_facies for each new facies zone.  
        """
        # check input type
        if not isinstance(df_pred, pd.DataFrame):
            raise TypeError("Check input, should be a pandas dataFrame.")
        
        # initialize empty lists to store start_depth and predicted_facies
        interval_list = []
        zone_list = []
        
        # loop through df_pred and check if predicted_facies value changes
        current_facies = None
        for index, row in df_pred.iterrows():
            if current_facies is None:
                # set current facies value for fist row
                current_facies = row['predicted_facies']
            elif current_facies != row['predicted_facies']:
                # facies chagned, add start_depth and predicted_facies values
                interval_list.append(row['start_depth'])
                zone_list.append(row['predicted_facies'])
                current_facies = row['predicted_facies'] 
        return interval_list, zone_list       
        
     # fucntion to break fmi image into chunks, save into dataframe.   
    def image2chunk(self):  
        """
        create chunk images in dataframe for prediction.
        Args:
            img_array(Techlog.Data.Array): FMI array containting the images.
            last_index(int): Index of the last image to be included in the subsample.   
        Returns:
            df_output (pandas.DataFrame): The chunk image.
            X(numpy.ndarray): The preprocessed image data for prediction.
        """
        # define input
        img_array = self.img_array
        depth = self.depth
        
        # get the last index
        last_index = depth.referenceSize()-1
        
        # define empty dataframe
        df_output = pd.DataFrame(columns=['chunk_image', 'start_depth', 'end_depth'])
        
        img_img = self.tech2np(img_array)
        r,c = img_img.shape
        chunk_size = 360
                
        for i in range(0, r, chunk_size):
            for j in range(0, c, chunk_size):
                if i + chunk_size <= last_index and j + chunk_size <= c:
                    chunk = img_img[i:i+chunk_size, j:chunk_size]
                    
                    if chunk.shape == (360, 360):
                        row = {'chunk_image': chunk, 'start_depth': img_array.referenceValue(i), 
                               'end_depth': img_array.referenceValue(i + chunk_size)}                       
                        df_output = df_output.append(row, ignore_index = True)
        
        X = []
        for i, row in df_output.iterrows():
            image = np.array(row['chunk_image'])
            X.append(image)

        # Convert the images to numpy array
        X = np.array(X)
        
        # Normalize the array
        # X_norm = (X - np.min(X)) / (np.max(X) - np.min(X))
        # X_norm *= 255
        
        # Convert to type uint8
        X = X.astype('uint8')
        print(len(df_output))
        print(X.shape)   

        return df_output, X
    
    @timer_decorator     
     # fucntion to predict with trained model   
    def predict(self, df_output, chunk_array):
        """
        This function takes in a dataframe of chunk images, preprocess and make predictions using a trained model.
        Args:
            df_output: Pandas dataframe containing chunk images and corresponding depth
            chunk_array: The preprocessed image data for prediction, Numpy array.   
        Returns:
            df_pred: Pandas dataframe with predicted facies and corresponding probablities
        """
        # creat predication dataframe
        df_pred = df_output.copy()
        
        # class label from 0 to 9 in list
        class_labels = ['Mature Paleosol', 'Siltstone', 'Heterolithic Sandstone', 'Immature Paleosol', 
                        'Heterolithic Shale', 'Crossbedded Sandstone', 'Massive Sand']
        
        # define dataiku API
        client = dataikuapi.APINodeClient("http://136.252.73.83:12000", "faciesteller")
        
        # define prediction labels and probabilities
        predicted_class_labels = []
        predicted_probabilities = []
        
        # convert image array to image and send back to server for prediction result
        for i in range(chunk_array.shape[0]):
            chunk_array_temp = (chunk_array[i].astype(np.uint8))
            if chunk_array_temp.ndim == 2:
                # Grayscale image: convert to RGB
                chunk_array_temp = np.stack([chunk_array_temp] * 3, axis=-1)
            elif chunk_array_temp.shape[2] == 1:
                # Single-channel image: convert to RGB
                chunk_array_temp = np.repeat(chunk_array_temp, 3, axis=-1)
    
            chunk_image = Image.fromarray(chunk_array_temp, mode='RGB')
            buffer = io.BytesIO()
            chunk_image.save(buffer, format='PNG')
            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            payload = {'input': base64_str}
            prediction = client.predict_record("tell_facies", payload)
            # print(prediction)
            prediction_result = prediction.get("result", {})
            prediction_value = prediction_result.get("prediction")
            
            if prediction_value is not None:
                label = class_labels[int(prediction_value)]
                print(label)                
                predicted_class_labels.append(label)
                max_prob = max(prediction_result['probas'].values())
                print(max_prob)
                predicted_probabilities.append(np.round(max_prob,2)*100) 
            else:
                # handing mssing prediciton value
                print('prediction_value from json is None')
                predicted_class_labels.append("unknown")
                predicted_probabilities.append(0)  
    
        df_pred['predicted_facies'] = predicted_class_labels
        df_pred['probability'] = predicted_probabilities    
        
        return df_pred
    
    def create_new_zone(self, df_pred):
        """
        create new dataset with intervals defined by the predicted facies values.
        Args:
            wellName(str): name of the well
            datasetName(str): name of the dataset to create
            var(str): name of the variable to create
            unit(str): unit of measurement for the variable
            df_pred(pandas.DataFrame): Pandas datafrarme containing predicted facies values, 
            with columns "start_depth" and "predicted_facies"   
        Returns:
            None
        """
        
        # Get well name etc.
        depth = self.depth
        wellName = depth.wellName()
        datasetName = wellName + '_Facies_Predicted'
        var = 'Zone Name'
        unit = ''
        
        # check input types
        if not isinstance(wellName, str):
            raise TypeError("Well name must be a string.")
        if not isinstance(datasetName, str):
            raise TypeError("Dataset name must be a string.")
        if not isinstance(var, str):
            raise TypeError("Variable name must be a string.")
        if not isinstance(unit, str):
            raise TypeError("Unit must be a string.")
        if not isinstance(df_pred, pd.DataFrame):
            raise TypeError("Input dataframe must be a pandas dataframe.")
        
        # Check well and dataset existence
        if not db.wellExists(wellName):
            raise ValueError("Well does not exist.")
        if db.datasetExists(wellName, datasetName):
            db.datasetDelete(wellName, datasetName)

        # Get interval and zone values
        interval, zones = self.get_zone_values(df_pred)
        
        # Create dataset and save variable
        db.datasetCreate(wellName, datasetName, 'MD', 'Measured Depth', 'm', interval)
        db.datasetTypeChange(wellName, datasetName, 'interval')
        if db.variableSave(wellName, datasetName, var, 'Zone Name', unit, zones):
            print('The variable %s.%s.%s has been successfully created.'%(wellName, datasetName, var))
        else:
            print('ERROR: The variable %s.%s.%s cannot be created.'%(wellName, datasetName, var))
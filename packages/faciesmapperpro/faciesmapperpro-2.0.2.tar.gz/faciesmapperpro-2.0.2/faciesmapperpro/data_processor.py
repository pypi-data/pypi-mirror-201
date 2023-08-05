import base64
from typing import List
import time
import io

import dataikuapi
import numpy as np
import pandas as pd
from PIL import Image

import TechlogDatabase as db

class DataProcessor:
    def __init__(self, fmi_array, tdep):
        self.fmi_array = fmi_array
        self.tdep = tdep

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
            tech_array (Techlog.Data.Array): The Techlog array to be converted.
            
        Returns:
            np_array (numpy.ndarray): The converted numpy array.
        """
        nrows = tech_array.referenceSize()
        ncols = tech_array.columnCount()
        np_array = np.zeros((nrows, ncols), dtype='float64')
        for i in range(nrows):
            np_array[i] = tech_array.valueList(i)
        return np_array
    
    @staticmethod
    def get_reference_values(pred_df):
        """
        Given a pandas dataframe containing predicted facies values, return the start_height and predicted_facies values
        for each new facies zone.

        Parameters:
        pred_df (pandas.DataFrame): a pandas dataframe containing predicted facies values, with columns 'start_height' and
                                    'predicted_facies'

        Returns:
        reference_list (list): a list of start_height values for each new facies zone
        zone_list (list): a list of predicted_facies values for each new facies zone
        """
        # Check input type
        if not isinstance(pred_df, pd.DataFrame):
            raise TypeError("Input must be a pandas dataframe.")

        # Initialize empty lists to store start_height and predicted_facies
        reference_list = []
        zone_list = []

        # Loop through the dataframe and check if the predicted_facies value changes
        current_facies = None
        for index, row in pred_df.iterrows():
            if current_facies is None:
                # first row, set the current facies value
                current_facies = row['predicted_facies']
            elif current_facies != row['predicted_facies']:
                # facies changed, add the start_height and predicted_facies values to the lists
                reference_list.append(row['start_height'])
                zone_list.append(row['predicted_facies'])
                current_facies = row['predicted_facies']

        return reference_list, zone_list
    
    def create_subsample(self):
        """
        Creates a subsampled dataframe of images for prediction.
        
        Args:
            fmi_array (Techlog.Data.Array): The FMI array containing the images.
            last_index (int): The index of the last image to be included in the subsample.
            
        Returns:
            df_final (pandas.DataFrame): The subsampled dataframe of images.
            X (numpy.ndarray): The preprocessed image data for prediction.
        """
        fmi_array = self.fmi_array
        tdep = self.tdep

        # get the last index
        last_index = tdep.referenceSize() - 1
        
        # Declare an empty dataframe
        df_final = pd.DataFrame(columns=['image_data', 'start_height', 'end_height'])

        fmi_img = self.tech2np(fmi_array)
        r, c = fmi_img.shape
        subsample_size = 224

        for i in range(0, r, subsample_size):
            for j in range(0, c, subsample_size):
                if j + subsample_size <= c and i + subsample_size <= last_index:
                    sub_image = fmi_img[i:i + subsample_size, j:j + subsample_size]

                    if sub_image.shape == (224, 224):
                        row = {'image_data': sub_image, 'start_height': fmi_array.referenceValue(i), 'end_height': fmi_array.referenceValue(i + subsample_size)}
                        df_final = df_final.append(row, ignore_index=True)

        X = []
        for i, row in df_final.iterrows():
            image = np.array(row['image_data'])
            X.append(image)

        # Convert the images to numpy array
        X = np.array(X)
        
        # Normalize the array
        X_norm = (X - np.min(X)) / (np.max(X) - np.min(X))
        X_norm *= 255
        
        # Convert to type uint8
        X = X_norm.astype('uint8')   

        return df_final, X
    
    @timer_decorator
    def predict(self, df, img_data):
        """
        This function takes in a dataframe of subsampled images, preprocesses them, and makes predictions using a trained model
        Arguments:
        - df: A pandas dataframe containing subsampled images and their corresponding heights
        - img_data: A numpy array containing the subsampled images
        - wellname: Name of the well to create a new zone for
        
        Returns:
        - res_df: A pandas dataframe with predicted facies and corresponding probabilities
        """
        res_df = df.copy()
        class_labels = ['Mature Paleosol', 'Heterolithic Shale', 'Silt stone', 'Massive Sand', 'Immature Paleosol', 'Heterolithic Sandstone', 'Laminated Sand', 'CrossBedded Sandstone', 'Undefined']

        client = dataikuapi.APINodeClient("http://136.252.73.83:12000", "faciesmapperpro")
        predicted_class_labels = []
        predicted_probabilities = []

        #base64_list = []
        for i in range(img_data.shape[0]):
            img_data_c = (img_data[i]).astype(np.uint8)  # convert to uint8
            image = Image.fromarray(img_data_c)
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            #base64_list.append(base64_str)

            payload = {'input': base64_str}
            prediction = client.predict_record("predict-facies", payload)
            prediction_result = prediction.get("result", {})
            prediction_value = prediction_result.get("prediction")
            if prediction_value is not None:
                print('prediction value: ', prediction_value)
                label = class_labels[int(prediction_value)-1]
                print('label: ', label)             
                predicted_class_labels.append(label)
                max_prob = max(prediction_result['probas'].values())
                predicted_probabilities.append(np.round(max_prob, 2) * 100)            
            else:
                # handle missing prediction value
                print('prediction_value from json is None')
                predicted_class_labels.append("unknown")
                predicted_probabilities.append(0)

        res_df['predicted_facies'] = predicted_class_labels
        res_df['probability'] = predicted_probabilities
        
        #with open('D:/Work/capstone_project/data/predictions/base64.txt', 'w') as file:
            #for base64_str in base64_list:
                #file.write(base64_str + '\n')

        return res_df
    
    def createNewZone(self, df):
        """
        Given well name, dataset name, variable name, unit and a pandas dataframe containing predicted facies values, create
        a new dataset with intervals defined by the predicted facies values.

        Parameters:
        wellName (str): the name of the well
        datasetName (str): the name of the dataset to create
        var (str): the name of the variable to create
        unit (str): the unit of measurement for the variable
        df (pandas.DataFrame): a pandas dataframe containing predicted facies values, with columns 'start_height' and
                            'predicted_facies'

        Returns:
        None
        """        
        tdep = self.tdep

        wellName = tdep.wellName()
        datasetName = wellName + '_Facies_Predicted'
        var = 'Zone Name'
        unit = ''

        # Check input types
        if not isinstance(wellName, str):
            raise TypeError("Well name must be a string.")
        if not isinstance(datasetName, str):
            raise TypeError("Dataset name must be a string.")
        if not isinstance(var, str):
            raise TypeError("Variable name must be a string.")
        if not isinstance(unit, str):
            raise TypeError("Unit must be a string.")
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input dataframe must be a pandas dataframe.")

        # Check well and dataset existence
        if not db.wellExists(wellName):
            raise ValueError("Well does not exist.")
        if db.datasetExists(wellName, datasetName):
            db.datasetDelete(wellName, datasetName)

        # Get reference and zone values
        reference, zones = self.get_reference_values(df)

        # Create dataset and save variable
        db.datasetCreate(wellName, datasetName, 'MD', 'Measured Depth', 'm', reference)
        db.datasetTypeChange(wellName, datasetName, 'interval')
        if db.variableSave(wellName, datasetName, var, 'Zone Name', unit, zones):
            print('The variable %s.%s.%s has been successfully created.'%(wellName, datasetName, var))
        else:
            print('ERROR: The variable %s.%s.%s cannot be created.'%(wellName, datasetName, var))
    

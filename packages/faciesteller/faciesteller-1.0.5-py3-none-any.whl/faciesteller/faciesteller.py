import pandas as pd
import numpy as np
import os
import getpass
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras.models import load_model

# Define class to wrap differnt functions for FaciesClassifier
class FaciesClassifier:
    def __init__(self, csv_path, img_path, well_name):
        self.csv_path = csv_path
        self.img_path = img_path
        self.well_name = well_name
        
        self.username = getpass.getuser()
        self.directory = os.path.join(f'C:\\Users\{self.username}\\AppData\\Roaming\\Schlumberger\\Techlog','predictions')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)        
     
     # load csv data and image data
    def load_data(self):
        
        # load fmi image and convert to array
        img_load = Image.open(self.img_path)
        img = img_load.convert('RGB')
        img_array = np.asarray(img)      
        
        # load csv file and process
        data_load = pd.read_csv(self.csv_path)
        df_csv = pd.DataFrame(data_load).iloc[1:].reset_index(drop=True)
        
        return df_csv, img_array   
        
     # fucntion to break fmi image into chunks, save into dataframe.   
    def imagetochunk(self, df_csv, img_array):  
        
        # check image, data rows
        if df_csv.shape[0] != img_array.shape[0]:
            raise ValueError("Files rows do not match.")
        
        # define chunk size
        chunk_size = 256
               
        # define output dataframe
        df_output = pd.DataFrame(columns=["chunk image", "start depth", "end depth"])     
         
        # Loop within image shape to generate chunks
        r,c = img_array.shape[0], img_array.shape[1]
                
        for i in range(0, r, chunk_size):
            for j in range(0, c, chunk_size):
                if i + chunk_size <= df_csv.index[-1] and j + chunk_size <= c:
                    chunk = img_array[i:i+chunk_size, j:chunk_size]
                    
                    if chunk.shape == (256, 256, 3):
                        row = {'chunk image': chunk, 'start depth': df_csv['TDEP'].iloc[i], 
                               'end depth': df_csv['TDEP'].iloc[i+chunk_size]}                       
                        df_output = df_output.append(row, ignore_index = True)
        return df_output
         
     # fucntion to predict with trained model   
    def predict(self, df_output):
        
        # Get well name
        well_name = self.well_name
        
        # Create a temp df to keep some column
        df_output_drop = df_output.drop('chunk image', axis=1)
        df_temp = df_output_drop.copy()
        
        # Get chunk array
        chunk_array = np.stack(df_output['chunk image'].values)
        
        # Reshape input
        chunk_array = chunk_array.reshape(chunk_array.shape[0], chunk_array.shape[1],
                                          chunk_array.shape[2], 3)
        
        # Load the pre-trained model
        model_path = f'C:\\Users\\{self.username}\\AppData\\Roaming\\Schlumberger\\Techlog\\model\\resnet50_acc97_val89_7wells.h5'
        model = load_model(model_path)

        # Use the model to make predictions on the image
        y_pred = model.predict(chunk_array)
        y_pred_class = np.argmax(y_pred, axis=1)
        y_pred_probs = np.max(y_pred, axis=1)
        y_pred_probs_rounded = np.round(y_pred_probs, 4) * 100
               
        # class map
        class_labels = {0:'Mature Paleosol', 1:'Siltstone',
             2:'Heterolithic Sandstone', 3:'Immature Paleosol',
             4:'Heterolithic Shale', 5:'Crossbedded Sandstone',
             6:'Massive Sand', 7:'Laminated Sand',
             8:'Undefined', 9:'Empty'}
             
        # convert to predict class to label
        y_pred_labels = [class_labels[c] for c in y_pred_class]
        
        # create empty list for predicated class and probablity
        predicted_class_labels: list[str] = []
        predicted_probabilities: list[float] = []
        
        # loop to write prediction inside list created
        for i, pred in enumerate(y_pred):  
            predicted_class_labels.append(y_pred_labels[i])
            predicted_probabilities.append(y_pred_probs_rounded[i])
            
        # add the predicted facies and probablity values to dataframe
        df_temp['preciated facies'] = predicted_class_labels
        df_temp['prediction probablity'] = predicted_probabilities
        
        df_predict = df_temp.copy()
                      
        # save df predict as csv
        df_predict.to_csv(os.path.join(self.directory,f'Prediction_Result_for_{well_name}.csv'))
        
        # genreate prediction image
        img_predict = self.recons_image(df_output, df_predict, well_name)
	
	    # get the full path of the predictions directory
        predictions_dir = os.path.abspath(self.directory)
	
	    # print the full path of the predictions directory
        print("Predictions directory:", predictions_dir)
        
        return img_predict
    
    def recons_image(self, df_output, df_predict, well_name):
        
        # make a copy of df_output
        df_recons_output = df_output.copy()
        df_recons_predict = df_predict.copy()
        
        # get reconstructed image
        img_path = self.img_path
        img = Image.open(img_path)
        recons_image = np.zeros(shape=(img.size[1], 256, 3), dtype=np.uint8)
        
        # create facies mask
        r = 0
        for i , row in df_recons_output.iterrows():
            recons_image[r:r+256, 0:256, :] = row['chunk image']
            r += 256
        
        # color map    
        color_dict = {
        'Mature Paleosol': (255, 0, 0),                     # Red
        'Siltstone': (0, 255, 0),                           # Green
        'Heterolithic Sandstone': (0, 0, 255),              # Blue
        'Immature Paleosol': (255, 255, 0),                 # Yellow
        'Heterolithic Shale': (255, 0, 255),                # Magenta
        'Crossbedded Sandstone': (0, 255, 255),             # Cyan
        'Massive Sand': (128, 0, 0),                        # Dark red
        'CrossBedded Sandstone': (0, 128, 0),               # Dark green
        'Laminated Sand': (128, 128, 128),                  # Grey
        'undefined': (128, 128, 0),                         # Oliver
        'Empty': (0,128,128)                                # Teal                              
        }
        
        # creat a masked array
        facies_mask = np.zeros(shape=(recons_image.shape[0], recons_image.shape[1], 4), dtype=np.uint8)
        facies_mask[:, :, 3] = 128
        
        # interate to update facies map with color
        for i, row in df_recons_predict.iterrows():
            facies = row['preciated facies']
            color = color_dict[facies]
            row_start = i * 256
            row_end = row_start + 256
            facies_mask[row_start:row_end, :, 0:3] = color
    
        # call base image and overlay iamge from array
        img_base = Image.fromarray(recons_image)
        img_overlay = Image.fromarray(facies_mask)
        img_base = img_base.convert("RGBA")
        img_overlay = img_overlay.convert("RGBA")
        
        # add facies name on image top        
        draw = ImageDraw.Draw(img_overlay)
        font = ImageFont.truetype("arial.ttf", 15, encoding="unic")
        for i, row in df_recons_predict.iterrows():
            facies = row['preciated facies']
            color = color_dict[facies]
            row_start = i * 256
            row_end = row_start + 256
            facies_mask[row_start:row_end, :, 0:3] = color
            text_width, text_height = draw.textsize(facies, font=font)
            x = (facies_mask.shape[1] - text_width) / 2
            y = i * 256 + (256 - text_height) / 2
            draw.text((x, y), facies, fill=(0, 0, 0, 255), font=font)
        
        # create composite image
        composite_image = Image.alpha_composite(img_base,img_overlay)      
        
        # save image
        img_predict = composite_image.save(os.path.join(self.directory, f'{well_name}.png'), format="PNG")
        return img_predict   
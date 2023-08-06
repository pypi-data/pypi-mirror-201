import tensorflow as tf
import pandas as pd
import numpy as np
import os
import folium
from PIL import Image
import sys

def main():

    if len(sys.argv) < 2:
        print("Error: No image path provided")
        folder_path = 'damagedetection\imgs'
    
    else:
         folder_path = sys.argv[1]

    loaded_model = tf.keras.models.load_model('damagedetection\model.h5')

    df_mapping = pd.DataFrame(columns=['longitude', 'latitude'])
    

    images = [] 
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        img = Image.open(path)
        img = img.resize((224, 224))
        images.append(img)
    images = np.array([np.array(img) for img in images])
    images = images / 255.0

    for filename in os.listdir(folder_path):
                if filename.endswith('.jpeg'):
                    lon, lat = filename.split('_')[0], filename.split('_')[1]
                    lat = lat.rstrip('.jpeg')
                    df_mapping = df_mapping.append({'longitude': lon, 'latitude': lat}, ignore_index=True)

    classes = ['damage','no_damage']
    predictions = loaded_model.predict(images)
    df_mapping['predicted'] = np.where(predictions>0.5, classes[1], classes[0])
    print(df_mapping)

    df_mapping['latitude'] = df_mapping['latitude'].astype(float)
    df_mapping['longitude'] = df_mapping['longitude'].astype(float)

    map_center = [df_mapping['latitude'].mean(), df_mapping['longitude'].mean()]
    map_obj = folium.Map(location=map_center, zoom_start=10)

    for index, row in df_mapping.iterrows():
        color = 'red' if row['predicted'] == 'damage' else 'green'
        
        marker = folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color=color))
        marker.add_to(map_obj)

    map_obj.show_in_browser()
    return

if __name__ == "__main__":
    main()


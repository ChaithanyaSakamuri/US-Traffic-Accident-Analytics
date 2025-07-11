import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Set up visualization style
plt.style.use('ggplot')
sns.set_palette("pastel")
# Check if file exists
file_path = 'US_Accidents_March23.csv'
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found in current directory.")
# Define columns we actually need to reduce memory usage
cols_to_use = [
    'Severity', 'Start_Time', 'End_Time', 'Start_Lat', 'Start_Lng',
    'Distance(mi)', 'City', 'State', 'Zipcode', 'Timezone',
    'Temperature(F)', 'Humidity(%)', 'Visibility(mi)', 
    'Wind_Speed(mph)', 'Precipitation(in)', 'Weather_Condition',
    'Amenity', 'Bump', 'Crossing', 'Junction', 'No_Exit', 
    'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Signal',
    'Sunrise_Sunset'
]
# Process data in chunks to handle large file
chunk_size = 100000
try:
    accident_chunks = pd.read_csv(file_path, chunksize=chunk_size, usecols=cols_to_use)
except Exception as e:
    print(f"Error reading file: {e}")
    exit()
# Initialize empty DataFrames to store aggregated results
time_patterns = pd.DataFrame()
weather_patterns = pd.DataFrame()
road_condition_patterns = pd.DataFrame()
location_patterns = pd.DataFrame()
for i, chunk in enumerate(accident_chunks):
    print(f"Processing chunk {i+1}...")
    try:
        # 1. Time of day analysis
        chunk['Start_Time'] = pd.to_datetime(chunk['Start_Time'])
        chunk['Hour'] = chunk['Start_Time'].dt.hour
        chunk['DayOfWeek'] = chunk['Start_Time'].dt.day_name()
        time_chunk = chunk.groupby(['Hour', 'DayOfWeek']).size().reset_index(name='Count')
        time_patterns = pd.concat([time_patterns, time_chunk])
        # 2. Weather condition analysis
        weather_chunk = chunk['Weather_Condition'].value_counts().reset_index()
        weather_chunk.columns = ['Weather_Condition', 'Count']
        weather_patterns = pd.concat([weather_patterns, weather_chunk])
        # 3. Road condition analysis
        road_cols = ['Amenity', 'Bump', 'Crossing', 'Junction', 
                    'No_Exit', 'Railway', 'Roundabout', 'Station', 
                    'Stop', 'Traffic_Signal']
        road_chunk = chunk[road_cols].sum().reset_index()
        road_chunk.columns = ['Condition', 'Count']
        road_condition_patterns = pd.concat([road_condition_patterns, road_chunk])
        # 4. Location analysis (sample for hotspots)
        location_chunk = chunk[['Start_Lat', 'Start_Lng', 'Severity']].sample(frac=0.1)
        location_patterns = pd.concat([location_patterns, location_chunk])
    except Exception as e:
        print(f"Error processing chunk {i+1}: {e}")
        continue
    if i == 10:  # Process first 11 chunks (1.1M rows) for demo purposes
        break
# Aggregate all the chunks
print("Aggregating results...")
# Visualization 1: Accidents by Hour of Day
plt.figure(figsize=(12, 6))
time_agg = time_patterns.groupby('Hour').sum().reset_index()
sns.lineplot(data=time_agg, x='Hour', y='Count')
plt.title('Accidents by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.show()
# Visualization 2: Accidents by Day of Week
plt.figure(figsize=(12, 6))
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
time_day_agg = time_patterns.groupby('DayOfWeek').sum().reindex(day_order).reset_index()
sns.barplot(data=time_day_agg, x='DayOfWeek', y='Count')
plt.title('Accidents by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.show()
# Visualization 3: Top Weather Conditions (top 10)
plt.figure(figsize=(12, 6))
weather_agg = weather_patterns.groupby('Weather_Condition').sum().nlargest(10, 'Count').reset_index()
sns.barplot(data=weather_agg, x='Count', y='Weather_Condition')
plt.title('Top 10 Weather Conditions During Accidents')
plt.xlabel('Number of Accidents')
plt.ylabel('Weather Condition')
plt.tight_layout()
plt.show()
# Visualization 4: Road Conditions
plt.figure(figsize=(12, 6))
road_agg = road_condition_patterns.groupby('Condition').sum().sort_values('Count', ascending=False).reset_index()
sns.barplot(data=road_agg, x='Count', y='Condition')
plt.title('Accidents by Road Condition')
plt.xlabel('Number of Accidents')
plt.ylabel('Road Feature')
plt.tight_layout()
plt.show()
# Visualization 5: Accident Hotspots (sampled)
plt.figure(figsize=(12, 8))
sns.scatterplot(data=location_patterns.sample(10000),
               x='Start_Lng', y='Start_Lat',
               hue='Severity', size='Severity',
               sizes=(10, 100), alpha=0.3)
plt.title('Accident Hotspots in US (Sample)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()
print("Analysis complete!")

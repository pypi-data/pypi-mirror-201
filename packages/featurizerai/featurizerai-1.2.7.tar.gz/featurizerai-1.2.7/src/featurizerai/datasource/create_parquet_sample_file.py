import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Sample dataset
data = [
    ("2023-03-30 09:00:00", "device_1", "Device One", "2023-03-30 08:59:00"),
    ("2023-03-30 09:15:00", "device_2", "Device Two", "2023-03-30 09:14:00"),
    ("2023-03-30 09:30:00", "device_3", "Device Three", "2023-03-30 09:29:00"),
]

# Define column names
column_names = ["timestamp", "device_id", "name", "created_at"]

# Create a DataFrame from the dataset
df = pd.DataFrame(data, columns=column_names)

# Convert the timestamp and created_at columns to datetime objects
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["created_at"] = pd.to_datetime(df["created_at"])

# Save the DataFrame as a Parquet file
table = pa.Table.from_pandas(df)
pq.write_table(table,'output.parquet', compression='snappy')

print("Parquet file created: output.parquet")

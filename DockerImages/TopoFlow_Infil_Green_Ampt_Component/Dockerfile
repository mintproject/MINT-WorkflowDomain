# Use an official Python runtime as a parent image
FROM python:2.7-slim
# Set the working directory to /app
WORKDIR /app
# Copy the topoflow directory contents into the container at /app
ADD ./topoflow /app
# Install topoflow and dependencies, topoflow requires an older version of NumPy.
#Also make the folder for model output
RUN pip install --editable ./
RUN pip install -U numpy==1.11.0
# Make directory for input and output
RUN mkdir -p /root/TF_Output/Treynor/
RUN mkdir /app/data
# Run the model when the container launches
CMD ls /app/data & python -m topoflow --cfg_prefix="June_20_67" --cfg_directory="/app/data/" --driver_comp_name=tf_infil_green_ampt

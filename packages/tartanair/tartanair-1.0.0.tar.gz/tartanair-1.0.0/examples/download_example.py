'''
Author: Yorai Shaoul
Date: 2023-02-03

Example script for downloading using the TartanAir dataset toolbox.
'''

# General imports.
import sys

# Local imports.
sys.path.append('..')
import tartanair as ta

# Create a TartanAir object.
tartanair_data_root = '/media/yoraish/overflow/data/tartanair-v2'
azure_token = "?sv=2021-10-04&st=2023-03-31T14%3A42%3A13Z&se=2023-07-01T14%3A42%3A00Z&sr=c&sp=rl&sig=IoZEVe1B5kQuZI5WzDSdGqiW%2BC9w8QKvmiK7QuaBhaA%3D"
 
ta.init(tartanair_data_root, azure_token)

# Download a trajectory.
env = [
"AbandonedCableExposure",
"ArchVizTinyHouseDayExposure",
"DesertGasStationExposure",
"HQWesternSaloonExposure",
"JapaneseCityExposure",
"ModularNeighborhoodIntExt",
"OldScandinaviaExposure"
]

# ta.download(env = env, difficulty = ['easy', 'hard'], trajectory_id = ["P001"],  modality = ['image', 'depth'],  camera_name = ['lcam_front', 'lcam_right', 'lcam_back', 'lcam_left', 'lcam_top', 'lcam_bottom'])

# Can also download via a yaml config file.
ta.download(config = 'download_config.yaml')

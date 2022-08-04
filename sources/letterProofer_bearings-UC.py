#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Bearings, UC
#     Version: 0.002
#
#     Still working on this. Needs to be optimized and restructured.
#     Extra page is drawn—need to figure this out when I have more time
#     
#
#     07/29/2022
#

# --------------------------------------
# -*- Imports -*- # 

import os
import time
import string
import numpy
import json
import tempfile
from datetime import date
from glob import glob
from os import listdir
from os.path import join, isfile
from pathlib import Path
from operator import itemgetter, attrgetter, methodcaller
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from drawBot import fill, stroke, rect, font, text, openTypeFeatures, height, newPage, textBox
from drawBot import installFont, pages, pageCount, saveImage
from fontTools.ttLib.ttFont import TTFont
from itertools import islice

# --------------------------------------
# -*- Set paths to directories -*- # 

font_folder = "/Users/smokh/S3P0/000-999/400-499 Creative/402 Type Design/02 Oldb/402.02.03 Fonts/2022-08-03"
proof_folder = "/Users/smokh/S3P0/000-999/400-499 Creative/402 Type Design/03 Leitmotiv/402.03.06 Proofs"

# --------------------------------------
# -*- Date & Time -*- # 

today = date.today()
now = time.localtime()
current_date = today.strftime ("%d/%m/%y")
current_year = today.strftime("%Y")
current_time = time.strftime("%H:%M", now)

# --------------------------------------
# -*- Settings -*- # 

# Set your information
designer_name = "Sepehr Mokhtarzadeh"
typeface_name = "Leitmotif"

# Set caption font
caption_font = "AndaleMono"
caption_size = 7
caption_color = 0

# --------------------------------------
# -*- Type Sizes -*- # 

# Set type scale
font_size_XXXL = 120
font_size_XXL = 96
font_size_XL = 80
font_size_L = 50
font_size_M = 24
font_size_S = 16
font_size_XS = 12
font_size_XXS = 9

# --------------------------------------
# -*- Text Strings -*- # 

textStrings = [ 
    
    [ "twelve_column", font_size_XS, "Side bearings - Capitals", "HAAAH\nHABAH\nHACAH\nHADAH\nHAEAH\nHAFAH\nHAGAH\nHAHAH\nHAIAH\nHAJAH\nHAKAH\nHALAH\nHAMAH\nHANAH\nHAOAH\nHAPAH\nHAQAH\nHARAH\nHASAH\nHATAH\nHAUAH\nHAVAH\nHAWAH\nHAXAH\nHAYAH\nHAZAH\nHBABH\nHBBBH\nHBCBH\nHBDBH\nHBEBH\nHBFBH\nHBGBH\nHBHBH\nHBIBH\nHBJBH\nHBKBH\nHBLBH\nHBMBH\nHBNBH\nHBOBH\nHBPBH\nHBQBH\nHBRBH\nHBSBH\nHBTBH\nHBUBH\nHBVBH\nHBWBH\nHBXBH\nHBYBH\nHBZBH\nHCACH\nHCBCH\nHCCCH\nHCDCH\nHCECH\nHCFCH\nHCGCH\nHCHCH\nHCICH\nHCJCH\nHCKCH\nHCLCH\nHCMCH\nHCNCH\nHCOCH\nHCPCH\nHCQCH\nHCRCH\nHCSCH\nHCTCH\nHCUCH\nHCVCH\nHCWCH\nHCXCH\nHCYCH\nHCZCH\nHDADH\nHDBDH\nHDCDH\nHDDDH\nHDEDH\nHDFDH\nHDGDH\nHDHDH\nHDIDH\nHDJDH\nHDKDH\nHDLDH\nHDMDH\nHDNDH\nHDODH\nHDPDH\nHDQDH\nHDRDH\nHDSDH\nHDTDH\nHDUDH\nHDVDH\nHDWDH\nHDXDH\nHDYDH\nHDZDH\nHEAEH\nHEBEH\nHECEH\nHEDEH\nHEEEH\nHEFEH\nHEGEH\nHEHEH\nHEIEH\nHEJEH\nHEKEH\nHELEH\nHEMEH\nHENEH\nHEOEH\nHEPEH\nHEQEH\nHEREH\nHESEH\nHETEH\nHEUEH\nHEVEH\nHEWEH\nHEXEH\nHEYEH\nHEZEH\nHFAFH\nHFBFH\nHFCFH\nHFDFH\nHFEFH\nHFFFH\nHFGFH\nHFHFH\nHFIFH\nHFJFH\nHFKFH\nHFLFH\nHFMFH\nHFNFH\nHFOFH\nHFPFH\nHFQFH\nHFRFH\nHFSFH\nHFTFH\nHFUFH\nHFVFH\nHFWFH\nHFXFH\nHFYFH\nHFZFH\nHGAGH\nHGBGH\nHGCGH\nHGDGH\nHGEGH\nHGFGH\nHGGGH\nHGHGH\nHGIGH\nHGJGH\nHGKGH\nHGLGH\nHGMGH\nHGNGH\nHGOGH\nHGPGH\nHGQGH\nHGRGH\nHGSGH\nHGTGH\nHGUGH\nHGVGH\nHGWGH\nHGXGH\nHGYGH\nHGZGH\nHHAHH\nHHBHH\nHHCHH\nHHDHH\nHHEHH\nHHFHH\nHHGHH\nHHHHH\nHHIHH\nHHJHH\nHHKHH\nHHLHH\nHHMHH\nHHNHH\nHHOHH\nHHPHH\nHHQHH\nHHRHH\nHHSHH\nHHTHH\nHHUHH\nHHVHH\nHHWHH\nHHXHH\nHHYHH\nHHZHH\nHIAIH\nHIBIH\nHICIH\nHIDIH\nHIEIH\nHIFIH\nHIGIH\nHIHIH\nHIIIH\nHIJIH\nHIKIH\nHILIH\nHIMIH\nHINIH\nHIOIH\nHIPIH\nHIQIH\nHIRIH\nHISIH\nHITIH\nHIUIH\nHIVIH\nHIWIH\nHIXIH\nHIYIH\nHIZIH\nHJAJH\nHJBJH\nHJCJH\nHJDJH\nHJEJH\nHJFJH\nHJGJH\nHJHJH\nHJIJH\nHJJJH\nHJKJH\nHJLJH\nHJMJH\nHJNJH\nHJOJH\nHJPJH\nHJQJH\nHJRJH\nHJSJH\nHJTJH\nHJUJH\nHJVJH\nHJWJH\nHJXJH\nHJYJH\nHJZJH\nHKAKH\nHKBKH\nHKCKH\nHKDKH\nHKEKH\nHKFKH\nHKGKH\nHKHKH\nHKIKH\nHKJKH\nHKKKH\nHKLKH\nHKMKH\nHKNKH\nHKOKH\nHKPKH\nHKQKH\nHKRKH\nHKSKH\nHKTKH\nHKUKH\nHKVKH\nHKWKH\nHKXKH\nHKYKH\nHKZKH\nHLALH\nHLBLH\nHLCLH\nHLDLH\nHLELH\nHLFLH\nHLGLH\nHLHLH\nHLILH\nHLJLH\nHLKLH\nHLLLH\nHLMLH\nHLNLH\nHLOLH\nHLPLH\nHLQLH\nHLRLH\nHLSLH\nHLTLH\nHLULH\nHLVLH\nHLWLH\nHLXLH\nHLYLH\nHLZLH\nHMAMH\nHMBMH\nHMCMH\nHMDMH\nHMEMH\nHMFMH\nHMGMH\nHMHMH\nHMIMH\nHMJMH\nHMKMH\nHMLMH\nHMMMH\nHMNMH\nHMOMH\nHMPMH\nHMQMH\nHMRMH\nHMSMH\nHMTMH\nHMUMH\nHMVMH\nHMWMH\nHMXMH\nHMYMH\nHMZMH\nHNANH\nHNBNH\nHNCNH\nHNDNH\nHNENH\nHNFNH\nHNGNH\nHNHNH\nHNINH\nHNJNH\nHNKNH\nHNLNH\nHNMNH\nHNNNH\nHNONH\nHNPNH\nHNQNH\nHNRNH\nHNSNH\nHNTNH\nHNUNH\nHNVNH\nHNWNH\nHNXNH\nHNYNH\nHNZNH\nHOAOH\nHOBOH\nHOCOH\nHODOH\nHOEOH\nHOFOH\nHOGOH\nHOHOH\nHOIOH\nHOJOH\nHOKOH\nHOLOH\nHOMOH\nHONOH\nHOOOH\nHOPOH\nHOQOH\nHOROH\nHOSOH\nHOTOH\nHOUOH\nHOVOH\nHOWOH\nHOXOH\nHOYOH\nHOZOH\nHPAPH\nHPBPH\nHPCPH\nHPDPH\nHPEPH\nHPFPH\nHPGPH\nHPHPH\nHPIPH\nHPJPH\nHPKPH\nHPLPH\nHPMPH\nHPNPH\nHPOPH\nHPPPH\nHPQPH\nHPRPH\nHPSPH\nHPTPH\nHPUPH\nHPVPH\nHPWPH\nHPXPH\nHPYPH\nHPZPH\nHQAQH\nHQBQH\nHQCQH\nHQDQH\nHQEQH\nHQFQH\nHQGQH\nHQHQH\nHQIQH\nHQJQH\nHQKQH\nHQLQH\nHQMQH\nHQNQH\nHQOQH\nHQPQH\nHQQQH\nHQRQH\nHQSQH\nHQTQH\nHQUQH\nHQVQH\nHQWQH\nHQXQH\nHQYQH\nHQZQH\nHRARH\nHRBRH\nHRCRH\nHRDRH\nHRERH\nHRFRH\nHRGRH\nHRHRH\nHRIRH\nHRJRH\nHRKRH\nHRLRH\nHRMRH\nHRNRH\nHRORH\nHRPRH\nHRQRH\nHRRRH\nHRSRH\nHRTRH\nHRURH\nHRVRH\nHRWRH\nHRXRH\nHRYRH\nHRZRH\nHSASH\nHSBSH\nHSCSH\nHSDSH\nHSESH\nHSFSH\nHSGSH\nHSHSH\nHSISH\nHSJSH\nHSKSH\nHSLSH\nHSMSH\nHSNSH\nHSOSH\nHSPSH\nHSQSH\nHSRSH\nHSSSH\nHSTSH\nHSUSH\nHSVSH\nHSWSH\nHSXSH\nHSYSH\nHSZSH\nHTATH\nHTBTH\nHTCTH\nHTDTH\nHTETH\nHTFTH\nHTGTH\nHTHTH\nHTITH\nHTJTH\nHTKTH\nHTLTH\nHTMTH\nHTNTH\nHTOTH\nHTPTH\nHTQTH\nHTRTH\nHTSTH\nHTTTH\nHTUTH\nHTVTH\nHTWTH\nHTXTH\nHTYTH\nHTZTH\nHUAUH\nHUBUH\nHUCUH\nHUDUH\nHUEUH\nHUFUH\nHUGUH\nHUHUH\nHUIUH\nHUJUH\nHUKUH\nHULUH\nHUMUH\nHUNUH\nHUOUH\nHUPUH\nHUQUH\nHURUH\nHUSUH\nHUTUH\nHUUUH\nHUVUH\nHUWUH\nHUXUH\nHUYUH\nHUZUH\nHVAVH\nHVBVH\nHVCVH\nHVDVH\nHVEVH\nHVFVH\nHVGVH\nHVHVH\nHVIVH\nHVJVH\nHVKVH\nHVLVH\nHVMVH\nHVNVH\nHVOVH\nHVPVH\nHVQVH\nHVRVH\nHVSVH\nHVTVH\nHVUVH\nHVVVH\nHVWVH\nHVXVH\nHVYVH\nHVZVH\nHWAWH\nHWBWH\nHWCWH\nHWDWH\nHWEWH\nHWFWH\nHWGWH\nHWHWH\nHWIWH\nHWJWH\nHWKWH\nHWLWH\nHWMWH\nHWNWH\nHWOWH\nHWPWH\nHWQWH\nHWRWH\nHWSWH\nHWTWH\nHWUWH\nHWVWH\nHWWWH\nHWXWH\nHWYWH\nHWZWH\nHXAXH\nHXBXH\nHXCXH\nHXDXH\nHXEXH\nHXFXH\nHXGXH\nHXHXH\nHXIXH\nHXJXH\nHXKXH\nHXLXH\nHXMXH\nHXNXH\nHXOXH\nHXPXH\nHXQXH\nHXRXH\nHXSXH\nHXTXH\nHXUXH\nHXVXH\nHXWXH\nHXXXH\nHXYXH\nHXZXH\nHYAYH\nHYBYH\nHYCYH\nHYDYH\nHYEYH\nHYFYH\nHYGYH\nHYHYH\nHYIYH\nHYJYH\nHYKYH\nHYLYH\nHYMYH\nHYNYH\nHYOYH\nHYPYH\nHYQYH\nHYRYH\nHYSYH\nHYTYH\nHYUYH\nHYVYH\nHYWYH\nHYXYH\nHYYYH\nHYZYH\nHZAZH\nHZBZH\nHZCZH\nHZDZH\nHZEZH\nHZFZH\nHZGZH\nHZHZH\nHZIZH\nHZJZH\nHZKZH\nHZLZH\nHZMZH\nHZNZH\nHZOZH\nHZPZH\nHZQZH\nHZRZH\nHZSZH\nHZTZH\nHZUZH\nHZVZH\nHZWZH\nHZXZH\nHZYZH\nHZZZH\nOAAAO\nOABAO\nOACAO\nOADAO\nOAEAO\nOAFAO\nOAGAO\nOAHAO\nOAIAO\nOAJAO\nOAKAO\nOALAO\nOAMAO\nOANAO\nOAOAO\nOAPAO\nOAQAO\nOARAO\nOASAO\nOATAO\nOAUAO\nOAVAO\nOAWAO\nOAXAO\nOAYAO\nOAZAO\nOBABO\nOBBBO\nOBCBO\nOBDBO\nOBEBO\nOBFBO\nOBGBO\nOBHBO\nOBIBO\nOBJBO\nOBKBO\nOBLBO\nOBMBO\nOBNBO\nOBOBO\nOBPBO\nOBQBO\nOBRBO\nOBSBO\nOBTBO\nOBUBO\nOBVBO\nOBWBO\nOBXBO\nOBYBO\nOBZBO\nOCACO\nOCBCO\nOCCCO\nOCDCO\nOCECO\nOCFCO\nOCGCO\nOCHCO\nOCICO\nOCJCO\nOCKCO\nOCLCO\nOCMCO\nOCNCO\nOCOCO\nOCPCO\nOCQCO\nOCRCO\nOCSCO\nOCTCO\nOCUCO\nOCVCO\nOCWCO\nOCXCO\nOCYCO\nOCZCO\nODADO\nODBDO\nODCDO\nODDDO\nODEDO\nODFDO\nODGDO\nODHDO\nODIDO\nODJDO\nODKDO\nODLDO\nODMDO\nODNDO\nODODO\nODPDO\nODQDO\nODRDO\nODSDO\nODTDO\nODUDO\nODVDO\nODWDO\nODXDO\nODYDO\nODZDO\nOEAEO\nOEBEO\nOECEO\nOEDEO\nOEEEO\nOEFEO\nOEGEO\nOEHEO\nOEIEO\nOEJEO\nOEKEO\nOELEO\nOEMEO\nOENEO\nOEOEO\nOEPEO\nOEQEO\nOEREO\nOESEO\nOETEO\nOEUEO\nOEVEO\nOEWEO\nOEXEO\nOEYEO\nOEZEO\nOFAFO\nOFBFO\nOFCFO\nOFDFO\nOFEFO\nOFFFO\nOFGFO\nOFHFO\nOFIFO\nOFJFO\nOFKFO\nOFLFO\nOFMFO\nOFNFO\nOFOFO\nOFPFO\nOFQFO\nOFRFO\nOFSFO\nOFTFO\nOFUFO\nOFVFO\nOFWFO\nOFXFO\nOFYFO\nOFZFO\nOGAGO\nOGBGO\nOGCGO\nOGDGO\nOGEGO\nOGFGO\nOGGGO\nOGHGO\nOGIGO\nOGJGO\nOGKGO\nOGLGO\nOGMGO\nOGNGO\nOGOGO\nOGPGO\nOGQGO\nOGRGO\nOGSGO\nOGTGO\nOGUGO\nOGVGO\nOGWGO\nOGXGO\nOGYGO\nOGZGO\nOHAHO\nOHBHO\nOHCHO\nOHDHO\nOHEHO\nOHFHO\nOHGHO\nOHHHO\nOHIHO\nOHJHO\nOHKHO\nOHLHO\nOHMHO\nOHNHO\nOHOHO\nOHPHO\nOHQHO\nOHRHO\nOHSHO\nOHTHO\nOHUHO\nOHVHO\nOHWHO\nOHXHO\nOHYHO\nOHZHO\nOIAIO\nOIBIO\nOICIO\nOIDIO\nOIEIO\nOIFIO\nOIGIO\nOIHIO\nOIIIO\nOIJIO\nOIKIO\nOILIO\nOIMIO\nOINIO\nOIOIO\nOIPIO\nOIQIO\nOIRIO\nOISIO\nOITIO\nOIUIO\nOIVIO\nOIWIO\nOIXIO\nOIYIO\nOIZIO\nOJAJO\nOJBJO\nOJCJO\nOJDJO\nOJEJO\nOJFJO\nOJGJO\nOJHJO\nOJIJO\nOJJJO\nOJKJO\nOJLJO\nOJMJO\nOJNJO\nOJOJO\nOJPJO\nOJQJO\nOJRJO\nOJSJO\nOJTJO\nOJUJO\nOJVJO\nOJWJO\nOJXJO\nOJYJO\nOJZJO\nOKAKO\nOKBKO\nOKCKO\nOKDKO\nOKEKO\nOKFKO\nOKGKO\nOKHKO\nOKIKO\nOKJKO\nOKKKO\nOKLKO\nOKMKO\nOKNKO\nOKOKO\nOKPKO\nOKQKO\nOKRKO\nOKSKO\nOKTKO\nOKUKO\nOKVKO\nOKWKO\nOKXKO\nOKYKO\nOKZKO\nOLALO\nOLBLO\nOLCLO\nOLDLO\nOLELO\nOLFLO\nOLGLO\nOLHLO\nOLILO\nOLJLO\nOLKLO\nOLLLO\nOLMLO\nOLNLO\nOLOLO\nOLPLO\nOLQLO\nOLRLO\nOLSLO\nOLTLO\nOLULO\nOLVLO\nOLWLO\nOLXLO\nOLYLO\nOLZLO\nOMAMO\nOMBMO\nOMCMO\nOMDMO\nOMEMO\nOMFMO\nOMGMO\nOMHMO\nOMIMO\nOMJMO\nOMKMO\nOMLMO\nOMMMO\nOMNMO\nOMOMO\nOMPMO\nOMQMO\nOMRMO\nOMSMO\nOMTMO\nOMUMO\nOMVMO\nOMWMO\nOMXMO\nOMYMO\nOMZMO\nONANO\nONBNO\nONCNO\nONDNO\nONENO\nONFNO\nONGNO\nONHNO\nONINO\nONJNO\nONKNO\nONLNO\nONMNO\nONNNO\nONONO\nONPNO\nONQNO\nONRNO\nONSNO\nONTNO\nONUNO\nONVNO\nONWNO\nONXNO\nONYNO\nONZNO\nOOAOO\nOOBOO\nOOCOO\nOODOO\nOOEOO\nOOFOO\nOOGOO\nOOHOO\nOOIOO\nOOJOO\nOOKOO\nOOLOO\nOOMOO\nOONOO\nOOOOO\nOOPOO\nOOQOO\nOOROO\nOOSOO\nOOTOO\nOOUOO\nOOVOO\nOOWOO\nOOXOO\nOOYOO\nOOZOO\nOPAPO\nOPBPO\nOPCPO\nOPDPO\nOPEPO\nOPFPO\nOPGPO\nOPHPO\nOPIPO\nOPJPO\nOPKPO\nOPLPO\nOPMPO\nOPNPO\nOPOPO\nOPPPO\nOPQPO\nOPRPO\nOPSPO\nOPTPO\nOPUPO\nOPVPO\nOPWPO\nOPXPO\nOPYPO\nOPZPO\nOQAQO\nOQBQO\nOQCQO\nOQDQO\nOQEQO\nOQFQO\nOQGQO\nOQHQO\nOQIQO\nOQJQO\nOQKQO\nOQLQO\nOQMQO\nOQNQO\nOQOQO\nOQPQO\nOQQQO\nOQRQO\nOQSQO\nOQTQO\nOQUQO\nOQVQO\nOQWQO\nOQXQO\nOQYQO\nOQZQO\nORARO\nORBRO\nORCRO\nORDRO\nORERO\nORFRO\nORGRO\nORHRO\nORIRO\nORJRO\nORKRO\nORLRO\nORMRO\nORNRO\nORORO\nORPRO\nORQRO\nORRRO\nORSRO\nORTRO\nORURO\nORVRO\nORWRO\nORXRO\nORYRO\nORZRO\nOSASO\nOSBSO\nOSCSO\nOSDSO\nOSESO\nOSFSO\nOSGSO\nOSHSO\nOSISO\nOSJSO\nOSKSO\nOSLSO\nOSMSO\nOSNSO\nOSOSO\nOSPSO\nOSQSO\nOSRSO\nOSSSO\nOSTSO\nOSUSO\nOSVSO\nOSWSO\nOSXSO\nOSYSO\nOSZSO\nOTATO\nOTBTO\nOTCTO\nOTDTO\nOTETO\nOTFTO\nOTGTO\nOTHTO\nOTITO\nOTJTO\nOTKTO\nOTLTO\nOTMTO\nOTNTO\nOTOTO\nOTPTO\nOTQTO\nOTRTO\nOTSTO\nOTTTO\nOTUTO\nOTVTO\nOTWTO\nOTXTO\nOTYTO\nOTZTO\nOUAUO\nOUBUO\nOUCUO\nOUDUO\nOUEUO\nOUFUO\nOUGUO\nOUHUO\nOUIUO\nOUJUO\nOUKUO\nOULUO\nOUMUO\nOUNUO\nOUOUO\nOUPUO\nOUQUO\nOURUO\nOUSUO\nOUTUO\nOUUUO\nOUVUO\nOUWUO\nOUXUO\nOUYUO\nOUZUO\nOVAVO\nOVBVO\nOVCVO\nOVDVO\nOVEVO\nOVFVO\nOVGVO\nOVHVO\nOVIVO\nOVJVO\nOVKVO\nOVLVO\nOVMVO\nOVNVO\nOVOVO\nOVPVO\nOVQVO\nOVRVO\nOVSVO\nOVTVO\nOVUVO\nOVVVO\nOVWVO\nOVXVO\nOVYVO\nOVZVO\nOWAWO\nOWBWO\nOWCWO\nOWDWO\nOWEWO\nOWFWO\nOWGWO\nOWHWO\nOWIWO\nOWJWO\nOWKWO\nOWLWO\nOWMWO\nOWNWO\nOWOWO\nOWPWO\nOWQWO\nOWRWO\nOWSWO\nOWTWO\nOWUWO\nOWVWO\nOWWWO\nOWXWO\nOWYWO\nOWZWO\nOXAXO\nOXBXO\nOXCXO\nOXDXO\nOXEXO\nOXFXO\nOXGXO\nOXHXO\nOXIXO\nOXJXO\nOXKXO\nOXLXO\nOXMXO\nOXNXO\nOXOXO\nOXPXO\nOXQXO\nOXRXO\nOXSXO\nOXTXO\nOXUXO\nOXVXO\nOXWXO\nOXXXO\nOXYXO\nOXZXO\nOYAYO\nOYBYO\nOYCYO\nOYDYO\nOYEYO\nOYFYO\nOYGYO\nOYHYO\nOYIYO\nOYJYO\nOYKYO\nOYLYO\nOYMYO\nOYNYO\nOYOYO\nOYPYO\nOYQYO\nOYRYO\nOYSYO\nOYTYO\nOYUYO\nOYVYO\nOYWYO\nOYXYO\nOYYYO\nOYZYO\nOZAZO\nOZBZO\nOZCZO\nOZDZO\nOZEZO\nOZFZO\nOZGZO\nOZHZO\nOZIZO\nOZJZO\nOZKZO\nOZLZO\nOZMZO\nOZNZO\nOZOZO\nOZPZO\nOZQZO\nOZRZO\nOZSZO\nOZTZO\nOZUZO\nOZVZO\nOZWZO\nOZXZO\nOZYZO\nOZZZO"],

    ]
    
# --------------------------------------
# -*- Page Info -*- # 

show_document_grid = False
show_grid = False
show_labels = False

# Metrics
mmmm = 2.834627813
inch = 72

# Margins
margin = (1/2) * inch
number_of_columns = 13
number_of_rows = 49

# Dimensions
page_dimensions = 'LetterLandscape'
newPage(page_dimensions)

# Document Grid
subdivisions = 8
grid_unit = inch / subdivisions

page_width = width() / inch
page_height = height() / inch

number_of_x_gridlines = float(grid_unit * page_width)
number_of_y_gridlines = float(grid_unit * page_height)

# Document Margins
margin_left_right = width() - (margin * 2)
margin_top_bottom = height() - (margin * 2)

col_width = margin_left_right / number_of_columns
row_height = margin_top_bottom / number_of_rows

# Coordinate helpers
edge_left = 0
edge_right = margin_left_right
edge_top = margin_top_bottom
edge_bottom = 0

# --------------------------------------
# -*- Functions, Style  -*- # 

def meta_style():
    fill(caption_color)
    font(caption_font, caption_size)
    
def type_style():
    fallbackFont("AdobeBlank")
    font(postscriptFontName)

# --------------------------------------
# -*- Functions, Components -*- # 

def drawHeaderFooter():
    with savedState():
        translate(margin,margin)
        with savedState():
            meta_style()
        
            translate(0, fontCapHeight() * 2)
        
            # Definitions
            leftHeader = ' '.join([typeface_name, "©", current_year, "copyright by designed by", designer_name])
            rightHeader = ' '.join(["output made on:", current_date, ",", current_time])
            rightFooter = ' '.join([postscriptFontName, font_version])
        
            # Draw
            text(leftHeader, (edge_left, edge_top + 5), align="left" )
            text(rightHeader, (edge_right, edge_top + 5), align="right")
        
            # Draw line below Header
            with savedState():
                stroke(0)
                strokeWidth(0.25)
                line((edge_left, y_cord["48"] + 5), (edge_right, y_cord["48"] + 5))
        
            # Draw Footer
            translate(0, -(fontCapHeight() * 3.25))
            text(rightFooter, (edge_left, edge_bottom - 10), align="left")
            
# --------------------------------------
# -*- Functions, Page Layouts -*- # 

def drawTwelveColumnLayout():
    global y_pos_1
    global y_pos_2


    # Set type for proof, single type size
    if font_size == font_size_XS:
        type_style()
        fontSize(font_size)
        line_height = font_size * 1.3
        translate(0, -fontCapHeight())

    
        # Page 1 columns
        textBox(proof_set[:227], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[228:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[462:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[690:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[918:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1146:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1374:], (x_cord["6"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1602:], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1830:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2058:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2286:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2514:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2742:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
    
        # Add new page if textString is too long
        if len(proof_set) >= 2742:
        
            newPage(page_dimensions)
            grid()
            drawHeaderFooter()
            translate(margin,margin)
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.3
            translate(0, -fontCapHeight())
        
            # Page 2 columns
            textBox(proof_set[2970:], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3198:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3426:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3654:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3882:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4110:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4338:], (x_cord["6"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4566:], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4794:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5022:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5250:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5478:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5706:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        
            # Add new page if textString is too long
            if len(proof_set) >= 5928:
            
                newPage(page_dimensions)
                grid()
                drawHeaderFooter()
                translate(margin,margin)
                type_style()
                fontSize(font_size)
                line_height = font_size * 1.3
                translate(0, -fontCapHeight())
        
                # Page 2 columns
            
                textBox(proof_set[5934:], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6162:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6390:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6618:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6846:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7074:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7302:], (x_cord["6"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7530:], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7758:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7986:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[8214:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[8442:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[8670:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")

# Page template       
def drawNewPage():
    grid()
    drawHeaderFooter()

    translate(margin,margin)
    if layout == "one_column":
        drawOneColumnLayout()
    elif layout == "two_column":
        drawTwoColumnLayout()
    elif layout == "asymmetric_two_column":
        drawAsymmetricTwoColumnLayout()
    elif layout == "three_column":
        drawThreeColumnLayout()
    elif layout == "four_column":
        drawOneColumnLayout()
    elif layout == "twelve_column":
        drawTwelveColumnLayout()
            
# Defines on/off button for grid and labels
def grid():
    if show_grid:
        drawGrid()     
    if show_labels:
        drawGridLabels()
# --------------------------------------
# -*- Coordinates -*- # 

x_cord_name_list = list()
x_cord_num_list = list()

y_cord_name_list = list()
y_cord_num_list = list()

x_cord_dict = dict(zip(x_cord_name_list, x_cord_num_list))
zip_x_cords = zip(x_cord_name_list, x_cord_num_list)

y_cord_dict = dict(zip(y_cord_name_list, y_cord_num_list))
zip_y_cords = zip(y_cord_name_list,  y_cord_num_list)

with savedState():
    for x in range(number_of_columns + 1):
        
        col_name = str(x)
        x_cord = str(x * col_width)
        
        x_cord_name_list.append(col_name)
        x_cord_num_list.append(float(x_cord))
        
        for y in range(number_of_rows + 1):
            
            row_name = str(y)
            y_cord = str(y * row_height)
            
            y_cord_name_list.append(row_name)
            y_cord_num_list.append(float(y_cord))

# Create dictionary from zip object
x_cord = dict(zip_x_cords)
y_cord = dict(zip_y_cords)

# --------------------------------------
# -*- Grid -*- # 

# Draws grid
def drawGrid():
    with savedState():
        translate(margin, margin)
        for x in numpy.arange(number_of_columns):
            for y in range(number_of_rows):
                with savedState():
                    fill(None)
                    stroke(1, 0, 0, 0.1)
                    strokeWidth(0.25)
                    rect(x * col_width, y * row_height, col_width, row_height)

# Draws grid labels        
def drawGridLabels():
    with savedState():
        translate(margin, margin)
    
        fill(1, 0, 0, 0.5)
        font(caption_font, 6)
    
        for x in range(number_of_columns + 1):
            text(str(x), (x_cord[str(x)], margin / -2), align="center")
        
        translate(0, (-fontCapHeight() / 2))
        for y in range(number_of_rows + 1):
            text(str(y), (margin / -2, y_cord[str(y)]), align="center")

# --------------------------------------

# def collectFilesPaths(folder, extension=''):
#     """hidden files (starting with a dot) are filtered out"""
#     paths = []
#     for eachFileName in [nn for nn in listdir(folder) if not nn.startswith('.')]:
#         eachPath = join(folder, eachFileName)
#         if isfile(eachPath) and eachPath.endswith(extension):
#             paths.append(eachPath)
#             print(paths)
#         else:
#             print(paths)
#         return paths

                    
# def getFont(folder, extension=''):
    
#     fonts = []
#     for eachFont in folder:
#         eachPath = join(folder, eachFont)
#         if isfile(eachPath) and eachPath.endswith(extension):
#             f = OpenFont(eachFontPath, showInterface = False)
#             fonts.append(f)
#             print(f)
        
# --------------------------------------
# -*- Instructions -*- # 

ufos = glob(os.path.join(font_folder, "*.ufo"))   
allFonts = ufos

if __name__ == '__main__':
    
    # Iterate over all fonts
    for eachFontPath in allFonts:
        
        # Definitions
        f = OpenFont(eachFontPath, showInterface = False)
        f.testInstall
        postscriptFontName = '%s-%s' % (f.info.familyName, f.info.styleName)
        font_version = ''.join(str(f.info.versionMajor) + '.' + str(f.info.versionMinor))
        print(font_version)
        print(postscriptFontName)
        
        # Draws pages
        for eachString in textStrings:
            
            # Definitions
            layout = eachString[0]
            section = eachString[2]
            proof_set = eachString[3]
            
            # Loop de loops
            if eachString[1] == font_size_XXXL:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XXL:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XL:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_L:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_M:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_S:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XS:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XXS:
                font_size = eachString[1]
                drawNewPage()

# --------------------------------------
# -*- Save -*- # 

# time_stamp = today.strftime ("%Y-%m-%d")
# path = Path(proof_folder + "/" + time_stamp)


# file_name = (str(path) + "/" + '-'.join(postscriptFontName.split()) + "_proof_" + '-'.join(proof_name.split()))
# file_version = 0


# if (os.path.exists(path)):
#     print("Folder Exists!")
#     while (os.path.exists(file_name + "_" + str(file_version) + ".pdf")):
#         print("File already exists, saved with a numerator")
#         file_version += 1
        
#     saveImage(file_name + "_" + str(file_version) + ".pdf")
#     print("File saved!")
# else:
#     print("Folder does not exist")
#     while (os.path.exists(file_name + "_" + str(file_version) + ".pdf")):
#         print("File already exists, saved with a numerator")
#         file_version += 1
#     path.mkdir(parents=True, exist_ok=True)
#     saveImage(file_name + "_" + str(file_version) + ".pdf")
 

    
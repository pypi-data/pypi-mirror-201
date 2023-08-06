#!/usr/bin/env python
# coding: utf-8
# Copyright (C) 2020 Miriam Cabero
# Edited by Man Leong Chan 2022
# this code references ligo.skymap

# import necessary libraries

from ligo.skymap import io
from ligo.skymap import io, distance as ls_distance
import numpy, tensorflow, os
from astropy.io import fits
from reproject import reproject_from_healpix
from scipy import interpolate

# Target header for reproject_from_healpix
# This will be used for reprojecting the skymaps from FITS file to a more manageable size
target_header = fits.Header.fromstring("""
NAXIS   =                    2
NAXIS1  =                  360
NAXIS2  =                  180
CTYPE1  = 'RA---CAR'
CRPIX1  =                180.5
CRVAL1  =                180.0
CDELT1  =                   -1
CUNIT1  = 'deg     '
CTYPE2  = 'DEC--CAR'
CRPIX2  =                 90.5
CRVAL2  =                  0.0
CDELT2  =                    1
CUNIT2  = 'deg     '
COORDSYS= 'icrs    '
""", sep='\n')


# these set the default model name and path to fetch the relevant model files

# added links for models and weights (15th Aug 2022)
# GWSkyNet_v1            : model in the original paper

# GWSkyNet_v2 performance: https://ldas-jobs.ligo.caltech.edu/~manleong.chan/test_output/2022-05-24-11-29-11/
# GWSkyNet_v2 model      : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-05-24-11-29-11/model.json
# GWSkyNet_v2 weight     : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-05-24-11-29-11/logs/best_weights.h5

# GWSkyNet_v3 performance: https://ldas-jobs.ligo.caltech.edu/~manleong.chan/test_output/raw_data/2022-07-04-08-19-30/Epoch_10-VL_0.1632-VA_0.9513-TL_0.1542-TA_0.9545/
# GWSkyNet_v3 model      : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-07-04-08-19-30/model.json
# GWSkyNet_v3 weight     : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-07-04-08-19-30/weights/Epoch_10-VL_0.1632-VA_0.9513-TL_0.1542-TA_0.9545.h5

# GWSkyNet_v4 performance: https://wiki.ligo.org/Bursts/EMFollow/GWSkyNet-MDC-Revised-Model
# GWSkyNet_v4 model      : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/start_over/2022-11-07-15-11-52/model/model.json
# GWSkyNet_v4 weight     : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/start_over/2022-11-07-15-11-52/weights/Epoch_585-VL_0.0932-VA_0.9720-TL_0.0777-TA_0.9759.h5


model_names = ['GWSkyNet_v4'] #
model_path  = os.path.join(os.path.dirname(__file__), 'GWSkyNet_data', 'models')
rate_path   = os.path.join(os.path.dirname(__file__), 'GWSkyNet_data', 'rates')

model_name  = 'GWSkyNet_v4'  # the model that is actually used.

# when training the GWSkyNet model, a few normalization factors are derived from the corresponding training data set by
# taking the absolute maximum values of the corresponding values of the training samples.
# for example, the training norm "distance" is the maximum value of the posterior mean distances (Mpc) for all samples,
# and "skymap" is the maximum value from the sky location posteriors for all training samples.
# These factors will also be applied to testing data or real data to be consistent.

# These factors are saved in model/training_norms.txt

tnf                     = open(os.path.join(model_path, 'training_norms.txt'), 'r')
tnf_content             = tnf.readlines()
training_norms_keywords = tnf_content[0].split()
training_norms_values   = tnf_content[1:]
tnf.close()

model_index             = [i for i, s in enumerate(training_norms_values) if model_name in s][0]
training_norms          = training_norms_values[model_index].split()

# select the training norms based on the model selected because the training normalization factors are derived from
# different training sets.
training_norms          = {training_norms_keywords[i] : float(training_norms[i]) for i in range(1, len(training_norms))}

if not model_name in model_names:
    raise Exception('Requested GWSkyNet model does not exist: %s.'%(model_name))

def nan_invalid(data, invalid_value):
    """Turn invalid values into numpy.nan"""
    invalid_indices = numpy.where(data==invalid_value)
    for idx in invalid_indices:
        data[idx] = numpy.nan
    return data

def prepare_data(fits_file):
    """Pre-processing data from FITS file for GWSkyNet"""
    # read FITS file. GWSkyNet only works with FITS file generated using Bayestar
    # as GWSkyNet uses the distance information so "distsances" is set to be true.
    (prob, mu, sigma, norm), metadata = io.read_sky_map(fits_file,
                                        distances=True, nest=None)
    
    #verify the skymap is generated using ligo.skymap
    if not metadata['creator'] == 'BAYESTAR':
        raise Exception ('The input skymap is not generated using ligo.skymap. GWSkyNet is only able to work FITS file generated using ligo.skymap.')
    
    # get the mean distance, and the sigma
    dist_mean, std = metadata['distmean'], metadata['diststd']
    # the maximum distance in the distance volume image projection
    max_distance   = dist_mean + 2.5 * std
    # normalize the mean distance so that it is within 0 to 1
    dist_mean    = dist_mean / training_norms['distance']
    # get the network detectors
    network = metadata['instruments']
    # get the log bayester factors
    logbci = metadata['log_bci'] / training_norms['logbci']
    logbsn = metadata['log_bsn'] / training_norms['logbsn']
    
    # Convert detector network to multi-hot format
    dets = []
    for ifo in ['H1', 'L1', 'V1']:
        if ifo in network:
            dets.append(1)
        else:
            dets.append(0)
            
    img_data, norms = dict(), dict()
    with numpy.errstate(invalid='ignore'):
        img, mask = reproject_from_healpix((prob, 'ICRS'), target_header,
                                    nested=metadata['nest'], hdu_in=None,
                                    order='bilinear', field=0)
        img_data['skymap'] = img
    
    # this references ligo-skymap-plot-volume
    rot          = numpy.ascontiguousarray(ls_distance.principal_axes(prob, mu, sigma, nest = metadata['nest']))
    # the value is smaller than that used in ligo-skymap-plot-volume for shorter computation time
    dpi          = 150
    figure_width = 3.5
    imgwidth     = int(dpi * figure_width / 2)
    s            = numpy.linspace(-max_distance, max_distance, imgwidth)
    xx, yy       = numpy.meshgrid(s, s)
    
    for iface, (axis0, axis1) in enumerate(((1,0), (0,2), (1,2))):
        density = ls_distance.volume_render(xx.ravel(), yy.ravel(), max_distance,
                                            axis0, axis1, rot, metadata['nest'], prob, mu,
                                            sigma, norm).reshape(xx.shape)
        img_data['vol{}'.format(iface)] = density
        
    for column in img_data.keys():
        norms[column]    = numpy.max(abs(img_data[column]))
        img_data[column] /= norms[column]
        norms[column]    /= training_norms[column]
      
    # Stack volume images
    dist_columns = ['vol0', 'vol1', 'vol2']
    # img_data has shape (1, 131, 131, 1), we need to reshape to (1, 131, 131) for stacking
    stacked_volume = numpy.stack([numpy.reshape(img_data[column],
                                          (1, img_data[column].shape[0], img_data[column].shape[1]))
                               for column in dist_columns], axis=-1)
    stacked_volnorms = numpy.stack([norms[column] for column in dist_columns], axis=-1)
    
    data  = [stacked_volume,
             img_data['skymap'].reshape(1, img_data['skymap'].shape[0], img_data['skymap'].shape[1], 1),
             numpy.reshape(dets, (1,3)),
             numpy.reshape(dist_mean , (1,1)),
             numpy.reshape(norms['skymap'], (1,1)),
             numpy.reshape(norms['vol0'], (1,1)),
             numpy.reshape(norms['vol1'], (1,1)),
             numpy.reshape(norms['vol2'], (1,1)),
             numpy.reshape(logbci, (1, 1)),
             numpy.reshape(logbsn, (1, 1))]
    
    return data


# In[5]:


def predict(loaded_model, data):
    """Use loaded model to predict result
    
    Keyword arguments:
    loaded_model: machine-learning model to use for prediction
    data: pre-processed data from FITS file
    threshold: real-noise threshold to predict real events (typically 0.5)
    """
    # apply the model to data
    prediction = tensorflow.squeeze(loaded_model(data), [-1])
    prediction = tensorflow.cast(prediction, tensorflow.float64).numpy()
    return prediction

# edited on 19th Nov 2022 to make v4 as the default
def get_rates(class_score, model = model_name):
    
    # check if model is one of the models for which FAR and FNR can be estimated.
    if not model == 'GWSkyNet_v4':
    
        raise Exception('Sorry, estimates of false positive rate and false negative rate currently works only with v4, while the requested model is %s.'%(model_name))
            
    else:
    # if yes, then read the corresponding rates
       temp       = numpy.genfromtxt(os.path.join(rate_path, '%s_rates.txt'%(model)), delimiter = '\t', comments = '#')
       thresholds = temp[:, 0]
       FARs       = temp[:, 1]
       FNRs       = temp[:, 2]
    
       # interpolate FAR and FNR for a given class score
       # if the class_score is less than the smallest value (threshold) in the rate txt file, just return the rates corresponding to
       # the smallest value (threshold) in the data because interpolation would then actually be exterpolation
       
       FAR_fun    = interpolate.interp1d(thresholds, FARs, bounds_error=False, fill_value=(FARs[0], FARs[-1]))
       FNR_fun    = interpolate.interp1d(thresholds, FNRs, bounds_error=False, fill_value=(FNRs[0], FNRs[-1]))
       
       far        = FAR_fun(class_score)
       fnr        = FNR_fun(class_score)
       
       return far, fnr
        
# In[25]:


def load_GWSkyNet_model(model_path = model_path, model_name = model_name):
    """Function to load the trained GWSkyNet model"""
    
    # check if the input model name has been defined earlier.
    if not model_name in model_names:
        raise ValueError('\n *** The input model name is not one of the available model names for the GWSkyNet classifier.')
    
    # the model file (architecture file and weight should use the same names).
    model_archi   = os.path.join(model_path, model_name + '.json')
    model_weights = os.path.join(model_path, model_name + '.h5')
    
    # raises if the relevant files are not found
    if not os.path.exists(model_archi):
        raise FileNotFoundError('\n *** The model architecture file %s does not exist. ' %(model_archi))
    
    if not os.path.exists(model_weights):
        raise FileNotFoundError('\n *** The model weight file %s does not exist. ' %(model_weights))
        
    # if the files are found, load the model and the weights
    with open(model_archi, 'r') as f:
        json_model = f.read()
        
    model = tensorflow.keras.models.model_from_json(json_model)
    model.load_weights(model_weights)
    
    return model

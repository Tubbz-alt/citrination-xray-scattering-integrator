import paws.api

paw = paws.api.start()

from pypif.obj import ChemicalSystem

def convert(files=[],pixel_size=None,detector_distance=None,wavelength=None,
        poni=None,rotations=None,**kwargs):
    """Convert .tif image files into labeled PIF records.

    Builds a PAWS workflow that uses pyFAI 
    to integrate a scattering spectrum
    and then produces a pypif.obj.ChemicalSystem
    that describes the scattering intensity.

    In the current version, 
    the input files are expected to be in .tif format.
    The integrator workflow is executed serially
    over the list of input files.

    Parameters
    ----------
    files : list
        list of filenames (strings) to be used as input,
        where one PIF will be produced for each input file.
    pixel_size : list
        list of two values: the x and y dimensions of the detector pixel,
        expressed in meters.

    Returns
    -------
    pifs : list
        pypif.obj.ChemicalSystem object describing scattering spectrum.    
    """
    if pixel_size is None:
        raise KeyError('No pixel size specified')
    if detector_distance is None:
        raise KeyError('No detector distance specified')
    if wavelength is None: 
        raise KeyError('No wavelength specified')
    if poni is None:
        raise KeyError('No poni (point of normal incidence) specified')

    poni_dict = dict(PixelSize1:pixel_size[0],
                    PixelSize2:pixel_size[1],
                    Distance:detector_distance,
                    Poni1: poni[0],
                    Poni2: poni[1],
                    Rot1: rotations[0],
                    Rot2: rotations[1],
                    Rot3: rotations[2],
                    Wavelength: wavelength)

PixelSize1: 7.9e-05
PixelSize2: 7.9e-05
Distance: 0.85827
Poni1: 0.08092839
Poni2: 0.0809276
Rot1: 0.0
Rot2: 0.0
Rot3: 0.0
Wavelength: 7.99898e-11

    paw = paws.api.start()
    paw.set_wf('batch')
    paw.execute()

    return paw.get_output('collect_pifs','pifs')



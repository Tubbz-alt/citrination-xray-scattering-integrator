import paws.api

paw = paws.api.start()

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

    poni_dict = dict(pixel1 = pixel_size[0],
                    pixel2 = pixel_size[1],
                    dist = detector_distance,
                    poni1 = poni[0],
                    poni2 = poni[1],
                    rot1 = rotations[0],
                    rot2 = rotations[1],
                    rot3 = rotations[2],
                    wavelength = wavelength)

    paw = paws.api.start()
    # prepare environment
    paw.activate_op('PROCESSING.INTEGRATION.BuildPyFAIIntegrator')
    paw.activate_op('EXECUTION.BATCH.BatchFromFiles')
    paw.activate_op('IO.IMAGE.LoadTif')
    paw.activate_op('PROCESSING.INTEGRATION.ApplyIntegrator1d')
    paw.activate_op('PACKAGING.PIF.Pif1dScatteringIntensity')
    paw.activate_op('PACKAGING.BATCH.BuildListFromBatch')
    
    # add workflows 
    # 1) integrate (integrates) 
    # 2) main (executes integrate as batch)
    paw.add_wf('main')
    paw.add_wf('integrate')
    
    # set up integration workflow
    paw.select_wf('integrate')
    paw.add_op('load_tif','IO.IMAGE.LoadTif')
    paw.add_op('integrate','PROCESSING.INTEGRATION.ApplyIntegrator1d')
    paw.add_op('build_pif','PACKAGING.PIF.Pif1dScatteringIntensity')
    # expect the file path and integrator to be set by batch controller at runtime
    paw.set_input('load_tif','file_path',None,'runtime')
    paw.set_input('integrate','integrator',None,'runtime')
    # expect image data to be passed down from load_tif
    paw.set_input('integrate','data','load_tif.outputs.image_data','workflow item')
    # name the pif with the filename, and feed it the integrated q, I(q)
    paw.set_input('build_pif','uid','load_tif.outputs.filename','workflow item')
    paw.set_input('build_pif','q_I','integrate.outputs.q_I','workflow item')
    # map workflow inputs and outputs to operation items
    paw.add_wf_input('file_path','load_tif.inputs.file_path')
    paw.add_wf_input('integrator','integrate.inputs.integrator')
    paw.add_wf_output('q_I','integrate.outputs.q_I')
    paw.add_wf_output('filename','load_tif.outputs.filename')
    paw.add_wf_output('pif','build_pif.outputs.pif')
    
    # set up main workflow
    paw.select_wf('main')
    paw.add_op('build_integrator','PROCESSING.INTEGRATION.BuildPyFAIIntegrator')
    paw.add_op('batch','EXECUTION.BATCH.BatchFromFiles')
    paw.add_op('collect_pifs','PACKAGING.BATCH.BuildListFromBatch')
    # set batch to run the 'integrate' workflow for all of `files`.
    # set to input type 'basic', i.e. use the value directly. 
    paw.set_input('build_integrator','poni_dict',poni_dict,'basic')
    paw.set_input('batch','file_list',files)
    paw.set_input('batch','workflow','integrate')
    paw.set_input('batch','input_name','file_path')
    paw.set_input('collect_pifs','batch_output','batch.outputs.batch_outputs')
    paw.set_input('collect_pifs','output_name','pif')
    # set the batch to also provide the 'integrator' input
    paw.set_input('batch','extra_input_names',['integrator'])
    # get the integrator from a workflow item: the output of build_integrator
    paw.set_input('batch','extra_inputs',['build_integrator.outputs.integrator'],'workflow item')
    
    paw.execute()

    return paw.get_output('collect_pifs','pifs')



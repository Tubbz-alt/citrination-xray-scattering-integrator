import os
import unittest

class TestIntegrator(unittest.TestCase):

    def __init__(self,methodname,paw=None):
        super(TestIntegrator,self).__init__(methodname)

    def test(self):
        from xray_scattering_integrator import integrate
        import pypif
        test_filepath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'examples','test0.tif')
        print(test_filepath)
        pif_list = integrate.convert(
            [test_filepath],
            pixel_size=[7.9e-5,7.9e-5],
            detector_distance=0.888,
            wavelength=8.e-11,
            poni=[0.086,0.075],
            rotations=[0.,0.,0.]) 
        self.assertIsInstance(pif_list,list)
        self.assertIsInstance(pif_list[0],pypif.obj.ChemicalSystem)

if __name__ == '__main__':
    unittest.main()


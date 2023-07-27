'''
This is the automated toolkit that:
(1) converts a NEURON nerve model to COMSOL nerve model,
(2) extracellularly stimulates the nerve with TIME electrode; meshes, and studies the COMSOL nerve model; and exports the 
extracellular voltage profile to a .txt file,
(3) imports the .txt extracellular voltage values from COMSOL back to NEURON model as transfer resistance.

This toolkit takes as input a nerve model created in the NEURON simulator, permitting users to deploy a pre-existing, 
validated, and high-quality models in the literature (e.g., Sundt, Gamper, & Jaffe, 2015: Sundt; McIntyre, Richardson, 
& Grill, 2002: MRG). This eliminates the need to re-create and re-validate models from scratch. 
'''

import matlab.engine
import NEURON2COMSOL_auto_conv as N2C
import COMSOL2NEURON_auto_conv as C2N

def pipeline(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R, \
                                e_type="monopolar", e2e_dist=None, rotate_deg=0, simBox_G=1.45, nerve_G=0.01, fasc_G=0.0517, mesh_size=3):

    # automatically generate MATLAB script for the COMSOL nerve model
    print("NEURON TO COMSOL conversion ...\n")
    N2C.convert(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R, \
                                e_type, e2e_dist, rotate_deg, simBox_G, nerve_G, fasc_G, mesh_size)

    # automatically initiate MATLAB with LiveLink, and run the COMSOL model from MATLAB
    print("running MATLAB ...\n")
    eng = matlab.engine.start_matlab()
    eng.NEURON2COMSOL_auto_conv(nargout=0)
    eng.quit()

    # automatically export COMSOL's extracellular voltage data as a .txt file ready to be imported back to NEURON
    print("COMSOL to NEURON conversion ...\n")
    C2N.convert()

    print("Automated pipeline finishes !\n")
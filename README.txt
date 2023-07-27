-- Last updated Wed 24 Jan 2023 21:22:02 AEST
Yuyang Xie
Biomedical Microsystem Lab, PI: David Tsai
School of Biomedical Engineering, UNSW, Sydney

PROTOTYPE of toolkit
    pipeline(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R, \
                                e_type="monopolar", e2e_dist=None, rotate_deg=0, simBox_G=1.45, nerve_G=0.01, \
                                fasc_G=0.0517, mesh_size=3)                            
        Automate the NEURON-to-COMSOL and COMSOL-to-NEURON pipeline.
        
        This function converts a NEURON nerve model to a COMSOL nerve model. It uses TIME electrode to extracellularly 
        stimulate the nerve. It meshes and studies the COMSOL model, and exports the generated extracellular voltage 
        values to the NEURON model. 
        
        The generated COMSOL model consists of a cubic simulation box. Inside the simulation box is a cylindrical
        nerve defined by users. The nerve consists of cylindrical fascicles, which consist of cylindrical fibres. 
        A TIME electrode is inserted transversally into the nerve. The TIME electrode consists of a cuboid substrate 
        of type P25N Polyimide and a cylindrical stimulating electrode recessed at its centre. Orientation is towards 
        x-axis. Unit of length is in micrometre. 

        Parameters: 
                    path2server     string
                                    absolute path to COMSOL server's execution file comsolmphserver.exe; this file 
                                    is automatically run to initiate COMSOL server
                    path2mph        string
                                    absolute path to COMSOL's MATLAB with LiveLink file mphstart.m; this file is
                                    automatically run to link COMSOL with MALTAB via LiveLink
                    simBox_3D:      array_like
                                    [x, y, z] position of the centre of the simulation box
                    simBox_size:    int or float
                                    side length of the simulation box
                    nerve_3D:       array_like
                                    [x, y, z] position of the centre of nerve's starting face
                    nerve_R:        int or float
                                    radius of the nerve
                    nerve_L:        int or float
                                    length of the nerve
                    fasc_3D:        2D array_like
                                    [[x1, y1, z1], [x2, y2, z2], ..., [xn, yn, zn]] position of the centre of each 
                                    fascicle's starting face  
                    fasc_R:         array_like
                                    [R1, R2, ..., Rn] radius of each fascicle at the position specified by fasc_3D 
                    fasc_L:         int or float
                                    length of each fascicle; assumed to be identical for all fascicles
                    substrate_3D:   array_like
                                    [x, y, z] position of the centre of the TIME substrate
                    substrate_W:    int or float
                                    width of the TIME subtrate
                    substrate_L:    int or float
                                    length of the TIME subtrate                     
                    substrate_D:    int or float
                                    depth of the TIME subtrate
                    e_R:            int or float
                                    radius of the stimulating TIME electrode, placed at the centre of the substrate
                    e_type:         string, optional
                                    type of electrode: "monopolar" or "hexapolar"; the default is "monopolar"
                    e2e_dist:       int or float, optional
                                    electrode-to-electrode distance of the hexapolar TIME electrode; the default value 
                                    is None, which translates to 4 times the electrode radius; this argument does not 
                                    apply to monopolar setup
                    rotate_deg:     int or float, optional
                                    rotation of TIME substrate and electrode along x-axis in degree; the default is 0
                    simBox_G:       float, optional
                                    conductivity of the simulation box; the default is 1.45 S/m
                    nerve_G:        float, optional
                                    conductivity of the nerve; the default is 0.01 S/m
                    fasc_G:         float, optional
                                    conductivity of fascicles; assumed to be identical for all fascicles; the default 
                                    is 0.0517 S/m
                    mesh_size:      int, optional
                                    mesh resolution: 1 - extremely fine, 2 - extra fine, 3 - finer, 4 - fine, 
                                    5 - normal, 6 - coarse, 7 - coarser, 8 - extra coarse, 9 - extremely coarse;
                                    the default is 3 - finer
                    
        Returns:    there is no explicit return, but it generates four files in the working directory for users:
                    NEURON2COMSOL_auto_conv.m:      the MATLAB script that describes the COMSOL nerve model
                    NEURON2COMSOL_auto_conv.mph:    the COMSOL morphology file that describes the COMSOL nerve model
                    exStimVoltProf.txt:             the voltage profile exported from COMSOL
                    rx_xtra_interpolated.txt:       the transfer resistance used by NEURON's xtra.mod mechanism

PREPARATION WORK of TOOLKIT
    1. Users should have matlab.engine installed as a Python package for full automation (instructions below): 
    https://au.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

    2. Note that the mod files containing the ion channel mechanisms must be compiled using mknrndll or nrnivmodl
    after migrating the files to a different machine or after making any edits. The resulting dll file must be 
    stored in the directory in which the .hoc files are stored. 

USAGE of TOOLKIT
    1. make clean && make
    2. The toolkit requires you to build a NEURON nerve model in advance, either in NEURON's .hoc file or with 
    Python's .hoc object.
    3. If the NEURON model was built in NEURON's .hoc file, open a new Python script and type "from neuron import h", 
    then load the NEURON model using h.load_file(). If the NEURON model was built with Python's .hoc object, just 
    continue on the same Python script. 
    4. Import toolkit's header by typing "import autoToolkit as tk". 
    5. Declare toolkit's arguements.
    6. Automate the pipeline by calling tk.pipeline() with the arguements.

    After the toolkit finishes running, the NEURON nerve model will be assigned with transfer resistance representing
    the extracellular voltage profile as simulated by COMSOL.

EXAMPLE of TOOLKIT
    Two step-by-step examples for how to use the toolkit can be found in example_simple.py and example_sciaticNerve.py.
    The former is an example for converting a simplified nerve structure from NEURON to COMSOL using the toolkit. The
    latter is a complex example for converting a sciatic nerve. However, despite the sciatic nerve example has a more 
    intricate structure, the steps taken to run the toolkit is similar. This program shields all modelling complexity 
    from users. 

    Expected terminal outcome after running example_simple.py:

        MATLAB is now connected to a COMSOL Multiphysics Server at localhost:2036

        Run the commands below to access the COMSOL ModelUtil commands:
        import com.comsol.model.util.*
        building simulation box ...
        building nerve ...
        building fascicles ...
        building fibre geometry:  100%
        getting fibre entity number:  100%
        assigning fibre conductivity:  100%
        meshing ...
        studying ...
        exporting data ...
        saving model ...
        NEURON-to-COMSOL automatic conversion done.
        Elapsed time is 155.853864 seconds.

        ans =

        COMSOL Model Object
        Name: NEURON2COMSOL_auto_conv.mph
        Tag: Model
        Identifier: root

SEPERATE USAGE of TOOLKIT FUNCTIONS
    The toolkit's functions can be run seperately. The toolkit contains two main functions: (i) N2C.convert() and 
    (ii) C2N.convert(). The former converts the NEURON nerve model to COMSOL nerve model. The latter converts the 
    generated COMSOL's voltage profile to NEURON's transfer resistance. While the toolkit provides full automation
    to run these two functions in one go, users are free to use these functions seperately according to their need, 
    with minimum manual work involved:

    * To use N2C.convert(), users should have the NEURON model ready, then import NEURON2COMSOL_auto_conv.py as N2C, 
    and call N2C.convert() with relevant arguments.
    * To use C2N.convert(), users should have the COMSOL voltage profile as .txt file ready, name it as 
    exVoltStimProf.txt, then import COMSOL2NEURON_auto_conv.py as C2N, and call C2N.convert() with relevant arguments.

    An example for seperate function usage is provided in example_seperate.py. 

TROUBLESHOOTING
    If users have difficulty installing matlab.engine, they can still automate the toolkit with minimual manual work:
    1. import NEURON2COMSOL_auto_conv.py as N2C, and call N2C.convert() with relevant arguments.
    2. Manually open the auto-generated MATLAB file NEURON2COMSOL_auto_conv.m and run it.
    3. import NEURON2COMSOL_auto_conv.py as N2C, and call N2C.convert() with relevant arguments.

DIRECTORY SUMMARY
    data/                       Data files for generating manuscript's figures
    mod/                        Model mechanism files
    nerve/                      NEURON's .hoc files for constructing a sciatic nerve
    scripts/                    Python and .hoc scripts for generating manuscript data; MATLAB scripts for plotting
                                manuscript figures

    In the data/ directory, some pre-run data is prepared for user to quickly test the toolkit. This includes:
    * Model validation data for A and C fibre (locate in data/modelValidation/AFibreModelValidation.txt and 
    data/modelValidation/CFibreModelValidation.txt). The data can be reproduced by running the script 
    Fig3_AFibreModelValidation.hoc and Fig3_CFibreModelValidation.hoc.
    * Fibre spike rates from kilohertz stimulation in monopolar and hexapolar TIME setup (locate in 
    data/PE/mono.txt and data/PE/hex.txt). The data can be reproduced by running Fig8_PE_mono.py or Fig8_PE_hex.py.
    * Transfer resistance from monopolar TIME setup (locate in data/rx/rx_xtra_interpolated_mono.txt). The data can 
    be reproduced by running the script example_sciaticNerve.py.

    Please move all scripts to the main directory before running them.

FILE SUMMARY
    autoToolkit.py              Automated toolkit for the NEURON-to-COMSOL and COMSOL-to-NEURON pipeline
    NEURON2COMSOL_auto_conv.py  Converts a NEURON nerve model to COMSOL nerve model; extracellularly stimulates, meshes, 
                                and studies the COMSOL nerve model; exports the COMSOL voltage profile as a .txt file
    COMSOL2NEURON_auto_conv.py  Imports and interpolates the .txt COMSOL voltage profile back to NEURON model; 
                                converts extracellular voltage to transfer resistance used by NEURON's .xtra mechanism;
    setrx.hoc                   Assigns transfer resistance to each NEURON's .hoc section
    example_simple.py           A toolkit example for a simple nerve containing one fascicle and two fibres
    example_sciaticNerve.py     A toolkit example for a complex sciatic nerve
    example_seperate.py         A toolkit example for using the toolkit's functions seperately
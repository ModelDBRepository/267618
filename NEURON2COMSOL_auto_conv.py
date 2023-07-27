'''
This file is automatically run by the toolkit. Or, it can be seperately run by users.

It generates a MATLAB script which converts one or many cable-like neuron, together with its extracellular environment, 
from NEURON to COMSOL Multiphysics. It stimulates, meshes, and studies the COMSOL model and exports the voltage profile 
as a .txt file. 

In detail, nine steps are implemented sequentially: 
(1) build the simulation box, 
(2) build the nerve,
(3) build the fascicles,
(4) build the fibres,
(5) build the TIME electrode,
(6) assign conductivity to all the elements,
(7) mesh the COMSOL model,
(8) study the COMSOL model,
(9) export the voltage profile to a .txt file.

Two assumptions / simplifications are made:
(1) the nerve and fascicles are approximated to be cylindrical,
(2) the nerve, fascicles, fibres are all oriented towards x-axis. 
'''

from neuron import h
from datetime import datetime


version = "1.0"


"""
Defines geometry entity, electric current entity, units, and mphselect margins.
"""
def writePreamble(fout, path2server, path2mph):

    # write function header
    txt = \
    "%% AUTO GENERATED CODE. DO NOT MODIFY.\n" \
    "%% Created on %s by NEURON2COMSOL_auto_conv.py version %s\n\n" \
    "function model = NEURON2COMSOL_auto_conv\n"
    fout.write(txt % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), version))

    # write preamble
    txt = \
        r"""
    clc; clear;
    tic;

    %% start COMSOL server
    cd '%s'
    open('comsolmphserver.exe');

    %% link COMSOL with MATLAB through LiveLink
    cd '%s'
    mphstart(2036);

    %% change back to current foler
    if(~isdeployed)
        cd(fileparts(matlab.desktop.editor.getActiveFilename));
    end

    import com.comsol.model.*
    import com.comsol.model.util.*

    model = ModelUtil.create('Model');
    model.label('NEURON2COMSOL_auto_conv.mph');
    model.component.create('comp1', true);

    %% create COMSOL geometry entity
    model.component('comp1').geom.create('geom1', 3);

    %% create COMSOL electric current entity
    model.component('comp1').physics.create('ec', 'ConductiveMedia', 'geom1');

    %% set units to um
    model.component('comp1').geom('geom1').lengthUnit( ...
            [native2unicode(hex2dec({'00' 'b5'}), 'unicode') 'm']);
    model.component('comp1').geom('geom1').geomRep('comsol');

    %% set the margin for the function mphselectbox()
    delta = 0.05;
        """ 
    fout.write(txt % (path2server, path2mph))


"""
Build a simulation environment box that contains the nerve, and refer the envionrment boundaries as electric gound.
Input:
simBox_3D:      array_like
                [x, y, z] position of the centre of the simulation box
simBox_size:    int or float
                side length of the simulation box
simBox_G:       float, optional
                conductivity of the simulation box; the default is 1.45 S/m
"""
def buildSimBox(fout, simBox_3D, simBox_size, simBox_G=1.45):

    txt = \
       r"""
    %% build a extracellular simulation box
    fprintf('building simulation box ...\n');
    xpos = %g;
    ypos = %g;
    zpos = %g;
    size = %g;
    model.component('comp1').geom('geom1').create('simBox', 'Block');
    model.component('comp1').geom('geom1').feature('simBox').set('base', 'center');
    model.component('comp1').geom('geom1').feature('simBox').set('pos', [xpos ypos zpos]);
    model.component('comp1').geom('geom1').feature('simBox').set('size', [size size size]);
    simBox_domain = mphselectbox(model, 'geom1', [xpos-size-delta ypos+size+delta zpos-size-delta; xpos+size+delta ...
        ypos-size-delta zpos+size+delta]', 'domain', 'include', 'any');
    model.component('comp1').geom('geom1').run('simBox');
    model.component('comp1').material.create('matsimBox', 'Common');
    model.component('comp1').material('matsimBox').selection.set([simBox_domain]);
    model.component('comp1').material('matsimBox').propertyGroup('def').set('electricconductivity', {'%g'});

    %% add ground reference to the simulation box
    simBox_bndry = mphselectbox(model, 'geom1', [xpos-size-delta ypos+size+delta zpos-size-delta; xpos+size+delta ...
        ypos-size-delta zpos+size+delta]', 'boundary', 'include', 'any');
    model.component('comp1').physics('ec').create('gndsimBox1', 'Ground', 2);
    model.component('comp1').physics('ec').feature('gndsimBox1').selection.set(simBox_bndry);
        """
    fout.write(txt % (simBox_3D[0], simBox_3D[1], simBox_3D[2], simBox_size, simBox_G))


"""
Build a cylindrical nerve that contains fascicle(s). The cylindrical nerve is oriented towards x-axis. 
Input:
nerve_3D:       array_like
                [x, y, z] position of the centre of nerve's starting face
nerve_R:        int or float
                radius of the nerve
nerve_L:        int or float
                length of the nerve
nerve_G:        float, optional
                conductivity of the nerve; the default is 0.01 S/m
"""
def buildNerve(fout, nerve_3D, nerve_R, nerve_L, nerve_G=0.01):

    txt = \
        r"""
    %% build the nerve wrapping arouond the fascicle(s)
    fprintf('building nerve ...\n');
    xpos = %g;
    ypos = %g;
    zpos = %g;
    h = %g;
    r = %g;
    model.component('comp1').geom('geom1').create('nerve1', 'Cylinder');
    model.component('comp1').geom('geom1').feature('nerve1').set('axis', [1 0 0]);
    model.component('comp1').geom('geom1').feature('nerve1').set('h', h);
    model.component('comp1').geom('geom1').feature('nerve1').set('r', r);
    model.component('comp1').geom('geom1').feature('nerve1').set('pos', [xpos ypos zpos]);
    nerve_domain = mphselectbox(model, 'geom1', [xpos-delta ypos+r+delta zpos-r-delta; xpos+h+delta ...
        ypos-r-delta zpos+r+delta]', 'domain', 'include', 'any');
    model.component('comp1').material.create('matnerve1');
    model.component('comp1').material('matnerve1').materialModel('def').set('electricconductivity', {'%g[S/m]'});    
    model.component('comp1').material('matnerve1').selection().set(nerve_domain);
        """
    fout.write(txt % (nerve_3D[0], nerve_3D[1], nerve_3D[2], nerve_L, nerve_R, nerve_G))


"""
Build a monopolar TIME electrode consisting of a cuboid substrate of type P25N Polyimide and a cylindrical 
stimulating electrode recessed at its centre.
Input:
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
rotate_deg:     int or float, optional
                rotation of TIME along x-axis in degree; the default is 0
"""
def buildMonopolarElectrode(fout, substrate_3D, substrate_W, substrate_L, substrate_D, e_R, rotate_deg):

    txt = \
        r"""
    %% build substrate for TIME electrode
    substrate_x = %g;
    substrate_y = %g;
    substrate_z = %g;
    substrate_width = %g;
    substrate_length = %g;
    substrate_thick = %g;
    model.component('comp1').geom('geom1').create('substrate', 'Block');
    model.component('comp1').geom('geom1').feature('substrate').set('size', [substrate_width substrate_length substrate_thick]);
    model.component('comp1').geom('geom1').feature('substrate').set('base', 'center');
    model.component('comp1').geom('geom1').feature('substrate').set('pos', [substrate_x substrate_y substrate_z]);
    substrate_domain = mphselectbox(model, 'geom1', [substrate_x-substrate_width/2-delta substrate_y+substrate_length/2+delta ...
        substrate_z-substrate_thick/2-delta; substrate_x+substrate_width/2+delta substrate_y-substrate_length/2-delta ...
        substrate_z+substrate_thick/2+delta]', 'domain', 'include', 'any');
    model.component('comp1').material.create('matsubstrate');
    model.component('comp1').material('matsubstrate').label('P96/P26 Polyimide-based Prepreg and Laminate');
    model.component('comp1').material('matsubstrate').propertyGroup('def').set('electricconductivity', {'1e-99'});
    model.component('comp1').material('matsubstrate').selection().set(substrate_domain);

    %% make a hole in the subtrate to reside electrode
    electrode_x = substrate_x;
    electrode_y = substrate_y;
    electrode_z = substrate_z;
    electrode_h = substrate_thick/4;
    recession_depth = substrate_thick/4;
    electrode_r = %g;
    model.component('comp1').geom('geom1').create('hole', 'Cylinder');
    model.component('comp1').geom('geom1').feature('hole').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('hole').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('hole').set('pos', [electrode_x electrode_y electrode_z]);
    model.component('comp1').geom('geom1').create('dif1', 'Difference');
    model.component('comp1').geom('geom1').feature('dif1').selection('input').set({'substrate'});
    model.component('comp1').geom('geom1').feature('dif1').selection('input2').set({'hole'});

    %% build TIME electrode
    model.component('comp1').geom('geom1').create('electrode', 'Cylinder');
    model.component('comp1').geom('geom1').feature('electrode').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('electrode').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('electrode').set('pos', [electrode_x electrode_y electrode_z]);
    e_domain = mphselectbox(model, 'geom1', [electrode_x-electrode_r-delta electrode_y+electrode_r+delta electrode_z-delta; ... 
        electrode_x+electrode_r+delta electrode_y-electrode_r-delta electrode_z+electrode_h+delta]', 'domain', 'include', 'any');
    model.component('comp1').material.create('mate1');
    model.component('comp1').material('mate1').materialModel('def').set('electricconductivity', {'1e7[S/m]'});    
    model.component('comp1').material('mate1').selection().set(e_domain);

    %% add current source to the electrode using floating potential
    model.component('comp1').physics('ec').create('fpe1', 'FloatingPotential', 2);
    e_bdrny = mphselectbox(model, 'geom1', [electrode_x-electrode_r-delta electrode_y+electrode_r+delta electrode_z-delta; ... 
        electrode_x+electrode_r+delta electrode_y-electrode_r-delta electrode_z+electrode_h+delta]', 'boundary', 'include', 'any');
    model.component('comp1').physics('ec').feature('fpe1').selection.set(e_bdrny);
    model.component('comp1').physics('ec').feature('fpe1').set('I0', '1e-6');

    %% optionally rotate TIME
    model.component('comp1').geom('geom1').create('rot1', 'Rotate');
    model.component('comp1').geom('geom1').feature('rot1').selection('input').set({'electrode' 'dif1'});
    model.component('comp1').geom('geom1').feature('rot1').set('axistype', 'x');
    model.component('comp1').geom('geom1').feature('rot1').set('rot', %g);
        """
    fout.write(txt % (substrate_3D[0], substrate_3D[1], substrate_3D[2], substrate_W, substrate_L, substrate_D, \
            e_R, rotate_deg))


"""
Build a hexapolar TIME electrode consisting of a cuboid substrate of type P25N Polyimid and a cylindrical 
stimulating electrode together with six surrounding return electrodes.
Input:
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
e2d_dist:       int or float
                electrode-to-electrode distance of the hexapolar TIME electrode; the default value is 4 times the 
                electrode radius
rotate_deg:     int or float, optional
                rotation of TIME along x-axis in degree; the default is 0
"""
def buildHexapolarElectrode(fout, substrate_3D, substrate_W, substrate_L, substrate_D, e_R, e2e_dist, rotate_deg):

    # if e2e_dist has value None, set e2e_dist to its default value: 4 times the electrode radius
    if e2e_dist == None:
        e2e_dist = e_R*4

    txt = \
        r"""
    %% build substrate for TIME electrode
    substrate_x = %g;
    substrate_y = %g;
    substrate_z = %g;
    substrate_width = %g;
    substrate_length = %g;
    substrate_thick = %g;
    model.component('comp1').geom('geom1').create('substrate', 'Block');
    model.component('comp1').geom('geom1').feature('substrate').set('size', [substrate_width substrate_length substrate_thick]);
    model.component('comp1').geom('geom1').feature('substrate').set('base', 'center');
    model.component('comp1').geom('geom1').feature('substrate').set('pos', [substrate_x substrate_y substrate_z]);
    substrate_domain = mphselectbox(model, 'geom1', [substrate_x-substrate_width/2-delta substrate_y+substrate_length/2+delta ...
        substrate_z-substrate_thick/2-delta; substrate_x+substrate_width/2+delta substrate_y-substrate_length/2-delta ...
        substrate_z+substrate_thick/2+delta]', 'domain', 'include', 'any');
    model.component('comp1').material.create('matsubstrate');
    model.component('comp1').material('matsubstrate').label('P96/P26 Polyimide-based Prepreg and Laminate');
    model.component('comp1').material('matsubstrate').propertyGroup('def').set('electricconductivity', {'1e-99'});
    model.component('comp1').material('matsubstrate').selection().set(substrate_domain);

    %% make one hole for the central stimulating electrode in the subtrate
    stim_electrode_x = substrate_x;
    stim_electrode_y = substrate_y;
    stim_electrode_z = substrate_z;
    electrode_h = substrate_thick/4;
    recession_depth = substrate_thick/4;
    electrode_r = %g;
    model.component('comp1').geom('geom1').create('stim_hole', 'Cylinder');
    model.component('comp1').geom('geom1').feature('stim_hole').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('stim_hole').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('stim_hole').set('pos', [stim_electrode_x stim_electrode_y stim_electrode_z]);

    %% make six holes for the surrounding return electrode in the subtrate
    e2e_dist = %g;
    rtn_electrode1_x = substrate_x + e2e_dist;
    rtn_electrode1_y = substrate_y;
    rtn_electrode1_z = substrate_z;
    model.component('comp1').geom('geom1').create('rtn_hole1', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_hole1').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_hole1').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('rtn_hole1').set('pos', [rtn_electrode1_x rtn_electrode1_y rtn_electrode1_z]);

    rtn_electrode2_x = substrate_x - e2e_dist;
    rtn_electrode2_y = substrate_y;
    rtn_electrode2_z = substrate_z;
    model.component('comp1').geom('geom1').create('rtn_hole2', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_hole2').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_hole2').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('rtn_hole2').set('pos', [rtn_electrode2_x rtn_electrode2_y rtn_electrode2_z]);

    rtn_electrode3_x = substrate_x + cos(pi/3)*e2e_dist;
    rtn_electrode3_y = substrate_y + sin(pi/3)*e2e_dist;
    rtn_electrode3_z = substrate_z;
    model.component('comp1').geom('geom1').create('rtn_hole3', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_hole3').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_hole3').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('rtn_hole3').set('pos', [rtn_electrode3_x rtn_electrode3_y rtn_electrode3_z]);

    rtn_electrode4_x = substrate_x - cos(pi/3)*e2e_dist;
    rtn_electrode4_y = substrate_y + sin(pi/3)*e2e_dist;
    rtn_electrode4_z = substrate_z;
    model.component('comp1').geom('geom1').create('rtn_hole4', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_hole4').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_hole4').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('rtn_hole4').set('pos', [rtn_electrode4_x rtn_electrode4_y rtn_electrode4_z]);

    rtn_electrode5_x = substrate_x - cos(pi/3)*e2e_dist;
    rtn_electrode5_y = substrate_y - sin(pi/3)*e2e_dist;
    rtn_electrode5_z = substrate_z;
    model.component('comp1').geom('geom1').create('rtn_hole5', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_hole5').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_hole5').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('rtn_hole5').set('pos', [rtn_electrode5_x rtn_electrode5_y rtn_electrode5_z]);

    rtn_electrode6_x = substrate_x + cos(pi/3)*e2e_dist;
    rtn_electrode6_y = substrate_y - sin(pi/3)*e2e_dist;
    rtn_electrode6_z = substrate_z;
    model.component('comp1').geom('geom1').create('rtn_hole6', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_hole6').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_hole6').set('h', electrode_h+recession_depth);
    model.component('comp1').geom('geom1').feature('rtn_hole6').set('pos', [rtn_electrode6_x rtn_electrode6_y rtn_electrode6_z]);

    model.component('comp1').geom('geom1').create('dif1', 'Difference');
    model.component('comp1').geom('geom1').feature('dif1').selection('input').set({'substrate'});
    model.component('comp1').geom('geom1').feature('dif1').selection('input2').set({'stim_hole', 'rtn_hole1', 'rtn_hole2', 'rtn_hole3', 'rtn_hole4', 'rtn_hole5', 'rtn_hole6'});

    %% build hexapolar TIME electrodes and assign conductivity
    model.component('comp1').geom('geom1').create('stim_electrode', 'Cylinder');
    model.component('comp1').geom('geom1').feature('stim_electrode').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('stim_electrode').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('stim_electrode').set('pos', [stim_electrode_x stim_electrode_y stim_electrode_z]);

    model.component('comp1').geom('geom1').create('rtn_electrode1', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_electrode1').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_electrode1').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('rtn_electrode1').set('pos', [rtn_electrode1_x rtn_electrode1_y rtn_electrode1_z]);

    model.component('comp1').geom('geom1').create('rtn_electrode2', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_electrode2').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_electrode2').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('rtn_electrode2').set('pos', [rtn_electrode2_x rtn_electrode2_y rtn_electrode2_z]);

    model.component('comp1').geom('geom1').create('rtn_electrode3', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_electrode3').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_electrode3').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('rtn_electrode3').set('pos', [rtn_electrode3_x rtn_electrode3_y rtn_electrode3_z]);

    model.component('comp1').geom('geom1').create('rtn_electrode4', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_electrode4').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_electrode4').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('rtn_electrode4').set('pos', [rtn_electrode4_x rtn_electrode4_y rtn_electrode4_z]);

    model.component('comp1').geom('geom1').create('rtn_electrode5', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_electrode5').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_electrode5').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('rtn_electrode5').set('pos', [rtn_electrode5_x rtn_electrode5_y rtn_electrode5_z]);

    model.component('comp1').geom('geom1').create('rtn_electrode6', 'Cylinder');
    model.component('comp1').geom('geom1').feature('rtn_electrode6').set('r', electrode_r);
    model.component('comp1').geom('geom1').feature('rtn_electrode6').set('h', electrode_h);
    model.component('comp1').geom('geom1').feature('rtn_electrode6').set('pos', [rtn_electrode6_x rtn_electrode6_y rtn_electrode6_z]);

    stim_e_domain = mphselectbox(model, 'geom1', [stim_electrode_x-electrode_r-delta stim_electrode_y+electrode_r+delta stim_electrode_z-delta; ... 
        stim_electrode_x+electrode_r+delta stim_electrode_y-electrode_r-delta stim_electrode_z+electrode_h+delta]', 'domain', 'include', 'any');
    rtn_e1_domain = mphselectbox(model, 'geom1', [rtn_electrode1_x-electrode_r-delta rtn_electrode1_y+electrode_r+delta rtn_electrode1_z-delta; ... 
        rtn_electrode1_x+electrode_r+delta rtn_electrode1_y-electrode_r-delta rtn_electrode1_z+electrode_h+delta]', 'domain', 'include', 'any');
    rtn_e2_domain = mphselectbox(model, 'geom1', [rtn_electrode2_x-electrode_r-delta rtn_electrode2_y+electrode_r+delta rtn_electrode2_z-delta; ... 
        rtn_electrode2_x+electrode_r+delta rtn_electrode2_y-electrode_r-delta rtn_electrode2_z+electrode_h+delta]', 'domain', 'include', 'any');
    rtn_e3_domain = mphselectbox(model, 'geom1', [rtn_electrode3_x-electrode_r-delta rtn_electrode3_y+electrode_r+delta rtn_electrode3_z-delta; ... 
        rtn_electrode3_x+electrode_r+delta rtn_electrode3_y-electrode_r-delta rtn_electrode3_z+electrode_h+delta]', 'domain', 'include', 'any');
    rtn_e4_domain = mphselectbox(model, 'geom1', [rtn_electrode4_x-electrode_r-delta rtn_electrode4_y+electrode_r+delta rtn_electrode4_z-delta; ... 
        rtn_electrode4_x+electrode_r+delta rtn_electrode4_y-electrode_r-delta rtn_electrode4_z+electrode_h+delta]', 'domain', 'include', 'any');
    rtn_e5_domain = mphselectbox(model, 'geom1', [rtn_electrode5_x-electrode_r-delta rtn_electrode5_y+electrode_r+delta rtn_electrode5_z-delta; ... 
        rtn_electrode5_x+electrode_r+delta rtn_electrode5_y-electrode_r-delta rtn_electrode5_z+electrode_h+delta]', 'domain', 'include', 'any');
    rtn_e6_domain = mphselectbox(model, 'geom1', [rtn_electrode6_x-electrode_r-delta rtn_electrode6_y+electrode_r+delta rtn_electrode6_z-delta; ... 
        rtn_electrode6_x+electrode_r+delta rtn_electrode6_y-electrode_r-delta rtn_electrode6_z+electrode_h+delta]', 'domain', 'include', 'any');

    model.component('comp1').material.create('mate1');
    model.component('comp1').material('mate1').materialModel('def').set('electricconductivity', {'1e7[S/m]'});    
    model.component('comp1').material('mate1').selection().set([stim_e_domain, rtn_e1_domain, rtn_e2_domain, rtn_e3_domain, rtn_e4_domain, rtn_e5_domain, rtn_e6_domain]);

    %% add stimulating current source to the stimulating electrode using floating potential
    stim_e_bdrny = mphselectbox(model, 'geom1', [stim_electrode_x-electrode_r-delta stim_electrode_y+electrode_r+delta stim_electrode_z-delta; ... 
        stim_electrode_x+electrode_r+delta stim_electrode_y-electrode_r-delta stim_electrode_z+electrode_h+delta]', 'boundary', 'include', 'any');
    model.component('comp1').physics('ec').create('stim_fpe', 'FloatingPotential', 2);
    model.component('comp1').physics('ec').feature('stim_fpe').selection.set(stim_e_bdrny);
    model.component('comp1').physics('ec').feature('stim_fpe').set('I0', '1e-6');

    %% add sinking current source to the return electrodes using floating potential
    rtn_e1_bdrny = mphselectbox(model, 'geom1', [rtn_electrode1_x-electrode_r-delta rtn_electrode1_y+electrode_r+delta rtn_electrode1_z-delta; ... 
        rtn_electrode1_x+electrode_r+delta rtn_electrode1_y-electrode_r-delta rtn_electrode1_z+electrode_h+delta]', 'boundary', 'include', 'any');
    rtn_e2_bdrny = mphselectbox(model, 'geom1', [rtn_electrode2_x-electrode_r-delta rtn_electrode2_y+electrode_r+delta rtn_electrode2_z-delta; ... 
        rtn_electrode2_x+electrode_r+delta rtn_electrode2_y-electrode_r-delta rtn_electrode2_z+electrode_h+delta]', 'boundary', 'include', 'any');
    rtn_e3_bdrny = mphselectbox(model, 'geom1', [rtn_electrode3_x-electrode_r-delta rtn_electrode3_y+electrode_r+delta rtn_electrode3_z-delta; ... 
        rtn_electrode3_x+electrode_r+delta rtn_electrode3_y-electrode_r-delta rtn_electrode3_z+electrode_h+delta]', 'boundary', 'include', 'any');
    rtn_e4_bdrny = mphselectbox(model, 'geom1', [rtn_electrode4_x-electrode_r-delta rtn_electrode4_y+electrode_r+delta rtn_electrode4_z-delta; ... 
        rtn_electrode4_x+electrode_r+delta rtn_electrode4_y-electrode_r-delta rtn_electrode4_z+electrode_h+delta]', 'boundary', 'include', 'any');
    rtn_e5_bdrny = mphselectbox(model, 'geom1', [rtn_electrode5_x-electrode_r-delta rtn_electrode5_y+electrode_r+delta rtn_electrode5_z-delta; ... 
        rtn_electrode5_x+electrode_r+delta rtn_electrode5_y-electrode_r-delta rtn_electrode5_z+electrode_h+delta]', 'boundary', 'include', 'any');
    rtn_e6_bdrny = mphselectbox(model, 'geom1', [rtn_electrode6_x-electrode_r-delta rtn_electrode6_y+electrode_r+delta rtn_electrode6_z-delta; ... 
        rtn_electrode6_x+electrode_r+delta rtn_electrode6_y-electrode_r-delta rtn_electrode6_z+electrode_h+delta]', 'boundary', 'include', 'any');
    model.component('comp1').physics('ec').create('rtn_fpe', 'FloatingPotential', 2);
    model.component('comp1').physics('ec').feature('rtn_fpe').selection.set([rtn_e1_bdrny, rtn_e2_bdrny, rtn_e3_bdrny, rtn_e4_bdrny, rtn_e5_bdrny, rtn_e6_bdrny]);
    model.component('comp1').physics('ec').feature('rtn_fpe').set('I0', '-1e-6');

    %% optionally rotate TIME
    model.component('comp1').geom('geom1').create('rot1', 'Rotate');
    model.component('comp1').geom('geom1').feature('rot1').selection('input').set({'stim_electrode' 'rtn_electrode1' 'rtn_electrode2' 'rtn_electrode3' 'rtn_electrode4' 'rtn_electrode5' 'rtn_electrode6' 'dif1'});
    model.component('comp1').geom('geom1').feature('rot1').set('axistype', 'x');
    model.component('comp1').geom('geom1').feature('rot1').set('rot', %g);
        """
    fout.write(txt % (substrate_3D[0], substrate_3D[1], substrate_3D[2], substrate_W, substrate_L, substrate_D, \
            e_R, e2e_dist, rotate_deg))


"""
Build cylindrical fascicles. 
Input:
fasc_3D:        2D array_like
                [[x1, y1, z1], [x2, y2, z2], ..., [xn, yn, zn]] position of the centre of each 
                fascicle's starting face  
fasc_R:         array_like
                [R1, R2, ..., Rn] radius of each fascicle at the position specified by fasc_3D 
fasc_L:         int or float
                length of each fascicle; assumed to be identical for all fascicles
fasc_G:         float, optional
                conductivity of fascicles; assumed to be identical for all fascicles; 
                the default is 0.0517 S/m
"""
def buildFascicle(fout, fasc_3D, fasc_R, fasc_L, fasc_G=0.0517):

    txt = \
        r"""
    % build the fascicle wrapping arouond the fibre(s)
    fprintf('building fascicles ...\n');
    fasc_domains = [];
        """
    fout.write(txt)

    Nfasc = len(fasc_R)
    for i in range(Nfasc):
        txt = \
        r"""
    fascName = append('fasc', '%g');
    matName = append('mat', fascName);
    h = %g;
    r = %g;
    xpos = %g;
    ypos = %g;
    zpos = %g;
    model.component('comp1').geom('geom1').create(fascName, 'Cylinder');
    model.component('comp1').geom('geom1').feature(fascName).set('axis', [1 0 0]);
    model.component('comp1').geom('geom1').feature(fascName).set('h', h);
    model.component('comp1').geom('geom1').feature(fascName).set('r', r);
    model.component('comp1').geom('geom1').feature(fascName).set('pos', [xpos ypos zpos]);
    fasc_domain = mphselectbox(model, 'geom1', [xpos-delta ypos+r+delta zpos-r-delta; xpos+h+delta ...
        ypos-r-delta zpos+r+delta]', 'domain', 'include', 'any');
    fasc_domains = [fasc_domains, fasc_domain];
    model.component('comp1').material.create(matName);
    model.component('comp1').material(matName).materialModel('def').set('electricconductivity', {'%g[S/m]'});   
    model.component('comp1').material(matName).selection().set(fasc_domain);
        """
        fout.write(txt % (i, fasc_L, fasc_R[i], fasc_3D[i][0], fasc_3D[i][1], fasc_3D[i][2], fasc_G))


"""
Build the COMSOL fibre geometries by copying fibres' geometrical information from NEURON's .hoc section.
"""
def buildFibreGeom(fout):

    txt = \
        r"""
    % build fibre(s)
    fprintf('building fibre geometry: %3d%%\n', 0);
        """
    fout.write(txt)

    # iterate through NEURON's .hoc sections, and describe each section using COMSOL's language
    Nsec = 0
    for sec in h.allsec():
        Nsec = Nsec + 1

    secCounter = 0
    for sec in h.allsec():
        secCounter = secCounter + 1
        name = ''.join(e for e in str(sec) if e.isalnum())
        height = sec.L
        radius = sec.diam / 2
        x = sec.x3d(0)
        y = sec.y3d(0)
        z = sec.z3d(0)
        txt = \
        r"""
    cylName = "%s";
    model.component('comp1').geom('geom1').create(cylName, 'Cylinder');
    model.component('comp1').geom('geom1').feature(cylName).set('axis', [1 0 0]);
    model.component('comp1').geom('geom1').feature(cylName).set('h', %g);
    model.component('comp1').geom('geom1').feature(cylName).set('r', %g);
    model.component('comp1').geom('geom1').feature(cylName).set('pos', [%g %g %g]);
    fprintf('\b\b\b\b%%3.0f%%%%', %g); pause(0.1);
        """
        fout.write(txt % (name, height, radius, x, y, z, 100*secCounter/Nsec))

    txt = \
        r"""
    fprintf('\n');
        """
    fout.write(txt)


"""
Obtain fibres' entity number which uniquely refer to a fibre domain, and store them in a dictionary.
"""
def getFibreEntityNum(fout):

    txt = \
        r"""
    % get entity number
    entityNum = containers.Map; 
    fprintf('getting fibre entity number: %3d%%\n', 0);
        """
    fout.write(txt)

    # store fibre's entity number in a dictionary
    Nsec = 0
    for sec in h.allsec():
        Nsec = Nsec + 1

    secCounter = 0
    for sec in h.allsec():
        secCounter = secCounter + 1
        name = ''.join(e for e in str(sec) if e.isalnum())
        height = sec.L
        radius = sec.diam / 2
        x = sec.x3d(0)
        y = sec.y3d(0)
        z = sec.z3d(0)
        txt = \
        r"""
    h = %g;
    r = %g;
    xpos = %g;
    ypos = %g;
    zpos = %g;
    entityNum('%s') = mphselectbox(model, 'geom1', [xpos-delta ypos+r+delta zpos-r-delta; xpos+h+delta ...
            ypos-r-delta zpos+r+delta]', 'domain', 'include', 'any');
    fprintf('\b\b\b\b%%3.0f%%%%', %g); pause(0.1);
        """
        fout.write(txt % (height, radius, x, y, z, name, 100*secCounter/Nsec))

    # create an array to store all geom domains
    txt = \
        r"""
    fprintf('\n');
    fibre_domains = cell2mat(entityNum.values());
        """
    fout.write(txt)


"""
Assign conductivity to each fibre geometry.
"""
def assignFibreConductivity(fout):

    # write preamble
    txt = \
        r"""
    % assign conductivity 
    fprintf('assigning fibre conductivity: %3d%%\n', 0);
        """
    fout.write(txt)

    # assign conductivity
    Nsec = 0
    for sec in h.allsec():
        Nsec = Nsec + 1

    secCounter = 0
    for sec in h.allsec():
        secCounter = secCounter + 1
        name = ''.join(e for e in str(sec) if e.isalnum())
        g = 100 / sec.Ra
        txt = \
        r"""
    secName = '%s';
    matName = append('mat', secName);
    model.component('comp1').material.create(matName);
    model.component('comp1').material(matName).materialModel('def').set('electricconductivity', {'%g[S/m]'});
    model.component('comp1').material(matName).selection().set(entityNum(secName));
    fprintf('\b\b\b\b%%3.0f%%%%', %g); pause(0.1);
        """
        fout.write(txt % (name, g, 100*secCounter/Nsec))

    txt = \
        r"""
    fprintf('\n');
    model.save(append(fileparts(matlab.desktop.editor.getActiveFilename), '/NEURON2COMSOL_auto_conv.mph'));
        """
    fout.write(txt)


"""
Mesh the COMSOL model with free tetrahedral elements.
Input:
mesh_size:      int, optional
                mesh resolution: 1 - extremely fine, 2 - extra fine, 3 - finer, 4 - fine, 
                5 - normal, 6 - coarse, 7 - coarser, 8 - extra coarse, 9 - extremely coarse;
                the default is 3 - finer
"""
def mesh(fout, mesh_size=3):

    txt = \
        r"""
    %% fine meshing
    fprintf('meshing ...\n');
    model.component('comp1').mesh.create('mesh1');
    model.component('comp1').mesh('mesh1').feature('size').set('hauto', %g);
    model.component('comp1').mesh('mesh1').create('ftet1', 'FreeTet');
    model.component('comp1').mesh('mesh1').run();
    model.save(append(fileparts(matlab.desktop.editor.getActiveFilename), '/NEURON2COMSOL_auto_conv.mph'));
        """
    fout.write(txt % (mesh_size))


"""
Study the meshed structure to obtain the extracellular voltage profile.
"""
def study(fout):

    txt = \
        r"""
    % study
    fprintf('studying ...\n');
    model.study.create('std');
    model.study('std').feature.create('stat', 'Stationary');
    model.study('std').run;
    data = mpheval(model,{'V'},'selection',1);
    model.save(append(fileparts(matlab.desktop.editor.getActiveFilename), '/NEURON2COMSOL_auto_conv.mph'));
        """
    fout.write(txt)


"""
Export the voltage profile into a .txt file, named exStimVoltProf.txt.
"""
def export(fout):

    txt = \
        r"""
    % export voltage profile
    fprintf('exporting data ...\n');
    model.result.numerical.create('pev1', 'EvalPoint');
    model.result.numerical('pev1').selection.all;
    model.result.export.create('data1', 'Data');
    model.result.export('data1').set('filename', append(fileparts(matlab.desktop.editor.getActiveFilename), ...
        '/exStimVoltProf.txt'));
    model.result.export('data1').setIndex('expr', 'V', 0);
    model.result.export('data1').run;        
        """
    fout.write(txt)


"""
Save the COMSOL model as .mph file, named NEURON2COMSOL_auto_conv.mph.
"""
def writeEpilog(fout):

    txt = \
        r"""
    % save model
    fprintf('saving model ...\n');
    model.save(append(fileparts(matlab.desktop.editor.getActiveFilename), '/NEURON2COMSOL_auto_conv.mph'));
    fprintf('NEURON-to-COMSOL automatic conversion done.\n');
    toc;
        """
    fout.write(txt)


""" 
Master function.
"""
def convert(path2server, path2mph, simBox_3D, simBox_size, nerve_3D, nerve_R, nerve_L, fasc_3D, fasc_R, fasc_L, \
                                substrate_3D, substrate_W, substrate_L, substrate_D, e_R, \
                                e_type="monopolar", e2e_dist=None, rotate_deg=0, simBox_G=1.45, nerve_G=0.01, fasc_G=0.0517, mesh_size=3):
    # write out MATLAB file for COMSOL
    fout = open("./NEURON2COMSOL_auto_conv.m", 'w')
    writePreamble(fout, path2server, path2mph)
    buildSimBox(fout, simBox_3D, simBox_size, simBox_G)
    buildNerve(fout, nerve_3D, nerve_R, nerve_L, nerve_G)
    buildFascicle(fout, fasc_3D, fasc_R, fasc_L, fasc_G)
    buildFibreGeom(fout)
    if e_type == "monopolar":
        buildMonopolarElectrode(fout, substrate_3D, substrate_W, substrate_L, substrate_D, e_R, rotate_deg)
    elif e_type == "hexapolar":
        buildHexapolarElectrode(fout, substrate_3D, substrate_W, substrate_L, substrate_D, e_R, e2e_dist, rotate_deg)
    else:
        print("Incorrect electrode type. Electrode should be either monopolar or hexapolar. Current electrode type is: %s\n" % (e_type))
    getFibreEntityNum(fout)
    assignFibreConductivity(fout)
    mesh(fout, mesh_size)
    study(fout)
    export(fout)
    writeEpilog(fout)
    fout.close()
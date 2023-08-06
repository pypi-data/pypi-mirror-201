from SerpentOut import SerpentOut
from XSParametersReader import XSParametersReader
import Utilities
import numpy as np
import os


def generate_base_files():
    # Creating base xs files
    butot, base_rho, base_t_coolant, base_t_fuel, base_c_b = Utilities.read_burnup_parameters("2eg_neutron_const.base")
    # serpent_results = SerpentOut('./22AU_0_0/22AU_0_0_res.m')
    serpent_base_res = SerpentOut('./22AU_b/22AU_b_res.m')
    xs_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [], 'D_1': [], 'D_2': [],
               'Sa_1': [], 'Sa_2': [], 'nuSf_1': [], 'nuSf_2': [], 'Sf_1': [], 'Sf_2': [], 'S12': [], 'kinf': []}

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        xs_dict['D_1'].append(serpent_base_res.results['CMM_DIFFCOEF '][i][0])
        xs_dict['D_2'].append(serpent_base_res.results['CMM_DIFFCOEF '][i][2])

        xs_dict['Sa_1'].append(serpent_base_res.results['INF_ABS'][i][0])
        xs_dict['Sa_2'].append(serpent_base_res.results['INF_ABS'][i][2])

        xs_dict['nuSf_1'].append(serpent_base_res.results['INF_NSF'][i][0])
        xs_dict['nuSf_2'].append(serpent_base_res.results['INF_NSF'][i][2])

        xs_dict['Sf_1'].append(serpent_base_res.results['INF_FISS '][i][0])
        xs_dict['Sf_2'].append(serpent_base_res.results['INF_FISS '][i][2])

        xs_dict['S12'].append(serpent_base_res.results['INF_S0'][i][2])

        xs_dict['kinf'].append(serpent_base_res.results['ANA_KEFF'][i][0])

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        xs_dict['BURNUP'].append(butot[i])
        xs_dict['RHO'].append(base_rho)
        xs_dict['T_coolant'].append(base_t_coolant)
        xs_dict['T_Fuel'].append(base_t_fuel)
        xs_dict['C_B'].append(base_c_b)

    print(xs_dict)
    print('=======')

    # Writing xs_dict and xsparameters to file
    npoints = len(serpent_base_res.results['CMM_DIFFCOEF '])
    results = np.zeros([npoints, 15])
    for i in range(npoints):
        pass
        results[i][0] = xs_dict['BURNUP'][i]
        results[i][1] = xs_dict['RHO'][i]
        results[i][2] = xs_dict['T_coolant'][i]
        results[i][3] = xs_dict['T_Fuel'][i]
        results[i][4] = xs_dict['C_B'][i]
        results[i][5] = xs_dict['D_1'][i]
        results[i][6] = xs_dict['D_2'][i]
        results[i][7] = xs_dict['Sa_1'][i]
        results[i][8] = xs_dict['Sa_2'][i]
        results[i][9] = xs_dict['nuSf_1'][i]
        results[i][10] = xs_dict['nuSf_2'][i]
        results[i][11] = xs_dict['Sf_1'][i]
        results[i][12] = xs_dict['Sf_2'][i]
        results[i][13] = xs_dict['S12'][i]
        results[i][14] = xs_dict['kinf'][i]
    np.savetxt('xs_22AU_np_base', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            D_1               D_2               Sa_1              '
                      'Sa_2              nuSf_1            nuSf_2            Sf_1              '
                      'Sf_2              s12               kinf',
               delimiter='\t', fmt='%18.8E')

    point_num = 0
    bstep_counter = 0
    burnup_input_file_path = os.path.join(os.getcwd(), '22AU_b', '22AU_b')
    fuel_nuclides = []
    fuel_concentrations = []
    for bstep_counter in range(len(butot)):
        # Checking if *.bumat file exists
        # burnup_folder_path, burnup_input_file_path
        is_burnup_material_file_exists = False
        while not is_burnup_material_file_exists:
            is_burnup_material_file_exists = os.path.isfile(f"{burnup_input_file_path}.bumat{bstep_counter}")
        bumat_file_path = f"{burnup_input_file_path}.bumat{bstep_counter}"

        # Copiing fuel materials from *.bumat file
        fuel_nuclides.append([])
        fuel_concentrations.append([])
        with open(bumat_file_path, 'r') as file:
            bumat_lines = file.readlines()
        for line_num, line in enumerate(bumat_lines):
            if line.startswith("% Material compositions"):
                pass
            elif line.startswith("mat  "):
                for nuclide_counter in range(line_num + 1, len(bumat_lines)):
                    _l = bumat_lines[nuclide_counter].split()
                    fuel_nuclides[bstep_counter].append(_l[0].split('.'[0])[0])
                    fuel_concentrations[bstep_counter].append(float(_l[1]))
                break

    print(fuel_nuclides[0])
    xe_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [], 'XE_abs_xs_1': [], 'XE_abs_xs_2': [],
               'SM_abs_xs_1': [], 'SM_abs_xs_2': [], 'XE_conc': [], 'SM_conc': []}

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        # fiss_rr_abs_1 = serpent_base_res.results['INF_FLX'][i][0] * serpent_base_res.results['INF_FISS '][i][0]
        # fiss_rr_abs_2 = serpent_base_res.results['INF_FLX'][i][2] * serpent_base_res.results['INF_FISS '][i][2]
        # fiss_rr_rel_1 = fiss_rr_abs_1 / (fiss_rr_abs_1 + fiss_rr_abs_2)
        # fiss_rr_rel_2 = fiss_rr_abs_2 / (fiss_rr_abs_1 + fiss_rr_abs_2)
        # xe_abs_xs = serpent_base_res.results['INF_XE135_MICRO_ABS'][i][0] * fiss_rr_rel_1 + \
        #     serpent_base_res.results['INF_XE135_MICRO_ABS'][i][2] * fiss_rr_rel_2
        # sm_abs_xs = serpent_base_res.results['INF_SM149_MICRO_ABS'][i][0] * fiss_rr_rel_1 + \
        #     serpent_base_res.results['INF_SM149_MICRO_ABS'][i][2] * fiss_rr_rel_2
        xe_dict['XE_abs_xs_1'].append(serpent_base_res.results['INF_XE135_MICRO_ABS'][i][0])
        xe_dict['XE_abs_xs_2'].append(serpent_base_res.results['INF_XE135_MICRO_ABS'][i][2])
        xe_dict['SM_abs_xs_1'].append(serpent_base_res.results['INF_SM149_MICRO_ABS'][i][0])
        xe_dict['SM_abs_xs_2'].append(serpent_base_res.results['INF_SM149_MICRO_ABS'][i][2])

        xe_nuclide_num = 0
        sm_nuclide_num = 0
        for j in range(len(fuel_nuclides[i])):
            if fuel_nuclides[i][j] == '54135':
                xe_nuclide_num = j
                # print(j, fuel_nuclides[i][j], fuel_concentrations[i][j])
            elif fuel_nuclides[i][j] == '62149':
                sm_nuclide_num = j
        if xe_nuclide_num != 0:
            xe_dict['XE_conc'].append(fuel_concentrations[i][xe_nuclide_num])
            xe_dict['SM_conc'].append(fuel_concentrations[i][sm_nuclide_num])
        else:
            xe_dict['XE_conc'].append(np.NAN)
            xe_dict['SM_conc'].append(np.NAN)

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        xe_dict['BURNUP'].append(butot[i])
        xe_dict['RHO'].append(base_rho)
        xe_dict['T_coolant'].append(base_t_coolant)
        xe_dict['T_Fuel'].append(base_t_fuel)
        xe_dict['C_B'].append(base_c_b)

    # Writing xe_dict and xsparameters to file
    npoints = len(serpent_base_res.results['CMM_DIFFCOEF '])
    results = np.zeros([npoints, 11])
    for i in range(npoints):
        pass
        results[i][0] = xe_dict['BURNUP'][i]
        results[i][1] = xe_dict['RHO'][i]
        results[i][2] = xe_dict['T_coolant'][i]
        results[i][3] = xe_dict['T_Fuel'][i]
        results[i][4] = xe_dict['C_B'][i]
        results[i][5] = xe_dict['XE_abs_xs_1'][i]
        results[i][6] = xe_dict['XE_abs_xs_2'][i]
        results[i][7] = xe_dict['SM_abs_xs_1'][i]
        results[i][8] = xe_dict['SM_abs_xs_2'][i]
        results[i][9] = xe_dict['XE_conc'][i]
        results[i][10] = xe_dict['SM_conc'][i]
    np.savetxt('xe_22AU_np_base', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            XE_abs_xs_1            XE_abs_xs_2               SM_abs_xs_1               '
                      '               SM_abs_xs_2           XE_conc              SM_conc',
               delimiter='\t', fmt='%18.8E')

    '================================='
    xkin_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [],
                 'beta': [], 'beta_1': [], 'beta_2': [], 'beta_3': [], 'beta_4': [], 'beta_5': [], 'beta_6': [],
                 'lambda_1': [], 'lambda_2': [], 'lambda_3': [], 'lambda_4': [], 'lambda_5': [], 'lambda_6': [],
                 '1/v_1': [], '1/v_2': []}

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        xkin_dict['beta'].append(serpent_base_res.results['BETA_EFF'][i][0])
        xkin_dict['beta_1'].append(serpent_base_res.results['BETA_EFF'][i][2])
        xkin_dict['beta_2'].append(serpent_base_res.results['BETA_EFF'][i][4])
        xkin_dict['beta_3'].append(serpent_base_res.results['BETA_EFF'][i][6])
        xkin_dict['beta_4'].append(serpent_base_res.results['BETA_EFF'][i][8])
        xkin_dict['beta_5'].append(serpent_base_res.results['BETA_EFF'][i][10])
        xkin_dict['beta_6'].append(serpent_base_res.results['BETA_EFF'][i][12])

        xkin_dict['lambda_1'].append(serpent_base_res.results['LAMBDA '][i][2])
        xkin_dict['lambda_2'].append(serpent_base_res.results['LAMBDA '][i][4])
        xkin_dict['lambda_3'].append(serpent_base_res.results['LAMBDA '][i][6])
        xkin_dict['lambda_4'].append(serpent_base_res.results['LAMBDA '][i][8])
        xkin_dict['lambda_5'].append(serpent_base_res.results['LAMBDA '][i][10])
        xkin_dict['lambda_6'].append(serpent_base_res.results['LAMBDA '][i][12])

        xkin_dict['1/v_1'].append(serpent_base_res.results['INF_INVV'][i][0])
        xkin_dict['1/v_2'].append(serpent_base_res.results['INF_INVV'][i][2])

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        xkin_dict['BURNUP'].append(butot[i])
        xkin_dict['RHO'].append(base_rho)
        xkin_dict['T_coolant'].append(base_t_coolant)
        xkin_dict['T_Fuel'].append(base_t_fuel)
        xkin_dict['C_B'].append(base_c_b)

    print(xs_dict)
    print('=======')

    # Writing xs_dict and xsparameters to file
    npoints = len(serpent_base_res.results['CMM_DIFFCOEF '])
    results = np.zeros([npoints, 20])
    for i in range(npoints):
        pass
        results[i][0] = xkin_dict['BURNUP'][i]
        results[i][1] = xkin_dict['RHO'][i]
        results[i][2] = xkin_dict['T_coolant'][i]
        results[i][3] = xkin_dict['T_Fuel'][i]
        results[i][4] = xkin_dict['C_B'][i]
        results[i][5] = xkin_dict['beta'][i]
        results[i][6] = xkin_dict['beta_1'][i]
        results[i][7] = xkin_dict['beta_2'][i]
        results[i][8] = xkin_dict['beta_3'][i]
        results[i][9] = xkin_dict['beta_4'][i]
        results[i][10] = xkin_dict['beta_5'][i]
        results[i][11] = xkin_dict['beta_6'][i]
        results[i][12] = xkin_dict['lambda_1'][i]
        results[i][13] = xkin_dict['lambda_2'][i]
        results[i][14] = xkin_dict['lambda_3'][i]
        results[i][15] = xkin_dict['lambda_4'][i]
        results[i][16] = xkin_dict['lambda_5'][i]
        results[i][17] = xkin_dict['lambda_6'][i]
        results[i][18] = xkin_dict['1/v_1'][i]
        results[i][19] = xkin_dict['1/v_2'][i]
    np.savetxt('xkin_22AU_np_base', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            beta               beta_1               beta_2              '
                      'beta_3              beta_4            beta_5            beta_6              '
                      'lambda_1              lambda2            lambda_3            lambda_4              '
                      'lambda_5              lambda_6               1/v_1               1/v_2',
               delimiter='', fmt='%18.8E')

    '================================='
    xye_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [], 'i135_ye': [], 'xe135_ye': [],
                'pm149_ye': []}

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        fiss_rr_abs_1 = serpent_base_res.results['INF_FLX'][i][0] * serpent_base_res.results['INF_FISS '][i][0]
        fiss_rr_abs_2 = serpent_base_res.results['INF_FLX'][i][2] * serpent_base_res.results['INF_FISS '][i][2]
        fiss_rr_rel_1 = fiss_rr_abs_1 / (fiss_rr_abs_1 + fiss_rr_abs_2)
        fiss_rr_rel_2 = fiss_rr_abs_2 / (fiss_rr_abs_1 + fiss_rr_abs_2)
        i135_ye = serpent_base_res.results['INF_I135_YIELD'][i][0] * fiss_rr_rel_1 + \
            serpent_base_res.results['INF_I135_YIELD'][i][2] * fiss_rr_rel_2
        xe135_ye = serpent_base_res.results['INF_XE135_YIELD'][i][0] * fiss_rr_rel_1 + \
                  serpent_base_res.results['INF_XE135_YIELD'][i][2] * fiss_rr_rel_2
        pm149_ye = serpent_base_res.results['INF_PM149_YIELD'][i][0] * fiss_rr_rel_1 + \
            serpent_base_res.results['INF_PM149_YIELD'][i][2] * fiss_rr_rel_2
        xye_dict['i135_ye'].append(i135_ye)
        xye_dict['xe135_ye'].append(xe135_ye)
        xye_dict['pm149_ye'].append(pm149_ye)

    for i in range(len(serpent_base_res.results['CMM_DIFFCOEF '])):
        xye_dict['BURNUP'].append(butot[i])
        xye_dict['RHO'].append(base_rho)
        xye_dict['T_coolant'].append(base_t_coolant)
        xye_dict['T_Fuel'].append(base_t_fuel)
        xye_dict['C_B'].append(base_c_b)

    print('=======')

    # Writing xs_dict and xsparameters to file
    npoints = len(serpent_base_res.results['CMM_DIFFCOEF '])
    results = np.zeros([npoints, 8])
    for i in range(npoints):
        pass
        results[i][0] = xye_dict['BURNUP'][i]
        results[i][1] = xye_dict['RHO'][i]
        results[i][2] = xye_dict['T_coolant'][i]
        results[i][3] = xye_dict['T_Fuel'][i]
        results[i][4] = xye_dict['C_B'][i]
        results[i][5] = xye_dict['i135_ye'][i]
        results[i][6] = xye_dict['xe135_ye'][i]
        results[i][7] = xye_dict['pm149_ye'][i]

    np.savetxt('xye_22AU_np_base', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            i135_ye               xe135_ye               pm149_ye              ',
               delimiter='', fmt='%18.8E')


def generate_variation_files():
    # Creates an array of the parameters, used for xs library generation
    xsreader = XSParametersReader("lptau_ro_05.DAT", 1024)
    for point in xsreader.points_array:
        print(point)
    curr_dir = os.getcwd()
    files_list = os.listdir()
    calculation_prefix = '22AU_'
    calc_folders_list = Utilities.filter_calculation_folders(files_list, calculation_prefix)

    calc_folders_list.sort(key=Utilities.int_val_2d)
    print(calc_folders_list)

    butot, base_rho, base_t_coolant, base_t_fuel, base_c_b = Utilities.read_burnup_parameters("2eg_neutron_const.base")

    xs_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [], 'D_1': [], 'D_2': [],
               'Sa_1': [], 'Sa_2': [], 'nuSf_1': [], 'nuSf_2': [], 'Sf_1': [], 'Sf_2': [], 'S12': [], 'kinf': []}

    xe_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [], 'XE_abs_xs_1': [], 'XE_abs_xs_2': [],
               'SM_abs_xs_1': [], 'SM_abs_xs_2': [], 'XE_conc': [], 'SM_conc': []}

    xkin_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [],
                 'beta': [], 'beta_1': [], 'beta_2': [], 'beta_3': [], 'beta_4': [], 'beta_5': [], 'beta_6': [],
                 'lambda_1': [], 'lambda_2': [], 'lambda_3': [], 'lambda_4': [], 'lambda_5': [], 'lambda_6': [],
                 '1/v_1': [], '1/v_2': []}

    xye_dict = {'BURNUP': [], 'RHO': [], 'T_coolant': [], 'T_Fuel': [], 'C_B': [], 'i135_ye': [], 'xe135_ye': [],
                'pm149_ye': []}

    point_num = 0
    npoints = 4
    for i in range(len(butot)):
        for j in range(npoints):
            if os.path.exists(f'./22AU_{i}_{j}/22AU_{i}_{j}_res.m'):
                serpent_res = SerpentOut(f'./22AU_{i}_{j}/22AU_{i}_{j}_res.m')
            else:
                raise FileNotFoundError(f'File ./22AU_{i}_{j}/22AU_{i}_{j}_res.m not found')

            xs_dict['D_1'].append(serpent_res.results['CMM_DIFFCOEF '][0][0])
            xs_dict['D_2'].append(serpent_res.results['CMM_DIFFCOEF '][0][2])
            xs_dict['Sa_1'].append(serpent_res.results['INF_ABS'][0][0])
            xs_dict['Sa_2'].append(serpent_res.results['INF_ABS'][0][2])
            xs_dict['nuSf_1'].append(serpent_res.results['INF_NSF'][0][0])
            xs_dict['nuSf_2'].append(serpent_res.results['INF_NSF'][0][2])
            xs_dict['Sf_1'].append(serpent_res.results['INF_FISS '][0][0])
            xs_dict['Sf_2'].append(serpent_res.results['INF_FISS '][0][2])
            xs_dict['S12'].append(serpent_res.results['INF_S0'][0][2])
            xs_dict['kinf'].append(serpent_res.results['ANA_KEFF'][0][0])

            xs_dict['BURNUP'].append(butot[i])
            xs_dict['RHO'].append(xsreader.points_array[point_num]['RHO'])
            xs_dict['T_coolant'].append(xsreader.points_array[point_num]['T_coolant'])
            xs_dict['T_Fuel'].append(xsreader.points_array[point_num]['T_Fuel'])
            xs_dict['C_B'].append(xsreader.points_array[point_num]['C_B'])

            # xe dict
            xe_dict['XE_abs_xs_1'].append(serpent_res.results['INF_XE135_MICRO_ABS'][0][0])
            xe_dict['XE_abs_xs_2'].append(serpent_res.results['INF_XE135_MICRO_ABS'][0][2])
            xe_dict['SM_abs_xs_1'].append(serpent_res.results['INF_SM149_MICRO_ABS'][0][0])
            xe_dict['SM_abs_xs_2'].append(serpent_res.results['INF_SM149_MICRO_ABS'][0][2])

            burnup_input_file_path = os.path.join(os.getcwd(), '22AU_b', '22AU_b')
            fuel_nuclides = []
            fuel_concentrations = []
            is_burnup_material_file_exists = False
            while not is_burnup_material_file_exists:
                is_burnup_material_file_exists = os.path.isfile(f"{burnup_input_file_path}.bumat{i}")
            bumat_file_path = f"{burnup_input_file_path}.bumat{i}"
            # Copiing fuel materials from *.bumat file
            with open(bumat_file_path, 'r') as file:
                bumat_lines = file.readlines()
            for line_num, line in enumerate(bumat_lines):
                if line.startswith("% Material compositions"):
                    pass
                elif line.startswith("mat  "):
                    for nuclide_counter in range(line_num + 1, len(bumat_lines)):
                        _l = bumat_lines[nuclide_counter].split()
                        fuel_nuclides.append(_l[0].split('.'[0])[0])
                        fuel_concentrations.append(float(_l[1]))
                    break

            xe_nuclide_num = 0
            sm_nuclide_num = 0
            for nucl in range(len(fuel_nuclides)):
                if fuel_nuclides[nucl] == '54135':
                    xe_nuclide_num = nucl
                    # print(j, fuel_nuclides[i][j], fuel_concentrations[i][j])
                elif fuel_nuclides[nucl] == '62149':
                    sm_nuclide_num = nucl
            if xe_nuclide_num != 0:
                xe_dict['XE_conc'].append(fuel_concentrations[xe_nuclide_num])
                xe_dict['SM_conc'].append(fuel_concentrations[sm_nuclide_num])
            else:
                xe_dict['XE_conc'].append(np.NAN)
                xe_dict['SM_conc'].append(np.NAN)

            xe_dict['BURNUP'].append(butot[i])
            xe_dict['RHO'].append(xsreader.points_array[point_num]['RHO'])
            xe_dict['T_coolant'].append(xsreader.points_array[point_num]['T_coolant'])
            xe_dict['T_Fuel'].append(xsreader.points_array[point_num]['T_Fuel'])
            xe_dict['C_B'].append(xsreader.points_array[point_num]['C_B'])

            # xkin dict
            xkin_dict['beta'].append(serpent_res.results['BETA_EFF'][0][0])
            xkin_dict['beta_1'].append(serpent_res.results['BETA_EFF'][0][2])
            xkin_dict['beta_2'].append(serpent_res.results['BETA_EFF'][0][4])
            xkin_dict['beta_3'].append(serpent_res.results['BETA_EFF'][0][6])
            xkin_dict['beta_4'].append(serpent_res.results['BETA_EFF'][0][8])
            xkin_dict['beta_5'].append(serpent_res.results['BETA_EFF'][0][10])
            xkin_dict['beta_6'].append(serpent_res.results['BETA_EFF'][0][12])
            xkin_dict['lambda_1'].append(serpent_res.results['LAMBDA '][0][2])
            xkin_dict['lambda_2'].append(serpent_res.results['LAMBDA '][0][4])
            xkin_dict['lambda_3'].append(serpent_res.results['LAMBDA '][0][6])
            xkin_dict['lambda_4'].append(serpent_res.results['LAMBDA '][0][8])
            xkin_dict['lambda_5'].append(serpent_res.results['LAMBDA '][0][10])
            xkin_dict['lambda_6'].append(serpent_res.results['LAMBDA '][0][12])
            xkin_dict['1/v_1'].append(serpent_res.results['INF_INVV'][0][0])
            xkin_dict['1/v_2'].append(serpent_res.results['INF_INVV'][0][2])

            xkin_dict['BURNUP'].append(butot[i])
            xkin_dict['RHO'].append(xsreader.points_array[point_num]['RHO'])
            xkin_dict['T_coolant'].append(xsreader.points_array[point_num]['T_coolant'])
            xkin_dict['T_Fuel'].append(xsreader.points_array[point_num]['T_Fuel'])
            xkin_dict['C_B'].append(xsreader.points_array[point_num]['C_B'])

            # xye_dict
            fiss_rr_abs_1 = serpent_res.results['INF_FLX'][0][0] * serpent_res.results['INF_FISS '][0][0]
            fiss_rr_abs_2 = serpent_res.results['INF_FLX'][0][2] * serpent_res.results['INF_FISS '][0][2]
            fiss_rr_rel_1 = fiss_rr_abs_1 / (fiss_rr_abs_1 + fiss_rr_abs_2)
            fiss_rr_rel_2 = fiss_rr_abs_2 / (fiss_rr_abs_1 + fiss_rr_abs_2)
            i135_ye = serpent_res.results['INF_I135_YIELD'][0][0] * fiss_rr_rel_1 + \
                      serpent_res.results['INF_I135_YIELD'][0][2] * fiss_rr_rel_2
            xe135_ye = serpent_res.results['INF_XE135_YIELD'][0][0] * fiss_rr_rel_1 + \
                       serpent_res.results['INF_XE135_YIELD'][0][2] * fiss_rr_rel_2
            pm149_ye = serpent_res.results['INF_PM149_YIELD'][0][0] * fiss_rr_rel_1 + \
                       serpent_res.results['INF_PM149_YIELD'][0][2] * fiss_rr_rel_2
            xye_dict['i135_ye'].append(i135_ye)
            xye_dict['xe135_ye'].append(xe135_ye)
            xye_dict['pm149_ye'].append(pm149_ye)

            xye_dict['BURNUP'].append(butot[i])
            xye_dict['RHO'].append(xsreader.points_array[point_num]['RHO'])
            xye_dict['T_coolant'].append(xsreader.points_array[point_num]['T_coolant'])
            xye_dict['T_Fuel'].append(xsreader.points_array[point_num]['T_Fuel'])
            xye_dict['C_B'].append(xsreader.points_array[point_num]['C_B'])

            point_num += 1
            pass
        pass

    # Writing xs_dict and xsparameters to file
    npoints = len(xs_dict['D_1'])
    results = np.zeros([npoints, 15])
    for i in range(npoints):
        pass
        results[i][0] = xs_dict['BURNUP'][i]
        results[i][1] = xs_dict['RHO'][i]
        results[i][2] = xs_dict['T_coolant'][i]
        results[i][3] = xs_dict['T_Fuel'][i]
        results[i][4] = xs_dict['C_B'][i]
        results[i][5] = xs_dict['D_1'][i]
        results[i][6] = xs_dict['D_2'][i]
        results[i][7] = xs_dict['Sa_1'][i]
        results[i][8] = xs_dict['Sa_2'][i]
        results[i][9] = xs_dict['nuSf_1'][i]
        results[i][10] = xs_dict['nuSf_2'][i]
        results[i][11] = xs_dict['Sf_1'][i]
        results[i][12] = xs_dict['Sf_2'][i]
        results[i][13] = xs_dict['S12'][i]
        results[i][14] = xs_dict['kinf'][i]
    np.savetxt('xs_22AU_np_var', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            D_1               D_2               Sa_1              '
                      'Sa_2              nuSf_1            nuSf_2            Sf_1              '
                      'Sf_2              s12               kinf',
               delimiter='\t', fmt='%18.8E')

    results = np.zeros([npoints, 11])
    for i in range(npoints):
        pass
        results[i][0] = xe_dict['BURNUP'][i]
        results[i][1] = xe_dict['RHO'][i]
        results[i][2] = xe_dict['T_coolant'][i]
        results[i][3] = xe_dict['T_Fuel'][i]
        results[i][4] = xe_dict['C_B'][i]
        results[i][5] = xe_dict['XE_abs_xs_1'][i]
        results[i][6] = xe_dict['XE_abs_xs_2'][i]
        results[i][7] = xe_dict['SM_abs_xs_1'][i]
        results[i][8] = xe_dict['SM_abs_xs_2'][i]
        results[i][9] = xe_dict['XE_conc'][i]
        results[i][10] = xe_dict['SM_conc'][i]
    np.savetxt('xe_22AU_np_var', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            XE_abs_xs_1            XE_abs_xs_2               SM_abs_xs_1               '
                      '               SM_abs_xs_2           XE_conc              SM_conc',
               delimiter='\t', fmt='%18.8E')

    results = np.zeros([npoints, 20])
    for i in range(npoints):
        pass
        results[i][0] = xkin_dict['BURNUP'][i]
        results[i][1] = xkin_dict['RHO'][i]
        results[i][2] = xkin_dict['T_coolant'][i]
        results[i][3] = xkin_dict['T_Fuel'][i]
        results[i][4] = xkin_dict['C_B'][i]
        results[i][5] = xkin_dict['beta'][i]
        results[i][6] = xkin_dict['beta_1'][i]
        results[i][7] = xkin_dict['beta_2'][i]
        results[i][8] = xkin_dict['beta_3'][i]
        results[i][9] = xkin_dict['beta_4'][i]
        results[i][10] = xkin_dict['beta_5'][i]
        results[i][11] = xkin_dict['beta_6'][i]
        results[i][12] = xkin_dict['lambda_1'][i]
        results[i][13] = xkin_dict['lambda_2'][i]
        results[i][14] = xkin_dict['lambda_3'][i]
        results[i][15] = xkin_dict['lambda_4'][i]
        results[i][16] = xkin_dict['lambda_5'][i]
        results[i][17] = xkin_dict['lambda_6'][i]
        results[i][18] = xkin_dict['1/v_1'][i]
        results[i][19] = xkin_dict['1/v_2'][i]
    np.savetxt('xkin_22AU_np_var', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            beta               beta_1               beta_2              '
                      'beta_3              beta_4            beta_5            beta_6              '
                      'lambda_1              lambda2            lambda_3            lambda_4              '
                      'lambda_5              lambda_6               1/v_1               1/v_2',
               delimiter='', fmt='%18.8E')

    results = np.zeros([npoints, 8])
    for i in range(npoints):
        pass
        results[i][0] = xye_dict['BURNUP'][i]
        results[i][1] = xye_dict['RHO'][i]
        results[i][2] = xye_dict['T_coolant'][i]
        results[i][3] = xye_dict['T_Fuel'][i]
        results[i][4] = xye_dict['C_B'][i]
        results[i][5] = xye_dict['i135_ye'][i]
        results[i][6] = xye_dict['xe135_ye'][i]
        results[i][7] = xye_dict['pm149_ye'][i]

    np.savetxt('xye_22AU_np_var', results,
               header='BURNUP               RHO               T_coolant         T_Fuel            '
                      'C_B ppm            i135_ye               xe135_ye               pm149_ye              ',
               delimiter='', fmt='%18.8E')
    pass


if __name__ == '__main__':
    # Creates an array of the parameters, used for xs library generation
    # xsreader = XSParametersReader("lptau_ro_05.DAT", 1024)
    generate_base_files()
    generate_variation_files()
    pass



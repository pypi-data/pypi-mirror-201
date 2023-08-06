import shutil
import subprocess
import os
import Parameters
from Material import Material


def calculate_water_concentrations(h2o_dens=0.7235, boric_acid_ppm=600):
    avagadro = 0.6022045
    aem = 1.66057
    h2o_m = 18.01528
    cof = 1. / (aem * h2o_m)
    c10x = 0.1974
    c11x = 0.8026
    gamma = 0.013
    nh2o = h2o_dens * avagadro / h2o_m
    dop = 1.e-6 * cof * h2o_dens * boric_acid_ppm * h2o_m / (10. * c10x + 11. * c11x)
    cb10_atoms = dop * c10x * (1 - gamma)
    cb11_atoms = dop * c11x * (1 - gamma)
    h_atoms = (3 * dop + 2 * nh2o) * (1 - gamma)
    o_atoms = (1 - gamma) * (nh2o + 3 * dop)
    return h_atoms, o_atoms, cb10_atoms, cb11_atoms


def checkout(command: str, arg: str) -> str:
    stdout = subprocess.check_output([command, arg])
    stdout = stdout.decode("utf-16")
    return stdout


def divide_out_to_lines(stdout: str) -> list[list]:
    """
    Works for MEPhI hpc cluster Senpai (SLURM queue system)
    Divides stdout to the list of lines, each line also divided by words
    Returns list of lines
    """
    lines = stdout.split("\n")
    del lines[-1]
    for i in range(len(lines)):
        lines[i] = lines[i].split()
    return lines


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_file(original_path, target_path):
    if os.path.exists(original_path):
        shutil.copyfile(original_path, target_path)
    else:
        raise OSError(f"File {original_path} does not exist")


def int_val(string):
    val = int(string.split('_')[-1])
    return val


def filter_calculation_folders(files_list: list[str], calculation_prefix: str) -> list[str]:
    calc_folders_list = []
    for file in files_list:
        file_path = os.path.join(os.getcwd(), file)
        if os.path.isdir(file_path):
            if file.startswith(calculation_prefix):
                calc_folders_list.append(file_path)
    # calc_folders_list.sort(key=__class__.int_val)
    return calc_folders_list


def read_burnup_parameters(filename):
    with open(filename, 'r') as file:
        base_lines = file.readlines()
    butot = []
    rho = None
    t_coolant = None
    t_fuel = None
    c_b = None
    for i in range(1, len(base_lines)):
        splited_line = base_lines[i].split()
        butot.append(float(splited_line[0]))
        if i == 1:
            rho = float(splited_line[1])
            t_coolant = float(splited_line[2])
            t_fuel = float(splited_line[3])
            c_b = float(splited_line[4])
    return butot, rho, t_coolant, t_fuel, c_b


def set_file_path_and_copy(new_folder_name: str, original_input_file_name: str):
    cur_path = os.getcwd()
    new_folder_path = os.path.join(cur_path, new_folder_name)
    print(f'Burnup calculation directory: {new_folder_path}')
    create_folder(new_folder_path)

    # Copying needed files
    # Input file
    original_input_file_path = os.path.join(cur_path, original_input_file_name)
    target_input_file_path = os.path.join(new_folder_path, new_folder_name)
    copy_file(original_input_file_path, target_input_file_path)

    # lwtr file
    original_lwtr_file_path = os.path.join(cur_path, "lwtr")
    target_lwtr_file_path = os.path.join(new_folder_path, "lwtr")
    copy_file(original_lwtr_file_path, target_lwtr_file_path)

    # run.sh file
    original_sh_file_path = os.path.join(cur_path, "run.sh")
    target_sh_file_path = os.path.join(new_folder_path, "run.sh")
    copy_file(original_sh_file_path, target_sh_file_path)

    # cells file
    original_cells_file_path = os.path.join(cur_path, "22AU_cells")
    target_cells_file_path = os.path.join(new_folder_path, "22AU_cells")
    copy_file(original_cells_file_path, target_cells_file_path)

    # pins file
    original_pins_file_path = os.path.join(cur_path, "22AU_pins")
    target_pins_file_path = os.path.join(new_folder_path, "22AU_pins")
    copy_file(original_pins_file_path, target_pins_file_path)

    # print section
    print(f"Creating input files")
    print(f"Current path = {cur_path}")
    print(f"Calculation folder path = {new_folder_path}")
    print(f"Calculation input file path = {target_input_file_path}")
    print(f"Calculation lwtr file path = {target_lwtr_file_path}")
    print(f"Calculation run.sh file path = {target_sh_file_path}")
    return cur_path, new_folder_path, target_input_file_path, target_lwtr_file_path, target_sh_file_path


def change_sh_file(target_sh_file_path, target_input_file_path):
    with open(target_sh_file_path, 'r') as file:
        sh_lines = file.readlines()
    for j, line in enumerate(sh_lines):
        if line.startswith('/home/SHARED/Serpent'):
            l = line.split()
            l[-1] = target_input_file_path
            sh_lines[j] = " ".join(l)
            # sh_lines[j] = sh_lines[j] + f" out>>{stdout_file_path}"
    with open(target_sh_file_path, 'w') as file:
        file.writelines(sh_lines)


def create_burnup_parameters_file(new_folder_path, burnup_parameters_file_name, powdens, butot):
    with open(os.path.join(new_folder_path, burnup_parameters_file_name), 'w') as file:
        file.write(f'set powdens {powdens}\n')
        file.write(f'dep butot\n')
        for i, b_step in enumerate(butot):
            if i > 0:
                file.write(f'{b_step:18.8E}\n')
        file.write(f'set pcc leli 10 10\n')
        file.write(f'set inventory all\n')
        file.write(f'set printm 1\n')


def create_fuel_materials_for_all_pins(
        fuel_nuclides: list,
        fuel_concentrations: list,
        temp: float,
        burn=1,
        nuclides_format="Mendeleev_table"
) -> list:
    fuel_materials = []
    for i in range(Parameters.VVER_1000_number_of_pins):
        gc = False
        cc = False
        for j in range(len(Parameters.VVER_1000_guide_channels_numbers)):
            if i + 1 == Parameters.VVER_1000_guide_channels_numbers[j]:
                gc = True

        for j in range(len(Parameters.VVER_1000_central_guide_channels_numbers)):
            if i + 1 == Parameters.VVER_1000_central_guide_channels_numbers[j]:
                cc = True

        if (not gc) and (not cc):
            fuel_material = Material(
                name=f'fu_Fuel_{i + 1:03}',
                nuclides=fuel_nuclides,
                concentrations=fuel_concentrations,
                burn=burn,
                temp=temp,
                is_fuel=True,
                nuclides_format=nuclides_format
            )
            fuel_materials.append(fuel_material)
    return fuel_materials


def create_bumat_fuel_materials_for_all_pins(
        fuel_materials_nuclides_and_concentrations: dict,
        temp: float,
        burn=1,
        nuclides_format="Mendeleev_table"
) -> list:
    fuel_materials = []
    for i in range(Parameters.VVER_1000_number_of_pins):
        gc = False
        cc = False
        for j in range(len(Parameters.VVER_1000_guide_channels_numbers)):
            if i + 1 == Parameters.VVER_1000_guide_channels_numbers[j]:
                gc = True

        for j in range(len(Parameters.VVER_1000_central_guide_channels_numbers)):
            if i + 1 == Parameters.VVER_1000_central_guide_channels_numbers[j]:
                cc = True

        if (not gc) and (not cc):
            fuel_material = Material(
                name=f'fu_Fuel_{i + 1:03}',
                nuclides=fuel_materials_nuclides_and_concentrations[i + 1][0],
                concentrations=fuel_materials_nuclides_and_concentrations[i + 1][1],
                burn=burn,
                temp=temp,
                is_fuel=True,
                nuclides_format=nuclides_format
            )
            fuel_materials.append(fuel_material)
    return fuel_materials


def read_bumat_file_for_all_pins(
        bumat_file_path: str
) -> (dict, str):
    # Copiing fuel materials from *.bumat file
    with open(bumat_file_path, 'r') as file:
        bumat_lines = file.readlines()
    fuel_materials_nuclides_and_concentrations = {}

    burnup_serpent = 'None'
    for line_num, line in enumerate(bumat_lines):
        if line.startswith("% Material compositions"):
            burnup_serpent = line.split('(')[-1][:-1]
            break

    # get indexes (lines numbers) for all start lines for each material
    indexes = [i for i, line in enumerate(bumat_lines) if line.startswith("mat  fu_Fuel_")]

    for ind_num, ind in enumerate(indexes):
        fuel_nuclides = []
        fuel_concentrations = []

        _f_name_line = bumat_lines[ind]
        _f = _f_name_line.split()[1]
        # print(_f_name_line)
        # print(_f.split('_')[2])
        _f_num = int(_f.split('_')[2][0:3])
        fuel_materials_nuclides_and_concentrations[_f_num] = []
        if ind_num != len(indexes) - 1:
            for nuclide_counter in range(0, indexes[ind_num + 1] - (ind + 1)):
                _l = bumat_lines[ind + 1 + nuclide_counter].split()
                fuel_nuclides.append(_l[0].split('.'[0])[0])
                fuel_concentrations.append(float(_l[1]))
            fuel_materials_nuclides_and_concentrations[_f_num].append(fuel_nuclides)
            fuel_materials_nuclides_and_concentrations[_f_num].append(fuel_concentrations)
        else:
            for nuclide_counter in range(0, len(bumat_lines) - (ind + 1)):
                _l = bumat_lines[ind + 1 + nuclide_counter].split()
                fuel_nuclides.append(_l[0].split('.'[0])[0])
                fuel_concentrations.append(float(_l[1]))
            fuel_materials_nuclides_and_concentrations[_f_num].append(fuel_nuclides)
            fuel_materials_nuclides_and_concentrations[_f_num].append(fuel_concentrations)

    # print(fuel_materials_nuclides_and_concentrations)
    # input()

    # for line_num, line in enumerate(bumat_lines):
    #     if line.startswith("% Material compositions"):
    #         burnup_serpent = line.split('(')[-1][:-1]
    #     elif line.startswith("mat  "):
    #         for nuclide_counter in range(line_num + 1, len(bumat_lines)):
    #             _l = bumat_lines[nuclide_counter].split()
    #             fuel_nuclides.append(_l[0].split('.'[0])[0])
    #             fuel_concentrations.append(float(_l[1]))
    #         # print(fuel_nuclides)
    #         # print(fuel_concentrations)
    #         break
    return fuel_materials_nuclides_and_concentrations, burnup_serpent


if __name__ == '__main__':
    fuel_materials_nuclides_and_concentrations, burnup_serpent = read_bumat_file_for_all_pins('22AU_312_b.bumat1')
    f_mats = create_bumat_fuel_materials_for_all_pins(
        fuel_materials_nuclides_and_concentrations, 100.0, burn=1, nuclides_format="Serpent"
    )
    with open('fffuel_materials', 'w') as file:
        for mat in f_mats:
            mat.write_to_file(file)

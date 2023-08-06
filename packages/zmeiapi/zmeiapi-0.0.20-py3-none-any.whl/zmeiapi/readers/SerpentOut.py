from zmeiapi.zmei_io.Logger import logger


class OutReader:
    def __init__(self, out_filename):
        self.out_filename = out_filename
        with open(self.out_filename, 'r') as file:
            self.lines = file.readlines()

        self.blines = []
        self.bresults = []

        self.results = {
            'ANA_KEFF': [],
            'IMP_KEFF': [],
            'INF_FLX': [],
            # xs results
            'MACRO_NG': [],
            'MACRO_E': [],
            'INF_ABS': [],
            'INF_FISS ': [],
            'INF_NSF': [],
            'INF_S0': [],
            'CMM_DIFFCOEF ': [],
            'INF_I135_YIELD': [],
            'INF_XE135_YIELD': [],
            'INF_PM149_YIELD': [],
            'INF_XE135_MICRO_ABS': [],
            'INF_SM149_MICRO_ABS': [],
            'INF_INVV': [],
            'BETA_EFF': [],
            'LAMBDA ': [],
            'BURN_STEP': [],
            'BURNUP ': [],
            'BURN_DAYS': []
        }

        self.divide_file_to_burnup_steps()
        # '''
        for bstep, lines in enumerate(self.blines):

            for key in self.results.keys():
                self.results[key].append([])

            for line in self.blines[bstep]:
                for key in self.results.keys():
                    if line.startswith(key):
                        splited_line = line.split('=')
                        res_line = splited_line[-1].split()
                        if key == 'MACRO_NG':
                            self.results[key][bstep].append(res_line[0])
                            # print(key, self.results[key])
                        elif key == 'BURN_STEP':
                            self.results[key][bstep].append(res_line[0])
                        else:
                            # print(self.results[key])
                            self.results[key][bstep].append(res_line[1:-1])
                            self.results[key][bstep] = self.results[key][bstep][0]
                            # print(key, self.results[key])
            # self.bresults.append(self.results)

        self.results_to_float()
        # self.print_res()
        # '''

        pass

    def divide_file_to_burnup_steps(self):
        with open(self.out_filename, 'r') as file:
            lines = file.read()
        self.blines = lines.split('% Increase counter:')[1:]
        for i, part in enumerate(self.blines):
            self.blines[i] = part.split('\n')
        pass

    def results_to_float(self):
        # print(len(self.results))
        for key in self.results.keys():
            for bstep in range(len(self.results['ANA_KEFF'])):
                for i, el in enumerate(self.results[key][bstep]):
                    # pass
                    self.results[key][bstep][i] = float(el)

    def print_res(self):
        for key in self.results.keys():
            print(key, self.results[key])


if __name__ == '__main__':
    serpent_results = OutReader('./22AU_0_0/22AU_0_0_res.m')
    # serpent_results = SerpentOut('./22AU_b_res.m')
    print(len(serpent_results.bresults))
    # for result in serpent_results.results:
    for key in serpent_results.results.keys():
        print(key, serpent_results.results[key])
    print('=======')

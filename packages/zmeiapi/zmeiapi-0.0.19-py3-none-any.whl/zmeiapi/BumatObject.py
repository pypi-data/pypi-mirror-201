__version__ = '0.0.1'
__author__ = 'Vlad Romanenko'


class BumatMaterialObject:
    def __init__(
            self,
            material_name,
            burnup,
            burnup_days,
            concentrations_sum,
            vol,
            nuclides,
            concentrations
    ):
        self.burnup = burnup
        self.burnup_days = burnup_days
        self.material_name = material_name
        self.concentrations_sum = concentrations_sum
        self.vol = vol

        self.nuclides = nuclides
        self.concentrations = concentrations

        self.nuclides_and_concentrations = {}
        for nuclide, concentration in zip(self.nuclides, self.concentrations):
            self.nuclides_and_concentrations[nuclide] = concentration

    def __str__(self):
        return f'BumatObject {self.material_name}, burnup = {self.burnup} MWd/kgU'

class XSParametersReader:
    def __init__(self, filename, npoints):
        self.filename = filename
        self.npoints = npoints
        self.lines = self.read_file(self.filename)
        self.points_array = self.get_points_array(self.lines, self.npoints)

    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return lines

    @staticmethod
    def get_points_array(lines, npoints):
        points_array = []
        point_dict = {}
        for i in range(npoints + 1):
            if i == 0:
                continue
            else:
                point_dict = {}
                point = lines[i].split()
                point_dict["RHO"] = float(point[0])
                point_dict["T_coolant"] = float(point[1])
                point_dict["T_Fuel"] = float(point[2])
                point_dict["C_B"] = float(point[3])
                points_array.append(point_dict)
        return points_array


if __name__ == "__main__":
    xsreader = XSParametersReader("lptau_ro_05.DAT", 256)
    for point in xsreader.points_array:
        print(point)

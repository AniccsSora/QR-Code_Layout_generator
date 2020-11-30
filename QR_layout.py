import numpy as np
import math
import matplotlib.pyplot as plt

class qrBan():

    def __set_module_color(self, loc=None, c=(0, 0, 0)):
        """
        loc=(row,col)
        ---------------------
        support "<0" index.
        """
        _0, _1 = None, None
        if loc[0] < 0:
            tmp = loc[0] * (-1)
            tmp %= self.param_dict['len_module']
            tmp *= (-1)
            tmp += self.param_dict['len_module']
            _0 = tmp
        else:
            _0 = loc[0]
        if loc[1] < 0:
            tmp = loc[1] * (-1)
            tmp %= self.param_dict['len_module']
            tmp *= (-1)
            tmp += self.param_dict['len_module'];
            _1 = tmp
        else:
            _1 = loc[1]

        # qr code always square just set common param
        r_start = self.param_dict['divide_bold'] + \
                  _0 * (self.param_dict['pixels_per_module'] + self.param_dict['divide_bold'])
        r_end = r_start + self.param_dict['pixels_per_module']
        c_start = self.param_dict['divide_bold'] + \
                  _1 * (self.param_dict['pixels_per_module'] + self.param_dict['divide_bold'])
        c_end = c_start + self.param_dict['pixels_per_module']

        self.__canvas[r_start:r_end, c_start:c_end] = c

    def __get_loc_finder_pattern(self):
        """
        return {'high':[(r1,c1),(r2,c2), ... ], 'low': [...] }
        """
        high_loc, low_loc = [], []
        # left top
        high_loc[:0] = [(1, 1 + _) for _ in range(5)]  # row 1
        high_loc[:0] = [(5, 1 + _) for _ in range(5)]  # row 2
        high_loc[:0] = [(1 + _, 1) for _ in range(5)]  # col 1
        high_loc[:0] = [(1 + _, 5) for _ in range(5)]  # col 2
        low_loc[:0] = [(0, _) for _ in range(7)]  # row 1
        low_loc[:0] = [(6, _) for _ in range(7)]  # r btm
        low_loc[:0] = [(_, 0) for _ in range(7)]  # col1
        low_loc[:0] = [(_, 6) for _ in range(7)]  # col_end
        low_loc[:0] = [(2, 2 + _) for _ in range(3)]  # inner row 1
        low_loc[:0] = [(3, 2 + _) for _ in range(3)]  # inner row 2
        low_loc[:0] = [(4, 2 + _) for _ in range(3)]  # inner row 3
        # right top
        high_loc[:0] = [(_ + 1, -6) for _ in range(5)]  # col 2
        high_loc[:0] = [(_ + 1, -2) for _ in range(5)]  # col 3
        high_loc[:0] = [(1, -3 - _) for _ in range(3)]  # row 1
        high_loc[:0] = [(5, -3 - _) for _ in range(3)]  # row 2 +++
        low_loc[:0] = [(0, -1 - _) for _ in range(7)]  # row 1
        low_loc[:0] = [(6, -1 - _) for _ in range(7)]  # row btm
        low_loc[:0] = [(_ + 1, -7) for _ in range(5)]  # col 1
        low_loc[:0] = [(_ + 1, -1) for _ in range(5)]  # col end
        low_loc[:0] = [(2, -3 - _) for _ in range(3)]  # inner row 1
        low_loc[:0] = [(3, -3 - _) for _ in range(3)]  # inner row 2
        low_loc[:0] = [(4, -3 - _) for _ in range(3)]  # inner row 3
        # left bottom
        low_loc[:0] = [(-1, _) for _ in range(7)]  # row -1
        low_loc[:0] = [(-7, _) for _ in range(7)]  # row -2
        low_loc[:0] = [(-2 - _, 0) for _ in range(5)]  # col 1
        low_loc[:0] = [(-2 - _, 6) for _ in range(5)]  # col 2
        low_loc[:0] = [(-3, 2 + _) for _ in range(3)]  # inner row -1
        low_loc[:0] = [(-4, 2 + _) for _ in range(3)]  # inner row -2
        low_loc[:0] = [(-5, 2 + _) for _ in range(3)]  # inner row -3
        high_loc[:0] = [(-2, 1 + _) for _ in range(5)]  # row -1
        high_loc[:0] = [(-6, 1 + _) for _ in range(5)]  # row -2
        high_loc[:0] = [(-3 - _, 1) for _ in range(3)]  # col 1
        high_loc[:0] = [(-3 - _, 5) for _ in range(3)]  # col 1

        return {'high': high_loc, 'low': low_loc}

    def __get_loc_finder_pattern_white_zone(self):
        loc = []

        loc[:0] = [(_, 7) for _ in range(7)]  # col 3
        loc[:0] = [(7, _) for _ in range(8)]  # row 3
        loc[:0] = [(_, -8) for _ in range(8)]  # col 1
        loc[:0] = [(7, -1 - _) for _ in range(7)]  # rend
        loc[:0] = [(-8, _) for _ in range(7)]  # outter row
        loc[:0] = [(-1 - _, 7) for _ in range(8)]  # outter col

        return loc

    def __get_loc_timing(self):
        high_loc, low_loc = [], []

        low_timing = 3 + (self.param_dict['version'] - 1) * 2
        high_timing = 3 + (self.param_dict['version'] - 1) * 2 - 1
        # horizion and vertical low timing
        for lt in range(low_timing):
            low_loc.append((6, 8 + lt * 2))
            low_loc.append((8 + lt * 2, 6))
        # horizion and vertical high timing
        for ht in range(high_timing):
            high_loc.append((6, 9 + ht * 2))
            high_loc.append((9 + ht * 2, 6))

        return {'high': high_loc, 'low': low_loc}

    def __get_module_pos_by_minus_0_idx(self, idx):
        if idx >= 0:
            raise Exception("Please assign minus 0 idx, your idx = {}".format(idx))
        tmp = idx * (-1);
        tmp %= self.param_dict['len_module'];
        tmp *= (-1);
        tmp += self.param_dict['len_module'];
        _0 = tmp
        return tmp

    def __deprecated_get_align_pattern_position(self):
        """
        Not working, because align pattern is NOT evenly distributed.
        It is defined by document "ISO/IEC JTC 1/SC 31 N" Page 79 .
        url: http://www.arscreatio.com/repositorio/images/n_23/SC031-N-1915-18004Text.pdf

        # align pattern dependency by version
        formula of number of align pattern(s) diagonal:

        ==> ceil( (End_pos - 6)/28 + 1 )

        End_pos (most right bottom idx) : ( 17 + 4*version ) - 7
        """
        if self.param_dict['version'] == 1:
            return []
        rtn = []
        align_appear_period = ((self.param_dict['version'] * 4) + 4) / (self.param_dict['number_of_align_pattern_diagonal'] - 1)
        rtn.append(6)  # left top
        for _ in range(self.param_dict['number_of_align_pattern_diagonal'] - 2):
            rtn.append(6 + align_appear_period * (_ + 1))
        rtn.append(self.__get_module_pos_by_minus_0_idx(-7))  # right bottom

        return rtn

    def __get_align_pattern_position(self):
        # ref http://www.arscreatio.com/repositorio/images/n_23/SC031-N-1915-18004Text.pdf
        table = {'1': [], \
                 '2': [6, 18], \
                 '3': [6, 22], \
                 '4': [6, 26], \
                 '5': [6, 30], \
                 '6': [6, 34], \
                 '7': [6, 22, 38], \
                 '8': [6, 24, 42], \
                 '9': [6, 26, 46], \
                 '10': [6, 28, 50], \
                 '11': [6, 30, 54], \
                 '12': [6, 32, 58], \
                 '13': [6, 34, 62], \
                 '14': [6, 26, 46, 66], \
                 '15': [6, 26, 48, 70], \
                 '16': [6, 26, 50, 74], \
                 '17': [6, 30, 54, 78], \
                 '18': [6, 30, 56, 82], \
                 '19': [6, 30, 58, 86], \
                 '20': [6, 34, 62, 90], \
                 '21': [6, 28, 50, 72, 94], \
                 '22': [6, 26, 50, 74, 98], \
                 '23': [6, 30, 54, 78, 102], \
                 '24': [6, 28, 54, 80, 106], \
                 '25': [6, 32, 58, 84, 110], \
                 '26': [6, 30, 58, 86, 114], \
                 '27': [6, 34, 62, 90, 118], \
                 '28': [6, 26, 50, 74, 98, 122], \
                 '29': [6, 30, 54, 78, 102, 126], \
                 '30': [6, 26, 52, 78, 104, 130], \
                 '31': [6, 30, 56, 82, 108, 134], \
                 '32': [6, 34, 60, 86, 112, 138], \
                 '33': [6, 30, 58, 86, 114, 142], \
                 '34': [6, 34, 62, 90, 118, 146], \
                 '35': [6, 30, 54, 78, 102, 126, 150], \
                 '36': [6, 24, 50, 76, 102, 128, 154], \
                 '37': [6, 28, 54, 80, 106, 132, 158], \
                 '38': [6, 32, 58, 84, 110, 136, 162], \
                 '39': [6, 26, 54, 82, 110, 138, 166], \
                 '40': [6, 30, 58, 86, 114, 142, 170]}
        ap_rc = table[str(self.param_dict['version'])]
        tmp = []
        for idx_r in ap_rc:
            for idx_c in ap_rc:
                tmp.append((idx_r, idx_c))
        dia = len(ap_rc)
        t1 = tmp[1:dia - 1]
        t2 = tmp[dia:dia ** 2 - dia]
        t3 = tmp[dia ** 2 - dia + 1:]
        return t1 + t2 + t3

    def __stress_align_pattern_on(self, pos):
        row, col = pos[0], pos[1]
        # set low color
        self.__set_module_color(loc=pos, c=self.param_dict['c_align_low'])  # center
        for _ in range(5):
            self.__set_module_color(loc=(row - 2, col - 2 + _), c=self.param_dict['c_align_low'])  # row 1
            self.__set_module_color(loc=(row + 2, col - 2 + _), c=self.param_dict['c_align_low'])  # row 2
        for _ in range(3):
            self.__set_module_color(loc=(row - 1 + _, col - 2), c=self.param_dict['c_align_low'])  # col 1
            self.__set_module_color(loc=(row - 1 + _, col + 2), c=self.param_dict['c_align_low'])  # col 2
        # set high color
        for _ in range(3):
            self.__set_module_color(loc=(row - 1, col - 1 + _), c=self.param_dict['c_align_high'])  # row 1
            self.__set_module_color(loc=(row + 1, col - 1 + _), c=self.param_dict['c_align_high'])  # row 2

        self.__set_module_color(loc=(row, col - 1), c=self.param_dict['c_align_high'])  # col 1-just 1 module
        self.__set_module_color(loc=(row, col + 1), c=self.param_dict['c_align_high'])  # col 2-just 1 module

    def __stress_format_pattern(self):
        # left top
        for i in range(9):
            if i == 6: continue  # avoid cover timing pattern
            self.__set_module_color(loc=(8, i), c=self.param_dict['c_format_zone'])  # row
            self.__set_module_color(loc=(i, 8), c=self.param_dict['c_format_zone'])  # row
        # right top
        for i in range(8):
            self.__set_module_color(loc=(8, -1 - i), c=self.param_dict['c_format_zone'])  # row
        # left bottom
        for i in range(7):
            if i == 6: pass  # avoid cover timing pattern
            self.__set_module_color(loc=(-1 - i, 8), c=self.param_dict['c_format_zone'])  # col

    def __stress_version_pattern(self):
        for i in range(3):
            for j in range(6):
                self.__set_module_color(loc=(-11 + i, j), c=self.param_dict['c_version_zone'])  # left-bottom
                self.__set_module_color(loc=(j, -11 + i), c=self.param_dict['c_version_zone'])  # right-top

    def __gen_Processing(self):
        # initial image size
        self.__canvas = np.zeros((self.param_dict['len_pixels'], self.param_dict['len_pixels'], 3), dtype=np.uint8)
        print("output size =", self.param_dict['len_pixels'], 'x', self.param_dict['len_pixels'])
        print("Each side have ", self.param_dict['len_module'], "modules")
        # set bk color

        self.__canvas[:, :] = self.param_dict['c_data_zone']

        # stress finder pattern
        f_pattern = self.__get_loc_finder_pattern()
        for loc_high in f_pattern['high']:
            self.__set_module_color(loc_high, self.param_dict['c_find_pattern_high'])
        for loc_low in f_pattern['low']:
            self.__set_module_color(loc_low, self.param_dict['c_find_pattern_low'])

        # stress finder pattern surrounding while zone
        f_p_white_zone = self.__get_loc_finder_pattern_white_zone()
        for white_loc in f_p_white_zone:
            self.__set_module_color(white_loc, self.param_dict['c_find_pattern_while_zone'])

        # stress timing pattern
        timing_pattern = self.__get_loc_timing()
        for t_p in timing_pattern['low']:
            self.__set_module_color(t_p, self.param_dict['c_timing_low'])
        for t_p in timing_pattern['high']:
            self.__set_module_color(t_p, self.param_dict['c_timing_high'])

        # stress align pattern(s)
        align_loc = self.__get_align_pattern_position()

        for loc in align_loc:
            self.__stress_align_pattern_on(pos=loc)

        # stress format patterns
        self.__stress_format_pattern()

        # stress version patters
        self.__stress_version_pattern()

        # Don't forget Dark Module
        self.__set_module_color((-8, 8), self.param_dict['c_dark_module'])

        #### finally padding ####
        # pixel_of_actual_padding
        if self.param_dict['len__padding_module'] != 0:
            _PoAP = self.param_dict['len__padding_module'] \
                    * (self.param_dict['pixels_per_module'] + self.param_dict['divide_bold'])
            pds = ((_PoAP, _PoAP), (_PoAP, _PoAP))

            def pad_with(vector, pad_width, iaxis, kwargs):
                pad_value = kwargs.get('padder', 10)
                vector[:pad_width[0]] = pad_value
                vector[-pad_width[1]:] = pad_value

            ca0 = np.pad(self.__canvas[:, :, 0], _PoAP, pad_with, padder=self.param_dict['c_quite_zone'][0])
            ca1 = np.pad(self.__canvas[:, :, 1], _PoAP, pad_with, padder=self.param_dict['c_quite_zone'][1])
            ca2 = np.pad(self.__canvas[:, :, 2], _PoAP, pad_with, padder=self.param_dict['c_quite_zone'][2])
            self.__canvas = np.dstack((ca0, ca1, ca2))
        else:
            # No padding
            pass

        # stress bold line in padding area
        for i in range(self.param_dict['divide_bold']):
            _ = self.param_dict['pixels_per_module'] + self.param_dict['divide_bold']
            self.__canvas[i::_, :] = self.param_dict['c_divide']
            self.__canvas[:, i::_] = self.param_dict['c_divide']

    def valid_all_key(self, **kwargs):
        for key in kwargs:
            try:
                self.param_dict[key]
            except KeyError as err:
                print("NOT EXISTS parameter key = {}".format(err))
                avaliable_key = [key for key in self.param_dict.keys()]

                print("\t => Can assign key is :")

                # beauty output order
                show_range = 3
                wantOut = avaliable_key
                for idx in range(0, len(wantOut), show_range):
                    if idx == 0: print("{", end='')
                    head_idx, end_idx = idx, idx + show_range
                    end_idx = end_idx if end_idx + 1 < len(wantOut) else len(wantOut)
                    end = '\n' if end_idx != len(wantOut) else ' }\n'
                    print(" " + str(wantOut[head_idx:end_idx]).strip('[]').replace(',', ''), end=end)

                exit(87)

    def __init__(self, **kwargs):

        # 預設參數
            # padding module
        self.param_dict = {
            'version': 1,
            'c_quite_zone':  (255, 253, 218),
            'c_find_pattern_low':  (178, 16, 22),
            'c_find_pattern_high':  (248, 161, 164),
            'c_find_pattern_while_zone':  (255, 255, 255),
            'c_format_zone':  (0, 255, 0),
            'c_version_zone':  (0, 0, 255),
            'c_data_zone':  (192, 192, 192),
            'c_align_low':  (49, 108, 140),
            'c_align_high':  (87, 223, 214),
            'c_timing_low':  (122, 41, 123),
            'c_timing_high':  (237, 211, 237),
            'c_dark_module':  (0, 0, 0),
            'c_divide':  (158, 157, 153),
            'pixels_per_module': 16,
            'divide_bold': 1,
            'len__padding_module': 4,
            # Below parameters will not assign by user.
            'len_module': None,
            'len_pixels': None,
            'number_of_align_pattern_diagonal': None,
        }
        # 檢查 傳入 kwargs 在 在預設參數是有東西的
        self.valid_all_key(**kwargs)

        # 依照使用者給定 覆蓋預設參數
        print("Setting parameter :")
        for key in kwargs:
            self.param_dict[key] = kwargs[key]
            print("(", key, '=', self.param_dict[key], "),", end="")
        print("\n====================")
        if self.param_dict['version'] < 1 or self.param_dict['version'] > 40:
            raise Exception("version must in 1~40, get version= {}".format(self.param_dict['version']))

        #
        self.__canvas = None

        # calculate parameters, careful order
        # set each side of module length by version
        self.param_dict['len_module'] = (self.param_dict['version'] * 4) + 17

        # actual image size
        self.param_dict["len_pixels"] = ((self.param_dict["pixels_per_module"] + self.param_dict["divide_bold"])
                                         * self.param_dict["len_module"]) + self.param_dict["divide_bold"]

        #  number of diagonal
        self.param_dict['number_of_align_pattern_diagonal'] = None
        if self.param_dict['version'] == 1:  # 無
            self.param_dict['number_of_align_pattern_diagonal'] = 0
        else:
            end_pos = (17 + 4 * self.param_dict['version']) - 7
            ___Otz___ = math.ceil((end_pos - 6) / 28 + 1)
            self.param_dict['number_of_align_pattern_diagonal'] = ___Otz___
        print("diag:", self.param_dict['number_of_align_pattern_diagonal'],
              ",version =", self.param_dict['version'])
        #### timing pattern length
        """
        timing pattern length formula:
        => 4*version + 1
        """
        # no used: self.__len_of_timing_pattern = 4*self.param_dict['version'] + 1

        # Check  all parameter were initialed.
        # 該計算的參數都算好了，才能進去 processing
        for key, value in self.param_dict.items():
            if value is None:
                raise Exception("keyNoInitial: \'self.param_dict[\"{}\"]\' was NOT initial, it still None.".format(key))

        #### gen Processing ####
        self.__gen_Processing()

    def get_layout(self):

        return self.__canvas


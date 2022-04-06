
import numpy as np
import math
from skimage import io

class helper:

    def __init__(self, in_img_name, encode_file_name, decode_file_name, out_img_name):
        self.setA()
        self.in_img_name = in_img_name
        self.encode_file_name = encode_file_name
        self.decode_file_name = decode_file_name
        self.out_img_name = out_img_name

    def set_encode_file_name(self, in_img_name, encode_file_name):
        self.in_img_name = in_img_name
        self.encode_file_name = encode_file_name

    def dbf(self, tag, img):
        print(
            f"{tag}: max: {np.max(img)}, min: {np.min(img)}, shape: {img.shape}, "
            f"type: {img.dtype}, mean: {np.mean(img)}")
        return img

    def up_align(self, x, y):
        if x % y == 0:
            return x
        return x + y - x % y


    def quantification(self, frequency_domain: np.ndarray,
                       standard_table: np.ndarray) -> None:
        for i in range(0, 8):
            for j in range(0, 8):
                frequency_domain[i][j] = \
                    round(frequency_domain[i][j] / standard_table[i][j])


    def encode(self, time_domain: np.ndarray, standard_table: np.ndarray,
               directing, alternating) -> None:
        for i in range(0, time_domain.shape[0], 8):
            for j in range(0, time_domain.shape[1], 8):
                t = np.empty([8, 8], dtype=float)
                for u in range(0, 8):
                    for v in range(0, 8):
                        t[u][v] = time_domain[i + u][j + v]
                f = np.matmul(self.A, t)
                f = np.matmul(f, self.A_T)
                self.quantification(f, standard_table)
                x = 0
                y = 0
                cnt = 0
                directing.append(f[0][0])
                for u in self.Z:
                    x += u[0]
                    y += u[1]
                    if f[x][y] == 0:
                        cnt = cnt + 1
                    else:
                        alternating.append([cnt, f[x][y]])
                        cnt = 0
                if f[7][7] == 0:
                    alternating.append([0, 0])


    def encode_from_img(self):
        image = io.imread(self.in_img_name)
        data = np.array(image, dtype=float)
        print(data.shape)
        file_handle = open(self.encode_file_name, mode='w')
        file_handle.write(str(int(len(data) // 16 * 16)) + '\n')
        file_handle.write(str(int(len(data[0]) // 16 * 16)) + '\n')

        luminance_time_domain = np.zeros([len(data) // 16 * 16,
                                          len(data[0]) // 16 * 16], dtype=float)
        blue_chrominance_time_domain = np.zeros([len(data) // 16 * 16,
                                                 len(data[0]) // 16 * 16], dtype=float)
        red_chrominance_time_domain = np.zeros([len(data) // 16 * 16,
                                                len(data[0]) // 16 * 16], dtype=float)
        for i in range(0, luminance_time_domain.shape[0]):
            for j in range(0, luminance_time_domain.shape[1]):
                luminance_time_domain[i][j] = 0.299 * data[i][j][0] + \
                                              0.587 * data[i][j][1] + 0.114 * data[i][j][2]
                blue_chrominance_time_domain[i][j] = \
                    0.492 * (data[i][j][2] - luminance_time_domain[i][j])
                red_chrominance_time_domain[i][j] = \
                    0.877 * (data[i][j][0] - luminance_time_domain[i][j])
        luminance_quantification = np.array(
            [[16, 11, 10, 16, 24, 40, 51, 61],
             [12, 12, 14, 19, 26, 58, 60, 55],
             [14, 13, 16, 24, 40, 57, 69, 56],
             [14, 17, 22, 29, 51, 87, 80, 62],
             [18, 22, 37, 56, 68, 109, 103, 77],
             [24, 35, 55, 64, 81, 104, 113, 92],
             [49, 64, 78, 87, 103, 121, 120, 101],
             [72, 92, 95, 98, 112, 100, 103, 99]]
        )
        chrominance_quantification = np.array(
            [[17, 18, 24, 47, 99, 99, 99, 99],
             [18, 21, 26, 66, 99, 99, 99, 99],
             [24, 26, 56, 99, 99, 99, 99, 99],
             [47, 66, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99]]
        )
        luminance_alternating = []
        blue_chrominance_alternating = []
        red_chrominance_alternating = []
        luminance_directing = []
        blue_chrominance_directing = []
        red_chrominance_directing = []

        self.encode(luminance_time_domain, luminance_quantification,
               luminance_directing, luminance_alternating)
        file_handle.write(str(len(luminance_directing)) + '\n')
        for i in luminance_directing:
            file_handle.write(str(int(i)) + '\n')
        file_handle.write(str(len(luminance_alternating)) + '\n')
        for i in luminance_alternating:
            file_handle.write(str(int(i[0])) + '\n')
            file_handle.write(str(int(i[1])) + '\n')

        self.encode(blue_chrominance_time_domain, chrominance_quantification, blue_chrominance_directing,
               blue_chrominance_alternating)
        file_handle.write(str(len(blue_chrominance_directing)) + '\n')
        for i in blue_chrominance_directing:
            file_handle.write(str(int(i)) + '\n')
        file_handle.write(str(len(blue_chrominance_alternating)) + '\n')
        for i in blue_chrominance_alternating:
            file_handle.write(str(int(i[0])) + '\n')
            file_handle.write(str(int(i[1])) + '\n')

        self.encode(red_chrominance_time_domain, chrominance_quantification, red_chrominance_directing,
               red_chrominance_alternating)
        file_handle.write(str(len(red_chrominance_directing)) + '\n')
        for i in red_chrominance_directing:
            file_handle.write(str(int(i)) + '\n')
        file_handle.write(str(len(red_chrominance_alternating)) + '\n')
        for i in red_chrominance_alternating:
            file_handle.write(str(int(i[0])) + '\n')
            file_handle.write(str(int(i[1])) + '\n')
        print("encode end")
        file_handle.close()

    def inverse_quantification(self, frequency_domain: np.ndarray,
                               standard_table: np.ndarray) -> None:
        for i in range(0, 8):
            for j in range(0, 8):
                frequency_domain[i][j] *= standard_table[i][j]

    def decode(self, time_domain: np.ndarray, 
               directing, alternating, standard_table: np.ndarray) -> None:
        frequency_domain = np.empty([time_domain.shape[0], time_domain.shape[1]])
        alternating_current = 0
        directing_current = 0
        for i in range(0, time_domain.shape[0], 8):
            for j in range(0, time_domain.shape[1], 8):
                x = i
                y = j
                frequency_domain[x][y] = directing[directing_current]
                directing_current = directing_current + 1
                cnt = 0
                flag = 0
                for u in self.Z:
                    x += u[0]
                    y += u[1]
                    if flag:
                        frequency_domain[x][y] = 0
                    elif cnt == alternating[alternating_current][0]:
                        frequency_domain[x][y] = alternating[alternating_current][1]
                        if alternating[alternating_current][1] == 0:
                            flag = 1
                        alternating_current = alternating_current + 1
                        cnt = 0
                    else:
                        frequency_domain[x][y] = 0
                        cnt = cnt + 1
        for i in range(0, frequency_domain.shape[0], 8):
            for j in range(0, frequency_domain.shape[1], 8):
                f = np.empty([8, 8])
                for u in range(0, 8):
                    for v in range(0, 8):
                        f[u][v] = frequency_domain[i + u][j + v]
                self.inverse_quantification(f, standard_table)
                t = np.matmul(self.A_i, f)
                t = np.matmul(t, self.A_iT)
                for u in range(0, 8):
                    for v in range(0, 8):
                        time_domain[i + u][j + v] = t[u][v]

    def decode_to_img(self):
        luminance_quantification = np.array(
            [[16, 11, 10, 16, 24, 40, 51, 61],
             [12, 12, 14, 19, 26, 58, 60, 55],
             [14, 13, 16, 24, 40, 57, 69, 56],
             [14, 17, 22, 29, 51, 87, 80, 62],
             [18, 22, 37, 56, 68, 109, 103, 77],
             [24, 35, 55, 64, 81, 104, 113, 92],
             [49, 64, 78, 87, 103, 121, 120, 101],
             [72, 92, 95, 98, 112, 100, 103, 99]]
        )
        chrominance_quantification = np.array(
            [[17, 18, 24, 47, 99, 99, 99, 99],
             [18, 21, 26, 66, 99, 99, 99, 99],
             [24, 26, 56, 99, 99, 99, 99, 99],
             [47, 66, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99],
             [99, 99, 99, 99, 99, 99, 99, 99]]
        )

        file_handle = open(self.decode_file_name, mode='r')
        buffer = []
        for i in file_handle.readlines():
            buffer.append(int(i))
        file_handle.close()
        # os.remove("1.txt")
        now = 2
        luminance_time_domain = np.empty([buffer[0], buffer[1]])
        blue_chrominance_time_domain = np.empty([buffer[0], buffer[1]])
        red_chrominance_time_domain = np.empty([buffer[0], buffer[1]])
        luminance_directing = []
        size = buffer[now]
        now = now + 1
        for i in range(0, size):
            luminance_directing.append(buffer[now])
            now = now + 1
        luminance_alternating = []
        size = buffer[now]
        now = now + 1
        for i in range(0, size):
            luminance_alternating.append([buffer[now], buffer[now + 1]])
            now = now + 2
        self.decode(luminance_time_domain, luminance_directing,
                    luminance_alternating, luminance_quantification)

        blue_chrominance_directing = []
        size = buffer[now]
        now = now + 1
        for i in range(0, size):
            blue_chrominance_directing.append(buffer[now])
            now = now + 1
        blue_chrominance_alternating = []
        size = buffer[now]
        now = now + 1
        for i in range(0, size):
            blue_chrominance_alternating.append([buffer[now], buffer[now + 1]])
            now = now + 2
        self.decode(blue_chrominance_time_domain, blue_chrominance_directing,
                    blue_chrominance_alternating, chrominance_quantification)

        red_chrominance_directing = []
        size = buffer[now]
        now = now + 1
        for i in range(0, size):
            red_chrominance_directing.append(buffer[now])
            now = now + 1
        red_chrominance_alternating = []
        size = buffer[now]
        now = now + 1
        for i in range(0, size):
            red_chrominance_alternating.append([buffer[now], buffer[now + 1]])
            now = now + 2
        self.decode(red_chrominance_time_domain, red_chrominance_directing,
                    red_chrominance_alternating, chrominance_quantification)
        res = np.empty([luminance_time_domain.shape[0], luminance_time_domain.shape[1], 3], dtype=float)
        for i in range(0, luminance_time_domain.shape[0]):
            for j in range(0, luminance_time_domain.shape[1]):
                res[i][j][0] = luminance_time_domain[i][j] + 1.140 * red_chrominance_time_domain[i][j]
                res[i][j][1] = luminance_time_domain[i][j] - 0.395 * blue_chrominance_time_domain[i][j] - \
                               0.581 * red_chrominance_time_domain[i][j]
                res[i][j][2] = luminance_time_domain[i][j] + 2.032 * blue_chrominance_time_domain[i][j]
        res = res.clip(0, 255)
        io.imsave("images/out.bmp", res)


    def init(self, matrix):
        for i in range(8):
            for j in range(8):
                if i == 0:
                    x = math.sqrt(1 / 8)
                else:
                    x = math.sqrt(2 / 8)
                matrix[i][j] = x * math.cos(math.pi * (j + 0.5) * i / 8)

    def setA(self):
        self.A = np.zeros([8, 8])
        self.Z = np.array(
            [[0, 1], [1, -1],
             [1, 0], [-1, 1], [-1, 1],
             [0, 1], [1, -1], [1, -1], [1, -1],
             [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
             [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
             [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
             [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
             [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
             [1, 0], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
             [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
             [1, 0], [1, -1], [1, -1], [1, -1],
             [0, 1], [-1, 1], [-1, 1],
             [1, 0], [1, -1],
             [0, 1]
             ]
        )
        self.init(self.A)
        self.A_T = self.A.transpose()
        self.A_i = np.linalg.inv(self.A)
        self.A_iT = np.linalg.inv(self.A_T)


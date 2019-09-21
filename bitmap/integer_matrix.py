#coding:utf-8

def make_matrix_key(matrix_name):
    return "matrix::" + matrix_name

def calculate_index(row, col, row_num, col_num):
    if not (row < row_num):
        raise ValueError("row out of range")
    if not (col < col_num):
        raise ValueError("col out of range")
    return "#" + str(row*row_num+col)

class IntegerMatrix:

    def __init__(self, client, name, row_num, col_num, bit_length=64, signed=True):
        self.client = client
        self.bitmap = make_matrix_key(name)
        self.row_num = row_num
        self.col_num = col_num
        if signed:
            self.type = "i" + str(bit_length)
        else:
            self.type = "u" + str(bit_length)

    def set(self, row, col, value):
        """
        对矩阵的指定位置进行设置。
        """
        index = calculate_index(row, col, self.row_num, self.col_num)
        self.client.bitfield(self.bitmap, "SET", self.type, index, value)

    def get(self, row, col):
        """
        获取矩阵在指定位置上的值。
        """
        index = calculate_index(row, col, self.row_num, self.col_num)
        return self.client.bitfield(self.bitmap, "GET", self.type, index)

    def show(self):
        """
        打印出整个矩阵。
        """
        for row in range(self.row_num):
            elements = []
            for col in range(self.col_num):
                elements.append(self.get(row, col))
            print("matrix[{0}]: {1}".format(row, elements))

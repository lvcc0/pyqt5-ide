# example file
# try "plus plus plus minus print inc print dec print print"

class Interpreter:

    INC = 'plus'
    DEC = 'minus'
    INCPTR = 'inc'
    DECPTR = 'dec'
    OUT = 'print'

    def __init__(self):
        self.cells = [0] * 256
        self.ptr = 0
        
    def run(self, code, con):
        code = code.split()
        
        for instruction in code:
            if instruction == self.INC: self.cells[self.ptr] += 1
            elif instruction == self.DEC: self.cells[self.ptr] -= 1
            elif instruction == self.INCPTR: self.ptr += 1
            elif instruction == self.DECPTR: self.ptr -= 1
            elif instruction == self.OUT: con.print(self.cells[self.ptr])

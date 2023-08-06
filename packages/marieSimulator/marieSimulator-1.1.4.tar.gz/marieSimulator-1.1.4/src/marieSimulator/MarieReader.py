class MarieReader:
    def __init__(self, filename):
        self.input = []
        self.M = []
        self.symbolTable = {}

        self.read(filename)
    
    def read(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                self.input.append(line)
                if line != '\n':
                    self.M.append(0)
        
        self.interpret()
        for item in self.M:
            if item & 0b100000000000 == 0b100000000000:
                self.interpret()
                break

    def interpret(self):
        ctr = 0
        for line in self.input:
            if line[-1] == '\n':
                line = line[:-1]

            line = " ".join(line.strip().split())
            
            tokens = line.split(' ') 

            if tokens[0][-1] == ',':
                self.symbolTable[tokens[0][:-1]] = ctr
                tokens = tokens[1:]

            opcode = None

            instruction = (tokens[0]).upper()
            if instruction == 'JNS':
                opcode = 0xF
            elif instruction == 'LOAD':
                opcode = 0x1
            elif instruction == 'STORE':
                opcode = 0x2
            elif instruction == 'ADD':
                opcode = 0x3
            elif instruction == 'SUBT':
                opcode = 0x4
            elif instruction == 'INPUT':
                opcode = 0x5
                tokens.append('000')
            elif instruction == 'OUTPUT':
                opcode = 0x6
                tokens.append('000')
            elif instruction == 'HALT':
                opcode = 0x7
                tokens.append('000')
            elif instruction == 'SKIPCOND':
                opcode = 0x8
            elif instruction == 'JUMP':
                opcode = 0x9
            elif instruction == 'CLEAR':
                opcode = 0xA
                tokens.append('000')
            elif instruction == 'ADDI':
                opcode = 0xB
            elif instruction == 'JUMPI':
                opcode = 0xC
            elif instruction == 'LOADI':
                opcode = 0xD
            elif instruction == 'STOREI':
                opcode = 0xE
            else:
                opcode = 0x0

            address = tokens[1]
            try:
                address = int(address, 16)
            except:
                if address in self.symbolTable:
                    address = self.symbolTable[address]
                else:
                    address = -1
            
            self.M[ctr] = (opcode << 12) | address

            ctr += 1


    


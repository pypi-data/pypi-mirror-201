class Marie:
    def __init__(self, mr = None):
        self.AC = 0x0000
        self.PC = 0b000000000000
        self.MAR = 0b000000000000
        self.MBR = 0x0000
        self.IR = 0x0000
        self.InReg = 0x00
        self.OutReg = 0x00

        self.GUI = False

        self.M = []

        self.operation = None
        self.running = True

        if mr != None:
            self.parse(mr)
    
    def parse(self, mr):
        self.M = mr.M
        self.symbolTable = mr.symbolTable

    def show(self):
        output = "\n"

        for item in self.M:
            output += hex(item) + " | "
        output = output[:-3] + "\n"

        print(output)
    
    def run(self):
        while self.running:
            self.fetch()
            self.next()
            self.decode()
            self.getOperand()
            self.execute()

    def fetch(self):
        self.MAR = self.PC
        self.MBR = self.M[self.MAR]
        self.IR = self.MBR
    
    def next(self):
        self.PC += 1
    
    def decode(self):
        self.MAR = (self.IR & 0x0FFF)
        self.operation = (self.IR & 0xF000) >> 12

    def getOperand(self):
        if self.operation not in [0x5, 0x6, 0x7, 0x8, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF]:
            self.MBR = self.M[self.MAR]

    def execute(self):
        if self.operation == 0x0:
            pass
        elif self.operation == 0x1:
            self.load()
        elif self.operation == 0x2:
            self.store()
        elif self.operation == 0x3:
            self.add()
        elif self.operation == 0x4:
            self.subt()
        elif self.operation == 0x5:
            self.input()
        elif self.operation == 0x6:
            self.output()
        elif self.operation == 0x7:
            self.halt()
        elif self.operation == 0x8:
            self.skipcond()
        elif self.operation == 0x9:
            self.jump()
        elif self.operation == 0xA:
            self.clear()
        elif self.operation == 0xB:
            self.addI()
        elif self.operation == 0xC:
            self.jumpI()
        elif self.operation == 0xD:
            self.loadI()
        elif self.operation == 0xE:
            self.storeI()
        elif self.operation == 0xF:
            self.jnS()
        


    def jnS(self):
        self.MBR = self.PC
        self.M[self.MAR] = self.MBR
        self.MBR = (self.IR & 0x0FFF)
        self.AC = 0x1
        self.AC = self.AC + self.MBR
        self.PC = self.AC

    def load(self):
        self.AC = self.MBR

    def store(self):
        self.MBR = self.AC
        self.M[self.MAR] = self.MBR

    def add(self):
        self.AC = self.AC + self.MBR

    def subt(self):
        self.AC = self.AC - self.MBR

    def input(self):
        if self.GUI:
            self.InReg = None
            while self.InReg == None:
                self.InReg = self.InReg
        else:
            self.InReg = int(input("Input (HEX): "), 16)
        self.AC = self.InReg

    def output(self):
        self.OutReg = self.AC
        if not self.GUI:
            print("Output (HEX): " + hex(self.OutReg))


    def halt(self):
        self.running = False

    def skipcond(self):
        skipBits = (self.IR & 0b0000110000000000) >> 8
        if skipBits == 0b0000:
            if self.AC < 0:
                self.next()
        elif skipBits == 0b0100:
            if self.AC == 0:
                self.next()
        elif skipBits == 0b1000:
            if self.AC > 0:
                self.next()

    def jump(self):
        self.PC = (self.IR & 0x0FFF)
    
    def clear(self):
        self.AC = 0x0
    
    def addI(self):
        self.MAR = self.MBR
        self.MBR = self.M[self.MAR]
        self.AC = self.AC + self.MBR

    def jumpI(self):
        self.PC = self.MBR
    
    def loadI(self):
        self.MAR = self.MBR
        self.MBR = self.M[self.MAR]
        self.AC = self.MBR
    
    def storeI(self):
        self.MAR = self.MBR
        self.MBR = self.AC
        self.M[self.MAR] = self.MBR


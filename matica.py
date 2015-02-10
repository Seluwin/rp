

class Matica():
    def __init__(self, m):
        a = max([ len(i) for i in m])
        b = min([len(i) for i in m])
        if a != b:
            raise Exception('nie je matica')
        self.stlpce = a
        self.riadky = len(m)
        self.matrix = m

    def vypis(self):
        #print(self.matrix)
        #print('riadkov ',self.riadky)
        #print('stlpcov ', self.stlpce)
        for i in self.matrix:
            for j in i:
                print(j, end='')
            print()

    def __str__(self):
        st = ''
        res = ''
        for i in self:
            st = str(i)
            st = st[1:len(st)-1]
            res += st + '\n'
        return res

    def __len__(self):
        return self.riadky

    def __iter__(self):
        for x in self.matrix:
            yield x

    def __getitem__(self,key):
        return self.matrix[key]

    def __mul__(self, other):
        if self.stlpce != other.riadky:
            raise Exception('Error:matice nemaju spravne dimenzie')
        riadok = []
        ret = []
        tmp = 0
        for i in self:
            for stlpec in range(len(other[0])):
                for j in range(len(i)):
                    tmp += (i[j] * other[j][stlpec])
                riadok.append(tmp)
                tmp = 0
            ret.append(riadok)
            riadok = []
        return Matica(ret)


if __name__ == '__main__':
    print('test')
    m1 = Matica( [ [1,0,5],[0,1,1],[0,0,1 ]])
    print(m1)
    m2 = Matica( [ [1,1,0],[2,1,1],[1,3,2]])
    m3 = m1 * m2
    print(m3)
    bod = Matica([[2],[2],[1]])
    print( m2 * bod)

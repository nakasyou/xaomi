class Maruko:
    def __init__(self,n):
        self.data={}
        self.n=n
    def arr_hash(self,arr):
        return "/".join([hex(_.__hash__()).replace("0x","") for _ in arr])
    def larn(self,data:list):
        if len(data)<=self.n: raise TypeError("input data length must n←英語崩壊()")
        for i in range(len(data)-self.n):
            x=data[i:i+self.n]
            y=data[i+self.n]
            #print(x,y)
            x_hash=self.arr_hash(x)
            if x_hash not in self.data:
                self.data[x_hash]={}
            if y not in self.data[x_hash]:
                self.data[x_hash][y]=0
            self.data[x_hash][y]+=1
    def choice(self,x:list,size):
        if len(x)!=self.n: raise TypeError()
        x_hash=self.arr_hash(x)
        if x_hash not in self.data:return []
        
        y_datas=self.data[x_hash]
        p=np.array(list(y_datas.values()))
        p=p/p.sum()
        return np.random.choice(list(y_datas.keys()),p=p,size=size).tolist()
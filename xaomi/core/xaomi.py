import random
import pickle
import janome
from .maruko import Maruko
from ..utils.cos_sim import cos_sim
from ..utils.doc2vec import doc2vec

class Xaomi:
    def __init__(self,maruko_n=2,larn=True):
        self.maruko_n=maruko_n
        self.back=[]
        self.tokenizer=janome.tokenizer.Tokenizer()
        self.mkf={}
        self.maruko=Maruko(maruko_n)
        self.io={}
        self.larn=larn

        self.add_io("こんにちは","こんにちは！調子はどうですか？")
        self.maruko.larn(["__bof__"]*maruko_n+["こんにちは"]+["__eof__"])
    def talk(self,input,id="main"):
        # larn
        if self.larn:
            #print("larning...")
            # mkf
            tokens=["__bof__"]*self.maruko_n +list(self.tokenizer.tokenize(input,wakati=True)) +["__eof__"]
            self.maruko.larn(tokens)
            # io
            back=None
            for b in self.back:
                if b[0]==id:
                    back=b[1]
                    break
            if back==None:
                back=""
                if len(self.back)>100:
                    self.back.pop(0)
                self.back.append([id,""])
            self.add_io(back,input)
        #print("predicting...")
        # set target
        target_point=-1000;
        target=None
        input_vec=doc2vec(input)

        for i_vec,o_vec in self.io.values():
            cos=cos_sim(i_vec,input_vec)
            if target_point<cos:
                target_point=cos
                target=o_vec

        # predict
        result=["__bof__"]*self.maruko_n
        index=0
        while True:
            index+=1
            searched=self.maruko.choice(result[-self.maruko_n:],50)
            if len(searched)==0:break
            if index>50:break
            if result[-1]=="__eof__":break
            # token select
            token_point=-1000
            token_set=""
            for token in searched:
                cos=cos_sim(doc2vec("".join(result+[token])),target)
                if token_point<cos:
                    token_point=cos
                    token_set=token
            result.append(token_set)
        result=result[self.maruko_n:-1]
        result="".join(result)
        back_index=0
        for i,b in enumerate(self.back):
            if b[0]==id:
                back_index=i
                break
        if self.larn:
            self.back[back_index][1]=result
        return result
    def add_io(self,i,o):
        i_vec=doc2vec(i)
        o_vec=doc2vec(o)

        self.io[i+"-"+o]=(i_vec,o_vec)
    def save(self):
        return pickle.dumps({
            "io":self.io,
            "maruko":self.maruko
        })
    def load(self,pick):
        loaded=pickle.loads(pick)
        self.io=loaded["io"]
        self.maruko=loaded["maruko"]
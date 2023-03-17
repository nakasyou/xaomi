import janome, pykakasi
import unicodedata
import numpy as np
import janome.tokenizer

kks = pykakasi.kakasi()
alphas=list("abcdefghijklmnopqrstuvwxyz0123456789!?., ")
def doc2vec(text: str):
    if text=="":text=" "
    text=unicodedata.normalize('NFKC',text)
    text="".join([token["passport"] for token in kks.convert(text)])
    text=text.lower()
    result=np.zeros(len(alphas))
    for i,alpha in enumerate(alphas):
        result[i]=text.count(alpha)
    if result.sum()==0:
        result[-1]=1
    return result/result.sum()
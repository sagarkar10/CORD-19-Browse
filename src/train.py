import pandas as pd
import xmltodict
import fasttext
import glob

from tokenizer import Tokenizer
import numpy as np

def preprocess(data):
    data = data.replace("-", " ")
    data = data.replace(".", " ")
    data = data.replace("_", " ")
    data = data.replace(":", " ")
    
    data = ' '.join(Tokenizer.tokenize(data))
    return data

def get_train_data(df, cols_to_use):
    all_text = ". ".join(np.concatenate(df[cols_to_use].values))
    return preprocess(all_text)

def read_xmls(filenames):
    mdf = []
    for fn in filenames:
        with open(fn, "rb") as f:
            d = xmltodict.parse(f)
            for each in d["Response"]["ListRecords"]["record"]:
                mdf.append(each["metadata"]['oai_dc:dc'])

    mdf = pd.DataFrame(mdf, columns=['dc:title', 'dc:creator', 'dc:subject', 'dc:description', 'dc:date', 'dc:identifier'])
    mdf["dc:subject"] = mdf["dc:subject"].apply(lambda x:[x] if isinstance(x, str) else x)
    mdf["dc:creator"] = mdf["dc:creator"].apply(lambda x:[x] if isinstance(x, str) else x)
    mdf["dc:date"] = mdf["dc:date"].apply(lambda x:[x] if isinstance(x, str) else x)
    mdf["dc:identifier"] = mdf["dc:identifier"].apply(lambda x:[x] if isinstance(x, str) else x)
    mdf["dc:description"] = mdf["dc:description"].apply(lambda x:x[0] if isinstance(x, list) else x)
    mdf["dc:title"] = mdf["dc:title"].apply(lambda x:x if isinstance(x, str) else x)
    mdf = mdf.rename(columns={'dc:title':'title', 'dc:creator':'author', 'dc:subject':'subject', 'dc:description':'abstract', 'dc:date':'date', 'dc:identifier':'identifier'})
    mdf.to_csv("../data/arxiv_cs.csv", index=False)
    return mdf

base_name = "arxiv_cs"
train_filename = f"{base_name}_train_data.txt"
fl = glob.glob(f"../data/{base_name}/*.xml")

df = read_xmls(fl) #pd.read_csv("../data/arxiv_cs.csv")
train_data = get_train_data(df, cols_to_use=["title", "abstract"])

with open(train_filename, "w") as f:
    f.write(train_data)

model = fasttext.train_unsupervised(train_filename)
model.save_model(f"{base_name}-100d-2nd.bin")

# from gensim.models.wrappers import FastText as ft
# model = ft.load_fasttext_format("arxiv_cs-100d-2nd.bin")
# model.most_similar(positive=["faceebook"])

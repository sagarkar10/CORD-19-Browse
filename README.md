### Covid19
Trying to build a Document Analysis Pipeline with Covid-19 open data set

#### Download Resources
Download the model file form [here](https://www.kaggle.com/davidmezzetti/cord19-fasttext-vectors#cord19-300d.magnitude) and after unzipping keep it in dir `resources` in the root directory

#### Download Data
For now we will only use the `Metadata File` from [here](https://pages.semanticscholar.org/coronavirus-research) and keep it as `metadata.csv` in dir `data` at the root folder

#### DIR structure should look like
```
.
├── LICENSE
├── README.md
├── config.cfg
├── data
│   ├── metadata.csv
|   | --- metadata_processed.pickle ( this file will be generated after you run update.py)
├── file
├── resources
│   ├── cord19-300d.magnitude
├── src
│   ├── app.py
│   ├── data_io.py
│   ├── embedding.py
│   ├── tokenizer.py
│   ├── update.py
│   ├── utils.py
│   └── vectorizer.py

```

 
### Running the Streamlit App
```
cd src
streamlit run app.py
```

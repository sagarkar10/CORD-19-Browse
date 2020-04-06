### Covid19
A app to intelligently search through COVID-19 Open Research Dataset (CORD-19)[link](https://pages.semanticscholar.org/coronavirus-research) and find similar papers powered with Machine Learning and NLP. All with a sleek UI.

###### Note: Project Under Development

#### Download Resources
Download the model file `cord19-300d.magnitude (644.95 MB)` form [here](https://www.kaggle.com/davidmezzetti/cord19-fasttext-vectors#cord19-300d.magnitude) and after unzipping keep it in dir `resources` in the root directory.
Note: You will need to login into Kaggle.

For now we will only use the Metadata File from [Semantic Scholar](https://pages.semanticscholar.org/coronavirus-research).
A `sample_metadata.csv` with only `1000` doc is added for app readiness. Please update the file by running the app and clicking `Update Data`

#### DIR structure should look like
```
.
├── LICENSE
├── README.md
├── data
│   ├── sample_metadata.csv
│   ├── metadata.csv (will be created on first upate run from the app)
|   ├── metadata_processed.pickle (will be created on first upate run from the app)
├── resources
│   ├── cord19-300d.magnitude (You need to download this file, keep the name same or change in config.cfg)
├── src
│   ├── cord19_app.py
│   ├── config.cfg
│   ├── data_io.py
│   ├── embedding.py
│   ├── tokenizer.py
│   ├── utils.py
│   └── vectorizer.py

... (excluded others)

```

 
#### Running the Streamlit App
```
cd src
streamlit run cord19_app.py
```

**Note: On first run Click on `Update Data` button on sidebar of the app, it will take around 5-7 min, wait for it. Then you can run query. This is only required first time and next when you want to update new data from the source.**

![Landing](img/landing.png)
![QueryResponse](img/query1.png)
![QueryResponse](img/query2.png)

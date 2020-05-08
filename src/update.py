from data_io import DataIO

data = DataIO(autoload=False)
df = data.update()
print(df.shape)

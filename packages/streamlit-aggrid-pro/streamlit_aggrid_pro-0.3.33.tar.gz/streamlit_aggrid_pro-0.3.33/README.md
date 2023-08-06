# streamlit-aggrid-pro

<br>

# Install
```
pip install streamlit-aggrid-pro

```

# Quick Use
Create an example.py file
```python
from st_aggrid_pro import AgGridPro
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
AgGridPro(df)
```
Run :
```shell
streamlit run example.py
```

# 注：
由于aggrid的最新包样式有问题，所以调整代码和样式，紧急升级此包

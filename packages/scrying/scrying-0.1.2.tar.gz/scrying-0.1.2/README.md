# Scrying
### A ScryfallAPI written in Python
<a href="https://colab.research.google.com/drive/1972QB-yQlUi5OIWJGe94s_n1NLxHLTZ3?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>


### Usage:

```
from scrying.main import Scrying

scry = Scrying()

prompt = "f:pauper t:myr"
scry.download_from_url(prompt)
```


N.B: This is used only to retrieve artworks. For personalized or specific requests, **open a PR**.
# rapidgator-api
A Python Wrapper for the official Rapidgator API

Currently not many things are tested I just implemented it like to [documentation](https://rapidgator.net/article/api/) says. If you find any bugs please report them.

### General Usage
Clone the repo and install the requirements with `pip install -r requirements.txt` and then you can use it like this:
```python
from rapidgatorAPI import RapidgatorAPI

rg = RapidgatorAPI("myEmail", "myPassword")
print(rg.info())
```

### TODO
- Test the functions
- Upload it to PyPi
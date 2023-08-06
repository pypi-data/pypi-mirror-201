# DateTime
DateTime is Python package that contains functions to get the current date and time.

## Installation and updating

Use the package manager  [pip](https://pip.pypa.io/en/stable/)  to install package.

## Usage
Features:
-   datetime_funcs.get_date --> retrns current date, wheter in shamsi or miladi
-   datetime_funcs.get_time --> returns current time
-   datetime_funcs.get_datetime --> returns both current date and time in wheater shamsi or miladi format
-   datetime_funcs.get_days_per_month --> returns number of days for a given month
#### Demo of the features:
```python
from  datetime_funcs  import  get_date
from  datetime_funcs  import  get_time
from  datetime_funcs  import  get_datetime
from  datetime_funcs  import  get_days_per_month

print(get_date(persian=True, folder_path=True))
print(get_time(folder_path=False))
print(get_datetime(persian=False, folder_path=False))
print(get_days_per_month(month=6, persian=True))
```
## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)


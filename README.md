# US Bond Yield Curve Visualisation App

## About

This app produces an animation of the US Bond Yield curve over a certain period, taking data from the [US Government Treausry website](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve).

## Preparation
You need Python 3.0 or greater to run the script.

You also need the following libraries installed:

**numpy** - For array operations on the data<br/>
**pandas** - For handling data frames<br/>
**matplotlib** - For plotting graphs and data animation.  `Matplotlib.animation.FuncAnimation` for creating animated plots.<br/>
**requests** - Retrieves data from websites through HTML requests<br/>
**beautifulsoup4** - Parses and extracts information from HTML<br/>
**tkcalendar** - Creates calendar widget in Tkinter<br/>
**tkinter** - Creates the GUI. Core Python library; usually comes along when you install Python.<br/>

```
# Installing dependencies
pip install numpy pandas matplotlib requests beautifulsoup4 tkcalendar

# Running script
python main_app.py
```
## Running the code
To use the app, you only need to run `main_app.py`.
Note that it will take around 10 seconds for the first run of each day as it needs time to access the latest daily data online. The app should launch quicker after the first run.

## License
Licensed under the [MIT License](https://opensource.org/license/mit).



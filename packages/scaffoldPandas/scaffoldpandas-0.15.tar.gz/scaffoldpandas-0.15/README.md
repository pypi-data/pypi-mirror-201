# scaffold-pandas
Helper functions to do common things in Pandas

These are things I learned how to do in Python Pandas, and want to more easily, but it will also include examples of code that helps explain useful ways of solving problems.

## Functions Included:

`scaffold-pandas`.**`byType`**(*`series, printout=False`*)
Returns a dictionary which includes the contents of the series divided into six lists, which are "integers", "strings", "floats", "booleans", "nones", and "others". If the "printout" flag is True, it also prints the counts of each type.

Mostly used to tell you useful things about a column, and enable other tools like returning minimum and maximum values.


`scaffold-pandas`.**`proportionOfTypes`**(*`columnname, printout=False`*)
Returns a dictionary of percentages of the given field types from a column (or series - it's a list, because a column in pandas can be addressed as if it is a list). It uses the same types as **`byType`**, and returns the proportion in percent of that type in the column. If the "printout" flag is True, it also prints the percentages of each type.

A good way to see how many outliers or nulls are in a column without scrolling through it all to figure it out.


`scaffold-pandas`.**`typeCoerce`**(*`mylist, dtype=float`*)
Returns a list where all of the list elements have been forced into the named type (`dtype`).

Useful for casting the whole column into the same type (like when a date column with weird NaN value gets cast all as floats, and you want to fix it, or when you want to get a maximum and minimum value).


`scaffold-pandas`.**`minMaxNumbers`**(*`*lists`*)
Returns a dictionary with a "minimum" and a "maximum" value for one or more lists, coercing all of the list elements to a float if necessary. Assumes that the list elements are non-complex numbers.


`scaffold-pandas`.**`minMaxDates`**(*`*lists`*)
Returns a dictionary with a "minimum" and a "maximum" value for one or more lists which may include dates. Uses `dateutil.parser.parse` to check if a date can be understood from the element, ignoring anything that isn't a possible date.


`scaffold-pandas`.**`makeDateTimeIndex`**(*`dataframe, columnname`*)
Returns a `pandas` Dataframe with a copy of columnname as an index of `datetime` objects.


`scaffold-pandas`.**`plotRowsOverTime`**(*`dataframe, frequency`*)
Display a plot of a Dataframe where the index is datetime objects and the rows are data points. Frequency values are D for day, M for month, Y for year. More information in the `pandas.Grouper` documentation.


`scaffold-pandas`.**`inspectColumn`**(*`columnname, printout=True`*)
Returns a dictionary of useful information about a column. Basics such as how many rows, how many factors, what the proportions of the factors are with respect to the whole column if there are fewer than eleven factors, maximum and minimum values, numbers of possible dates and non-dates, and the number of nulls in the column. If `printout` is True this is also printed to the console.


## Pattern Examples

NOTE: The patterns are at the bottom of the source file, and are commented out by default, so as to prevent this example code from running.

- Merge and de-duplicate two overlapping Dataframes
- Alter the default NA (Not Available) list to match your data
- Pad a column on read using `converters` and string formatting
- Filter a Dataframe based on a column having a value matching one in a list
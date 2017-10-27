# Table of Contents
1. [Prerequisites](README.md#Prerequisites)
2. [How to use](README.md#How-to-use)
3. [Implementation details](README.md#Implementation-details)
4. [Test](README.md#Test)

# Prerequisites

Python 2 or 3. No extra packages are needed. (In practice, if the input data is too large, it is better to use numpy to handle large input and lists)

# How to use

The main python program `main_parse.py` is in src folder.

To run the program, use following command in the root directory (find_political_donors_junyi):

	python ./src/main_parse.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt

The first argument is the input file name and the second and third arguments are two filenames for output.

	
**Or** you can using `run.sh` in the root directory to run it from bash


I also implemented a **multi-process** version of main_parse.py named as `main_parse_multiprocess.py` in src folder. In this implementation I used two processes to handle two different tasks separetely. The running time is ~30% shorter compared to `main_parse.py`. The usage is the same as `main_parse.py`:
	
	python ./src/main_parse_multiprocess.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt

# Implementation details

For there are two different tasks, one is based on `recipeint` and `zipcode` and the other is based on `recipeint` and `time`, I used
two dictionaries to store the data: **`zipDict`** and **`dateDict`**:

The key for **`zipDict`** is `(recipeint,zipcode)` and the value is a list with 5 fields:

* `Amount`: total amount of transactions received so far for recipeint from zipcode
* `n_transactions`:  number of transactions received so far for recipeint from zipcode
* `n_minheap`: number of elements in minheap
* `maxheap`: a maxheap to store half of transactions with smaller or equal to median
* `minheap`: a minheap to store half of transactions with value larger or equal to median
	
To efficiently get the running median of contributions received by recipient from the contributor's zip code streamed, I used two heaps to store
the streamed data sofar and made sure `size(maxheap)==size(minheap) or size(maxheap)==size(minheap)+1`. The running time for each transaction insertion and median calculation 
is `O(log(n))` and `O(1)`. As a result, the total running time is `O(nlog(n))` (n is the total number of valid transactions).


The key for **`dateDict`** is `(recipeint,date)`:
* the value of the **dateDict** a list containing all transactions.

When a new valid transaction was found, it was appended to the list. In the end, the list is sorted to get the median. The running time is limited by sorting, which is `O(nlog(n)` (n is the max length of dateDict[key]).


## Test

The code passed the given test and I also tested it using much larger files (300 M). However, since the file size of github is limited, I only include another medium sized self-created test in the tests folder (test_2). To test the corner case, I added a test without inputfile (invalid input path) and it is in test_nofile. To test the script's ability to handle larger files, I added a large test in test_4

If use the `run_tests.sh` in directory ./insight/testsuite, a tmp folder will be created and all script, input and output can be found there.

To test the individual functions in `main_parse.py`, I also wrote a python unittest code in folder `src`.
To run the test, use the following command in the root directory (find_political_donors_junyi):
```python src/test.py```

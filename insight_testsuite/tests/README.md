## Test

The code passed the given test and I also tested it using much larger files (300 M). However, since the file size of github is limited, I didn't include it here. In the tests folder, I also created several tests to test for corner cases and relative large file:
* `test_1`: original test created by insight
* `test_2`: A medium sized test (2000 lines).
* `test_emptyinput`: EMpty itcont.txt file. Two empty output files(medianvals_by_zip.txt and medianvals_by_date.txt) were generated after running.
* `test_emptyline`: There is one empty line in input  itcont.txt, aiming to test how the scripts deal with invalid lines.
* `test_invalidinput`: The itcont.txt doesn't follow the FEC rule. Test how the scripts handle with invalid lines.
* `test_largefile`: A large test to test how the script handle large files.
* `test_noinput`: No inputfile in input folder.Two empty output files(medianvals_by_zip.txt and medianvals_by_date.txt) were generated after running.


If use the `run_tests.sh` in directory ./insight/testsuite, a tmp folder will be created and all script, input and output can be found there.


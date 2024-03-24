Install Deap, Numpy, and Matplotlib before running. To do so run the command

```bash
pip install numpy deap matplotlib
```

If desired, edit the *args.txt* file before running the GP system. To run the GP system, run the command

```bash
python main.py
```

Running *main.py* will produce a directory called *output* with a structure that looks like the following

 ┣ run0 \
 ┃ ┣ gen0 \
 ┃ ┃ ┣ ind0 \
 ┃ ┃ ┃ ┣ predator.txt \
 ┃ ┃ ┃ ┣ prey0.txt \
 ┃ ┃ ┃ ┣ prey1.txt \
 ┃ ┃ ┃ ┣ ... \
 ┃ ┃ ┣ ind1 \
 ┃ ┃ ┃ ┣ ... \
 ┃ ┃ ┗ ind2 \
 ┃ ┣ hall_of_famers \
 ┃ ┃ ┣ 0.txt \
 ┃ ┃ ┗ 1.txt \
 ┃ ┣ args.txt \
 ┃ ┣ average_values.txt \
 ┃ ┗ best_values.txt \
 ┣ run1 \
 ┃ ┣ ... 

Every time you run *main.py*, a new "run" directory will be created that will essentially contain all the best individuals, best and average values, and arguments used for that particular run.

To view any of the hall of famers you can use the *display.py* script. First, open the script in a text editor and scroll all the way to the bottom. Let's say you have done two runs so you have a *run0* directory and a *run1* directory. To view a hall of famer from *run1*, configure the script to be

```python
if __name__ == "__main__":
    display = Display("args.txt", run=1, gen=0, ind=0)
    display.run()
```

and then run it with the command

```bash
python display.py
```

To generate plots from your runs, open the *getplot.py* script and edit the *runs_to_plot* variable which is located near the top of the script. For example, if I have the runs *run0*, *run1*, *run5*, and *run9*, and I would like to average their values and generate a plot with those values. Then I would change the line near the top to

```python
runs_to_plot = [0, 1, 5, 9]
```

then just run the script with

```bash
python getplot.py
```

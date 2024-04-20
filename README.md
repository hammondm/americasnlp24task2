# Materials for AmericasNLP 2024 task 2

In our paper, we describe three systems and the code for those is here. These draw on code from the repo for the task at: https://github.com/AmericasNLP/americasnlp2024/.

1. Transformer.
    - `doit`: batch script to run code and run evaluation
    - `anlp.py`: python code for network architecture and training
1. Edit trees as transductions
    - `dotest`: batch script to generate and evaluate results
    - `dolang.py`: python code to run experiment
    - `edittree.py`: edit tree implementation, invoked by `dolang.py`
1. Edit trees with morphosyntactic similarity
    - `newmytest`: batch script to generate and evaluate results
    - `newmhtest.py`: python code for baseline, augmented by applying similar rules

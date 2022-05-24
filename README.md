# IBM Model 1

To run this part, the following command will run the IBM model 1 with an iteration
count of 5. The first line will generate an output file that specifies the alignment
which is then used to check on the score.
```
python3 ibm_model1.py 5
python3 eval_alignment.py dev.key ibm_model1.out  
```

# IBM model 2
To run this part, the following command will run the IBM model 2 with an iteration
count of 5. The first line will generate an output file that specifies the alignment
which is then used to check on the score.
```
python3 ibm_model2.py 5
python3 eval_alignment.py dev.key ibm_model2.out  
```
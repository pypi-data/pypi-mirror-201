# What is OCAICM ?
The tool can complete the construction of diffierent dataset classification models with only one line of code, and recommend the optimal model for virtual screening.  
The tool integrates multiple machine learning models, common molecular descriptors and three data set splitting methods.   
The tool integrates the virtual screening function and uses the optimal model to screen the quick screening of the compound library provided by users through a single code.



# How to use this tool ?

## 1 Bulid the environment

1. conda create -n envir_name python=3.8              
2. conda install rdkit rdkit             
3. conda install pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cudatoolkit=10.2 -c pytorch  # need to confirm your cuda>=10.2  
4. conda install -c dglteam dgl==0.4.3post2   
5. conda install **xgboost,hyperopt,mxnet,requests**    
6. pip install PyaiVS   

## 2 Bulid models

### 1 Submit a file in a given .csv format file(Simple single task only needs to provide two columns of content: Smiles and label)              
   such as  (The result output is the optimal model recommendation order considering AUC_ROC and F1_score):                
|Smiles |task1|task2|...|taskn|   
|smiles1|  0  |  0  |...|  1  |   
|smiles2|  0  |  1  |...|  1  |    
...         
|smilesm|  1  |  0  |...|  0  |     
Dataframe including smiles and labels. Can be loaded by pandas.read_csv(file_path). One column includes smiles and other columns for labels.Column names other than smiles column would be considered as task names.                      
    
    >>>from PyaiVS import model_bulid                                
    >>>model_bulid.running('submit_file.csv',run_type='param') 
    >>>model_bulid.running('submit_file.csv',run_type='result') 
    model    des   split   auc_roc  f1_score       acc       mcc
    2   SVM  ECFP4  random  0.969047  0.903497  0.917723  0.831872                     
    
### 2 Parameter setting

model_bulid.running(file_name,out_dir = './',split=None,model=None,FP=None, cpus=4)         
* 1 file_name         
#the submitted file             
* 2 out_dir = './'            
#As the processing can generate some file , we need to give a dir to save this file. If there is no input,by default, it is in the same directory as the submission folder.         
* 3 split=None            
#There are three ways to partition data sets `['random','scaffold','cluster']`.If there is no input, only random will be used by default.          
* 4 model=None            
#There are nine methods for data set modeling `['SVM','RF','KNN','DNN','XGB','gcn','gat','attentivefp','mpnn']`. If there is no input, only SVM will be used by default.           
* 5 FP=None           
#Compound molecular fingerprint, there are four choices `['MACCS','ECFP4','2d-3d','pubchem']`.If there is no input, only MACCS will be used by default.            
* 6 cpus=4            
#When executing the traditional machine learning model algorithm, parallel computing can be selected. By default, 4 tasks are performed simultaneously.         
If a parameter task has been run, the modeling will not be performed again if the same parameter is entered.  
* 7 run_type = 'param'
#run_type setting('param' means to compute best model parameters,'result' means to compute best model auc_roc and mcc)
###### such as:  


    >>>from PyaiVS import model_bulid
    >>>model_bulid.running('Opioid_receptor_δ.csv',model=['SVM','DNN'],run_type='param')
    >>>model_bulid.running('Opioid_receptor_δ.csv',model=['SVM','DNN'],run_type='result')
           model    des   split   auc_roc  f1_score       acc       mcc
         2   SVM  ECFP4  random  0.969047  0.903497  0.917723  0.831872
         4   DNN  ECFP4  random  0.961781  0.881708  0.898430  0.426201
    (The result output is the optimal model recommendation order considering auc_roc and mcc)

### 3 Generated Files


The process will generate a directory with the same name as the input file in the output location.  
submit_file     
>submit_file.csv                   // Copy of original document      
>> submit_file_pro.csv               // Modeling data after data preprocessing         
>> submit_file_auc.csv               // AUC-ROC numerical statistics results of all models     
>> model_save                        // Save folder of modeling model      
>>> KNN                           // Different algorithm models are saved separately            
>>> SVM             
>>>> cluster_cla_MACCS_SVM_bestModel.pkl     
>>>> random_cla_ECFP4_SVM_bestModel.pkl      
>>>> ...     

>>> GCN     
>>> ...   

>> result_save                       // Save folder of modeling data results       
>>> KNN                           // The results of different algorithms are saved separatel        
>>> SVM     
>>> RF      
>>>> random_RF_ECFP4_best.csv  // Model Results of Ten Times Random Seeds with Optimal Parameters        
>>>> random_RF_ECFP4_para.csv  // Saving model results under optimal parameters      
>>>> ...     

>> submit_file.smi                   // Intermediate file generated by padelpy descriptor calculation      
>> submit_file_23d.csv               // 2D-3D descriptor characteristic file       
>> submit_file_pro.bin               // Graph based feature file       
>> submit_file_punchem.csv           // Pubchem fingerprint file       

## 3 Virtual Screen     
model_screen(screen_file=None,model_dir=None,model=None,FP= None,split=None,prop = 0.5,sep = ',',smiles_col =None)
* 1 screen_file   # Compound library files used for screening 
* 2 model_dir # Model generated during modeling in the previous step_ Save location
* 3 model   # the best model recommended by model_bulid.py ,The default value is SVM.
* 4 FP      # the best FP recommended by model_bulid.py ,it can omit if model in graph model.The default value is MACCS.
* 5 split   # the best model recommended by model_bulid.py ,The default value is random.
* 6 prop    # When the prediction probability of the compound is greater than this value, the compound will be identified as an active compound,The default value is 0.5.
* 7 sep     # Content separator of compound library file ,The default value is ','.
* 8 smiles_col #  The column name of the smiles column in the compound library file,The default value is Smiles.

###### such as:       

    >>>from OCAICM import virtul_screen
    >>>virtul_screen.model_screen(model='attentivefp',FP= None,split='random',screen_file='/tmp/screen',prop = 0.5,sep = ',',
        model_dir='/tmp/Opioid_receptor_δ/model_save/',smiles_col=0)
    (Finally, folder screen will be generated under the set mdoel_dir peer directory to store the filtering results)


 

    
    

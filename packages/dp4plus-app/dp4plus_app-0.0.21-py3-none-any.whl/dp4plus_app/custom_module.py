# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:23:46 2023

@author: Franco, Bruno Agustín 
         
DP4+ parameterization module
It uses the DP4+ nmr correlation and calculation modules, as well as having 
its own functions to complete the proccess. 
"""
from collections import Counter
from random import sample

import pandas as pd
import numpy as np
import scipy.stats as st
import glob


##### AGREGAR RELATIVE IMPORTS 
from . import correlation_module as nmr_correl
from . import dp4_module as dp4
from . import bugs_a_warning_module as warn
from . import output_module as output

def tms_mean(tms_g09_tens):
    '''Indicates the two most frequent tensors in a vector.
    It is designed for tms, where the most frequent tensor is the H nucleus 
    and the second is that of C
    '''
    nucleis = Counter(tms_g09_tens.T.tolist()[0])
    H = nucleis.most_common()[0][0]
    C = nucleis.most_common()[1][0]
    return {'C':C, 'H':H}

def add_errors(e_vectors, df_selections, uns_e, sca_e):
    '''Attaches the errors of a molecule to the global parameterization sets
    '''
    e_vectors['Csca'] = np.append(e_vectors['Csca'], sca_e[df_selections['C']])
    e_vectors['Hsca'] = np.append(e_vectors['Hsca'], sca_e[df_selections['H']])
    
    e_vectors['Csp2'] = np.append(e_vectors['Csp2'], uns_e[df_selections['C_sp2']])
    e_vectors['Csp3'] = np.append(e_vectors['Csp3'], uns_e[df_selections['C_sp3']])
    
    e_vectors['Hsp2'] = np.append(e_vectors['Hsp2'], uns_e[df_selections['H_sp2']])
    e_vectors['Hsp3'] = np.append(e_vectors['Hsp3'], uns_e[df_selections['H_sp3']])
    
    return e_vectors

def get_parameters(e_vectors):
    '''Estimates the parameters of the t studen probability distribution
    '''
    param = pd.DataFrame(columns=['n', 'm', 's'],
                         index = ['Csp3','Csp2','Csca',
                                  'Hsp3','Hsp2','Hsca'])
    
    param.loc['Csca'] = st.t.fit(e_vectors['Csca'])
    param.loc['Hsca'] = st.t.fit(e_vectors['Hsca'])
    
    param.loc['Csp2'] = st.t.fit(e_vectors['Csp2'])
    param.loc['Csp3'] = st.t.fit(e_vectors['Csp3'])
    
    param.loc['Hsp2'] = st.t.fit(e_vectors['Hsp2'])
    param.loc['Hsp3'] = st.t.fit(e_vectors['Hsp3'])

    return param

def get_command():
    '''saves the command line of 10% of the files used in the 
    parameterization
    '''
    files= glob.glob('*nmr*.log') + glob.glob('*nmr*.out')
    choose = sample(files, len(files)//10)
    g09command =[]
    
    for file in choose: 
        with open(file,'r') as to_read: 
                for row in to_read.readlines(): 
                    if '#' in row:   
                        g09command.append(row)
                        break
                    
    g09command = Counter(g09command).most_common()[0][0]
    return g09command

def parametrize(xlsx: str, molec_set: list):
    '''Main algorithm of the parameterization process using G09 calculations.
    It uses the correlation module and some funtions of the dp4 module. 
    '''
    try: 
        tms_tens = nmr_correl.G09_tens_matrix(['TMS'])
    except: 
        tms_tens = nmr_correl.G09_tens_matrix(['tms'])
    standard = tms_mean(tms_tens)
    
    e_vectors = {'Csca':np.empty(0), 'Csp2':np.empty(0), 'Csp3':np.empty(0),
                'Hsca':np.empty(0), 'Hsp2':np.empty(0), 'Hsp3':np.empty(0)}
    
    for molec in molec_set:
        exp_data, wtl = nmr_correl.get_exp_data(xlsx, molec)
        df_selections = nmr_correl.selections(exp_data)
        
        tens = nmr_correl.G09_tens_matrix([molec]) #hay q dar una lista a la funcion
        tens = nmr_correl.sort_tens_matrix(tens, [molec], exp_data, wtl) 
        
        uns = dp4.get_uns_shifts(tens,df_selections, standard )
        sca = dp4.get_sca_shifts(uns, df_selections, exp_data)
        
        uns_e = dp4.calc_errors(uns,exp_data)
        sca_e = dp4.calc_errors(sca,exp_data)
        
        e_hl = warn.sca_e_control(exp_data, sca_e)
        exp_hl = warn.exp_data_control(exp_data)
        if e_hl + exp_hl: 
            output.add_highlights_warn(xlsx, molec, 
                                       e_hl, exp_hl, 
                                       param_mode = True)
        
        e_vectors = add_errors(e_vectors, df_selections, uns_e, sca_e)
    
    parameters = get_parameters(e_vectors)
    
    command_line = get_command()
    
    return standard, parameters, command_line
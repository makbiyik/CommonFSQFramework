#!/usr/bin/env python

#
# HERE you do (both for gains/corr's and gain_widths/err's):
# -- em-channel-factor-2-division (if needed, otherwise set it to 1)
# -- absolute calibration
# -- swap  
# -- print suitable for DB
#

                     #2011  #2013
em_factor = 1.0 #0.5     #0.5   #1.0
abs_e_factor = 1.0 #0.015 #0.015 #1.49475628341732545e+02/3.38945322418397409e+04 * 7.82961248095532028e+02/1.33096168279108213e+02

#
# ./final_corr_nice_print_script.py hi1_output.csv
# ./final_tune_nice_print_script.py pPb_corr_output.csv > pPb_corr_db.txt
#

import csv,sys,math
from collections import OrderedDict

def main():
    usage = 'Usage: %s csv-input-file' % sys.argv[0]
#
    try:
        in1filename = './gainwidth__equ_38T_HighGain_input.csv' 
        in2filename = sys.argv[1]
    except:
        print usage; sys.exit(1)

    det_typ_dict = {}
    det_id_dict = {}
    with open(in1filename, 'rb') as f1:
        data = csv.DictReader(f1)
        try:
             for row in data:
                 det_typ_dict[row['sec'],row['mod']] = row['typ']
                 det_id_dict[row['sec'],row['mod']] = '{:x}'.format(int(row['detid'])).upper()###############row['detid']
        except csv.Error, e1:
             sys.exit('file %s, line %d: %s' % (in1filename, data.line_num, e1))

    #corr_val = {}
    corr_val = OrderedDict()
    with open(in2filename, 'rb') as f2:
         data = csv.DictReader(f2)
         try:
              for row in data:
                  corr_val[row['sec'],row['mod']] = row['corr']
         except csv.Error, e1:
             sys.exit('file %s, line %d: %s' % (in2filename, data.line_num, e1))

    #SWAP THE CORRECTIONS for the channels that were found to be swapped
    s5m10 = corr_val[('5','10')]
    s5m12 = corr_val[('5','12')]
    s6m10 = corr_val[('6','10')]
    s6m12 = corr_val[('6','12')] 
    s7m10 = corr_val[('7','10')]
    s7m12 = corr_val[('7','12')]
    corr_val[('5','10')] = s5m12
    corr_val[('5','12')] = s5m10
    corr_val[('6','10')] = s6m12
    corr_val[('6','12')] = s6m10
    corr_val[('7','10')] = s7m12
    corr_val[('7','12')] = s7m10

    #for key in iter(corr_val.keys()):
    for key,value in corr_val.iteritems():
         if (key in det_typ_dict) and (key in det_id_dict):
             #print row['sec'],row['mod'],float(datadict[key])*float(row['corr']),'\n'
             overall_factor = float(corr_val[key]) * abs_e_factor
             if int(key[1]) < 3:
                  overall_factor = float(corr_val[key]) * abs_e_factor * em_factor
             sys.stdout.write('%5g%5s%5s%15s%10.4g%10.4g%10.4g%10.4g%20s\n' % (-1,key[0],key[1],det_typ_dict[key],overall_factor,overall_factor,overall_factor,overall_factor,det_id_dict[key]) )

    f2.close()
    f1.close()

if __name__ == "__main__":
    main()


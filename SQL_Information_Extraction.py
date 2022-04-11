#!/usr/bin/env python
# coding: utf-8

import re
import json

file=open('sample_stored_procedure.sql')
sql_file=file.read()

queries=sql_file.split(';')

out_json={}
q_length=len(queries)

print("Lase query in list is:", queries[67])

queries.pop(67)
print("Dropped last query since it was blank query.")
q_length=len(queries)

extracted_info=[]

for i in range(q_length):
    present_info={}
    source_information=[]
    sub_info={}
    main=re.findall(r"INSERT INTO.+|CREATE.+|DELETE.+|UPDATE.+|USE.+|SELECT COUNT.+",queries[i])[0].split(' ')
    present_info["statement_id"]=i+1
    if 'OR' in main:
        present_info["statement_type"]=' '.join(main[0:3])
    elif 'USE' in main:
        present_info["statement_type"]=' '.join(main[0:2])
    else:
        present_info["statement_type"]=main[0]
    if(main[-2]=="AS"):
        present_info["target_table"]=main[-3]
    elif 'USE' in main:
        present_info["target_table"]=' '.join(main[1:])
    else:
        present_info["target_table"]=main[-1]
    sub=re.findall(r"JOIN.+|FROM.+",queries[i])
    for j in range(len(sub)):
        sub_table=sub[j].split(' ')
        sub_info['type']="JOIN or FROM"
        sub_info['source_table']=sub_table[1]
        source_information.append(sub_info)
    present_info["source"]=source_information
    extracted_info.append(present_info)

json_file=open('sample_stored_procedure.json', 'w')

json_file.write(json.dumps(extracted_info,indent='\t'))

json_file.close()

print("\nExtracted information from SQL query is stored in sample_stored_procedure.json.")



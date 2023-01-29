
import os
import operator
content_list =['Hash','fh.']
counter = 0
with open('client.log','r',encoding='utf-8') as f:
    with open('log_result.txt','w',encoding='utf-8') as w:
        for file_content in f:
            # print(file_content)
            for i in range(len(content_list)):
                # print('12222')
                # print(f'i : {i}')
                if operator.contains(file_content,content_list[i]):
                    # print(file_content,content_list[i])
                    # print(operator.contains(file_content,'wor'))
                    counter = counter + 1
                    # print(counter)
            if not counter == 0:
                print(file_content)
                w.write(file_content[30:])
                counter = 0 
            else:
                counter = 0 

        

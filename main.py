#coding=utf-8
import os
import json
import logging
import traceback
import operator

log_file_name='RN_log_filter.log'

main_path = '.\\'

log_input_dir_name1 = 'log_input1'
log_input_dir_name2 = 'log_input2'

result_file_name = "log_result.txt"
differ_result_name = "differ_result.txt"

Separator_lenth = 100   # 定义分隔符的长度
Separator = '-' * Separator_lenth  

logformat = "[%(asctime)s] [%(levelname)s] %(msg)s"   #log打印的格式

console_handler = logging.StreamHandler()  #输出到控制台
console_handler.setLevel('INFO')   #info以上才输出到控制台
console_handler.setFormatter(logging.Formatter(logformat))   #设置输出到控制台的格式

logging.basicConfig(filename=log_file_name,level=logging.DEBUG, format=logformat)
# 这里定义日志的名字，日志的文本编码，日志的等级

logger = logging.getLogger(__name__)   #logging使用规范，有了这句就可以用logger.xxx了

logger.addHandler(console_handler) #logging输出到控制台
2



def clean_old_log():   #把旧的日志清理掉，这样就不会新旧日志叠在一个文件里了
    try:
        if os.access(log_file_name, os.F_OK):   # 判断log文件是不是存在
            with open(log_file_name, "r+") as f:
                f.truncate()
            return 
        else:                #没有log就什么都不做
            return
    except:
        logger.error(traceback.format_exc())


def check_make_input_dir(
        path:str
):
    input1_path = os.path.join(path,log_input_dir_name1)
    input2_path = os.path.join(path,log_input_dir_name2)
    have_input1 = os.access(input1_path, os.F_OK)
    have_input2 = os.access(input2_path, os.F_OK)
    try:
        if not have_input1:
            logger.info(f'making dir "log_input1" , path : {input1_path}')
            os.makedirs(input1_path, exist_ok=True)
            logger.info(f'making dir "log_input1" successfully')
        else:
            logger.info(f'log_input1 dir found')
        if not have_input2:
            logger.info(f'making dir "log_input2" , path : {input2_path}')
            os.makedirs(input2_path, exist_ok=True)
            logger.info(f'making dir "log_input1" successfully')
        else:
            logger.info(f'log_input2 dir found')
    except:
        logger.error(traceback.format_exc())

        

def have_config():
    have_config= os.access("RN_log_filter_config.json", os.F_OK)    #判断有没有RN_log_filter_config.json，返回布尔值
    if have_config:
        logger.info(f'RN_log_filter_config.json found , reading json')
    if not have_config:
        logger.info(f'RN_log_filter_config.json not found')
    return have_config


def read_config_json(
        config_path:str
): # 此函数返回RN的路径（字符串），要hash的文件后缀名（列表），并吧上述内容传递给search_file函数
    is_read_config=False
    RN_path = ''
    search_content = []
    log_differ_error = False
    try:
        path=f'{config_path}RN_log_filter_config.json'
        with open (path,'r',encoding='utf-8') as f:
            data = json.load(f)
            RN_path = data["RN_path"]     # RN的路径
            search_content = data["search_content"]  # 查找内容
            black_list = data["black_list"] # 这里会读到一个“log文本内容片段”的黑名单列表
            is_read_config = True
            logger.info(f'read RN_log_filter_config.json successfully')
            logger.info(f'RN_path : "{RN_path}"')
            logger.info(f'search_content list:{search_content}')
            logger.info(f'black_list list:{black_list}')
            client_log_dir_path1 = os.path.join(RN_path,log_input_dir_name1)
            client_log_dir_path2 = os.path.join(RN_path,log_input_dir_name2)
            is_read_client_log1 = read_clientLog(client_log_dir_path1,search_content,black_list)
            is_read_client_log2 = read_clientLog(client_log_dir_path2,search_content,black_list)
            if is_read_client_log1 and is_read_client_log2:
                log_differ_error=log_differ(client_log_dir_path1,client_log_dir_path2,RN_path)
            if not is_read_client_log1 and not is_read_client_log2:
                logger.info(f'two client.log not found , skiping log_differ')

            only_one_log = f'one client.log not found , skiping log_differ'
            if is_read_client_log1 and not is_read_client_log2:
                logger.info(only_one_log)
            if is_read_client_log2 and not is_read_client_log1:
                logger.info(only_one_log)
        return is_read_client_log1,is_read_client_log2,log_differ_error
    except:
        logger.error(f'Error reading config.json,please check log file')
        logger.error(traceback.format_exc())
        return 
    
def write_config_json(
        path:str
): #如果没有config.json，那么这个函数会写一个标准json出来，可惜的是返回的布尔值都没用上
    have_configs = have_config()
    is_write_config=False
    if not have_configs:
        json_dict={}
        try:
            path_ = os.path.join(path,'RN_log_filter_config.json')
            RN_path = '.\\'
            black_list = []
            search_content = ['Hash','fh.']
            json_dict['RN_path'] = RN_path
            json_dict['black_list'] = black_list
            json_dict['search_content'] = search_content
            with open(path_,'w',encoding='utf-8') as f:
                json.dump(json_dict,f,ensure_ascii=False,indent = 4)        
            is_write_config = True
            logger.info(f'writing default RN_log_filter_config.json')        
            return is_write_config,have_configs

        except:
            logger.error(f'Error writing default config.json,please check log file')
            logger.error(traceback.format_exc())
            return is_write_config,have_configs
        
    else:
        return is_write_config,have_configs
    
def have_client_log(
        client_log_path:str
):
    status = False
    try:
        if os.access(client_log_path, os.F_OK):
            status = True
        return status

    except:
        logger.error(traceback.format_exc())
    
    
    
def read_clientLog(
        log_path:str,
        search_content:list,
        black_list:list
):    
    # i = 0
    is_read_client_log = False
    black_list_counter = 0  
    counter1 = 0
    counter2 = 0
    total_hash = 0
    searching_list = []
    result_path = os.path.join(log_path,result_file_name)
    client_log_path = os.path.join(log_path,"client.log")
    if have_client_log(client_log_path):
        logger.info(f'client log found , log path : {client_log_path}')
    else:
        logger.info(f'client log not found , please check {client_log_path}')
        return is_read_client_log
    
    try:
        with open(client_log_path,'r',encoding='utf-8') as f:
            logger.info(f'reading {client_log_path}')
            with open(result_path,'w',encoding='utf-8') as w:
                logger.info(f'create file : {result_path}')
                for file_content in f:
                    # print(file_content)
                    for i1 in range(len(search_content)):
                        # print('12222')
                        # print(f'i : {i}')
                        if operator.contains(file_content,search_content[i1]):
                            # print(file_content,content_list[i])
                            # print(operator.contains(file_content,'wor'))
                            counter1 = counter1 + 1
                            # print(counter)
                    for i2 in range(len(black_list)):

                        if operator.contains(file_content,black_list[i2]):
                            counter2 = counter2 + 1 

                    if not counter1 == 0 and counter2 == 0:
                        # logger.info(file_content)
                        
                        seacrhing_result= file_content[30:]
                        # w.write(seacrhing_result)
                        searching_list.append(seacrhing_result)
                        # total_hash += 1
                        counter1 = 0 
                        counter2 = 0
                    else:
                        counter1 = 0 
                        counter2 = 0
                finallist=list(set(searching_list)) 
                # logger.info(total_hash_)
                finallist.sort(reverse = False) # 逆序排序
                logger.info(f'sorting result')
                for ii in finallist:
                    # logger.info(ii)
                    total_hash = total_hash + 1
                    w.write(ii)     # 输出结果
                total_hash_ = f'number of hash : {total_hash}'
                logger.info(f'writing result to {result_path}')
                w.write(f' {total_hash_}')  # 总共search到的hash数量
                is_read_client_log = True
                return is_read_client_log
                

                # w.write(total_hash_)

    except:
        logger.error(traceback.format_exc())

def log_differ(
        client_log_dir_path1:str,
        client_log_dir_path2:str,
        RN_path:str
): 
        differ_error = False
        logger.info(f'running log_differ')
        differ_list1 = []
        differ_list2 = []
        final_list_1 = []
        final_list_2 = []
        the_same = []
        final_list_1_counter = 0
        final_list_2_counter = 0
        the_same_counter = 0
        log_result_path1 = os.path.join(client_log_dir_path1,result_file_name)
        log_result_path2 = os.path.join(client_log_dir_path2,result_file_name)
        differ_result_path = os.path.join(RN_path,differ_result_name)
        try:
            with open(log_result_path1,'r',encoding='utf-8') as f1:
                logger.info(f'reading {log_result_path1}')
                for i1 in f1:
                    i1.replace('\\','/')
                    differ_list1.append(i1)
            with open(log_result_path2,'r',encoding='utf-8') as f2:
                logger.info(f'reading {log_result_path2}')
                for i2 in f2:
                    i2.replace('\\','/')
                    differ_list2.append(i2)
            logger.info(f'comparing hash')
            final_list_1 = list(set(differ_list1).difference(set(differ_list2)))
            final_list_2 = list(set(differ_list2).difference(set(differ_list1)))
            the_same = list(set(differ_list1).intersection(set(differ_list2)))
            logger.info(f'sorting result')
            final_list_1.sort(reverse = False)
            final_list_2.sort(reverse = False)
            the_same.sort(reverse = False)
            with open(differ_result_path,'w',encoding='utf-8') as f3:
                logger.info(f'writing differ result--1 in {differ_result_path}')
                f3.write(f'log_input1 difference hash: \n\n')
                for i3 in final_list_1:
                    f3.write(i3)
                    final_list_1_counter +=1
                logger.info(f'writing differ result--2 in {differ_result_path}')
                f3.write(f'\n{Separator}\n\n')
                f3.write(f'log_input2 difference hash: \n\n')
                for i4 in final_list_2:
                    f3.write(i4)
                    final_list_2_counter += 1
                f3.write(f'\n{Separator}\n\n')
                logger.info(f'writing the same hash  in {differ_result_path}')
                f3.write(f'the same hash: \n\n')
                for i5 in the_same:
                    f3.write(i5)
                    the_same_counter += 1
                f3.write(f'\n\n{Separator}\n\n')
                logger.info(f'writing hash counter in {differ_result_path}')
                f3.write(f'number of log_input1 difference hash : {final_list_1_counter}\n')
                f3.write(f'number of log_input2 difference hash : {final_list_2_counter}\n')
                f3.write(f'number of same hash : {the_same_counter}\n')
                return differ_error
                
        except:
            logger.error(f'error of running log_differ , log_differ stop')
            logger.error(traceback.format_exc())
            differ_error = True
            return differ_error



if __name__ == "__main__":
    # print(list_allfile(r'./'))
    error_counter = 0
    clean_old_log()
    check_make_input_dir(main_path)
    write_config_json(main_path)
    client_log1_status,client_log2_status,differ_error = read_config_json(main_path)
    if not client_log1_status:
        error_counter += 1
    if not client_log2_status:
        error_counter += 1
    if differ_error:
        error_counter += 1
    if not error_counter == 0:
        logger.info(f'program exit')
        exit()
    else:
        logger.info(f'Done')
        # logger.info('123我是中文123')

    
    

#coding=utf-8
import os
import hashlib
import json
import logging
import traceback
import hashlib
import operator

log_file_name='RN_log_filter.log'

logformat = "[%(asctime)s] [%(levelname)s] %(msg)s"   #log打印的格式

console_handler = logging.StreamHandler()  #输出到控制台
console_handler.setLevel('INFO')   #info以上才输出到控制台
console_handler.setFormatter(logging.Formatter(logformat))   #设置输出到控制台的格式

logging.basicConfig(filename=log_file_name,level=logging.DEBUG, format=logformat)
# 这里定义日志的名字，日志的文本编码，日志的等级
logger = logging.getLogger(__name__)   #logging使用规范，有了这句就可以用logger.xxx了

logger.addHandler(console_handler) #logging输出到控制台



def clean_old_log():   #把旧的日志清理掉，这样就不会新旧日志叠在一个文件里了
    try:
        if os.access(log_file_name, os.F_OK):   # 判断log文件是不是存在
            with open(log_file_name, "r+") as f:
                f.truncate()
            return 
        else:                #没有log就什么都不做
            return
    except:
        logging.error(traceback.format_exc())
        

def have_config():
    have_config= os.access("RN_log_filter_config.json", os.F_OK)    #判断有没有config.json，返回布尔值
    if have_config:
        logger.info(f'RN_log_filter_config.json found , reading json')
    if not have_config:
        logger.inifo(f'RN_log_filter_config.json not found')
    return have_config


def read_config_json(
        config_path:str
): # 此函数返回RN的路径（字符串），要hash的文件后缀名（列表），并吧上述内容传递给search_file函数
    is_read_config=False
    RN_path = ''
    search_content = []
    try:
        path=f'{config_path}RN_log_filter_config.json'
        with open (path,'r',encoding='utf-8') as f:
            data = json.load(f)
            RN_path = data["RN_path"]     # RN的路径
            search_content = data["search_content"]  # 查找内容
            black_list = data["black_list"] # 这里会读到一个“log文本内容片段”的黑名单列表
            is_read_config = True
            logger.info(f'read RN_log_filter_config.json successfully , RN_path : "{RN_path}"')
            logger.info(f'checking search_content list:{search_content}')
            logger.info(f'checking black_list list:{black_list}')
            read_clientLog(RN_path,search_content,black_list)
        return 
    except:
        logging.error(f'Error reading config.json,please check log file')
        logging.error(traceback.format_exc())
        return 
    
def write_config_json(
): #如果没有config.json，那么这个函数会写一个标准json出来，可惜的是返回的布尔值都没用上
    have_configs = have_config()
    is_write_config=False
    if not have_configs:
        json_dict={}
        try:
            path = f'.\\RN_log_filter_config.json'
            RN_path = '.\\'
            black_list = []
            search_content = ['Hash','fh.']
            json_dict['RN_path'] = RN_path
            json_dict['black_list'] = black_list
            json_dict['search_content'] = search_content
            with open(path,'w',encoding='utf-8') as f:
                json.dump(json_dict,f,ensure_ascii=False,indent = 4)        
            is_write_config = True
            logger.info(f'writing default RN_log_filter_config.json')        
            return is_write_config,have_configs

        except:
            logging.error(f'Error writing default config.json,please check log file')
            logging.error(traceback.format_exc())
            return is_write_config,have_configs
        
    else:
        return is_write_config,have_configs
    
    
    
def read_clientLog(
        RN_path:str,
        search_content:list,
        black_list:list
):      
    total_hash = 0
    searching_list = []
    result_path = os.path.join(RN_path,"log_result.txt")
    client_log_path = os.path.join(RN_path,"client.log")
    # i = 0
    black_list_counter = 0
    counter = 0
    try:
        with open(client_log_path,'r',encoding='utf-8') as f:
            logger.info(f'reading client.log')
            with open(result_path,'w',encoding='utf-8') as w:
                logger.info(f'create log_result.txt')
                for file_content in f:
                    # print(file_content)
                    for i in range(len(search_content)):
                        # print('12222')
                        # print(f'i : {i}')
                        if operator.contains(file_content,search_content[i]):
                            # print(file_content,content_list[i])
                            # print(operator.contains(file_content,'wor'))
                            counter = counter + 1
                            # print(counter)
                    if not counter == 0:
                        # logger.info(file_content)
                        total_hash += 1
                        seacrhing_result= file_content[30:]
                        # w.write(seacrhing_result)
                        searching_list.append(seacrhing_result)
                        counter = 0 
                    else:
                        counter = 0 
                finallist=list(set(searching_list)) 
                total_hash_ = f'number of hash : {total_hash}'
                logger.info(total_hash_)
                finallist.sort(reverse = False)
                for ii in finallist:
                    w.write(ii)

                # w.write(total_hash_)

    except:
        logging.error(traceback.format_exc())

# def append_list(
#         file_content:str
# ):      # 把匹配到的内容全部缝到一个列表里，然后输出这个列表
#     content_list = []
#     try:
#         content_list.append(file_content)   
#         return content_list
#     except:
#         logging.error(traceback.format_exc())
#         return
        

    


# def sha256_compute(
#         file_path:str
# ): # 得到文件路径后打开文件，计算sha256值，然后返回sha256值
#     try:
#         with open (file_path,'rb') as f:
#             sha256obj = hashlib.sha256()
#             sha256obj.update(f.read())
#             hash_value = sha256obj.hexdigest()
#             return hash_value
#     except:
#         logging.error(traceback.format_exc())


if __name__ == "__main__":
    # print(list_allfile(r'./'))
    clean_old_log()
    write_config_json()
    read_config_json('.\\')
    logger.info(f'Done')

    
    

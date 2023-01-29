#coding=utf-8
import os
import hashlib
import json
import logging
import traceback
import hashlib

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
    have_config= os.access("config.json", os.F_OK)    #判断有没有config.json，返回布尔值
    return have_config


def read_config_json(
        config_path:str
): # 此函数返回RN的路径（字符串），要hash的文件后缀名（列表），并吧上述内容传递给search_file函数
    is_read_config=False
    RN_path = ''
    extension = []
    try:
        path=f'{config_path}RN_log_filter_config.json'
        with open (path,'r',encoding='utf-8') as f:
            data = json.load(f)
            RN_path = data["RN_path"]     # RN的路径
            black_list = data["black_list"] # 这里会读到一个“log文本内容片段”的黑名单列表
            is_read_config = True
            logger.info(f'read config.json successfully , RN_path : "{RN_path}"')
            logger.info(f'checking extension list:{extension}')
            logger.info(f'checking black_list list:{black_list}')
            search_file(RN_path,black_list)
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
            json_dict['RN_path'] = RN_path
            json_dict['black_list'] = black_list
            with open(path,'w',encoding='utf-8') as f:
                json.dump(json_dict,f,ensure_ascii=False,indent = 4)        
            is_write_config = True
            logger.info(f'writing default config.json')        
            return is_write_config,have_configs

        except:
            logging.error(f'Error writing default config.json,please check log file')
            logging.error(traceback.format_exc())
            return is_write_config,have_configs
        
    else:
        return is_write_config,have_configs
    
    
    
def search_file(
        RN_path:str,
        black_list:list
):      # 查文件，config.json读到之后，用os.walk循环查一边目录，可以查出要hash的文件名
        # 然后吧路径和文件名拼在一起，在传给计算sha256的sha256_compute函数
        # sha256_compute函数会把hash结果返回来，然后写进result.txt
        # 这里不查子目录
    file_number = 0
    with open(".\\result.txt", "w", encoding='utf-8') as f:
        logger.info(f'create result.txt')
        i = 0
        black_list_counter = 0
        try:
            logger.info(f'searching file')
            for root,dirs,files in os.walk(RN_path, topdown=True):
                for e in range(len(extension)):
                    for file in files:
                        if file.endswith(extension[i]): 
                            # print(os.path.join(root,file))
                            for d in range(len(black_list)):
                                # logger.info(f'{black_list[d]}')
                                # stage = black_list[d] in file
                                # logger.info(f'{file} {stage}')
                                if black_list[d] in file:
                                    black_list_counter = black_list_counter+1
                                

                            if black_list_counter==0 :   
                                result = str(sha256_compute(os.path.join(root,file)))
                                f.write(f'{file} hash :')
                                logger.info(f'{file} hash : {result}')
                                f.write(f'{result}\n')
                                file_number = file_number + 1

                            black_list_counter=0
                            
                            
                            
                            
                    i=i+1
                    if i==len(extension):
                        Done=True
                        break
                if i==len(extension):
                        break
            f.write(f'checking file number :{file_number}')
            logger.info(f'checking file number :{file_number}')
            f.close()

        except:
            logging.error(traceback.format_exc())


def sha256_compute(
        file_path:str
): # 得到文件路径后打开文件，计算sha256值，然后返回sha256值
    try:
        with open (file_path,'rb') as f:
            sha256obj = hashlib.sha256()
            sha256obj.update(f.read())
            hash_value = sha256obj.hexdigest()
            return hash_value
    except:
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    # print(list_allfile(r'./'))
    clean_old_log()
    write_config_json()
    read_config_json('.\\')
    logger.info(f'Done')

    
    

"""Text Analyzer
# Description:
    This program contains a functions to analyze text files at different
    process step.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/24
"""
import os
import logging
import matplotlib.pyplot as plt

###############################################################################
def analyze_parsed_text(txt_dir, result_dir, threshold):
    """ Analyze Parsed Text
    This function will generate statistics of parsed .txt files.
    
    Parameters
    ----------
    txt_dir: string
        This is the directory of the parsed .txt files.
    result_dir: string
        This is the directory to save the results of analyzed results.
    threshold: float
        This is file size (Kb) threshold. The files with size smaller than the 
        threshold will be considered as abnormal data.
    
    Return
    ------
    anomalies_name: list of strings
        This list contains names of all the abnormal files.
    """
    
    # Logging Settings
    log_path = os.path.join(result_dir, 'parsed_file_stats.log')
    log_name = 'analyze_parsed_text'
    logger = set_logger(log_path, log_name, mode='w', format='%(message)s')
    
    # Read parsed .txt files
    txt_files = [x[2] for x in os.walk(txt_dir)][0]
    file_size = []
    for txt_file in txt_files:
        file_size.append(os.path.getsize(os.path.join(txt_dir, txt_file)) \
                         / 1000) # Unit in KB
    
    # Sort the file by it's size
    sorted_file = [x for (y, x) in sorted(zip(file_size, txt_files))]
    sorted_size = sorted(file_size)
    
    # Get abnormal files
    anomalies_name = [sorted_file[i] for i in range(len(sorted_size)) \
                      if sorted_size[i] < threshold]
    anomalies_size = [x for x in sorted_size if x < threshold]
    
    # Print abnormal files
    logger.info('Anomalies:')
    for i in range(len(anomalies_name)):
        logger.info('- %s (%.2f KB)' %(anomalies_name[i], anomalies_size[i]))
    logger.info('Radio: %d / %d (%.4f %%)' %(len(anomalies_name), \
                len(txt_files), len(anomalies_name) / len(txt_files) * 100))        
    
    # The minial-sized normal file for checking
    logger.info('-- the minial-sized normal file: %s (%.2f KB) --' %( \
          sorted_file[len(anomalies_name)], sorted_size[len(anomalies_name)]))
    
    # Plot histogram
    # Figure settings    
    fig_dir = os.path.join(result_dir, 'fig')
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
    
    fig_size = (15, 5)
    bin_interval = 10
    dpi = 200
    
    plt.figure(figsize=fig_size)
    plt.title('Parsed .txt File Statistics')
    plt.xlabel('File size (KB)')
    plt.ylabel('Number of Files')
    bins = int(max(file_size)/bin_interval)    
    plt.hist(file_size, bins=bins)
    plt.savefig(os.path.join(fig_dir, 'parsed_file_stats.jpg'), dpi=dpi)
    plt.close()
    
    return anomalies_name
###############################################################################
def set_logger(log_path, log_name, mode='a', format='%(message)s'):
    """Set Logger
    This function initialize a file logger object.
    
    Parameters
    ----------
    log_path: string
        This is the path of log file.
    log_name: string
        This is the name of logger object. 
    format: string
        This is the log format.
    
    Returns
    -------
    logger: logging.logger object
        This is the logger object that user can use.
    """
    
    # Logging Settings
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    
    # Delete all the handlers in the logger
    logger.handlers = []
    
    # Set the mode 'a'(apend) -> 'w'(overwrite) 
    file_handler = logging.FileHandler(log_path, mode=mode) 
    file_handler.setLevel(logging.DEBUG)
    
    # Set logging format
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

###############################################################################
def analyze_metadata_type(txt_dir, result_dir):
    """Analyze Metadata Type
    This function analyze the proportion of each metadata type.
    - head_tail_1: The Project Gutenberg style
    - head_tail_2: The metadata is in head in tail of the article
    - tail: the rest of them
    
    Parameters
    ----------
    txt_dir: string
        This is the directory of the parsed .txt files.
    result_dir: string
        This is the directory to save the results of analyzed results.    
    """
    # Initialize statistics
    head_tail_1 = 0
    head_tail_2 = 0
    tail = 0
    special_texts = ['author', 'title', 'license', 'acknowledgements']
    
    # Logging Settings
    log_path = os.path.join(result_dir, 'metadata_stats.log')
    log_name = 'analyze_metadata_type'
    logger = set_logger(log_path, log_name, mode='w', format='%(message)s')
    
    # Read parsed .txt files
    txt_files = [x[2] for x in os.walk(txt_dir)][0]
    for txt_file in txt_files:
        with open(os.path.join(txt_dir, txt_file), 'r') as read_file:
            lines = read_file.readlines()
            meta = ''.join(lines[:20])
            tail_flag = True
            if 'project gutenberg' in meta.lower():
                head_tail_1 += 1
                tail_flag = False
            else:
                meta = ''.join(lines[:20])
                for special_text in special_texts:
                    if special_text in meta.lower():
                        head_tail_2 += 1
                        tail_flag = False
                        break
            if tail_flag:
                tail += 1
    
    # Record statistics
    logger.info('Type 1 (head-tail-1): %d' %head_tail_1)
    logger.info('Type 2 (head-tail-2): %d' %head_tail_2)
    logger.info('Type 3 (tail): %d' %tail)
    logger.info('-> Total: %d' %(head_tail_1 + head_tail_2 + tail))
    
    # Draw pie chart
    # Figure settings    
    fig_dir = os.path.join(result_dir, 'fig')
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
        
    plt.figure()
    fig1, ax1 = plt.subplots()
    ax1.pie([head_tail_1, head_tail_2, tail], 
            labels=['head_tail_1', 'head_tail_2', 'tail'],
            explode = (0.1, 0, 0),
            autopct='%1.1f%%',
            shadow=True,
            startangle=90)
    ax1.axis('equal')    
    plt.savefig(os.path.join(fig_dir,'metadata_type_pie_chart.jpg'), dpi=200)
    plt.close()
    
###############################################################################
if __name__ == '__main__':
    
    # Settings
    # The directory of the parsed .txt files 
    txt_dir = os.path.join(os.path.dirname(__file__), 'txt')
    # The directory to save the analyzed results
    result_dir = os.path.join(os.path.dirname(__file__), 'results')   
    # File size (Kb) threshold
    threshold = 1.0
    
    # Create the folder to save analyzed results
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    # Analyze the file size of the parsed .txt files
    anomalies_name = analyze_parsed_text(txt_dir, result_dir, threshold)

    # Analyze the metadata type of parsed .txt files
    analyze_metadata_type(txt_dir, result_dir)
    
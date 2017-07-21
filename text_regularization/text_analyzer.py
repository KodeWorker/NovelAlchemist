"""Text Analyzer
# Description:
    This program contains a functions to analyze text files at different
    process step.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/21
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
        This is the directory of the parsed .txt files 
    fig_dir: string
        This is the directory to save the figuares of analyzed results
    threshold: float
        This is file size (Kb) threshold. The files with size smaller than the 
        threshold will be considered as abnormal data.
    
    Return
    ------
    anomalies_name: list of strings
        This list contains names of all the abnormal files.
    """
    
    # Logging Settings
    log_name = os.path.join(result_dir, 'parsed_file_stats.log')
    logger = logging.getLogger('analyze_parsed_text')
    logger.setLevel(logging.DEBUG)
    
    # Delete all the handlers in the logger
    logger.handlers = []
    
    # Set the mode 'a'(apend) -> 'w'(overwrite) 
    file_handler = logging.FileHandler(log_name, mode='w') 
    file_handler.setLevel(logging.DEBUG)
    
    # Set logging format
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
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
    logger.info('** next minial-sized normal file: %s (%.2f KB) **' %( \
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
    
import os
from epub_converter import convert_epub_to_txt
from text_analyzer import analyze_parsed_text, analyze_metadata_type
###############################################################################
if __name__ == '__main__':
    
    # Settings
    
    # The directory of the scraped .epub files 
    epub_dir = os.path.join(os.path.dirname(__file__), '..', 'web_scraping', 'epub')
    # The directory of the converted .txt files 
    txt_dir = os.path.join(os.path.dirname(__file__), 'txt')
    # The directory to save the analyzed results
    result_dir = os.path.join(os.path.dirname(__file__), 'results')   
    # File size (Kb) threshold
    threshold = 1.0
    
    # Create the folder to save converted files
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    # Create the folder to save analyzed results
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    # Convert .epub to .txt
    epub_files = [x[2] for x in os.walk(epub_dir)][0]
    for i in range(len(epub_files)):
        print('\rprogress: %d / %d' %(i+1, len(epub_files)), end='\r')
        epub_path = os.path.join(epub_dir, epub_files[i])
        txt_path = os.path.join(txt_dir, \
                                epub_files[i].replace('.epub', '.txt'))
        convert_epub_to_txt(epub_path, txt_path, encode='utf-8')
    print('\n-- All .epub Files Parsed --')
    
    # Analyze parsed .txt files
    anomalies_name = analyze_parsed_text(txt_dir, result_dir, threshold)
    print('-- Parsed Files Analyzed --')
    
    # Remove abnormal files
    for file in anomalies_name:
        os.remove(os.path.join(txt_dir, file))
    print('-- Abnormal Files Removed --')
    
    # Analyze the metadata type of parsed .txt files
    analyze_metadata_type(txt_dir, result_dir)
    print('-- File Metadata Analyzed --')
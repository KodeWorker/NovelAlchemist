"""Metadata Extractor
# Description:
    This program categorize the metadata format into three major types and 
    use different appraoches to extract the contant and metadata.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/24
"""
import os
import shutil
###############################################################################
def extract_metadata(txt_dir, ext_dir, result_dir, purge=False):
    """Extract Metadata
    This function categorize the metadata and extract the metadata and content
    corespondingly.
    
    Parameters
    ----------
    txt_dir: string
        This is the directory of the parsed .txt files.
    ext_dir: string
        This is the directory of the extracted files.
    result_dir: string
        This is the directory to save the results of analyzed results.    
    """
    
    # Settings
#    special_texts = ['author', 'title', 'license', 'acknowledgements']
    
    # Create the extracted dir
    if purge:
        shutil.rmtree(ext_dir)
        os.makedirs(ext_dir)    
    
    # Read parsed .txt files
    txt_files = [x[2] for x in os.walk(txt_dir)][0]
    for i in range(len(txt_files)):
        print('\rprogress: %d / %d' %(i + 1, len(txt_files)), end='\r')
        file_path = os.path.join(txt_dir, txt_files[i])
        txt_ext_dir = os.path.join(ext_dir, txt_files[i].replace('.txt', '').replace('.', ''))        
        
        if not os.path.exists(txt_ext_dir):
            os.makedirs(txt_ext_dir)
        
        with open(file_path, 'r') as read_file:
            lines = read_file.readlines()
            meta = ''.join(lines[:20])
#            tail_flag = True
            if 'project gutenberg' in meta.lower():
                # Process Type 1 Metadata
                extract_type_1(lines, txt_ext_dir)
#                tail_flag = False
            else:
#                meta = ''.join(lines[:20])
#                for special_text in special_texts:
#                    if special_text in meta.lower():
#                        # Process Type 2 Metadata
#                        extract_type_2(lines, txt_ext_dir)
#                        tail_flag = False
#                        break
#            if tail_flag:
#                # Process Type 3 Metadata
#                extract_type_3(lines, txt_ext_dir)
                extract_type_2
###############################################################################
def extract_type_1(lines, txt_ext_dir):

    content_init_idx = 0
    content_end_idx = len(lines) - 1
    
    for i in range(len(lines)):
        if '*** START OF'.lower() in lines[i].lower() and 'PROJECT GUTENBERG'\
        .lower() in lines[i].lower():
            content_init_idx = i + 1
            break
        elif '***START OF'.lower() in lines[i].lower() and 'PROJECT GUTENBERG'\
        .lower() in lines[i].lower():
            content_init_idx = i + 1
            break
        elif 'The Project gratefully accepts contributions of money, time, \
        public domain materials, or royalty free copyright licenses. Money \
        should be paid to the: "Project Gutenberg Literary Archive Foundation.\
        "'.lower() in lines[i].lower():
            content_init_idx = i + 2
            break
        elif 'Just search by the first five letters of the filename you want, \
        as it appears in our Newsletters.'.lower() in lines[i].lower():
            content_init_idx = i + 2
            break        
        elif 'This etext was prepared'.lower() in lines[i].lower() and \
        i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif 'This etext was produced'.lower() in lines[i].lower() and \
        i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif 'Project Gutenberg of Australia go to http://gutenberg.net.au'.\
        lower() in lines[i].lower():
            content_init_idx = i + 1
            break
        elif 'SMALL PRINT'.lower() in lines[i].lower() and \
        'FOR PUBLIC DOMAIN ETEXTS'.lower() in lines[i].lower():
            content_init_idx = i + 1
            break
        
        # Special case: An-Old-Womans-Tale
        elif 'Character set encoding'.lower() in lines[i].lower():
            content_init_idx = i + 1
            break

    for i in range(len(lines)-1, -1, -1):  
        if '*** END OF'.lower() in lines[i].lower() and 'PROJECT GUTENBERG'.\
        lower() in lines[i].lower():
            content_end_idx = i - 1
            break
        elif '***END OF'.lower() in lines[i].lower() and 'PROJECT GUTENBERG'.\
        lower() in lines[i].lower():
            content_end_idx = i - 1
            break        
        elif 'THE END' in lines[i]:
            content_end_idx = i - 1
            break
        elif 'This file should be named'.lower() in lines[i].lower() and \
        '.txt' in lines[i] and '.zip' in lines[i] and i > len(lines)/2:
            content_end_idx = i - 1
            break
        
        # Special case: The-Wandering-Jew
        elif 'end' in lines[i].lower() and 'etext' in lines[i].lower() and \
        'Project Gutenberg'.lower() in lines[i].lower() and ', v' in \
        lines[i].lower():
            lines[i] = ''
            continue
        
        elif 'END OF'.lower() in lines[i].lower() and 'PROJECT GUTENBERG'.\
        lower() in lines[i].lower() and 'edition' in lines[i].lower():
            content_end_idx = i - 1
            break
        
        elif 'etext' in lines[i].lower() and 'Project Gutenberg'.lower() \
        in lines[i].lower() and i > len(lines)/2:
            content_end_idx = i - 1
            break
        
        # Special case: An-Old-Womans-Tale
        elif '***** This file should be named' in lines[i]:
            content_end_idx = i - 1
            break
        
    content = lines[content_init_idx: content_end_idx]
    if 'from http://' in content[-1]:
        content = content[:-1]
    metadata = lines[:content_init_idx] + lines[content_end_idx:]    
        
    # Write content and metadata files
    with open(os.path.join(txt_ext_dir, 'content.txt'), 'w') as write_file:
        write_file.writelines(content)
    with open(os.path.join(txt_ext_dir, 'metadata.txt'), 'w') as write_file:
        write_file.writelines(metadata)
    
###############################################################################
def extract_type_2(lines, txt_ext_dir):
    content_init_idx = 0
    content_end_idx = len(lines) - 1    
    
    for i in range(len(lines)):
        if 'CONTENTS'.lower() in lines[i].lower() and i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif ('-' in lines[i] or ('*') in lines[i]) and \
        ('chapter' in lines[i+1].lower() or 'one' in lines[i+1].lower()) and\
         i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif 'for more information' in lines[i].lower() and 'visit' in \
        lines[i].lower() and i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif 'publishe' in lines[i].lower() and i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif 'illustration' in lines[i].lower() and i < len(lines)/2:
            content_init_idx = i + 1
            break
        elif 'a free download from http://' in lines[i].lower() and \
        i < len(lines)/2:
            content_init_idx = i + 1
            break
    
    for i in range(len(lines)-1, -1, -1):
        if 'THE END' in lines[i]:
            content_end_idx = i - 1
            break
        if 'END' in lines[i]:
            content_end_idx = i - 1
            break
        elif i != len(lines)-1 and ('-' in lines[i] or ('*') in lines[i]) and \
        'acknowledgements' in lines[i+1].lower() and i > len(lines)/2 :
            content_end_idx = i - 1
            break
        elif i != len(lines)-1 and ('-' in lines[i] or ('*') in lines[i]) and \
        'creative commons' in lines[i+1].lower() and i > len(lines)/2 :
            content_end_idx = i - 1
            break
        elif 'biography' in lines[i].lower() and i > len(lines)/2:
            content_end_idx = i - 1
            break
        elif 'About the Author'.lower() in lines[i].lower() and \
        i > len(lines)/2:
            content_end_idx = i - 1
            break
        elif '2 RTEXT' in lines[i]:
            content_end_idx = i - 1
            break
        elif 'Titles by'.lower() in lines[i].lower() and i > len(lines)/2:
            content_end_idx = i - 1
            break
        elif 'visit http://'.lower() in lines[i].lower() and i > \
        len(lines)/2:
            content_end_idx = i - 1
            break
        elif i != len(lines)-1 and ('-' in lines[i] or ('*') in lines[i]) and \
        'finished' in lines[i+1].lower() and i > len(lines)/2 :
            content_end_idx = i - 1
            break
        elif 'Creative Commons'.lower() in lines[i].lower() and\
        i > len(lines)/2 and i != len(lines) - 1:
            content_end_idx = i - 1
            break
            
    content = lines[content_init_idx: content_end_idx]
    if 'from http://' in content[-1]:
        content = content[:-1]
    metadata = lines[:content_init_idx] + lines[content_end_idx:]
    
    # Write content and metadata files
    with open(os.path.join(txt_ext_dir, 'content.txt'), 'w') as write_file:
        write_file.writelines(content)
    with open(os.path.join(txt_ext_dir, 'metadata.txt'), 'w') as write_file:
        write_file.writelines(metadata)
###############################################################################
#def extract_type_3(lines, txt_ext_dir):
#    extract_type_2(lines, txt_ext_dir)
###############################################################################
if __name__ == '__main__':
    
    # Settings
    # The directory of the parsed .txt files 
    txt_dir = os.path.join(os.path.dirname(__file__), 'txt')
    # The directory of the extracted files 
    ext_dir = os.path.join(os.path.dirname(__file__), 'ext')
    # The directory to save the analyzed results
    result_dir = os.path.join(os.path.dirname(__file__), 'results')
    
    # Create the folfer to save extracted metadata and content
    if not os.path.exists(ext_dir):
        os.makedirs(ext_dir)
    # Create the folder to save analyzed results
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    extract_metadata(txt_dir, ext_dir, result_dir, purge=True)
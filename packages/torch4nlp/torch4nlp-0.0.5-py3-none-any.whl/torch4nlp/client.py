task = 'text_classification'

if task == 'text_classification':
    from text_classification.data_utils import DataProcessor
    from configparser import ConfigParser

    parser = ConfigParser()
    res = parser.read('text_classification.cfg')
    
    print(res.sections)


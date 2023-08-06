class Example:
    def __init__(self, text, label1, label2) -> None:
        self.label1, label2


class DataProcessor:
    def __init__(self, line_parser, label_mappings, max_multilabel_nums=[]) -> None:
        self.label_mappings = label_mappings
        self.max_multilabel_nums = max_multilabel_nums
        self.line_parser = line_parser
    

    
class DataProcessor():
    def __init__(self, label_mappings):
        self.label_mappings = label_mappings
    

    def init_tokenizer(str_or_class='bert'):
        return tokenizer
    
    def get_dataloader_from_ann_file(infile):
        return dataloader
    
    def load_dataloader_from_ann_file(infile, chunk):
        yield dataloader

    def get_tensors_from_unann_file(infile):
        pass
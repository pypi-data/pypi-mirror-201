# youngnlp

youngnlp is a pytorch-based natural language processing library for nlu and nlg.

定义文件解析函数

```python
def line_parser(line):
    text, label1, label2 = line.rstrip().split('\t')
    

    model_output
    {
        'name': 'label1_logits',
        'loss_fn': 'cross_entropy',
        'corresponding_label': 'label1',
        'weight': 1
    },
    {
        'name': 'label2_logits',
        'loss_fn': 'circle_loss',
        'label': 'label2',
        'weight': 1
    }


```
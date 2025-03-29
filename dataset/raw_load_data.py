import os
import json
import pandas as pd  # 新增导入 pandas

def load_data_aitw_l1(base_path):
    # 加载 aitw-l1.json 文件中的 JSON 数据
    json_path = os.path.join(base_path, 'aitw-l2.json')
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    # list len 18992
    # json_data[0].keys() dict_keys(['image', 'conversations'])
    # len(json_data[0]['conversations']) 4
    return json_data

def aitw_to_dataset(json_data):
    # 将 aitw-l1.json 数据转换为另一种格式的数据集
    dataset = []
    i = 0
    for item in json_data:
        # breakpoint()
        local_dir ='/datasets_aguvis/aitw-v1/images'
        image = os.path.join(local_dir, item['image'])
        # image = item['image']
        conversations = item['conversations']
        if len(conversations) >= 4:
            assert conversations[1]['from'] == 'human'
            prompt = conversations[1]['value']
            assert conversations[3]['from'] == 'gpt'
            solution = '<answer>'+conversations[3]['value']+'</answer>'
            # dict_keys(['image', 'prompt', 'solution'])
            dataset.append({
                'image': image, # googleapps_1984213201603669913_8.jpg'
                'problem': prompt, # instruct + previous actions
                'solution': solution # pyautogui.click(x=0.963, y=0.064
            })
        i += 1
        if i > 100:
            break
    # breakpoint()
    return dataset

def save_dataset(dataset, save_path):
    # 将数据集存储到指定路径的 parquet 文件中
    df = pd.DataFrame(dataset)
    df.to_parquet(save_path, index=False)

def save_dataset_jsonl(dataset, save_path):
    # 将数据集存储到指定路径的 JSON 文件中
    with open(save_path, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
# 示例调用
base_path = '/datasets_aguvis'
json_data = load_data_aitw_l1(base_path)
dataset = aitw_to_dataset(json_data)
# save_path = 'aitw-l1-v1-2000.parquet'
# save_dataset(dataset, save_path)
save_path = 'aitw/aitw-l1-v1-100.jsonl'
save_dataset_jsonl(dataset, save_path)

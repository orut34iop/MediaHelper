import json
from googletrans import Translator

def translate_tags(input_file, output_file):
    """
    读取输入文件中的英文标签名，翻译为中文，并输出为字典文件。
    :param input_file: 包含英文标签名的文本文件，每行为一个标签名。
    :param output_file: 输出的字典文件，包含翻译后的标签名。
    """
    # 创建翻译器对象
    translator = Translator()

    # 初始化字典
    tags_dict = {}

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行首行尾的空白字符
            tag = line.strip()
            if tag:
                # 翻译标签
                try:
                    # 使用 translate 方法进行翻译
                    translated = translator.translate(tag, src='en', dest='zh-cn')
                    # 确保翻译结果是字符串类型
                    if hasattr(translated, 'text'):
                        tags_dict[tag] = translated.text
                        print(f"Translated: {tag} -> {translated.text}")
                    else:
                        print(f"Failed to translate: {tag}. No 'text' attribute found.")
                except Exception as e:
                    print(f"Failed to translate: {tag}. Error: {e}")

    # 将字典写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(tags_dict, file, ensure_ascii=False, indent=4)

    print(f"Translation completed. Output saved to {output_file}")





if __name__ == "__main__":
    # 获取用户输入的目录路径
    input_file = r"C:\Users\wiz\Desktop\dev\MediaHelper\movie_tags.log"
    output_file = r"C:\Users\wiz\Desktop\dev\MediaHelper\movie_tags_cn.log"
    translate_tags(input_file, output_file)
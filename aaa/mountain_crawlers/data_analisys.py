import os
from typing import List
from PIL import Image
from .constants import root


class PV:
    """圖形驗證"""

    @property
    def platform(self):
        return self.__class__.__name__

    @staticmethod
    def get_projection_x(image: Image, **kwargs) -> List[int]:
        """
        获取x轴投影
        :param image:
        :return:
        """

        width, height = image.size
        p_x = [0 for _ in range(width)]

        for h in range(height):
            for w in range(width):
                if image.getpixel((w, h)) == 0:
                    p_x[w] = 1
        return p_x

    @staticmethod
    def get_split_seq(projection_x: list, **kwargs) -> List[List[int]]:
        """
        :param projection_x:
        :return: [[起始位置, 长度]]
        """
        res = []
        for idx in range(len(projection_x) - 1):
            p1 = projection_x[idx]
            p2 = projection_x[idx + 1]
            if p1 == 1 and idx == 0:
                res.append([0, 1])  # 如果第一个点为黑， 则起始点为0， 长度为1
            elif p1 == 1 and p2 == 1:
                res[-1][1] += 1  # 长度加1
            elif p1 == 0 and p2 == 1:  # 新数字
                res.append([idx + 1, 1])
            else:
                continue
        return res

    def split_image(self, image: Image, **kwargs) -> List[Image.Image]:
        """
        图片分割
        :param image:
        :return:
        """
        split_seq = self.get_split_seq(self.get_projection_x(image))
        length = len(split_seq)
        images = [[] for _ in range(length)]
        result = []
        width, height = image.size
        for h in range(height):
            line = [image.getpixel((w, h)) for w in range(width)]
            for idx in range(length):
                pos, img_len = split_seq[idx]
                images[idx].append(line[pos: pos + img_len])

        for idx in range(length):
            new_data = []
            height = 0
            for data in images[idx]:
                if 0 in data:  # [255, 0]
                    height += 1
                    new_data += data
            child_img = Image.new('L', (split_seq[idx][1], height))
            child_img.putdata(new_data)
            child_img.save(f'{idx}.png')
            result.append(child_img)
        return result

    @staticmethod
    def _analysis(image: Image.Image, trained_data: List) -> str:
        """
        对比分析，返回相似度最高的值
        :param image:
        :param trained_data:
        :return:
        """
        res = -1
        total_same = 0
        data = list(image.getdata())
        for num in range(len(trained_data)):
            for per_img in trained_data[num]:
                idx = min(len(data), len(per_img))
                same = 0
                for i in range(idx):
                    if data[i] == per_img[i]:
                        same += 1
                if same > total_same:
                    total_same = same
                    res = num
        return str(res)

    def get_trained_data(self, num=10, platform=None) -> List[List]:
        """
        获取训练数据集
        :return:
        """
        platform = platform or self.platform
        trained_data = []
        for i in range(num):
            trained_data.append([])
            sample_dir = os.listdir(os.path.join(root(f'mountain_crawlers/trained/{platform}'), f'{i}'))
            for file in sample_dir:
                fn = os.path.join(root(f'mountain_crawlers/trained/{platform}'), f'{i}', file)
                img = Image.open(fn)
                trained_data[i].append(list(img.getdata()))
                img.close()
        return trained_data

    @staticmethod
    def crop(image: Image, crop_size: tuple) -> Image.Image:
        """
        裁剪
        :param image:
        :param crop_size:
        :return:
        """
        cropped = image.crop(crop_size)
        return cropped

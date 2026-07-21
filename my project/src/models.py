# src/models.py
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import time

class Comment:
    def __init__(self, commenter, text):
        self.commenter = commenter
        self.text = text
        self.time = datetime.now().strftime("%H:%M:%S")

class Content:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.likes = 12400
        self.comments = []
        self.publish_time = datetime.now().strftime("%Y-%m-%d")

    def add_like(self):
        self.likes += 1

    def add_comment(self, commenter, text):
        new_comment = Comment(commenter, text)
        self.comments.append(new_comment)
        print(f"🔴 【实时互动流】@{commenter} 刚刚发表评论: \"{text}\" (当前总评论数: {len(self.comments)})")

    def generate_xiaohongshu_card(self, filename="xiaohongshu_post.png"):
        width, height = 800, 1100
        image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        font_path = self._get_system_font()
        try:
            font_title = ImageFont.truetype(font_path, 28)
            font_text = ImageFont.truetype(font_path, 20)
            font_small = ImageFont.truetype(font_path, 16)
        except:
            font_title = font_text = font_small = ImageFont.load_default()

        # 1. 顶部栏
        draw.rectangle([0, 0, width, 80], fill=(245, 245, 245))
        draw.text((40, 25), f"@{self.author}", fill=(50, 50, 50), font=font_title)
        draw.rounded_rectangle([660, 22, 760, 60], radius=18, fill=(255, 36, 66))
        draw.text((690, 30), "关注", fill=(255, 255, 255), font=font_text)

        # 2. 中间模拟区
        draw.rectangle([40, 100, 760, 600], fill=(240, 242, 245), outline=(220, 220, 220))
        draw.text((250, 340), "[ 多媒体内容动态渲染区 ]", fill=(150, 150, 150), font=font_text)

        # 3. 标题与正文
        draw.text((40, 630), self.title, fill=(20, 20, 20), font=font_title)
        desc_text = "实时多线程并发评论模拟中，观察不同用户动态发送的效果！#Python多线程 #实时交互"
        draw.text((40, 680), desc_text, fill=(80, 80, 80), font=font_text)

        # 4. 数据统计
        draw.line([(40, 750), (760, 750)], fill=(230, 230, 230), width=1)
        draw.text((40, 770), f"❤️ 点赞: {self.likes}", fill=(255, 36, 66), font=font_text)
        draw.text((240, 770), "⭐ 收藏: 3,420", fill=(120, 120, 120), font=font_text)
        draw.text((440, 770), f"💬 实时评论: {len(self.comments)}", fill=(120, 120, 120), font=font_text)

        # 5. 动态评论区（展示最新的多条评论）
        draw.rectangle([40, 820, 760, 1050], fill=(249, 249, 249), outline=(235, 235, 235))
        draw.text((60, 840), "实时弹出的评论区：", fill=(100, 100, 100), font=font_small)
        
        start_y = 875
        if not self.comments:
            draw.text((60, start_y), "暂无评论...", fill=(150, 150, 150), font=font_small)
        else:
            # 倒序取最新的几条评论展示在页面上
            recent_comments = self.comments[-4:]
            for c in recent_comments:
                comment_str = f"[{c.time}] @{c.commenter}: {c.text}"
                draw.text((60, start_y), comment_str, fill=(60, 60, 60), font=font_small)
                start_y += 35

        image.save(filename)

    def _get_system_font(self):
        if os.name == 'nt':
            return "C:/Windows/Fonts/msyh.ttc"
        elif os.name == 'posix':
            return "/System/Library/Fonts/PingFang.ttc"
        return "arial.ttf"

class ImageNote(Content):
    def __init__(self, title, author, image_count):
        super().__init__(title, author)
        self.image_count = image_count

class VideoNote(Content):
    def __init__(self, title, author, duration):
        super().__init__(title, author)
        self.duration = duration

class User:
    def __init__(self, username):
        self.username = username
        self.contents = []

    def publish_content(self, content_obj):
        self.contents.append(content_obj)

class ContentFactory:
    @staticmethod
    def auto_create_content(title, author, **kwargs):
        if "image_count" in kwargs:
            return ImageNote(title, author, image_count=kwargs["image_count"])
        elif "duration" in kwargs:
            return VideoNote(title, author, duration=kwargs["duration"])
        else:
            raise ValueError("无法识别内容类型！")
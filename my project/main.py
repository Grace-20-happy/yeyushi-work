# main.py
from src.models import User, ContentFactory
import threading
import time
import random

# 定义一个模拟用户实时发送评论的函数
def simulated_user_comment(note, username, texts):
    # 随机等待 1 到 4 秒，模拟不同用户在网络另一端输入的速度差
    delay = random.uniform(1.0, 4.0)
    time.sleep(delay)
    
    # 随机挑选一句评论内容发送
    text = random.choice(texts)
    note.add_comment(username, text)
    
    # 每来一条新评论，就动态刷新并重新生成一张实时的 PNG 界面图
    note.generate_xiaohongshu_card("xiaohongshu_realtime_preview.png")

if __name__ == "__main__":
    print("=== 小红书多用户实时评论并发模拟系统启动 ===\n")
    
    # 1. 博主发布笔记
    blogger = User("知安")
    note = ContentFactory.auto_create_content(
        title="Python面向对象期末大作业:多线程高分技巧",
        author=blogger.username,
        image_count=6
    )
    blogger.publish_content(note)
    print(f"笔记《{note.title}》已成功上线，等待用户实时围观...\n")

    # 2. 准备几组不同用户的名字和常用评论库
    user_pool = [
        ("张同学", ["太强了，多线程秒懂！", "学到了，这就去加进大作业", "支持大佬！"]),
        ("李学长", ["工厂模式和多线程结合得很妙", "求源码合集~", "已三连支持！"]),
        ("助教老师", ["架构设计很规范，面向对象拿捏了", "不错，有创新点", "期末加分项！"]),
        ("王同学", ["刚好卡在怎么模拟实时评论，救了大命", "666，代码跑通了"]),
        ("路人甲", ["前排围观大神", "进来学习一下OOP"])
    ]

    # 3. 创建多个线程，模拟不同用户在同一时间段并发访问并发送实时评论
    threads = []
    for username, texts in user_pool:
        # 每一个用户启动一个独立的线程
        t = threading.Thread(target=simulated_user_comment, args=(note, username, texts))
        threads.append(t)
        t.start()

    # 4. 等待所有用户评论线程执行完毕
    for t in threads:
        t.join()

    # 为了让代码里能直接调用上面名字的实时生成，我们给 Content 临时补一个方法别名
    # (或直接用生成的默认图片)
    note.generate_xiaohongshu_card("xiaohongshu_realtime_preview.png")

    print("\n=== 所有用户评论结束，最终实时界面图已保存为: xiaohongshu_realtime_preview.png ===")
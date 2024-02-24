from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent

from .exchange import get_redirect_url
from .limiter import limiter
from .get import get_msgurl
from .post import get_msg
from io import BytesIO

###################

erro = "https://moetu.org/image/Ur3aj"

food = on_command("随机美食", priority=5, block=True)
wp = on_command("随机壁纸", priority=5, block=True)
re = on_command("运气检测", priority=5, block=True)
day_ = on_command("每日新闻", priority=5, block=True)
msn = on_command("微软美图", priority=5, block=True)
sese = on_command("sese")


@wp.handle()
async def _handle(matcher: Matcher, event: MessageEvent, bot: Bot):
    user_id = event.user_id
    if not limiter.check(user_id):
        left_time = limiter.left_time(user_id)
        await matcher.finish(f"我知道你急了.但是你先别急,cd还有{left_time}秒")
        return

    limiter.start_cd(user_id)
    # url2='https://image.anosu.top/pixiv/direct'
    # url2="https://moe.anosu.top/img"
    # url = get_redirect_url(url2)

    url = get_redirect_url("https://iw233.cn/api.php?sort=iw233")
    base64 = await get_msgurl(url)
    byte_data = BytesIO(base64)
    pic = byte_data.getvalue()

    try:
        await wp.send(
            "您点的图来了{}".format(url) + MessageSegment.image(file=url, cache=False),
            at_sender=True,
        )
    except Exception as e:
        await wp.finish(
            "tx风控了..." + MessageSegment.image(file=erro, cache=False), at_sender=True
        )
    pass


@re.handle()
async def _handle(matcher: Matcher, event: MessageEvent, bot: Bot):
    user_id = event.user_id
    if not limiter.check(user_id):
        left_time = limiter.left_time(user_id)
        await re.finish(f"我知道你很非.但是你先别急,cd还有{left_time}秒")
        return

    limiter.start_cd(user_id)
    # msgs = []
    # url =
    # url=get_redirect_url("https://iw233.cn/API/Random.php")
    url = get_redirect_url("https://iw233.cn/api.php?sort=top")
    base64 = await get_msgurl(url)

    byte_data = BytesIO(base64)
    pic = byte_data.getvalue()

    # url = get_msg2('https://api.lolicon.app/setu/v2')
    try:
        await re.send(
            "看看你的运气{}".format(url) + MessageSegment.image(file=pic, cache=False),
            at_sender=True,
        )
    except Exception as e:
        await re.finish("tx风控了..." + str(e))
    pass


@food.handle()
async def _handle(matcher: Matcher, event: MessageEvent):
    user_id = event.user_id
    if not limiter.check(user_id):
        left_time = limiter.left_time(user_id)
        await matcher.finish(f"我知道你很饿.但是你先别急,cd还有{left_time}秒")
        return

    limiter.start_cd(user_id)

    url = get_redirect_url("https://source.unsplash.com/1600x900/?food")
    # await re.send("haha我不给")
    await food.finish(MessageSegment.image(file=url, cache=False), at_sender=True)


@msn.handle()
async def _handle(matcher: Matcher, event: MessageEvent):
    url = get_redirect_url("https://api.vvhan.com/api/bing?rand=sj&size=1920x1680")
    await msn.finish(MessageSegment.image(file=url, cache=False), at_sender=True)


@day_.handle()
async def _handle(matcher: Matcher, event: MessageEvent):
    url = "https://v2.alapi.cn/api/zaobao"
    token = "VNk9bbtpNdCSO702"
    msg = await get_msg(url, token)
    await day_.finish(MessageSegment.image(file=msg, cache=False), at_sender=True)


@sese.handle()
async def _handle(matcher: Matcher, event: MessageEvent):
    url = get_redirect_url("https://api.vvhan.com/api/girl")

    user_id = event.user_id

    if not limiter.check(user_id):
        left_time = limiter.left_time(user_id)
        await matcher.finish(f"我知道你想要打∠.但是你先别急,cd还有{left_time}秒")
        return

    limiter.start_cd(user_id)

    await sese.finish(MessageSegment.image(file=url, cache=False), at_sender=True)

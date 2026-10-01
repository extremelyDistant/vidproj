# vidproj.py
from pathlib import Path
import click
from datetime import datetime

# ========== 【根据你思维导图更新的目录树，不要改前缀数字】 ==========
DIR_TREE = [
    "01_工程文件",
    "02_原始素材/01_图片",
    "02_原始素材/02_音频",
    "02_原始素材/03_原素材/01_时间_机型_机位",
    "02_原始素材/04_转码素材",
    "03_素材/01_视频",
    "03_素材/02_音乐",
    "03_素材/03_音频",
    "03_素材/04_音效",
    "04_特效/01_素材",
    "04_特效/02_导出/01_视频",
    "04_特效/02_导出/02_图片",
    "04_特效/02_导出/03_音频",
    "05_字幕/01_工程文件",
    "05_字幕/02_文稿",
    "05_字幕/03_音频文件",
    "06_导出/01_成片",
    "06_导出/02_小样",
    "06_导出/03_音频",
    "07_通用素材/01_片头片尾",
    "07_通用素材/02_logo",
    "08_封面",
    "09_归档",
]

def sanitize_name(name: str) -> str:
    """过滤操作系统非法文件名，自动替换为下划线"""
    bad_chars = r'\/:*?"<>|'
    for c in bad_chars:
        name = name.replace(c, "_")
    return name

@click.group()
def cli():
    """vidproj：视频项目脚手架工具，一键生成思维导图规范文件夹 + 素材批量重命名"""
    pass

@cli.command("new")
@click.argument("project_name")
def new_project(project_name):
    """新建视频项目脚手架：vidproj new 20261001_短视频项目"""
    root = Path(sanitize_name(project_name))
    if root.exists():
        click.echo(f"⚠️ 项目文件夹【{root}】已存在，终止操作，防止误覆盖")
        return
    for sub_path in DIR_TREE:
        full_path = root / sub_path
        full_path.mkdir(parents=True, exist_ok=True)
    click.echo(f"✅ 项目创建完成！根目录完整路径：\n{root.resolve()}")

@cli.command("rename_raw")
def rename_raw():
    """批量重命名原始素材，模板：时间_机型_机位.后缀（交互式录入）
    建议：在 02_原始素材/03_原素材/01_时间_机型_机位 目录执行"""
    cwd = Path.cwd()
    media_ext = {".mov", ".mp4", ".mxf", ".m4v", ".wav", ".mp3"}
    medias = [f for f in cwd.glob("*") if f.is_file() and f.suffix.lower() in media_ext]
    if not medias:
        click.echo("❌ 当前目录没有找到视频/音频素材")
        return
    click.echo(f"📋 共发现 {len(medias)} 个媒体文件，预览重命名清单")
    for f in medias:
        shoot_time = click.prompt(f"\n文件【{f.name}】拍摄时间(格式 202610011430)")
        camera_model = click.prompt(f"【{f.name}】机型", default="UnknownCam")
        cam_pos = click.prompt(f"【{f.name}】机位", default="Cam01")
        new_name = f"{shoot_time}_{camera_model}_{cam_pos}{f.suffix}"
        new_path = cwd / sanitize_name(new_name)
        click.echo(f"预览：{f.name} → {new_name}")
        if click.confirm("确认执行本条改名?", default=False):
            if new_path.exists():
                click.echo("⚠️ 同名文件已存在，跳过")
                continue
            f.rename(new_path)
            click.echo("✅ 改名成功")

@cli.command("rename_export")
def rename_export():
    """批量重命名成片，模板：时间_片名_分辨率_编码_格式_导出人_备注_版本
    建议在 06_导出/01_成片 目录执行"""
    cwd = Path.cwd()
    media_ext = {".mov", ".mp4", ".mxf", ".m4v"}
    medias = [f for f in cwd.glob("*") if f.is_file() and f.suffix.lower() in media_ext]
    if not medias:
        click.echo("❌ 当前目录没有找到成片视频")
        return
    for f in medias:
        export_time = click.prompt(f"\n文件【{f.name}】导出时间(202610011800)")
        title = click.prompt(f"片名")
        res = click.prompt(f"分辨率(1920x1080)")
        codec = click.prompt(f"编码(H264/H265/ProRes)")
        fmt = f.suffix.strip(".")
        exporter = click.prompt(f"导出人")
        note = click.prompt(f"备注，无备注直接回车", default="")
        ver = click.prompt(f"版本(v01)", default="v01")
        new_name = f"{export_time}_{title}_{res}_{codec}_{fmt}_{exporter}_{note}_{ver}{f.suffix}"
        new_path = cwd / sanitize_name(new_name)
        click.echo(f"预览：{f.name} → {new_name}")
        if click.confirm("确认执行本条改名?", default=False):
            if new_path.exists():
                click.echo("⚠️ 同名文件已存在，跳过")
                continue
            f.rename(new_path)
            click.echo("✅ 改名成功")

if __name__ == "__main__":
    cli()

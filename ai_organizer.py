import os
import json
import shutil
import asyncio
import re
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional

# ================= 0. 日志记录器 (黑匣子) =================
log_file_path = 'ai_organizer_debug.log'
# 如果文件已存在，先清空（忽略占用错误）
if os.path.exists(log_file_path):
    try:
        os.remove(log_file_path)
    except PermissionError:
        pass  # 文件被占用，继续执行

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler() # 同时输出到控制台
    ]
)

# ================= 1. 模型配置与初始化 =================

# 支持的AI模型配置
MODEL_CONFIGS = {
    "gemini": {
        "name": "Google Gemini",
        "api_key_env": "GOOGLE_API_KEY",
        "model_ids": {
            "1": "models/gemini-2.5-flash-lite",  # 极速版
            "2": "models/gemini-2.0-flash",       # 标准版
            "3": "models/gemini-2.5-pro",         # 专业版
        },
        "default_model": "models/gemini-2.5-flash-lite",
        "module": "google.genai",
        "client_class": "genai.Client",
    },
    "kimi": {
        "name": "Moonshot Kimi",
        "api_key_env": "KIMI_API_KEY",
        "model_ids": {
            "1": "kimi-k2",             # ⭐Kimi K2 (推荐)
            "2": "kimi-k2.5",           # Kimi K2.5
            "3": "moonshot-v1-8k",      # 8K上下文
            "4": "moonshot-v1-32k",     # 32K上下文
            "5": "moonshot-v1-128k",    # 128K上下文
        },
        "default_model": "kimi-k2.5",
        "module": "openai",
        "client_class": "OpenAI",
        "base_url": "https://api.moonshot.cn/v1",
        "async_module": "openai",
        "async_client_class": "AsyncOpenAI",
    }
}

# 全局配置变量
selected_provider: str = ""
selected_model_id: str = ""
client: Any = None
async_client: Any = None
sem: asyncio.Semaphore = asyncio.Semaphore(5)

REPORT_PATH = Path(r'./organize_audit_report.md')

# 扩展名定义
VIDEO_EXTS = ('.mkv', '.iso', '.ts', '.mp4', '.avi', '.rmvb', '.wmv', '.m2ts', '.mpg', '.flv', '.rm', '.m4v')
EXTRA_EXTS = ('.ass', '.srt', '.ssa', '.nfo', '.jpg', '.png')
ALL_VALID_EXTS = VIDEO_EXTS + EXTRA_EXTS


def select_model() -> tuple[str, str]:
    """
    自动选择 Google Gemini 模型，无需交互
    返回: (provider, model_id)
    """
    provider = "gemini"
    model_id = "models/gemini-2.5-flash-lite"  # 使用 Gemini 2.5 Flash Lite 模型
    logging.info(f"自动选择模型: Google Gemini ({model_id})")
    print(f"[自动] 使用模型: Google Gemini ({model_id})")
    return provider, model_id


def init_client(provider: str, model_id: str) -> Any:
    """
    初始化AI客户端
    """
    global client, async_client, sem, last_request_time
    last_request_time = 0
    
    config = MODEL_CONFIGS[provider]
    # 使用硬编码的 API Key（强制使用，不受环境变量影响）
    if provider == "gemini":
        # Gemini API Key - 优先从环境变量读取
        api_key = os.environ.get("GOOGLE_API_KEY", "")
    else:
        # Kimi API Key
        api_key = "sk-OCqaHJpNkLykg7OmpP7c2iT8lohLmSYJux3ROzcwEmDMNTbH"
    
    if not api_key:
        raise ValueError(
            f"❌ 未检测到环境变量 {config['api_key_env']}。\n"
            f"请在系统环境变量中设置，或在运行前使用:\n"
            f"  Windows: set {config['api_key_env']}=your_key\n"
            f"  Linux/Mac: export {config['api_key_env']}=your_key"
        )
    
    logging.info(f"初始化 {config['name']} 客户端，模型: {model_id}")
    
    if provider == "gemini":
        from google import genai
        client = genai.Client(api_key=api_key)
        # Gemini使用相同的客户端
        async_client = None  # 将通过aio方法使用
        # Gemini的并发控制
        sem = asyncio.Semaphore(5)
        
    elif provider == "kimi":
        # Kimi 使用 OpenAI 兼容的SDK
        try:
            from openai import OpenAI, AsyncOpenAI
        except ImportError:
            raise ImportError(
                "使用 Kimi 模型需要安装 openai 库。\n"
                "请运行: pip install openai"
            )
        
        client = OpenAI(
            api_key=api_key,
            base_url=config["base_url"]
        )
        async_client = AsyncOpenAI(
            api_key=api_key,
            base_url=config["base_url"],
            max_retries=0  # 禁用内部重试，我们自己控制
        )
        # Kimi的并发控制（Kimi的Rate Limit较严格）
        sem = asyncio.Semaphore(1)  # 串行处理以避免 429 错误
    
    return client


def build_system_prompt() -> str:
    """
    构建系统提示词（用于Kimi等支持system角色的模型）
    """
    return """你是一个专业的影视整理专家。请严格遵循以下规则：

【核心命名禁令】：
1. 严禁修改文件名：目标路径的最后一段（文件名）必须与原始文件名完全一致，不得做任何改动。

【目录构造规则】：
1. 一级目录：剧集名称 (年份)。
   - 必须保留非年份括号：若原名包含地名或版本（如：(合肥)、(美版)），视为剧名一部分保留。
   - 年份处理：只有从原始文件路径或文件名中**直接识别出** 4 位纯数字年份才加括号 `(年份)`。若无年份则仅保留剧名，不带空括号。**严禁凭空推测年份。**
2. 二级目录：
   - 如果原始文件路径中已经包含二级目录,且二级目录名称明确包含了季数（Sxx）信息，则直接沿用原来的二级目录名称,不做任何修改;否则创建二级目录
   - 如果原始文件路径中已经包含二级目录,则不管改二级目录名称有没有变化,且该二级目录目录下的视频文件也依然归属到这个目录下,
   - 需要创建二级目录时,优先命名为"剧名.Sxx.年份.画质.视频编码格式.音频编码格式"文件夹,其中Sxx为季数（如果能从原路径中识别出季数），年份、画质、视频编码格式、音频编码格式等信息仅在原路径中明确存在时才添加到二级目录名称中，且各信息之间必须使用点号（.）连接，且二级目录名称结尾不得有点号。**此处的年份等信息，严禁从一级目录继承，必须来自文件自身的原始路径。**
   - 如果只能识别出季数（Sxx）信息，而无法识别出年份、画质、视频编码格式、音频编码格式等其他信息，则二级目录命名为"Season XX"。

【最终路径结构】: 目标路径 `target` 必须是以下两种格式之一：
   - `[一级目录]/剧名.Sxx.年份.画质.视频编码格式.音频编码格式.组名/[原始文件名]` 
   - `[一级目录]/Season XX/[原始文件名]`

请直接返回 JSON 数组格式。"""


def build_user_prompt(file_chunk: List[str]) -> str:
    """
    构建用户提示词
    """
    return f"请为以下文件列表计算 Emby 目标路径：\n\n文件列表: {json.dumps(file_chunk, ensure_ascii=False)}\n\n请返回格式：[{{\"original\": \"...\", \"target\": \"...\", \"reason\": \"...\"}}]"


# ================= 2. 树状图与统计工具 =================
def build_tree_string(paths):
    """构建有序的目录树文本结构"""
    tree = {}
    for path in paths:
        parts = Path(path).parts
        current_level = tree
        for part in parts:
            if part not in current_level: current_level[part] = {}
            current_level = current_level[part]

    def recurse(node, prefix=""):
        tree_str = ""
        items = sorted(node.keys())
        for i, name in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            tree_str += f"{prefix}{connector}{name}\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_str += recurse(node[name], new_prefix)
        return tree_str
    return "/TV Shows\n" + recurse(tree)

def generate_audit_stats(all_decisions):
    """生成剧集和季度的结构化审计统计"""
    stats = defaultdict(lambda: {"orig_sources": set(), "total_count": 0, "seasons": defaultdict(int)})
    for d in all_decisions:
        orig_p, targ_p = Path(d.get('original', '')), Path(d.get('target', ''))
        if not targ_p.parts: continue
        
        orig_root = orig_p.parts[0] if len(orig_p.parts) > 1 else "根目录"
        show_name = targ_p.parts[0]
        season_name = targ_p.parts[1] if len(targ_p.parts) >= 2 else "一级目录直放"
        
        stats[show_name]["orig_sources"].add(orig_root)
        stats[show_name]["total_count"] += 1
        stats[show_name]["seasons"][season_name] += 1
    return stats


# ================= 3. 异步 AI 决策逻辑 =================
async def call_gemini_api(prompt: str, model_id: str, chunk_id: int) -> List[Dict]:
    """
    调用 Google Gemini API
    """
    from google import genai
    
    max_retries = 6
    wait_time = 5
    
    for attempt in range(max_retries):
        try:
            response = await client.aio.models.generate_content(model=model_id, contents=prompt)
            text = response.text
            logging.debug(f"[批次 {chunk_id}] 收到 AI 原始响应:\n---\n{text}\n---")
            
            # 清理响应文本
            text = text.replace('```json', '').replace('```', '').strip()
            match = re.search(r'\[.*\]', text, re.DOTALL)
            result = json.loads(match.group()) if match else json.loads(text)
            return result
            
        except Exception as e:
            logging.error(f"[批次 {chunk_id}] 第 {attempt+1} 次尝试失败: {e}")
            err_msg = str(e).lower()
            if any(x in err_msg for x in ["503", "429", "disconnected", "timeout"]):
                print(f"⏳ [批次 {chunk_id}] 繁忙/重连，{wait_time}s 后重试 ({attempt+1}/{max_retries})...")
                await asyncio.sleep(wait_time)
                wait_time *= 2
                continue
            print(f"[X] [批次 {chunk_id}] 致命错误: {e}")
            return []
    
    return []


async def call_kimi_api(prompt: str, system_prompt: str, model_id: str, chunk_id: int) -> List[Dict]:
    """
    调用 Moonshot Kimi API (OpenAI兼容)
    """
    global last_request_time
    max_retries = 10
    wait_time = 3  # 初始等待时间
    
    # 全局请求间隔控制 - 每个请求间隔2秒
    import time
    elapsed = time.time() - last_request_time
    if elapsed < 2.0:
        await asyncio.sleep(2.0 - elapsed)
    
    for attempt in range(max_retries):
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = await async_client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=0.1,  # 低温度，提高确定性
                max_tokens=4096
            )
            
            last_request_time = time.time()
            text = response.choices[0].message.content
            logging.debug(f"[批次 {chunk_id}] 收到 AI 原始响应:\n---\n{text}\n---")
            
            # 清理响应文本
            text = text.replace('```json', '').replace('```', '').strip()
            match = re.search(r'\[.*\]', text, re.DOTALL)
            result = json.loads(match.group()) if match else json.loads(text)
            return result
            
        except Exception as e:
            logging.error(f"[批次 {chunk_id}] 第 {attempt+1} 次尝试失败: {e}")
            err_msg = str(e).lower()
            # Kimi/OpenAI 的错误类型
            if any(x in err_msg for x in ["rate limit", "429", "timeout", "connection", "503", "500"]):
                print(f"[等待] [批次 {chunk_id}] 繁忙/限流，{wait_time}s 后重试 ({attempt+1}/{max_retries})...")
                await asyncio.sleep(wait_time)
                wait_time *= 2
                continue
            print(f"[X] [批次 {chunk_id}] 致命错误: {e}")
            return []
    
    return []


async def get_ai_decision_async(file_chunk: List[str], chunk_id: int, total_chunks: int) -> List[Dict]:
    """
    统一的AI决策接口，根据选择的模型调用不同的API
    """
    async with sem:
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(file_chunk)
        
        # 构建完整的prompt用于日志
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        logging.debug(f"[批次 {chunk_id}] 发送给 AI 的 Prompt:\n---\n{full_prompt}\n---")
        
        # 根据提供商调用不同的API
        if selected_provider == "gemini":
            # Gemini 将system和user合并
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            result = await call_gemini_api(combined_prompt, selected_model_id, chunk_id)
        elif selected_provider == "kimi":
            result = await call_kimi_api(user_prompt, system_prompt, selected_model_id, chunk_id)
        else:
            logging.error(f"未知的模型提供商: {selected_provider}")
            return []
        
        if result:
            logging.info(f"[OK] [AI 分析] 批次 {chunk_id}/{total_chunks} 成功 ({len(file_chunk)} 文件)")
        
        return result


# ================= 4. 扫描函数 =================
def scan_files(root_path: Path) -> tuple[List[str], List[str]]:
    """
    扫描目录中的媒体文件
    返回: (处理列表, 跳过的BDMV列表)
    """
    process_list, skipped_bdmv = [], []
    for root, dirs, files in os.walk(root_path):
        # 识别并跳过 BDMV
        if 'BDMV' in [d.upper() for d in dirs] or 'index.bdmv' in [f.lower() for f in files]:
            skipped_bdmv.append(root)
            dirs[:] = []
            continue
        for file in files:
            if file.lower().endswith(ALL_VALID_EXTS):
                process_list.append(os.path.relpath(os.path.join(root, file), root_path))
    return process_list, skipped_bdmv


# ================= 5. 主异步入口 =================
async def run_organizer():
    global selected_provider, selected_model_id
    
    logging.info("="*60)
    logging.info("[Emby AI] 异步媒体整理工具 v2026.Universal (Gemini + Kimi)")
    logging.info("="*60)
    
    # 0. 选择模型
    selected_provider, selected_model_id = select_model()
    logging.info(f"用户选择模型: {selected_provider} - {selected_model_id}")
    
    # 1. 初始化客户端
    try:
        init_client(selected_provider, selected_model_id)
        print(f"[OK] 成功初始化 {MODEL_CONFIGS[selected_provider]['name']} 客户端")
    except Exception as e:
        print(f"[X] 初始化失败: {e}")
        return
    
    # 2. 获取用户输入
    src_input = r"C:\Users\wiz\Desktop\aftermovetmps\Step1Tmp\tvshow"  # 硬编码源目录
    print(f"\n1. 源目录 (待整理): {src_input}")
    dst_input = r"C:\Users\wiz\Desktop\aftermovetmps\Step1Tmp\test"  # 硬编码目的目录
    print(f"2. 目的目录 (媒体库): {dst_input}")
    source_dir, target_dir = Path(src_input), Path(dst_input)
    is_dry_run = True  # 自动开启预览模式
    print("[自动] 预览模式: 已开启")
    
    logging.info(f"用户输入 - 源目录: {source_dir}")
    logging.info(f"用户输入 - 目的目录: {target_dir}")
    logging.info(f"用户输入 - 预览模式: {'是' if is_dry_run else '否'}")
    
    # 3. 扫描
    files, skipped_bdmv = scan_files(source_dir)
    if not files:
        logging.info("[提示] 没发现可处理的文件，任务结束。")
        return
    logging.info(f"[扫描] 完成：发现 {len(files)} 个文件，跳过 {len(skipped_bdmv)} 个 BDMV 目录。")
    
    # 4. 顺序分析 (避免API并发限制)
    chunk_size = 20  # 每批20个文件
    chunks = [files[i:i+chunk_size] for i in range(0, len(files), chunk_size)]
    logging.info(f"[AI] 模型 {selected_model_id} 已就绪，将分 {len(chunks)} 批次顺序分析...")
    
    # 顺序处理每个批次，避免并发429错误
    all_results = []
    for i, chunk in enumerate(chunks):
        result = await get_ai_decision_async(chunk, i+1, len(chunks))
        all_results.append(result)
        # 批次间间隔2秒
        if i < len(chunks) - 1:
            await asyncio.sleep(2)
    
    # 合并结果并按目标路径全局排序
    all_decisions = [item for sublist in all_results for item in sublist]
    all_decisions.sort(key=lambda x: x.get('target', ''))
    
    if not all_decisions:
        logging.warning("⚠️ AI 未返回任何有效结果，请检查日志。")
        return
    
    # 5. 统计审计
    audit_stats = generate_audit_stats(all_decisions)
    
    # 6. 构建报告
    logging.info(f"[报告] 分析完成，共获得 {len(all_decisions)} 条整理决策，开始构建审计报告...")
    target_paths = [d.get('target') for d in all_decisions if d.get('target')]
    
    # 审计汇总表
    audit_table = ["| 整理后剧名 | 原始来源 | 文件总数 | 季数及集数分布 |", "| :--- | :--- | :--- | :--- |"]
    for show, data in sorted(audit_stats.items()):
        orig_src = "<br>".join(list(data["orig_sources"]))
        dist = " / ".join([f"{s}({c}集)" for s, c in sorted(data["seasons"].items())])
        audit_table.append(f"| **{show}** | {orig_src} | {data['total_count']} | {dist} |")
    
    report = [
        f"# 媒体库整理审计报告 ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
        f"\n**使用模型**: {MODEL_CONFIGS[selected_provider]['name']} ({selected_model_id})",
        "\n## 1. 结构合规性审计表",
        "> 请在此检查是否有文件丢失或剧集被错误合并。",
        "\n".join(audit_table),
        "\n## 2. 预期目录树预览 (有序)",
        "```text", build_tree_string(target_paths), "```",
        "\n## 3. 详细映射清单 (已排序)",
        "| 目标位置 (有序) | ⬅️ 原始文件 | 理由 |",
        "| :--- | :--- | :--- |"
    ]
    for d in all_decisions:
        report.append(f"| **{d.get('target')}** | {d.get('original')} | {d.get('reason')} |")
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    logging.info(f"[完成] 审计报告已生成：{REPORT_PATH.absolute()}")
    
    # 7. 物理执行
    if not is_dry_run and all_decisions:
        confirm = input(f"\n⚠️ 预览已完成，确认物理移动 {len(all_decisions)} 个文件？(y/n): ")
        if confirm.lower() == 'y':
            logging.info("用户确认执行物理移动。")
            moved_count = 0
            for item in all_decisions:
                src, dst = source_dir / item.get('original', ''), target_dir / item.get('target', '')
                if src.exists() and item.get('target'):
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        logging.debug(f"正在移动: '{src}' -> '{dst}'")
                        shutil.move(str(src), str(dst))
                        moved_count += 1
                        if moved_count % 10 == 0:
                            logging.info(f"   🚚 移动进度: [{moved_count}/{len(all_decisions)}]")
                    except Exception as e:
                        logging.error(f"❌ 移动失败: 从 '{src}' 到 '{dst}' 失败! 错误: {e}")
            logging.info(f"✅ 归档任务圆满完成，共移动 {moved_count} 个文件。")
        else:
            logging.info("用户取消了物理移动操作。")
    
    if skipped_bdmv:
        logging.warning(f"[提示] 有 {len(skipped_bdmv)} 个 BDMV 原盘被跳过，详情请查看日志。")
        logging.debug(f"跳过的 BDMV 目录列表: {skipped_bdmv}")


if __name__ == "__main__":
    asyncio.run(run_organizer())

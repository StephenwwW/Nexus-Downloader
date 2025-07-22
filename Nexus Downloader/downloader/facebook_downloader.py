# downloader/facebook_downloader.py
import os
import json
import subprocess

# --- 通用輔助函數 ---
def _convert_json_to_netscape(json_path):
    """將 JSON cookie 轉換為 Netscape 格式，返回檔案路徑或 None"""
    if not os.path.exists(json_path): return None
    netscape_cookie_path = "facebook_cookies_netscape.txt"
    try:
        with open(json_path, "r", encoding="utf-8") as f: cookies = json.load(f)
        with open(netscape_cookie_path, "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for cookie in cookies:
                domain = cookie.get("domain", "")
                if not domain.startswith("."): domain = "." + domain
                f.write(f"{domain}\tTRUE\t{cookie.get('path', '/')}\t{str(cookie.get('secure', False)).upper()}\t{str(int(cookie.get('expirationDate', 0)))}\t{cookie.get('name', '')}\t{cookie.get('value', '')}\n")
        return netscape_cookie_path
    except Exception: return None

def _is_video_url(url):
    """更嚴謹的 URL 分析，正確識別影片連結"""
    return any(keyword in url for keyword in ["/reel/", "/videos/", "/watch"])

# --- 影片下載策略核心 ---
def _strategy_yt_dlp_video(url, output_dir, cookie_file, progress_callback):
    """yt-dlp 主力影片下載引擎，負責下載並修復影片"""
    files_before = set(os.listdir(output_dir))
    try:
        output_template = os.path.join(output_dir, "%(id)s.%(ext)s")
        # 經過驗證最可靠的 FFmpeg 指令，用以重建時間戳，解決播放卡頓問題
        postprocessor_args = ["ffmpeg:-fflags", "+genpts", "-r", "30", "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p"]
        cmd = ["yt-dlp", url, "-f", "bestvideo+bestaudio/best", "--postprocessor-args", " ".join(postprocessor_args), "--output", output_template, "--no-playlist", "--no-warnings", "--restrict-filenames"]
        if cookie_file: cmd.extend(["--cookies", cookie_file])

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for line in process.stdout:
            if "[download]" in line or "[ffmpeg]" in line:
                progress_callback(f"  {line.strip()}")
        process.wait()
        return bool(set(os.listdir(output_dir)) - files_before)
    except Exception as e:
        progress_callback(f"  [失敗] yt-dlp 執行時發生未知錯誤: {e}")
        return False

# --- 主下載函數 ---
def download(url: str, status_callback, progress_callback):
    """
    主下載函數，專注於下載 Facebook 影片。
    照片下載功能已根據使用者要求移除。
    """
    output_dir = os.path.join("downloads", "facebook")
    os.makedirs(output_dir, exist_ok=True)
    
    if not _is_video_url(url):
        status_callback("❌ 功能限制：目前僅支援 Facebook 的影片 (Reels/Watch) 下載。")
        progress_callback("   根據您的要求，已移除尚不穩定的照片下載功能。")
        return

    status_callback("ℹ️ 已識別內容類型為: 影片")
    
    # --- 影片策略 1/2：匿名下載 ---
    status_callback("--- 影片策略 1/2：匿名下載 (yt-dlp) ---")
    if _strategy_yt_dlp_video(url, output_dir, None, progress_callback):
        status_callback("✅ 匿名下載成功！")
        return
    
    # --- 影片策略 2/2：使用 Cookie 作為最後手段 ---
    status_callback("--- 影片策略 2/2：Cookie 下載 (yt-dlp) ---")
    cookie_json_path = "facebook_cookies.json"
    if not os.path.exists(cookie_json_path):
        status_callback("❌ 找不到 facebook_cookies.json，無法執行需要 Cookie 的最後手段。")
        return
        
    netscape_cookie_file = _convert_json_to_netscape(cookie_json_path)
    if not netscape_cookie_file:
        status_callback("❌ 轉換 Cookie 格式時發生錯誤。")
        return
        
    if _strategy_yt_dlp_video(url, output_dir, netscape_cookie_file, progress_callback):
        status_callback("✅ 使用 Cookie 下載成功！")
    else:
        status_callback("❌ 所有影片下載策略均失敗。")
        
    if os.path.exists(netscape_cookie_file):
        os.remove(netscape_cookie_file)

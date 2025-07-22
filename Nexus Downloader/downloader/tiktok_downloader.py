# downloader/tiktok_downloader.py
import os
import subprocess

def download(url: str, status_callback, progress_callback):
    """
    使用 yt-dlp 下載 TikTok 影片，並確保影音合併。
    """
    try:
        output_dir = os.path.join("downloads", "tiktok")
        os.makedirs(output_dir, exist_ok=True)
        
        output_template = os.path.join(output_dir, "%(id)s.%(ext)s")

        status_callback(f"正在呼叫 yt-dlp 處理 TikTok 連結...")

        # --- 關鍵指令更新 ---
        # 新增格式選擇與合併指令，確保下載最佳品質並合併為 mp4
        cmd = [
            "yt-dlp",
            url,
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "--output", output_template,
            "--no-playlist",
            "--no-warnings",
            "--restrict-filenames",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "--referer", "https://www.tiktok.com/"
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if "[download]" in output:
                    progress_callback(output.strip())
        
        stderr = process.communicate()[1]
        if process.returncode != 0:
            if "ffmpeg" in stderr.lower() or "ffprobe" in stderr.lower():
                 status_callback("❌ 錯誤：找不到 FFmpeg！這是造成影片卡頓或無聲的主要原因。")
                 status_callback("請根據 README 檔案的指示安裝 FFmpeg。")
            else:
                status_callback("❌ yt-dlp 下載失敗。")
                progress_callback(f"錯誤詳情: {stderr}")
        else:
            status_callback("✅ TikTok 影片下載並合併成功！")

    except FileNotFoundError:
        status_callback("❌ 錯誤: `yt-dlp` 未安裝或未在系統 PATH 中。請參考 README 進行安裝。")
    except Exception as e:
        status_callback(f"❌ 發生未知錯誤: {e}")

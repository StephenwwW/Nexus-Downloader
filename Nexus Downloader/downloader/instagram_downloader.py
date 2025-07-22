# downloader/instagram_downloader.py
import os
import re
import json
import instaloader # 使用專為 Instagram 設計的、最可靠的工具

def download(url: str, status_callback, progress_callback):
    """
    使用 Instaloader 下載 Instagram 內容。
    實行「匿名優先，Cookie 為輔，絕不互動」的最終策略。
    """
    output_dir = os.path.join("downloads", "instagram")
    os.makedirs(output_dir, exist_ok=True)

    # --- 策略一：匿名下載 (僅適用於公開貼文/Reels) ---
    status_callback("🚀 策略一：嘗試匿名下載...")
    L_anon = instaloader.Instaloader(
        dirname_pattern=output_dir,
        filename_pattern="{shortcode}_{date_utc}_UTC_{mediacount}",
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
        download_comments=False
    )

    is_story = "/stories/" in url
    post_match = re.search(r"/(p|tv|reel)/([^/]+)", url)

    if not is_story and post_match:
        try:
            shortcode = post_match.group(2)
            post = instaloader.Post.from_shortcode(L_anon.context, shortcode)
            
            files_before = set(os.listdir(output_dir))
            L_anon.download_post(post, target=output_dir)
            files_after = set(os.listdir(output_dir))

            if files_after - files_before:
                 status_callback("✅ 匿名下載成功！")
                 return
            else:
                 raise Exception("匿名下載未產生任何檔案")
        except Exception as e:
            status_callback(f"⚠️ 匿名下載失敗 ({e})，正在轉為 Cookie 模式...")
    elif is_story:
        status_callback("⚠️ 限時動態需要登入，直接進入 Cookie 模式。")
    else:
        status_callback("❌ 無法識別的 Instagram URL 格式。")
        return

    # --- 策略二：使用 Cookie 檔案登入下載 ---
    status_callback("🚀 策略二：嘗試使用 Cookie 檔案登入...")
    
    cookie_json_path = "instagram_cookies.json"
    if not os.path.exists(cookie_json_path):
        status_callback("❌ 下載失敗：此內容需要登入，且未提供 `instagram_cookies.json` 檔案。")
        return

    try:
        L_login = instaloader.Instaloader(
            download_video_thumbnails=False,
            save_metadata=False,
            compress_json=False,
            quiet=True,
            download_comments=False
        )

        status_callback("正在讀取 instagram_cookies.json...")
        # --- 關鍵錯誤修正 ---
        # 使用 instaloader 內建的、最可靠的 cookie 匯入方法
        L_login.context.load_cookies_from_file(cookie_json_path)
        
        status_callback("正在驗證 Cookie...")
        username = L_login.test_login()
        if not username:
            status_callback("❌ Cookie 驗證失敗。Cookie 可能已過期或無效。")
            return
        
        status_callback(f"✔️ Cookie 驗證成功，已登入為: {username}")
        progress_callback("正在使用已登入的帳號下載內容...")
        
        if post_match:
            shortcode = post_match.group(2)
            post = instaloader.Post.from_shortcode(L_login.context, shortcode)
            L_login.dirname_pattern = output_dir
            L_login.filename_pattern = "{shortcode}_{date_utc}_UTC_{n}"
            L_login.download_post(post, target=output_dir)
            status_callback("✅ 使用 Cookie 下載貼文成功！")

        elif is_story:
            story_username = re.search(r"/stories/([^/]+)", url).group(1)
            profile = instaloader.Profile.from_username(L_login.context, story_username)
            # 為限時動態設定獨立的資料夾
            L_login.dirname_pattern = os.path.join(output_dir, f"{profile.username}_stories")
            L_login.download_stories(userids=[profile.userid], fast_update=True)
            status_callback(f"✅ 使用 Cookie 下載 {story_username} 的限時動態成功！")

    except Exception as e:
        status_callback(f"❌ 使用 Cookie 下載時發生錯誤: {e}")

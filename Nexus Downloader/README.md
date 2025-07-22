# Nexus Downloader

\<div align="center"\>A simple and robust GUI downloader for TikTok, Instagram, and Facebook, built with Python and PyQt6.\</div\>

-----

### ✨ Features

  * **Multi-Platform Support**:
      * [cite\_start]**Facebook**: Reliably downloads Videos (Reels/Watch). [cite: 1]
      * [cite\_start]**Instagram**: Downloads Posts, Reels, and Stories using the professional `instaloader` library. [cite: 1]
      * [cite\_start]**TikTok**: Downloads videos using `yt-dlp`. [cite: 1]
  * [cite\_start]**Intelligent Fallback**: Prioritizes anonymous downloading. [cite: 1] [cite\_start]If that fails, it automatically and silently uses a provided cookie file as a fallback. [cite: 2]
  * [cite\_start]**No Interactive Login**: This application will never ask for your username or password. [cite: 2] [cite\_start]All authentication is handled non-interactively via cookie files. [cite: 3]
  * [cite\_start]**Video Post-Processing**: Automatically uses FFmpeg to rebuild timestamps for downloaded Facebook videos, fundamentally solving playback stuttering issues. [cite: 3]
  * [cite\_start]**GitHub Ready**: Comes with a pre-configured `.gitignore` to protect your sensitive data. [cite: 3]

### 🛑 IMPORTANT: Security Notice

[cite\_start]This project is designed to be safely shared and uploaded to GitHub. [cite: 3] [cite\_start]The included `.gitignore` file is configured to prevent your sensitive `*.json` cookie files from being tracked by Git. [cite: 4]

[cite\_start]⚠️ **Before your first `git commit`, please verify that the `.gitignore` file exists in your project's root directory.** [cite: 4]

### 🛠️ Setup & Installation

**1. Prerequisites**

  * [cite\_start]Python 3.8+ [cite: 5, 13]
  * [cite\_start]**FFmpeg**: Absolutely required for fixing Facebook video playback issues. [cite: 5, 13]
      * [cite\_start]**Windows**: Download from the [FFmpeg Official Website](https://ffmpeg.org/download.html), unzip, and add the `bin` folder to your system's PATH environment variable. [cite: 5, 13]
      * [cite\_start]**macOS**: The easiest way is to install via Homebrew: `brew install ffmpeg` [cite: 5, 13]

**2. Install Python Libraries**
[cite\_start]Open your terminal (or Command Prompt) and run the following command to install all necessary libraries: [cite: 6, 14]

```bash
pip install PyQt6 yt-dlp requests instaloader
```

### 🚀 How to Use

**1. Provide Cookie Files (Optional but Recommended)**

[cite\_start]To download private content (like IG Stories) and ensure the highest success rate for Facebook videos, providing cookies is the best method. [cite: 7]

  * [cite\_start]**Install a Browser Extension**: We recommend **Cookie-Editor** for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/). [cite: 7]
  * **Export Cookies**:
    1.  [cite\_start]Log in to the desired platform (Facebook or Instagram) in your browser. [cite: 7]
    2.  [cite\_start]On the platform's page, click the Cookie-Editor icon. [cite: 7]
    3.  Select `Export` -\> `Export as JSON`. [cite\_start]This will copy the cookie data to your clipboard. [cite: 7]
    4.  [cite\_start]Create a new file in your project's root directory with the corresponding name and paste the content: [cite: 8]
          * [cite\_start]For Facebook, save as `facebook_cookies.json`. [cite: 8]
          * [cite\_start]For Instagram, save as `instagram_cookies.json`. [cite: 8]

**2. Run the Application**

1.  [cite\_start]Ensure all project files (`main_app.py`, the `downloader` folder) and your optional cookie files are in the same directory. [cite: 9, 15]
2.  [cite\_start]Open your terminal, navigate to the project directory, and run: [cite: 9, 15]
    ```bash
    python main_app.py
    ```
3.  [cite\_start]Paste a URL into the input field and click the "Download" button. [cite: 9, 15]

### ⚙️ How It Works (Download Strategy)

  * [cite\_start]**TikTok**: Fully anonymous download via `yt-dlp`. [cite: 9]
  * **Instagram**: Attempts anonymous download first. [cite\_start]Falls back to using `instagram_cookies.json` for Stories or if the anonymous download fails. [cite: 9, 10]
  * **Facebook**:
      * [cite\_start]**Videos**: Attempts anonymous download first. [cite: 10] [cite\_start]Falls back to using `facebook_cookies.json`. [cite: 11]
      * **Photos/Posts**: Not Supported. [cite\_start]This feature was removed to focus on providing a stable and reliable video downloading experience. [cite: 11]

### 📄 License

[cite\_start]This project is released under the MIT License. [cite: 11] [cite\_start]See the `LICENSE` file for details. [cite: 12]

-----

[Read this document in 繁體中文 (Traditional Chinese)](https://www.google.com/search?q=%23t3-%E7%A4%BE%E7%BE%A4%E5%AA%92%E9%AB%94%E4%B8%8B%E8%BC%89%E5%99%A8)

\<br\>
\<hr\>
\<br\>

# Nexus 社群媒體下載器

\<div align="center"\>一款簡潔、強大的 GUI 下載工具，支援 TikTok、Instagram 和 Facebook，使用 Python 和 PyQt6 打造。\</div\>

-----

### ✨ 功能特色

  * **支援多平台**:
      * **Facebook**: 可靠地下載影片 (Reels/Watch)。
      * **Instagram**: 使用專業的 `instaloader` 函式庫，可下載貼文、Reels 和限時動態。
      * **TikTok**: 可下載影片。
  * **智慧備援**: 優先嘗試匿名下載。如果失敗，程式會自動、靜默地使用您提供的 Cookie 檔案作為備援方案。
  * **無互動登入**: 本程式絕對不會在終端機中要求您輸入任何帳號密碼。所有身分驗證都透過 Cookie 檔案以非互動方式處理。
  * **影片重建 (Facebook)**: 自動使用 FFmpeg 對下載的 Facebook 影片進行時間戳重建，從根本上解決播放卡頓問題。
  * **GitHub 安全就緒**: 附帶預先配置好的 `.gitignore` 檔案，保護您的個人隱私資訊。

### 🛑 重要：安全性提醒

本專案已為您準備好安全的 GitHub 發布設定。附帶的 `.gitignore` 檔案會防止您的個人隱私檔案（`*.json`）被 Git 追蹤。

⚠️ **在您執行第一次 `git commit` 之前，請務必確認 `.gitignore` 檔案位於您專案的根目錄中。**

### 🛠️ 環境設定與安裝

**1. 前置需求**

  * [cite\_start]Python 3.8+ [cite: 13]
  * [cite\_start]**FFmpeg**: 絕對必要，這是確保 Facebook 影片能正常播放的關鍵步驟！ [cite: 13]
      * [cite\_start]**Windows**: 從 [FFmpeg 官網](https://ffmpeg.org/download.html)下載，解壓縮後，將 `bin` 資料夾的路徑加入到系統的 PATH 環境變數中。 [cite: 13]
      * [cite\_start]**macOS**: 透過 Homebrew 安裝：`brew install ffmpeg` [cite: 13]

**2. 安裝 Python 函式庫**
[cite\_start]打開您的終端機或命令提示字元，並執行以下指令來安裝所有必要的函式庫： [cite: 14]

```bash
pip install PyQt6 yt-dlp requests instaloader
```

### 🚀 如何使用

**1. 提供 Cookie 檔案 (選用但強烈建議)**

要下載私人內容（如 IG 限時動態）並確保 Facebook 影片的最高下載成功率，提供 Cookies 是最佳方法。

  * **安裝瀏覽器擴充功能**: 我們推薦 **Cookie-Editor** 適用於 [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)。
  * **匯出 Cookies**:
    1.  在您的瀏覽器中，分別登入您想使用的平台 (Facebook 或 Instagram)。
    2.  在該平台的頁面上，點擊 Cookie-Editor 圖示。
    3.  選擇 `Export` -\> `Export as JSON`。這會將 Cookie 資訊複製到您的剪貼簿。
    4.  在您專案的根目錄中建立一個新檔案，使用對應的檔名並貼上內容：
          * Facebook 的 Cookies 請存成 `facebook_cookies.json`。
          * Instagram 的 Cookies 請存成 `instagram_cookies.json`。

**2. 執行應用程式**

1.  [cite\_start]確保所有專案檔案（`main_app.py`、`downloader` 資料夾，以及您選擇性加入的 `*.json` Cookie 檔案）都放在同一個資料夾中。 [cite: 15]
2.  [cite\_start]打開您的終端機，切換到專案資料夾的路徑，然後執行： [cite: 15]
    ```bash
    python main_app.py
    ```
3.  [cite\_start]將網址貼到輸入框中，然後點擊「下載」按鈕。 [cite: 15]

### ⚙️ 運作原理 (下載策略)

  * **TikTok**: 完全匿名下載。
  * **Instagram**: 優先嘗試匿名下載。對於限時動態或匿名下載失敗的內容，會使用 `instagram_cookies.json` 作為備援。
  * **Facebook**:
      * **影片**: 優先嘗試匿名下載，失敗後使用 `facebook_cookies.json` 作為備援。
      * **照片/貼文**: 不再支援。此功能已移除，以專注於提供穩定可靠的影片下載體驗。

### 📄 授權條款

本專案採用 MIT 授權條款。詳情請見 `LICENSE` 檔案。

-----

[View this document in English](https://www.google.com/search?q=%23t3-downloader)
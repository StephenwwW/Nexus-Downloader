# Nexus Downloader

<div align="center">
A GUI downloader for TikTok, Instagram, and Facebook, built with Python and PyQt6.
</div>

---

[Read this document in 繁體中文 (Traditional Chinese)](#nexus-downloader-繁體中文)

### Features

* **Platform Support**:
    * **Facebook**: Downloads videos (Reels/Watch).
    * **Instagram**: Downloads posts, Reels, and Stories via the `instaloader` library.
    * **TikTok**: Downloads videos via `yt-dlp`.
* **Download Logic**: The application first attempts an anonymous download. If this fails, it falls back to using a provided cookie file for authentication.
* **Non-Interactive Authentication**: The application does not prompt for usernames or passwords. Authentication is handled via cookie files.
* **Video Post-Processing**: Uses FFmpeg to rebuild timestamps for downloaded Facebook videos to address potential playback stuttering.
* **Git Configuration**: Includes a pre-configured `.gitignore` file to prevent cookie files from being committed.

### User Interface
![Screenshot](Nexus Downloader/images/screenshot.png)

### Security Notice

The `.gitignore` file is configured to prevent sensitive `*.json` cookie files from being tracked by Git.

⚠️ **Before your first `git commit`, please verify that the `.gitignore` file exists in your project's root directory to protect your private data.**

### Setup & Installation

**1. Prerequisites**

* Python 3.8+
* **FFmpeg**: Required for post-processing Facebook videos.
    * **Windows**: Download from the [FFmpeg Official Website](https://ffmpeg.org/download.html), unzip, and add the `bin` folder to your system's PATH environment variable.
    * **macOS**: Install via Homebrew: `brew install ffmpeg`

**2. Install Libraries**

Open a terminal and run the following command:

```bash
pip install PyQt6 yt-dlp requests instaloader
```

### How to Use

**1. Obtain and Use Cookie Files (Optional)**

For downloading private content (e.g., Instagram Stories) or to improve download reliability for Facebook, cookie files are recommended.

1. **Install a Browser Extension**:
    * A tool like **Cookie-Editor** for Chrome or Firefox is recommended for exporting cookies.

2. **Export Cookies as JSON**:
    * Log in to Facebook or Instagram in your browser.
    * Navigate to the site, open the Cookie-Editor extension, and select `Export` → `Export as JSON`. This copies the cookie data to your clipboard.

3. **Create the Cookie File**:
    * You must **manually create a new file** in the project's root directory.
    * Paste the copied JSON data into your new file.
    * Save the file with the correct name:
        * For Facebook, name the file `facebook_cookies.json`.
        * For Instagram, name the file `instagram_cookies.json`.

**2. Run the Application**

1. Ensure all project files and your optional `*.json` cookie files are in the same directory.
2. Navigate to the project directory in your terminal and run:

```bash
python main_app.py
```

### Download Strategy

* **TikTok**: Uses anonymous download via `yt-dlp`.
* **Instagram**: Attempts anonymous download first. For Stories or if anonymous download fails, it uses `instagram_cookies.json` as a fallback.
* **Facebook**:
    * **Videos**: Attempts anonymous download first, falling back to `facebook_cookies.json` if needed.
    * **Photos/Posts**: This functionality is not supported.

### License

This project is released under the MIT License.

---

<br>

# Nexus Downloader (繁體中文)

<div align="center">
一款使用 Python 和 PyQt6 開發的 GUI 下載工具，支援 TikTok、Instagram 和 Facebook。
</div>

---
[View this document in English](#Nexus-Downloader)

### 功能

* **平台支援**:
    * **Facebook**: 下載影片 (Reels/Watch)。
    * **Instagram**: 透過 `instaloader` 函式庫下載貼文、Reels 和限時動態。
    * **TikTok**: 透過 `yt-dlp` 下載影片。
* **下載邏輯**: 程式會優先嘗試匿名下載。若失敗，則會使用提供的 Cookie 檔案進行驗證。
* **非互動式驗證**: 程式不會要求輸入帳號密碼，所有身份驗證均透過 Cookie 檔案處理。
* **影片後處理**: 使用 FFmpeg 重建已下載的 Facebook 影片時間戳，以處理潛在的播放卡頓問題。
* **Git 設定**: 內附已設定好的 `.gitignore` 檔案，以避免 Cookie 檔案被提交。

## 軟體截圖
![Screenshot](Nexus%20Downloader/images/screenshot.png)

### 安全性提醒

`.gitignore` 檔案已設定完成，可防止敏感的 `*.json` Cookie 檔案被 Git 追蹤。

⚠️ **在執行第一次 `git commit` 前，請確認專案根目錄中存在 `.gitignore` 檔案，以保護您的個人隱私資料。**

### 環境設定與安裝

**1. 前置需求**

* Python 3.8+
* **FFmpeg**: 處理 Facebook 影片後續步驟所需。
    * **Windows**: 至 [FFmpeg 官網](https://ffmpeg.org/download.html) 下載，解壓縮後將 `bin` 資料夾路徑加入系統的 PATH 環境變數。
    * **macOS**: 透過 Homebrew 安裝：`brew install ffmpeg`

**2. 安裝函式庫**

打開終端機並執行以下指令：

```bash
pip install PyQt6 yt-dlp requests instaloader
```

### 如何使用

**1. 取得並使用 Cookie 檔案 (選用)**

若要下載私人內容（如 IG 限時動態）或提升 Facebook 下載穩定性，建議使用 Cookie 檔案。

1. **安裝瀏覽器擴充功能**:
    * 建議安裝如 **Cookie-Editor**（適用於 Chrome/Firefox） 的擴充功能以匯出 Cookie。

2. **匯出 Cookie 為 JSON 格式**:
    * 在瀏覽器中登入 Facebook 或 Instagram。
    * 在該網站頁面上，打開 Cookie-Editor 擴充功能，選擇 `Export` → `Export as JSON`，此操作會將 Cookie 資料複製到剪貼簿。

3. **建立 Cookie 檔案**:
    * 您必須在專案根目錄中 **手動建立一個新檔案**。
    * 將剪貼簿中的 JSON 資料貼到新檔案中。
    * 根據來源平台，使用對應的檔名儲存檔案：
        * Facebook 的 Cookie：請將檔案命名為 `facebook_cookies.json`。
        * Instagram 的 Cookie：請將檔案命名為 `instagram_cookies.json`。

**2. 執行程式**

1. 確認所有專案檔案及您選擇性建立的 `*.json` 檔案都位於同一個資料夾。
2. 在終端機中切換至專案目錄，並執行：

```bash
python main_app.py
```

### 下載策略

* **TikTok**: 透過 `yt-dlp` 進行匿名下載。
* **Instagram**: 優先嘗試匿名下載。下載限時動態或匿名下載失敗時，會使用 `instagram_cookies.json` 作為備援。
* **Facebook**:
    * **影片**: 優先嘗試匿名下載，若失敗則使用 `facebook_cookies.json` 作為備援。
    * **照片/貼文**: 不支援此功能。

### 授權條款

本專案採用 MIT 授權條款。

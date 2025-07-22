# main_app.py
import sys
import os
import re
import json
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QGroupBox
)
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtGui import QIcon

# -----------------------------------------------------------------------------
# 下載器模組導入 (假設它們在 downloader 資料夾中)
# -----------------------------------------------------------------------------
# 我們將在主程式啟動時動態檢查並導入
try:
    from downloader import tiktok_downloader
    from downloader import facebook_downloader
    from downloader import instagram_downloader
except ImportError:
    # 建立一個假的模組，以便程式可以啟動並提示使用者
    class FakeDownloader:
        def download(self, url, status_callback, progress_callback):
            status_callback.emit("錯誤：找不到 'downloader' 資料夾或模組。\n請確保 'downloader' 資料夾與主程式在同一目錄下。")
            return
    tiktok_downloader = facebook_downloader = instagram_downloader = FakeDownloader()


# -----------------------------------------------------------------------------
# 下載工作執行緒
# -----------------------------------------------------------------------------
class DownloadWorker(QObject):
    """
    在單獨的執行緒中執行下載任務，以防止GUI凍結。
    """
    finished = pyqtSignal(str)
    status = pyqtSignal(str)
    progress = pyqtSignal(str) # 用於更詳細的進度更新

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """根據 URL 自動選擇下載器並開始下載"""
        downloader = None
        platform = "未知"

        if "tiktok.com" in self.url:
            platform = "TikTok"
            downloader = tiktok_downloader
        elif "instagram.com" in self.url:
            platform = "Instagram"
            downloader = instagram_downloader
        elif "facebook.com" in self.url or "fb.watch" in self.url:
            platform = "Facebook"
            downloader = facebook_downloader
        else:
            self.finished.emit("❌ 錯誤：無法識別的網址，請確認是否為 TikTok, Instagram 或 Facebook 的有效網址。")
            return

        self.status.emit(f"▶️ 平台: {platform}。開始處理...")

        try:
            # 傳遞 signal emitters 作為回呼函數
            downloader.download(self.url, self.status.emit, self.progress.emit)
            self.finished.emit(f"✅ {platform} 下載任務完成！")
        except Exception as e:
            print(f"下載執行緒錯誤: {e}")
            self.finished.emit(f"❌ {platform} 下載失敗: {e}")


# -----------------------------------------------------------------------------
# 主視窗應用程式
# -----------------------------------------------------------------------------
class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None
        self.init_ui()
        self.check_dependencies()

    def init_ui(self):
        """初始化使用者介面"""
        self.setWindowTitle("社群媒體下載器 (IG/FB/TikTok)")
        self.setGeometry(300, 300, 500, 400)
        
        # 設置圖標 (可選)
        # self.setWindowIcon(QIcon('icon.png'))

        # 主佈局
        main_layout = QVBoxLayout()

        # URL 輸入框
        url_group = QGroupBox("1. 貼上網址")
        url_layout = QVBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("貼上 TikTok / Instagram / Facebook 的影片或圖片網址")
        url_layout.addWidget(self.url_input)
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)

        # 下載按鈕
        self.download_btn = QPushButton("🚀 開始下載")
        self.download_btn.setFixedHeight(40)
        self.download_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.download_btn.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_btn)

        # 狀態輸出框
        status_group = QGroupBox("2. 下載狀態")
        status_layout = QVBoxLayout()
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setPlaceholderText("這裡會顯示下載進度和結果...")
        status_layout.addWidget(self.status_output)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        self.setLayout(main_layout)

    def check_dependencies(self):
        """檢查必要的檔案是否存在 (例如 cookies)"""
        if not os.path.exists("downloader"):
             self.update_status("⚠️ 警告： 'downloader' 資料夾不存在，請將其與主程式放在一起。")
        
        if not os.path.exists("facebook_cookies.json"):
            self.update_status("ℹ️ 提示：未找到 `facebook_cookies.json`。下載 Facebook 私人影片可能會失敗。")
        else:
            self.update_status("✔️ 已找到 `facebook_cookies.json`。")
            
        self.update_status("ℹ️ 提示：首次下載 Instagram 內容時，可能需要在終端機中登入。")


    def update_status(self, message):
        """線程安全地更新狀態顯示框"""
        self.status_output.append(message)
        QApplication.processEvents() # 處理UI更新

    def lock_ui(self, is_locked):
        """下載時鎖定UI，防止重複點擊"""
        self.url_input.setEnabled(not is_locked)
        self.download_btn.setEnabled(not is_locked)
        self.download_btn.setText("下載中..." if is_locked else "🚀 開始下載")

    def start_download(self):
        """點擊下載按鈕時觸發"""
        url = self.url_input.text().strip()
        if not url:
            self.update_status("❌ 錯誤：網址不能為空！")
            return

        self.status_output.clear()
        self.update_status(f"準備下載: {url}")
        self.lock_ui(True)

        # 創建並啟動下載執行緒
        self.thread = QThread()
        self.worker = DownloadWorker(url)
        self.worker.moveToThread(self.thread)

        # 連接信號與槽
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.status.connect(self.update_status)
        self.worker.progress.connect(self.update_status) # 連接進度信號

        self.thread.start()

    def on_download_finished(self, message):
        """下載完成後的清理工作"""
        self.update_status(message)
        self.lock_ui(False)
        self.thread.quit()
        self.thread.wait()
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        """關閉視窗時確保執行緒已終止"""
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        event.accept()

# -----------------------------------------------------------------------------
# 應用程式入口
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # 確保 downloads 目錄存在
    os.makedirs("downloads", exist_ok=True)
    
    app = QApplication(sys.argv)
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec())

import json
import os

def convert_cookie_editor_json_to_netscape(json_file, output_file):
    with open(json_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie["domain"]
            include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
            path = cookie["path"]
            secure = "TRUE" if cookie.get("secure", False) else "FALSE"
            expires = int(cookie.get("expirationDate", 9999999999))
            name = cookie["name"]
            value = cookie["value"]
            line = f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n"
            f.write(line)

    print(f"✅ 已轉換完成：{output_file}")


if __name__ == "__main__":
    input_json = "fb_cookie.json"          # 請改成你 Cookie-Editor 匯出的 JSON 檔名
    output_txt = "cookie/fb.cookie.txt"    # 產生的 Netscape 格式 cookie 路徑

    convert_cookie_editor_json_to_netscape(input_json, output_txt)

import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def install_xvfb():
    try:
        # Cài đặt xvfb nếu chưa được cài đặt
        cmd = "sudo apt install xvfb -y"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("Đã cài đặt xvfb thành công.")
        else:
            print("Lỗi khi cài đặt xvfb:", result.stderr)
    except Exception as e:
        print(f"Lỗi khi cài đặt xvfb: {e}")

def install_freerdp():
    try:
        # Cài đặt freerdp2-x11
        cmd = "sudo apt install freerdp2-x11 -y"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("Đã cài đặt freerdp2-x11 thành công.")
        else:
            print("Lỗi khi cài đặt freerdp2-x11:", result.stderr)
    except Exception as e:
        print(f"Lỗi khi cài đặt freerdp2-x11: {e}")

def scan_ip(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Địa chỉ IP {ip} mở cổng {port}")
                return ip
            return None
    except Exception as e:
        print(f"Lỗi khi quét IP {ip}: {e}")
        return None

def connect_rdp(ip, username, password):
    try:
        # Sử dụng xvfb-run để chạy xfreerdp trong môi trường ảo và thêm tùy chọn +clipboard
        cmd = f"xvfb-run -a xfreerdp /v:{ip}:{port} /u:{username} /p:{password} /cert:ignore +clipboard"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Kiểm tra kết quả, nếu thành công thì trả về thông tin đăng nhập
        if result.returncode == 0:
            return f"IP: {ip}:{port} - User: {username}, Password: {password}"
        print(f"Lỗi khi kết nối RDP đến IP {ip}: {result.stderr}")
        return None
    except Exception as e:
        print(f"Lỗi khi kết nối RDP đến IP {ip}: {e}")
        return None

def main():
    install_xvfb()
    install_freerdp()
    
    port = input("Nhập cổng: ")
    start_ip = input("Nhập địa chỉ IP bắt đầu: ")
    end_ip = input("Nhập địa chỉ IP kết thúc: ")
    username = input("Nhập tên người dùng RDP: ")
    password = input("Nhập mật khẩu RDP: ")
    start_ip_obj = ipaddress.ip_address(start_ip)
    end_ip_obj = ipaddress.ip_address(end_ip)
    num_ips = int(end_ip_obj) - int(start_ip_obj) + 1

    print(f"Số lượng IP cần phải quét: {num_ips}")  
    print("________________________________")

    ips_to_scan = [str(ipaddress.ip_address(ip)) for ip in range(int(start_ip_obj), int(end_ip_obj) + 1)]
    successful_ips = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for ip in ips_to_scan:
            futures.append(executor.submit(scan_ip, ip, port))

        for future in as_completed(futures):
            result = future.result()
            if result:
                successful_ips.append(result)

    for ip in successful_ips:
        result = connect_rdp(ip, username, password)
        if result:
            print(result)

if __name__ == "__main__":
    main()

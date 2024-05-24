#!/bin/bash

# Hàm để đọc thông tin từ người dùng
read_input() {
    read -p "Nhập địa chỉ IP: " ip
    read -p "Nhập tên người dùng: " username
    read -sp "Nhập mật khẩu: " password
    echo
}

# Kiểm tra nếu xvfb chưa được khởi động
if ! pgrep -x "Xvfb" > /dev/null; then
    Xvfb :99 -screen 0 1024x768x16 &  # Khởi động Xvfb trên màn hình ảo :99
    export DISPLAY=:99
fi

while true; do
    read_input

    echo "Đang kiểm tra kết nối với $ip..."

    # Sử dụng xfreerdp để kiểm tra kết nối RDP
    xfreerdp /u:$username /p:$password /v:$ip +auth-only

    # Kiểm tra mã trạng thái của lệnh xfreerdp
    if [ $? -eq 0 ]; then
        echo "Kết nối RDP với $ip thành công."
    else
        echo "Kết nối RDP với $ip thất bại."
    fi

    read -p "Bạn có muốn kiểm tra địa chỉ IP khác không? (y/n): " continue_check
    if [[ "$continue_check" != "y" ]]; then
        break
    fi
done

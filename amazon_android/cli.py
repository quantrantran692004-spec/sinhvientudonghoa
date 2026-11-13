from __future__ import annotations

import argparse
import csv
import getpass
import sys

from .core import (DEVICES, Store, ToolError, check_play, create_avd, device_avd_name,
                   device_resources, doctor, emergency_stop, get_device, install_amazon,
                   open_amazon, print_json, start_device, stop_device)
from .setup import setup_sdk
from .cloud import CloudPhone, open_amazon as cloud_open_amazon, scan as cloud_scan
from .registration import status as registration_status, open_entry as registration_open_entry
from .batch import BatchItem, parse_proxy_line, prepare_five
from .swarmote_desktop import (ProxyConfig, create_profile as swarmote_create_profile,
                               inspect as swarmote_inspect, profile_status as swarmote_profile_status,
                               start_profile as swarmote_start_profile,
                               open_adb_shell as swarmote_open_adb_shell,
                               install_amazon as swarmote_install_amazon,
                               ready_for_registration as swarmote_ready)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="amazon-android", description="Điều khiển Android và Amazon Shopping thật")
    sub = p.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("doctor", "Kiểm tra môi trường thật"),
        ("setup-sdk", "Cài SDK từ Google sau khi xác nhận"),
        ("devices", "Xem 5 cấu hình và trạng thái"),
        ("test-report", "Báo cáo nghiệm thu thực tế"),
        ("cloud-scan", "Tìm điện thoại Swarmote đã mở ADB Shell"),
        ("swarmote-inspect", "Kiểm tra cửa sổ Swarmote không lấy chuột"),
    ):
        sub.add_parser(name, help=help_text)
    cloud_open = sub.add_parser("cloud-open-amazon", help="Mở Amazon trên điện thoại đám mây qua ADB")
    cloud_open.add_argument("serial", help="Serial ADB cục bộ, ví dụ 127.0.0.1:12345")
    registration = sub.add_parser("cloud-registration", help="Mở và kiểm tra trang bắt đầu đăng ký Amazon")
    registration.add_argument("serial")
    registration.add_argument("--open", action="store_true", help="Bấm nút Create an account nếu đang ở trang giới thiệu")
    profile = sub.add_parser("swarmote-create-profile", help="Tạo Profile với proxy qua UIA, không lấy chuột")
    profile.add_argument("--name", required=True, help="Tên Profile mới")
    profile.add_argument("--host", required=True, help="Host proxy")
    profile.add_argument("--port", required=True, type=int, help="Port proxy")
    profile.add_argument("--type", default="socks5", choices=("socks5", "http", "https"))
    profile.add_argument("--username", default="", help="Tên đăng nhập proxy; mật khẩu được hỏi riêng")
    status = sub.add_parser("swarmote-status", help="Trạng thái Profile Swarmote theo tên chính xác")
    status.add_argument("name")
    start_profile_cmd = sub.add_parser("swarmote-start", help="Khởi chạy Profile bằng UIA không lấy chuột")
    start_profile_cmd.add_argument("name")
    adb_shell_cmd = sub.add_parser("swarmote-adb-shell", help="Mở ADB Shell của Profile không lấy chuột")
    adb_shell_cmd.add_argument("name")
    cloud_install = sub.add_parser("swarmote-install-amazon", help="Cài Amazon từ Swarmote App Store và kiểm tra ADB")
    cloud_install.add_argument("name")
    cloud_install.add_argument("--timeout", type=int, default=180)
    ready = sub.add_parser("swarmote-ready", help="Khởi chạy Profile, cài Amazon và tới màn đăng ký")
    ready.add_argument("name")
    batch = sub.add_parser("swarmote-batch-five", help="Tạo 5 Profile/proxy và chuẩn bị Amazon trong một mẻ")
    batch.add_argument("--prefix", default="Amazon", help="Tiền tố tên Profile mới")
    batch.add_argument("--input", help="CSV cục bộ có cột profile_name,proxy; bỏ qua để nhập 5 lần trong terminal")
    for name, help_text in (
        ("create-avd", "Tạo AVD Google Play riêng"),
        ("start", "Khởi động emulator và đợi ADB"),
        ("stop", "Dừng emulator"),
        ("emergency-stop", "Dừng khẩn cấp emulator đã xác định"),
        ("status", "Xem ADB, CPU và RAM thực tế"),
        ("check-play", "Kiểm tra Play Store và Play Services"),
        ("install-amazon", "Mở Google Play và chờ cài Amazon"),
        ("open-amazon", "Mở và kiểm tra Amazon đang chạy"),
        ("logs", "Xem nhật ký trạng thái"),
    ):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("device", type=int, choices=range(1, 6), metavar="1-5")
        if name == "start":
            cmd.add_argument("--allow-second", action="store_true", help="Cho phép thiết bị thứ hai khi đủ RAM")
            cmd.add_argument("--force-low-memory", action="store_true", help="Bỏ ngưỡng RAM khi người dùng đã cho phép")
            cmd.add_argument("--timeout", type=int, default=240)
        if name == "install-amazon":
            cmd.add_argument("--timeout", type=int, default=600)
    return p


def report(store: Store) -> dict:
    environment = doctor()
    states = {row["number"]: row for row in store.devices()}
    results = []
    for number in (1, 2):
        d = get_device(number)
        adb_seen = d.serial in environment["adb_devices"] and device_avd_name(d) == d.avd
        results.append({"test": f"TEST {number:02d}", "status": "PASS" if adb_seen else "BLOCKED",
                        "evidence": f"ADB {'thấy' if adb_seen else 'không thấy'} {d.serial}"})
    for test in range(3, 13):
        results.append({"test": f"TEST {test:02d}", "status": "NOT TESTED",
                        "evidence": "Chưa thực hiện phép thử nghiệm thu trên Android/Amazon thật"})
    return {"environment": environment, "stored_states": states, "acceptance": results}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    try:
        if args.command == "doctor":
            print_json(doctor())
        elif args.command == "setup-sdk":
            setup_sdk()
            print("Đã hoàn tất cài SDK. Chạy doctor để xác minh.")
        elif args.command == "cloud-scan":
            print_json(cloud_scan())
        elif args.command == "cloud-open-amazon":
            print_json(cloud_open_amazon(CloudPhone(args.serial)))
        elif args.command == "cloud-registration":
            phone = CloudPhone(args.serial)
            print_json(registration_open_entry(phone) if args.open else registration_status(phone))
        elif args.command == "swarmote-inspect":
            print_json(swarmote_inspect())
        elif args.command == "swarmote-create-profile":
            password = getpass.getpass("Mật khẩu proxy: ") if args.username else ""
            print_json(swarmote_create_profile(args.name, ProxyConfig(
                args.type, args.host, args.port, args.username, password)))
        elif args.command == "swarmote-status":
            print_json(swarmote_profile_status(args.name))
        elif args.command == "swarmote-start":
            print_json(swarmote_start_profile(args.name))
        elif args.command == "swarmote-adb-shell":
            print_json(swarmote_open_adb_shell(args.name))
        elif args.command == "swarmote-install-amazon":
            print_json(swarmote_install_amazon(args.name, args.timeout))
        elif args.command == "swarmote-ready":
            print_json(swarmote_ready(args.name))
        elif args.command == "swarmote-batch-five":
            import datetime
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            items = []
            if args.input:
                with open(args.input, newline="", encoding="utf-8-sig") as source:
                    rows = list(csv.DictReader(source))
                if len(rows) != 5 or any(not row.get("proxy") for row in rows):
                    raise ToolError("CSV cần đúng 5 dòng, có cột proxy")
                for i, row in enumerate(rows, 1):
                    items.append(BatchItem(row.get("profile_name") or f"{args.prefix}-{stamp}-{i}",
                                           parse_proxy_line(row["proxy"])))
            else:
                for i in range(1, 6):
                    line = getpass.getpass(f"Proxy {i}/5 (host:port:username:password): ")
                    items.append(BatchItem(f"{args.prefix}-{stamp}-{i}", parse_proxy_line(line)))
            print_json(prepare_five(items, lambda i, stage, message:
                print(f"[{i + 1}/5] {stage}: {message}", file=sys.stderr)))
        else:
            store = Store()
            if args.command == "devices":
                stored = store.devices()
                print_json([{"name": d.name, "avd": d.avd, "serial": d.serial,
                             **stored[d.number - 1]} for d in DEVICES])
            elif args.command == "test-report":
                print_json(report(store))
            else:
                d = get_device(args.device)
                if args.command == "create-avd":
                    print(create_avd(d))
                elif args.command == "start":
                    seconds = start_device(d, store, args.allow_second, args.timeout,
                                           args.force_low_memory)
                    print(f"{d.name} sẵn sàng sau {seconds}s")
                elif args.command == "stop":
                    stop_device(d, store)
                    print(f"{d.name} đã dừng")
                elif args.command == "emergency-stop":
                    emergency_stop(d, store)
                    print(f"{d.name} đã dừng khẩn cấp")
                elif args.command == "status":
                    print_json(device_resources(d))
                elif args.command == "check-play":
                    check_play(d)
                    print(f"{d.name}: Google Play Store và Play Services đã cài")
                elif args.command == "install-amazon":
                    install_amazon(d, store, args.timeout)
                    print(f"{d.name}: Android Package Manager xác nhận Amazon Shopping đã cài")
                elif args.command == "open-amazon":
                    open_amazon(d, store)
                    print(f"{d.name}: Amazon Shopping đang chạy ở màn hình trước")
                elif args.command == "logs":
                    print_json(store.events(d.number))
        return 0
    except (ToolError, OSError, ValueError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

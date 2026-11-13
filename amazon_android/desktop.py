"""Self-service Swarmote desk. Input values stay in memory for this session."""
from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from .bulk_input import MAX_PROFILES, parse_column, parse_records, validate_card
from .batch_state import BatchDraft
from .core import ToolError
from .otp import otp_token, validate_otp_url
from .post_menu import PostMenuSession, PostMenuStep
from .account_flow import resume_common_index, verify_menu_open
from .q1_flow import build_q1_steps
from .q2_flow import build_q2_steps
from .cloud import CloudPhone
from .profile_registry import ProfileRegistry
from .registration import PHONE
from .runner import AccountData, RunJob, run_batch
from .settings import AppSettings, load_settings, save_settings
from .swarmote_desktop import (
    ProxyConfig, open_adb_shell, profile_status,
)


BG = "#EAF1F4"
SURFACE = "#FFFFFF"
INPUT = "#F6FAFC"
WHITE = "#FFFFFF"
INK = "#18313E"
MUTED = "#536C78"
BLUE = "#126D82"
BLUE_HOVER = "#0C586A"
PALE = "#DDEEF1"
BORDER = "#D1E0E5"
FIELD_BORDER = "#ACC4CC"
SECONDARY = "#EDF4F6"
SECONDARY_HOVER = "#DFECF0"
GREEN = "#167354"
RED = "#B23F4A"
SIDEBAR = "#1E4251"
SIDEBAR_HOVER = "#2B5969"
SIDEBAR_MUTED = "#C5D8DE"
SIDEBAR_SELECTED = "#D9F2F1"
SIDEBAR_SELECTED_HOVER = "#C7E8E8"
ROW_ALT = "#F7FAFB"
HERO = "#18313F"
HERO_BORDER = "#31586A"
HERO_INK = "#F6FAFB"
HERO_MUTED = "#C2D7E0"
HERO_ACCENT = "#A8EBE7"

BULK = (
    ("proxy", "Proxy", "host:port:user:password", "Proxy dư tự dùng thay proxy lỗi"),
    ("account", "Thông tin Amazon", "SĐT | Mật khẩu | Tên | Thẻ | URL OTP", "Dán 1 lần: tối đa 12 hàng"),
)

FIELD_KEYS = (
    "host", "port", "username", "proxy_password",
    "full_name", "phone", "amazon_password", "profile_name", "card", "otp_url",
)


def _automatic_resume_slots(items: list[dict]) -> list[int]:
    """Resume queued work after a restart; errors require an explicit Continue."""
    return [item["slot"] for item in items
            if item.get("state") in {"READY", "RUNNING"}
            and item.get("stage") != "MENU_OPEN"]


def _crystal_art() -> ctk.CTkImage:
    """Load the project-local 3D obsidian artwork for the hero panel."""
    art_path = Path(__file__).parent / "assets" / "obsidian_prism.png"
    with Image.open(art_path) as source:
        art = source.convert("RGBA")
    return ctk.CTkImage(light_image=art, dark_image=art, size=(270, 140))


def _edge_light(card: ctk.CTkFrame, color: str = "#B7D6DF") -> None:
    ctk.CTkFrame(card, fg_color=color, height=1,
                 corner_radius=1).place(relx=0.045, y=0, relwidth=0.91)


class Window:
    def __init__(self) -> None:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk(fg_color=BG)
        self.root.title("Swarmote · Amazon workspace")
        self.root.geometry("1380x800+20+15")
        self.root.minsize(1280, 720)

        self.count = tk.StringVar(value="1")
        try:
            self.settings = load_settings()
            self.settings_error = ""
        except ToolError as exc:
            self.settings = AppSettings()
            self.settings_error = str(exc)
        self.draft = BatchDraft()
        self.jobs: dict[int, RunJob] = {}
        self.post_menu_step_factories = {0: build_q1_steps, 1: build_q2_steps}
        self.post_menu_steps: dict[int, tuple[PostMenuStep, ...]] = {}
        self.post_menu_sessions: dict[int, PostMenuSession] = {}
        self.post_menu_stops: dict[int, threading.Event] = {}
        self.post_menu_workers: dict[int, threading.Thread] = {}
        self.menu_opened_at: dict[int, float] = {}
        self.phone_serials: dict[int, str] = {}
        self.attach_in_progress = False
        self.attaching_index = 0
        self.attach_events: queue.Queue[tuple[str, AccountData | None, str | None]] = queue.Queue()
        self.proxy_fallbacks = []
        try:
            self.registry = ProfileRegistry(persistent=False)
            self.registry_error = ""
        except ToolError as exc:
            self.registry = None
            self.registry_error = str(exc)
        self.restored_batch = None  # Every launch starts a fresh 1–12 workspace.
        self.selected = 0
        self.running = False
        self.cancel = threading.Event()
        self.events: queue.Queue[tuple[int, str, str, str | None]] = queue.Queue()
        self.otp_events: queue.Queue[tuple[str, int, str]] = queue.Queue()
        self.otp_status_events: queue.Queue[tuple[str, int, str]] = queue.Queue()
        self.values = [
            {key: tk.StringVar(value="") for key in FIELD_KEYS}
            for _ in range(MAX_PROFILES)
        ]
        predicted = (self.registry.preview_names(MAX_PROFILES) if self.registry else
                     [f"q{i}" for i in range(1, MAX_PROFILES + 1)])
        for index, row in enumerate(self.values):
            row["profile_name"].set(predicted[index])
        self.status = [("Chưa chạy", "idle") for _ in range(MAX_PROFILES)]
        self.otp_status = ["Chưa yêu cầu mã" for _ in range(MAX_PROFILES)]
        self.otp_codes = ["" for _ in range(MAX_PROFILES)]
        if self.restored_batch:
            batch_id, items = self.restored_batch
            self.count.set(str(len(items)))
            self.draft.batch_id = batch_id
            self.draft.proxy_count = len(items)
            self.draft.locked = True
            for item in items:
                index = item["slot"]
                self.jobs[index] = RunJob(index, batch_id, None)
                self.values[index]["profile_name"].set(item["name"])
                if item["stage"] == "MENU_OPEN":
                    self.status[index] = (f"{item['name']} đã tới menu", "done")
                elif item["state"] == "ERROR":
                    self.status[index] = (
                        f"Dừng tại {item['name']}: {item.get('last_error') or 'cần kiểm tra lại'}",
                        "error",
                    )
                elif item["state"] == "STOPPED":
                    self.status[index] = (f"{item['name']} đã dừng", "stopped")
                else:
                    self.status[index] = (
                        f"{item['name']} đã tạo · đang chờ tiếp tục", "queued",
                    )
        self.devices: list[ctk.CTkButton] = []
        self.row_buttons: list[ctk.CTkButton] = []
        self.bulk_boxes: dict[str, ctk.CTkEntry] = {}
        self.bulk_feedback: dict[str, ctk.CTkLabel] = {}
        self.detail_entries: dict[str, ctk.CTkEntry] = {}
        self.table_rows: list[dict[str, ctk.CTkLabel]] = []
        self._refresh_after_id: str | None = None

        self._build()
        if self.restored_batch:
            self._set_editing(False)
        for row in self.values:
            for value in row.values():
                value.trace_add("write", lambda *_: self._schedule_refresh())
        self._refresh_devices()
        self._select(0)
        if self.registry_error:
            self.run_note.configure(text=self.registry_error, text_color=RED)
        elif self.settings_error:
            self.run_note.configure(text=self.settings_error, text_color=RED)
        elif self.restored_batch:
            self.run_note.configure(text="Đã khôi phục mẻ đang chờ từ Swarmote",
                                    text_color=BLUE)
        self.root.after(150, self._poll)
        if self.restored_batch:
            self.root.after(450, self._resume_restored)

    def _label(self, parent, text: str, size: int = 13, *,
               color: str = MUTED, weight: str = "normal", **kwargs):
        return ctk.CTkLabel(
            parent, text=text, text_color=color,
            font=ctk.CTkFont(family="Segoe UI Variable", size=size, weight=weight),
            **kwargs,
        )

    def _build(self) -> None:
        header = ctk.CTkFrame(self.root, fg_color=SURFACE, corner_radius=0,
                              height=78, border_width=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        brand = ctk.CTkFrame(header, fg_color=SURFACE, corner_radius=10,
                             border_color=BORDER, border_width=1,
                             width=44, height=44)
        brand.pack(side="left", padx=(26, 14), pady=17)
        brand.pack_propagate(False)
        self._label(brand, "◆", 24, color=BLUE, weight="bold").place(
            relx=.5, rely=.5, anchor="center")
        name_block = ctk.CTkFrame(header, fg_color="transparent")
        name_block.pack(side="left")
        self._label(name_block, "SWARMOTE", 18,
                    color=INK, weight="bold").pack(anchor="w")
        self._label(name_block, "LOCAL CONTROL  ·  v0.1", 11,
                    color=MUTED).pack(anchor="w", pady=(1, 0))
        self._label(header, "●  Nhập liệu tại máy của bạn", 12,
                    color=GREEN).pack(side="right", padx=26)
        self.settings_button = ctk.CTkButton(
            header, text="Settings", width=112, height=38,
            corner_radius=9, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            border_width=1, border_color=BORDER, text_color=INK,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
            command=self._open_settings,
        )
        self.settings_button.pack(side="right", padx=(0, 3))

        shell = ctk.CTkFrame(self.root, fg_color="transparent")
        shell.pack(fill="both", expand=True, padx=16, pady=16)
        shell.grid_columnconfigure(1, weight=1)
        shell.grid_rowconfigure(0, weight=1)

        side = ctk.CTkFrame(shell, fg_color=SIDEBAR, corner_radius=10,
                            border_width=0, width=220)
        side.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        side.grid_propagate(False)
        self._build_sidebar(side)

        work_area = ctk.CTkFrame(shell, fg_color="transparent")
        work_area.grid(row=0, column=1, sticky="nsew")
        work_area.grid_columnconfigure(0, weight=6, minsize=580)
        work_area.grid_columnconfigure(1, weight=4, minsize=340)
        work_area.grid_rowconfigure(1, weight=1)
        self._build_hero(work_area)
        self.main = ctk.CTkScrollableFrame(work_area, fg_color="transparent",
                                            corner_radius=0)
        self.main.grid(row=1, column=0, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.detail_panel = ctk.CTkScrollableFrame(
            work_area, fg_color="transparent", corner_radius=0,
        )
        self.detail_panel.grid(row=1, column=1, sticky="nsew", padx=(14, 0))
        self.detail_panel.grid_columnconfigure(0, weight=1)
        self._build_main()
        self._build_actions(work_area)

    def _build_hero(self, parent) -> None:
        hero = ctk.CTkFrame(parent, fg_color=HERO, corner_radius=10,
                            border_width=1, border_color=HERO_BORDER, height=154)
        hero.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        hero.grid_propagate(False)
        _edge_light(hero, HERO_ACCENT)
        self.crystal_art = _crystal_art()
        self._label(hero, "", image=self.crystal_art, width=270,
                    height=140).pack(side="right", padx=(0, 26), pady=6)
        copy = ctk.CTkFrame(hero, fg_color="transparent")
        copy.pack(side="left", fill="both", expand=True, padx=28, pady=12)
        ctk.CTkLabel(copy, text="LOCAL WORKSPACE  /  01",
                     text_color=HERO_ACCENT,
                     font=ctk.CTkFont("Consolas", 12, weight="bold"),
                     anchor="w").pack(anchor="w")
        self._label(copy, "Swarmote Workspace", 27,
                    color=HERO_INK, weight="bold").pack(anchor="w", pady=(6, 2))
        self._label(copy, "Chuẩn bị và theo dõi tối đa 12 máy trong một mẻ.",
                    13, color=HERO_MUTED).pack(anchor="w")
        ctk.CTkLabel(copy, text="●  PROFILE  ·  START  ·  AMAZON  ·  MENU",
                     text_color=HERO_ACCENT,
                     font=ctk.CTkFont("Consolas", 11),
                     anchor="w").pack(anchor="w", pady=(8, 0))

    def _build_sidebar(self, side) -> None:
        top = ctk.CTkFrame(side, fg_color="transparent")
        top.pack(fill="x", padx=18, pady=(20, 8))
        self._label(top, "DANH SÁCH MÁY", 12,
                    color=SIDEBAR_MUTED, weight="bold").pack(anchor="w")
        count_row = ctk.CTkFrame(side, fg_color="transparent")
        count_row.pack(fill="x", padx=18, pady=(4, 13))
        self._label(count_row, "Số máy trong mẻ", 13,
                    color=WHITE, weight="bold").pack(side="left")
        self.count_menu = ctk.CTkOptionMenu(
            count_row, values=[str(i) for i in range(1, MAX_PROFILES + 1)],
            variable=self.count, command=lambda _: self._refresh_devices(),
            width=70, height=36, corner_radius=9,
            fg_color=SIDEBAR_HOVER, button_color=SIDEBAR_HOVER,
            button_hover_color=SIDEBAR, text_color=WHITE,
            dropdown_fg_color=SURFACE, dropdown_text_color=INK,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
        )
        self.count_menu.pack(side="right")
        ctk.CTkFrame(side, fg_color=SIDEBAR_HOVER, height=1).pack(fill="x", padx=18)

        device_list = ctk.CTkScrollableFrame(side, fg_color=SIDEBAR, corner_radius=0,
                                            scrollbar_button_color="#668995",
                                            scrollbar_button_hover_color="#86A9B3")
        device_list.pack(fill="both", expand=True, padx=7, pady=(8, 0))
        for i in range(MAX_PROFILES):
            button = ctk.CTkButton(
                device_list, text="", anchor="w", height=48, corner_radius=10,
                font=ctk.CTkFont("Segoe UI Variable", 12, weight="bold"),
                text_color_disabled="#9BB9C1",
                command=lambda idx=i: self._select(idx),
            )
            button.pack(fill="x", padx=4, pady=(5 if i == 0 else 2, 2))
            self.devices.append(button)

        self.reset_button = ctk.CTkButton(
            side, text="Làm lại / mẻ mới", height=42, corner_radius=9,
            fg_color=SIDEBAR_HOVER, hover_color="#356879",
            text_color=WHITE, text_color_disabled="#9BB9C1",
            border_color="#668995", border_width=1,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
            command=self._reset,
        )
        self.reset_button.pack(fill="x", padx=13, pady=(14, 8))

    def _build_main(self) -> None:
        bulk_card = ctk.CTkFrame(self.main, fg_color=SURFACE, corner_radius=10,
                                 border_width=1, border_color=BORDER)
        bulk_card.grid(row=0, column=0, sticky="ew")
        _edge_light(bulk_card)
        bulk_card.grid_columnconfigure(1, weight=1)
        self._label(bulk_card, "Dán nhanh theo danh sách", 18,
                    color=INK, weight="bold").grid(
                        row=0, column=0, columnspan=2, sticky="w",
                        padx=22, pady=(18, 2))
        self._label(bulk_card, "Copy cả bảng Markdown hoặc 1–12 hàng cùng lúc, gồm cả hàng gạch phân cách.",
                    12, wraplength=530, justify="left").grid(row=1, column=0, columnspan=4,
                             sticky="w", padx=22, pady=(0, 10))
        for index, (kind, title, placeholder, hint) in enumerate(BULK):
            self._bulk_row(bulk_card, kind, title, placeholder, hint,
                           index + 2)
        self.validation_label = self._label(bulk_card, "Cần dán proxy để chạy", 13)
        self.validation_label.grid(row=4, column=0, columnspan=4,
                                   sticky="w", padx=22, pady=(5, 16))

        self._build_preview_table()

        detail_card = ctk.CTkFrame(self.detail_panel, fg_color=SURFACE, corner_radius=10,
                                   border_width=1, border_color=BORDER)
        detail_card.grid(row=0, column=0, sticky="ew", pady=(2, 0))
        _edge_light(detail_card)
        detail_card.grid_columnconfigure((0, 1), weight=1, uniform="detail")
        title_row = ctk.CTkFrame(detail_card, fg_color="transparent")
        title_row.grid(row=0, column=0, columnspan=2, sticky="ew",
                       padx=22, pady=(20, 6))
        self.detail_title = self._label(title_row, "Máy 1", 18,
                                        color=INK, weight="bold")
        self.detail_title.pack(side="left")
        self._label(detail_card, "Bạn có thể sửa từng máy sau khi dán hàng loạt.",
                    12, wraplength=305, justify="left").grid(
                        row=1, column=0, columnspan=2,
                        sticky="w", padx=20, pady=(0, 6))
        self.detail_status = self._label(
            detail_card, "Chưa chạy", 12, color=MUTED,
            wraplength=305, justify="left",
        )
        self.detail_status.grid(row=2, column=0, columnspan=2,
                                sticky="w", padx=20, pady=(0, 14))

        self._label(detail_card, "Dán 1–12 proxy để tự điền", 13,
                    color=INK, weight="bold").grid(
                        row=3, column=0, columnspan=2, sticky="w", padx=20)
        self.proxy_line = ctk.CTkEntry(
            detail_card, placeholder_text="host:port:user:password",
            height=44, corner_radius=8, border_color=FIELD_BORDER,
            fg_color=INPUT, text_color=INK, placeholder_text_color=MUTED,
            font=ctk.CTkFont("Segoe UI Variable", 13),
        )
        self.proxy_line.grid(row=4, column=0, columnspan=2,
                             sticky="ew", padx=20, pady=(5, 6))
        self.proxy_line.bind("<Control-v>", self._paste_single_proxy, add="+")
        self.proxy_line.bind("<Return>", lambda _: self._split_single_proxy())
        self._label(detail_card, "Một proxy vào máy đang chọn; nhiều proxy tự chia Máy 1–12.",
                    11, wraplength=305, justify="left").grid(row=5, column=0, columnspan=2, sticky="w",
                             padx=20, pady=(0, 12))

        fields = [
            ("Host", "host", 6, 0, False),
            ("Port", "port", 6, 1, False),
            ("User proxy", "username", 7, 0, False),
            ("Pass proxy", "proxy_password", 7, 1, True),
            ("Tên Amazon", "full_name", 8, 0, False),
            ("Số điện thoại", "phone", 8, 1, False),
            ("Mật khẩu Amazon", "amazon_password", 9, 0, True),
            ("Tên Profile (dự kiến, tự cấp)", "profile_name", 9, 1, False),
            ("Thẻ của số điện thoại này", "card", 10, 0, True),
            ("URL OTP của số điện thoại này", "otp_url", 11, 0, False),
        ]
        for label, key, row, col, _secret in fields:
            cell = ctk.CTkFrame(detail_card, fg_color="transparent")
            cell.grid(row=row, column=col,
                      columnspan=2 if key in {"card", "otp_url"} else 1, sticky="ew",
                      padx=(20, 20) if key in {"card", "otp_url"} else
                           (20 if col == 0 else 8, 20 if col == 1 else 8),
                      pady=(0, 13))
            self._label(cell, label, 13, color=INK,
                        weight="bold").pack(anchor="w", pady=(0, 5))
            entry = ctk.CTkEntry(
                cell, height=42, corner_radius=8, border_color=FIELD_BORDER,
                fg_color=INPUT, text_color=INK, placeholder_text_color=MUTED,
                font=ctk.CTkFont("Segoe UI Variable", 13),
                show="•" if _secret else "",
            )
            entry.pack(fill="x")
            if key == "profile_name":
                entry.configure(state="disabled")
            self.detail_entries[key] = entry
        self.detail_entries["host"].bind("<Control-v>", self._paste_host, add="+")
        for key, kind in (
            ("full_name", "name"),
            ("phone", "phone"),
            ("amazon_password", "password"),
        ):
            self.detail_entries[key].bind(
                "<Control-v>",
                lambda _event, column=kind: self._paste_detail_column(column),
                add="+",
            )
        self._label(
            detail_card,
            "Điểm dừng: menu ba gạch. Thông tin Amazon chỉ được phân bổ, chưa nhập vào app.",
            12, color=MUTED,
        ).grid(row=12, column=0, columnspan=2, sticky="w",
               padx=20, pady=(0, 10))
        otp_row = ctk.CTkFrame(detail_card, fg_color=SECONDARY, corner_radius=8)
        otp_row.grid(row=13, column=0, columnspan=2, sticky="ew",
                     padx=20, pady=(0, 17))
        otp_row.grid_columnconfigure(0, weight=1)
        self.otp_detail_status = self._label(
            otp_row, "OTP · Chưa yêu cầu mã", 12, color=INK, anchor="w")
        self.otp_detail_status.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 2))
        self.otp_detail_code = self._label(
            otp_row, "—", 18, color=BLUE, weight="bold", anchor="w")
        self.otp_detail_code.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        self.otp_copy_button = ctk.CTkButton(
            otp_row, text="Sao chép", width=95, height=36,
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, border_color=FIELD_BORDER, border_width=1,
            state="disabled", command=self._copy_otp,
        )
        self.otp_copy_button.grid(row=0, column=1, rowspan=2,
                                  padx=10, pady=8)
        self.attach_profile_button = ctk.CTkButton(
            detail_card, text="Thử q1 từ menu ba gạch", height=40,
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, border_color=FIELD_BORDER, border_width=1,
            command=self._attach_from_menu,
        )
        self.attach_profile_button.grid(row=14, column=0, columnspan=2,
                                   sticky="ew", padx=20, pady=(0, 17))

    def _build_actions(self, parent) -> None:
        action = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=10,
                              border_width=1, border_color=BORDER)
        action.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        self.run_button = ctk.CTkButton(
            action, text="Chạy 1 máy trong mẻ", width=214, height=46,
            corner_radius=10, fg_color=BLUE, hover_color=BLUE_HOVER,
            border_width=1, border_color=BLUE,
            text_color=WHITE,
            font=ctk.CTkFont("Segoe UI Variable", 14, weight="bold"),
            command=self._start,
        )
        self.run_button.pack(side="left", padx=(12, 0), pady=10)
        self.stop_button = ctk.CTkButton(
            action, text="Dừng sau bước hiện tại", width=185, height=46,
            corner_radius=9, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
            state="disabled",
            command=self._request_stop,
        )
        self.stop_button.pack(side="left", padx=9)
        ctk.CTkButton(
            action, text="Kiểm tra phân bổ", width=146, height=46,
            corner_radius=9, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, border_color=FIELD_BORDER, border_width=1,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
            command=self._show_preview_table,
        ).pack(side="left")
        self.run_note = self._label(action, "Sẵn sàng nhập liệu", 12,
                                    wraplength=260, justify="right")
        self.run_note.pack(side="right", padx=15)

    def _show_preview_table(self) -> None:
        self.root.update_idletasks()
        canvas = self.main._parent_canvas
        bounds = canvas.bbox("all")
        if bounds:
            canvas.yview_moveto(
                min(1.0, self.preview_table.winfo_y() /
                    max(1, bounds[3] - bounds[1]))
            )

    def _show_row_status(self, index: int) -> None:
        name = self.values[index]["profile_name"].get()
        messagebox.showinfo(f"Máy {index + 1} · {name}",
                            f"{self.status[index][0]}\nOTP: {self.otp_status[index]}")

    def _copy_otp(self) -> None:
        code = self.otp_codes[self.selected]
        if code:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)

    def show_otp(self, batch_id: str, index: int, code: str) -> bool:
        """UI-thread hook; discard a late OTP from a batch already reset."""
        if batch_id != self.draft.batch_id:
            return False
        if not 0 <= index < MAX_PROFILES or not (len(code) == 6 and code.isascii() and code.isdigit()):
            raise ValueError("OTP must be six ASCII digits for an existing machine")
        self.otp_codes[index] = code
        self.otp_status[index] = "Đã lấy mã"
        if self.selected == index:
            self._refresh_otp_detail()
        self._refresh_table()
        return True

    def show_otp_status(self, batch_id: str, index: int, status: str) -> bool:
        if batch_id != self.draft.batch_id:
            return False
        self.otp_status[index] = status
        if self.selected == index:
            self._refresh_otp_detail()
        self._refresh_table()
        return True

    def _refresh_otp_detail(self) -> None:
        self.otp_detail_status.configure(text=f"OTP · {self.otp_status[self.selected]}")
        code = self.otp_codes[self.selected]
        self.otp_detail_code.configure(text=code or "—")
        self.otp_copy_button.configure(state="normal" if code else "disabled")

    def _maybe_show_preview(self) -> None:
        keys = ("host", "port", "full_name", "phone", "amazon_password", "otp_url")
        if all(all(self.values[i][key].get() for key in keys)
               for i in range(int(self.count.get()))):
            self.root.after(80, self._show_preview_table)

    def _build_preview_table(self) -> None:
        table = ctk.CTkFrame(self.main, fg_color=SURFACE, corner_radius=10,
                             border_width=1, border_color=BORDER)
        self.preview_table = table
        table.grid(row=1, column=0, sticky="ew", pady=(20, 0))
        _edge_light(table)
        for col, weight in enumerate((1, 2, 3, 2, 1)):
            table.grid_columnconfigure(col, weight=weight)
        self._label(table, "Bảng phân bổ", 18, color=INK,
                    weight="bold").grid(row=0, column=0, columnspan=2,
                                        sticky="w", padx=20, pady=(17, 0))
        self._label(table, "Bấm một hàng để sửa máy đó", 12).grid(
            row=0, column=2, columnspan=3, sticky="e", padx=20,
            pady=(17, 0))
        headings = ("MÁY", "PROXY", "THÔNG TIN", "TRẠNG THÁI", "")
        keys = ("machine", "proxy", "account", "status")
        for col, heading in enumerate(headings):
            self._label(table, heading, 11, color=MUTED,
                        weight="bold", anchor="w").grid(
                            row=1, column=col, sticky="ew",
                            padx=(20 if col == 0 else 6, 12 if col == 4 else 6),
                            pady=(13, 9))
        for index in range(MAX_PROFILES):
            cells = {}
            for col, key in enumerate(keys):
                label = self._label(
                    table, "", 13, color=MUTED, anchor="w",
                    height=62, corner_radius=7,
                )
                label.grid(row=index + 2, column=col, sticky="ew",
                           padx=(16 if col == 0 else 3, 4),
                           pady=2)
                if key == "status":
                    label.bind("<Button-1>", lambda _event, i=index: self._show_row_status(i))
                else:
                    label.bind("<Button-1>", lambda _event, i=index: self._select(i))
                cells[key] = label
            self.table_rows.append(cells)
            button = ctk.CTkButton(
                table, text="Tiếp tục", width=78, height=36, corner_radius=8,
                fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                text_color=INK, border_width=1, border_color=FIELD_BORDER,
                font=ctk.CTkFont("Segoe UI Variable", 12, weight="bold"),
                command=lambda i=index: self._continue_profile(i),
            )
            button.grid(row=index + 2, column=4, padx=(3, 12), pady=2)
            self.row_buttons.append(button)
        ctk.CTkFrame(table, fg_color="transparent", height=5).grid(
            row=MAX_PROFILES + 2, column=0, columnspan=5)

    def _bulk_row(self, parent, kind: str, title: str,
                  placeholder: str, _hint: str, row: int) -> None:
        self._label(parent, title, 13, color=INK,
                    weight="bold").grid(row=row, column=0, sticky="w",
                                        padx=(20, 10), pady=7)
        entry = ctk.CTkEntry(
            parent, placeholder_text=(
                f"Ctrl+V 1–100 proxy · {placeholder}" if kind == "proxy" else
                f"Ctrl+V 1–12 dòng · {placeholder}"),
            height=42, corner_radius=8, border_color=FIELD_BORDER,
            fg_color=INPUT, text_color=INK, placeholder_text_color=MUTED,
            font=ctk.CTkFont("Segoe UI Variable", 13),
        )
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 8), pady=5)
        entry.bind("<Control-v>",
                   lambda _event, k=kind: self._paste_bulk_entry(k), add="+")
        entry.bind("<Return>", lambda _event, k=kind: self._apply_bulk(k))
        self.bulk_boxes[kind] = entry
        ctk.CTkButton(
            parent, text="Dán clipboard", width=116, height=42,
            corner_radius=8, fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
            text_color=INK, border_width=1, border_color=FIELD_BORDER,
            font=ctk.CTkFont("Segoe UI Variable", 12, weight="bold"),
            command=lambda k=kind: self._paste_from_clipboard(k),
        ).grid(row=row, column=2, padx=(0, 8), pady=5)
        feedback = self._label(parent, "Chưa dán", 12)
        feedback.grid(row=row, column=3, sticky="w", padx=(0, 16), pady=3)
        self.bulk_feedback[kind] = feedback
        if row == 3:
            ctk.CTkFrame(parent, fg_color="transparent", height=5).grid(
                row=5, column=0, columnspan=4)

    def _paste_bulk_entry(self, kind: str) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            return None
        self._apply_bulk_text(kind, copied)
        return "break"

    def _paste_from_clipboard(self, kind: str) -> None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            messagebox.showerror("Clipboard trống", "Không có văn bản để dán.")
            return
        self._apply_bulk_text(kind, copied)

    def _apply_account_text(self, copied: str) -> None:
        records = parse_records(copied, account_table=True)
        self.draft.replace("account", len(records))
        for target in self.values:
            for key in ("phone", "amazon_password", "full_name", "card", "otp_url"):
                target[key].set("")
        self.otp_status = ["Chưa yêu cầu mã" for _ in range(MAX_PROFILES)]
        self.otp_codes = ["" for _ in range(MAX_PROFILES)]
        for index, record in enumerate(records):
            target = self.values[index]
            target["phone"].set(record.phone)
            target["amazon_password"].set(record.password)
            target["full_name"].set(record.full_name)
            target["card"].set(record.card)
            target["otp_url"].set(record.otp_url)
        self.count.set(str(self.draft.count))
        self._refresh_devices()
        self.bulk_feedback["account"].configure(
            text=f"✓ {len(records)} máy", text_color=GREEN)
        if all(record.proxy for record in records):
            self.bulk_feedback["proxy"].configure(
                text=f"✓ {len(records)} máy", text_color=GREEN)
        self.run_note.configure(
            text=f"Đã gán {len(records)} hàng vào mẻ; chưa nhập vào Amazon", text_color=GREEN)
        self.bulk_boxes["account"].delete(0, "end")
        self._refresh_otp_detail()
        self._maybe_show_preview()

    def _apply_bulk(self, kind: str) -> None:
        self._apply_bulk_text(kind, self.bulk_boxes[kind].get())

    def _apply_bulk_text(self, kind: str, content: str) -> None:
        try:
            if self.draft.locked:
                raise ToolError("Mẻ đã chạy; bấm Mẻ mới để nhập dữ liệu khác")
            if kind == "account":
                self._apply_account_text(content)
                return
            parsed = parse_column(kind, content)
            self.draft.replace("proxy", len(parsed))
        except (ToolError, ValueError) as exc:
            self.bulk_feedback[kind].configure(text=str(exc), text_color=RED)
            self.run_note.configure(text=str(exc), text_color=RED)
            return
        for target in self.values:
            for key in ("host", "port", "username", "proxy_password"):
                target[key].set("")
        for index, value in enumerate(parsed[:MAX_PROFILES]):
            target = self.values[index]
            target["host"].set(value.host)
            target["port"].set(str(value.port))
            target["username"].set(value.username)
            target["proxy_password"].set(value.password)
        if kind == "proxy":
            self.proxy_fallbacks = parsed[MAX_PROFILES:]
        self.count.set(str(self.draft.count))
        self._refresh_devices()
        self.bulk_feedback[kind].configure(
            text=(f"✓ {min(len(parsed), MAX_PROFILES)} máy · "
                  f"{max(0, len(parsed) - MAX_PROFILES)} dự phòng"
                  if kind == "proxy" else f"✓ {len(parsed)} máy"),
            text_color=GREEN)
        self.run_note.configure(text=f"Đã gán {len(parsed)} proxy vào mẻ",
                                text_color=GREEN)
        self.bulk_boxes[kind].delete(0, "end")
        self._maybe_show_preview()

    def _paste_single_proxy(self, _event) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            self.root.after(80, self._split_single_proxy)
            return None
        self._accept_proxy_text(copied)
        return "break"

    def _paste_host(self, _event) -> str | None:
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            self.root.after(80, self._split_host_if_full)
            return None
        if copied.count(":") >= 3:
            self._accept_proxy_text(copied)
            return "break"
        return None

    def _paste_detail_column(self, kind: str) -> str | None:
        if self.draft.locked:
            return "break"
        try:
            copied = self.root.clipboard_get()
        except tk.TclError:
            return None
        if "\n" not in copied and "\r" not in copied:
            return None
        try:
            parsed = parse_column(kind, copied)
        except (ToolError, ValueError) as exc:
            self.run_note.configure(text=str(exc), text_color=RED)
            return "break"
        key = {"name": "full_name", "phone": "phone",
               "password": "amazon_password"}[kind]
        for index, value in enumerate(parsed):
            self.values[index][key].set(value)
        self.count.set(str(max(int(self.count.get()), len(parsed))))
        self.run_note.configure(
            text=f"Đã tự điền {len(parsed)} {kind} vào Máy 1–{len(parsed)}",
            text_color=GREEN,
        )
        self._refresh_devices()
        return "break"

    def _split_host_if_full(self) -> None:
        if self.detail_entries["host"].get().count(":") >= 3:
            self.proxy_line.delete(0, "end")
            self.proxy_line.insert(0, self.detail_entries["host"].get())
            self._split_single_proxy()

    def _split_single_proxy(self) -> None:
        raw = self.proxy_line.get()
        if not raw.strip():
            return
        self._accept_proxy_text(raw)

    def _accept_proxy_text(self, raw: str) -> None:
        try:
            if self.draft.locked:
                raise ToolError("Mẻ đã chạy; bấm Mẻ mới để nhập dữ liệu khác")
            parsed = parse_column("proxy", raw)
            if len(parsed) > 1:
                self.draft.replace("proxy", len(parsed))
                self.proxy_fallbacks = parsed[MAX_PROFILES:]
            else:
                self.draft.replace("proxy", max(self.draft.proxy_count, self.selected + 1))
        except (ToolError, ValueError) as exc:
            self.run_note.configure(text=str(exc), text_color=RED)
            return
        if len(parsed) > 1:
            for target in self.values:
                for key in ("host", "port", "username", "proxy_password"):
                    target[key].set("")
        for index, proxy in enumerate(parsed[:MAX_PROFILES]):
            row = self.values[self.selected if len(parsed) == 1 else index]
            for key, value in (
                ("host", proxy.host), ("port", str(proxy.port)),
                ("username", proxy.username), ("proxy_password", proxy.password),
            ):
                row[key].set(value)
        self.count.set(str(self.draft.count))
        self.proxy_line.delete(0, "end")
        result = (f"Đã tự điền {len(parsed)} proxy vào Máy 1–{len(parsed)}"
                  if len(parsed) > 1 else
                  f"Đã điền proxy vào Máy {self.selected + 1}")
        self.run_note.configure(text=result, text_color=GREEN)
        self._refresh_devices()

    def _schedule_refresh(self) -> None:
        if self._refresh_after_id is None:
            self._refresh_after_id = self.root.after(40, self._delayed_refresh)

    def _delayed_refresh(self) -> None:
        self._refresh_after_id = None
        self._refresh_devices()

    def _refresh_devices(self) -> None:
        if self._refresh_after_id is not None:
            self.root.after_cancel(self._refresh_after_id)
            self._refresh_after_id = None
        if not self.devices:
            return
        active = int(self.count.get())
        post_busy = any(session.state == "RUNNING"
                        for session in self.post_menu_sessions.values())
        has_post_menu = bool(self.post_menu_sessions)
        partial_jobs = self.draft.locked and any(
            index not in self.jobs for index in range(active))
        issue = self._input_issue()
        if self.registry_error:
            validation = self.registry_error
        elif self.draft.locked:
            validation = (f"Mẻ đang chạy · tối đa {self.run_group_size} máy Running · "
                          f"{active} Profile" if self.running else
                          f"Mẻ đã khóa · {active} máy · bấm Mẻ mới để nhập mẻ tiếp theo")
        elif issue:
            validation = issue
        else:
            validation = f"✓ {active} máy đã phân bổ đúng · thông tin Amazon chưa nhập vào app"
        self.validation_label.configure(
            text=validation,
            text_color=RED if issue else GREEN if not self.draft.locked else MUTED,
        )
        self.run_button.configure(
            text=f"Chạy {active} máy trong mẻ",
            state="disabled" if self.running or self.attach_in_progress or post_busy or has_post_menu or partial_jobs or issue else "normal",
            fg_color=SECONDARY if self.running or self.attach_in_progress or post_busy or has_post_menu or partial_jobs or issue else BLUE,
            text_color=MUTED if self.running or self.attach_in_progress or post_busy or has_post_menu or partial_jobs or issue else WHITE,
        )
        self.stop_button.configure(state="normal" if self.running or post_busy else "disabled")
        self.reset_button.configure(state="disabled" if self.running or post_busy or
                                    self.attach_in_progress else "normal")
        self.attach_profile_button.configure(
            text=f"Thử q{self.selected + 1} từ menu ba gạch",
            state="normal" if self.selected in self.post_menu_step_factories
            and self.selected not in self.jobs and not self.running
            and not self.attach_in_progress else "disabled")
        if self.selected >= active:
            self.selected = active - 1
            self._select(self.selected)
        for i, button in enumerate(self.devices):
            text, state = self.status[i]
            has_profile = self.draft.locked and i in self.jobs and not self.values[i]["host"].get()
            has_proxy = bool(self.values[i]["host"].get()) or has_profile
            has_account = all(self.values[i][key].get()
                              for key in ("full_name", "phone", "amazon_password"))
            summary = {
                "done": "Đã mở menu",
                "error": "Cần xử lý",
                "uncertain": "Cần xác minh",
                "stopped": "Đã dừng",
                "created": "Profile OK",
                "started": "Đã mở máy",
                "installed": "Đã cài Amazon",
                "queued": "Đợi máy trống",
                "post_running": "Đang tự động hóa",
                "post_paused": "Lỗi · sửa rồi tiếp tục",
                "post_done": "Đã xong bước q1",
            }.get(state, text) if state != "idle" else (
                "Proxy sẵn sàng" if has_proxy else
                "Đã nhập thông tin" if has_account else "Chưa nhập")
            checks = (
                ("P", bool(self.values[i]["host"].get() and
                           self.values[i]["port"].get()) or has_profile),
                ("T", bool(self.values[i]["full_name"].get())),
                ("S", bool(self.values[i]["phone"].get())),
                ("MK", bool(self.values[i]["amazon_password"].get())),
                ("THẺ", bool(self.values[i]["card"].get())),
                ("OTP", bool(self.values[i]["otp_url"].get())),
            )
            marks = "   ".join(f"{label}{'✓' if ok else '·'}"
                                 for label, ok in checks)
            button.configure(
                text=f"  Máy {i + 1} · {summary}\n  {marks}",
                state="normal" if i < active else "disabled",
                fg_color=SIDEBAR_SELECTED if i == self.selected else SIDEBAR,
                hover_color=SIDEBAR_SELECTED_HOVER if i == self.selected else SIDEBAR_HOVER,
                text_color=INK if i == self.selected else WHITE,
            )
            session = self.post_menu_sessions.get(i)
            if session is not None:
                may_continue = session.state == "PAUSED"
            elif self.draft.locked:
                may_continue = (i in self.jobs and not self.running
                                and state != "menu_only")
            else:
                may_continue = not self.running and not issue
            self.row_buttons[i].configure(
                state="normal" if i < active and may_continue else "disabled")
        self._refresh_table()

    def _input_issue(self) -> str:
        if self.registry is None:
            return self.registry_error
        if self.draft.locked and self.jobs:
            return ""
        active = int(self.count.get())
        if self.draft.proxy_count and self.draft.proxy_count < active:
            return f"Cần ít nhất {active} proxy; hiện có {self.draft.proxy_count}"
        if self.draft.account_count not in {0, active}:
            return f"Thông tin Amazon có {self.draft.account_count} hàng, cần {active}"
        for index in range(active):
            row = self.values[index]
            if not all(row[key].get().strip() for key in
                       ("host", "port", "username", "proxy_password")):
                return f"Máy {index + 1}: proxy chưa đủ"
            try:
                ProxyConfig("socks5", row["host"].get().strip(),
                            int(row["port"].get()), row["username"].get(),
                            row["proxy_password"].get())
            except (ToolError, ValueError) as exc:
                return f"Máy {index + 1}: {exc}"
        account_keys = ("phone", "amazon_password", "full_name", "card", "otp_url")
        account_rows = [any(self.values[i][key].get() for key in account_keys)
                        for i in range(active)]
        if any(account_rows) and not all(
            all(self.values[i][key].get() for key in account_keys)
            for i in range(active)
        ):
            return "Thông tin Amazon chưa đủ cho mọi máy trong mẻ"
        if any(account_rows):
            tokens = []
            for index in range(active):
                row = self.values[index]
                if not PHONE.fullmatch(row["phone"].get().strip()):
                    return f"Máy {index + 1}: số điện thoại sai định dạng"
                password = row["amazon_password"].get()
                if len(password) < 8 or any(ord(c) < 33 or ord(c) > 126 for c in password):
                    return f"Máy {index + 1}: mật khẩu cần ít nhất 8 ký tự ASCII không dấu cách"
                if len(row["full_name"].get()) > 100:
                    return f"Máy {index + 1}: tên Amazon quá dài"
                if row["card"].get():
                    try:
                        validate_card(row["card"].get())
                    except ToolError as exc:
                        return f"Máy {index + 1}: {exc}"
                try:
                    tokens.append(otp_token(row["otp_url"].get()))
                except ToolError as exc:
                    return f"Máy {index + 1}: {exc}"
            if len(tokens) != len(set(tokens)):
                return "URL OTP bị trùng giữa các máy"
        return ""

    def _refresh_table(self) -> None:
        for index, cells in enumerate(self.table_rows):
            values = self.values[index]
            host = values["host"].get()
            proxy_text = (f"{host}:{values['port'].get()}" if host else
                          "Profile đã tạo" if self.draft.locked and index in self.jobs else "—")
            otp_url = values["otp_url"].get()
            try:
                url_summary = f"URL …{otp_token(otp_url)[-6:]}" if otp_url else "URL —"
            except ToolError:
                url_summary = "URL sai"
            card = values["card"].get()
            card_summary = f"Thẻ ••••{card.split('|', 1)[0][-4:]}" if card else "Thẻ —"
            account_text = (f"{values['full_name'].get() or 'Chưa có tên'}\n"
                            f"{values['phone'].get() or 'Chưa có SĐT'} · "
                            f"{'MK ✓' if values['amazon_password'].get() else 'MK —'} · {card_summary}\n"
                            f"{url_summary}")
            run_status = {"idle": "Chưa chạy", "running": "Đang chạy",
                          "created": "Profile OK", "started": "Đã mở máy",
                          "installed": "Đã cài app", "queued": "Đợi máy trống",
                          "done": "Đã tới menu",
                          "post_running": "Đang tự động hóa",
                          "post_paused": "Lỗi · bấm xem",
                          "post_done": "Đã bấm Create",
                          "error": "Lỗi · bấm xem", "uncertain": "Chưa rõ · xem",
                          "stopped": "Đã dừng"}.get(
                              self.status[index][1], self.status[index][0])
            items = {
                "machine": values["profile_name"].get() or f"Máy {index + 1}",
                "proxy": proxy_text[:24] + ("…" if len(proxy_text) > 24 else ""),
                "account": account_text,
                "status": f"{run_status}\nOTP: {self.otp_status[index]}",
            }
            status_color = (RED if self.status[index][1] in {"error", "uncertain", "post_paused"}
                            else GREEN if self.status[index][1] in {"done", "post_done"}
                            else BLUE if self.status[index][1] in
                            {"running", "created", "started", "installed", "post_running"}
                            else MUTED)
            for key, cell in cells.items():
                cell.configure(
                    text=(items[key] if key in {"account", "status"} else
                          items[key][:46] + ("…" if len(items[key]) > 46 else "")),
                    fg_color=PALE if index == self.selected else
                             ROW_ALT if index % 2 else SURFACE,
                    text_color=(status_color if key == "status" else
                                BLUE if index == self.selected else
                                INK if index < int(self.count.get()) else MUTED),
                )

    def _select(self, index: int) -> None:
        if index >= int(self.count.get()):
            return
        self.selected = index
        if not self.draft.locked:
            self.proxy_line.delete(0, "end")
        for key, entry in self.detail_entries.items():
            entry.configure(textvariable=self.values[index][key])
        self.detail_title.configure(text=f"Máy {index + 1}")
        self.detail_status.configure(text=self.status[index][0])
        self._refresh_otp_detail()
        self._refresh_devices()

    def _reset(self) -> None:
        if self.running or self.attach_in_progress or any(session.state == "RUNNING"
                               for session in self.post_menu_sessions.values()):
            return
        if self.registry is not None:
            self.registry = ProfileRegistry(persistent=False)
        self._set_editing(True)
        self.draft = self.draft.new()
        self.jobs.clear()
        self.post_menu_sessions.clear()
        self.post_menu_stops.clear()
        self.post_menu_workers.clear()
        self.post_menu_steps.clear()
        self.menu_opened_at.clear()
        self.phone_serials.clear()
        self.proxy_fallbacks.clear()
        for row in self.values:
            for value in row.values():
                value.set("")
        predicted = (self.registry.preview_names(MAX_PROFILES) if self.registry else
                     [f"q{i}" for i in range(1, MAX_PROFILES + 1)])
        for index, row in enumerate(self.values):
            row["profile_name"].set(predicted[index])
        for box in self.bulk_boxes.values():
            box.delete(0, "end")
        for kind, _, _, _hint in BULK:
            self.bulk_feedback[kind].configure(text="Chưa dán", text_color=MUTED)
        self.status = [("Chưa chạy", "idle") for _ in range(MAX_PROFILES)]
        self.otp_status = ["Chưa yêu cầu mã" for _ in range(MAX_PROFILES)]
        self.otp_codes = ["" for _ in range(MAX_PROFILES)]
        self.count.set("1")
        self._select(0)
        self.run_note.configure(text="Sẵn sàng nhập liệu", text_color=MUTED)

    def _set_editing(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for box in self.bulk_boxes.values():
            box.configure(state=state)
        for key, entry in self.detail_entries.items():
            if key != "profile_name":
                entry.configure(state=state)
        self.proxy_line.configure(state=state)
        self.count_menu.configure(state=state)

    def _open_settings(self) -> None:
        current = getattr(self, "settings_window", None)
        if current is not None and current.winfo_exists():
            current.lift()
            return
        dialog = ctk.CTkToplevel(self.root, fg_color=BG)
        self.settings_window = dialog
        dialog.title("Settings · Swarmote")
        dialog.geometry("480x450+120+100")
        dialog.resizable(False, False)
        card = ctk.CTkFrame(dialog, fg_color=SURFACE, corner_radius=10,
                            border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, padx=16, pady=16)
        self._label(card, "Mở máy sau khi tạo Profile", 19,
                    color=INK, weight="bold").pack(anchor="w", padx=22, pady=(20, 8))
        self._label(card, "Tối đa máy Running trong mẻ (1–12)", 13,
                    color=INK).pack(anchor="w", padx=22)
        group_size = tk.StringVar(value=str(self.settings.start_group_size))
        ctk.CTkOptionMenu(
            card, values=[str(i) for i in range(1, MAX_PROFILES + 1)],
            variable=group_size, width=112, height=38, corner_radius=9,
            fg_color=PALE, button_color=PALE, text_color=BLUE,
            dropdown_fg_color=SURFACE, dropdown_text_color=INK,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
        ).pack(anchor="w", padx=22, pady=(10, 14))
        self._label(
            card,
            "Tạo Profile tiếp tục khi máy khác đang cài Amazon.\n"
            "Stop một máy về Offline để Profile đang đợi tự mở.",
            12, justify="left",
        ).pack(anchor="w", padx=22)
        hide_creation = tk.BooleanVar(value=self.settings.hide_profile_creation)
        ctk.CTkSwitch(
            card, text="Ẩn cửa sổ Swarmote khi tạo Profile",
            variable=hide_creation, onvalue=True, offvalue=False,
            text_color=INK, fg_color=SECONDARY,
            progress_color=BLUE, button_color=WHITE,
            font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
        ).pack(anchor="w", padx=22, pady=(14, 3))
        self._label(card, "Các điện thoại Running vẫn hiện bình thường.",
                    12, color=MUTED).pack(anchor="w", padx=22)

        def save() -> None:
            if self.running:
                messagebox.showerror("Mẻ đang chạy", "Đổi Settings sau khi mẻ kết thúc")
                return
            try:
                updated = AppSettings(int(group_size.get()), hide_creation.get())
                save_settings(updated)
            except (ToolError, OSError, ValueError) as exc:
                messagebox.showerror("Không lưu được Settings", str(exc))
                return
            self.settings = updated
            dialog.destroy()
            self.run_note.configure(
                text=f"Đã lưu: tối đa {updated.start_group_size} máy Running",
                text_color=GREEN,
            )

        ctk.CTkButton(card, text="Lưu Settings", width=136, height=38,
                      corner_radius=9, fg_color=BLUE, hover_color=BLUE_HOVER,
                      text_color=WHITE,
                      font=ctk.CTkFont("Segoe UI Variable", 13, weight="bold"),
                      command=save).pack(anchor="e", padx=22, pady=(8, 18))

    def _continue_profile(self, index: int) -> None:
        session = self.post_menu_sessions.get(index)
        if session is not None:
            if session.state == "PAUSED":
                self._start_post_menu(index)
            return
        self._launch([index])

    def _request_stop(self) -> None:
        self.cancel.set()
        for event in self.post_menu_stops.values():
            event.set()

    def _account_for_profile(self, index: int) -> AccountData:
        row = self.values[index]
        label = f"Máy q{index + 1}"
        phone = row["phone"].get().strip()
        name = row["full_name"].get().strip()
        password = row["amazon_password"].get()
        if not PHONE.fullmatch(phone):
            raise ToolError(f"{label}: SĐT chưa hợp lệ")
        if not name or len(name) > 100:
            raise ToolError(f"{label}: tên Amazon chưa hợp lệ")
        if len(password) < 8 or any(ord(c) < 33 or ord(c) > 126 for c in password):
            raise ToolError(f"{label}: mật khẩu cần ít nhất 8 ký tự ASCII không dấu cách")
        url = validate_otp_url(row["otp_url"].get())
        card = validate_card(row["card"].get()) if row["card"].get() else ""
        return AccountData(phone, name, password, url, card)

    def _attach_from_menu(self) -> None:
        index = self.selected
        if (self.running or self.attach_in_progress or
                index not in self.post_menu_step_factories or index in self.jobs):
            return
        try:
            account = self._account_for_profile(index)
        except ToolError as exc:
            messagebox.showerror(f"Dữ liệu q{index + 1}", str(exc))
            return
        self.attach_in_progress = True
        self.attaching_index = index
        self._set_editing(False)
        self.attach_profile_button.configure(state="disabled")
        self._refresh_devices()
        self.run_note.configure(text=f"Đang kiểm tra q{index + 1} và menu ba gạch...", text_color=BLUE)
        threading.Thread(target=self._probe_existing_profile,
                         args=(index, account), daemon=True).start()

    def _probe_existing_profile(self, index: int, account: AccountData) -> None:
        import pythoncom

        name = f"q{index + 1}"
        pythoncom.CoInitialize()
        try:
            profile = profile_status(name)
            if profile["state"] != "Running" or not profile.get("device_id"):
                raise ToolError(f"{name} đang Offline; Start {name} và mở menu ba gạch trước khi thử")
            shell = open_adb_shell(name, profile["device_id"])
            phone = CloudPhone(shell["serial"])
            verify_menu_open(phone, name)
            self.attach_events.put(("ready", account, phone.serial))
        except Exception as exc:
            reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
            self.attach_events.put(("error", None, reason))
        finally:
            pythoncom.CoUninitialize()

    def _start_post_menu(self, index: int) -> None:
        """Use only the steps supplied after the menu UI has been documented."""
        factory = self.post_menu_step_factories.get(index)
        if factory is None:
            return
        if self.cancel.is_set() and index not in self.post_menu_sessions:
            self.events.put((index, f"q{index + 1} đã tới menu; mẻ đang dừng",
                             "stopped", f"q{index + 1}"))
            return
        job = self.jobs.get(index)
        serial = self.phone_serials.get(index)
        if job is None or job.account is None:
            self.events.put((index,
                             f"q{index + 1} đã tới menu nhưng chưa có hàng Amazon trong mẻ",
                             "menu_only", f"q{index + 1}"))
            return
        if serial is None:
            self.events.put((index,
                             f"q{index + 1} đã tới menu nhưng chưa nối ADB; bấm Tiếp tục để nối lại",
                             "post_paused", f"q{index + 1}"))
            return
        steps = self.post_menu_steps.get(index)
        if steps is None:
            steps = factory(
                CloudPhone(serial),
                lambda code, batch_id=job.batch_id, slot=index:
                    self.otp_events.put((batch_id, slot, code)),
                lambda status, batch_id=job.batch_id, slot=index:
                    self.otp_status_events.put((batch_id, slot, status)),
            )
            self.post_menu_steps[index] = steps
        session = self.post_menu_sessions.setdefault(
            index, PostMenuSession(job.batch_id, index,
                                   self.values[index]["profile_name"].get(),
                                   self.menu_opened_at.get(index)))
        if session.state not in {"READY", "PAUSED"}:
            return
        worker = self.post_menu_workers.get(index)
        if worker is not None and worker.is_alive():
            return
        stop = threading.Event()
        self.post_menu_stops[index] = stop
        worker = threading.Thread(target=self._run_post_menu,
                                  args=(session, job, steps, stop), daemon=True)
        self.post_menu_workers[index] = worker
        worker.start()

    def _run_post_menu(self, session: PostMenuSession, job: RunJob,
                       steps: tuple[PostMenuStep, ...],
                       stop: threading.Event) -> None:
        import pythoncom

        pythoncom.CoInitialize()
        try:
            def reconcile(current, active_job, deadline, active_stop):
                phone = CloudPhone(self.phone_serials[job.index])
                target = resume_common_index(phone, steps, current,
                                             deadline, active_stop)
                if target == current:
                    return None
                factory = self.post_menu_step_factories[job.index]
                replacement = factory(
                    phone,
                    lambda code, batch_id=active_job.batch_id, slot=job.index:
                        self.otp_events.put((batch_id, slot, code)),
                    lambda status, batch_id=active_job.batch_id, slot=job.index:
                        self.otp_status_events.put((batch_id, slot, status)),
                )
                self.post_menu_steps[job.index] = replacement
                return target, replacement

            session.run(job, steps,
                        lambda index, message, state, name:
                            self.events.put((index, message, state, name)),
                        stop, reconcile=reconcile)
        finally:
            pythoncom.CoUninitialize()

    def _start(self) -> None:
        self._launch(list(range(int(self.count.get()))))

    def _resume_restored(self) -> None:
        if self.restored_batch:
            slots = _automatic_resume_slots(self.restored_batch[1])
            if slots:
                self._launch(slots)

    def _launch(self, indices: list[int]) -> None:
        if self.running or self.attach_in_progress:
            return
        if self.registry is None:
            messagebox.showerror("Danh sách Profile", self.registry_error)
            return
        try:
            if not self.jobs:
                issue = self._input_issue()
                if issue:
                    raise ToolError(issue)
                for index in range(int(self.count.get())):
                    values = {key: item.get() for key, item in self.values[index].items()}
                    proxy = ProxyConfig("socks5", values["host"].strip(),
                                        int(values["port"]), values["username"],
                                        values["proxy_password"])
                    fallbacks = tuple(self.proxy_fallbacks) if index == 0 else ()
                    account = (AccountData(
                        values["phone"].strip(), values["full_name"].strip(),
                        values["amazon_password"], values["otp_url"].strip(),
                        values["card"].strip(),
                    ) if values["phone"] else None)
                    self.jobs[index] = RunJob(index, self.draft.batch_id, proxy,
                                              fallbacks, account)
                self.draft.locked = True
                self._set_editing(False)
            if any(index not in self.jobs for index in indices):
                raise ToolError("Máy này chưa được nối vào mẻ đang thử q1")
            jobs = [self.jobs[index] for index in indices]
        except (ToolError, ValueError) as exc:
            messagebox.showerror("Dữ liệu chưa hợp lệ", str(exc))
            return
        self.running = True
        self.run_group_size = self.settings.start_group_size
        self.run_hide_profile_creation = self.settings.hide_profile_creation
        self.cancel.clear()
        self.run_button.configure(state="disabled")
        self.settings_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.reset_button.configure(state="disabled")
        self._refresh_devices()
        self.run_note.configure(text="Đang tạo Profile và mở máy song song...", text_color=BLUE)
        threading.Thread(target=self._run, args=(jobs,), daemon=True).start()

    def _run(self, jobs: list[RunJob]) -> None:
        initialized = False
        message = "Mẻ đã kết thúc"
        final_state = "finished"
        try:
            import pythoncom
            pythoncom.CoInitialize()
            initialized = True
            def emit(index: int, update: str, state: str, name: str | None) -> None:
                if state == "done":
                    self.menu_opened_at.setdefault(index, time.monotonic())
                self.events.put((index, update, state, name))

            summary = run_batch(
                jobs, self.registry,
                emit,
                self.cancel,
                start_group_size=self.run_group_size,
                hide_profile_creation=self.run_hide_profile_creation,
                menu_ready=lambda index, _name, _device_id, serial:
                    self.phone_serials.__setitem__(index, serial),
            )
            message = (f"Mẻ kết thúc: {summary['menu_open']} tới menu · "
                       f"{summary['error']} lỗi · {summary['stopped']} dừng"
                       " · bấm trạng thái để xem lỗi" if summary["error"] else
                       f"Mẻ kết thúc: {summary['menu_open']} tới menu · 0 lỗi · "
                       f"{summary['stopped']} dừng")
            final_state = "error" if summary["error"] else "finished"
        except Exception as exc:
            message = f"Mẻ dừng do lỗi: {exc}"
            final_state = "error"
        finally:
            if initialized:
                pythoncom.CoUninitialize()
            self.events.put((-1, message, final_state, None))

    def _poll(self) -> None:
        try:
            while True:
                state, account, detail = self.attach_events.get_nowait()
                self.attach_in_progress = False
                index = self.attaching_index
                if state == "ready" and account is not None and detail is not None:
                    self.cancel.clear()
                    self.jobs[index] = RunJob(index, self.draft.batch_id, None,
                                          account=account)
                    self.draft.locked = True
                    self._set_editing(False)
                    self.phone_serials[index] = detail
                    self.menu_opened_at[index] = time.monotonic()
                    self.status[index] = (f"q{index + 1} đã ở menu ba gạch", "done")
                    self._refresh_devices()
                    self._start_post_menu(index)
                else:
                    if not self.draft.locked:
                        self._set_editing(True)
                    self.run_note.configure(text=detail or f"Không gắn được q{index + 1}",
                                            text_color=RED)
                    self._refresh_devices()
        except queue.Empty:
            pass
        try:
            while True:
                index, message, state, name = self.events.get_nowait()
                if index == -1:
                    self.running = False
                    self.run_button.configure(state="normal")
                    self.settings_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    self.reset_button.configure(state="normal")
                    self._refresh_devices()
                    self.run_note.configure(
                        text=message,
                        text_color=RED if state == "error" else MUTED,
                    )
                else:
                    if name:
                        self.values[index]["profile_name"].set(name)
                    self.status[index] = (message, state)
                    if self.selected == index:
                        self.detail_status.configure(text=message)
                    self._refresh_devices()
                    if state == "done":
                        self._start_post_menu(index)
        except queue.Empty:
            pass
        try:
            while True:
                batch_id, index, code = self.otp_events.get_nowait()
                self.show_otp(batch_id, index, code)
        except queue.Empty:
            pass
        try:
            while True:
                batch_id, index, status = self.otp_status_events.get_nowait()
                self.show_otp_status(batch_id, index, status)
        except queue.Empty:
            pass
        self.root.after(150, self._poll)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    Window().run()


if __name__ == "__main__":
    main()

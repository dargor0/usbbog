#!/usr/bin/env python3

import socket
import threading
import queue
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class Messenger:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP Messenger")
        self.root.geometry("700x500")

        self.sock = None
        self.running = False
        self.incoming = queue.Queue()

        # Network controls
        network_frame = tk.LabelFrame(root, text="Network")
        network_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(network_frame, text="UDP port:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.port_entry = tk.Entry(network_frame, width=8)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.start_button = tk.Button(
            network_frame,
            text="Start listening",
            command=self.start_listening
        )
        self.start_button.grid(row=0, column=2, padx=5, pady=5)

        self.stop_button = tk.Button(
            network_frame,
            text="Stop listening",
            command=self.stop_listening,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)

        self.status_label = tk.Label(
            network_frame,
            text="Not listening",
            anchor="w"
        )
        self.status_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # Incoming and outgoing messages
        self.output = tk.Text(root, height=18, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Sending controls
        send_frame = tk.LabelFrame(root, text="Send message")
        send_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(send_frame, text="Destination IP:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.ip_entry = tk.Entry(send_frame, width=20)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(send_frame, text="Message:").grid(
            row=1, column=0, padx=5, pady=5, sticky="nw"
        )

        self.message_entry = tk.Text(send_frame, height=4, wrap="word")
        self.message_entry.grid(
            row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew"
        )

        self.send_button = tk.Button(
            send_frame,
            text="Send message",
            command=self.send_message,
            width=15
        )
        self.send_button.grid(row=1, column=3, padx=10, pady=5)

        send_frame.columnconfigure(1, weight=1)
        send_frame.columnconfigure(2, weight=1)

        self.root.after(100, self.check_incoming)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def get_port(self):
        try:
            port = int(self.port_entry.get())
            if not 1 <= port <= 65535:
                raise ValueError
            return port
        except ValueError:
            messagebox.showerror(
                "Invalid port",
                "Enter a port between 1 and 65535."
            )
            return None

    def start_listening(self):
        if self.running:
            return

        port = self.get_port()
        if port is None:
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", port))
            self.running = True

            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(
                text=f"Listening on UDP port {port}"
            )

            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()

        except OSError as error:
            if self.sock:
                self.sock.close()
                self.sock = None

            messagebox.showerror("Could not listen", str(error))

    def receive_messages(self):
        while self.running:
            try:
                data, address = self.sock.recvfrom(65535)
                message = data.decode("utf-8", errors="replace")
                self.incoming.put((address[0], address[1], message))
            except OSError:
                break

    def check_incoming(self):
        while True:
            try:
                ip, port, message = self.incoming.get_nowait()
            except queue.Empty:
                break

            timestamp = datetime.now().strftime("%H:%M:%S")
            self.add_output(
                f"[{timestamp}] Received from {ip}:{port}\n"
                f"{message}\n\n"
            )

        self.root.after(100, self.check_incoming)

    def send_message(self):
        ip = self.ip_entry.get().strip()
        message = self.message_entry.get("1.0", "end").strip()
        port = self.get_port()

        if port is None:
            return

        if not ip:
            messagebox.showerror("Missing IP", "Enter a destination IP address.")
            return

        if not message:
            messagebox.showerror("Missing message", "Enter a message.")
            return

        try:
            # Resolve/validate the destination address.
            socket.gethostbyname(ip)

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as send_socket:
                send_socket.sendto(
                    message.encode("utf-8"),
                    (ip, port)
                )

            timestamp = datetime.now().strftime("%H:%M:%S")
            self.add_output(
                f"[{timestamp}] Sent to {ip}:{port}\n"
                f"{message}\n\n"
            )

            self.message_entry.delete("1.0", "end")

        except OSError as error:
            messagebox.showerror("Send failed", str(error))

    def add_output(self, text):
        self.output.config(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.config(state="disabled")

    def stop_listening(self):
        self.running = False

        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Not listening")

    def close(self):
        self.stop_listening()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Messenger(root)
    root.mainloop()

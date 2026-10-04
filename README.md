# 🚀 PyRedis — Lightweight In-Memory Key-Value Store

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python&logoColor=white)
![Networking](https://img.shields.io/badge/Networking-TCP_Sockets-orange.svg?style=flat-square)
![Concurrency](https://img.shields.io/badge/Concurrency-Multithreaded-green.svg?style=flat-square)
![Data Structures](https://img.shields.io/badge/Cache-O(1)_LRU-purple.svg?style=flat-square)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero_External-red.svg?style=flat-square)

PyRedis is an in-memory key-value database built from scratch in Python using raw TCP sockets, multithreading, $O(1)$ LRU cache eviction, hybrid TTL key expiration, thread safety, and snapshot persistence. It provides a lightweight, zero-dependency alternative to Redis for understanding low-level networking, database engine design, and concurrency controls.

---

## 📁 Repository Architecture

```text
pyredis/
├── client.py          # Python TCP client demo with padded message framing
├── server.py          # Multithreaded TCP server, LRUCache engine, TTL sweeper & handlers
├── data.json          # Auto-generated JSON snapshot persistence store
├── notes.md           # Engineering notes on TCP sockets, LRU logic & concurrency
└── README.md          # Project documentation
```

---

## ✨ Key Technical Features

* **📡 Fixed-Header Message Framing**: Implements a 64-byte fixed-length header prefix over raw TCP streams (`socket.SOCK_STREAM`) to encode payload byte counts, ensuring safe message framing and preventing TCP stream fragmentation.
* **⚡ $O(1)$ LRU Eviction Policy**: Custom `LRUCache` pairing a Hash Map for constant-time key lookups with a Doubly-Linked List (DLL) and sentinel `head`/`tail` nodes for $O(1)$ access re-ordering and cache capacity purging.
* **⏱ Hybrid TTL Expiration**: Features passive on-access eviction (`GET`/`TTL`) combined with an active background sweeper daemon thread (`threading.Thread`) that checks and purges expired keys every second out-of-band.
* **🔒 Thread Safety & Concurrency**: Spawns dedicated worker threads per client connection (`handle_client`) guarded by a global mutual exclusion lock (`threading.Lock()`) to eliminate race conditions during concurrent state mutations.
* **💾 Snapshot Persistence & Recovery**: Automatically serializes cache state to `data.json` upon state modifications (`SET`, `DEL`, `INCR`) and auto-loads valid non-expired entries during server startup.

---

## 🛠 Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Language** | Python 3.8+ (Zero external dependencies) |
| **Networking** | Raw TCP Sockets (`socket.SOCK_STREAM`, AF_INET) |
| **Concurrency** | Multithreading (`threading.Thread`, `threading.Lock`) |
| **Data Structures** | Hash Map (`dict`) + Doubly Linked List (`Node`) |
| **Persistence** | Synchronous Snapshot Storage (`json`) |

---

## 🚀 Quick Start & Local Setup

### 1. Start the PyRedis Server
Run the multithreaded server in your main terminal window:

```bash
python server.py
```

*Output:*
```text
Server is starting...
Server is listening to 127.0.0.1
```

### 2. Run the Client Demonstration
In a second terminal window, run the client script to execute commands against the server:

```bash
python client.py
```

---

## ⚡ Supported Commands

| Command | Syntax | Description | Returns |
| :--- | :--- | :--- | :--- |
| **`PING`** | `PING` | Health check to test server connection. | `PONG` |
| **`SET`** | `SET <key> <value> [EX <seconds>]` | Sets key-value pair with optional TTL expiry. | `OK` |
| **`GET`** | `GET <key>` | Retrieves the value of a key and promotes key to MRU. | `<value>` or `nil` |
| **`DEL`** | `DEL <key>` | Removes the specified key from cache. | `1` (deleted) / `0` (not found) |
| **`INCR`** | `INCR <key>` | Increments the integer value of a key by 1. | Incremented `value` |
| **`TTL`** | `TTL <key>` | Returns remaining time-to-live in seconds. | Seconds, `-1` (no EX), or `nil` |
| **`DISCONNECTED`** | `DISCONNECTED` | Gracefully closes the client TCP connection. | `DISCONNECTED` |
```

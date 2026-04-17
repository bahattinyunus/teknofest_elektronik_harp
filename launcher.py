import sys
import os
import argparse
import threading

def start_gui():
    import webview
    from src.dashboard.app import app
    print("[Aegis-AI] Başlatılıyor: Masaüstü Arayüzü...")
    
    def start_server():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    window = webview.create_window(
        title='Aegis-AI | Taktik Elektronik Harp Kontrol Paneli',
        url='http://127.0.0.1:5000',
        width=1280,
        height=800,
        resizable=True,
        background_color='#050a14'
    )
    webview.start()

def start_cli_dashboard():
    from src.dashboard.cli_dashboard import AegisDashboard
    dash = AegisDashboard()
    try:
        dash.run()
    except KeyboardInterrupt:
        print("\n[Aegis-AI] Dashboard sonlandırıldı.")

def start_simulation():
    from main import run_autonomous_loop
    run_autonomous_loop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Aegis-AI OMEGA Launcher")
    parser.add_argument("--mode", type=str, choices=["gui", "dashboard", "simulation"], default="dashboard",
                        help="Başlatma modu: gui, dashboard veya simulation")
    
    args = parser.parse_args()
    
    if args.mode == "gui":
        start_gui()
    elif args.mode == "simulation":
        start_simulation()
    else:
        start_cli_dashboard()

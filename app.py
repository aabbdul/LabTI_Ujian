
import flask
from flask import Flask, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# Database simulasi status paket
paket_db = {
    "KC12345678": {"status": "Dalam Perjalanan", "estimasi_tiba": "2024-12-25 14:00"},
    "KC87654321": {"status": "Telah Diterima", "penerima": "Budi Santoso"},
    "KC22334455": {"status": "Sedang Dikemas", "gudang": "Jakarta"},
    "KC99887766": {"status": "Dalam Perjalanan", "posisi_terakhir": "Gudang Transit Surabaya"},
}
db_lock = threading.Lock()

def log_server_activity(message):
    """Fungsi sederhana untuk logging di sisi server (ke konsol)."""
    print(f"[SERVER-KIRIMCEPAT] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

@app.route('/paket/<nomor_resi>/status', methods=['GET'])
def get_status_paket(nomor_resi):
    """Endpoint untuk mendapatkan status paket berdasarkan nomor resi."""
    log_server_activity(f"Permintaan status untuk resi: {nomor_resi}")
    
    # Simulasi delay jaringan atau pemrosesan di server
    time.sleep(random.uniform(0.2, 0.6)) 
    
    with db_lock:
        paket = paket_db.get(nomor_resi)
    
    if paket:
        response_data = paket.copy()
        response_data["nomor_resi"] = nomor_resi
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "Nomor resi tidak ditemukan"}), 404

if __name__ == '__main__':
    log_server_activity("API Pelacakan Paket KirimCepat Express dimulai.")
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False, use_reloader=False)
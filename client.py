import requests
import threading
import time

# --- Konfigurasi Klien ---
BASE_API_URL = "http://127.0.0.1:5000"

# Data untuk diuji oleh klien: Daftar nomor resi yang akan dilacak
RESI_UNTUK_DILACAK = ["KC12345678", "KC22334455", "KC99999999", "KC87654321"] # Satu resi (KC999...) tidak ada

# ==============================================================================
# SOAL: Implementasi Fungsi untuk Melacak Paket via API
# ==============================================================================
def client_lacak_paket_via_api(nomor_resi, thread_name):
    """
    TUGAS ANDA:
    Lengkapi fungsi ini untuk mengambil informasi status paket dari API
    dan mencetak hasilnya ke konsol.

    Langkah-langkah:
    1. Bentuk URL target untuk mendapatkan status: f"{BASE_API_URL}/paket/{nomor_resi}/status"
    2. Cetak pesan ke konsol bahwa thread ini ('thread_name') memulai pelacakan untuk 'nomor_resi'.
       Contoh: print(f"[{thread_name}] Melacak paket: {nomor_resi}")
    3. Gunakan blok 'try-except' untuk menangani potensi error saat melakukan permintaan HTTP.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke URL target menggunakan 'requests.get()'. Sertakan timeout (misalnya, 5 detik).
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses):
                  - Dapatkan data JSON dari 'response.json()'.
                  - Cetak status dan detail paket ke konsol.
                    Contoh: print(f"[{thread_name}] Status {nomor_resi}: {data.get('status')}, Estimasi: {data.get('estimasi_tiba', 'N/A')}")
              - Jika 404 (resi tidak ditemukan):
                  - Cetak pesan bahwa resi tidak ditemukan ke konsol.
                    Contoh: print(f"[{thread_name}] Paket {nomor_resi} tidak ditemukan.")
              - Untuk status code lain:
                  - Cetak pesan error umum ke konsol, sertakan status code.
                    Contoh: print(f"[{thread_name}] Error API untuk {nomor_resi}: Status {response.status_code}")
       b. Di blok 'except requests.exceptions.Timeout':
          - Cetak pesan bahwa permintaan timeout ke konsol.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Cetak pesan error permintaan umum ke konsol, sertakan pesan error 'e'.
    4. Setelah blok try-except, cetak pesan ke konsol bahwa thread ini ('thread_name') selesai memproses 'nomor_resi'.
    """
    target_url = f"{BASE_API_URL}/paket/{nomor_resi}/status"
    # ===== TULIS KODE ANDA DI SINI =====
    print(f"[{thread_name}] Meminta lacak paket untuk resi: {nomor_resi}")

    try:
        response = requests.get(target_url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"[{thread_name}] lacak {nomor_resi} : ({data.get('nomor_resi')})")
        elif response.status_code == 404:
            print(f"[{thread_name}] Nomor resi {nomor_resi} tidak ditemukan.")
        else:
            print(f"[{thread_name}] Error API untuk {nomor_resi}: Status {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"[{thread_name}] Permintaan ke {nomor_resi} timeout.")

    except requests.exceptions.RequestException as e:
        print(f"[{thread_name}] Error saat menghubungi API untuk {nomor_resi}: {e}")
    
    
    print(f"[{thread_name}] Selesai memproses nomor resi : {nomor_resi}")
    #
    #
    # ====================================

# --- Bagian Utama Skrip (Tidak Perlu Diubah Peserta) ---
if __name__ == "__main__":
    print(f"Memulai Klien Pelacak Paket untuk {len(RESI_UNTUK_DILACAK)} Resi Secara Concurrent.")
    
    threads = []
    start_time = time.time()

    for i, resi_lacak in enumerate(RESI_UNTUK_DILACAK):
        thread_name_for_task = f"Pelanggan-{i+1}" 
        thread = threading.Thread(target=client_lacak_paket_via_api, args=(resi_lacak, thread_name_for_task))
        threads.append(thread)
        thread.start()

    for thread_instance in threads:
        thread_instance.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nSemua pelacakan paket telah selesai diproses dalam {total_time:.2f} detik.")
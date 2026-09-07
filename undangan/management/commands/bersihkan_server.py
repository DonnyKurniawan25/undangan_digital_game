from django.core.management.base import BaseCommand
from django.utils import timezone
from undangan.models import Undangan


class Command(BaseCommand):
    help = "Membersihkan data dan seluruh file foto dari undangan yang telah kedaluwarsa lebih dari 1 bulan dan tidak diperpanjang."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulasi pembersihan tanpa menghapus berkas dan data nyata.",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        semua_undangan = Undangan.objects.all()

        siap_dibersihkan = [u for u in semua_undangan if u.is_siap_dibersihkan]
        total_undangan = len(siap_dibersihkan)

        if total_undangan == 0:
            self.stdout.write(self.style.SUCCESS("Tidak ada undangan yang kedaluwarsa > 1 bulan. Server dalam kondisi bersih!"))
            return

        self.stdout.write(f"Ditemukan {total_undangan} proyek undangan yang kedaluwarsa lebih dari 1 bulan.")

        total_berkas = 0
        for und in siap_dibersihkan:
            judul = und.judul
            slug = und.slug
            if dry_run:
                self.stdout.write(f" [DRY-RUN] Siap dibersihkan: {judul} ({slug})")
            else:
                _, _, jml_berkas = und.bersihkan_total()
                total_berkas += jml_berkas
                self.stdout.write(self.style.WARNING(f" [TERHAPUS] {judul} ({slug}) - {jml_berkas} berkas media dihapus dari server."))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"Simulasi selesai. Total {total_undangan} undangan siap dibersihkan."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Pembersihan server selesai! Berhasil menghapus {total_undangan} undangan dan {total_berkas} berkas media dari harddisk server."))

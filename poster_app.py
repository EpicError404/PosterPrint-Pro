import sys
import os
import math
from PIL import Image, ImageDraw, ImageFont

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QFileDialog, QDoubleSpinBox, 
    QSpinBox, QFormLayout, QMessageBox, QGraphicsView, 
    QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem,
    QGraphicsLineItem, QGraphicsSimpleTextItem, QComboBox, 
    QCheckBox, QProgressBar, QFrame, QSplitter, QToolButton, 
    QScrollArea, QGroupBox
)
from PyQt6.QtGui import (
    QPixmap, QImage, QPainter, QColor, QPen, QBrush, QFont, 
    QPageLayout, QPageSize, QIcon, QAction
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QPointF
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

# Standart Kağıt Ölçüleri (mm cinsinden: Genişlik, Yükseklik)
PAPER_SIZES = {
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
    "A5": (148.0, 210.0),
    "Letter": (215.9, 279.4),
    "Legal": (215.9, 355.6),
    "Custom": (210.0, 297.0)
}

TRANSLATIONS = {
    "tr": {
        "app_title": "PosterPrint Pro - Çok Sayfalı Poster Bölücü & Doğrudan Yazdırıcı",
        "app_subtitle": "Büyük Poster Baskı ve Dilimleme",
        "lang_btn": "🌐 Dil / Language: Türkçe",
        "grp_image": "🖼️ Görsel & Kalite",
        "btn_load": "📁 Görsel Seç / Değiştir",
        "no_image": "Henüz bir görsel seçilmedi.",
        "grp_target": "📏 Hedef Poster Boyutları",
        "lbl_target_width": "Hedef Genişlik:",
        "lbl_target_height": "Hedef Yükseklik:",
        "cb_aspect_lock": "🔒 En-Boy Oranını Koru",
        "grp_paper": "📄 Kağıt Seçenekleri",
        "lbl_paper_size": "Kağıt Boyutu:",
        "lbl_orientation": "Kağıt Yönü:",
        "orientation_portrait": "Dikey (Portrait)",
        "orientation_landscape": "Yatay (Landscape)",
        "lbl_custom_w": "Özel Genişlik:",
        "lbl_custom_h": "Özel Yükseklik:",
        "paper_custom": "Özel (Custom)",
        "grp_margins": "📐 Montaj & Kenar Payları",
        "lbl_margin": "Yazıcı Kenarlık Payı:",
        "lbl_overlap": "Örtüşme (Bant) Payı:",
        "cb_crop_marks": "✂ Kesim & Hizalama İmleri",
        "tip_margin": "Yazıcıların kenarda basamadığı boşluk payı (Tipik: 3-5 mm).",
        "tip_overlap": "Sayfaları birbirine bantlamak/yapıştırmak için bırakılan örtüşme payı.",
        "tip_crop_marks": "Köşe kesim işaretleri, yapıştırma çizgileri ve sayfa numarası ekler.",
        "grp_dpi": "⚙️ Çıkış Çözünürlüğü",
        "lbl_dpi": "Baskı DPI:",
        "dpi_150": "150 DPI (Hızlı / Düşük Dosya Boyutu)",
        "dpi_300": "300 DPI (Önerilen Baskı Kalitesi)",
        "dpi_600": "600 DPI (Ultra Yüksek Çözünürlük)",
        "page_summary_waiting": "Sayfa Dağılımı: Bekleniyor...",
        "page_summary_format": "<b>Sayfa Dağılımı:</b> {cols} Sütun x {rows} Satır<br><b>Toplam Sayfa:</b> {total_pages} Adet ({paper_name})<br><b>Sayfa Başına Etkin Alan:</b> {eff_w:.1f} x {eff_h:.1f} cm",
        "btn_save_pdf": "💾 Tek PDF Olarak Kaydet",
        "btn_direct_print": "🖨️ Doğrudan Yazdır",
        "lbl_status_ready": "Hazır",
        "lbl_status_starting": "Başlatılıyor...",
        "lbl_status_printing_prep": "Yazdırma için hazırlanıyor...",
        "lbl_status_sending_printer": "Yazıcıya gönderiliyor...",
        "lbl_status_print_done": "Yazdırma Tamamlandı!",
        "lbl_status_pdf_done": "PDF Başarıyla Kaydedildi!",
        "lbl_status_cancelling": "İptal ediliyor...",
        "lbl_status_error_cancel": "Hata veya İptal.",
        "btn_cancel": "İptal Et",
        "canvas_title": "🎨 İnteraktif Poster Tuvali",
        "tip_bar": "💡 İpucu: Fare tekerleğiyle yakınlaştırabilir, tıklayıp sürükleyerek tuvalde gezinebilirsiniz. Dosyayı doğrudan pencereye bırakabilirsiniz.",
        "empty_canvas": "📂 Başlamak için sol menüden bir resim seçin veya buraya sürükleyin.",
        "zoom_in_tip": "Yakınlaş (Mouse Tekerleği Yukarı)",
        "zoom_out_tip": "Uzaklaş (Mouse Tekerleği Aşağı)",
        "zoom_100_tip": "Gerçek Boyut (%100)",
        "zoom_fit_tip": "Posteri Ekrana Sığdır",
        "zoom_fit_btn": "🔲 Sığdır",
        "select_image_title": "Resim Seç",
        "image_filter": "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.webp)",
        "error_open_img": "Görsel açılırken hata oluştu:\n",
        "err_title": "Hata",
        "warn_title": "Uyarı",
        "warn_select_img": "Lütfen önce bir görsel seçin!",
        "save_pdf_title": "PDF Kaydet",
        "save_pdf_filter": "PDF Dosyaları (*.pdf)",
        "print_dialog_title": "Posteri Yazdır",
        "print_err_title": "Yazıcı Hatası",
        "print_err_init": "Yazıcı başlatılırken hata oluştu:\n",
        "print_err_pages": "Sayfalar yazdırılırken hata oluştu:\n",
        "print_success_title": "Yazdırma Başarılı",
        "print_success_msg": "{total} sayfa yazıcıya başarıyla aktarıldı!",
        "pdf_success_title": "Başarılı",
        "pdf_success_msg": "Poster PDF dosyası başarıyla oluşturuldu!\n\nDosya Konumu:\n{path}",
        "info_title": "Bilgi",
        "badge_excellent_title": "🟢 Mükemmel Kalite (~{dpi} DPI)",
        "badge_excellent_desc": "Baskı son derece keskin ve net görünecektir.",
        "badge_standard_title": "🔵 Standart Baskı Kalitesi (~{dpi} DPI)",
        "badge_standard_desc": "Poster ve duvar baskıları için ideal netlikte.",
        "badge_medium_title": "🟠 Orta Kalite (~{dpi} DPI)",
        "badge_medium_desc": "Uzaktan iyi durur, ancak yakından hafif pürüzlü görünebilir.",
        "badge_low_title": "🔴 Düşük Çözünürlük Uyarısı (~{dpi} DPI)",
        "badge_low_desc": "Görsel bu boyutta pikselleşebilir veya bulanık çıkabilir!",
        "worker_calc": "Hedef boyutlar hesaplanıyor...",
        "worker_resize": "Görsel yüksek çözünürlükte boyutlandırılıyor ({dpi} DPI)...",
        "worker_cancelled": "İşlem kullanıcı tarafından iptal edildi.",
        "worker_page_prep": "Sayfa {current} / {total} hazırlanıyor...",
        "worker_pdf_saving": "PDF dosyası kaydediliyor...",
        "worker_completed": "Tamamlandı!",
        "worker_print_ready": "Sayfalar hazırlandı, yazıcıya aktarılıyor...",
        "page_label_watermark": "Sayfa {curr} / {total}  [Sütun {col}/{cols}, Satır {row}/{rows}]  •  Hedef: {w:.1f}x{h:.1f} cm  •  Örtüşme: {overlap:.0f}mm",
        "badge_preview_page": "Sayfa {num} [{col},{row}]"
    },
    "en": {
        "app_title": "PosterPrint Pro - Multi-Page Poster Splitter & Direct Printer",
        "app_subtitle": "Large Poster Printing & Tiling",
        "lang_btn": "🌐 Dil / Language: English",
        "grp_image": "🖼️ Image & Quality",
        "btn_load": "📁 Select / Change Image",
        "no_image": "No image selected yet.",
        "grp_target": "📏 Target Poster Dimensions",
        "lbl_target_width": "Target Width:",
        "lbl_target_height": "Target Height:",
        "cb_aspect_lock": "🔒 Lock Aspect Ratio",
        "grp_paper": "📄 Paper Options",
        "lbl_paper_size": "Paper Size:",
        "lbl_orientation": "Orientation:",
        "orientation_portrait": "Portrait",
        "orientation_landscape": "Landscape",
        "lbl_custom_w": "Custom Width:",
        "lbl_custom_h": "Custom Height:",
        "paper_custom": "Custom",
        "grp_margins": "📐 Assembly & Margins",
        "lbl_margin": "Printer Margin:",
        "lbl_overlap": "Overlap (Tape) Margin:",
        "cb_crop_marks": "✂ Cut & Alignment Marks",
        "tip_margin": "Unprintable margin of printers (Typically: 3-5 mm).",
        "tip_overlap": "Overlap margin used for taping/gluing pages together.",
        "tip_crop_marks": "Adds corner cut marks, alignment lines, and page numbers.",
        "grp_dpi": "⚙️ Output Resolution",
        "lbl_dpi": "Print DPI:",
        "dpi_150": "150 DPI (Fast / Lower File Size)",
        "dpi_300": "300 DPI (Recommended Print Quality)",
        "dpi_600": "600 DPI (Ultra High Resolution)",
        "page_summary_waiting": "Page Distribution: Waiting...",
        "page_summary_format": "<b>Page Layout:</b> {cols} Columns x {rows} Rows<br><b>Total Pages:</b> {total_pages} Sheets ({paper_name})<br><b>Effective Printable Area:</b> {eff_w:.1f} x {eff_h:.1f} cm",
        "btn_save_pdf": "💾 Save as Single PDF",
        "btn_direct_print": "🖨️ Print Directly",
        "lbl_status_ready": "Ready",
        "lbl_status_starting": "Starting...",
        "lbl_status_printing_prep": "Preparing for printing...",
        "lbl_status_sending_printer": "Sending to printer...",
        "lbl_status_print_done": "Printing Completed!",
        "lbl_status_pdf_done": "PDF Saved Successfully!",
        "lbl_status_cancelling": "Cancelling...",
        "lbl_status_error_cancel": "Error or Cancelled.",
        "btn_cancel": "Cancel",
        "canvas_title": "🎨 Interactive Poster Canvas",
        "tip_bar": "💡 Tip: Zoom in/out with the mouse wheel, click and drag to pan across canvas. You can also drop image files directly.",
        "empty_canvas": "📂 Select an image from the left panel or drag & drop here to start.",
        "zoom_in_tip": "Zoom In (Mouse Wheel Up)",
        "zoom_out_tip": "Zoom Out (Mouse Wheel Down)",
        "zoom_100_tip": "Actual Size (100%)",
        "zoom_fit_tip": "Fit Poster in View",
        "zoom_fit_btn": "🔲 Fit",
        "select_image_title": "Select Image",
        "image_filter": "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)",
        "error_open_img": "An error occurred while opening the image:\n",
        "err_title": "Error",
        "warn_title": "Warning",
        "warn_select_img": "Please select an image first!",
        "save_pdf_title": "Save PDF",
        "save_pdf_filter": "PDF Files (*.pdf)",
        "print_dialog_title": "Print Poster",
        "print_err_title": "Printer Error",
        "print_err_init": "Error initializing printer:\n",
        "print_err_pages": "Error occurred while printing pages:\n",
        "print_success_title": "Print Successful",
        "print_success_msg": "{total} page(s) successfully sent to printer!",
        "pdf_success_title": "Success",
        "pdf_success_msg": "Poster PDF created successfully!\n\nFile Location:\n{path}",
        "info_title": "Information",
        "badge_excellent_title": "🟢 Excellent Quality (~{dpi} DPI)",
        "badge_excellent_desc": "The print will look extremely crisp and sharp.",
        "badge_standard_title": "🔵 Standard Print Quality (~{dpi} DPI)",
        "badge_standard_desc": "Ideal sharpness for posters and wall displays.",
        "badge_medium_title": "🟠 Medium Quality (~{dpi} DPI)",
        "badge_medium_desc": "Looks good from a distance, but slightly coarse up close.",
        "badge_low_title": "🔴 Low Resolution Warning (~{dpi} DPI)",
        "badge_low_desc": "Image may appear pixelated or blurry at this size!",
        "worker_calc": "Calculating target dimensions...",
        "worker_resize": "Resizing image to high resolution ({dpi} DPI)...",
        "worker_cancelled": "Operation cancelled by user.",
        "worker_page_prep": "Preparing page {current} / {total}...",
        "worker_pdf_saving": "Saving PDF file...",
        "worker_completed": "Completed!",
        "worker_print_ready": "Pages prepared, transferring to printer...",
        "page_label_watermark": "Page {curr} / {total}  [Col {col}/{cols}, Row {row}/{rows}]  •  Target: {w:.1f}x{h:.1f} cm  •  Overlap: {overlap:.0f}mm",
        "badge_preview_page": "Page {num} [{col},{row}]"
    }
}




class PosterRenderWorker(QThread):
    """
    PDF oluşturma ve doğrudan yazdırma için ağır görüntü işleme ve
    dilimleme işlemlerini arka planda yürüten iş parçacığı (QThread).
    """
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str, object)  # durum mesajı, sayfa listesi (veya None)
    error = pyqtSignal(str)

    def __init__(self, mode, pil_image, target_w_cm, target_h_cm, paper_w_mm, paper_h_mm,
                 margin_mm, overlap_mm, dpi, draw_marks, lang="tr", save_path=None):
        super().__init__()
        self.mode = mode  # "pdf" veya "print"
        self.pil_image = pil_image
        self.target_w_cm = target_w_cm
        self.target_h_cm = target_h_cm
        self.paper_w_mm = paper_w_mm
        self.paper_h_mm = paper_h_mm
        self.margin_mm = margin_mm
        self.overlap_mm = overlap_mm
        self.dpi = dpi
        self.draw_marks = draw_marks
        self.lang = lang
        self.save_path = save_path
        self._is_cancelled = False

    def tr_text(self, key, **kwargs):
        text = TRANSLATIONS.get(self.lang, TRANSLATIONS["tr"]).get(key, "")
        if kwargs:
            return text.format(**kwargs)
        return text

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        try:
            self.progress.emit(5, self.tr_text("worker_calc"))
            target_w_mm = self.target_w_cm * 10
            target_h_mm = self.target_h_cm * 10

            scale = self.dpi / 25.4
            target_w_px = max(1, int(round(target_w_mm * scale)))
            target_h_px = max(1, int(round(target_h_mm * scale)))
            paper_w_px = max(1, int(round(self.paper_w_mm * scale)))
            paper_h_px = max(1, int(round(self.paper_h_mm * scale)))
            margin_x_px = int(round(self.margin_mm * scale))
            margin_y_px = int(round(self.margin_mm * scale))
            overlap_px = int(round(self.overlap_mm * scale))

            printable_w_mm = max(10.0, self.paper_w_mm - 2 * self.margin_mm)
            printable_h_mm = max(10.0, self.paper_h_mm - 2 * self.margin_mm)

            stride_w_mm = max(10.0, printable_w_mm - self.overlap_mm)
            stride_h_mm = max(10.0, printable_h_mm - self.overlap_mm)

            cols = 1 if target_w_mm <= printable_w_mm else math.ceil((target_w_mm - printable_w_mm) / stride_w_mm) + 1
            rows = 1 if target_h_mm <= printable_h_mm else math.ceil((target_h_mm - printable_h_mm) / stride_h_mm) + 1
            total_pages = cols * rows

            self.progress.emit(10, self.tr_text("worker_resize", dpi=self.dpi))
            resized_img = self.pil_image.resize((target_w_px, target_h_px), Image.Resampling.LANCZOS)

            if self._is_cancelled:
                self.error.emit(self.tr_text("worker_cancelled"))
                return

            pages = []
            font_size = max(11, int(round(self.dpi * 0.05)))
            font = ImageFont.load_default(size=font_size)

            current_page_idx = 0
            for r in range(rows):
                for c in range(cols):
                    if self._is_cancelled:
                        self.error.emit(self.tr_text("worker_cancelled"))
                        return

                    current_page_idx += 1
                    pct = 15 + int((current_page_idx / total_pages) * 75)
                    self.progress.emit(pct, self.tr_text("worker_page_prep", current=current_page_idx, total=total_pages))

                    sheet = Image.new("RGB", (paper_w_px, paper_h_px), (255, 255, 255))
                    draw_sheet = ImageDraw.Draw(sheet)

                    src_x_mm = c * stride_w_mm
                    src_y_mm = r * stride_h_mm

                    crop_x1 = int(round(src_x_mm * scale))
                    crop_y1 = int(round(src_y_mm * scale))
                    crop_x2 = min(target_w_px, int(round((src_x_mm + printable_w_mm) * scale)))
                    crop_y2 = min(target_h_px, int(round((src_y_mm + printable_h_mm) * scale)))

                    tile = resized_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
                    sheet.paste(tile, (margin_x_px, margin_y_px))

                    # Kesim, hizalama ve sayfa imleri çizimi
                    if self.draw_marks:
                        t_l = margin_x_px
                        t_t = margin_y_px
                        t_r = margin_x_px + tile.width
                        t_b = margin_y_px + tile.height
                        mark_len = max(8, int(round(4.0 * scale)))
                        m_col = (110, 110, 110)

                        # 4 Köşe Kesim İmleri
                        draw_sheet.line([(t_l - mark_len, t_t), (t_l, t_t)], fill=m_col, width=2)
                        draw_sheet.line([(t_l, t_t - mark_len), (t_l, t_t)], fill=m_col, width=2)

                        draw_sheet.line([(t_r, t_t), (t_r + mark_len, t_t)], fill=m_col, width=2)
                        draw_sheet.line([(t_r, t_t - mark_len), (t_r, t_t)], fill=m_col, width=2)

                        draw_sheet.line([(t_l - mark_len, t_b), (t_l, t_b)], fill=m_col, width=2)
                        draw_sheet.line([(t_l, t_b), (t_l, t_b + mark_len)], fill=m_col, width=2)

                        draw_sheet.line([(t_r, t_b), (t_r + mark_len, t_b)], fill=m_col, width=2)
                        draw_sheet.line([(t_r, t_b), (t_r, t_b + mark_len)], fill=m_col, width=2)

                        # Örtüşme (Yapıştırma / Hizalama) Kılavuz Çizgileri
                        if c > 0 and overlap_px > 0:
                            ol_x = t_l + overlap_px
                            dash_step = max(8, int(scale * 3))
                            for y in range(t_t, t_b, dash_step * 2):
                                draw_sheet.line([(ol_x, y), (ol_x, min(y + dash_step, t_b))], fill=(160, 160, 160), width=1)

                        if r > 0 and overlap_px > 0:
                            ol_y = t_t + overlap_px
                            dash_step = max(8, int(scale * 3))
                            for x in range(t_l, t_r, dash_step * 2):
                                draw_sheet.line([(x, ol_y), (min(x + dash_step, t_r), ol_y)], fill=(160, 160, 160), width=1)

                        # Sayfa Numarası ve Konum Bilgisi (Marj alanında)
                        label_text = self.tr_text(
                            "page_label_watermark",
                            curr=current_page_idx,
                            total=total_pages,
                            col=c + 1,
                            cols=cols,
                            row=r + 1,
                            rows=rows,
                            w=self.target_w_cm,
                            h=self.target_h_cm,
                            overlap=self.overlap_mm
                        )
                        label_y = t_b + max(4, int(scale * 1.5))
                        draw_sheet.text((t_l + 4, label_y), label_text, fill=(100, 100, 100), font=font)

                    pages.append(sheet)

            if self.mode == "pdf":
                self.progress.emit(95, self.tr_text("worker_pdf_saving"))
                pages[0].save(
                    self.save_path,
                    "PDF",
                    resolution=float(self.dpi),
                    save_all=True,
                    append_images=pages[1:]
                )
                self.progress.emit(100, self.tr_text("worker_completed"))
                self.finished.emit("PDF_SUCCESS", self.save_path)
            elif self.mode == "print":
                self.progress.emit(100, self.tr_text("worker_print_ready"))
                self.finished.emit("PRINT_READY", pages)

        except Exception as e:
            self.error.emit(str(e))


class PosterGraphicsView(QGraphicsView):
    """
    İnteraktif Tuval: Mouse tekerleğiyle yakınlaştırma/uzaklaştırma (Zoom),
    tıklayıp sürükleyerek kaydırma (Pan) ve sürükle-bırak görsel yükleme.
    """
    zoom_changed = pyqtSignal(float)
    image_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(QColor("#25282c")))
        self.current_zoom = 1.0
        self.setAcceptDrops(True)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.15
        else:
            factor = 1.0 / 1.15

        new_zoom = self.current_zoom * factor
        if 0.05 <= new_zoom <= 25.0:
            self.current_zoom = new_zoom
            self.scale(factor, factor)
            self.zoom_changed.emit(self.current_zoom)

    def zoom_in(self):
        factor = 1.2
        new_zoom = self.current_zoom * factor
        if new_zoom <= 25.0:
            self.current_zoom = new_zoom
            self.scale(factor, factor)
            self.zoom_changed.emit(self.current_zoom)

    def zoom_out(self):
        factor = 1.0 / 1.2
        new_zoom = self.current_zoom * factor
        if new_zoom >= 0.05:
            self.current_zoom = new_zoom
            self.scale(factor, factor)
            self.zoom_changed.emit(self.current_zoom)

    def zoom_reset(self):
        self.resetTransform()
        self.current_zoom = 1.0
        self.zoom_changed.emit(self.current_zoom)

    def fit_in_view(self):
        rect = self.scene.itemsBoundingRect()
        if not rect.isEmpty():
            self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
            self.current_zoom = self.transform().m11()
            self.zoom_changed.emit(self.current_zoom)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                event.acceptProposedAction()
                return
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                    self.image_dropped.emit(file_path)
                    event.acceptProposedAction()
                    return
        super().dropEvent(event)


class PosterPrinterApp(QMainWindow):
    """
    Gelişmiş Poster Bölücü, Çoklu Sayfa PDF Oluşturucu ve Doğrudan Yazdırma Uygulaması.
    """
    def __init__(self):
        super().__init__()
        self.current_lang = "tr"
        self.setGeometry(60, 60, 1280, 840)

        # Uygulama / Pencere İkonu
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.image_path = None
        self.pil_image = None
        self.image_aspect_ratio = 1.0
        self._updating_dimensions = False
        self.worker = None
        self.pending_printer = None

        self.init_ui()
        self.apply_styles()
        self.retranslate_ui()

    def t(self, key, **kwargs):
        text = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["tr"]).get(key, "")
        if kwargs:
            return text.format(**kwargs)
        return text

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "tr" else "tr"
        self.retranslate_ui()

    def set_language(self, lang):
        if lang in TRANSLATIONS and lang != self.current_lang:
            self.current_lang = lang
            self.retranslate_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- SOL KONTROL PANELİ ----------------
        control_scroll = QScrollArea()
        control_scroll.setFixedWidth(360)
        control_scroll.setWidgetResizable(True)
        control_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        control_scroll.setObjectName("controlScroll")

        control_container = QWidget()
        control_layout = QVBoxLayout(control_container)
        control_layout.setContentsMargins(15, 15, 15, 15)
        control_layout.setSpacing(12)

        # Marka & Logo Başlık Alanı
        brand_container = QFrame()
        brand_container.setObjectName("brandHeader")
        brand_layout = QHBoxLayout(brand_container)
        brand_layout.setContentsMargins(10, 10, 10, 10)
        brand_layout.setSpacing(12)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        self.lbl_logo = QLabel()
        if os.path.exists(icon_path):
            logo_pix = QPixmap(icon_path).scaled(44, 44, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.lbl_logo.setPixmap(logo_pix)
        self.lbl_logo.setFixedSize(44, 44)
        brand_layout.addWidget(self.lbl_logo)

        brand_text_layout = QVBoxLayout()
        brand_text_layout.setSpacing(2)
        self.lbl_app_name = QLabel("PosterPrint Pro")
        self.lbl_app_name.setStyleSheet("font-weight: 800; font-size: 16px; color: #0f172a;")
        self.lbl_app_subtitle = QLabel()
        self.lbl_app_subtitle.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 500;")
        brand_text_layout.addWidget(self.lbl_app_name)
        brand_text_layout.addWidget(self.lbl_app_subtitle)
        brand_layout.addLayout(brand_text_layout)

        control_layout.addWidget(brand_container)

        # 0. Dil Seçici Buton
        lang_bar = QHBoxLayout()
        lang_bar.setSpacing(6)
        self.btn_lang = QPushButton("🌐 Dil / Language: Türkçe")
        self.btn_lang.setObjectName("btnLang")
        self.btn_lang.setToolTip("Türkçe / English dilleri arasında geçiş yapın")
        self.btn_lang.clicked.connect(self.toggle_language)
        lang_bar.addWidget(self.btn_lang)
        control_layout.addLayout(lang_bar)

        # 1. Görsel & Kalite Grubu
        self.grp_image = QGroupBox()
        grp_image_layout = QVBoxLayout(self.grp_image)

        self.btn_load = QPushButton()
        self.btn_load.clicked.connect(self.select_image_dialog)
        grp_image_layout.addWidget(self.btn_load)

        self.lbl_img_info = QLabel()
        self.lbl_img_info.setStyleSheet("color: #666; font-size: 11px;")
        grp_image_layout.addWidget(self.lbl_img_info)

        self.lbl_dpi_quality = QLabel("")
        self.lbl_dpi_quality.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_dpi_quality.setWordWrap(True)
        grp_image_layout.addWidget(self.lbl_dpi_quality)
        control_layout.addWidget(self.grp_image)

        # 2. Hedef Boyutlar Grubu
        self.grp_target = QGroupBox()
        self.grp_target_layout = QFormLayout(self.grp_target)

        self.lbl_target_width = QLabel()
        self.input_width = QDoubleSpinBox()
        self.input_width.setRange(5.0, 1000.0)
        self.input_width.setValue(60.0)
        self.input_width.setSuffix(" cm")
        self.input_width.setSingleStep(1.0)
        self.input_width.valueChanged.connect(self.on_width_changed)
        self.grp_target_layout.addRow(self.lbl_target_width, self.input_width)

        self.lbl_target_height = QLabel()
        self.input_height = QDoubleSpinBox()
        self.input_height.setRange(5.0, 1000.0)
        self.input_height.setValue(80.0)
        self.input_height.setSuffix(" cm")
        self.input_height.setSingleStep(1.0)
        self.input_height.valueChanged.connect(self.on_height_changed)
        self.grp_target_layout.addRow(self.lbl_target_height, self.input_height)

        self.cb_aspect_lock = QCheckBox()
        self.cb_aspect_lock.setChecked(True)
        self.cb_aspect_lock.toggled.connect(self.on_aspect_lock_toggled)
        self.grp_target_layout.addRow("", self.cb_aspect_lock)

        control_layout.addWidget(self.grp_target)

        # 3. Kağıt Boyutu & Yönlendirme Grubu
        self.grp_paper = QGroupBox()
        self.grp_paper_layout = QFormLayout(self.grp_paper)

        self.lbl_paper_size = QLabel()
        self.combo_paper = QComboBox()
        self.populate_paper_combo()
        self.combo_paper.currentIndexChanged.connect(self.on_paper_changed)
        self.grp_paper_layout.addRow(self.lbl_paper_size, self.combo_paper)

        self.lbl_orientation = QLabel()
        self.combo_orientation = QComboBox()
        self.combo_orientation.addItem("", "portrait")
        self.combo_orientation.addItem("", "landscape")
        self.combo_orientation.currentIndexChanged.connect(self.update_preview)
        self.grp_paper_layout.addRow(self.lbl_orientation, self.combo_orientation)

        # Özel kağıt boyutu için giriş alanları
        self.input_custom_w = QDoubleSpinBox()
        self.input_custom_w.setRange(50.0, 2000.0)
        self.input_custom_w.setValue(210.0)
        self.input_custom_w.setSuffix(" mm")
        self.input_custom_w.valueChanged.connect(self.update_preview)

        self.input_custom_h = QDoubleSpinBox()
        self.input_custom_h.setRange(50.0, 2000.0)
        self.input_custom_h.setValue(297.0)
        self.input_custom_h.setSuffix(" mm")
        self.input_custom_h.valueChanged.connect(self.update_preview)

        self.lbl_custom_w = QLabel()
        self.lbl_custom_h = QLabel()
        self.grp_paper_layout.addRow(self.lbl_custom_w, self.input_custom_w)
        self.grp_paper_layout.addRow(self.lbl_custom_h, self.input_custom_h)
        self.input_custom_w.hide()
        self.input_custom_h.hide()
        self.lbl_custom_w.hide()
        self.lbl_custom_h.hide()

        control_layout.addWidget(self.grp_paper)

        # 4. Baskı & Montaj Payları Grubu
        self.grp_margins = QGroupBox()
        self.grp_margins_layout = QFormLayout(self.grp_margins)

        self.lbl_margin = QLabel()
        self.input_margin = QDoubleSpinBox()
        self.input_margin.setRange(0.0, 30.0)
        self.input_margin.setValue(5.0)
        self.input_margin.setSuffix(" mm")
        self.input_margin.valueChanged.connect(self.update_preview)
        self.grp_margins_layout.addRow(self.lbl_margin, self.input_margin)

        self.lbl_overlap = QLabel()
        self.input_overlap = QDoubleSpinBox()
        self.input_overlap.setRange(0.0, 40.0)
        self.input_overlap.setValue(10.0)
        self.input_overlap.setSuffix(" mm")
        self.input_overlap.valueChanged.connect(self.update_preview)
        self.grp_margins_layout.addRow(self.lbl_overlap, self.input_overlap)

        self.cb_crop_marks = QCheckBox()
        self.cb_crop_marks.setChecked(True)
        self.grp_margins_layout.addRow("", self.cb_crop_marks)

        control_layout.addWidget(self.grp_margins)

        # 5. Baskı Çözünürlüğü Grubu
        self.grp_dpi = QGroupBox()
        self.grp_dpi_layout = QFormLayout(self.grp_dpi)

        self.lbl_dpi = QLabel()
        self.combo_dpi = QComboBox()
        self.combo_dpi.addItem("", 150)
        self.combo_dpi.addItem("", 300)
        self.combo_dpi.addItem("", 600)
        self.combo_dpi.setCurrentIndex(1)
        self.grp_dpi_layout.addRow(self.lbl_dpi, self.combo_dpi)

        control_layout.addWidget(self.grp_dpi)

        # 6. Sayfa Özeti & Bilgi
        self.lbl_page_summary = QLabel()
        self.lbl_page_summary.setObjectName("pageSummaryLabel")
        self.lbl_page_summary.setWordWrap(True)
        control_layout.addWidget(self.lbl_page_summary)

        # 7. İşlem Butonları
        self.btn_save_pdf = QPushButton()
        self.btn_save_pdf.setObjectName("btnSavePdf")
        self.btn_save_pdf.clicked.connect(self.start_pdf_generation)
        control_layout.addWidget(self.btn_save_pdf)

        self.btn_direct_print = QPushButton()
        self.btn_direct_print.setObjectName("btnPrintDirect")
        self.btn_direct_print.clicked.connect(self.start_direct_print)
        control_layout.addWidget(self.btn_direct_print)

        # 8. İlerleme & Arka Plan Durum Çubuğu
        self.progress_frame = QFrame()
        self.progress_frame.setObjectName("progressFrame")
        progress_layout = QVBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(8, 8, 8, 8)

        self.lbl_worker_status = QLabel()
        self.lbl_worker_status.setStyleSheet("font-size: 11px; color: #444; font-weight: bold;")
        progress_layout.addWidget(self.lbl_worker_status)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)

        self.btn_cancel = QPushButton()
        self.btn_cancel.setObjectName("btnCancel")
        self.btn_cancel.clicked.connect(self.cancel_worker)
        self.btn_cancel.hide()
        progress_layout.addWidget(self.btn_cancel)

        control_layout.addWidget(self.progress_frame)
        control_layout.addStretch()

        control_scroll.setWidget(control_container)
        main_layout.addWidget(control_scroll)

        # ---------------- SAĞ ÖNİZLEME & TUVAL ALANI ----------------
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(0)

        # Tuval Üst Araç Çubuğu
        canvas_toolbar = QWidget()
        canvas_toolbar.setObjectName("canvasToolbar")
        canvas_toolbar.setFixedHeight(42)
        tb_layout = QHBoxLayout(canvas_toolbar)
        tb_layout.setContentsMargins(12, 4, 12, 4)
        tb_layout.setSpacing(8)

        self.tb_title = QLabel()
        self.tb_title.setStyleSheet("font-weight: bold; color: #e2e8f0; font-size: 13px;")
        tb_layout.addWidget(self.tb_title)

        tb_layout.addStretch()

        self.btn_zoom_in = QToolButton()
        self.btn_zoom_in.setText("🔍 +")
        self.btn_zoom_in.clicked.connect(lambda: self.graphics_view.zoom_in())
        tb_layout.addWidget(self.btn_zoom_in)

        self.btn_zoom_out = QToolButton()
        self.btn_zoom_out.setText("🔍 -")
        self.btn_zoom_out.clicked.connect(lambda: self.graphics_view.zoom_out())
        tb_layout.addWidget(self.btn_zoom_out)

        self.btn_zoom_100 = QToolButton()
        self.btn_zoom_100.setText("1:1")
        self.btn_zoom_100.clicked.connect(lambda: self.graphics_view.zoom_reset())
        tb_layout.addWidget(self.btn_zoom_100)

        self.btn_zoom_fit = QToolButton()
        self.btn_zoom_fit.clicked.connect(lambda: self.graphics_view.fit_in_view())
        tb_layout.addWidget(self.btn_zoom_fit)

        self.lbl_zoom = QLabel("%100")
        self.lbl_zoom.setStyleSheet("color: #a0aec0; min-width: 48px; text-align: center; font-size: 11px;")
        tb_layout.addWidget(self.lbl_zoom)

        preview_layout.addWidget(canvas_toolbar)

        # İnteraktif Tuval (QGraphicsView)
        self.graphics_view = PosterGraphicsView()
        self.graphics_view.zoom_changed.connect(self.on_zoom_changed)
        self.graphics_view.image_dropped.connect(self.load_image_from_path)
        preview_layout.addWidget(self.graphics_view)

        # Alt İpucu Çubuğu
        self.tip_bar = QLabel()
        self.tip_bar.setStyleSheet("background-color: #1a202c; color: #a0aec0; font-size: 11px; padding: 6px 12px; border-top: 1px solid #2d3748;")
        preview_layout.addWidget(self.tip_bar)

        main_layout.addWidget(preview_container)
        self.setCentralWidget(main_widget)

        self.show_empty_canvas()

    def populate_paper_combo(self):
        curr_key = self.combo_paper.currentData() if self.combo_paper.count() > 0 else "A4"
        self.combo_paper.blockSignals(True)
        self.combo_paper.clear()
        for key in ["A4", "A3", "A5", "Letter", "Legal", "Custom"]:
            w, h = PAPER_SIZES[key]
            if key == "Custom":
                label = self.t("paper_custom")
            else:
                label = f"{key} ({int(w)} x {int(h)} mm)"
            self.combo_paper.addItem(label, key)
        idx = self.combo_paper.findData(curr_key)
        if idx >= 0:
            self.combo_paper.setCurrentIndex(idx)
        self.combo_paper.blockSignals(False)

    def retranslate_ui(self):
        self.setWindowTitle(self.t("app_title"))
        self.lbl_app_subtitle.setText(self.t("app_subtitle"))
        self.btn_lang.setText(self.t("lang_btn"))

        # 1. Image
        self.grp_image.setTitle(self.t("grp_image"))
        self.btn_load.setText(self.t("btn_load"))
        if not self.pil_image:
            self.lbl_img_info.setText(self.t("no_image"))

        # 2. Target Dimensions
        self.grp_target.setTitle(self.t("grp_target"))
        self.lbl_target_width.setText(self.t("lbl_target_width"))
        self.lbl_target_height.setText(self.t("lbl_target_height"))
        self.cb_aspect_lock.setText(self.t("cb_aspect_lock"))

        # 3. Paper Options
        self.grp_paper.setTitle(self.t("grp_paper"))
        self.lbl_paper_size.setText(self.t("lbl_paper_size"))
        self.lbl_orientation.setText(self.t("lbl_orientation"))
        self.lbl_custom_w.setText(self.t("lbl_custom_w"))
        self.lbl_custom_h.setText(self.t("lbl_custom_h"))

        self.populate_paper_combo()

        curr_orient_idx = self.combo_orientation.currentIndex()
        self.combo_orientation.blockSignals(True)
        self.combo_orientation.setItemText(0, self.t("orientation_portrait"))
        self.combo_orientation.setItemText(1, self.t("orientation_landscape"))
        if curr_orient_idx >= 0:
            self.combo_orientation.setCurrentIndex(curr_orient_idx)
        self.combo_orientation.blockSignals(False)

        # 4. Margins
        self.grp_margins.setTitle(self.t("grp_margins"))
        self.lbl_margin.setText(self.t("lbl_margin"))
        self.lbl_overlap.setText(self.t("lbl_overlap"))
        self.input_margin.setToolTip(self.t("tip_margin"))
        self.input_overlap.setToolTip(self.t("tip_overlap"))
        self.cb_crop_marks.setText(self.t("cb_crop_marks"))
        self.cb_crop_marks.setToolTip(self.t("tip_crop_marks"))

        # 5. DPI
        self.grp_dpi.setTitle(self.t("grp_dpi"))
        self.lbl_dpi.setText(self.t("lbl_dpi"))
        self.combo_dpi.setItemText(0, self.t("dpi_150"))
        self.combo_dpi.setItemText(1, self.t("dpi_300"))
        self.combo_dpi.setItemText(2, self.t("dpi_600"))

        # 6. Buttons & Status
        self.btn_save_pdf.setText(self.t("btn_save_pdf"))
        self.btn_direct_print.setText(self.t("btn_direct_print"))
        self.btn_cancel.setText(self.t("btn_cancel"))
        if not self.worker or not self.worker.isRunning():
            self.lbl_worker_status.setText(self.t("lbl_status_ready"))

        # Toolbar & canvas
        self.tb_title.setText(self.t("canvas_title"))
        self.tip_bar.setText(self.t("tip_bar"))
        self.btn_zoom_in.setToolTip(self.t("zoom_in_tip"))
        self.btn_zoom_out.setToolTip(self.t("zoom_out_tip"))
        self.btn_zoom_100.setToolTip(self.t("zoom_100_tip"))
        self.btn_zoom_fit.setToolTip(self.t("zoom_fit_tip"))
        self.btn_zoom_fit.setText(self.t("zoom_fit_btn"))

        # Canvas & Preview update
        if not self.pil_image:
            self.lbl_page_summary.setText(self.t("page_summary_waiting"))
            self.show_empty_canvas()
        else:
            self.update_preview()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            #controlScroll {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
            #brandHeader {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            #btnLang {
                background-color: #f1f5f9;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
                font-size: 12px;
                text-align: center;
            }
            #btnLang:hover {
                background-color: #e2e8f0;
                border-color: #94a3b8;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 12px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QPushButton {
                background-color: #f1f5f9;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 7px 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                border-color: #94a3b8;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
            #btnSavePdf {
                background-color: #15803d;
                color: #ffffff;
                border: none;
                font-weight: bold;
                padding: 10px;
                font-size: 13px;
                border-radius: 6px;
            }
            #btnSavePdf:hover {
                background-color: #16a34a;
            }
            #btnSavePdf:disabled {
                background-color: #94a3b8;
            }
            #btnPrintDirect {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                font-weight: bold;
                padding: 10px;
                font-size: 13px;
                border-radius: 6px;
            }
            #btnPrintDirect:hover {
                background-color: #3b82f6;
            }
            #btnPrintDirect:disabled {
                background-color: #94a3b8;
            }
            #btnCancel {
                background-color: #dc2626;
                color: #ffffff;
                border: none;
                padding: 5px;
                border-radius: 4px;
                font-weight: bold;
            }
            #btnCancel:hover {
                background-color: #ef4444;
            }
            #canvasToolbar {
                background-color: #1e293b;
                border-bottom: 1px solid #334155;
            }
            QToolButton {
                background-color: #334155;
                color: #f8fafc;
                border: 1px solid #475569;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #475569;
            }
            #pageSummaryLabel {
                background-color: #eff6ff;
                color: #1e40af;
                border: 1px solid #bfdbfe;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                font-weight: 500;
            }
            #progressFrame {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
            }
            QProgressBar {
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                text-align: center;
                background-color: #e2e8f0;
                height: 18px;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 3px;
            }
            QDoubleSpinBox, QSpinBox, QComboBox {
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                padding: 4px 6px;
                background-color: #ffffff;
            }
        """)

    def show_empty_canvas(self):
        self.graphics_view.scene.clear()
        text_item = QGraphicsSimpleTextItem(self.t("empty_canvas"))
        font = QFont("Segoe UI", 13)
        text_item.setFont(font)
        text_item.setBrush(QBrush(QColor("#94a3b8")))
        self.graphics_view.scene.addItem(text_item)
        rect = text_item.boundingRect()
        text_item.setPos(-rect.width() / 2, -rect.height() / 2)
        self.graphics_view.fitInView(self.graphics_view.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def select_image_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.t("select_image_title"), "", self.t("image_filter")
        )
        if file_path:
            self.load_image_from_path(file_path)

    def load_image_from_path(self, file_path):
        try:
            pil_img = Image.open(file_path).convert("RGB")
            self.image_path = file_path
            self.pil_image = pil_img
            self.image_aspect_ratio = pil_img.width / pil_img.height

            file_name = os.path.basename(file_path)
            self.lbl_img_info.setText(f"<b>{file_name}</b><br>{pil_img.width} x {pil_img.height} px")

            # İlk açılışta en-boy oranını koruyarak yükseklik değerini ayarla
            self._updating_dimensions = True
            current_w = self.input_width.value()
            self.input_height.setValue(round(current_w / self.image_aspect_ratio, 1))
            self._updating_dimensions = False

            self.update_preview()
            self.graphics_view.fit_in_view()

        except Exception as e:
            QMessageBox.critical(self, self.t("err_title"), f"{self.t('error_open_img')}{str(e)}")

    def on_width_changed(self, val):
        if self._updating_dimensions or not self.pil_image:
            self.update_preview()
            return
        if self.cb_aspect_lock.isChecked() and self.image_aspect_ratio > 0:
            self._updating_dimensions = True
            new_height = val / self.image_aspect_ratio
            self.input_height.setValue(round(new_height, 1))
            self._updating_dimensions = False
        self.update_preview()

    def on_height_changed(self, val):
        if self._updating_dimensions or not self.pil_image:
            self.update_preview()
            return
        if self.cb_aspect_lock.isChecked() and self.image_aspect_ratio > 0:
            self._updating_dimensions = True
            new_width = val * self.image_aspect_ratio
            self.input_width.setValue(round(new_width, 1))
            self._updating_dimensions = False
        self.update_preview()

    def on_aspect_lock_toggled(self, checked):
        if checked and self.pil_image and self.image_aspect_ratio > 0:
            self._updating_dimensions = True
            current_w = self.input_width.value()
            self.input_height.setValue(round(current_w / self.image_aspect_ratio, 1))
            self._updating_dimensions = False
            self.update_preview()

    def on_paper_changed(self):
        paper_key = self.combo_paper.currentData()
        is_custom = (paper_key == "Custom")
        self.input_custom_w.setVisible(is_custom)
        self.input_custom_h.setVisible(is_custom)
        self.lbl_custom_w.setVisible(is_custom)
        self.lbl_custom_h.setVisible(is_custom)
        self.update_preview()

    def get_selected_paper_dims(self):
        paper_key = self.combo_paper.currentData()
        if paper_key == "Custom":
            w_mm = self.input_custom_w.value()
            h_mm = self.input_custom_h.value()
        else:
            w_mm, h_mm = PAPER_SIZES.get(paper_key, (210.0, 297.0))

        orientation_key = self.combo_orientation.currentData()
        if orientation_key == "landscape":
            return max(w_mm, h_mm), min(w_mm, h_mm)
        else:
            return min(w_mm, h_mm), max(w_mm, h_mm)

    def on_zoom_changed(self, zoom_val):
        pct = int(round(zoom_val * 100))
        self.lbl_zoom.setText(f"%{pct}")

    def update_preview(self):
        if not self.pil_image:
            return

        target_w_cm = self.input_width.value()
        target_h_cm = self.input_height.value()
        paper_w_mm, paper_h_mm = self.get_selected_paper_dims()
        margin_mm = self.input_margin.value()
        overlap_mm = self.input_overlap.value()

        # Etkin Çözünürlük (DPI) & Kalite Uyarısı Hesabı
        w_inch = target_w_cm / 2.54
        h_inch = target_h_cm / 2.54
        eff_dpi_w = self.pil_image.width / max(0.1, w_inch)
        eff_dpi_h = self.pil_image.height / max(0.1, h_inch)
        effective_dpi = int(min(eff_dpi_w, eff_dpi_h))

        if effective_dpi >= 250:
            badge_html = f"""
            <div style="background-color: #dcfce7; color: #166534; padding: 6px 10px; border-radius: 5px; border: 1px solid #bbf7d0; font-size: 11px;">
                <b>{self.t('badge_excellent_title', dpi=effective_dpi)}</b><br>
                {self.t('badge_excellent_desc')}
            </div>
            """
        elif effective_dpi >= 150:
            badge_html = f"""
            <div style="background-color: #e0f2fe; color: #075985; padding: 6px 10px; border-radius: 5px; border: 1px solid #bae6fd; font-size: 11px;">
                <b>{self.t('badge_standard_title', dpi=effective_dpi)}</b><br>
                {self.t('badge_standard_desc')}
            </div>
            """
        elif effective_dpi >= 100:
            badge_html = f"""
            <div style="background-color: #fef3c7; color: #92400e; padding: 6px 10px; border-radius: 5px; border: 1px solid #fde68a; font-size: 11px;">
                <b>{self.t('badge_medium_title', dpi=effective_dpi)}</b><br>
                {self.t('badge_medium_desc')}
            </div>
            """
        else:
            badge_html = f"""
            <div style="background-color: #fee2e2; color: #991b1b; padding: 6px 10px; border-radius: 5px; border: 1px solid #fecaca; font-size: 11px;">
                <b>{self.t('badge_low_title', dpi=effective_dpi)}</b><br>
                {self.t('badge_low_desc')}
            </div>
            """
        self.lbl_dpi_quality.setText(badge_html)

        # Dilimleme ve Sayfa Hesabı (mm cinsinden)
        target_w_mm = target_w_cm * 10
        target_h_mm = target_h_cm * 10

        printable_w_mm = max(10.0, paper_w_mm - 2 * margin_mm)
        printable_h_mm = max(10.0, paper_h_mm - 2 * margin_mm)

        stride_w_mm = max(10.0, printable_w_mm - overlap_mm)
        stride_h_mm = max(10.0, printable_h_mm - overlap_mm)

        cols = 1 if target_w_mm <= printable_w_mm else math.ceil((target_w_mm - printable_w_mm) / stride_w_mm) + 1
        rows = 1 if target_h_mm <= printable_h_mm else math.ceil((target_h_mm - printable_h_mm) / stride_h_mm) + 1
        total_pages = cols * rows

        paper_name = self.combo_paper.currentText().split(' ')[0]
        self.lbl_page_summary.setText(
            self.t("page_summary_format",
                   cols=cols,
                   rows=rows,
                   total_pages=total_pages,
                   paper_name=paper_name,
                   eff_w=printable_w_mm / 10,
                   eff_h=printable_h_mm / 10)
        )

        # Önizleme sahnesi oluşturma (96 DPI)
        prev_dpi = 96
        scale = prev_dpi / 25.4
        t_w_px = max(10, int(round(target_w_mm * scale)))
        t_h_px = max(10, int(round(target_h_mm * scale)))

        preview_img = self.pil_image.resize((t_w_px, t_h_px), Image.Resampling.BILINEAR)

        # Pillow -> QPixmap
        im_data = preview_img.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QImage(im_data, preview_img.width, preview_img.height, QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)

        self.graphics_view.scene.clear()

        # 1. Poster Görseli
        pixmap_item = self.graphics_view.scene.addPixmap(pixmap)
        pixmap_item.setPos(0, 0)

        # 2. Dış Çerçeve
        border_rect = QGraphicsRectItem(0, 0, t_w_px, t_h_px)
        border_rect.setPen(QPen(QColor("#000000"), 2))
        self.graphics_view.scene.addItem(border_rect)

        # 3. Sayfa Izgaraları, Örtüşme Şeritleri ve Sayfa Numaraları
        stride_w_px = stride_w_mm * scale
        stride_h_px = stride_h_mm * scale
        overlap_px = overlap_mm * scale

        grid_pen = QPen(QColor("#ef4444"), 2, Qt.PenStyle.DashLine)
        overlap_brush = QBrush(QColor(245, 158, 11, 65))  # Yarı saydam amber örtüşme alanı
        overlap_pen = QPen(QColor(217, 119, 6, 120), 1, Qt.PenStyle.DotLine)

        # Dikey kesim çizgileri ve örtüşme alanları
        for c in range(1, cols):
            cut_x = c * stride_w_px
            if cut_x < t_w_px:
                line = QGraphicsLineItem(cut_x, 0, cut_x, t_h_px)
                line.setPen(grid_pen)
                self.graphics_view.scene.addItem(line)

                # Örtüşme şeridi
                ol_rect = QGraphicsRectItem(cut_x, 0, min(overlap_px, t_w_px - cut_x), t_h_px)
                ol_rect.setBrush(overlap_brush)
                ol_rect.setPen(overlap_pen)
                self.graphics_view.scene.addItem(ol_rect)

        # Yatay kesim çizgileri ve örtüşme alanları
        for r in range(1, rows):
            cut_y = r * stride_h_px
            if cut_y < t_h_px:
                line = QGraphicsLineItem(0, cut_y, t_w_px, cut_y)
                line.setPen(grid_pen)
                self.graphics_view.scene.addItem(line)

                # Örtüşme şeridi
                ol_rect = QGraphicsRectItem(0, cut_y, t_w_px, min(overlap_px, t_h_px - cut_y))
                ol_rect.setBrush(overlap_brush)
                ol_rect.setPen(overlap_pen)
                self.graphics_view.scene.addItem(ol_rect)

        # Sayfa rozetleri
        page_num = 1
        font_badge = QFont("Segoe UI", 10, QFont.Weight.Bold)
        for r in range(rows):
            for c in range(cols):
                box_x = c * stride_w_px
                box_y = r * stride_h_px
                badge_bg = QGraphicsRectItem(box_x + 8, box_y + 8, 110, 24)
                badge_bg.setBrush(QBrush(QColor(15, 23, 42, 190)))
                badge_bg.setPen(QPen(Qt.PenStyle.NoPen))
                self.graphics_view.scene.addItem(badge_bg)

                badge_str = self.t("badge_preview_page", num=page_num, col=c + 1, row=r + 1)
                badge_text = QGraphicsSimpleTextItem(badge_str)
                badge_text.setFont(font_badge)
                badge_text.setBrush(QBrush(QColor("#ffffff")))
                badge_text.setPos(box_x + 14, box_y + 11)
                self.graphics_view.scene.addItem(badge_text)
                page_num += 1

    def set_controls_enabled(self, enabled):
        self.btn_load.setEnabled(enabled)
        self.btn_save_pdf.setEnabled(enabled)
        self.btn_direct_print.setEnabled(enabled)
        self.input_width.setEnabled(enabled)
        self.input_height.setEnabled(enabled)
        self.combo_paper.setEnabled(enabled)
        self.combo_orientation.setEnabled(enabled)
        self.combo_dpi.setEnabled(enabled)
        self.btn_lang.setEnabled(enabled)
        self.btn_cancel.setVisible(not enabled)

    def start_pdf_generation(self):
        if not self.pil_image:
            QMessageBox.warning(self, self.t("warn_title"), self.t("warn_select_img"))
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, self.t("save_pdf_title"), "poster_output.pdf", self.t("save_pdf_filter")
        )
        if not save_path:
            return

        self.set_controls_enabled(False)
        self.progress_bar.setValue(0)
        self.lbl_worker_status.setText(self.t("lbl_status_starting"))

        paper_w_mm, paper_h_mm = self.get_selected_paper_dims()
        dpi = self.combo_dpi.currentData()

        self.worker = PosterRenderWorker(
            mode="pdf",
            pil_image=self.pil_image,
            target_w_cm=self.input_width.value(),
            target_h_cm=self.input_height.value(),
            paper_w_mm=paper_w_mm,
            paper_h_mm=paper_h_mm,
            margin_mm=self.input_margin.value(),
            overlap_mm=self.input_overlap.value(),
            dpi=dpi,
            draw_marks=self.cb_crop_marks.isChecked(),
            lang=self.current_lang,
            save_path=save_path
        )
        self.worker.progress.connect(self.on_worker_progress)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.error.connect(self.on_worker_error)
        self.worker.start()

    def start_direct_print(self):
        if not self.pil_image:
            QMessageBox.warning(self, self.t("warn_title"), self.t("warn_select_img"))
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            orientation_key = self.combo_orientation.currentData()
            if orientation_key == "landscape":
                printer.setPageOrientation(QPageLayout.Orientation.Landscape)
            else:
                printer.setPageOrientation(QPageLayout.Orientation.Portrait)

            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle(self.t("print_dialog_title"))
            if dialog.exec() != QPrintDialog.DialogCode.Accepted:
                return

            self.pending_printer = printer
            self.set_controls_enabled(False)
            self.progress_bar.setValue(0)
            self.lbl_worker_status.setText(self.t("lbl_status_printing_prep"))

            paper_w_mm, paper_h_mm = self.get_selected_paper_dims()
            dpi = self.combo_dpi.currentData()

            self.worker = PosterRenderWorker(
                mode="print",
                pil_image=self.pil_image,
                target_w_cm=self.input_width.value(),
                target_h_cm=self.input_height.value(),
                paper_w_mm=paper_w_mm,
                paper_h_mm=paper_h_mm,
                margin_mm=self.input_margin.value(),
                overlap_mm=self.input_overlap.value(),
                dpi=dpi,
                draw_marks=self.cb_crop_marks.isChecked(),
                lang=self.current_lang
            )
            self.worker.progress.connect(self.on_worker_progress)
            self.worker.finished.connect(self.on_worker_finished)
            self.worker.error.connect(self.on_worker_error)
            self.worker.start()

        except Exception as e:
            QMessageBox.critical(self, self.t("print_err_title"), f"{self.t('print_err_init')}{str(e)}")

    def cancel_worker(self):
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.lbl_worker_status.setText(self.t("lbl_status_cancelling"))

    def on_worker_progress(self, percent, text):
        self.progress_bar.setValue(percent)
        self.lbl_worker_status.setText(text)

    def on_worker_finished(self, status, data):
        self.set_controls_enabled(True)
        if status == "PDF_SUCCESS":
            self.lbl_worker_status.setText(self.t("lbl_status_pdf_done"))
            QMessageBox.information(
                self, self.t("pdf_success_title"),
                self.t("pdf_success_msg", path=data)
            )
        elif status == "PRINT_READY":
            pages = data
            if self.pending_printer and pages:
                try:
                    self.lbl_worker_status.setText(self.t("lbl_status_sending_printer"))
                    painter = QPainter(self.pending_printer)
                    total = len(pages)
                    for i, page_img in enumerate(pages):
                        if i > 0:
                            self.pending_printer.newPage()
                        im_data = page_img.convert("RGBA").tobytes("raw", "RGBA")
                        qimg = QImage(im_data, page_img.width, page_img.height, QImage.Format.Format_RGBA8888)
                        rect = self.pending_printer.pageRect(QPrinter.Unit.DevicePixel)
                        painter.drawImage(rect, qimg)
                    painter.end()
                    self.lbl_worker_status.setText(self.t("lbl_status_print_done"))
                    QMessageBox.information(
                        self, self.t("print_success_title"),
                        self.t("print_success_msg", total=total)
                    )
                except Exception as e:
                    QMessageBox.critical(self, self.t("print_err_title"), f"{self.t('print_err_pages')}{str(e)}")
            self.pending_printer = None

    def on_worker_error(self, err_msg):
        self.set_controls_enabled(True)
        self.pending_printer = None
        self.lbl_worker_status.setText(self.t("lbl_status_error_cancel"))
        QMessageBox.warning(self, self.t("info_title"), f"{err_msg}")


if __name__ == "__main__":
    # Windows görev çubuğunda uygulamanın kendi ikonunun doğru görünmesi için
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("posterprint.pro.app.v1")
        except Exception:
            pass

    app = QApplication(sys.argv)

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = PosterPrinterApp()
    window.show()
    sys.exit(app.exec())
"""GUIインターフェース"""

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .core import generate_metronome
from .io import save_as_mp3


class MetronomeGUI:
    """メトロノームGUIアプリケーション"""

    def __init__(self, root):
        self.root = root
        self.root.title("メトロノーム音声生成ツール")
        self.root.geometry("500x400")

        # ウィンドウのサイズを固定
        self.root.resizable(False, False)

        # 生成中フラグ
        self.is_generating = False

        self._create_widgets()

    def _create_widgets(self):
        """ウィジェットを作成"""

        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # タイトル
        title_label = ttk.Label(
            main_frame, text="メトロノーム音声生成ツール", font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # BPM設定
        ttk.Label(main_frame, text="BPM:", font=("Helvetica", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )

        self.bpm_var = tk.IntVar(value=120)
        bpm_frame = ttk.Frame(main_frame)
        bpm_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # BPM数値入力
        self.bpm_spinbox = ttk.Spinbox(
            bpm_frame,
            from_=20,
            to=300,
            textvariable=self.bpm_var,
            width=8,
            command=self._update_bpm_from_spinbox,
        )
        self.bpm_spinbox.pack(side=tk.LEFT, padx=(0, 10))

        # BPMスライダー
        self.bpm_scale = ttk.Scale(
            bpm_frame,
            from_=20,
            to=300,
            orient=tk.HORIZONTAL,
            variable=self.bpm_var,
            command=self._update_bpm_from_scale,
        )
        self.bpm_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 長さ設定
        ttk.Label(main_frame, text="長さ（秒）:", font=("Helvetica", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )

        self.duration_var = tk.IntVar(value=60)
        duration_frame = ttk.Frame(main_frame)
        duration_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        self.duration_spinbox = ttk.Spinbox(
            duration_frame, from_=10, to=600, textvariable=self.duration_var, width=10
        )
        self.duration_spinbox.pack(side=tk.LEFT)

        ttk.Label(duration_frame, text="（10〜600秒）").pack(side=tk.LEFT, padx=(10, 0))

        # サンプリングレート設定
        ttk.Label(main_frame, text="サンプリングレート:", font=("Helvetica", 12)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )

        self.sample_rate_var = tk.StringVar(value="44100")
        sample_rate_combo = ttk.Combobox(
            main_frame,
            textvariable=self.sample_rate_var,
            values=["22050", "44100", "48000"],
            state="readonly",
            width=15,
        )
        sample_rate_combo.grid(row=3, column=1, sticky=tk.W, pady=5)

        # リズムパターン設定
        ttk.Label(main_frame, text="リズムパターン:", font=("Helvetica", 12)).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )

        self.pattern_var = tk.StringVar(value="4beat")
        pattern_combo = ttk.Combobox(
            main_frame,
            textvariable=self.pattern_var,
            values=["4beat", "4to8"],
            state="readonly",
            width=15,
        )
        pattern_combo.grid(row=4, column=1, sticky=tk.W, pady=5)

        # パターン説明
        pattern_info = "4beat: 4つ打ち | 4to8: 4つ打ち2小節→8つ打ち1小節"
        ttk.Label(main_frame, text=pattern_info, font=("Helvetica", 9), foreground="gray").grid(
            row=5, column=0, columnspan=2, pady=(0, 5)
        )

        # 出力ファイル名
        ttk.Label(main_frame, text="出力ファイル名:", font=("Helvetica", 12)).grid(
            row=6, column=0, sticky=tk.W, pady=5
        )

        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)

        self.filename_var = tk.StringVar(value="")
        self.filename_entry = ttk.Entry(file_frame, textvariable=self.filename_var)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_button = ttk.Button(file_frame, text="参照", command=self._browse_file, width=8)
        browse_button.pack(side=tk.LEFT, padx=(5, 0))

        # 説明文
        info_text = "ファイル名を指定しない場合、デフォルト名で保存されます"
        ttk.Label(main_frame, text=info_text, font=("Helvetica", 9), foreground="gray").grid(
            row=7, column=0, columnspan=2, pady=(0, 10)
        )

        # 生成ボタン
        self.generate_button = ttk.Button(
            main_frame, text="音声を生成", command=self._generate_audio, style="Accent.TButton"
        )
        self.generate_button.grid(row=8, column=0, columnspan=2, pady=20)

        # プログレスバー
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate", length=300)
        self.progress.grid(row=9, column=0, columnspan=2, pady=(0, 10))

        # ステータスラベル
        self.status_label = ttk.Label(
            main_frame,
            text="BPMとオプションを設定して「音声を生成」をクリック",
            font=("Helvetica", 10),
        )
        self.status_label.grid(row=10, column=0, columnspan=2)

        # カラムの重みを設定
        main_frame.columnconfigure(1, weight=1)

    def _update_bpm_from_scale(self, value):
        """スライダーからBPMを更新"""
        bpm = int(float(value))
        self.bpm_var.set(bpm)

    def _update_bpm_from_spinbox(self):
        """スピンボックスからBPMを更新"""
        try:
            bpm = self.bpm_var.get()
            # スライダーも更新
            self.bpm_scale.set(bpm)
        except tk.TclError:
            pass

    def _browse_file(self):
        """ファイル保存ダイアログを表示"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if filename:
            self.filename_var.set(filename)

    def _generate_audio(self):
        """音声を生成（別スレッドで実行）"""
        if self.is_generating:
            messagebox.showwarning("警告", "既に音声を生成中です")
            return

        # パラメータを取得
        bpm = self.bpm_var.get()
        duration = self.duration_var.get()
        sample_rate = int(self.sample_rate_var.get())
        pattern = self.pattern_var.get()
        output_file = self.filename_var.get().strip()

        # 妥当性チェック
        if bpm < 20 or bpm > 300:
            messagebox.showwarning("警告", "BPMは20〜300の範囲で指定してください")
            return

        if duration < 10 or duration > 600:
            messagebox.showwarning("警告", "長さは10〜600秒の範囲で指定してください")
            return

        # UIを無効化
        self.generate_button.config(state="disabled")
        self.progress.start(10)
        self.status_label.config(text="音声を生成中...")
        self.is_generating = True

        # 別スレッドで生成
        thread = threading.Thread(
            target=self._generate_audio_thread,
            args=(bpm, duration, sample_rate, pattern, output_file),
        )
        thread.daemon = True
        thread.start()

    def _generate_audio_thread(self, bpm, duration, sample_rate, pattern, output_file):
        """音声生成を実行（スレッド内）"""
        try:
            # メトロノーム音声を生成
            wave_data = generate_metronome(
                bpm=bpm, duration_seconds=duration, sample_rate=sample_rate, pattern=pattern
            )

            # MP3として保存
            if not output_file:
                output_file = None

            saved_file = save_as_mp3(wave_data, sample_rate, output_file, bpm)

            # UIを更新（メインスレッドで実行）
            self.root.after(0, self._generation_complete, saved_file, None)

        except Exception as e:
            # エラー処理
            self.root.after(0, self._generation_complete, None, str(e))

    def _generation_complete(self, output_file, error):
        """生成完了時の処理"""
        # UIを有効化
        self.progress.stop()
        self.generate_button.config(state="normal")
        self.is_generating = False

        if error:
            self.status_label.config(text="エラーが発生しました")
            messagebox.showerror("エラー", f"音声生成に失敗しました:\n{error}")
        else:
            self.status_label.config(text=f"✓ 保存完了: {output_file}")
            messagebox.showinfo("完了", f"メトロノーム音声を保存しました:\n{output_file}")


def main():
    """GUIアプリケーションのエントリーポイント"""
    root = tk.Tk()
    MetronomeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

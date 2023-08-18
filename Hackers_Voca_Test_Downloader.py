import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from urllib import request
import time
from threading import Thread


class ExamDownloaderApp:
    def __init__(self, root):
        """
        시험지 생성 프로그램의 GUI 애플리케이션을 초기화합니다.

        Parameters:
            root (tk.Tk): Tkinter root 인스턴스
        """
        self.root = root
        self.root.title("시험지 생성 프로그램")

        self.q_type_options = ["우리말 뜻 맞히기", "표제어 보고 동의어 고르기", "우리말 뜻 맞히기 + 표제어 보고 동의어 고르기", "우리말 보고 영어단어 쓰기",
                               "동의어 보고 우리말 뜻 맞히기"]
        self.q_range_options = ["기출동의어", "중요동의어", "기출동의어 + 중요동의어"]

        self.q_type_var = tk.StringVar()
        self.q_range_var = tk.StringVar()
        self.answer_sheet_var = tk.StringVar(value="Y")

        self.create_widgets()

    def create_widgets(self):
        """위젯들을 생성하고 배치합니다."""
        self.create_input_widgets()
        self.create_option_widgets()
        self.create_download_button()

    def create_input_widgets(self):
        """입력 위젯들을 생성하고 배치합니다."""
        tk.Label(self.root, text="시작일:").pack()
        self.start_day_spinbox = tk.Spinbox(self.root, from_=1, to=30, increment=1)
        self.start_day_spinbox.pack()

        tk.Label(self.root, text="종료일:").pack()
        self.end_day_spinbox = tk.Spinbox(self.root, from_=1, to=30, increment=1)
        self.end_day_spinbox.pack()

        tk.Label(self.root, text="문항 수:").pack()
        self.q_num_spinbox = tk.Spinbox(self.root, from_=1, to=50, increment=1)
        self.q_num_spinbox.pack()

    def create_option_widgets(self):
        """옵션 위젯들을 생성하고 배치합니다."""
        self.create_combobox("문제 유형 선택:", self.q_type_options, self.q_type_var)
        self.create_combobox("출제 범위 선택:", self.q_range_options, self.q_range_var)
        self.create_combobox("문제지 출력 여부:", ["출력", "미출력"], self.answer_sheet_var)

    def create_combobox(self, label_text, options, variable):
        """
        콤보박스 위젯을 생성하고 배치합니다.

        Parameters:
            label_text (str): 라벨에 표시될 텍스트
            options (list): 콤보박스에 표시될 옵션 리스트
            variable (tk.StringVar): 선택된 값을 저장할 변수
        """
        tk.Label(self.root, text=label_text).pack()
        combobox = ttk.Combobox(self.root, values=options, textvariable=variable, state="readonly")
        combobox.pack()

    def create_download_button(self):
        """시험지 생성 버튼을 생성하고 배치합니다."""
        self.download_button = tk.Button(self.root, text="시험지 생성", command=self.download_exams)
        self.download_button.pack()

    def download_exams(self):
        """시험지 다운로드 작업을 수행합니다."""
        try:
            start_day = int(self.start_day_spinbox.get())
            end_day = int(self.end_day_spinbox.get())
            q_num = int(self.q_num_spinbox.get())
            q_type = self.q_type_var.get()
            q_range = self.q_range_var.get()
            answer_sheet = self.answer_sheet_var.get()

            self.validate_inputs(start_day, end_day, q_num, q_type, q_range, answer_sheet)

            q_type_index = self.get_index_from_option(q_type, self.q_type_options)
            q_range_index = self.get_index_from_option(q_range, self.q_range_options)

            download_thread = Thread(target=self.download_thread_func,
                                     args=(start_day, end_day, q_num, q_type_index, q_range_index, answer_sheet))
            download_thread.start()
        except ValueError as e:
            messagebox.showerror("에러", str(e))

    def get_index_from_option(self, value, options):
        return options.index(value)

    def validate_inputs(self, start_day, end_day, q_num, q_type, q_range, answer_sheet):
        """사용자 입력값을 검증합니다."""
        if not (0 < start_day <= 30) or not (0 < end_day <= 30) or start_day > end_day:
            raise ValueError("시험 생성 일은 1부터 30이여야 합니다.")
        if not (0 < q_num <= 50):
            raise ValueError("문항 수는 1부터 50 사이여야 합니다.")
        valid_ranges = ["우리말 뜻 맞히기", "표제어 보고 동의어 고르기", "우리말 뜻 맞히기 + 표제어 보고 동의어 고르기", "우리말 보고 영어단어 쓰기",
                        "동의어 보고 우리말 뜻 맞히기"]
        if q_type not in valid_ranges:
            raise ValueError("문제 유형 선택이 올바르지 않습니다.")
        valid_ranges = ["기출동의어", "중요동의어", "기출동의어 + 중요동의어"]
        if q_range not in valid_ranges:
            raise ValueError("출제 범위 선택이 올바르지 않습니다.")
        if answer_sheet != "Y" and answer_sheet != "N":
            raise ValueError("문제지 출력 여부는 'Y' 또는 'N'이어야 합니다.")

    def download_thread_func(self, start_day, end_day, q_num, q_type, q_range, answer_sheet):
        """시험지 다운로드를 위한 스레드 함수입니다."""
        for day in range(start_day, end_day + 1):
            url = f'https://www.gohackers.com/modules/contents/lang.korean/pages/voca_program/pdf_paper.php?m=contents&front=voca_program&mode=pdf&iframe=Y&day1={day}&day2={day}&question={q_num}&type={q_type}&cate={q_range}&answer={answer_sheet}'
            with request.urlopen(url) as url_data:
                with open(f"./Day{day}_test.pdf", "wb") as pdf:
                    pdf.write(url_data.read())
                    time.sleep(0.5)
        messagebox.showinfo("다운로드 완료", f"Day{day}_test.pdf가 다운로드 되었습니다.")  # TODO: 저장할 공간을 구현


if __name__ == "__main__":
    root = tk.Tk()
    app = ExamDownloaderApp(root)
    root.mainloop()

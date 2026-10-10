"""
Quiz / Exam Marking System

A Python (tkinter) desktop application that manages student quiz/exam
marks: adding students, validating marks, calculating grades, viewing
results, searching, and showing the highest mark.

Run with:  python exam_marking_system.py
No external libraries required — uses only Python's standard library.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Colors (purple / cream design)
# Colors (Modern Slate & Stress-Reducing Teal Design)
BG = "#F2F6F3"              # Ultra-light mint/sage window background
PANEL = "#162E20"           # Rich dark forest green card background
CARD_TEXT = "#FAFCFA"       # Crisp white/off-white text on dark cards
CARD_MUTED = "#9FB0A5"      # Balanced soft sage secondary text on dark cards
CARD_HOVER = "#244432"      # Dark green hover highlight state
BORDER = "#CBD2CE"          # Clean grey-green border line color
INK = "#0F1A13"             # Deep charcoal green text for light canvas areas
MUTED = "#5C6E63"           # Muted sage text for light canvas areas
PRIMARY = "#2E7D46"         # Vibrant leaf green accent for main buttons
PRIMARY_DARK = "#1E5A30"    # Deep emerald for button hover states
PRIMARY_LIGHT = "#66BB80"   # Light emerald accent lines and badges
PRIMARY_TINT = "#EAF5EE"    # Light mint tint for external highlights
GOLD = "#F5A623"            # Energetic amber gold for trophy highlights
RED = "#D9453B"             # Clean crimson red for validation alerts
RED_TINT = "#FCECEB"        # Soft rose tint for error areas
ABSENT_COLOR = "#66BB80"    # Bright light green for "AB" mark entries



FONT_FAMILY = ("Aptos", "Arial", "Helvetica") # Modern typographic stack

FONT_TITLE = (FONT_FAMILY[0], 24, "bold")      # Scaled up from 18
FONT_SUB = (FONT_FAMILY[0], 12)               # Scaled up from 10
FONT_LABEL = (FONT_FAMILY[0], 12, "bold")     # Scaled up from 10
FONT_BODY = (FONT_FAMILY[0], 13)               # Scaled up from 11
FONT_BODY_BOLD = (FONT_FAMILY[0], 13, "bold")  # Scaled up from 11
FONT_BIG = (FONT_FAMILY[0], 28, "bold")       # Scaled up from 22

# ---------------------------------------------------------------------
# Core logic (same functions you'd use in a console version)
# ---------------------------------------------------------------------
students = []          # list of student dictionaries
id_counter = 1000       # used to generate simple student IDs


def calculate_grade(average):
    """Return (grade, status) based on the report's grading table."""
    if average >= 75:
        return "A", "Pass"
    elif average >= 65:
        return "B", "Pass"
    elif average >= 55:
        return "C", "Pass"
    elif average >= 45:
        return "S", "Pass"
    else:
        return "F", "Fail"


def add_student(name, index_number, subject_marks):
    """Validate marks, calculate results, and store the student record.

    subject_marks: a list of (subject_label, value) tuples, in subject
    order, where value is either a numeric mark (0-100) or the string
    "AB" for a subject the student was absent for. An absent subject
    contributes 0 toward the total, but the total/max is always shown
    out of the full 300 (3 subjects x 100), never reduced.
    """
    global id_counter
    numeric_values = [v for _, v in subject_marks if isinstance(v, (int, float))]
    total = sum(numeric_values)
    max_total = len(subject_marks) * 100
    average = total / len(subject_marks)
    grade, status = calculate_grade(average)
    has_absent = any(v == "AB" for _, v in subject_marks)
    id_counter += 1

    student = {
        "id": f"STU-{id_counter}",
        "index_number": index_number,
        "name": name,
        "subjects": dict(subject_marks),
        "total": total,
        "max": max_total,
        "average": average,
        "grade": grade,
        "status": status,
        "has_absent": has_absent,
    }
    students.append(student)
    return student


def find_student(query):
    """Find a student by exact name match or by index number."""
    query = query.strip().lower()
    for s in students:
        if s["name"].strip().lower() == query:
            return s
    for s in students:
        if s["index_number"].strip().lower() == query:
            return s
    return None


def get_highest():
    if not students:
        return None
    return max(students, key=lambda s: s["average"])


def initials(name):
    parts = name.strip().split()
    return "".join(p[0] for p in parts[:2]).upper() if parts else "?"


def _is_letters_input(value):
    """Validation for the Student Name field — letters and spaces only."""
    return value == "" or all(c.isalpha() or c.isspace() for c in value)


def _is_number_input(value):
    """Validation for a plain numeric field — digits with an optional decimal point."""
    if value == "":
        return True
    if value.count(".") > 1:
        return False
    return all(c.isdigit() or c == "." for c in value)


def _is_mark_input(value):
    """Validation for subject mark fields — a number (0-100), or the
    letters that build up to 'AB' (case-insensitive) for an absent student."""
    if value == "":
        return True
    if value.upper() in ("A", "AB"):
        return True
    if value.count(".") > 1:
        return False
    return all(c.isdigit() or c == "." for c in value)


def _is_digits_input(value):
    """Validation for the Index Number field — digits only."""
    return value == "" or value.isdigit()


# ---------------------------------------------------------------------
# GUI helper widgets
# ---------------------------------------------------------------------

class Card(tk.Frame):
    """A rounded-looking panel (tkinter has no real border-radius, so we
    fake it with a subtle border and padding)."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PANEL, highlightbackground=BORDER,
                          highlightthickness=1, **kwargs)


class PrimaryButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PRIMARY, fg="white", activebackground=PRIMARY_DARK,
                          activeforeground="white", relief="flat", font=FONT_BODY_BOLD,
                          bd=0, padx=14, pady=10, cursor="hand2", **kwargs)
        self.bind("<Enter>", lambda e: self.config(bg=PRIMARY_DARK))
        self.bind("<Leave>", lambda e: self.config(bg=PRIMARY))


class OutlineButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", fg=INK, activebackground=PRIMARY_TINT,
                          relief="solid", bd=1, font=FONT_BODY, padx=14, pady=9,
                          cursor="hand2", highlightbackground=BORDER, **kwargs)
        self.bind("<Enter>", lambda e: self.config(bg=PRIMARY_TINT, highlightbackground=PRIMARY_LIGHT))
        self.bind("<Leave>", lambda e: self.config(bg="white", highlightbackground=BORDER))


class MenuItem(tk.Button):
    def __init__(self, parent, number, text, command, accent=PRIMARY_LIGHT):
        super().__init__(
            parent, text=f"  {number}    {text}", anchor="w", justify="left",
            bg=PANEL, fg=CARD_TEXT, activebackground=CARD_HOVER, activeforeground=CARD_TEXT,
            relief="flat", bd=1, font=FONT_BODY_BOLD, padx=14, pady=14, cursor="hand2",
            highlightbackground=BORDER, highlightthickness=1, command=command
        )
        self._accent = accent
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=CARD_HOVER, fg=CARD_TEXT, highlightbackground=self._accent, highlightthickness=2)

    def _on_leave(self, e):
        self.config(bg=PANEL, fg=CARD_TEXT, highlightbackground=BORDER, highlightthickness=1)


class GradientStripe(tk.Canvas):
    """A small horizontal gradient bar blending the two accent colors,
    used under the header for a more dynamic, less flat look."""
    def __init__(self, parent, width=140, height=4, c1=PRIMARY, c2=PRIMARY_LIGHT, **kwargs):
        super().__init__(parent, width=width, height=height, bg=BG,
                          highlightthickness=0, **kwargs)
        steps = width
        r1, g1, b1 = self.winfo_rgb(c1)
        r2, g2, b2 = self.winfo_rgb(c2)
        for i in range(steps):
            t = i / steps
            r = int(r1 + (r2 - r1) * t) >> 8
            g = int(g1 + (g2 - g1) * t) >> 8
            b = int(b1 + (b2 - b1) * t) >> 8
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(i, 0, i, height, fill=color)


# ---------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------

class ExamMarkingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz / Exam Marking System")
        self.configure(bg=BG)
        self.resizable(True, True)

        # Open filling the screen automatically so nothing needs manual
        # resizing, then still allow the user to resize/restore freely.
        self._maximize_on_start()
        self.minsize(420, 520)

        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", pady=(24, 10))
        self.title_lbl = tk.Label(header, text="Quiz / Exam Marking System", font=FONT_TITLE,
                                   bg=BG, fg=INK, justify="center")
        self.title_lbl.pack(padx=12)
        self.subtitle_lbl = tk.Label(header, text="Principles of Computer Programming", font=FONT_SUB,
                                      bg=BG, fg=MUTED, justify="center")
        self.subtitle_lbl.pack(pady=(2, 8), padx=12)
        GradientStripe(header, width=64, height=4).pack()

        # Container that holds all screens (only one visible at a time)
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True, padx=24, pady=10)

        self.frames = {}
        for F in (MainMenu, AddStudent, ResultView, SearchStudent,
                  ViewAllResults, HighestMark):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("MainMenu")

        # Keep the header text wrapping to the current window width instead
        # of being clipped when the window is made narrower.
        self.bind("<Configure>", self._on_resize)

    def _maximize_on_start(self):
        """Open the window maximized so the whole UI fills the screen
        immediately, without the user having to drag it larger.

        Tk's maximize mechanism differs by platform, so this tries each
        in turn and falls back to an explicit full-screen-sized geometry
        if none of the native mechanisms are available."""
        try:
            # Windows, and some macOS Tk builds
            self.state("zoomed")
            return
        except tk.TclError:
            pass
        try:
            # Linux / X11
            self.attributes("-zoomed", True)
            return
        except tk.TclError:
            pass
        # Last-resort fallback: size the window to the full screen manually.
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"{screen_w}x{screen_h}+0+0")

    def _on_resize(self, event):
        if event.widget is self:
            wrap = max(200, event.width - 48)
            self.title_lbl.config(wraplength=wrap)
            self.subtitle_lbl.config(wraplength=wrap)

    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()


# ---------------------------------------------------------------------
# Screen: Main Menu
# ---------------------------------------------------------------------

class MainMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        items = [
            ("01", "Add Student Marks", lambda: app.show_frame("AddStudent")),
            ("02", "View Student Result", lambda: app.show_frame("SearchStudent")),
            ("03", "View All Results", lambda: app.show_frame("ViewAllResults")),
            ("04", "Show Highest Mark", lambda: app.show_frame("HighestMark")),
            ("05", "Exit", self.exit_app),
        ]
        # Alternate the hover accent between the two accent colors for
        # a livelier, less uniform feel.
        accents = [PRIMARY_LIGHT, GOLD]
        for i, (num, text, cmd) in enumerate(items):
            MenuItem(self, num, text, cmd, accent=accents[i % 2]).pack(fill="x", pady=5)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Exit the program?"):
            self.app.destroy()


# ---------------------------------------------------------------------
# Screen: Add Student
# ---------------------------------------------------------------------

class AddStudent(tk.Frame):
    SUBJECT_LABELS = ["MATHS", "IT", "PHYSICS"]

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        # Validation commands (registered against this widget so tkinter
        # can call them on every keystroke)
        vcmd_letters = (self.register(_is_letters_input), "%P")
        vcmd_digits = (self.register(_is_digits_input), "%P")
        vcmd_mark = (self.register(_is_mark_input), "%P")

        card = Card(self, padx=24, pady=24)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Add Student Marks", font=("Segoe UI", 15, "bold"),
                 bg=PANEL, fg=CARD_TEXT).pack(anchor="w")
        tk.Label(card, text="Enter the student's name and marks (0-100, or AB if absent).",
                 font=FONT_SUB, bg=PANEL, fg=CARD_MUTED).pack(anchor="w", pady=(2, 18))

        tk.Label(card, text="STUDENT NAME", font=FONT_LABEL, bg=PANEL, fg=CARD_MUTED).pack(anchor="w")
        self.name_entry = tk.Entry(card, font=FONT_BODY, relief="solid", bd=1,
                                    highlightbackground=BORDER,
                                    validate="key", validatecommand=vcmd_letters)
        self.name_entry.pack(fill="x", pady=(4, 16), ipady=6)

        tk.Label(card, text="INDEX NUMBER", font=FONT_LABEL, bg=PANEL, fg=CARD_MUTED).pack(anchor="w")
        self.index_entry = tk.Entry(card, font=FONT_BODY, relief="solid", bd=1,
                                     highlightbackground=BORDER,
                                     validate="key", validatecommand=vcmd_digits)
        self.index_entry.pack(fill="x", pady=(4, 16), ipady=6)

        marks_row = tk.Frame(card, bg=PANEL)
        marks_row.pack(fill="x", pady=(0, 4))
        self.mark_entries = []
        for i in range(3):
            col = tk.Frame(marks_row, bg=PANEL)
            col.pack(side="left", fill="x", expand=True, padx=(0 if i == 0 else 8, 0))
            tk.Label(col, text=self.SUBJECT_LABELS[i], font=FONT_LABEL, bg=PANEL, fg=CARD_MUTED).pack(anchor="w")
            e = tk.Entry(col, font=FONT_BODY, relief="solid", bd=1, highlightbackground=BORDER,
                         validate="key", validatecommand=vcmd_mark)
            e.pack(fill="x", pady=(4, 0), ipady=6)
            e.bind("<KeyRelease>", lambda ev, entry=e: self._format_mark_entry(entry))
            self.mark_entries.append(e)

        self.error_label = tk.Label(card, text="", font=FONT_SUB, bg=PANEL, fg=RED)
        self.error_label.pack(anchor="w", pady=(8, 6))

        btn_row = tk.Frame(card, bg=PANEL)
        btn_row.pack(fill="x", pady=(14, 0))
        OutlineButton(btn_row, text="Back to Main Menu",
                      command=lambda: app.show_frame("MainMenu")).pack(side="left", expand=True, fill="x", padx=(0, 6))
        PrimaryButton(btn_row, text="Submit & Calculate",
                      command=self.submit).pack(side="left", expand=True, fill="x", padx=(6, 0))

        # Pressing Enter in any field moves focus to the next one; on the
        # last field it submits the form.
        self.tab_order = [self.name_entry, self.index_entry, *self.mark_entries]
        for i, entry in enumerate(self.tab_order):
            if i + 1 < len(self.tab_order):
                next_widget = self.tab_order[i + 1]
                entry.bind("<Return>", lambda e, w=next_widget: (w.focus_set(), "break"))
            else:
                entry.bind("<Return>", lambda e: (self.submit(), "break"))

    def on_show(self):
        self.name_entry.delete(0, tk.END)
        self.index_entry.delete(0, tk.END)
        for e in self.mark_entries:
            e.delete(0, tk.END)
            e.config(highlightbackground=BORDER, highlightcolor=BORDER, fg="black", font=FONT_BODY)
        self.error_label.config(text="")

    def _format_mark_entry(self, entry):
        """Auto-uppercase 'ab'/'Ab' to 'AB' as the student types it, and
        color the field differently to flag it as an absent mark."""
        value = entry.get()
        if value.upper() == "AB":
            if value != "AB":
                entry.delete(0, tk.END)
                entry.insert(0, "AB")
            entry.config(fg=ABSENT_COLOR, font=FONT_BODY_BOLD)
        else:
            entry.config(fg="black", font=FONT_BODY)

    def submit(self):
        name = self.name_entry.get().strip()
        index_number = self.index_entry.get().strip()
        subject_marks = []
        has_error = False

        for label, e in zip(self.SUBJECT_LABELS, self.mark_entries):
            val = e.get().strip()
            e.config(highlightbackground=BORDER)
            if val == "":
                has_error = True
                continue
            if val.upper() == "AB":
                subject_marks.append((label, "AB"))
                continue
            try:
                num = float(val)
                if 0 <= num <= 100:
                    subject_marks.append((label, num))
                else:
                    e.config(highlightbackground=RED)
                    has_error = True
            except ValueError:
                e.config(highlightbackground=RED)
                has_error = True

        if not name:
            self.error_label.config(text="Please enter a student name.")
            return
        if not index_number:
            self.error_label.config(text="Please enter an index number.")
            return
        if has_error or len(subject_marks) != len(self.SUBJECT_LABELS):
            self.error_label.config(text="Enter a mark (0-100) or AB for each of the three subjects.")
            return

        self.error_label.config(text="")
        student = add_student(name, index_number, subject_marks)

        self.app.frames["ResultView"].display(student)
        self.app.show_frame("ResultView")


# ---------------------------------------------------------------------
# Screen: Individual Result
# ---------------------------------------------------------------------

class ResultView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        self.card = Card(self, padx=24, pady=24)
        self.card.pack(fill="both", expand=True)

        tk.Label(self.card, text="Individual Student Result",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=CARD_TEXT).pack(anchor="w")
        tk.Label(self.card, text="Assessment summary report", font=FONT_SUB,
                 bg=PANEL, fg=CARD_MUTED).pack(anchor="w", pady=(2, 18))

        profile = tk.Frame(self.card, bg=PANEL)
        profile.pack(fill="x", pady=(0, 16))
        self.avatar = tk.Label(profile, text="JD", font=FONT_BODY_BOLD, bg=PRIMARY_TINT,
                                fg=PRIMARY_DARK, width=4, height=2)
        self.avatar.pack(side="left")
        name_col = tk.Frame(profile, bg=PANEL)
        name_col.pack(side="left", padx=12)
        self.name_lbl = tk.Label(name_col, text="", font=("Segoe UI", 14, "bold"), bg=PANEL, fg=CARD_TEXT)
        self.name_lbl.pack(anchor="w")
        self.id_lbl = tk.Label(name_col, text="", font=FONT_SUB, bg=PANEL, fg=CARD_MUTED)
        self.id_lbl.pack(anchor="w")

        stats = tk.Frame(self.card, bg=PANEL)
        stats.pack(fill="x", pady=(0, 16))
        self.total_stat = self._make_stat(stats, "TOTAL MARKS")
        self.avg_stat = self._make_stat(stats, "AVERAGE MARK")

        badges = tk.Frame(self.card, bg=PANEL)
        badges.pack(fill="x", pady=(0, 20))
        self.grade_lbl = tk.Label(badges, text="", font=FONT_BODY_BOLD, bg=PRIMARY_TINT,
                                   fg=PRIMARY_DARK, padx=10, pady=6)
        self.grade_lbl.pack(side="left")
        self.status_lbl = tk.Label(badges, text="", font=FONT_BODY_BOLD, padx=10, pady=6)
        self.status_lbl.pack(side="right")

        PrimaryButton(self.card, text="Calculate Another",
                      command=lambda: app.show_frame("AddStudent")).pack(fill="x")
        OutlineButton(self.card, text="Back to Main Menu",
                      command=lambda: app.show_frame("MainMenu")).pack(fill="x", pady=(10, 0))

    def _make_stat(self, parent, label):
        box = tk.Frame(parent, bg="white", highlightbackground=BORDER, highlightthickness=1)
        box.pack(side="left", fill="both", expand=True, padx=(0, 8), ipady=8, ipadx=8)
        tk.Label(box, text=label, font=("Segoe UI", 8, "bold"), bg="white", fg=MUTED).pack(anchor="w", padx=10, pady=(6, 0))
        value = tk.Label(box, text="", font=("Segoe UI", 16, "bold"), bg="white", fg=INK)
        value.pack(anchor="w", padx=10, pady=(0, 6))
        return value

    def display(self, student):
        self.avatar.config(text=initials(student["name"]))
        self.name_lbl.config(text=student["name"])
        self.id_lbl.config(text=f"Index No: {student['index_number']}")
        self.total_stat.config(text=f"{student['total']} / {student['max']}")
        self.avg_stat.config(text=f"{student['average']:.1f}%")
        self.grade_lbl.config(text=f"Grade: {student['grade']}")

        if student["status"] == "Pass":
            self.status_lbl.config(text="PASS", bg=PRIMARY_TINT, fg=PRIMARY_DARK)
        else:
            self.status_lbl.config(text="FAIL", bg=RED_TINT, fg=RED)


# ---------------------------------------------------------------------
# Screen: Search / View Student
# ---------------------------------------------------------------------

class SearchStudent(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        card = Card(self, padx=24, pady=24)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Search Student", font=("Segoe UI", 15, "bold"),
                 bg=PANEL, fg=CARD_TEXT).pack(anchor="w")
        tk.Label(card, text="Find a student by name or index number to view their result.",
                 font=FONT_SUB, bg=PANEL, fg=CARD_MUTED).pack(anchor="w", pady=(2, 16))

        row = tk.Frame(card, bg=PANEL)
        row.pack(fill="x", pady=(0, 16))
        self.search_entry = tk.Entry(row, font=FONT_BODY, relief="solid", bd=1,
                                      highlightbackground=BORDER)
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.search_entry.bind("<Return>", lambda e: self.search())
        PrimaryButton(row, text="Search", command=self.search).pack(side="left", padx=(8, 0))

        self.result_area = tk.Frame(card, bg=PANEL)
        self.result_area.pack(fill="both", expand=True)
        self.empty_lbl = tk.Label(self.result_area, text="Enter a name or index number and press Search.",
                                   font=FONT_BODY, bg=PANEL, fg=CARD_MUTED)
        self.empty_lbl.pack(pady=30)

        OutlineButton(card, text="Back to Main Menu",
                      command=lambda: app.show_frame("MainMenu")).pack(fill="x", pady=(12, 0))

    def on_show(self):
        self.search_entry.delete(0, tk.END)
        for w in self.result_area.winfo_children():
            w.destroy()
        self.empty_lbl = tk.Label(self.result_area, text="Enter a name or index number and press Search.",
                                   font=FONT_BODY, bg=PANEL, fg=CARD_MUTED)
        self.empty_lbl.pack(pady=30)

    def search(self):
        for w in self.result_area.winfo_children():
            w.destroy()

        student = find_student(self.search_entry.get())
        if not student:
            tk.Label(self.result_area, text="No matching student found.",
                     font=FONT_BODY, bg=PANEL, fg=CARD_MUTED).pack(pady=30)
            return

        profile = tk.Frame(self.result_area, bg=PANEL)
        profile.pack(fill="x", pady=(6, 12))
        tk.Label(profile, text=initials(student["name"]), font=FONT_BODY_BOLD, bg=PRIMARY_TINT,
                 fg=PRIMARY_DARK, width=4, height=2).pack(side="left")
        col = tk.Frame(profile, bg=PANEL)
        col.pack(side="left", padx=12)
        tk.Label(col, text=student["name"], font=("Segoe UI", 13, "bold"), bg=PANEL, fg=CARD_TEXT).pack(anchor="w")
        tk.Label(col, text=f"Index No: {student['index_number']}", font=FONT_SUB, bg=PANEL, fg=CARD_MUTED).pack(anchor="w")

        stats = tk.Frame(self.result_area, bg=PANEL)
        stats.pack(fill="x", pady=(0, 10))
        for label, value in [("AVERAGE", f"{student['average']:.1f}%"), ("GRADE", student["grade"])]:
            box = tk.Frame(stats, bg="white", highlightbackground=BORDER, highlightthickness=1)
            box.pack(side="left", fill="both", expand=True, padx=(0, 8), ipady=8, ipadx=8)
            tk.Label(box, text=label, font=("Segoe UI", 8, "bold"), bg="white", fg=MUTED).pack(anchor="w", padx=10, pady=(6, 0))
            tk.Label(box, text=value, font=("Segoe UI", 15, "bold"), bg="white", fg=INK).pack(anchor="w", padx=10, pady=(0, 6))

        color, tint = (PRIMARY_DARK, PRIMARY_TINT) if student["status"] == "Pass" else (RED, RED_TINT)
        tk.Label(self.result_area, text=student["status"].upper(), font=FONT_BODY_BOLD,
                 bg=tint, fg=color, padx=10, pady=6).pack(anchor="w")


# ---------------------------------------------------------------------
# Screen: View All Results
# ---------------------------------------------------------------------

class ViewAllResults(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        card = Card(self, padx=24, pady=24)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="All Student Results", font=("Segoe UI", 15, "bold"),
                 bg=PANEL, fg=CARD_TEXT).pack(anchor="w")
        tk.Label(card, text="Marks are shown per subject; totals are always out of 300.",
                 font=FONT_SUB, bg=PANEL, fg=CARD_MUTED).pack(anchor="w", pady=(2, 4))
        self.count_lbl = tk.Label(card, text="", font=FONT_SUB, bg=PANEL, fg=CARD_MUTED)
        self.count_lbl.pack(anchor="w", pady=(2, 14))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", fieldbackground="white",
                         foreground=INK, rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background=PANEL, foreground=CARD_MUTED)
        style.map("Treeview", background=[("selected", PRIMARY_TINT)])

        cols = ("Index No", "Name", "Maths", "IT", "Physics", "Total", "Attendance", "Grade", "Status")
        # Relative weights used to divide up whatever width is available,
        # so the table fills the window instead of relying on a fixed
        # pixel width per column.
        col_weights = {
            "Index No": 10, "Name": 20, "Maths": 8, "IT": 8, "Physics": 8,
            "Total": 10, "Attendance": 12, "Grade": 8, "Status": 10,
        }
        min_widths = {
            "Index No": 60, "Name": 90, "Maths": 50, "IT": 45, "Physics": 55,
            "Total": 60, "Attendance": 65, "Grade": 45, "Status": 55,
        }

        # A dedicated frame holds the tree plus its scrollbars so the
        # table stays fully usable when the window is narrower or shorter
        # than the full table, or when there are more rows than fit.
        table_frame = tk.Frame(card, bg=PANEL)
        table_frame.pack(fill="both", expand=True, pady=(0, 14))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
        self._col_weights = col_weights
        self._min_widths = min_widths
        for c in cols:
            self.tree.heading(c, text=c)
            anchor = "w" if c in ("Index No", "Name") else "center"
            # stretch=True lets columns grow to fill the Treeview's actual
            # width; we additionally recompute exact widths on resize
            # (see _on_tree_resize) so extra space is distributed
            # proportionally rather than piling onto the last column.
            self.tree.column(c, anchor=anchor, width=min_widths[c], minwidth=min_widths[c], stretch=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Recompute column widths whenever the table area is resized so
        # the columns keep filling the full width automatically.
        self.tree.bind("<Configure>", self._on_tree_resize)

        # Alternate row shading for readability
        self.tree.tag_configure("odd", background=BG)
        self.tree.tag_configure("even", background="white")

        OutlineButton(card, text="Back to Main Menu",
                      command=lambda: app.show_frame("MainMenu")).pack(fill="x")

    def _on_tree_resize(self, event):
        """Distribute the Treeview's current width across the columns
        proportionally to their weight, never going below each column's
        minimum readable width."""
        cols = self.tree["columns"]
        total_weight = sum(self._col_weights[c] for c in cols)
        total_min = sum(self._min_widths[c] for c in cols)
        available = max(event.width, total_min)
        extra = available - total_min
        for c in cols:
            share = extra * (self._col_weights[c] / total_weight) if extra > 0 else 0
            self.tree.column(c, width=int(self._min_widths[c] + share))

    @staticmethod
    def _fmt_subject(student, label):
        """Return the display text for a single subject cell — the mark,
        or 'AB' if the student was absent for that subject."""
        value = student["subjects"].get(label)
        if value == "AB":
            return "AB"
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.1f}"

    def on_show(self):
        self.count_lbl.config(text=f"{len(students)} student record(s)")
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, s in enumerate(students):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(
                s["index_number"], s["name"],
                self._fmt_subject(s, "MATHS"), self._fmt_subject(s, "IT"), self._fmt_subject(s, "PHYSICS"),
                f"{s['total']:.0f}/{s['max']}",
                "AB" if s["has_absent"] else "Present",
                s["grade"], s["status"],
            ), tags=(tag,))


# ---------------------------------------------------------------------
# Screen: Highest Mark
# ---------------------------------------------------------------------

class HighestMark(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        card = Card(self, padx=24, pady=30)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="TOP PERFORMER", font=("Segoe UI", 9, "bold"),
                 bg=PANEL, fg=PRIMARY_LIGHT).pack()
        tk.Label(card, text="Highest Mark", font=("Segoe UI", 17, "bold"),
                 bg=PANEL, fg=CARD_TEXT).pack(pady=(2, 16))

        tk.Label(card, text="🏆", font=("Segoe UI", 26), bg=PRIMARY_TINT, width=3, height=1).pack(pady=(0, 14))

        self.name_lbl = tk.Label(card, text="No students yet", font=("Segoe UI", 15, "bold"),
                                  bg=PANEL, fg=CARD_TEXT)
        self.name_lbl.pack()
        self.index_lbl = tk.Label(card, text="", font=FONT_SUB, bg=PANEL, fg=CARD_MUTED)
        self.index_lbl.pack(pady=(2, 16))

        self.stats_frame = tk.Frame(card, bg=PANEL)
        self.avg_val = self._stat("AVERAGE SCORE")
        self.grade_val = self._stat("GRADE")

        OutlineButton(card, text="Back to Main Menu",
                      command=lambda: app.show_frame("MainMenu")).pack(fill="x", pady=(20, 0))

    def _stat(self, label):
        box = tk.Frame(self.stats_frame, bg="white", highlightbackground=BORDER, highlightthickness=1)
        box.pack(side="left", fill="both", expand=True, padx=6, ipady=10, ipadx=10)
        tk.Label(box, text=label, font=("Segoe UI", 8, "bold"), bg="white", fg=MUTED).pack(anchor="w", padx=10)
        val = tk.Label(box, text="–", font=("Segoe UI", 17, "bold"), bg="white", fg=INK)
        val.pack(anchor="w", padx=10, pady=(2, 4))
        return val

    def on_show(self):
        top = get_highest()
        if not top:
            self.name_lbl.config(text="No students yet")
            self.index_lbl.config(text="")
            self.stats_frame.pack_forget()
            return
        self.name_lbl.config(text=top["name"])
        self.index_lbl.config(text=f"Index No: {top['index_number']}")
        self.avg_val.config(text=f"{top['average']:.1f}%")
        self.grade_val.config(text=top["grade"])
        self.stats_frame.pack(fill="x", pady=(0, 6))


if __name__ == "__main__":
    app = ExamMarkingApp()
    app.mainloop()
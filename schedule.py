import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# Lưu công việc của các tuần
schedule_data = {}

# Hàm thêm công việc vào ca
def add_task():
    task = task_entry.get()
    if task != "":
        day = day_var.get()
        time_of_day = time_of_day_var.get()

        if current_week not in schedule_data:
            schedule_data[current_week] = {}

        if day not in schedule_data[current_week]:
            schedule_data[current_week][day] = {"sáng": [], "chiều": [], "tối": []}
        
        schedule_data[current_week][day][time_of_day].append(task)
        
        update_schedule()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Hàm sửa công việc
def edit_task():
    task = task_entry.get()
    if task != "":
        day = day_var.get()
        time_of_day = time_of_day_var.get()

        selected_index = schedule_listboxes[day][time_of_day].curselection()
        if selected_index:
            selected_task = schedule_listboxes[day][time_of_day].get(selected_index)
            schedule_listboxes[day][time_of_day].delete(selected_index)
            schedule_data[current_week][day][time_of_day].remove(selected_task)
            schedule_data[current_week][day][time_of_day].append(task)
            update_schedule()
            task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")
    else:
        messagebox.showwarning("Input Error", "Please enter a task to edit.")

# Hàm xóa công việc
# Hàm xóa công việc chỉ cần gõ "delete"
def delete_task():
    task = task_entry.get().lower()  # Chuyển chữ thành chữ thường để so sánh dễ dàng hơn
    if task == "delete":
        day = day_var.get()
        time_of_day = time_of_day_var.get()

        # Kiểm tra và xóa tất cả các công việc trong ca được chọn
        if current_week in schedule_data and day in schedule_data[current_week]:
            if time_of_day in schedule_data[current_week][day]:
                tasks_to_delete = schedule_data[current_week][day][time_of_day]
                if tasks_to_delete:  # Nếu có công việc trong ca
                    schedule_listboxes[day][time_of_day].delete(0, tk.END)  # Xóa các công việc hiển thị
                    schedule_data[current_week][day][time_of_day] = []  # Xóa công việc trong schedule_data
                    update_schedule()  # Cập nhật lại giao diện
                else:
                    messagebox.showwarning("No Tasks", "There are no tasks to delete.")
            else:
                messagebox.showwarning("Invalid Time Slot", "No tasks found for the selected time.")
        else:
            messagebox.showwarning("Invalid Day", "No tasks found for the selected day.")
    else:
        messagebox.showwarning("Input Error", "Please type 'delete' to remove tasks.")

# Hàm tạo ảnh PNG của thời khóa biểu
def print_schedule():
    # Tạo một hình ảnh mới
    img = Image.new("RGB", (2400, 2000), color="white")  # Increased width to fit all 7 days horizontally
    draw = ImageDraw.Draw(img)

    # Cài đặt font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Tiêu đề
    draw.text((10, 10), f"Thời khóa biểu tuần {current_week}", font=font, fill="black")

    # Vẽ thời khóa biểu
    y_offset = 40  # Start a bit lower for the first day
    x_offset = 10  # Start drawing from the left

    for i, day in enumerate(week_days):
        # Vẽ tên ngày và ngày tháng năm theo chiều ngang
        day_date_text = f"{day} ({get_day_of_week(i, start_of_week)})"
        draw.text((x_offset, y_offset), day_date_text, font=font, fill="black")
        x_offset += 200  # Space out the days horizontally (adjust width as needed)

        # If the x_offset exceeds the image width, move to the next row
        if x_offset > 1200:
            x_offset = 10
            y_offset += 100  # Move down to the next row after Friday

        # Vẽ các ca (sáng, chiều, tối)
        for time_of_day in ["sáng", "chiều", "tối"]:
            tasks = schedule_data.get(current_week, {}).get(day, {}).get(time_of_day, [])
            tasks_str = "\n".join(tasks) if tasks else "No tasks"
            draw.text((x_offset, y_offset), f"{time_of_day.capitalize()}: {tasks_str}", font=font, fill="black")
            y_offset += 60  # Move down after each time of day

        # Reset x_offset for the next day and start a new row
        x_offset = 10

    # Tạo tên tệp dựa trên tuần hiện tại
    filename = f"schedule_{current_week}.png"
    
    # Lưu ảnh thành file PNG
    img.save(filename)
    messagebox.showinfo("Success", f"Schedule has been printed to {filename}")

    # Tạo tên tệp dựa trên tuần hiện tại
    filename = f"schedule_{current_week}.png"
    
    # Lưu ảnh thành file PNG
    img.save(filename)
    messagebox.showinfo("Success", f"Schedule has been printed to {filename}")


    # Tạo tên tệp dựa trên tuần hiện tại
    filename = f"schedule_{current_week}.png"
    
    # Lưu ảnh thành file PNG
    img.save(filename)
    messagebox.showinfo("Success", f"Schedule has been printed to {filename}")


# Cập nhật ngày tháng hiện tại
def update_date():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    date_label.config(text=f"TODAY: {current_date}")

# Cập nhật thời khóa biểu
def update_schedule():
    # Clear các danh sách công việc hiện tại
    for day in week_days:
        for time_of_day in ["sáng", "chiều", "tối"]:
            schedule_listboxes[day][time_of_day].delete(0, tk.END)
            # Thêm lại các công việc cho mỗi ca
            if current_week in schedule_data and day in schedule_data[current_week]:
                if time_of_day in schedule_data[current_week][day]:
                    for task in schedule_data[current_week][day][time_of_day]:
                        schedule_listboxes[day][time_of_day].insert(tk.END, task)

# Tính toán ngày cho từng ngày trong tuần
def get_day_of_week(offset, start_date):
    day_of_week = start_date + timedelta(days=offset)
    return day_of_week.strftime("%d-%m-%Y")

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Quản lý thời khóa biểu tuần")

# Hiển thị ngày tháng
date_label = tk.Label(window, text="", font=("Helvetica", 14))
date_label.grid(row=0, column=0, columnspan=7, pady=10)
update_date()

# Nhập công việc
task_label = tk.Label(window, text="Nhập công việc:")
task_label.grid(row=1, column=0, columnspan=7, pady=5)

task_entry = tk.Entry(window, width=40)
task_entry.grid(row=2, column=0, columnspan=7, pady=5)

# Lựa chọn ngày và ca
day_var = tk.StringVar(window)
time_of_day_var = tk.StringVar(window)

# Thêm lựa chọn ngày và ca
frame_day_time = tk.Frame(window)
frame_day_time.grid(row=3, column=0, columnspan=7, pady=10)

day_label = tk.Label(frame_day_time, text="Chọn ngày:")
day_label.grid(row=0, column=0, padx=5)

day_menu = tk.OptionMenu(frame_day_time, day_var, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
day_menu.grid(row=0, column=1, padx=5)

time_of_day_label = tk.Label(frame_day_time, text="Chọn ca:")
time_of_day_label.grid(row=0, column=2, padx=5)

time_of_day_menu = tk.OptionMenu(frame_day_time, time_of_day_var, "sáng", "chiều", "tối")
time_of_day_menu.grid(row=0, column=3, padx=5)

# Tạo khung cho các nút Thêm, Sửa, Xóa
frame_buttons = tk.Frame(window)
frame_buttons.grid(row=4, column=0, columnspan=7, pady=10)

# Nút thêm, sửa, xóa công việc và căn chỉnh sang bên phải
add_button = tk.Button(frame_buttons, text="Thêm công việc", width=15, command=add_task)
add_button.grid(row=0, column=0, padx=5)

edit_button = tk.Button(frame_buttons, text="Sửa công việc", width=15, command=edit_task)
edit_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(frame_buttons, text="Xóa công việc", width=15, command=delete_task)
delete_button.grid(row=0, column=2, padx=5)

# Nút Print
print_button = tk.Button(window, text="Print Schedule", width=20, command=print_schedule)
print_button.grid(row=6, column=0, columnspan=7, pady=10)

# Lịch các ngày trong tuần (Monday-Sunday)
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
schedule_listboxes = {}

# Tạo khung thời khóa biểu cho cả tuần
frame_schedule = tk.Frame(window)
frame_schedule.grid(row=5, column=0, columnspan=7, pady=20)

# Tạo ngày bắt đầu cho tuần hiện tại (thứ 2)
start_of_week = datetime.today() - timedelta(days=datetime.today().weekday())  # Monday of the current week

# Tạo giao diện cho từng ngày trong tuần và từng ca (sáng, chiều, tối)
def create_schedule(start_of_week):
    for i, day in enumerate(week_days):
        frame_day = tk.Frame(frame_schedule)
        frame_day.grid(row=0, column=i, padx=10)
        
        day_label = tk.Label(frame_day, text=day, font=("Helvetica", 12))
        day_label.grid(row=0, column=0, pady=5)

        # Hiển thị ngày tháng năm dưới mỗi ngày
        day_date_label = tk.Label(frame_day, text=get_day_of_week(i, start_of_week), font=("Helvetica", 10))
        day_date_label.grid(row=1, column=0, pady=5)
        
        # Tạo listbox cho sáng, chiều, tối
        schedule_listboxes[day] = {}
        for j, time_of_day in enumerate(["sáng", "chiều", "tối"]):
            listbox = tk.Listbox(frame_day, width=20, height=5)
            listbox.grid(row=j+2, column=0, pady=5)
            schedule_listboxes[day][time_of_day] = listbox

# Tạo lịch cho tuần hiện tại
current_week = start_of_week.strftime("%Y-%U")  # Current week identifier (Year-WeekNumber)
create_schedule(start_of_week)

# Hàm để chuyển sang tuần tiếp theo
def next_week():
    global start_of_week, current_week
    start_of_week += timedelta(weeks=1)
    current_week = start_of_week.strftime("%Y-%U")
    
    # Cập nhật lại giao diện với lịch mới
    for widget in frame_schedule.winfo_children():
        widget.destroy()  # Xóa các widget cũ
    create_schedule(start_of_week)
    update_schedule()

# Hàm để quay lại tuần trước
def previous_week():
    global start_of_week, current_week
    start_of_week -= timedelta(weeks=1)
    current_week = start_of_week.strftime("%Y-%U")
    
    # Cập nhật lại giao diện với lịch mới
    for widget in frame_schedule.winfo_children():
        widget.destroy()  # Xóa các widget cũ
    create_schedule(start_of_week)
    update_schedule()

# Thêm nút chuyển sang tuần sau
next_week_button = tk.Button(window, text="BACK", width=20, command=previous_week)
next_week_button.grid(row=6, column=0, columnspan=3, pady=10)

# Thêm nút quay lại tuần trước
previous_week_button = tk.Button(window, text="NEXT", width=20, command=next_week)
previous_week_button.grid(row=6, column=3, columnspan=4, pady=10)

# Chạy giao diện
window.mainloop()

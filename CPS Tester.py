import customtkinter as ctk

root = ctk.CTk()

root.title("CPS Tester")

ctk.set_appearance_mode("dark")

screen_width = root.winfo_screenwidth()

screen_height = root.winfo_screenheight()

# Subtract task bar space

task_bar_height = 50

window_height = screen_height - task_bar_height

# Set geometry to full screen minus task bar

root.geometry(f"{screen_width}x{window_height}+0+0")

click_count = 0

game_active = False

timer = 20


def on_click():

    global click_count

    if game_active:

        click_count += 1

        click_label.configure(text=f"Clicks: {click_count}")


def update_timer():

    global timer, game_active, click_count

    if timer > 0 and game_active:

        timer -= 1

        timer_label.configure(text=f"Time: {timer}")

        root.after(1000, update_timer)  # Update every 1 second

    elif timer == 0:

        game_active = False

        button.configure(state="disabled")  # Disable button when time's up

        # Calculate and display CPS

        cps = click_count / 20

        cps_label.configure(text=f"CPS: {cps:.2f}")

        label.configure(
            text=f"Game Over!\nFinal Score: {click_count}\nCPS: {cps:.2f}"
        )


def start_game():

    global game_active, click_count, timer

    game_active = True

    click_count = 0

    timer = 20  # Reset timer

    start_button.destroy()

    click_label.configure(text="Clicks: 0")

    timer_label.configure(text="Time: 20")  # Show initial time

    cps_label.configure(text="CPS: 0.00")  # Reset CPS display

    button.configure(state="normal")

    update_timer()  # Start the timer


label = ctk.CTkLabel(
    root,
    text="CPS TESTER",
    font=("Arial", 30)
)

label.pack(pady=20)


label_2 = ctk.CTkLabel(
    root,
    text="Use this to test your cps or auto clicker strength.",
    font=("Arial", 16)
)

label_2.pack(pady=10)


click_label = ctk.CTkLabel(
    root,
    text="Press Start to Begin!",
    font=("Arial", 24)
)

click_label.pack(pady=20)


timer_label = ctk.CTkLabel(
    root,
    text="Time: 20",
    font=("Arial", 24)
)

timer_label.pack(pady=10)


cps_label = ctk.CTkLabel(
    root,
    text="CPS: 0.00",
    font=("Arial", 24)
)

cps_label.pack(pady=10)


start_button = ctk.CTkButton(
    root,
    text="START!",
    command=start_game,
    font=("Arial", 20),
    height=50,
    width=200
)

start_button.pack(pady=10)


button = ctk.CTkButton(
    root,
    text="CLICK ME!",
    command=on_click,
    font=("Arial", 20),
    height=200,
    width=300,
    state="disabled"
)

button.pack(pady=30)


root.mainloop()

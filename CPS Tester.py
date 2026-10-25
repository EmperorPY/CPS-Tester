import customtkinter as ctk  # Import the CustomTkinter library, aliased as ctk for modern-looking widgets

root = ctk.CTk()  # Create the main application window (the root window)
root.title("CPS Tester")  # Set the title text that appears in the window's title bar
ctk.set_appearance_mode("dark")  # Set the overall theme to dark mode (alternatives: "light", "system")

root.geometry("500x700+0+0")  # Set window size and position: full width, adjusted height, at top-left corner

click_count = 0  # Global counter tracking how many times the user has clicked during the test
game_active = False  # Global flag indicating whether a test is currently in progress (clicks only count when True)
timer = 20  # Global countdown value, counts down from test_duration to 0 during a test
test_duration = 20  # The total length of the test in seconds, set from the entry field when the game starts


def on_click():
    # Handler called every time the big "CLICK ME!" button is pressed
    global click_count  # Declare global so we modify the module-level click_count
    if game_active:  # Only count clicks if a test is currently running
        click_count += 1  # Increment the click counter
        click_label.configure(text=f"Clicks: {click_count}")  # Update the label showing the live click count


def update_timer():
    # Recursive function that runs once per second to count down the timer
    global timer, game_active, click_count  # Declare globals we modify within this function
    if timer > 0 and game_active:  # If time remains and the game is still active
        timer -= 1  # Decrease the remaining time by one second
        timer_label.configure(text=f"Time: {timer}")  # Update the timer label with the new remaining time
        root.after(1000, update_timer)  # Schedule this same function to run again after 1000 ms (1 second)
    elif timer == 0:  # If the timer has reached zero, end the test
        game_active = False  # Mark the game as inactive so clicks stop counting
        button.configure(state="disabled")  # Disable the click button since the test is over
        cps = click_count / test_duration  # Calculate clicks per second by dividing total clicks by test length
        cps_label.configure(text=f"CPS: {cps:.2f}")  # Display the CPS result formatted to two decimal places
        label.configure(
            text=f"Game Over!\nFinal Score: {click_count}\nCPS: {cps:.2f}"
        )  # Update the main title label to show the final results


def start_game():
    # Handler called when the user presses the "START!" button
    global game_active, click_count, timer, test_duration  # Declare globals we modify within this function

    # Read the time the user entered
    try:  # Attempt to read and validate the entry value
        test_duration = int(timer_input.get())  # Convert the entry text to an integer (seconds)
        if test_duration <= 0:  # Reject zero or negative durations
            raise ValueError  # Raise an error to be caught by the except block below
    except ValueError:  # If conversion fails or value is invalid
        label.configure(text="Please enter a valid positive number of seconds!", wraplength=300) # Show an error message to the user
        return  # Exit the function early so the game doesn't start

    game_active = True  # Mark the game as active so clicks will be counted
    click_count = 0  # Reset the click counter to zero
    timer = test_duration  # Set the countdown timer to the chosen test duration

    start_button.destroy()  # Remove the start button so it can't be pressed again mid-test
    timer_input.configure(state="disabled")  # Disable the entry field so duration can't change mid-test

    click_label.configure(text="Clicks: 0")  # Reset the click count display
    timer_label.configure(text=f"Time: {timer}")  # Show the initial remaining time
    cps_label.configure(text="CPS: 0.00")  # Reset the CPS display

    button.configure(state="normal")  # Enable the click button now that the test has begun
    update_timer()  # Kick off the countdown loop


label = ctk.CTkLabel(root, text="CPS TESTER", font=("Arial", 30))  # Main title label at the top of the window
label.pack(pady=20)  # Place the title label with 20px vertical padding

label_2 = ctk.CTkLabel(
    root,
    text="Use this to test your cps or auto clicker strength.",
    font=("Arial", 16)
)  # Subtitle/instruction label explaining the purpose of the app
label_2.pack(pady=10)  # Place the subtitle with 10px vertical padding

click_label = ctk.CTkLabel(
    root,
    text="Press Start to Begin!",
    font=("Arial", 24)
)  # Label showing the live click count (starts as an instruction)
click_label.pack(pady=20)  # Place the click count label with 20px vertical padding

timer_input = ctk.CTkEntry(
    root,
    placeholder_text="Enter time for testing (s):",
    font=("Arial", 24),
    width=300
)  # Text entry field where the user types the desired test duration in seconds
timer_input.pack(pady=10)  # Place the entry field with 10px vertical padding

timer_label = ctk.CTkLabel(root, text="Time:", font=("Arial", 24))  # Label showing the remaining time countdown
timer_label.pack(pady=10)  # Place the timer label with 10px vertical padding

cps_label = ctk.CTkLabel(root, text="CPS: 0.00", font=("Arial", 24))  # Label showing the calculated clicks-per-second result
cps_label.pack(pady=10)  # Place the CPS label with 10px vertical padding

start_button = ctk.CTkButton(
    root,
    text="START!",
    command=start_game,
    font=("Arial", 20),
    height=50,
    width=200
)  # Button that begins the test when pressed, calling start_game
start_button.pack(pady=10)  # Place the start button with 10px vertical padding

button = ctk.CTkButton(
    root,
    text="CLICK ME!",
    command=on_click,
    font=("Arial", 20),
    height=270,
    width=300,
    state="disabled"
)  # The big button the user repeatedly clicks during the test (starts disabled)
button.pack(pady=30)  # Place the click button with 30px vertical padding

root.mainloop()  # Start the Tkinter event loop, keeping the window open and responsive

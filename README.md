# Phantom | FiveM Trigger Finder

Phantom is a tool to analyze FiveM resource files for triggers, webhooks, and obfuscated code by categories and outputting the data into categorized files. Our tool also includes an automatic updater to ensure the tool stays up to date.

## Features

- **Trigger Detection:** Our tool searches for triggers in `.lua` files (e.g., `RegisterNetEvent`, `TriggerServerEvent`, `TriggerClientEvent`).
- **Categorization:** Our tool organizes detected triggers into categories (e.g., Robbery, Police, Money, Drugs, etc.).
- **Custom Events & Strings:** Our tool allows you to include additional events and custom strings for scanning.
- **Webhook & Obfuscation Scan:** Our tool detects webhook URLs and potential obfuscated code within files.
- **Simple GUI:** Our tool has an easy to use GUI for selecting folders and configuring scan options.
- **Automatic Updates:** Our tool stays always updated to our newest release by checking each time you run our tool.

## Requirements

- **Python 3.10.5**  
  Make sure to add Python to your path and disable path limit.
  
## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/astrapy/FiveM-Trigger-Finder.git
   ```

2. **Navigate to the Path:**

   ```bash
   cd FiveM-Trigger-Finder
   ```

3. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Tool:**

   Open CMD and run the program by typing:

   ```bash
   python main.py
   ```

2. **Usage:**

   - **Select Folder:** Click the "Select Folder" button to choose the directory containing the FiveM files.
   - **Scan Additional Events:** You can include or exclude scanning of additional events like `AddEventHandler` or `RegisterNetEvent`.
   - **Custom Strings:** Input additional custom strings or event names (comma-separated) you want to search for.
   - **Start Scan:** Click the "Start Scan" button to begin analyzing the selected folder.

3. **Output:**
   
   - **JSON Files:** Detailed results of the webhook URLs and obfuscated code detections.
   - **Lua Files:** Categorized in the `output/<...>/triggers` directory.
   - **Custom Strings File:** If custom strings were given, we will create a JSON file under `output/customstrings`.

## Suggestions

For any suggestions, feedback, or support, join our Discord server: [discord.gg/phantomai](https://discord.gg/phantomai)

## License

Phantom Software License Agreement

Copyright (c) [Year] [Your Name or Organization]

This software is provided for personal and non-commercial use only. By using this software, you agree to the following terms:

1. **No Modification** – You are NOT allowed to modify, or alter this software in any way.
2. **No Redistribution or Rebranding** – You may NOT sell, redistribute, or rebrand this software under any other name.
3. **Non-Commercial Use Only** – You may NOT use this software for any commercial purposes or financial gain.
4. **Ownership** – This software remains the property of [astrapy].
   
If you still think to sell it your gay

## Disclaimer

Phantom is for educational purposes only. We are not responsible for any misuse or consequences arising from its use. Use at your own risk.

## Preview
![image](https://cdn.discordapp.com/attachments/1349281052585365596/1349390251679809627/image.png?ex=67d2ed1a&is=67d19b9a&hm=f9d87abaf6baeea5f65b552561e125f4c955efd6def1da36dd3d85e2b2f821a0&)

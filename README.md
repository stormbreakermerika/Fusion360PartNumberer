# Fusion 360 Numberer Script

## Overview

This Fusion 360 script automates the process of generating STL files for parts with sequentially numbered text extrusions. It creates a custom command within Fusion 360, allowing you to add numbered text to a body and export each body as an STL file.

## Features

- Adds a custom command to Fusion 360's UI.
- Allows you to generate numbered text extrusions on a selected body.
- Exports each numbered body as an STL file to a specified directory.

## Installation

1. **Download and Install Fusion 360 API Scripts**:
   - Open Fusion 360.
   - Go to the "Scripts and Add-Ins" dialog (`Tools > Scripts and Add-Ins`).
   - Click the "Add-Ins" tab, then click "Create" to create a new script.
   - Copy and paste the provided script into the new script file.

2. **Run the Script**:
   - In the "Scripts and Add-Ins" dialog, find the script under "My Scripts".
   - Click "Run" to execute the script.

## Script Details

### Imports

The script uses the following Python modules:

- `os`: For file path operations.
- `adsk.core`, `adsk.fusion`, `adsk.cam`: Fusion 360 API modules.
- `traceback`: For error handling.

### Command Created Handler

`NumbererCommandCreatedHandler` handles the creation of a custom command in Fusion 360. It adds a string input for specifying the starting number.

### `create_text_sketch` Function

Creates a text sketch on the specified plane with the given text, position, and size. Uses Fusion 360’s sketch text API to generate the text.

### `run` Function

1. **Command Definition**:
   - Checks if the custom command (`Numberer`) already exists.
   - If not, creates a new button definition for it.
   - Attaches the `NumbererCommandCreatedHandler` to handle command creation.

2. **Body Duplication and Text Extrusion**:
   - Retrieves the root component and body to be duplicated.
   - Creates new components and adds numbered text extrusions to each.
   - Exports each body as an STL file to a directory specified by the script’s location.

3. **Cleanup**:
   - Deletes the temporary components and sketches to maintain a clean design environment.

### Error Handling

Includes basic error handling to catch and display any issues encountered during execution.

## Example Usage

1. **Add Command**: Add the command to Fusion 360 through the "Scripts and Add-Ins" dialog.
2. **Execute Command**: Run the command from the Fusion 360 toolbar or menu to start the process of generating STL files.

## Troubleshooting

- **Command Not Visible**: Ensure that the script is correctly installed and that Fusion 360 is restarted.
- **Error Messages**: Check the message box in Fusion 360 for details. Use the traceback to diagnose issues.

## License

This script is provided as-is. Use it at your own risk. The author is not responsible for any issues that arise from its use.

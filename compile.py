import os
import subprocess
import sys

def compile_to_exe(source_file):
    if not os.path.isfile(source_file):
        print("Error: File not found!")
        return
    
    print(f"Compiling {source_file} to .exe ...")
    
    # PyInstaller command with --noconsole to hide the black window
    command = [
        "pyinstaller",
        "--onefile",      # creates a single .exe file
        "--noconsole",    # hides the console window (GUI apps only)
        "--clean",        # clean PyInstaller cache before building
        source_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print("\n✔ Compilation successful!")
        print("Your EXE is located inside the 'dist' folder.")
        print("The annoying black console window is now GONE! 🎉")
    except subprocess.CalledProcessError:
        print("\n❌ Compilation failed. Check for errors in your script.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compile.py <your_script.py>")
    else:
        compile_to_exe(sys.argv[1])

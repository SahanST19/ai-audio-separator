import os
import subprocess
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("========================================")
    print("      MY AUDIO SEPARATOR TOOL           ")
    print("========================================")
    
    # 1. Ask for song name
    song_name = input("\n[?] Enter the song name (e.g., song.mp3): ").strip() # Removes accidental spaces

    # Check if song file exists
    if not os.path.exists(song_name):
        print(f"\n[Error] File '{song_name}' not found inside this folder!")
        return

    # 2. Setup FFmpeg Path (Absolute Path)
    # Get current folder path
    current_dir = os.getcwd()
    # Path to our 'bin' folder
    bin_path = os.path.join(current_dir, "bin")

    # Check if ffmpeg exists in bin
    ffmpeg_exe = os.path.join(bin_path, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        print(f"\n[Error] FFmpeg not found in 'bin' folder!")
        print(f"Please move all FFmpeg files into: {bin_path}")
        return

    # Add 'bin' folder to system PATH for this run
    os.environ["PATH"] += os.pathsep + bin_path

    print(f"\n[Processing] Separating '{song_name}'...")
    print("Please wait, this might take about a minute...\n")

    # 3. Run Demucs
    try:
        # Using subprocess with the modified environment
        command = f'demucs -n htdemucs --two-stems=vocals "{song_name}"'
        subprocess.run(command, shell=True, check=True, env=os.environ)
        
        print("\n========================================")
        print("✅ Success! Separation complete.")
        folder_name = song_name.rsplit(".", 1)[0]
        print(f"📁 Output Path: separated/htdemucs/{folder_name}")
        print("========================================")
        
    except subprocess.CalledProcessError:
        print("\n[Error] Separation failed. Check the error message above.")

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup

# Your Genius API access token here
GENIUS_ACCESS_TOKEN = "RW7dPZWcWUJ5bRWhn20hy9SVZZBpZKYb4Y2nr2L5dESkB0eRTbp34X-_tO7ZQ4K5"

def get_song_url(artist, title):
    base_url = "https://api.genius.com/search"
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    params = {'q': f"{artist} {title}"}

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    hits = data['response']['hits']
    if hits:
        # Return the first song url
        return hits[0]['result']['url']
    return None

def scrape_lyrics(song_url):
    page = requests.get(song_url)
    if page.status_code != 200:
        return None

    soup = BeautifulSoup(page.text, 'html.parser')

    # Genius lyrics are inside a div with data-lyrics-container="true"
    lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    if not lyrics_divs:
        # fallback to old div class (sometimes changes)
        lyrics_div = soup.find("div", class_="lyrics")
        if lyrics_div:
            return lyrics_div.get_text(separator="\n").strip()
        return None

    lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
    return lyrics

def fetch_lyrics():
    artist = artist_entry.get().strip()
    title = song_entry.get().strip()

    if not artist or not title:
        messagebox.showwarning("Input Error", "Please enter both artist and song title.")
        return

    lyrics_text.delete("1.0", tk.END)
    lyrics_text.insert(tk.END, "Searching for the song...\n")

    song_url = get_song_url(artist, title)
    if not song_url:
        lyrics_text.delete("1.0", tk.END)
        messagebox.showerror("Not Found", "Song not found on Genius.")
        return

    lyrics_text.insert(tk.END, f"Found song URL: {song_url}\nFetching lyrics...\n")

    lyrics = scrape_lyrics(song_url)
    if not lyrics:
        lyrics_text.delete("1.0", tk.END)
        messagebox.showerror("Error", "Lyrics not found or unable to scrape lyrics.")
        return

    lyrics_text.delete("1.0", tk.END)
    lyrics_text.insert(tk.END, lyrics)

# GUI Setup
root = tk.Tk()
root.title("Genius Lyrics Extractor")
root.geometry("700x700")
root.configure(bg="#121212")

# Artist Name
tk.Label(root, text="Artist Name:", bg="#121212", fg="white", font=("Arial", 12)).pack(pady=5)
artist_entry = tk.Entry(root, width=60)
artist_entry.pack(pady=5)

# Song Title
tk.Label(root, text="Song Title:", bg="#121212", fg="white", font=("Arial", 12)).pack(pady=5)
song_entry = tk.Entry(root, width=60)
song_entry.pack(pady=5)

# Get Lyrics Button
tk.Button(root, text="Get Lyrics", command=fetch_lyrics, bg="#1DB954", fg="white", font=("Arial", 12)).pack(pady=10)

# Lyrics Output
lyrics_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30, bg="#1e1e1e", fg="white", font=("Courier", 10))
lyrics_text.pack(pady=10)

root.mainloop()

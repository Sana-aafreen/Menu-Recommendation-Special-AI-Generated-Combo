import requests
URL = "https://script.google.com/macros/s/AKfycbziwt_310-tDnkzPTpgbgW89M6jxjDXQVbRIn7k-JzBiezCzoDcjhPjDDbZDjVrLf4N5w/exec"

with open("probe_log.txt", "w", encoding="utf-8") as f:
    try:
        f.write(f"Fetching: {URL}\n")
        res = requests.get(URL, allow_redirects=True)
        f.write(f"Status: {res.status_code}\n")
        f.write(f"URL: {res.url}\n") 
        f.write(f"First 500 chars: {res.text[:500]}\n")
        
        try:
            data = res.json()
            f.write("JSON Parse: SUCCESS\n")
            f.write(f"Keys: {list(data.keys())}\n")
        except Exception as e:
            f.write(f"JSON Parse: FAILED - {e}\n")
    except Exception as e:
        f.write(f"Request Failed: {e}\n")

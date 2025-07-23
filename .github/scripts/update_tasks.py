# Tüm repolardaki TASKS.md'leri tarar
def sync_status():
    for repo in ["core", "signal"]:
        with open(f"{repo}/TASKS.md") as f:
            print(f"### {repo} Son Durum")
            print(f.read())

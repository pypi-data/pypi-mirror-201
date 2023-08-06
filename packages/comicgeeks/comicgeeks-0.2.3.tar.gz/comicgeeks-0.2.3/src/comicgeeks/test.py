from Comic_Geeks import Comic_Geeks

client = Comic_Geeks()

isu = client.issue_info(6650558)

print(isu.json())

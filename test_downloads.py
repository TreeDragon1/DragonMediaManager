from core.dragon_downloads import DragonDownloads

dragon = DragonDownloads()

data = dragon.get_statistics()

print(data)
mkdir "%PROGRAMDATA%\WallpaperEngineLiveWeather"
copy /y "WallpaperEngineLiveWeather.exe" "%PROGRAMDATA%\WallpaperEngineLiveWeather\WallpaperEngineLiveWeather.exe"
echo n | copy /-y "config_sample.json" "%PROGRAMDATA%\WallpaperEngineLiveWeather\config.json"
schtasks /create /sc DAILY /tn "WallpaperEngineLiveWeather" /tr "%PROGRAMDATA%\WallpaperEngineLiveWeather\WallpaperEngineLiveWeather.exe" /du 24:00 /ri 60 /it /f
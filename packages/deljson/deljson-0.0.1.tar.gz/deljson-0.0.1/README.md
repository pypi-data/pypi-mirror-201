# deljson
用於刪除json值

# 安裝
```
pip install deljson
```

## 範例
```py
import deljson
data={"name":"hans","year":2023}
a=deljson.start(["name"])
print(a)
#{"year":2023}
```
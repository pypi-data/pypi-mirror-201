## 簡介

`to_pip.sh` 是一個簡單的 bash 腳本，可以將 Python 程式打包成 pip 可以安裝的套件並上傳至 PyPI。使用者只需要提供套件名稱、版本號和 Python 程式檔案，腳本就會幫忙打包並上傳至 PyPI。

## 使用方法

執行以下指令以顯示使用方法：

```
$ ./to_pip.sh -h
Usage: ./to_pip.sh -n <package_name> -v <package_version> [-u <pypi_username> -p <pypi_password>] <python_files>
```

必要參數：
- `-n` : 套件名稱
- `-v` : 套件版本號
- `<python_files>` : Python 程式檔案

選用參數：
- `-u` : PyPI 帳號
- `-p` : PyPI 密碼

範例：
```
$ ./to_pip.sh -n my_package -v 1.0.0 script1.py script2.py
```
此指令會將 `script1.py` 和 `script2.py` 打包成名為 `my_package`、版本為 `1.0.0` 的套件。

若有 PyPI 帳號和密碼，可以使用 `-u` 和 `-p` 參數上傳套件：
```
$ ./to_pip.sh -n my_package -v 1.0.0 -u my_username -p my_password script1.py script2.py
```

## 說明

腳本會做以下事情：

1. 創建一個臨時目錄，並將 Python 程式複製到目錄中。
2. 如果有 `requirements.txt` 檔案，則複製到目錄中。
3. 創建 `setup.py` 檔案。
4. 如果有 `README.md` 檔案，則複製到目錄中，並在 `setup.py` 檔案中將其作為專案說明。
5. 使用 `setup.py` 檔案建立套件。
6. 如果提供了 PyPI 帳號和密碼，則在本機建立 `.pypirc` 檔案以進行身份驗證。
7. 上傳套件到 PyPI。

## 注意事項

- 預設使用 `twine` 上傳套件到 PyPI，請先確認已安裝 `twine`。
- Python 程式檔案中必須包含 `main()` 函數，並且可以使用 `argparse` 進行參數解析。
- 腳本中的 PyPI 上傳方式只適用於使用 `username` 和 `password` 進行身份驗證的情況。如果您使用其他身份驗證方式，請自行修改腳本。
- 請務必確認套件名稱和版本號是正確的，否則上傳可能會失敗。

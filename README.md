# 使い方
```bash
# 結合テスト仕様書作成(全て)
poetry run python create_integrated_test.py
# 結合テスト仕様書作成(指定)
poetry run python create_integrated_test.py "【画面】ログイン"

# スケジュール作成
poetry run python create_schedule.py "yyyy-mm-dd" "yyyy-mm-dd"

# 単体テスト
python -m unittest tests.{module_name}
```

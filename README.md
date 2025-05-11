# 使い方
## スケジュール
```bash
cp ./storage/schedule_config/メンバー.yml.example ./storage/schedule_config/メンバー.yml
cp ./storage/schedule_config/休日.yml.example ./storage/schedule_config/休日.yml
cp ./storage/schedule_config/施策.yml.example ./storage/schedule_config/施策.yml

# 案件のスケジュールファイルを作成して内容を埋めていく
cp ./storage/schedule/案件名.yml.example ./storage/schedule/案件名.yml
```
## テストケース
```bash
# テスト観点の共通設定を作成
cp ./storage/integrated_test/view_config/テスト観点.yml.example ./storage/integrated_test/view_config/テスト観点.yml

# テストケースの共通設定を作成
cp ./storage/integrated_test/view_config/共通.yml.example ./storage/integrated_test/view_config/共通.yml

# その後 ./storage/integrated_test にテストケースを作成していく
```

# チートシート
```bash
# 結合テスト仕様書作成(全て)
poetry run python create_integrated_test.py
# 結合テスト仕様書作成(指定)
poetry run python create_integrated_test.py "【画面】ログイン"

# スケジュール作成
# 引数は開始日と終了日
poetry run python create_schedule.py yyyy-mm-dd yyyy-mm-dd

# 単体テスト
python -m unittest tests.{module_name}
```

# 研究室向け業績アーカイブ
## 特徴
- 筆頭著者ごとに業績を表示
- タグによる管理
- bibtexを含む多様な表示形式
- docker-composeによる起動(https://github.com/yamaken1343/gyoseki-docker )

## Requirements
- Python3
- Django

## Quick Start
```
# Download
git clone https://github.com/yamaken1343/gyoseki-archive
cd gyoseki-archive

# Install requirements
pip3 install -r requirements.txt

# Initialzie django and create superuser
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

# Up
python3 manage.py runserver 0.0.0.0:8001

# Access on http://localhost:8001
```
起動後, 管理者ページ(http://localuost:8001/admin/ )にアクセスして
- Authors (筆頭著者)
- divisions (業績区分: 学術論文, 学位論文, 学会 等)
- languages (言語)

を追加してください

## マニュアルの追加
マニュアルページにPDFを置くことが可能です.
  
`gyoseki-archive/gyoseki/static`にそれぞれ
- `user.pdf` (ユーザ向け)
- `admin.pdf` (管理者向け)
- `register.pdf` (登録時にルールがある場合に)

という名前で保存してください

## メール通知
業績登録時に管理者へメール通知が可能です.  
`gyoseki_beta/settings.py`および`gyoseki_beta/settings_production.py`の`EMAIL_`から始まる行に適切な値を入れた上で,   
`register@gyoseki/views.py`の`mail(s, m)`についているコメントアウトを外してください.

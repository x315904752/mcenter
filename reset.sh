rm -rf account/account
rm -rf account/cmdb
rm -rf account/procedures
rm -rf account/procedure
python manage.py makemigrations --empty account
python manage.py makemigrations --empty procedure
python manage.py makemigrations --empty procedures
python manage.py makemigrations --empty cmdb
python manage.py makemigrations 
python manage.py  migrate


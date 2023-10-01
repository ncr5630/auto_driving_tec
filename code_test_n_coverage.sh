virtualenv venv_test -p /usr/bin/python3;
. venv_test/bin/activate;
python -m pip install -r test-requirements.txt;

coverage run -m \
    pytest gic_auto_driving/test_app.py

coverage html -i \
    gic_auto_driving/*.py;

coverage xml -i \
    gic_auto_driving/*.py;

mkdir -p coverage_reports_xml;
mv coverage.xml coverage_reports_xml;
deactivate;

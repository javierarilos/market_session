# market_session

## transform session files to numpy array in pickle file
```bash
echo transform_session for only one instrument: F:FESXU4
python transform_session.py --out numpy --instrument F:FESXU4 f_mupssan20140901.log
```

```bash
echo transform_session for the complete session. result is too large.
python transform_session.py --out numpy f_mupssan20140901.log f_mupssan20140902.log
```

## installing
Base requirements: `python-2.7`, `pip`, `virtualenv`.


```bash
echo this are the installation instructions for ubuntu
sudo apt-get install -y python-dev

pip install -r requirements.txt
```

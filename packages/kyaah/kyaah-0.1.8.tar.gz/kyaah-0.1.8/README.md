
# Kyaah

Kyaah abstract away cognitive over-head of sending SMTP mail, together with other mailing operations things like, mail with file, tokens etc.

# Simple use of kyaah
First we recommend creating a virtual environment `python3 -m venv venv` and then activate it `source venv/bin/activate`

Once that finish now install the library using

```
pip install kyaah
```

Wait for the installation to finish, basically the library was uploaded using `sdist` (Source Distribution). After that create a new file let call it `test.py` in the file paste the below code with your credentials.

```python
import kyaah
            
sender = "my_email@gmail.com"
receiver = ["receiver_1@gmail.com", "receiver_2@gmail.com"]
passwd = "*********" # use app password

server = "gmail"
subj = f"Hellow world!"
body = "Lorem ipsum dolor sit amet adipisicing elit, rerum voluptate ipsum volupt."

kyaah.sendMail(from_usr=sender, to_usr=receiver, svr=server, subject=subj, body=body, mail_passwd=passwd)
```

save the file and navigate to where the file is located in terminal and your are ready to go (run the file)

```
python3 test.py
```

See more documentations <a href="https://kyaah.readthedocs.io">here!</a>

## Useful links

- Documentation: https://kyaah.readthedocs.io
- Repository: https://github.com/usmanmusa1920/kyaah

Pull requests are welcome

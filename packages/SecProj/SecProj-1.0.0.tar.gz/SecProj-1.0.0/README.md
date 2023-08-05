# secproj
# Description
Simple tools to help you secure your projects in a more simple manner, allowing for simple and secure development.
The purpose of this project is to allow developers to simplify the boilerplate code necessary to create secure projects.
This would encourage and promote secure coding practices and produce more safe code across several platforms.
The code safely encrypts variables using cryptography.Fernet(), which uses AES in CBC mode with a 128-bit key and PKC57 padding.
The encryption and decryption key is stored in your project under the /data/ folder as enc.key.
The variables are stored in a standard .env file that is also stored in the same folder.
There is a template .gitignore file that can be used to overwrite or simply create the default .gitignore for your project.
This default template contains exceptions for both files, which enforces the standard that neither should be uploaded to git.
Instead, to migrate or share a project one should securely share these two files which can be dropped into the /data folder
giving the new host access to decrypt these variables and run as per normal. The concept of not having access to the information
with the additional encryption of the information being stored on the hard drive creates two layers of security when coding.

Of course all of this is for nothing if your systems are breached and these files get copied because then the values can be decrypted.
It is up to each person using these tools to secure the key and env files accordingly.

The gitignore overwrite is disabled by default because it can create a nuisance for developers but it can easily be enabled.
# Dependencies
This code is very simple and only has two dependencies, cryptography and python-dotenv.
# Installation
```
pip install secproj
```
# Usage
## Create Encrypted Variables
NOTE: _You can signal which part of a string you want encrypted by wrapping it in $$$, or you can just encrypt the whole string by not wrapping it._
```
import secproj.core as sp

sec = sp.Secure()
# Encrypting only a portion of a string.
sec.set_var("TEST1","THIS $$$IS A$$$ TEST!")
# Encrypting the full string.
sec.set_var("TEST2","THIS IS A TEST!")

```
## Reading Encrypted Variables
NOTE: _Assuming we are reading the encrypted variables we created above, lets read the value of TEST1._
```
import secproj.core as sp

sec = sp.Secure()
# Reading Encrypted TEST1 into tmp.
tmp = sec.get_var("TEST1")
print(tmp)
```
## Enabling the Automatic Overwrite of .gitignore
```
import secproj.core as sp

sec = sp.Secure(gitignore_overwrite=True)
# Encrypting only a portion of a string.
sec.set_var("TEST1","THIS $$$IS A$$$ TEST!")
# Encrypting the full string.
sec.set_var("TEST2","THIS IS A TEST!")
# Reading Encrypted variable "TEST1" into tmp.
tmp = sec.get_var("TEST1")
print(tmp)
```